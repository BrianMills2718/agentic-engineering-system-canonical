#!/usr/bin/env python3
"""Is a project's brain older than the work done since? (hive brain v1, C-CONTEXT)

A project brain is the `.project-brain/` folder in the repo (layout: agent-skills
`contracts/client-config/agents/project-brain.md`). Agents read `now.md` first, so
a brain that stopped being updated while work went on sends them off with stale
context. This compares the brain's last commit with the commits since that
touched anything else, and says whether the local checkout is behind GitHub
(Paperclip keeps a task's checkout between runs).

  python3 scripts/hive/brain_fresh.py ~/code/agentic-engineering-system-canonical
  python3 scripts/hive/brain_fresh.py ~/code/theory-forge --brain HANDOFF.md
  python3 scripts/hive/brain_fresh.py <repo> --fetch     # also check against origin

Stale when more than --max-commits other commits landed since the brain's last
update, or when the brain is older than --max-days and anything landed since.
Exit status: 0 = fresh, 1 = stale or behind origin, 2 = no brain or not a repo.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", type=Path)
    ap.add_argument("--brain", default=".project-brain", help="brain path inside the repo (default .project-brain)")
    ap.add_argument("--max-commits", type=int, default=15)
    ap.add_argument("--max-days", type=int, default=14)
    ap.add_argument("--fetch", action="store_true", help="git fetch first and report commits the checkout is behind")
    a = ap.parse_args()
    repo = a.repo.expanduser().resolve()
    try:
        git(repo, "rev-parse", "--git-dir")
        if a.fetch:
            git(repo, "fetch", "--quiet")
        last = git(repo, "log", "-1", "--format=%H %ct", "--", a.brain)
    except RuntimeError as e:
        print(f"brain_fresh: {repo}: {e}", file=sys.stderr)
        return 2
    if not last:
        print(f"{repo.name}: no brain at {a.brain} (never committed)")
        return 2
    sha, when = last.split()
    since = git(repo, "rev-list", "--count", f"{sha}..HEAD", "--", ".", f":(exclude){a.brain}")
    since = int(since or 0)
    days = (time.time() - int(when)) / 86400
    behind = 0
    if a.fetch:
        try:
            behind = int(git(repo, "rev-list", "--count", "HEAD..@{upstream}") or 0)
        except RuntimeError:
            behind = 0
    stale = since > a.max_commits or (days > a.max_days and since > 0)
    verdict = "STALE" if stale else "fresh"
    print(f"{repo.name}: {verdict}: {a.brain} last updated {days:.0f} days ago at {sha[:8]}; "
          f"{since} other commits since (limits: {a.max_commits} commits, {a.max_days} days)"
          + (f"; checkout {behind} commits behind origin" if a.fetch else ""))
    return 1 if stale or behind else 0


if __name__ == "__main__":
    sys.exit(main())
