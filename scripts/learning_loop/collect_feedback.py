#!/usr/bin/env python3
"""Nightly feedback collector: transcripts -> one daily feedback log -> the learnings register.

Why: closeout Learnings/Concerns/Policy/Decisions fields, Brian's corrections and
friction agents mention in passing reached no log unless an agent ran the
`learned` skill by hand (Brian approved this collector 2026-10-06). The learning
loop's input contract is the learnings register (docs/failure-modes.md,
"Accepted inputs and maintenance contract"); this script feeds it.

Steps, each timed and counted in the printed summary and in runs.jsonl:
  1. read   new bytes of every Claude Code and Codex transcript changed since the
            last run (byte offsets in state.sqlite; first run: --since-days)
  2. closeouts  the four fields under fixed bold headings, parsed with code
  3. extract    Brian's corrections, friction and in-passing learnings in
                interactive sessions, by the light LLM through llm_client
                (structured output; a quote not found verbatim is dropped)
  4. triage     each item -> learning/friction/correction/concern/noise with
                Jev (llm_client.call_decisions)
  5. covered    annotation only: nearest register entry by word overlap, then
                Jev's probability that it already states the item. Never used
                to drop an item until it is measured on a labeled sample.
  6. write      one JSON line per item to items-<date>.jsonl
  7. file       learning/friction/correction items Jev is sure of go to the
                legacy register through project-meta/scripts/log_learning.py, only
                with --file --legacy-register (off since 2026-10-08: the register is
                legacy; AES issue #242)
  R. reports    each closeout Feedback (or older Learnings) field becomes one
                feedback-report.v1 report: marked lines parsed by records.py, free
                text split by the light model (links always read by code), filed as
                one issue in the private log FEEDBACK_LOG_REPO with --file
                (plan proposals/aes-learning-loop, slice S1)

Privacy: transcript text goes only to OpenRouter through llm_client and to the
local output folder; nothing here is committed anywhere. Exit 0 = clean, 1 = some
LLM/Jev/filing calls failed (counted; their files are re-read next run), 2 =
crashed. Any non-zero exit opens a keyed agent concern via notify_operator.py.

  uv run --no-project --with-editable ~/code/llm_client python \
      scripts/learning_loop/collect_feedback.py [--since-days 3] [--file] [--max-file 25]
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import glob
import hashlib
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transcripts as T  # noqa: E402
import feedback_log as FL  # noqa: E402
import subagents as SA  # noqa: E402

HOME = Path.home()
OUT = Path(os.environ.get("FEEDBACK_OUT", HOME / "projects/data/feedback-collector"))
PROJECT_META = Path(os.environ.get("PROJECT_META", HOME / "code/project-meta"))
# log_learning.py runs from a copy refreshed to origin/main before each run (the timer's ExecStartPre):
# the canonical checkout is refreshed by canonical-sync about every 17 minutes, so right after a merge it
# can lack the fix the collector depends on (2026-10-07: minutes after --auto-job merged). Entries still
# go to the canonical register through --store-path.
PROJECT_META_TOOLS = Path(os.environ.get("PROJECT_META_TOOLS", HOME / ".hive-brain/project-meta"))
EXTRACT_MODEL = "openrouter/deepseek/deepseek-v4-flash"
JEV = "openrouter/typesafe/jev-1.13"
KINDS = {
    "learning": "A reusable fact or practice about tools, code, data, process or the environment that would help a future agent.",
    "friction": "A rule, tool, process or policy got in the way, wasted work, misfired, or had to be worked around.",
    "correction": "Brian told an agent it was wrong, misunderstood him, or should work differently, or stated how he wants agents to work.",
    "concern": "An open risk or unresolved problem that still needs action; not yet a lesson.",
    "noise": "Nothing reusable: routine status, compliance boilerplate, 'none', or text that only makes sense inside its own session.",
}
FILE_KINDS = ("learning", "friction", "correction")
# Closeout Concerns and Decisions have their own homes (concern issues, decision records) and stay in
# the daily log; only these sources can be filed to the register.
FILE_SOURCES = {("closeout", "Learnings"), ("closeout", "Policy"), ("llm", "learning"), ("llm", "friction"),
                ("llm", "correction"), ("llm", "direction")}
# Reusability gate (2026-10-06 spot check of the first night's 33 filed entries, hand-labelled):
# lines an agent wrote under its own closeout "Learnings" heading were 8/8 reusable; items the
# light LLM extracted from session narration were 7/25. Jev's yes/no "reusable?" answer did not
# separate them on its own (best 9/14 = 64% at p>=0.8). It gates as a second filter at p>=0.6
# (--min-reusable): every entry the hand check judged reusable scored >= 0.61, so it drops nothing
# good there, and it stops an obviously session-bound line that slips past the source gate. Only these sources are filed automatically; every other
# item stays in the daily log. Wrong if a 10-entry spot check of filed items falls below 8/10.
AUTO_FILE_SOURCES = {("closeout", "Learnings")}
REUSABLE_Q = ("Would this help a future AI coding agent working on a DIFFERENT task or project? "
              "Yes only if it states a general fact or practice about tools, code, data, process or the "
              "environment. No if it is narration of what this session is doing, a status update, or "
              "details that only matter for this one task, document, client or person.")
WINDOW_CHARS, TURN_CHARS = 14000, 1500


def log(msg: str) -> None:
    print(f"[{dt.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def clip(text: str, head: int = 700, tail: int = 300) -> str:
    """Keep the start and the end of a long error. log_learning prints the failing step first
    ("AUTOMATIC LEARNING LANE FAILED at: <step>") and the closeout residue last; keeping only the
    last 300 characters hid the cause of the 2026-10-07 stranded entries."""
    text = text.strip()
    return text if len(text) <= head + tail else f"{text[:head]} … [{len(text) - head - tail} chars] … {text[-tail:]}"


def norm(s: str) -> str:
    return " ".join(s.split())


def item_id(*parts: str) -> str:
    return hashlib.sha256("\0".join(parts).encode()).hexdigest()[:16]


# ---------- 1. read ----------
def discover() -> list[tuple[Path, str]]:
    files = [(Path(p), "claude") for p in glob.glob(str(HOME / ".claude/projects/*/*.jsonl"))]
    files += [(Path(p), "codex") for p in glob.glob(str(HOME / ".codex/sessions/**/*.jsonl"), recursive=True)]
    return files


def read_changed(db: sqlite3.Connection, since_days: float, limit: int | None):
    cutoff_ts = time.time() - since_days * 86400
    since_iso = dt.datetime.fromtimestamp(cutoff_ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    known = {r[0]: (r[1], r[2]) for r in db.execute("SELECT path, offset, mtime FROM files")}
    out, skipped = [], 0
    for path, client in discover():
        try:
            st = path.stat()
        except FileNotFoundError:
            continue
        prev = known.get(str(path))
        if prev is None and st.st_mtime < cutoff_ts:
            continue
        if prev and prev[1] >= st.st_mtime and prev[0] <= st.st_size:
            skipped += 1
            continue
        offset = prev[0] if prev and prev[0] <= st.st_size else 0
        since = "" if prev and offset else since_iso
        out.append(T.read_transcript(path, client, offset, since))
        out[-1].mtime = st.st_mtime  # type: ignore[attr-defined]
        if limit and len(out) >= limit:
            break
    return out, skipped


# ---------- 2. closeouts ----------
def closeout_items(t: T.Transcript, counts: collections.Counter) -> list[dict]:
    items = []
    for turn in t.turns:
        if turn.role != "agent":
            continue
        _, fields = T.split_closeout(turn.text)
        if fields:
            counts["closeouts"] += 1
        for name in T.COLLECTED_FIELDS:
            value = fields.get(name, "").strip()
            if not value:
                continue
            if T.field_is_none(value):
                counts[f"closeout_{name}_none"] += 1
                continue
            counts[f"closeout_{name}"] += 1
            items.append(base_item(t, turn, "closeout", name, "agent", value, "",
                                   already_recorded=T.already_recorded(value)))
    return items


def base_item(t, turn, source, field_name, speaker, quote, lesson, already_recorded=False) -> dict:
    return {"id": item_id(t.session_id, source, field_name, norm(quote)), "client": t.client,
            "cwd": turn.cwd or t.cwd,
            "transcript": t.path, "byte_offset": turn.offset, "session_id": t.session_id, "ts": turn.ts,
            "source": source, "field": field_name, "speaker": speaker, "quote": quote, "lesson": lesson,
            "already_recorded": already_recorded}


# ---------- 3. extract ----------
def windows(t: T.Transcript) -> list[tuple[str, list[T.Turn]]]:
    out, buf, turns, size = [], [], [], 0
    for turn in t.turns:
        text = T.split_closeout(turn.text)[0] if turn.role == "agent" else turn.text
        text = text.strip()[:TURN_CHARS]
        if not text:
            continue
        block = f"[{'BRIAN' if turn.role == 'human' else 'AGENT'}]\n{text}\n"
        if size + len(block) > WINDOW_CHARS and buf:
            out.append(("\n".join(buf), turns))
            buf, turns, size = [], [], 0
        buf.append(block)
        turns.append(turn)
        size += len(block)
    if buf and any(x.role == "human" for x in turns):
        out.append(("\n".join(buf), turns))
    return [w for w in out if any(x.role == "human" for x in w[1])]


EXTRACT_PROMPT = """You read part of a conversation between Brian (a software developer) and his AI coding agent.
Find feedback that should change how agents work in future:
- correction: Brian objects to what the agent did or said, says it is wrong or not what he asked, has to repeat himself, or says he does not understand the agent's wording ("no, do X", "why did you...", "I already said...", "what do you mean X?").
- friction: Brian or the agent says a rule, tool, hook, process or policy got in the way, misfired, wasted time, or had to be worked around.
- direction: Brian states a standing preference or how he wants agents or his systems to work in general, beyond the task at hand ("we should make X broader", "from now on...", "I always want...").
- learning: the agent or Brian states a reusable fact or practice that future agents should know (not routine progress, not a plan for this task).
Skip approvals ("yes", "proceed", "ok do that"), new task requests, routine status, and questions that only ask for information.
For each item give: kind; speaker (brian or agent); quote = an exact verbatim excerpt (max 300 characters, copied character for character from ONE message, typos included); lesson = one plain sentence a future agent could act on, using only what this conversation shows (do not invent context or generalize beyond it).
Return an empty list when there is nothing; most windows have 0-3 items.

