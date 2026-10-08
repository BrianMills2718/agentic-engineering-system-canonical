#!/usr/bin/env python3
"""Daily report on the AES commit rule across every repository (plan aes-planning, P4/P6).

Runs from a user timer. Each run:

1. runs ``install_everywhere.py check`` and, when any repository is unwired or the ``aes``
   runtime is missing, opens or updates the keyed concern ``aes-commit-rule-coverage``
   (a control that went dark somewhere reaches an agent the same day);
2. rebuilds the plan index (`aes commit index`: which plans each repository holds on its default
   branch), then reads every repository's observe log for the previous days
   (``<git-common-dir>/aes/commit-rule-<date>.jsonl``), counts verdicts by tag and refusal
   reason, and appends one line per day to ``~/.local/state/aes/commit-rule-daily.jsonl``;
3. once, on the first run on or after ``REVIEW_DATE``, opens the keyed concern ``aes-commit-rule-enforce-review`` with
   the observe-period totals, so the decision on enforce mode (Brian, 2026-10-07: enforce
   only where false refusals are at or under 1 in 5) is taken from the logs, not from memory.

Exit status: 0 when every repository is wired, 1 otherwise.
"""

from __future__ import annotations

import collections
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = Path.home() / "code"
STATE = Path.home() / ".local" / "state" / "aes" / "commit-rule-daily.jsonl"
REVIEW_MARKER = STATE.with_name("commit-rule-review-opened")
# The checkout the hooks' `aes` tool is installed from and that serves as the shared plan root.
RUNTIME = Path.home() / "code" / "agentic-engineering-system-canonical" / "worktrees" / "hook-runtime"
CONCERN = Path.home() / "code" / "project-meta" / "scripts" / "concern_issue.py"
CONCERN_REPO = "BrianMills2718/agentic-engineering-system-canonical"
OBSERVE_START = dt.date(2026, 10, 7)
REVIEW_DATE = dt.date(2026, 10, 9)


