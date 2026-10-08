#!/usr/bin/env python3
"""S3: group related feedback records into problems and analyse the recurring ones (PLAN.md, slice S3).

Input: the collector's reports-<date>.jsonl files (feedback-report.v1 records) for the last --days.

  1. family    each observation and claim gets failure-mode families from Jev with the frozen
               question set of label_items.py (cached by record id)
  2. relate    each record is paired with its most similar record from another report (word overlap) and
               Jev judges the relation (S2 result); a Jev `challenges` is confirmed by the stronger model
               before it counts (cached by pair)
  3. group     records joined by `supports` or `same_problem` form one problem (union-find)
  4. recurring a problem counts as recurring when at least two independent sightings support it: records
               from different sessions or days that carry a resolvable link and are not `guessed`
  5. analyse   one stronger-model call per recurring problem drafts the causal chain and the general fix as
               claims and actions, each resting on member record ids; their links are copied by code from
               those records, never written by the model
  6. write     problems-<date>.jsonl; with --file, one issue per recurring problem in the private log
               (new members and a changed analysis are added as comments)

Exit 0 = clean, 1 = some model or GitHub calls failed (counted; retried next run), 2 = crashed.
Traces: feedback-collector/relate/<pair>, feedback-loop/analyse/<problem>.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import glob
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent))
import label_items as LI  # noqa: E402
import licences as LC  # noqa: E402
import relation_check as RC  # noqa: E402

OUT = Path(os.environ.get("FEEDBACK_OUT", Path.home() / "projects/data/feedback-collector"))
LOG_REPO = os.environ.get("FEEDBACK_LOG_REPO", "BrianMills2718/agent-feedback-log")
RULE_REPO = os.environ.get("FEEDBACK_RULE_REPO", "BrianMills2718/agentic-engineering-system-canonical")
PROJECT_META = Path(os.environ.get("PROJECT_META", Path.home() / "code/project-meta"))
NOTIFY_AT_IMPACT = 8.0  # an active licence at or above this impact also notifies Brian (attention, no decision)
ANALYSE_MODEL = RC.STRONG
MIN_SIMILARITY = 0.12
WORD = re.compile(r"[a-z][a-z0-9_]{3,}")
JOINS = ("supports", "same_problem")


def log(msg: str) -> None:
    print(f"[{dt.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------- load ----------
def load_records(out: Path, days: int) -> list[dict]:
    """Every record of every report in the window, with the report's session, day and issue."""
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    recs, seen = [], set()
    for f in sorted(glob.glob(str(out / "reports-*.jsonl"))):
        if Path(f).stem.split("-", 1)[1] < cutoff:
            continue
        for line in open(f):
            rep = json.loads(line)
            p = rep["provenance"]
            for r in rep.get("records", []):
                if r["id"] in seen:
                    continue
                seen.add(r["id"])
                recs.append(r | {"report_id": rep["id"], "session": p.get("session_id", ""),
                                 "day": (p.get("ts") or "")[:10], "issue": rep.get("filing", "")})
    return recs


def _words(text: str) -> set[str]:
    return set(WORD.findall(text.lower()))


def nearest_pairs(recs: list[dict]) -> list[tuple[int, int, float]]:
    """For each record, its most similar record from another report (one pair per unordered couple)."""
    words = [_words(r["text"]) for r in recs]
    pairs = {}
    for i, a in enumerate(recs):
        best = (0.0, -1)
        for j, b in enumerate(recs):
            if j == i or b["report_id"] == a["report_id"]:
                continue
            u = len(words[i] | words[j]) or 1
            best = max(best, (len(words[i] & words[j]) / u, j))
        if best[1] >= 0 and best[0] >= MIN_SIMILARITY:
            key = tuple(sorted((i, best[1])))
            pairs[key] = best[0]
    return [(i, j, s) for (i, j), s in sorted(pairs.items())]


# ---------- cache ----------
def open_db(out: Path) -> sqlite3.Connection:
    db = sqlite3.connect(out / "problems.sqlite")
    db.execute("CREATE TABLE IF NOT EXISTS family (record TEXT PRIMARY KEY, answer TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS relation (pair TEXT PRIMARY KEY, answer TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS problem (id TEXT PRIMARY KEY, issue TEXT, members TEXT, analysis TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS evidence (ref TEXT PRIMARY KEY, text TEXT)")
    return db


