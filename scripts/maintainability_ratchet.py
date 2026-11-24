"""Fail only on maintainability findings this branch adds; findings already on the base never block.

Compares the tree where the branch started (the merge base with --base) with the working tree, over the
Python files under the given folders:

- ruff (pinned): blind `except` (BLE), `try/except/pass` and `try/except/continue` (S110, S112), and
  function complexity (C901). A complexity finding is new when a function over the limit has no base
  function of that name at least as complex, so an unrelated edit inside an already complex function
  passes and a body edit that adds a branch fails.
- pylint (pinned) duplicate-code: blocks of 6 or more similar lines; new when there are more blocks.
- file growth: a file over --max-lines that grew on this branch (a renamed file keeps its base size).

Findings are counted without paths or line numbers, so code moved within or between files, or a file
renamed, is not new; the price is that removing one finding and adding a like one elsewhere passes.
Not covered: an existing helper rewritten under a new name (that needs reading for meaning). Exit 0 when
nothing is new or the base is missing, 1 on a new finding, 2 when a tool fails. Base results are cached
under the git folder by base commit and a hash of this script. Pilot for AES (Brian, 2026-11-24, slice 3
of the Reddit-ideas plan: "i will trust your jdugement on the impelemtnation prirotiy").
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lockstep.checks.changed import compare_with, extract  # noqa: E402 -- the path is set just above

RUFF = ["uvx", "ruff@0.14.0", "check", "--isolated", "--select", "BLE,S110,S112,C901", "--output-format", "json", "--exit-zero"]
PYLINT = ["uvx", "--from", "pylint==3.3.9", "pylint", "--disable=all", "--enable=duplicate-code",
          "--min-similarity-lines=6", "--output-format=json", "--score=n", "--persistent=n"]
PYLINT_REFACTOR = 8  # the exit bit for refactor messages, which duplicate-code is; any other bit means failure
COMPLEX = re.compile(r"^`(?P<name>[^`]+)` is too complex \((?P<n>\d+) > \d+\)$")
DUP_MODULE = re.compile(r"^==(?P<module>[^:]+):\[")


class ToolFailed(RuntimeError):
    pass


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout


def _python_files(root: Path, folders: list[str]) -> list[str]:
    listed = _git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", *folders).split("\0")
    return sorted(p for p in set(listed) if p.endswith(".py") and (root / p).is_file())


def _renames(root: Path, base: str) -> dict[str, str]:
    """Base path -> working-tree path for files renamed on the branch (staged or committed)."""
    parts, renamed, i = _git(root, "diff", "-M", "--name-status", "-z", base).split("\0"), {}, 0
    while i < len(parts) and parts[i]:
        if parts[i].startswith(("R", "C")):
            renamed[parts[i + 1]] = parts[i + 2]
            i += 3
        else:
            i += 2
    return renamed


def _json_output(name: str, done: subprocess.CompletedProcess) -> list:
    try:
        found = json.loads(done.stdout)
    except json.JSONDecodeError as exc:
        raise ToolFailed(f"{name} exit {done.returncode}: {(done.stderr or done.stdout).strip()[-300:]}") from exc
    if not isinstance(found, list):
        raise ToolFailed(f"{name} printed JSON that is not a list")
    return found


def _ruff(cwd: Path, files: list[str]) -> list[dict]:
    if not files:
        return []
    done = subprocess.run([*RUFF, *files], cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:  # --exit-zero: findings exit 0, so anything else is a failed run
        raise ToolFailed(f"ruff exit {done.returncode}: {done.stderr.strip()[-300:]}")
    found = _json_output("ruff", done)
    for item in found:
        item["filename"] = Path(item["filename"]).resolve().relative_to(cwd.resolve()).as_posix()
    return found


def _duplicates(cwd: Path, files: list[str]) -> list[str]:
    """One line per duplicate block, naming the modules it joins."""
    if len(files) < 2:
        return []
    with tempfile.NamedTemporaryFile("w", suffix=".rc") as rc:
        done = subprocess.run([*PYLINT, f"--rcfile={rc.name}", *files], cwd=cwd, capture_output=True, text=True)
    if done.returncode & ~PYLINT_REFACTOR:
        raise ToolFailed(f"pylint exit {done.returncode}: {(done.stderr or done.stdout).strip()[-300:]}")
    blocks = []
    for item in _json_output("pylint", done):
        if item.get("symbol") == "duplicate-code":
            modules = sorted({m.group("module") for line in item["message"].splitlines() if (m := DUP_MODULE.match(line))})
            blocks.append(", ".join(modules))
    return sorted(blocks)


def _findings(cwd: Path, files: list[str]) -> dict:
    """Plain ruff findings with their paths, complexity per function name, duplicate blocks, line counts."""
    plain: dict = defaultdict(list)
    complexity: dict = defaultdict(list)
    for item in _ruff(cwd, files):
        hit = COMPLEX.match(item["message"]) if item["code"] == "C901" else None
        if hit:
            complexity[hit.group("name")].append([int(hit.group("n")), item["filename"]])
        else:
            plain[f"{item['code']} {item['message']}"].append(item["filename"])
    lines = {f: len((cwd / f).read_text(errors="replace").splitlines()) for f in files}
    return {"plain": dict(plain), "cx": dict(complexity), "dup": _duplicates(cwd, files), "lines": lines}


def _base_findings(root: Path, base: str, folders: list[str]) -> dict:
    """Findings for the base tree, cached under the git folder by commit, folders and this script's hash."""
    sha = _git(root, "rev-parse", base).strip()
    common = Path(_git(root, "rev-parse", "--git-common-dir").strip())
    common = common if common.is_absolute() else root / common
    script = hashlib.sha256(Path(__file__).read_bytes() + ",".join(folders).encode()).hexdigest()[:16]
    cached = common / "maintainability-ratchet" / f"{sha}-{script}.json"
    try:
        return json.loads(cached.read_text())
    except (OSError, json.JSONDecodeError):
        pass  # no cache yet, or a damaged one: compute again and overwrite it
    with tempfile.TemporaryDirectory() as tmp:
        base_root = Path(tmp)
        extract(root, sha, base_root, folders)
        files = sorted(p.relative_to(base_root).as_posix() for p in base_root.rglob("*.py"))
        found = _findings(base_root, files)
    cached.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=cached.parent, delete=False, suffix=".tmp") as out:
        json.dump(found, out)
    os.replace(out.name, cached)
    return found


