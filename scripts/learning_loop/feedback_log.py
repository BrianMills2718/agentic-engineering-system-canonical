"""Closeout Feedback fields -> feedback-report.v1 records -> the private feedback log.

Plan: proposals/aes-learning-loop/PLAN.md, slice S1. One report per closeout Feedback field (the
pre-2026-10-07 "Learnings" heading counts too). Marked lines are parsed by records.py (code); the
remaining free text is split by the light model, which writes only the one-sentence text and the
qualifiers: every record's links come from code reading a verbatim excerpt, and an excerpt not found
in the field is dropped. Each report becomes one issue in the private log repository, records in a
JSON block, labels by record kind. Grouping into problems, licences and effects are later slices.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from typing import Literal

from pydantic import BaseModel, Field

import records as R
import transcripts as T

LOG_REPO = os.environ.get("FEEDBACK_LOG_REPO", "BrianMills2718/agent-feedback-log")
SPLIT_MODEL = "openrouter/deepseek/deepseek-v4-flash"
REPORT_FIELDS = ("Feedback", "Learnings")


_REPOS: dict[str, str] = {}


def repo_of(cwd: str) -> str:
    """`owner/repo` of the GitHub remote of the session's working directory ("" when unknown), cached."""
    if not cwd:
        return ""
    if cwd not in _REPOS:
        try:
            url = subprocess.run(["git", "-C", cwd, "remote", "get-url", "origin"], capture_output=True,
                                 text=True, timeout=10).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            url = ""
        m = __import__("re").search(r"github[^:/]*[:/]([\w.-]+/[\w.-]+?)(?:\.git)?$", url)
        _REPOS[cwd] = m.group(1) if m else ""
    return _REPOS[cwd]


def _norm(s: str) -> str:
    return " ".join(s.split()).lower()


def report_id(t: T.Transcript, turn: T.Turn, field: str) -> str:
    return "rep-" + hashlib.sha256(f"{t.client}|{t.session_id}|{turn.offset}|{field}".encode()).hexdigest()[:12]


def reports(t: T.Transcript, counts) -> list[dict]:
    """Every non-empty, non-"None" Feedback (or legacy Learnings) field in the agent's closeouts."""
    out = []
    for turn in t.turns:
        if turn.role != "agent":
            continue
        _, fields = T.split_closeout(turn.text)
        for name in REPORT_FIELDS:
            value = fields.get(name, "").strip()
            if not value:
                continue
            if T.field_is_none(value):
                counts[f"report_{name}_none"] += 1
                continue
            prov = R.Provenance(client=t.client, session_id=t.session_id, turn_offset=turn.offset, ts=turn.ts,
                                cwd=turn.cwd)
            recs, rest = R.parse_feedback(value, prov, repo_of(turn.cwd))
            counts[f"report_{name}"] += 1
            counts["records_markers"] += len(recs)
            out.append({"id": report_id(t, turn, name), "field": name, "transcript": t.path,
                        "provenance": prov.model_dump(), "value": value,
                        "records": [r.model_dump() for r in recs], "rest": rest})
    return out


def correction_reports(items: list[dict]) -> list[dict]:
    """Bridge already-extracted human corrections directly to immutable reports.

    No second semantic judgment or agent closeout is needed. Keep the literal
    human quote, with the transcript and byte offset that extraction verified.
    """
    out = {}
    for item in items:
        if item.get("speaker") != "brian" or item.get("source") != "llm" or item.get("field") not in ("correction", "direction"):
            continue
        if not item.get("quote", "").strip() or not item.get("transcript"):
            continue
        prov = R.Provenance(client=item["client"], session_id=item["session_id"],
                            turn_offset=item["byte_offset"], ts=item["ts"], cwd=item.get("cwd", ""), line=item["quote"])
        rec = R.Record(kind="observation", text=item["quote"],
                       links=[R.Link(kind="path", ref=item["transcript"])],
                       subject_kind="work", provenance=prov)
        rec.id = R.record_id(prov, rec.kind, rec.text)
        rid = "rep-human-" + item["id"]
        out[rid] = {"id": rid, "field": "Human correction", "transcript": item["transcript"],
                    "provenance": prov.model_dump(), "value": item["quote"],
                    "records": [rec.model_dump()], "rest": []}
    return list(out.values())


