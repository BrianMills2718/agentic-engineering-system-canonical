#!/usr/bin/env python3
"""reach.py REPO_PATH [REF] : how many tracked .md files a reader reaches from wiki/index.md by following links.

Reads files from the git ref (default origin/HEAD), follows relative Markdown links (anchors stripped),
and prints reachable-within-1, within-2, within-any hops, and the total. Read-only.
"""
import os, re, subprocess, sys
from collections import deque

repo, ref = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "origin/HEAD")
git = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout
md = {p for p in git("ls-tree", "-r", "--name-only", ref).splitlines() if p.lower().endswith(".md")}
LINK = re.compile(r"\]\(([^)\s]+)\)")
start = "wiki/index.md"
if start not in md:
    print(f"{repo}: no {start}; total md {len(md)}"); sys.exit(0)
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
within = lambda n: sum(1 for d in dist.values() if d <= n)
print(f"{os.path.basename(repo.rstrip('/'))}: total {len(md)}; reachable from wiki/index.md in 1 hop {within(1)}, 2 hops {within(2)}, any {len(dist)}; unreachable {len(md) - len(dist)}")
