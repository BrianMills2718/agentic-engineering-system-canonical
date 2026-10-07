#!/usr/bin/env python3
"""Nightly review of commits that passed the AES commit rule on form alone (plan aes-planning).

The commit rule is deterministic: ``[Unplanned]`` passes with any ``Emergency:`` line, and
``[Trivial]`` passes on file and line counts. Whether the emergency was real, or the "trivial"
change alters behaviour, is a question about meaning, so a light model judges it here, after
the fact, and never blocks a commit.

Each run, for one day (default: yesterday):

1. reads every repository's observe/enforce log (``daily_report.log_rows``) and keeps the
   accepted ``[Unplanned]`` and ``[Trivial]`` commits;
2. finds each commit by its subject in that repository's history for the day, and sends its
   message, file list and the first part of its diff to Jev (``llm_client.call_decisions``,
   OpenRouter) with one two-way choice;
3. appends one line per judged commit to ``~/.local/state/aes/commit-misuse-review.jsonl``
   (choice, probabilities, cost) and prints a summary with counts;
4. opens or updates the keyed concern ``aes-commit-tag-misuse`` listing commits judged misuse
   with probability at or above ``FLAG_P``.

Report-only: Jev's labels have not been spot-checked on this question yet (the learning loop's
first night filed junk at p=0.98), so a flag is a lead for an agent to read, not a verdict.

Exit status: 0 when every found commit was judged (commits with no reachable SHA are counted
as skipped), 1 when any git or model call failed (the
failures are listed and a concern is opened), 2 on a crash.

  uv run --no-project --with-editable ~/code/llm_client python \\
      proposals/aes-planning/rollout/misuse_review.py [--day 2026-10-07] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import daily_report  # noqa: E402  (log_rows, run, concern, WORKSPACE)

JEV = "openrouter/typesafe/jev-1.13"
STATE = Path.home() / ".local" / "state" / "aes" / "commit-misuse-review.jsonl"
FLAG_P = 0.8
DIFF_CHARS = 3000
# Never send these files' contents to the model; their names still appear in the file list.
SECRETISH = re.compile(r"(^|/)(\.env[^/]*|[^/]*(secret|credential|token|api_key)[^/]*|id_[a-z0-9]+|[^/]*\.pem)$", re.I)

QUESTIONS = {
    "Unplanned": ("emergency", "ordinary_work", (
        "This commit was tagged [Unplanned], which the commit rule reserves for emergencies: something "
        "broken or at risk that could not wait for a plan. Judge from the message, the files and the diff "
        "whether it is such an emergency or ordinary work that should have gone through a plan."), {
        "emergency": "fixes or contains something broken, failing, leaking or at immediate risk, and waiting for a plan would have cost real harm",
        "ordinary_work": "a feature, refactor, test, cleanup, documentation or other change that could have waited for a plan",
    }),
    "Trivial": ("no_behavior_change", "behavior_change", (
        "This commit was tagged [Trivial], which the commit rule allows only for changes that do not alter how "
        "anything behaves. Judge from the files and the diff whether running code, configuration values, prompts, "
        "rules, schedules or agent instructions now behave differently."), {
        "no_behavior_change": "wording, typo, formatting, comments, documentation or records only; nothing runs differently",
        "behavior_change": "changes logic, a configuration value, a prompt, a rule, a threshold, a schedule, a dependency or any instruction an agent or program follows",
    }),
}


def find_commit(repo: Path, subject: str, day: dt.date) -> str | None:
    """The commit in `repo` made on `day` whose subject is `subject` (logs carry no SHA: the
    commit-msg hook runs before the commit exists)."""
    # explicit times: git reads a bare date as that date at the current time of day; a day either
    # side covers time zones (the log stamps UTC, git compares in local time)
    since = f"{(day - dt.timedelta(days=1)).isoformat()} 00:00"
    until = f"{(day + dt.timedelta(days=2)).isoformat()} 00:00"
    out = daily_report.run("git", "-C", str(repo), "log", "--all", f"--since={since}", f"--until={until}",
                           "--format=%H%x00%s").stdout
    lines = [line.partition("\x00")[::2] for line in out.splitlines()]
    for sha, subj in lines:
        if subj == subject:
            return sha
    # a branch commit squash-merged on GitHub reappears on main as "<subject> (#N)"
    squashed = re.compile(re.escape(subject) + r" \(#\d+\)$")
    for sha, subj in lines:
        if squashed.match(subj):
            return sha
    return None


def commit_state(repo: Path, sha: str) -> dict:
    run = daily_report.run
    message = run("git", "-C", str(repo), "show", "-s", "--format=%B", sha).stdout.strip()
    files = run("git", "-C", str(repo), "show", "--format=", "--name-status", sha).stdout.split("\n")
    files = [f for f in files if f.strip()]
    sendable = [f.split("\t")[-1] for f in files if not SECRETISH.search(f.split("\t")[-1])]
    diff = run("git", "-C", str(repo), "show", "--format=", "--unified=2", sha, "--", *sendable).stdout if sendable else ""
    return {"repository": repo.name, "message": message[:2000], "files": files[:60],
            "diff": diff[:DIFF_CHARS] + ("\n[diff truncated]" if len(diff) > DIFF_CHARS else "")}


def judge(tag: str, state: dict, trace_id: str) -> dict:
    from llm_client import ChoiceQuestion, call_decisions

    ok_choice, misuse_choice, instructions, criteria = QUESTIONS[tag]
    r = call_decisions(JEV, state=state, questions={"use": ChoiceQuestion(instructions, criteria)},
                       task="aes-commit-rule.misuse-review", trace_id=trace_id, max_budget=0.01)
    a = r.answers["use"]
    p_misuse = round(a.probabilities.get(misuse_choice, 0.0), 3)
    return {"choice": a.choice, "p_misuse": p_misuse, "misuse": a.choice == misuse_choice and p_misuse >= FLAG_P,
            "probabilities": {k: round(v, 3) for k, v in a.probabilities.items()}, "cost": r.cost}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--day", type=dt.date.fromisoformat, default=dt.date.today() - dt.timedelta(days=1))
    ap.add_argument("--dry-run", action="store_true", help="list the commits that would be judged; no model calls, no concern")
    args = ap.parse_args()
    started = time.perf_counter()
    seen: set[tuple[str, str]] = set()
    picked = []
    for repo_name, e in daily_report.log_rows(args.day):
        tag = str(e.get("tag"))
        if e.get("verdict") != "accept" or tag not in QUESTIONS or (repo_name, e.get("subject")) in seen:
            continue
        seen.add((repo_name, e.get("subject")))
        picked.append((repo_name, tag, e.get("subject", "")))
    print(f"misuse review {args.day}: {len(picked)} accepted [Unplanned]/[Trivial] commit(s) to judge")
    rows, failures, skipped, flagged, cost = [], [], [], [], 0.0
    judged_shas: set[str] = set()
    for repo_name, tag, subject in picked:
        repo = daily_report.WORKSPACE / repo_name
        sha = find_commit(repo, subject, args.day)
        # Not found is normal, not a failure: smoke tests whose commit was never made, and commits
        # on branches later squashed or deleted. Two folders holding one repository share a SHA.
        if sha is None or sha in judged_shas:
            skipped.append(f"{repo_name}: {'same commit as another folder' if sha else 'no reachable commit'}: {subject[:80]}")
            continue
        judged_shas.add(sha)
        if args.dry_run:
            print(f"  would judge {repo_name} {sha[:8]} [{tag}] {subject[:80]}")
            continue
        t0 = time.perf_counter()
        try:
            verdict = judge(tag, commit_state(repo, sha), f"aes-commit-misuse/{args.day}/{repo_name}/{sha[:12]}")
        except Exception as exc:  # one failed call must not hide the rest; it is counted and reported
            failures.append(f"{repo_name} {sha[:8]}: {type(exc).__name__}: {str(exc)[:200]}")
            continue
        cost += verdict["cost"] or 0.0
        row = {"day": args.day.isoformat(), "repository": repo_name, "sha": sha, "tag": tag, "subject": subject,
               **verdict, "seconds": round(time.perf_counter() - t0, 2)}
        rows.append(row)
        if row["misuse"]:
            flagged.append(row)
        print(f"  {'FLAG' if row['misuse'] else 'ok  '} {repo_name} {sha[:8]} [{tag}] {row['choice']} "
              f"p_misuse={row['p_misuse']} {row['seconds']}s  {subject[:70]}")
    if not args.dry_run and rows:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        with STATE.open("a", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")
    print(f"judged={len(rows)} flagged={len(flagged)} skipped={len(skipped)} failed={len(failures)} cost=${cost:.4f} "
          f"elapsed={time.perf_counter() - started:.1f}s log={STATE}")
    for f in skipped:
        print(f"  skipped: {f}")
    for f in failures:
        print(f"  failed: {f}")
    if args.dry_run:
        return 1 if failures else 0
    if flagged:
        table = "\n".join(f"| {r['repository']} | `{r['sha'][:8]}` | [{r['tag']}] | {r['choice']} ({r['p_misuse']}) | {r['subject'][:90]} |"
                          for r in flagged)
        print(daily_report.concern(
            "aes-commit-tag-misuse", "Commits that passed the AES commit rule but may misuse their tag",
            f"Light-model review of {args.day} (Jev, report-only; a flag is a lead to read, not a verdict).\n\n"
            f"| Repository | Commit | Tag | Judged | Subject |\n|---|---|---|---|---|\n{table}\n\n"
            "For each: read the commit. If the tag was wrong, tell the agent or owner that made it (the plan "
            "route is `[Goal <id>]` under an adopted plan); if the model was wrong, note it in this issue so "
            "the question can be tuned (proposals/aes-planning/rollout/misuse_review.py). Every judged commit: "
            f"`{STATE}`.", occurrence=f"misuse:{args.day}:" + ",".join(sorted(r["sha"][:8] for r in flagged))))
    if failures:
        print(daily_report.concern(
            "aes-commit-misuse-review-failed", "AES commit misuse review could not judge every commit",
            f"Run for {args.day}: {len(failures)} failure(s).\n\n" + "\n".join(f"- {f}" for f in failures),
            occurrence=f"failed:{args.day}:{len(failures)}"))
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        print(daily_report.concern("aes-commit-misuse-review-failed", "AES commit misuse review crashed",
                                   f"```\n{traceback.format_exc()[-3000:]}\n```", occurrence=f"crash:{dt.date.today()}"))
        raise SystemExit(2)
