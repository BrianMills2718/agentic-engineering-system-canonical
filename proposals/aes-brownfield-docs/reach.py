#!/usr/bin/env python3
"""reach.py REPO_PATH [REF] [--list] : which tracked Markdown files a reader reaches from wiki/index.md.

Reads files from the git ref (default origin/HEAD; use HEAD for a working branch), follows relative
Markdown links (anchors stripped) breadth-first from wiki/index.md, and classifies every file it
cannot reach. Unreachable files are allowed only when they are one of:

  instruction  CLAUDE.md, AGENTS.md or SKILL.md, or anything under .claude/  (loaded by path)
  fixture      under tests/fixtures/                                          (opened by tests)
  template     named TEMPLATE.md                                              (read by a tool)
  generated    assigned to an *OUTPUT* path constant in a Python file under scripts/ (rebuilt by it)

Anything else unreachable is an ORPHAN: a reader document the wiki does not route to.
Prints counts per class and hop depth, lists orphans, and exits 1 when any orphan exists.
Read-only; classification uses file paths and code assignments, never document prose.
"""
import os, re, subprocess, sys
from collections import deque

args = [a for a in sys.argv[1:] if not a.startswith("--")]
repo, ref = args[0], (args[1] if len(args) > 1 else "origin/HEAD")
show_all = "--list" in sys.argv


def git(*a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout


tracked = git("ls-tree", "-r", "--name-only", ref).splitlines()
md = {p for p in tracked if p.lower().endswith(".md")}
start = "wiki/index.md"
if start not in md:
    print(f"{repo}: no {start}; {len(md)} tracked .md, every one unreachable")
    sys.exit(1)

LINK = re.compile(r"\]\(([^)\s]+)\)")
dist, q = {start: 0}, deque([start])
while q:
    cur = q.popleft()
    for target in LINK.findall(git("show", f"{ref}:{cur}")):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        path = os.path.normpath(os.path.join(os.path.dirname(cur), target.split("#")[0]))
        if path in md and path not in dist:
            dist[path] = dist[cur] + 1
            q.append(path)

OUTPUT_ASSIGN = re.compile(r"^\s*\w*OUTPUT\w*\s*=\s*Path\(\s*[\"']([^\"']+\.md)[\"']", re.M | re.I)
generated = set()
for py in (p for p in tracked if p.startswith("scripts/") and p.endswith(".py")):
    generated.update(OUTPUT_ASSIGN.findall(git("show", f"{ref}:{py}")))


def classify(path):
    base = os.path.basename(path)
    if base in ("CLAUDE.md", "AGENTS.md", "SKILL.md") or path.startswith(".claude/"):
        return "instruction"
    if path.startswith("tests/fixtures/"):
        return "fixture"
    if base == "TEMPLATE.md":
        return "template"
    if path in generated:
        return "generated"
    return "ORPHAN"


unreached = sorted(md - set(dist))
classes = {}
for p in unreached:
    classes.setdefault(classify(p), []).append(p)
within = lambda n: sum(1 for d in dist.values() if d <= n)
name = os.path.basename(os.path.abspath(repo))
print(f"{name} @ {ref}: {len(md)} tracked .md; reachable from {start}: 1 hop {within(1)}, 2 hops {within(2)}, any {len(dist)}")
print("unreachable by class: " + ", ".join(f"{k} {len(v)}" for k, v in sorted(classes.items())) if classes else "unreachable: none")
beyond = sorted(p for p, d in dist.items() if d > 2)
if beyond:
    print(f"reachable but more than two hops: {len(beyond)}")
    for p in beyond:
        print(f"  {dist[p]} hops  {p}")
for k, v in sorted(classes.items()):
    if k == "ORPHAN" or show_all:
        for p in v:
            print(f"  {k:<11} {p}")
orphans = len(classes.get("ORPHAN", []))
print(f"orphans: {orphans}   exit {1 if orphans else 0}")
sys.exit(1 if orphans else 0)