def pair_key(a: dict, b: dict) -> str:
    return "|".join(sorted((a["id"], b["id"])))


# ---------- 1. family ----------
def family(rec: dict, qs: dict, key: str) -> dict:
    links = " ".join(lk["ref"] for lk in rec["links"])
    r, err, _ = LI.ask({"learning": rec["text"][:1800], "recommended_action": links[:400]}, qs["question"], key)
    if err:
        return {"error": err}
    return LI.decide(r["answers"], qs) | {"cost": r.get("usage", {}).get("cost")}


# ---------- 2. relate ----------
def relate(a: dict, b: dict) -> dict:
    pair = {"pair_id": hashlib.sha256(pair_key(a, b).encode()).hexdigest()[:12],
            "a": RC._view(a), "b": RC._view(b), "label": "unrelated"}
    jev = RC.judge([pair], "jev")[0]
    out = {"jev": jev.get("relation"), "jev_p": jev.get("p"), "error": jev.get("error")}
    if jev.get("relation") == "challenges":
        strong = RC.judge([pair], "strong")[0]
        out |= {"confirmed_by": RC.STRONG, "strong": strong.get("relation"), "error": strong.get("error")}
        out["relation"] = strong.get("relation")
    else:
        out["relation"] = jev.get("relation")
    return out


