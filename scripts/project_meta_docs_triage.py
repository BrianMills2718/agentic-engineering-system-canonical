#!/usr/bin/env python3
"""Read-only triage of a repository's docs folders (Project Meta retirement plan, slice 0b).

For each immediate subfolder of docs/ it records: file count and size, file types, whether a
script in the repository names the folder (a generator or reader), how many files changed since a
cutoff date (from git history), the last commit date, and how many other repositories mention the
folder. It then proposes a disposition by fixed rules. It reads files and git history only; it
changes nothing and makes no model call.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return done.stdout.strip()


def files_in(folder: Path) -> list[Path]:
    return [p for p in folder.rglob("*") if p.is_file()]


def count_mentions(root: Path, needles: dict[str, str], suffixes: tuple[str, ...]) -> dict[str, int]:
    """For each key, the number of files under root (not .git or worktrees) containing its needle.

    Each file is read once and tested against every needle.
    """
    counts = {key: 0 for key in needles}
    skip = {".git", "worktrees", "node_modules", ".venv", "__pycache__"}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in suffixes or skip & set(path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for key, needle in needles.items():
            if needle in text:
                counts[key] += 1
    return counts


def disposition(row: dict) -> tuple[str, str]:
    """Fixed rules, in order. A proposal, never an action.

    generated_hint only says a build/render/generate script mentions the folder's path, so some of
    its files may be script-written; it never makes a whole folder regenerable. That is judged by hand.
    """
    if row["outside_mentions"] > 0:
        return "read", f"{row['outside_mentions']} file(s) in other repositories mention it"
    if row["changed_since"] > 0:
        return "read", f"{row['changed_since']} file(s) changed since the cutoff"
    return "archive", "unchanged since the cutoff and not mentioned elsewhere"


def triage(repo: Path, cutoff: str, others: list[Path]) -> list[dict]:
    docs = repo / "docs"
    scripts = repo / "scripts"
    folders = sorted(p for p in docs.iterdir() if p.is_dir())
    # A script "names" a folder only by a path reference (docs/<name>), not by an ordinary word.
    named = count_mentions(scripts, {f.name: f"docs/{f.name}" for f in folders}, (".py", ".sh", ".yaml", ".yml")) if scripts.is_dir() else {}
    builders = [p for p in scripts.glob("*.py") if any(k in p.name for k in ("render_", "generate", "build_"))] if scripts.is_dir() else []
    builder_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in builders)
    outside = {f.name: 0 for f in folders}
    suffixes = (".md", ".py", ".yaml", ".yml", ".json", ".sh")
    for other in others:
        if other.is_dir():
            for name, n in count_mentions(other, {f.name: f"{repo.name}/docs/{f.name}" for f in folders}, suffixes).items():
                outside[name] += n
    rows = []
    for folder in folders:
        files = files_in(folder)
        types = collections.Counter(p.suffix.lstrip(".") or "none" for p in files)
        needle = f"docs/{folder.name}"
        changed = {l for l in git(repo, "log", f"--since={cutoff}", "--name-only", "--format=", "--", needle).splitlines() if l}
        row = {
            "folder": folder.name, "files": len(files), "mib": round(sum(p.stat().st_size for p in files) / 2**20, 1),
            "types": dict(types.most_common(3)), "named_by_scripts": named.get(folder.name, 0),
            "generated_hint": bool(re.search(r"docs/%s\b|/\s*[\"']%s[\"']" % (re.escape(folder.name), re.escape(folder.name)), builder_text)), "changed_since": len(changed),
            "last_commit": git(repo, "log", "-1", "--format=%cs", "--", needle) or "none",
            "outside_mentions": outside[folder.name],
        }
        row["proposed"], row["because"] = disposition(row)
        rows.append(row)
    return sorted(rows, key=lambda r: -r["files"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--cutoff", default="2026-10-14")
    ap.add_argument("--others", type=Path, nargs="*", default=[])
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if not (a.repo / "docs").is_dir():
        print(f"no docs/ folder in {a.repo}", file=sys.stderr)
        return 2
    rows = triage(a.repo, a.cutoff, a.others)
    result = {"repo": a.repo.name, "revision": git(a.repo, "rev-parse", "HEAD"), "cutoff": a.cutoff, "rows": rows}
    text = json.dumps(result, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        a.out.write_text(text)
    print(f"{len(rows)} folders, {sum(r['files'] for r in rows)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