def run(*cmd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def concern(key: str, title: str, body: str, occurrence: str) -> str:
    done = run(sys.executable, str(CONCERN), "open", "--repo", CONCERN_REPO, "--key", key, "--title", title,
               "--body", body, "--source", "aes-commit-rule", "--occurrence", occurrence)
    return (done.stdout or done.stderr).strip().splitlines()[-1] if (done.stdout or done.stderr) else f"exit {done.returncode}"


def log_rows(day: dt.date) -> list[tuple[str, dict]]:
    rows = []
    for repo in sorted(p for p in WORKSPACE.iterdir() if (p / ".git").exists()):
        common = run("git", "-C", str(repo), "rev-parse", "--path-format=absolute", "--git-common-dir").stdout.strip()
        if not common:
            continue
        path = Path(common) / "aes" / f"commit-rule-{day.isoformat()}.jsonl"
        if path.is_file():
            rows.extend((repo.name, json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    return rows


def classify(entry: dict) -> str:
    if entry.get("verdict") == "accept":
        return f"accept {entry.get('tag')}"
    tag = str(entry.get("tag"))
    if tag == "none":
        return "refuse: no tag"
    if tag.startswith(("Plan", "Goal")):
        return "refuse: plan not adopted"
    if tag == "Trivial":
        return "refuse: trivial with running-thing file" if entry.get("running_things") else "refuse: trivial too big"
    return f"refuse: {tag}"


QUICK_PROBLEM_MARKERS = ("saved check output", "files outside the plan's list")


def quick_plan_problems(rows: list[tuple[str, dict]]) -> list[dict]:
    """[Goal] commits whose quick-plan notes (AES #269) say the saved check output is missing or that files
    fall outside the plan's list, one record per commit with the problem notes. Clean notes are not problems."""
    found = []
    seen = set()
    for repo, entry in rows:
        if not str(entry.get("tag", "")).startswith("Goal "):
            continue
        bad = [n for n in entry.get("notes") or []
               if (n.startswith("quick plan ") and n.endswith(" missing")) or "files outside the plan's list:" in n]
        key = (repo, entry.get("subject"))
        if bad and key not in seen:
            seen.add(key)
            found.append({"repo": repo, "plan": str(entry["tag"]).split(" ", 1)[1], "subject": entry.get("subject", ""),
                          "problems": bad})
    return found


def quick_plan_concern_body(day: dt.date, problems: list[dict]) -> str:
    rows = "\n".join(f"| {p['repo']} | {p['plan']} | {p['subject'][:80]} | {'; '.join(p['problems'])} |" for p in problems)
    return (f"Commits on {day} under quick-adopt plans whose commit-rule notes report a problem (the rule logs these "
            f"and never blocks on them):\n\n| Repository | Plan | Commit subject | Notes |\n|---|---|---|---|\n{rows}\n\n"
            "For each: if the plan's saved check output is missing, commit it (`<plan folder>/<id>.check.txt`); if files "
            "fall outside the plan's list, either the work drifted beyond the plan (plan it, or move it to its own plan) "
            "or the list was incomplete (re-adopt the plan with the right files). Source: each repository's "
            "`.git/aes/commit-rule-<date>.jsonl`; plan commit-rule-notes-report, AES #279.")


def refresh_runtime() -> str:
    """Keep the hook runtime and shared plan root at AES main: fetch, move the runtime worktree
    to origin/main, and reinstall the `aes` tool when main moved (plans adopted in AES resolve
    from every repository through this checkout)."""
    runtime = RUNTIME
    if not (runtime / ".git").exists():
        # Recreate rather than report: it went missing once (2026-10-07, remover unknown) and every
        # repository's hook reads plans and the installed `aes` from it.
        main = runtime.parents[1]
        run("git", "-C", str(main), "worktree", "prune")
        made = run("git", "-C", str(main), "worktree", "add", "-q", "--detach", str(runtime), "origin/main")
        if made.returncode != 0:
            return f"runtime checkout {runtime} missing and could not be recreated: {made.stderr.strip()}"
    before = run("git", "-C", str(runtime), "rev-parse", "HEAD").stdout.strip()
    run("git", "-C", str(runtime), "fetch", "-q", "origin")
    moved = run("git", "-C", str(runtime), "checkout", "-q", "--detach", "origin/main")
    after = run("git", "-C", str(runtime), "rev-parse", "HEAD").stdout.strip()
    if moved.returncode != 0:
        return f"runtime refresh failed: {moved.stderr.strip()}"
    if before != after:
        uv = Path.home() / ".local" / "bin" / "uv"
        done = run(str(uv), "tool", "install", "--force", "--from", str(runtime), "agentic-engineering-system")
        return f"runtime moved {before[:8]} -> {after[:8]}; aes reinstalled (exit {done.returncode})"
    return f"runtime at {after[:8]} (unchanged)"


def main() -> int:
    today = dt.date.today()
    print(refresh_runtime())
    # [Goal <id>] lookups read each repository's default branch from this index when its checkout is
    # elsewhere (AES #215); the hook also refreshes it in the background when it is over an hour old.
    aes = Path.home() / ".local" / "bin" / "aes"
    idx = run(str(aes), "commit", "index", "--fetch", "--workspace", str(WORKSPACE))
    print((idx.stdout or idx.stderr).strip().splitlines()[-1] if (idx.stdout or idx.stderr).strip() else f"plan index: exit {idx.returncode}")
    check = run(sys.executable, str(HERE / "install_everywhere.py"), "check")
    summary = check.stdout.strip().splitlines()[-1] if check.stdout.strip() else check.stderr.strip()
    print(summary)
    if check.returncode != 0:
        print(concern("aes-commit-rule-coverage", "AES commit rule is not running in every repository",
                      f"`install_everywhere.py check` on {today}:\n\n```\n{check.stdout.strip()}\n```\n\n"
                      "Fix: rerun `install_everywhere.py install` (AES canonical proposals/aes-planning/rollout/) "
                      "or wire the listed repository by hand; see proposals/aes-planning/ROLLOUT.md.",
                      occurrence=f"{today}:{summary}"))
    STATE.parent.mkdir(parents=True, exist_ok=True)
    seen = {json.loads(l)["day"] for l in STATE.read_text(encoding="utf-8").splitlines()} if STATE.exists() else set()
    day = OBSERVE_START
    while day < today:
        if day.isoformat() not in seen:
            rows = log_rows(day)
            counts = collections.Counter(classify(e) for _, e in rows)
            repos = collections.Counter(r for r, e in rows if e.get("verdict") == "refuse")
            problems = quick_plan_problems(rows)
            print(f"quick-plan notes {day}: {len(problems)} commit(s) with a missing check output or files outside the plan")
            with STATE.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"day": day.isoformat(), "commits": len(rows), "counts": dict(counts),
                                     "top_refusing_repos": repos.most_common(10), "quick_plan_problems": len(problems),
                                     "quick_plan_commits": [f"{p['repo']}: {p['subject'][:80]}" for p in problems]}) + "\n")
            if problems:
                print(concern("aes-quick-plan-drift", "Quick-plan commits with a missing check output or files outside the plan",
                              quick_plan_concern_body(day, problems), occurrence=f"quick-plan:{day}:{len(problems)}"))
        day += dt.timedelta(days=1)
    if today >= REVIEW_DATE and not REVIEW_MARKER.exists():
        days = [json.loads(l) for l in STATE.read_text(encoding="utf-8").splitlines()] if STATE.exists() else []
        total = collections.Counter()
        for d in days:
            total.update(d["counts"])
        commits = sum(d["commits"] for d in days)
        table = "\n".join(f"| {k} | {v} |" for k, v in total.most_common())
        print(concern("aes-commit-rule-enforce-review", "Decide AES commit rule enforce mode from the observe logs",
                      f"Observe period {OBSERVE_START} to {today - dt.timedelta(days=1)}: {commits} commits checked.\n\n"
                      f"| Verdict | Commits |\n|---|---:|\n{table}\n\nBrian's condition (2026-10-07): enforce a repository only "
                      "where false refusals (refused commits a reader judges genuinely fine) are at or under 1 in 5; any "
                      "other repository stays in observe and is reported to him. Per-day lines: "
                      f"`{STATE}`. Read a sample of the refused commits per repository before switching; switch with "
                      "`repos: {<dir>: {mode: enforce}}` in ~/.config/aes/commit_rule.yaml. Context: "
                      "proposals/aes-planning/ROLLOUT.md (the replay of past commits refused 99%, mostly untagged).",
                      occurrence=f"review:{today}"))
        REVIEW_MARKER.write_text(f"{today}\n", encoding="utf-8")  # once: closing the issue must not be undone by the timer
    return 0 if check.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