SPLIT_PROMPT = """An AI coding agent ended its work with this free-text Feedback note. Split what it reports into records:
- observation: something that happened (including a mistake the agent made, a tool or rule that got in the way, a failure).
- claim: what the agent now believes: a cause, a lesson, a practice to follow or avoid. basis: seen (directly observed), inferred (reasoned from evidence), or guessed. A lesson drawn from a mistake is a claim about the reasoning that went wrong.
- action: something the agent tried, did, or proposes to change: intent Investigate (an experiment or research), Mitigate (a workaround), Repair (a fix), Detect (a check or alert), or Prevent (a rule or design change).
Notes often say "Filed #N (summary)" or "Recorded as #N: summary": the issue IS the evidence. Make records from the summary's content and keep the issue link inside each record's excerpt. Never make a record of the filing itself, and skip pure bookkeeping ("nothing new this turn", "recorded earlier", "None").
For each record give: kind; text = ONE plain sentence saying only what the note says (do not add causes or numbers it does not state); excerpt = the exact span of the note this record comes from, copied character for character, wide enough to include the link or issue number that supports it; for claims basis and confidence; for actions intent and status.
Return an empty list when the note holds nothing.

NOTE:
"""


class _Split(BaseModel):
    kind: Literal["observation", "claim", "action"]
    text: str
    excerpt: str = Field(description="exact verbatim span of the note")
    basis: Literal["seen", "inferred", "guessed"] | None = None
    confidence: Literal["low", "medium", "high"] | None = None
    intent: Literal["Investigate", "Mitigate", "Repair", "Detect", "Prevent"] | None = None
    status: Literal["proposed", "done"] | None = None


class _Splits(BaseModel):
    records: list[_Split]


def sentence_links(note: str, excerpt: str) -> list[R.Link]:
    """Links of the sentence holding `excerpt` when the excerpt itself has none: the nearest one before
    it in that sentence, else the nearest after. Position only; meaning is the model's job."""
    i = note.find(excerpt)
    if i < 0:
        return []
    lo = max(note.rfind(". ", 0, i), note.rfind("\n", 0, i)) + 1
    hi_dot, hi_nl = note.find(". ", i + len(excerpt)), note.find("\n", i + len(excerpt))
    hi = min(x for x in (hi_dot, hi_nl, len(note)) if x >= 0)
    before, after = R.find_links(note[lo:i]), R.find_links(note[i + len(excerpt):hi])
    return before[-1:] or after[:1]


def split_rest(rep: dict, counts) -> list[str]:
    """Light-model split of a report's unmarked lines; returns error strings (empty when clean)."""
    text = "\n".join(rep["rest"]).strip()
    if not text:
        return []
    from llm_client import call_llm_structured
    try:
        res, meta = call_llm_structured(
            SPLIT_MODEL, [{"role": "user", "content": SPLIT_PROMPT + text}], response_model=_Splits,
            reasoning_effort="none", task="feedback-collector.split",
            model_justification="light model splits free-text Feedback notes into records (prose meaning; workspace rule)",
            trace_id=f"feedback-collector/split/{rep['id']}", max_budget=0.02)
    except Exception as exc:
        return [f"split {rep['id']}: {type(exc).__name__}: {str(exc)[:200]}"]
    counts["cost_split_usd_micro"] += int((meta.cost or 0) * 1e6)
    counts["split_calls"] += 1
    prov = R.Provenance(**rep["provenance"])
    seen_text = {_norm(r["text"]) for r in rep["records"]}
    for s in res.records:
        if not s.excerpt.strip() or _norm(s.excerpt) not in _norm(text):
            counts["split_excerpt_not_found"] += 1
            continue
        if _norm(s.text) in seen_text:
            counts["split_duplicate_text"] += 1
            continue
        seen_text.add(_norm(s.text))
        links = R.normalize_links(R.find_links(s.excerpt) or sentence_links(text, s.excerpt.strip()),
                                  repo_of(prov.cwd))
        rec = R.Record(kind=s.kind, text=s.text.strip(), links=links, parsed_by="light_model",
                       basis=s.basis if s.kind == "claim" else None,
                       confidence=s.confidence if s.kind == "claim" else None,
                       intent=s.intent if s.kind == "action" else None,
                       status=(s.status or "") if s.kind == "action" else "",
                       subject_kind="work" if s.kind == "observation" else "",
                       provenance=prov.model_copy(update={"line": s.excerpt.strip()}))
        rec.unprovenanced = not rec.links
        rec.id = R.record_id(prov, rec.kind, rec.text)
        rep["records"].append(rec.model_dump())
        counts["records_light_model"] += 1
    return []


