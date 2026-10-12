"""Weekly owner for the fixes the feedback loop licenses (plan aes-learning-loop, S6).

problems.py opens one "Feedback loop: adopt ..." concern per licensed fix and stops
there; until 2026-10-11 nobody owned them (19 open, 1 enforced). This hands a
bounded batch to one headless Claude Code session, which for each item either
lands the change through a sanctioned lane and adds the enforcement receipt that
effects.py counts, or closes it with a stated reason. Then this script checks
every handed item on GitHub itself, never the agent's own summary, and fails
loudly when one has no valid disposition.

Output (never committed; may quote private records):
  $FEEDBACK_OUT/fix-owner-<date>.jsonl   the session's full stream-json trace
  $FEEDBACK_OUT/fix-owner-runs.jsonl     one line per run: items, dispositions, checks
Exit 0 = every handed item has a valid disposition, 1 = some do not, 2 = crashed.
Non-zero opens a keyed agent concern via notify_operator.py.

  python scripts/learning_loop/fix_owner.py [--max-items 3] [--issue N] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import effects as EF  # noqa: E402

RULE_REPO = "BrianMills2718/agentic-engineering-system-canonical"
OUT = Path(os.environ.get("FEEDBACK_OUT", Path.home() / "projects/data/feedback-collector"))
PROJECT_META = Path(os.environ.get("PROJECT_META", Path.home() / ".hive-brain/project-meta"))
ATTEMPT = "<!-- fix-owner-attempt "
DISPOSITION = "<!-- fix-owner-disposition "
RETRY_AFTER = dt.timedelta(days=6)

PROMPT = """You are the weekly owner of fixes the feedback loop licensed. Each item below is an
open GitHub issue in {repo} titled "Feedback loop: adopt ...". Nobody else works these.
Read the workspace AGENTS.md rules that already load for you; they govern (plans, lanes,
commit tags, local checks as merge gate, never bypass hooks, no secrets).

Handle the items in this order: first any whose fix changes how agents are instructed or
checked (AGENTS.md files, skills, hooks, the Jev gate, company-planning checks), then the
rest oldest first. For EACH item, read the issue and the linked problem issue, then choose
exactly one disposition and carry it out:

1. implemented - the fix is a bounded, reversible change in a repository Brian owns.
   Work in that repository's sanctioned lane (its AGENTS.md names it: `make maintenance-worktree`
   or a claimed `git worktree`), under a plan when the change is non-trivial, run the
   repository's own checks, open a PR, merge it after the checks pass, and close the lane
   through its session-close route. Then comment on the item with BOTH an enforcement receipt
   and a disposition marker, and close it as completed:
     <!-- feedback-enforcement {{"enforced_at":"<UTC now, ISO 8601 with Z>","revision":"<merged commit sha>","verification":"<PR or check-output link>"}} -->
     <!-- fix-owner-disposition {{"disposition":"implemented","reason":"<one sentence>"}} -->
   plus one plain sentence of what changed and what observation pattern it should stop.
   `gh issue close N -R {repo} --reason completed`.
2. already_enforced - an existing check or rule already does this. Same receipt, pointing at
   the existing revision and the proof it runs; disposition "already_enforced"; close completed.
3. declined - the fix is wrong, a duplicate of another item (name it), too vague to act on, or
   would cost more than the recurrence it prevents. Comment the disposition marker with the
   reason and close with `--reason "not planned"`. No receipt.
