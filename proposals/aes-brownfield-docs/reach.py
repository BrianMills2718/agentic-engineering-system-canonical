#!/usr/bin/env python3
"""reach.py REPO_PATH [REF] [--list] : can a reader reach every reader document from wiki/index.md in two links?

Reads files from the git ref (default origin/HEAD; use HEAD for a working branch), follows relative
Markdown links (anchors stripped, %20 decoded) breadth-first from wiki/index.md, and classifies every
file that is unreachable or more than two links deep. Those are allowed only when they are one of:

  instruction  CLAUDE.md, AGENTS.md or SKILL.md, or anything under .claude/  (loaded by path)
  hidden       inside a hidden tool folder (.project-brain/, .wiki/, ...)
  fixture      under tests/fixtures/                                          (opened by tests)
  template     named TEMPLATE.md                                              (read by a tool)
  generated    under generated/, or a .md path assigned to an *OUTPUT* constant in a Python file
  unlinked_ok  under a folder or file listed in .md-file-cap.yaml unlinked_ok, each with a reason

Anything else is a finding: ORPHAN (not reachable) or DEEP (reachable only in more than two links).
This is the workspace documentation rule (AGENTS.md, Policy md-file-cap) that project-meta
scripts/md_file_cap.py checks daily for Brian's own repositories.
Prints counts per class and hop depth, lists findings, and exits 1 when any exists.
Read-only; classification uses file paths and code assignments, never document prose.
"""
import os, re, subprocess, sys
from collections import deque
from urllib.parse import unquote

MAX_HOPS = 2
args = [a for a in sys.argv[1:] if not a.startswith("--")]
repo, ref = args[0], (args[1] if len(args) > 1 else "origin/HEAD")
show_all = "--list" in sys.argv


def git(*a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout


class Blobs:
    """Read many files at one ref through a single `git cat-file --batch` process."""

    def __init__(self):
        self.p = subprocess.Popen(["git", "-C", repo, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read(self, path):
        self.p.stdin.write(f"{ref}:{path}\n".encode()); self.p.stdin.flush()
        header = self.p.stdout.readline().split()
        if len(header) < 3 or header[1] != b"blob":
            return ""
        data = self.p.stdout.read(int(header[2])); self.p.stdout.read(1)
        return data.decode("utf-8", "replace")

    def close(self):
        self.p.stdin.close(); self.p.wait()


tracked = git("ls-tree", "-r", "-z", "--name-only", ref).split("\0")
md = {p for p in tracked if p.lower().endswith(".md")}
start = "wiki/index.md"
if start not in md:
    print(f"{repo}: no {start}; {len(md)} tracked .md, every one unreachable")
    sys.exit(1)

blobs = Blobs()
allowed, problems = [], []
try:
    import yaml
    cap = yaml.safe_load(blobs.read(".md-file-cap.yaml") or "{}") or {}
except ImportError:
    cap = {}
for e in cap.get("unlinked_ok") or []:
    path, reason = str((e or {}).get("path") or "").strip(), str((e or {}).get("reason") or "").strip()
    if not path or not reason:
        problems.append(f"unlinked_ok entry without a path and a reason: {e!r}")
    else:
        allowed.append(path)

LINK = re.compile(r"\]\(([^)\s]+)\)")
dist, q = {start: 0}, deque([start])
while q:
    cur = q.popleft()
    for target in LINK.findall(blobs.read(cur)):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        path = os.path.normpath(os.path.join(os.path.dirname(cur), unquote(target.split("#")[0])))
        if path in md and path not in dist:
            dist[path] = dist[cur] + 1
            q.append(path)

OUTPUT_ASSIGN = re.compile(r"^\s*\w*OUTPUT\w*\s*=\s*Path\(\s*[\"']([^\"']+\.md)[\"']", re.M | re.I)
generated = set()
for py in (p for p in tracked if p.endswith(".py")):
    generated.update(OUTPUT_ASSIGN.findall(blobs.read(py)))
blobs.close()


def under(path, prefix):
    return path == prefix or path.startswith(prefix.rstrip("/") + "/")


def classify(path):
    base = os.path.basename(path)
    if base in ("CLAUDE.md", "AGENTS.md", "SKILL.md") or path.startswith(".claude/"):
        return "instruction"
    if any(part.startswith(".") for part in path.split("/")[:-1]):
        return "hidden"
    if path.startswith("tests/fixtures/"):
        return "fixture"
    if base == "TEMPLATE.md":
        return "template"
    if path.startswith("generated/") or path in generated:
        return "generated"
    if any(under(path, a) for a in allowed):
        return "unlinked_ok"
    return None


classes = {}
for p in sorted(md - set(dist)):
    classes.setdefault(classify(p) or "ORPHAN", []).append(p)
for p in sorted(p for p, d in dist.items() if d > MAX_HOPS):
    classes.setdefault(classify(p) or "DEEP", []).append(p)
within = lambda n: sum(1 for d in dist.values() if d <= n)
name = os.path.basename(os.path.abspath(repo))
print(f"{name} @ {ref}: {len(md)} tracked .md; reachable from {start}: 1 hop {within(1)}, 2 hops {within(2)}, any {len(dist)}")
print("outside two links, by class: " + ", ".join(f"{k} {len(v)}" for k, v in sorted(classes.items())) if classes else "outside two links: none")
for msg in problems:
    print(f"  INVALID     {msg}")
for k, v in sorted(classes.items()):
    if k in ("ORPHAN", "DEEP") or show_all:
        for p in v:
            hops = f"{dist[p]} hops" if p in dist else ""
            print(f"  {k:<11} {p} {hops}".rstrip())
findings = len(classes.get("ORPHAN", [])) + len(classes.get("DEEP", [])) + len(problems)
print(f"findings: {findings}   exit {1 if findings else 0}")
sys.exit(1 if findings else 0)