CONVERSATION:
"""


def extract(t: T.Transcript, text: str, turns: list[T.Turn], counts, errors) -> list[dict]:
    """One window of one transcript; windows of all transcripts run in one thread pool."""
    from pydantic import BaseModel, Field
    from llm_client import call_llm_structured

    class Found(BaseModel):
        kind: Literal["correction", "direction", "friction", "learning"]
        speaker: Literal["brian", "agent"]
        quote: str = Field(description="exact verbatim excerpt from one message")
        lesson: str

    class Extraction(BaseModel):
        items: list[Found]

    items: list[dict] = []
    counts["llm_windows"] += 1
    try:
        res, meta = call_llm_structured(
            EXTRACT_MODEL, [{"role": "user", "content": EXTRACT_PROMPT + text}], response_model=Extraction,
            reasoning_effort="none", task="feedback-collector.extract",
            model_justification="light model for bulk transcript extraction (workspace rule: approved light LLM for prose meaning)",
            trace_id=f"feedback-collector/{t.session_id}/{turns[0].offset}", max_budget=0.05)
        counts["cost_extract_usd_micro"] += int((meta.cost or 0) * 1e6)
    except Exception as exc:  # counted, file re-read next run
        errors.append(f"extract {t.path}: {type(exc).__name__}: {str(exc)[:200]}")
        return items
    for f in res.items:
        q = norm(f.quote)
        src = next((x for x in turns if q and q in norm(x.text)), None)
        if src is None:
            counts["llm_quote_not_found"] += 1
            continue
        role_ok = (src.role == "human") == (f.speaker == "brian")
        counts["llm_items"] += 1
        items.append(base_item(t, src, "llm", f.kind, "brian" if src.role == "human" else "agent",
                               f.quote.strip(), f.lesson.strip()) | {"speaker_mismatch": not role_ok})
    return items


# ---------- 4. triage / 5. covered ----------
def jev_triage(it: dict) -> dict:
    from llm_client import ChoiceQuestion, NoulQuestion, call_decisions
    r = call_decisions(
        JEV, state={"where": f"{it['source']} {it['field']}", "speaker": it["speaker"],
                    "text": it["quote"][:2000], "lesson": it["lesson"]},
        questions={"kind": ChoiceQuestion(
            "What kind of feedback is this text from a coding-agent session, for improving future agent work?", KINDS),
            "reusable": NoulQuestion(REUSABLE_Q)},
        task="feedback-collector.triage", trace_id=f"feedback-collector/triage/{it['id']}", max_budget=0.01)
    a = r.answers["kind"]
    return {"kind": a.choice, "p": round(a.probabilities.get(a.choice, 0.0), 3), "confidence": a.confidence,
            "reusable_p": round(float(r.answers["reusable"].probability), 3),
            "probabilities": {k: round(v, 3) for k, v in a.probabilities.items()}, "cost": r.cost}


WORD = re.compile(r"[a-z0-9_]{3,}")


class Register:
    """Word-overlap (BM25) candidate retrieval over existing learnings; Jev judges the match."""

    def __init__(self) -> None:
        self.ids, self.texts, self.docs = [], [], []
        for p in glob.glob(str(PROJECT_META / "learnings/entries/*.json")):
            try:
                d = json.load(open(p))
            except ValueError:
                continue
            text = " ".join(str(d.get(k) or "") for k in ("learning", "finding", "lesson", "recommended_action"))
            self.ids.append(d.get("entry_id", Path(p).stem))
            self.texts.append(text[:1500])
            self.docs.append(collections.Counter(WORD.findall(text.lower())))
        self.df = collections.Counter(w for d in self.docs for w in d)
        self.avg = sum(sum(d.values()) for d in self.docs) / max(1, len(self.docs))

    def nearest(self, text: str) -> int | None:
        q = set(WORD.findall(text.lower()))
        n, best, best_i = len(self.docs), 0.0, None
        for i, d in enumerate(self.docs):
            dl, s = sum(d.values()), 0.0
            for w in q & d.keys():
                idf = math.log(1 + (n - self.df[w] + 0.5) / (self.df[w] + 0.5))
                s += idf * d[w] * 2.2 / (d[w] + 1.2 * (0.25 + 0.75 * dl / self.avg))
            if s > best:
                best, best_i = s, i
        return best_i


def jev_covered(it: dict, reg: Register) -> dict:
    from llm_client import NoulQuestion, call_decisions
    i = reg.nearest(it["lesson"] + " " + it["quote"])
    if i is None:
        return {"p": 0.0, "entry_id": None}
    r = call_decisions(
        JEV, state={"new_item": (it["lesson"] or it["quote"])[:1500], "existing_learning": reg.texts[i]},
        questions={"covered": NoulQuestion("Does the existing learning already state the same lesson as the new item?")},
        task="feedback-collector.covered", trace_id=f"feedback-collector/covered/{it['id']}", max_budget=0.01)
    return {"p": round(float(r.answers["covered"].probability), 3), "entry_id": reg.ids[i], "cost": r.cost}


# ---------- 7. file ----------
class RegisterLocked(Exception):
    pass


PENDING = ("eligible_not_filed", "deferred_cap", "deferred_register_locked", "deferred_repeat_check")


def filed_quotes() -> set[str]:
    """Normalized text of every item already filed (from the daily logs), so a closeout line repeated
    across sessions is filed once. 2026-10-07 spot check: 2 of 10 filed entries were exact repeats."""
    seen: set[str] = set()
    for p in sorted(OUT.glob("items-*.jsonl")):
        by_id: dict[str, dict] = {}
        for line in open(p):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if "filing_update" in d:
                if d["id"] in by_id:
                    by_id[d["id"]]["filing"] = d["filing_update"]
            else:
                by_id[d["id"]] = d
        seen.update(norm(d["quote"]) for d in by_id.values() if str(d.get("filing", "")).startswith("lrn-"))
    return seen

def filed_texts(days: int = 14, limit: int = 60) -> list[str]:
    """Quotes filed in the last `days` daily logs, newest last, for the reworded-repeat check."""
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    out: list[str] = []
    for p in sorted(OUT.glob("items-*.jsonl")):
        if p.stem[len("items-"):] < cutoff:
            continue
        by_id: dict[str, dict] = {}
        for line in open(p):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if "filing_update" in d:
                if d["id"] in by_id:
                    by_id[d["id"]]["filing"] = d["filing_update"]
            else:
                by_id[d["id"]] = d
        out += [d["quote"].strip() for d in by_id.values() if str(d.get("filing", "")).startswith("lrn-")]
    return out[-limit:]


class _SameLesson(BaseModel):
    same_lesson_as: int | None
    reason: str


def repeats_filed(quote: str, recent: list[str]) -> bool:
    """Light-model check: does this line state the same lesson as one filed recently, even reworded?

    2026-10-07: exact-text dedup let 2 of 10 filed entries through as paraphrased repeats; this
    prompt caught both and flagged none of the 8 distinct entries (9/9 on that set). Raises on a
    model failure so the caller defers the item rather than filing a possible repeat.
    """
    if not recent:
        return False
    from llm_client import call_llm_structured
    earlier = "\n".join(f"[{i}] {t[:600]}" for i, t in enumerate(recent))
    r = call_llm_structured(
        EXTRACT_MODEL,
        [{"role": "user", "content": (
            "A new lesson is about to be added to a register of lessons for AI coding agents. Does it state the SAME "
            "lesson as one of the earlier entries (same fact or practice, even if worded differently or mixed with "
            "other points)? Answer the earlier entry's number, or null if none.\n\nEarlier entries:\n"
            f"{earlier}\n\nNew lesson:\n{quote[:1500]}")}],
        _SameLesson, task="feedback-collector.repeat-check", trace_id=f"feedback-collector/repeat-check/{item_id(quote)}",
        max_budget=0.02, reasoning_effort="none",
        model_justification="light model for prose meaning: does a new lesson repeat an earlier one")
    res = r[0] if isinstance(r, tuple) else r
    return res.same_lesson_as is not None


def _repeat_or_defer(it: dict, recent: list[str]) -> str | None:
    """'repeats_filed' for a reworded repeat, 'deferred_repeat_check' if the check failed (retried next run), else None."""
    try:
        return "repeats_filed" if repeats_filed(it["quote"], recent) else None
    except Exception as exc:  # never file an unchecked possible repeat; the item stays pending
        log(f"repeat check failed for {it['id']}: {type(exc).__name__}: {str(exc)[:200]}")
        return "deferred_repeat_check"


def file_item(it: dict) -> str:
    kind = it["triage"]["kind"]
    who = "Brian" if it["speaker"] == "brian" else "the agent"
    body = (f"[{kind}, collected automatically from a {it['client']} transcript; Jev p={it['triage']['p']}] "
            f"{who} wrote: {it['quote'].strip()}")
    if it["lesson"]:  # machine-drawn, so labelled as a suggestion rather than stated as the lesson
        body += f"\n\nSuggested lesson (light LLM, unreviewed): {it['lesson'].strip()}"
    if len(body) < 80:  # the register's own minimum; a shorter item is not actionable on review
        raise ValueError("body under 80 characters")
    tools = PROJECT_META_TOOLS if (PROJECT_META_TOOLS / "scripts/log_learning.py").exists() else PROJECT_META
    cmd = [sys.executable, str(tools / "scripts/log_learning.py"), "--type", "learning",
           "--store-path", str(PROJECT_META / "learnings/entries"), "--repo-root", str(PROJECT_META),
           "--agent", "claude-code" if it["client"] == "claude" else "codex", "--invocation", "import",
           "--knowledge-kind", "observation", "--applicability-task-type", "other",
           "--transcript-ref", f"{'claude-code' if it['client'] == 'claude' else 'codex'}:{it['session_id']}",
           "--source-ref", f"{it['transcript']}@byte{it['byte_offset']}", "--push",
           # A timer has no agent session: when a live claim locks the register, log_learning appends
           # straight onto main instead of opening a claimed lane (project-meta #2414).
           "--auto-job", "feedback-collector", body]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_META, timeout=300)
    if r.returncode != 0 and "requires the current native" in r.stdout + r.stderr:
        # The register is read-only while any lane claims project-meta, and log_learning's own lane
        # needs an agent session id a timer does not have. Root fix filed as a keyed concern
        # (feedback-collector-register-locked); until then the item waits for a later run.
        raise RegisterLocked()
    if r.returncode != 0:
        raise RuntimeError(f"log_learning exit {r.returncode}: {clip(r.stderr or r.stdout)}")
    m = re.search(r"lrn-\d{8}T\d+Z-[0-9a-f]+", r.stdout + r.stderr)
    return m.group(0) if m else "recorded"


# ---------- run ----------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--since-days", type=float, default=1.0, help="first-seen files: only records this recent")
    ap.add_argument("--file", action="store_true", help="file sure learning/friction/correction items to the register")
    ap.add_argument("--max-file", type=int, default=25, help="cap on register filings per run")
    ap.add_argument("--legacy-register", action="store_true",
                    help="with --file, also file items to the legacy project-meta register (off by default)")
    ap.add_argument("--max-reports", type=int, default=80, help="cap on private-log report issues per run")
    ap.add_argument("--min-p", type=float, default=0.8, help="Jev probability needed to file")
    ap.add_argument("--min-reusable", type=float, default=0.6,
                    help="Jev probability the item is reusable beyond its own task, needed to file")
    ap.add_argument("--limit-files", type=int, default=None, help="testing: stop after N changed transcripts")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--reports-only", action="store_true",
                    help="testing: only the report path (skip extraction, triage, covered and legacy filing)")
    ap.add_argument("--corrections-only", action="store_true",
                    help="recover already-extracted human corrections without rereading transcripts or model calls")
    ap.add_argument("--file-pending", metavar="ITEMS_JSONL",
                    help="file items an earlier run left eligible_not_filed or deferred_cap (appends filing updates)")
    ap.add_argument("--no-alert", action="store_true", help="testing: do not open a concern on failure")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.file_pending:
        filed, errs = file_pending(Path(args.file_pending), args.max_file, args.min_reusable)
        log(f"RESULT filed={filed} errors={len(errs)} exit={1 if errs else 0}")
        for e in errs[:5]:
            log(f"error: {e}")
        return 1 if errs else 0
    db = sqlite3.connect(OUT / "state.sqlite")
    db.execute("CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, offset INT, mtime REAL)")
    db.execute("CREATE TABLE IF NOT EXISTS items (id TEXT PRIMARY KEY, day TEXT, kind TEXT, filed TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS reports (id TEXT PRIMARY KEY, day TEXT, records INT, issue TEXT)")
    counts, errors, timing = collections.Counter(), [], {}
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    day = run_id[:4] + "-" + run_id[4:6] + "-" + run_id[6:8]

    def step(name, fn):
        t0 = time.perf_counter()
        r = fn()
        timing[name] = round(time.perf_counter() - t0, 1)
        log(f"step {name}: {timing[name]}s")
        return r

    trs, skipped = step("read", lambda: ([], 0) if args.corrections_only else read_changed(db, args.since_days, args.limit_files))
    counts["transcripts_unchanged"] = skipped
    for t in trs:
        counts[f"transcripts_{t.client}"] += 1
        counts[f"transcripts_{t.client}_interactive"] += t.interactive
        counts["turns"] += len(t.turns)
        counts["bad_lines"] += t.bad_lines
    items = step("closeouts", lambda: [i for t in trs for i in closeout_items(t, counts)])
    failed_files: set[str] = set()

    # R. reports: closeout Feedback fields -> records -> the private log
    filed_reports = {r[0] for r in db.execute("SELECT id FROM reports WHERE issue LIKE 'http%'")}
    reps = [r for r in step("reports", lambda: [r for t in trs for r in FL.reports(t, counts)] + SA.reports(trs, counts))
            if r["id"] not in filed_reports]
    counts["reports_new"] = len(reps)

    def split_one(r):
        errs = FL.split_rest(r, counts)
        counts["split_done"] += 1
        if counts["split_done"] % 25 == 0:
            log(f"split: {counts['split_done']}/{len(reps)} reports")
        if errs:
            errors.extend(errs)
            failed_files.add(r["transcript"])
            r["filing"] = "split_failed"
    with ThreadPoolExecutor(args.workers) as ex:
        step("split", lambda: list(ex.map(split_one, reps)))

    def file_reports():
        n = 0
        for r in reps:
            if r.get("filing") == "split_failed":
                continue
            if not r["records"]:
                r["filing"] = "no_records"
            elif not args.file:
                r["filing"] = "not_filed (run without --file)"
            elif n >= args.max_reports:
                r["filing"] = "deferred_cap"
                failed_files.add(r["transcript"])
            else:
                try:
                    r["filing"] = FL.file_report(r)
                    n += 1
                    if n % 10 == 0:
                        log(f"file_reports: {n}/{len(reps)} filed")
                except Exception as exc:
                    r["filing"] = "error"
                    errors.append(f"report {r['id']}: {clip(str(exc))}")
                    failed_files.add(r["transcript"])
            counts["reports_" + ("filed" if r["filing"].startswith("http") else r["filing"].split(" ")[0])] += 1
        for r in reps:
            for rec in r["records"]:
                counts["records_unprovenanced"] += rec["unprovenanced"]
                counts[f"records_{rec['kind']}"] += 1

    def extract_one(job):
        t, text, turns = job
        errs: list[str] = []
        local: collections.Counter = collections.Counter()  # merged in the main thread
        return extract(t, text, turns, local, errs), local, errs, t.path

    def extract_all():
        jobs = [(t, text, turns) for t in trs if t.interactive for text, turns in windows(t)]
        log(f"extract: {len(jobs)} windows from {sum(1 for t in trs if t.interactive)} interactive transcripts")
        found: list[dict] = []
        with ThreadPoolExecutor(args.workers) as ex:
            for got, local, errs, path in ex.map(extract_one, jobs):
                found += got
                counts.update(local)
                if errs:
                    errors.extend(errs)
                    failed_files.add(path)
        return found
    if args.reports_only or args.corrections_only:
        items = []
    else:
        items += step("extract", extract_all)

    seen = {r[0] for r in db.execute("SELECT id FROM items")}
    fresh, dup = {}, 0
    for it in items:
        if it["id"] in seen or it["id"] in fresh:
            dup += 1
        else:
            fresh[it["id"]] = it
    counts["items_duplicate"] = dup
    items = list(fresh.values())

    def triage_one(it):
        try:
            it["triage"] = jev_triage(it)
        except Exception as exc:
            it["triage"] = None
            errors.append(f"triage {it['id']}: {type(exc).__name__}: {str(exc)[:200]}")
            failed_files.add(it["transcript"])
    with ThreadPoolExecutor(args.workers) as ex:
        step("triage", lambda: list(ex.map(triage_one, items)))

    # Existing offsets must not strand previously extracted human corrections.
    # Backfill the bounded daily logs; the report id and filing table dedupe it.
    backlog = []
    cutoff = (dt.date.today() - dt.timedelta(days=14)).isoformat()
    for path in sorted(OUT.glob("items-*.jsonl")):
        if path.stem.removeprefix("items-") >= cutoff:
            with path.open() as fh:
                backlog.extend(json.loads(line) for line in fh)
    human = [r for r in FL.correction_reports(backlog + items) if r["id"] not in filed_reports]
    reps.extend(human)
    counts["human_reports_new"] = len(human)
    step("file_reports", file_reports)

    reg = step("load_register", Register)
    counts["register_entries"] = len(reg.ids)

    def covered_one(it):
        if not it["triage"] or it["triage"]["kind"] not in FILE_KINDS:
            return
        try:
            it["covered"] = jev_covered(it, reg)
        except Exception as exc:
            errors.append(f"covered {it['id']}: {type(exc).__name__}: {str(exc)[:200]}")
    with ThreadPoolExecutor(args.workers) as ex:
        step("covered", lambda: list(ex.map(covered_one, items)))

    # 7. filing (sequential: each call is one git commit in project-meta)
    def file_all():
        filed, locked = 0, False
        seen, recent = filed_quotes(), filed_texts()
        for it in sorted(items, key=lambda i: -(i["triage"] or {}).get("p", 0)):
            tr = it["triage"]
            if not tr or tr["kind"] not in FILE_KINDS:
                continue
            if it["already_recorded"]:
                it["filing"] = "already_recorded"
            elif (it["source"], it["field"]) not in AUTO_FILE_SOURCES:
                it["filing"] = "log_only_source"
            elif tr["p"] < args.min_p:
                it["filing"] = "below_threshold"
            elif tr.get("reusable_p", 0.0) < args.min_reusable:
                it["filing"] = "not_reusable"
            elif not (args.file and args.legacy_register):  # before the repeat check: its model calls only serve filing
                it["filing"] = "eligible_not_filed (legacy register off)"
            elif norm(it["quote"]) in seen:
                it["filing"] = "duplicate_of_filed"
            elif (verdict := _repeat_or_defer(it, recent)) is not None:
                it["filing"] = verdict
            elif filed >= args.max_file:
                it["filing"] = "deferred_cap"
            elif locked:
                it["filing"] = "deferred_register_locked"
            else:
                try:
                    it["filing"] = file_item(it)
                    filed += 1
                    seen.add(norm(it["quote"]))
                    recent.append(it["quote"].strip())
                except RegisterLocked:
                    it["filing"], locked = "deferred_register_locked", True
                except Exception as exc:
                    it["filing"] = "error"
                    errors.append(f"file {it['id']}: {clip(str(exc))}")
            counts["filing_" + ("filed" if it["filing"].startswith("lrn-") or it["filing"] == "recorded"
                                else it["filing"].split(" ")[0])] += 1
    step("file", file_all)

    def write():
        with open(OUT / f"items-{day}.jsonl", "a") as fh:
            for it in items:
                fh.write(json.dumps(it | {"run_id": run_id}, ensure_ascii=False) + "\n")
                db.execute("INSERT OR IGNORE INTO items VALUES (?,?,?,?)", (it["id"], day, (it["triage"] or {}).get("kind"),
                                                                             it.get("filing")))
        for t in trs:  # a file with a failed call is re-read next run (item ids dedupe the rest)
            if t.path not in failed_files:
                db.execute("INSERT OR REPLACE INTO files VALUES (?,?,?)", (t.path, t.end_offset, t.mtime))
        with open(OUT / f"reports-{day}.jsonl", "a") as fh:
            for r in reps:
                fh.write(json.dumps(r | {"run_id": run_id}, ensure_ascii=False) + "\n")
                db.execute("INSERT OR REPLACE INTO reports VALUES (?,?,?,?)",
                           (r["id"], day, len(r["records"]), r.get("filing", "")))
        db.commit()
    step("write", write)

    if args.file and args.legacy_register:  # earlier days' items still waiting (cap or a locked register), oldest first
        left = args.max_file - counts["filing_filed"]
        for f in sorted(OUT.glob("items-*.jsonl"))[-8:]:
            if left <= 0:
                break
            n, errs = file_pending(f, left, args.min_reusable)
            counts["backlog_filed"] += n
            left -= n
            errors.extend(errs)

    for it in items:
        k = (it["triage"] or {}).get("kind", "untriaged")
        counts[f"kind_{k}"] += 1
        counts[f"kind_{k}_{it['source']}"] += 1
        counts["cost_jev_usd_micro"] += int(((it["triage"] or {}).get("cost") or 0) * 1e6)
        counts["cost_jev_usd_micro"] += int((it.get("covered") or {}).get("cost", 0) * 1e6)
    summary = {"run_id": run_id, "items": len(items), "errors": len(errors), "error_samples": errors[:5],
               "timing_s": timing, "counts": dict(sorted(counts.items())),
               "cost_usd": round((counts["cost_extract_usd_micro"] + counts["cost_jev_usd_micro"]
                                  + counts["cost_split_usd_micro"]) / 1e6, 4),
               "reports": len(reps), "reports_out": str(OUT / f"reports-{day}.jsonl"),
               "out": str(OUT / f"items-{day}.jsonl")}
    with open(OUT / "runs.jsonl", "a") as fh:
        fh.write(json.dumps(summary) + "\n")
    print(json.dumps(summary, indent=1))
    log(f"RESULT reports={len(reps)} filed={counts['reports_filed']} items={len(items)} errors={len(errors)} cost=${summary['cost_usd']} exit={1 if errors else 0}")
    return 1 if errors else 0


def file_pending(path: Path, cap: int, min_reusable: float = 0.6) -> tuple[int, list[str]]:
    """File items a dry run judged eligible; the day file stays append-only (update lines carry `filing_update`)."""
    items: dict[str, dict] = {}
    for line in open(path):
        d = json.loads(line)
        if "filing_update" in d:
            items[d["id"]]["filing"] = d["filing_update"]
        else:
            items[d["id"]] = d
    todo = [i for i in items.values() if str(i.get("filing", "")).startswith(PENDING)
            and (i["source"], i["field"]) in AUTO_FILE_SOURCES
            and (i.get("triage") or {}).get("reusable_p", 0.0) >= min_reusable]
    todo.sort(key=lambda i: -i["triage"]["p"])
    filed, errors, seen, recent = 0, [], filed_quotes(), filed_texts()
    with open(path, "a") as fh:
        for it in todo:
            if filed >= cap:
                break
            if norm(it["quote"]) in seen:
                fh.write(json.dumps({"id": it["id"], "filing_update": "duplicate_of_filed"}) + "\n")
                continue
            verdict = _repeat_or_defer(it, recent)
            if verdict is not None:
                fh.write(json.dumps({"id": it["id"], "filing_update": verdict}) + "\n")
                continue
            try:
                entry = file_item(it)
                filed += 1
                seen.add(norm(it["quote"]))
                recent.append(it["quote"].strip())
            except RegisterLocked:
                log("register locked by a live project-meta lane; the rest wait for the next run")
                break
            except Exception as exc:
                entry = "error"
                errors.append(clip(str(exc)))
            fh.write(json.dumps({"id": it["id"], "filing_update": entry}) + "\n")
            log(f"filed {it['id']} -> {entry}")
    log(f"{path.name}: pending={len(todo)} filed={filed} errors={len(errors)}")
    return filed, errors


def alert(code: int, detail: str) -> None:
    subprocess.run([sys.executable, str(PROJECT_META / "scripts/notify_operator.py"), "--key", "feedback-collector-failed",
                    "--severity", "agent", "--source", "feedback-collector",
                    "--title", f"Nightly feedback collector exited {code}",
                    "--body", f"{detail[-1500:]}\nRun log: {OUT}/runs.jsonl; journal: journalctl --user -u feedback-collector"],
                   timeout=120)


if __name__ == "__main__":
    NO_ALERT = "--no-alert" in sys.argv
    try:
        rc = main()
        detail = "some LLM, Jev or filing calls failed; see error_samples in runs.jsonl"
    except Exception:
        rc, detail = 2, traceback.format_exc()
        print(detail, file=sys.stderr)
    if rc and not NO_ALERT:
        try:
            alert(rc, detail)
        except Exception as exc:  # the journal still shows the failure
            print(f"ALERT FAILED: {exc}", file=sys.stderr)
    sys.exit(rc)