4. deferred - only when it is right but blocked on something you cannot do in this session
   (access, another writer's active claim, a decision only Brian can make). Comment the
   disposition marker naming the exact blocker; leave it open.

If plan adoption refuses with stale_source_revision, that is a known install defect
(company-planning#136): commit under the plan you wrote (the commit rule is in observe mode) and
say so in the item comment rather than deferring the item for it.

Posting comments: end every comment body with a line `Trace-Review: none (<why no graded run>)`
(or the path of a committed trace review); the publishing hook blocks `gh issue comment` without it.
A blocked command runs none of its parts, including file writes earlier in it. After each comment,
read it back (`gh issue view N --json comments`) and confirm both markers are present before you
close the issue; this script checks the same thing afterwards and fails the run on any mismatch.

Stop after these {n} items. Do not start other work. Never force-push, delete branches or
history, publish, deploy, send anything outward, or spend money beyond this session.
Finish with one line, exactly: FIX_OWNER_SUMMARY {{"<issue number>":"<disposition>", ...}}

Items:
{items}
"""


def gh_json(*args: str) -> object:
    p = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if p.returncode:
        raise RuntimeError(f"gh {' '.join(args[:3])}: {p.stderr.strip()[-300:]}")
    return json.loads(p.stdout)


def marker(body: str, mark: str) -> dict | None:
    start = body.find(mark)
    end = body.find("-->", start + len(mark))
    if start < 0 or end < 0:
        return None
    try:
        return json.loads(body[start + len(mark):end])
    except ValueError:
        return None


def candidates(only: int | None, now: dt.datetime) -> list[dict]:
    if only:
        return [gh_json("issue", "view", str(only), "-R", RULE_REPO, "--json", "number,title,createdAt,comments")]
    rows = gh_json("issue", "list", "-R", RULE_REPO, "--state", "open", "--label", "source:feedback-loop",
                   "--limit", "100", "--json", "number,title,createdAt,comments")
    fresh = []
    for r in sorted(rows, key=lambda r: r["createdAt"]):
        # Only a recent `deferred` decision waits; an attempt that left no decision (a crash,
        # blocked tools) is retried on the next run.
        deferred = [EF.timestamp(c["createdAt"]) for c in r["comments"]
                    if (marker(c.get("body", ""), DISPOSITION) or {}).get("disposition") == "deferred"]
        if any(t and now - t < RETRY_AFTER for t in deferred):
            continue
        fresh.append(r)
    return fresh


def check(number: int) -> dict:
    """What GitHub shows for one handed item: the only evidence this script trusts."""
    issue = gh_json("issue", "view", str(number), "-R", RULE_REPO, "--json", "state,stateReason,comments")
    comments = issue["comments"]
    disp = next((d for c in reversed(comments) if (d := marker(c.get("body", ""), DISPOSITION))), None)
    receipt = EF.enforcement_receipt(comments)
    state, reason = issue["state"], (issue.get("stateReason") or "").lower()
    kind = (disp or {}).get("disposition")
    if kind in ("implemented", "already_enforced"):
        ok = state == "CLOSED" and reason == "completed" and receipt is not None
    elif kind == "declined":
        ok = state == "CLOSED" and reason == "not_planned" and bool(disp.get("reason"))
    elif kind == "deferred":
        ok = state == "OPEN" and bool(disp.get("reason"))
    else:
        ok = False
    return {"issue": number, "state": state, "state_reason": reason, "disposition": kind,
            "reason": (disp or {}).get("reason"), "receipt": receipt, "valid": ok}


def comment_attempt(number: int, now: dt.datetime, trace: Path) -> None:
    body = (f"{ATTEMPT}{json.dumps({'at': now.isoformat(), 'trace': str(trace)})} -->\n"
            "Weekly fix owner picked this up (`scripts/learning_loop/fix_owner.py`).")
    subprocess.run(["gh", "issue", "comment", str(number), "-R", RULE_REPO, "--body", body],
                   capture_output=True, text=True, timeout=60, check=True)


def run(a: argparse.Namespace) -> int:
    now = dt.datetime.now(dt.timezone.utc)
    picked = candidates(a.issue, now)[: a.max_items]
    trace = OUT / f"fix-owner-{now.date().isoformat()}.jsonl"
    record = {"started": now.isoformat(), "picked": [r["number"] for r in picked], "trace": str(trace)}
    print(f"fix-owner picked={record['picked']} open_candidates_shown_to_agent={len(picked)}", flush=True)
    if a.dry_run or not picked:
        record.update(result="dry-run" if a.dry_run else "nothing-to-do", exit=0)
        _log(record)
        print(f"RESULT fix-owner picked={len(picked)} exit=0 ({record['result']})")
        return 0
    for r in picked:
        comment_attempt(r["number"], now, trace)
    items = "\n".join(f"- #{r['number']} {r['title']} (https://github.com/{RULE_REPO}/issues/{r['number']})"
                      for r in picked)
    prompt = PROMPT.format(repo=RULE_REPO, n=len(picked), items=items)
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "bypassPermissions", "--max-budget-usd", str(a.max_budget_usd)]
    t0 = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    with trace.open("a") as fh:
        p = subprocess.run(cmd, cwd=Path.home() / "code", stdout=fh, stderr=subprocess.STDOUT, text=True)
    record["agent_exit"], record["agent_seconds"] = p.returncode, round(time.monotonic() - t0)
    record["agent_summary"], record["session_id"] = _summary(trace)
    record["checks"] = [check(r["number"]) for r in picked]
    bad = [c["issue"] for c in record["checks"] if not c["valid"]]
    record["exit"] = 1 if bad or p.returncode else 0
    _log(record)
    for c in record["checks"]:
        print(f"  #{c['issue']} disposition={c['disposition']} state={c['state']}/{c['state_reason'] or '-'} "
              f"receipt={'yes' if c['receipt'] else 'no'} valid={c['valid']}")
    print(f"RESULT fix-owner picked={len(picked)} valid={len(picked) - len(bad)} invalid={len(bad)} "
          f"agent_exit={p.returncode} seconds={record['agent_seconds']} exit={record['exit']}")
    if record["exit"] and not a.no_alert:
        alert(record["exit"], f"Items without a valid disposition: {bad}; agent exit {p.returncode}. Trace: {trace}")
    return record["exit"]


def _summary(trace: Path) -> tuple[dict | None, str | None]:
    summary = session = None
    for line in trace.read_text(errors="replace").splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        session = ev.get("session_id") or session
        if ev.get("type") == "result" and "FIX_OWNER_SUMMARY " in (ev.get("result") or ""):
            tail = ev["result"].split("FIX_OWNER_SUMMARY ", 1)[1].splitlines()[0]
            try:
                summary = json.loads(tail)
            except ValueError:
                summary = {"unparsed": tail[:300]}
    return summary, session


def _log(record: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "fix-owner-runs.jsonl").open("a") as fh:
        fh.write(json.dumps(record, default=str) + "\n")


def alert(code: int, detail: str) -> None:
    subprocess.run([sys.executable, str(PROJECT_META / "scripts/notify_operator.py"), "--key", "feedback-fix-owner-failed",
                    "--severity", "agent", "--source", "feedback-fix-owner",
                    "--title", f"Weekly feedback fix owner exited {code}",
                    "--body", f"{detail[-1500:]}\nRun log: {OUT}/fix-owner-runs.jsonl; journal: journalctl --user -u feedback-fix-owner"],
                   timeout=120)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--max-items", type=int, default=3)
    ap.add_argument("--issue", type=int, help="handle exactly this issue")
    ap.add_argument("--max-budget-usd", type=float, default=20.0)
    ap.add_argument("--dry-run", action="store_true", help="list what would be handed, change nothing")
    ap.add_argument("--no-alert", action="store_true")
    a = ap.parse_args(argv)
    try:
        return run(a)
    except Exception as exc:  # crash: still fail loudly to an agent
        print(f"RESULT fix-owner crashed={exc!r} exit=2")
        if not a.no_alert:
            alert(2, repr(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