def issue_title(rep: dict) -> str:
    kinds = [r["kind"] for r in rep["records"]]
    head = next((r["text"] for k in ("claim", "observation", "action") for r in rep["records"] if r["kind"] == k), "")
    tally = ", ".join(f"{kinds.count(k)} {k}" for k in ("observation", "claim", "action") if kinds.count(k))
    return f"[{tally}] {head}"[:200]


def issue_body(rep: dict) -> str:
    p = rep["provenance"]
    lines = [f"Report `{rep['id']}` from **{rep['field']}**.",
             f"Source: {p['client']} session `{p['session_id']}`, turn offset {p['turn_offset']}, {p['ts']}",
             *([f"Transcript: `{rep['transcript']}`"] if rep["transcript"] else []), "", "Records:"]
    for r in rep["records"]:
        q = {"observation": " (control)" if r.get("subject_kind") == "control" else "", "claim": f" ({r.get('basis') or '?'}, {r.get('confidence') or '?'})",
             "action": f" ({r.get('intent') or '?'}, {r.get('status') or '?'})"}[r["kind"]]
        refs = " ".join(f"[{lk['ref']}]" for lk in r["links"] + r.get("result", [])) or "**unprovenanced**"
        lines.append(f"- {r['kind']}{q}: {r['text']} {refs}  `{r['id']}` ({r['parsed_by']})")
    lines += ["", "<details><summary>Field as written</summary>", "", "```text", rep["value"][:6000], "```",
              "</details>", "", "```json", json.dumps({"contract": R.CONTRACT, "report_id": rep["id"],
                                                     "records": rep["records"]}, ensure_ascii=False, indent=1)[:50000],
              "```"]
    return "\n".join(lines)


def issue_labels(rep: dict) -> list[str]:
    labels = {f"kind:{r['kind']}" for r in rep["records"]} | {f"parsed:{r['parsed_by']}" for r in rep["records"]}
    labels.add("source:human" if rep["field"] == "Human correction" else
               "source:manual" if rep["field"] == "manual" else "source:closeout")
    if any(r["unprovenanced"] for r in rep["records"]):
        labels.add("unprovenanced")
    return sorted(labels)


def file_report(rep: dict) -> str:
    """Create the report's issue in the private log; returns its URL."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write(issue_body(rep))
        body = fh.name
    try:
        cmd = ["gh", "issue", "create", "--repo", LOG_REPO, "--title", issue_title(rep), "--body-file", body]
        for lb in issue_labels(rep):
            cmd += ["--label", lb]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if p.returncode:
            raise RuntimeError(f"gh issue create exit {p.returncode}: {(p.stderr or p.stdout).strip()[-400:]}")
        return p.stdout.strip().splitlines()[-1]
    finally:
        os.unlink(body)


def main() -> int:
    """File one report now (the `learned` skill's explicit invocation); the closeout then links the issue."""
    import argparse
    import collections
    import datetime as dt
    import sys

    ap = argparse.ArgumentParser(description="File Feedback lines to the private feedback log now.")
    ap.add_argument("--text", help="Feedback lines (default: stdin)")
    ap.add_argument("--session", default=os.environ.get("CLAUDE_SESSION_ID", ""), help="session id")
    ap.add_argument("--client", default="manual")
    ap.add_argument("--dry-run", action="store_true", help="print the report instead of filing it")
    a = ap.parse_args()
    value = (a.text if a.text is not None else sys.stdin.read()).strip()
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    prov = R.Provenance(client=a.client, session_id=a.session, ts=ts, cwd=os.getcwd())
    recs, rest = R.parse_feedback(value, prov, repo_of(prov.cwd))
    rep = {"id": "rep-" + hashlib.sha256(f"{a.client}|{a.session}|{ts}|{value}".encode()).hexdigest()[:12],
           "field": "manual", "transcript": "", "provenance": prov.model_dump(), "value": value,
           "records": [r.model_dump() for r in recs], "rest": rest}
    counts: collections.Counter = collections.Counter()
    errs = split_rest(rep, counts) if rest else []
    for e in errs:
        print(f"error: {e}", file=sys.stderr)
    n = len(rep["records"])
    unprov = sum(r["unprovenanced"] for r in rep["records"])
    if a.dry_run:
        print(issue_title(rep)); print(issue_body(rep))
        print(f"RESULT records={n} unprovenanced={unprov} filed=dry-run exit={1 if errs else 0}")
        return 1 if errs else 0
    if not n:
        print(f"RESULT records=0 filed=none exit={1 if errs else 2}")
        return 1 if errs else 2
    url = file_report(rep)
    print(url)
    print(f"RESULT records={n} unprovenanced={unprov} filed={url} exit={1 if errs else 0}")
    return 1 if errs else 0


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())
