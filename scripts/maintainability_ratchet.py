"""Fail only on maintainability findings this branch adds; findings already on the base never block.

Compares the tree where the branch started (the merge base with --base) with the working tree, over the
Python files under the given folders:

- ruff (pinned): blind `except` (BLE), `try/except/pass` and `try/except/continue` (S110, S112), and
  function complexity (C901). A complexity finding is new when a function is over the limit and is more
  complex than on the base, so an unrelated edit inside an already complex function passes and a body
  edit that adds a branch fails.
- pylint (pinned) duplicate-code: a block of 6 or more similar lines, keyed by the files it joins.
- file growth: a file over --max-lines that grew on this branch.

Findings are keyed without line numbers and counted, so moved code is not new; a file renamed on the
branch keeps its base findings. Not covered: an existing helper rewritten under a new name (that needs
reading for meaning). Exit 0 when nothing is new or the base is missing, 1 on a new finding, 2 when a
tool fails. Pilot for AES (Brian, 2026-11-24, slice 3 of the Reddit-ideas plan: "i will trust your
jdugement on the impelemtnation prirotiy").
"""
from __future__ import annotations

import argparse
import json
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
    out = _git(root, "diff", "-M", "--name-status", "-z", base)
    parts, renamed, i = out.split("\0"), {}, 0
    while i < len(parts) and parts[i]:
        status = parts[i]
        if status.startswith(("R", "C")):
            renamed[parts[i + 1]] = parts[i + 2]
            i += 3
        else:
            i += 2
    return renamed


