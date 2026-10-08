"""Replay for plan doc-reach-new-docs: for every commit since 2026-10-07 that added .md files in a
Brian-owned repository under ~/code, compare the commit rule's new-document answer (run on that
commit's tree loaded into a temporary index) with the daily check's (project-meta md_file_cap
reachability at that commit). Prints one row per added file and the totals.

Run: PYTHONPATH=src .venv/bin/python proposals/doc-reach-new-docs/replay_compare.py"""
import glob
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from agentic_engineering_system import commit_rule as cr

sys.path.insert(0, str(Path.home() / "code" / "project-meta" / "scripts"))
import md_file_cap as m  # noqa: E402

rows, agree, disagree = [], 0, 0
for g in sorted(glob.glob(str(Path.home() / "code" / "*" / ".git"))):
    top = g[:-5]
    slug = (m.remote_slug(top) or "").lower()
    if not slug.startswith(("brianmills2718/", "brianmills-spec/")):
        continue
    log = m.git(top, "log", "--since=2026-10-07", "--no-merges", "--diff-filter=A", "--name-only",
                "--format=@@%h", "origin/HEAD") or ""
    commit = None
    added: dict[str, list[str]] = {}
    for line in log.splitlines():
        if line.startswith("@@"):
            commit = line[2:]
            added[commit] = []
        elif commit and line.strip().lower().endswith(".md"):
            added[commit].append(line.strip())
    for commit, files in added.items():
        if not files:
            continue
        r = m.reachability(top, commit)
        daily_bad = set(r["orphans"]) | set(r["beyond"])
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["GIT_INDEX_FILE"] = str(Path(tmp) / "index")
            subprocess.run(["git", "-C", top, "read-tree", commit], check=True)
            try:
                rule_bad = set(cr.unreached_new_docs(Path(top), files))
            finally:
                del os.environ["GIT_INDEX_FILE"]
        for f in files:
            same = (f in daily_bad) == (f in rule_bad)
            agree += same
            disagree += not same
            rows.append(f"{'same' if same else 'DIFF'}\t{Path(top).name}\t{commit}\t{f}\tdaily={'unreached' if f in daily_bad else 'ok'}\trule={'unreached' if f in rule_bad else 'ok'}")
print("\n".join(rows))
print(f"files compared: {agree + disagree}; same answer: {agree}; different: {disagree}")
sys.exit(1 if disagree else 0)