def _plain(head: dict, base: dict) -> list[str]:
    new = []
    for key, paths in sorted(head.items()):
        before = base.get(key, [])
        if len(paths) > len(before):
            grew = sorted(p for p, n in Counter(paths).items() if n > Counter(before)[p]) or sorted(set(paths))
            new.append(f"new {key} in {', '.join(grew)} (base {len(before)}, now {len(paths)})")
    return new


def _complexity(head: dict, base: dict) -> list[str]:
    """Functions of one name are compared most complex first; one more complex than its base pair is new."""
    new = []
    for name, entries in sorted(head.items()):
        before = sorted((n for n, _ in base.get(name, [])), reverse=True)
        for i, (value, path) in enumerate(sorted(entries, key=lambda e: e[0], reverse=True)):
            if i >= len(before) or value > before[i]:
                was = before[i] if i < len(before) else "at or under the limit"
                new.append(f"new C901 {path}: `{name}` complexity {value} (base {was})")
    return new


def _duplicates_added(head: list[str], base: list[str]) -> list[str]:
    if len(head) <= len(base):
        return []
    extra = list((Counter(head) - Counter(base)).elements())
    return [f"new duplicate blocks: {len(base)} on the base, {len(head)} now; not on the base: "
            + ("; ".join(extra) if extra else "same files as existing blocks")]


def _growth(head: dict, base: dict, renamed: dict, max_lines: int) -> list[str]:
    before = {renamed.get(p, p): n for p, n in base.items()}
    return [f"new file-growth {path}: {n} lines, over {max_lines} (base {before.get(path, 'absent')})"
            for path, n in sorted(head.items()) if n > max_lines and n > before.get(path, 0)]


def compare(root: Path, base: str, folders: list[str], max_lines: int) -> tuple[list[str], int, int]:
    """Return the new findings as printable lines, and the base and head finding totals."""
    b = _base_findings(root, base, folders)
    h = _findings(root, _python_files(root, folders))
    new = _plain(h["plain"], b["plain"]) + _complexity(h["cx"], b["cx"]) + _duplicates_added(h["dup"], b["dup"])
    new += _growth(h["lines"], b["lines"], _renames(root, base), max_lines)
    return new, _total(b), _total(h)


def _total(found: dict) -> int:
    return sum(map(len, found["plain"].values())) + sum(map(len, found["cx"].values())) + len(found["dup"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=".")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--folders", default="src,scripts", help="comma-separated folders to read")
    parser.add_argument("--max-lines", type=int, default=800)
    args = parser.parse_args(argv)
    root = Path(args.repo).resolve()
    folders = [f for f in args.folders.split(",") if f]
    base = compare_with(root, args.base)
    if base is None:
        print(f"RESULT maintainability skipped=base-missing base={args.base} exit=0")
        return 0
    changed = [p for p in _git(root, "diff", "--name-only", "-z", base, "--", *folders).split("\0") if p.endswith(".py")]
    untracked = [p for p in _git(root, "ls-files", "-z", "--others", "--exclude-standard", "--", *folders).split("\0") if p.endswith(".py")]
    if not changed and not untracked:
        print("RESULT maintainability skipped=no-python-change exit=0")
        return 0
    try:
        new, base_total, head_total = compare(root, base, folders, args.max_lines)
    except (ToolFailed, subprocess.CalledProcessError, OSError) as exc:
        print(f"maintainability: a tool failed: {exc}")
        print("RESULT maintainability tool-failed exit=2")
        return 2
    for line in new:
        print(line)
    code = 1 if new else 0
    print(f"RESULT maintainability new={len(new)} base_findings={base_total} head_findings={head_total} exit={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