def _ruff(cwd: Path, files: list[str]) -> list[dict]:
    if not files:
        return []
    done = subprocess.run([*RUFF, *files], cwd=cwd, capture_output=True, text=True)
    try:
        found = json.loads(done.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise ToolFailed(f"ruff exit {done.returncode}: {done.stderr.strip()[-300:]}") from exc
    for item in found:
        item["filename"] = Path(item["filename"]).resolve().relative_to(cwd.resolve()).as_posix()
    return found


def _duplicates(cwd: Path, files: list[str]) -> Counter:
    if len(files) < 2:
        return Counter()
    with tempfile.NamedTemporaryFile("w", suffix=".rc") as rc:
        done = subprocess.run([*PYLINT, f"--rcfile={rc.name}", *files], cwd=cwd, capture_output=True, text=True)
    if done.returncode & (1 | 32):  # fatal message or usage error: the run did not happen
        raise ToolFailed(f"pylint exit {done.returncode}: {(done.stderr or done.stdout).strip()[-300:]}")
    try:
        found = json.loads(done.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise ToolFailed(f"pylint printed no JSON (exit {done.returncode})") from exc
    keys: Counter = Counter()
    for item in found:
        if item.get("symbol") != "duplicate-code":
            continue
        modules = sorted({m.group("module") for line in item["message"].splitlines() if (m := DUP_MODULE.match(line))})
        keys[tuple(modules)] += 1
    return keys


def _findings(cwd: Path, files: list[str]) -> tuple[Counter, dict, Counter, dict]:
    """Plain ruff findings, complexity per function, duplicate blocks and line counts for one tree."""
    plain: Counter = Counter()
    complexity: dict = defaultdict(list)
    for item in _ruff(cwd, files):
        hit = COMPLEX.match(item["message"]) if item["code"] == "C901" else None
        if hit:
            complexity[(item["filename"], hit.group("name"))].append(int(hit.group("n")))
        else:
            plain[(item["filename"], item["code"], item["message"])] += 1
    lines = {f: len((cwd / f).read_text(errors="replace").splitlines()) for f in files}
    return plain, complexity, _duplicates(cwd, files), lines


def _base_findings(root: Path, base: str, folders: list[str]) -> tuple[Counter, dict, Counter, dict]:
    """Findings for the base tree, cached under the git folder by commit, folders and tool versions."""
    sha = _git(root, "rev-parse", base).strip()
    common = Path(_git(root, "rev-parse", "--git-common-dir").strip())
    common = common if common.is_absolute() else root / common
    tag = re.sub(r"[^A-Za-z0-9_.-]", "_", f"{sha}-{'+'.join(folders)}-{RUFF[1]}-{PYLINT[2]}")
    cached = common / "maintainability-ratchet" / f"{tag}.json"
    if cached.is_file():
        data = json.loads(cached.read_text())
        return (Counter({tuple(k): n for k, n in data["plain"]}), {tuple(k): v for k, v in data["cx"]},
                Counter({tuple(k): n for k, n in data["dup"]}), data["lines"])
    with tempfile.TemporaryDirectory() as tmp:
        base_root = Path(tmp)
        extract(root, sha, base_root, folders)
        files = sorted(p.relative_to(base_root).as_posix() for p in base_root.rglob("*.py"))
        plain, cx, dup, lines = _findings(base_root, files)
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_text(json.dumps({"plain": [[list(k), n] for k, n in plain.items()], "cx": [[list(k), v] for k, v in cx.items()],
                                  "dup": [[list(k), n] for k, n in dup.items()], "lines": lines}))
    return plain, cx, dup, lines


def _stem(path: str) -> str:
    return Path(path).stem


def compare(root: Path, base: str, folders: list[str], max_lines: int) -> tuple[list[str], int, int]:
    """Return the new findings as printable lines, and the base and head finding totals."""
    head_files = _python_files(root, folders)
    renamed = _renames(root, base)
    b_plain, b_cx, b_dup, b_lines = _base_findings(root, base, folders)
    h_plain, h_cx, h_dup, h_lines = _findings(root, head_files)

    def move(path: str) -> str:
        return renamed.get(path, path)

    stems = {_stem(old): _stem(new) for old, new in renamed.items()}
    b_plain = Counter({(move(p), c, msg): n for (p, c, msg), n in b_plain.items()})
    b_cx = {(move(p), name): v for (p, name), v in b_cx.items()}
    b_dup = Counter({tuple(sorted(stems.get(x, x) for x in key)): n for key, n in b_dup.items()})
    b_lines = {move(p): n for p, n in b_lines.items()}

    new = _plain_and_duplicates(h_plain, b_plain, h_dup, b_dup) + _complexity(h_cx, b_cx)
    new += _growth(h_lines, b_lines, max_lines)
    return new, _total(b_plain, b_cx, b_dup), _total(h_plain, h_cx, h_dup)


def _plain_and_duplicates(h_plain: Counter, b_plain: Counter, h_dup: Counter, b_dup: Counter) -> list[str]:
    new = [f"new {key[1]} {key[0]}: {key[2]} (base {b_plain.get(key, 0)}, now {n})"
           for key, n in sorted(h_plain.items()) if n > b_plain.get(key, 0)]
    return new + [f"new duplicate block between {', '.join(key)} (base {b_dup.get(key, 0)}, now {n})"
                  for key, n in sorted(h_dup.items()) if n > b_dup.get(key, 0)]


def _complexity(h_cx: dict, b_cx: dict) -> list[str]:
    """A function over the limit is new when it has no base counterpart or is more complex than it."""
    new = []
    for (path, name), values in sorted(h_cx.items()):
        before = sorted(b_cx.get((path, name), []), reverse=True)
        for i, value in enumerate(sorted(values, reverse=True)):
            if i >= len(before) or value > before[i]:
                was = before[i] if i < len(before) else "at or under the limit"
                new.append(f"new C901 {path}: `{name}` complexity {value} (base {was})")
    return new


def _growth(h_lines: dict, b_lines: dict, max_lines: int) -> list[str]:
    return [f"new file-growth {path}: {n} lines, over {max_lines} (base {b_lines.get(path, 'absent')})"
            for path, n in sorted(h_lines.items()) if n > max_lines and n > b_lines.get(path, 0)]


def _total(plain: Counter, cx: dict, dup: Counter) -> int:
    return sum(plain.values()) + sum(len(v) for v in cx.values()) + sum(dup.values())


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