# ---------- 3. group / 4. recurring ----------
def group(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, j in edges:
        parent[find(i)] = find(j)
    comps = collections.defaultdict(list)
    for i in range(n):
        comps[find(i)].append(i)
    return [sorted(c) for c in comps.values() if len(c) > 1]


def _evidence(lk: dict) -> str:
    """A comparable form of one link: an issue is its number when either side is bare (#270 = owner/repo#270)."""
    ref = lk["ref"]
    m = re.search(r"(?:#|/(?:issues|pull)/)(\d+)$", ref)
    return f"#{m.group(1)}" if m and lk["kind"] in ("issue", "url") else ref


def sightings(members: list[dict]) -> list[set[str]]:
    """Independent sightings (PLAN.md: two or more independent observations, each with a resolvable link).
    Only observations count, never claims or actions; each needs a link; and two sessions that cite the same
    evidence are one sighting, since a second session restating a filed issue is an echo, not a new sighting."""
    groups: list[tuple[set[str], set[str]]] = []  # (sessions, evidence)
    for r in members:
        if r["kind"] != "observation" or r["unprovenanced"]:
            continue
        ev = {_evidence(lk) for lk in r["links"]}
        who = {r["session"] or r["day"]}
        hits = [g for g in groups if g[1] & ev or g[0] & who]
        for g in hits:
            groups.remove(g)
            who |= g[0]
            ev |= g[1]
        groups.append((who, ev))
    return [g[0] for g in groups]


def problem_id(members: list[dict]) -> str:
    return "prob-" + hashlib.sha256(min(r["id"] for r in members).encode()).hexdigest()[:10]


# ---------- 5. analyse ----------
class _Step(BaseModel):
    text: str = Field(description="one plain sentence")
    basis: Literal["seen", "inferred", "guessed"]
    confidence: Literal["low", "medium", "high"]
    rests_on: list[str] = Field(description="ids of the member records this step rests on")


class _Fix(BaseModel):
    intent: Literal["Investigate", "Mitigate", "Repair", "Detect", "Prevent"]
    text: str = Field(description="one plain sentence naming the general change, not this one incident")
    rests_on: list[str]


class _Analysis(BaseModel):
    cause_chain: list[_Step]
    fixes: list[_Fix]


ANALYSE_PROMPT = """These records come from AI coding agents' feedback about one recurring problem. Each has an id, a kind, one sentence and its evidence links.
Work out the causal chain behind the problem, from the root cause to what the agents saw, and the general fix that would stop it recurring for any agent in any project (not a patch for one incident).
Rules: each step is ONE sentence and says how it is known (seen when a record states it, inferred when you reason from records, guessed otherwise) and which record ids it rests on. Use only what the records say; do not invent tools, files or numbers. Prefer a Prevent fix (a rule or design change that makes the failure impossible) or a Detect fix (a check or alert); add Investigate when the cause is not yet known.

RECORDS:
"""


_ISSUE_REF = re.compile(r"(?:github\.com/)?([\w.-]+/[\w.-]+)(?:#|/(?:issues|pull)/)(\d+)")


def read_evidence(members: list[dict], db: sqlite3.Connection, limit: int = 10) -> list[str]:
    """Title and opening text of the GitHub issues the records link to, read by code (cached): the records
    point at their evidence instead of retelling it, so the analyst reads it here."""
    out, seen = [], set()
    for r in members:
        for lk in r["links"]:
            m = _ISSUE_REF.search(lk["ref"]) if lk["kind"] in ("issue", "url") else None
            if not m or (m.group(1), m.group(2)) in seen or len(out) >= limit:
                continue
            seen.add((m.group(1), m.group(2)))
            ref = f"{m.group(1)}#{m.group(2)}"
            row = db.execute("SELECT text FROM evidence WHERE ref=?", (ref,)).fetchone()
            if row is None:
                p = subprocess.run(["gh", "api", f"repos/{m.group(1)}/issues/{m.group(2)}", "-q",
                                    '.title + "\n" + (.body // "")'], capture_output=True, text=True, timeout=30)
                text = p.stdout.strip()[:1500] if p.returncode == 0 else ""
                db.execute("INSERT OR REPLACE INTO evidence VALUES (?,?)", (ref, text))
                db.commit()
            else:
                text = row[0]
            if text:
                out.append(f"[{ref}] {text}")
    return out


def analyse(pid: str, members: list[dict], evidence: list[str] | None = None) -> tuple[dict | None, str | None, float]:
    from llm_client import call_llm_structured
    body = "\n".join(f"- {r['id']} ({r['kind']}{', ' + r['basis'] if r.get('basis') else ''}): {r['text']} "
                     f"[{', '.join(lk['ref'] for lk in r['links']) or 'no link'}]" for r in members[:40])
    if evidence:
        body += "\n\nLINKED EVIDENCE (read from the links; cite the record ids above, not these):\n" + "\n\n".join(evidence)
    try:
        res, meta = call_llm_structured(
            ANALYSE_MODEL, [{"role": "user", "content": ANALYSE_PROMPT + body}], response_model=_Analysis,
            reasoning_effort="medium", task="feedback-loop.analyse", trace_id=f"feedback-loop/analyse/{pid}",
            max_budget=0.25, model_justification="S3 problem analysis, stronger model per PLAN.md")
    except Exception as exc:
        return None, f"analyse {pid}: {type(exc).__name__}: {str(exc)[:200]}", 0.0
    ids = {r["id"]: r for r in members}

    def keep(items):
        out = []
        for it in items:
            rests = [x for x in it.rests_on if x in ids]
            links = []
            for x in rests:
                links += [lk for lk in ids[x]["links"] if lk not in links]
            out.append(it.model_dump() | {"rests_on": rests, "links": links, "unprovenanced": not links,
                                         "dropped_ids": [x for x in it.rests_on if x not in ids]})
        return out
    return {"cause_chain": keep(res.cause_chain), "fixes": keep(res.fixes), "model": ANALYSE_MODEL}, None, meta.cost or 0.0


# ---------- 6. write ----------
def issue_body(p: dict) -> str:
    lines = [f"Problem `{p['id']}`: {p['sightings']} independent sightings, {len(p['members'])} records.", "",
             "Records:"]
    for r in p["members"]:
        refs = " ".join(f"[{lk['ref']}]" for lk in r["links"]) or "**unprovenanced**"
        src = f" ([report]({r['issue']}))" if str(r.get("issue", "")).startswith("http") else ""
        lines.append(f"- {r['kind']}: {r['text']} {refs}  `{r['id']}`{src}")
    a = p.get("analysis")
    if a:
        lines += ["", f"Analysis ({a['model']}):", "", "Cause chain:"]
        for s in a["cause_chain"]:
            lines.append(f"- claim ({s['basis']}, {s['confidence']}): {s['text']} ← {', '.join(s['rests_on']) or 'nothing'}")
        lines += ["", "General fix:"]
        for f in a["fixes"]:
            lines.append(f"- action ({f['intent']}, proposed): {f['text']} ← {', '.join(f['rests_on']) or 'nothing'}")
    lines += ["", "```json", json.dumps({"problem": p["id"], "members": [r["id"] for r in p["members"]],
                                         "families": p["families"], "analysis": a}, ensure_ascii=False)[:40000], "```"]
    return "\n".join(lines)


def concern_closed_at(key: str) -> str:
    """When the rule's concern was closed as completed (the agent enforced it), else ""."""
    p = subprocess.run(["gh", "issue", "list", "--repo", RULE_REPO, "--state", "closed", "--search",
                        f'"concern-key: {key}" in:body', "--json", "closedAt,stateReason", "--limit", "1"],
                       capture_output=True, text=True, timeout=60)
    try:
        rows = json.loads(p.stdout or "[]")
    except ValueError:
        return ""
    return rows[0]["closedAt"] if rows and rows[0].get("stateReason") in ("COMPLETED", "completed") else ""


def rank(p: dict) -> tuple:
    """Impact first (independent sightings, sessions, records), then uncertainty (no analysis, inferred or
    guessed steps, no licence yet): high impact with high uncertainty sorts to the top (PLAN.md, What Brian sees)."""
    sessions = len({r["session"] for r in p["members"]})
    impact = 3 * p["sightings"] + sessions + len(p["members"]) / 10
    a = p.get("analysis") or {}
    shaky = sum(1 for x in a.get("cause_chain", []) if x["basis"] != "seen")
    uncertainty = (0 if a else 3) + shaky + (0 if p.get("licence") == "active" else 2)
    return (round(impact, 1), uncertainty)


def render_view(problems: list[dict], day: str) -> str:
    rows = sorted(problems, key=lambda p: rank(p), reverse=True)
    lines = [f"# Agent feedback: problems by impact, then uncertainty", "",
             f"Rebuilt {day} by `scripts/learning_loop/problems.py` (AES canonical, plan aes-learning-loop). "
             "Impact = 3 x independent sightings + sessions + records/10. Uncertainty = no analysis (3) + "
             "inferred or guessed cause steps + no active licence (2). Nothing here asks for a decision.", "",
             "| Impact | Uncertainty | Sightings | Problem | Families | Issue |", "| --- | --- | --- | --- | --- | --- |"]
    for p in rows:
        imp, unc = rank(p)
        a = p.get("analysis") or {}
        head = (a.get("fixes") or [{}])[0].get("text") or p["members"][0]["text"]
        issue = f"[issue]({p['issue']})" if str(p.get("issue", "")).startswith("http") else ""
        lines.append(f"| {imp} | {unc} | {p['sightings']} | {head[:160].replace('|', '/')} | "
                     f"{', '.join(p['families'])} | {issue} |")
    return "\n".join(lines) + "\n"


def put_view(text: str, day: str) -> str:
    import base64
    sha = subprocess.run(["gh", "api", f"repos/{LOG_REPO}/contents/VIEW.md", "-q", ".sha"],
                         capture_output=True, text=True, timeout=30).stdout.strip()
    body = {"message": f"VIEW.md rebuilt {day}", "content": base64.b64encode(text.encode()).decode()}
    if sha:
        body["sha"] = sha
    p = subprocess.run(["gh", "api", "-X", "PUT", f"repos/{LOG_REPO}/contents/VIEW.md", "--input", "-",
                        "-q", ".content.html_url"], input=json.dumps(body), capture_output=True, text=True, timeout=60)
    if p.returncode:
        raise RuntimeError(f"VIEW.md put exit {p.returncode}: {p.stderr.strip()[-300:]}")
    return p.stdout.strip()


def gh_issue(args: list[str], body: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write(body)
    try:
        p = subprocess.run(["gh", *args, "--body-file", fh.name], capture_output=True, text=True, timeout=60)
        if p.returncode:
            raise RuntimeError(f"gh exit {p.returncode}: {(p.stderr or p.stdout).strip()[-300:]}")
        return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    finally:
        os.unlink(fh.name)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--file", action="store_true", help="create or update problem issues in the private log")
    ap.add_argument("--max-analyse", type=int, default=3, help="stronger-model analyses per run (PLAN.md spend cap)")
    a = ap.parse_args()
    timing, counts, errors = {}, collections.Counter(), []

    def step(name, fn):
        t0 = time.perf_counter()
        r = fn()
        timing[name] = round(time.perf_counter() - t0, 1)
        log(f"step {name}: {timing[name]}s")
        return r

    db = open_db(OUT)
    recs = step("load", lambda: load_records(OUT, a.days))
    counts["records"] = len(recs)

    qs, key = LI.question_set(), LI.api_key()

    def families_all():
        for r in recs:
            if r["kind"] == "action":
                continue
            row = db.execute("SELECT answer FROM family WHERE record=?", (r["id"],)).fetchone()
            if row:
                r["family"] = json.loads(row[0])
                continue
            ans = family(r, qs, key)
            counts["family_calls"] += 1
            if "error" in ans:
                errors.append(f"family {r['id']}: {ans['error']}")
                continue
            r["family"] = ans
            counts["cost_family_micro"] += int((ans.get("cost") or 0) * 1e6)
            db.execute("INSERT OR REPLACE INTO family VALUES (?,?)", (r["id"], json.dumps(ans)))
        db.commit()
    step("family", families_all)

    challenged: set[int] = set()

    def relate_all():
        edges = []
        for i, j, sim in nearest_pairs(recs):
            k = pair_key(recs[i], recs[j])
            row = db.execute("SELECT answer FROM relation WHERE pair=?", (k,)).fetchone()
            if row:
                ans = json.loads(row[0])
            else:
                ans = relate(recs[i], recs[j])
                counts["relate_calls"] += 1
                if ans.get("error") or ans.get("relation") is None:
                    errors.append(f"relate {k}: {ans.get('error')}")
                    continue
                db.execute("INSERT OR REPLACE INTO relation VALUES (?,?)", (k, json.dumps(ans | {"similarity": sim})))
            counts[f"relation_{ans['relation']}"] += 1
            counts["challenges_confirmed"] += ans.get("confirmed_by") is not None and ans["relation"] == "challenges"
            if ans["relation"] in JOINS:
                edges.append((i, j))
            elif ans["relation"] == "challenges":
                challenged.update((i, j))
        db.commit()
        return edges
    edges = step("relate", relate_all)

    problems = []
    for comp in group(len(recs), edges):
        members = [recs[i] for i in comp]
        fams = collections.Counter(f for r in members for f in (r.get("family") or {}).get("families", []))
        problems.append({"id": problem_id(members), "members": members, "sightings": len(sightings(members)),
                         "families": [f for f, _ in fams.most_common(3)]})
    recurring = [p for p in problems if p["sightings"] >= 2]
    recurring.sort(key=lambda p: (-p["sightings"], -len(p["members"])))
    counts["problems"], counts["problems_recurring"] = len(problems), len(recurring)

    def analyse_all():
        done = 0
        for p in recurring:
            members_key = ",".join(sorted(r["id"] for r in p["members"]))
            row = db.execute("SELECT members, analysis FROM problem WHERE id=?", (p["id"],)).fetchone()
            if row and row[0] == members_key and row[1]:
                p["analysis"] = json.loads(row[1])
                continue
            if done >= a.max_analyse:
                p["analysis_deferred"] = "spend cap"
                counts["analyse_deferred"] += 1
                continue
            ev = read_evidence(p["members"], db)
            counts["evidence_read"] += len(ev)
            res, err, cost = analyse(p["id"], p["members"], ev)
            done += 1
            counts["cost_analyse_micro"] += int(cost * 1e6)
            if err:
                errors.append(err)
                continue
            p["analysis"] = res
    step("analyse", analyse_all)

    index = {r["id"]: n for n, r in enumerate(recs)}

    def licence_all():
        for p in recurring:
            if not p.get("analysis"):
                continue
            hit = any(index[r["id"]] in challenged for r in p["members"])
            try:
                p["licences"] = LC.licences_for(p, hit)
            except Exception as exc:
                errors.append(f"licence {p['id']}: {type(exc).__name__}: {str(exc)[:200]}")
                continue
            p["licence"] = "active" if any(x["status"] == "active" for x in p["licences"]) else \
                (p["licences"][0]["status"] if p["licences"] else "none")
            for x in p["licences"]:
                counts[f"licence_{x['status']}"] += 1
    step("licence", licence_all)

    def hand_to_agents():
        """Active licences become keyed concerns in the agent work queue (an agent adopts the rule through
        company planning, or the check into the audit skill); Brian is notified of high-impact ones."""
        if not a.file:
            return
        for p in recurring:
            for x in p.get("licences", []):
                if x["status"] != "active":
                    continue
                key = f"feedback-rule-{p['id']}-{hashlib.sha256(x['text'].encode()).hexdigest()[:8]}"
                route = "a rule adopted through company planning (aes plan prepare)" if x["intent"] == "Prevent" \
                    else "a check added to the audit skill"
                body = (f"The feedback loop licensed a general fix for a recurring problem ({p['sightings']} independent "
                        f"sightings; licence derived `active` by the Observation-to-Action evaluator).\n\n"
                        f"Fix ({x['intent']}): {x['text']}\n\nAdopt it as {route}, by your best judgment; record the "
                        f"observation pattern it should stop, so the nightly effect count can revoke it.\n\n"
                        f"Problem, records and analysis: {p.get('issue') or 'private feedback log'}")
                cp = subprocess.run([sys.executable, str(PROJECT_META / "scripts/concern_issue.py"), "open",
                                     "--repo", RULE_REPO, "--key", key, "--title", f"Feedback loop: adopt {x['intent'].lower()} — {x['text'][:90]}",
                                     "--body", body, "--source", "feedback-loop", "--occurrence", key],
                                    capture_output=True, text=True, timeout=120)
                if cp.returncode:
                    errors.append(f"concern {key}: {(cp.stderr or cp.stdout).strip()[-200:]}")
                    continue
                counts["concerns_opened"] += 1
                if rank(p)[0] >= NOTIFY_AT_IMPACT:
                    subprocess.run([sys.executable, str(PROJECT_META / "scripts/operator_notify_router.py"),
                                    "--severity", "attention", "--key", key, "--state", "licensed",
                                    "--source", "feedback-loop", "--title", "Feedback loop handed agents a new rule",
                                    "--body", f"{x['text'][:200]} ({p['sightings']} separate sightings)."],
                                   capture_output=True, text=True, timeout=120)
                    counts["notified"] += 1
    step("hand_to_agents", hand_to_agents)

    def effects():
        """S5: for each licensed rule an agent has enforced (its concern closed as completed), count the problem's
        sightings before and after enforcement; a new independent sighting afterwards revokes the licence."""
        day = dt.date.today().isoformat()
        rows = []
        for p in recurring:
            for x in p.get("licences", []):
                if x["status"] != "active":
                    continue
                key = f"feedback-rule-{p['id']}-{hashlib.sha256(x['text'].encode()).hexdigest()[:8]}"
                enforced = concern_closed_at(key)
                if not enforced:
                    continue
                before = [r for r in p["members"] if r["day"] and r["day"] < enforced[:10]]
                after = [r for r in p["members"] if r["day"] and r["day"] >= enforced[:10]]
                new_sightings = sightings(after)
                row = {"day": day, "rule": key, "problem": p["id"], "enforced_at": enforced,
                       "sightings_before": len(sightings(before)), "sightings_after": len(new_sightings),
                       "matched_after": [{"id": r["id"], "text": r["text"], "links": r["links"]} for r in after]}
                if new_sightings:
                    x["status"] = LC.derive(LC.fixture_for(p, {"text": x["text"], "rests_on": [], "intent": x["intent"]},
                                                           False, revoked=True))
                    row["revoked"] = x["status"] == "revoked"
                    counts["licence_revoked"] += row["revoked"]
                    if a.file and row["revoked"]:
                        subprocess.run([sys.executable, str(PROJECT_META / "scripts/concern_issue.py"), "open",
                                        "--repo", RULE_REPO, "--key", key, "--title", f"Feedback loop: rule did not stop its failure",
                                        "--body", f"The failure recurred after enforcement ({len(new_sightings)} new sighting(s)); "
                                                  f"the licence derives revoked. Problem: {p.get('issue') or p['id']}",
                                        "--source", "feedback-loop", "--occurrence", f"{key}-revoked-{day}"],
                                       capture_output=True, text=True, timeout=120)
                        subprocess.run([sys.executable, str(PROJECT_META / "scripts/operator_notify_router.py"),
                                        "--severity", "attention", "--key", key, "--state", "revoked", "--source", "feedback-loop",
                                        "--title", "A feedback-loop rule did not stop its failure",
                                        "--body", f"{x['text'][:200]} — the failure came back; agents are reworking it."],
                                       capture_output=True, text=True, timeout=120)
                rows.append(row)
                counts["rules_enforced"] += 1
        if rows:
            with open(OUT / f"effects-{day}.jsonl", "a") as fh:
                for row in rows:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    step("effects", effects)

    def write_all():
        day = dt.date.today().isoformat()
        with open(OUT / f"problems-{day}.jsonl", "a") as fh:
            for p in recurring:
                fh.write(json.dumps(p, ensure_ascii=False) + "\n")
        for p in recurring:
            members_key = ",".join(sorted(r["id"] for r in p["members"]))
            row = db.execute("SELECT issue, members FROM problem WHERE id=?", (p["id"],)).fetchone()
            issue = row[0] if row else ""
            if a.file and "analysis" in p:
                try:
                    if not issue:
                        title = f"Problem ({p['sightings']} sightings): {p['analysis']['cause_chain'][-1]['text'] if p['analysis']['cause_chain'] else p['members'][0]['text']}"[:200]
                        issue = gh_issue(["issue", "create", "--repo", LOG_REPO, "--title", title, "--label", "problem"], issue_body(p))
                        counts["issues_created"] += 1
                    elif row[1] != members_key:
                        gh_issue(["issue", "comment", issue, "--repo", LOG_REPO], "Updated:\n\n" + issue_body(p))
                        counts["issues_updated"] += 1
                except Exception as exc:
                    errors.append(f"issue {p['id']}: {str(exc)[:200]}")
                    continue
            db.execute("INSERT OR REPLACE INTO problem VALUES (?,?,?,?)",
                       (p["id"], issue, members_key, json.dumps(p.get("analysis")) if p.get("analysis") else ""))
            p["issue"] = issue
        db.commit()
    step("write", write_all)

    def view():
        day = dt.date.today().isoformat()
        text = render_view(problems, day)
        (OUT / "VIEW.md").write_text(text)
        if a.file:
            try:
                summary_view.append(put_view(text, day))
            except Exception as exc:
                errors.append(str(exc)[:200])
    summary_view: list[str] = []
    step("view", view)

    summary = {"run": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "timing_s": timing,
               "counts": dict(sorted(counts.items())), "errors": len(errors), "error_samples": errors[:5],
               "cost_usd": round((counts["cost_family_micro"] + counts["cost_analyse_micro"]) / 1e6, 4),
               "view": summary_view[0] if summary_view else str(OUT / "VIEW.md"),
               "recurring": [{"id": p["id"], "sightings": p["sightings"], "members": len(p["members"]),
                              "issue": p.get("issue", ""), "families": p["families"], "licence": p.get("licence", "")}
                             for p in recurring]}
    with open(OUT / "problems-runs.jsonl", "a") as fh:
        fh.write(json.dumps(summary) + "\n")
    print(json.dumps(summary, indent=1))
    log(f"RESULT records={len(recs)} problems={len(problems)} recurring={len(recurring)} errors={len(errors)} "
        f"cost=${summary['cost_usd']} exit={1 if errors else 0}")
    return 1 if errors else 0


def alert(code: int, detail: str) -> None:
    subprocess.run([sys.executable, str(PROJECT_META / "scripts/notify_operator.py"), "--key", "feedback-problems-failed",
                    "--severity", "agent", "--source", "feedback-loop", "--title", f"Weekly feedback loop exited {code}",
                    "--body", f"{detail[-1500:]}\nRun log: {OUT}/problems-runs.jsonl; journal: journalctl --user -u feedback-problems"],
                   timeout=120)


if __name__ == "__main__":
    import traceback
    try:
        rc, detail = main(), "some model, GitHub or licence calls failed; see error_samples in problems-runs.jsonl"
    except Exception:
        rc, detail = 2, traceback.format_exc()
        print(detail, file=sys.stderr)
    if rc and "--file" in sys.argv:
        try:
            alert(rc, detail)
        except Exception as exc:
            print(f"ALERT FAILED: {exc}", file=sys.stderr)
    sys.exit(rc)
