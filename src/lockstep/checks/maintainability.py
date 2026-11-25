"""Fail only on maintainability findings this branch adds; findings already on the base never block.

Compares the tree where the branch started (the merge base with --base) with the working tree, over the
Python files under the given folders:

- ruff (pinned): blind `except` (BLE), `try/except/pass` and `try/except/continue` (S110, S112), and
  function complexity (C901). A complexity finding is new when a function over the limit has no base
  function of that name at least as complex, so an unrelated edit inside an already complex function
  passes and a body edit that adds a branch fails.
- duplicate code: every window of 6 code lines (blank, comment, import and docstring lines left out) that occurs
  more than once; new when there are more repeated windows than on the base, so a third copy counts.
- file growth: a file over --max-lines that grew on this branch (a renamed file keeps its base size).

Findings are counted without paths or line numbers, so code moved within or between files, or a file
renamed, is not new; the price is that removing one finding and adding a like one elsewhere passes.
Not covered: an existing helper rewritten under a new name (that needs reading for meaning), or a copy
with renamed variables (windows match exact tokens). Exit 0 when
nothing is new or the base is missing, 1 on a new finding, 2 when a tool fails. Base results are cached
under the git folder by base commit and a hash of this module. Pilot for AES (Brian, 2026-11-24, slice 3
of the Reddit-ideas plan: "i will trust your jdugement on the impelemtnation prirotiy"); a Lockstep check
each repository switches on in its `lockstep.yaml` since Brian, 2026-11-25 ("ia prpove yourr ecommednations").

Run as `lockstep check maintainability [--base REV] [--folders src,scripts] [--max-lines 800]`; off unless
`checks: {maintainability: block}` (or warn) is set.

Implements: lockstep-checks/maintainability-only-findings-the-branch-adds-fail,
    lockstep-checks/maintainability-off-unless-switched-on

Requirement text (generated):
    lockstep-checks/maintainability-only-findings-the-branch-adds-fail: `lockstep check
        maintainability --base <rev>` SHALL compare the merge base with the working tree over the
        Python files under `--folders` (default `src,scripts`) and exit 1 only on a finding the
        branch adds: a blind `except` or `try/except/pass` (ruff BLE, S110, S112), a function over
        the complexity limit more complex than on the base (C901), more repeated 6-line windows of
        code, or a file over `--max-lines` (default 800) that grew. It SHALL end with `RESULT
        maintainability new=<n> base_findings=<n> head_findings=<n> exit=<0|1>`, SHALL exit 0 with a
        `skipped=` line when the base is missing or no Python file changed, and SHALL exit 2 when a
        tool fails.
    lockstep-checks/maintainability-off-unless-switched-on: `maintainability` SHALL be a check name
        in `lockstep.yaml`, `off` when absent, so a repository runs it only after setting it to
        `block` or `warn`; the template's `make check` SHALL call it, printing `maintainability:
        skipped (off)` until then.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:maintainability.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/maintainability-only-findings-the-branch-adds-fail, lockstep-checks/maintainability-off-unless-switched-on

### Requirement: Maintainability: Only findings the branch adds fail

`lockstep check maintainability --base <rev>` SHALL compare the merge base with the working tree over the Python
files under `--folders` (default `src,scripts`) and exit 1 only on a finding the branch adds: a blind `except` or
`try/except/pass` (ruff BLE, S110, S112), a function over the complexity limit more complex than on the base (C901),
more repeated 6-line windows of code, or a file over `--max-lines` (default 800) that grew. It SHALL end with
`RESULT maintainability new=<n> base_findings=<n> head_findings=<n> exit=<0|1>`, SHALL exit 0 with a `skipped=` line
when the base is missing or no Python file changed, and SHALL exit 2 when a tool fails.

Source: Brian, 2026-11-24 (Reddit-ideas plan, slice 3: "i will trust your jdugement on the impelemtnation prirotiy"; an AES script until now) and Brian, 2026-11-25: "ia prpove yourr ecommednations" (moved into Lockstep)

#### Scenario: Maintainability: Only findings the branch adds fail

- **GIVEN** a branch that adds a blind `except`, raises a function's complexity, adds a third copy of a block, or
  grows a large file
- **WHEN** `lockstep check maintainability --base main` runs
- **THEN** it exits 1 naming the finding; a finding already on the base, moved or renamed, passes

### Requirement: Maintainability: Off unless switched on

`maintainability` SHALL be a check name in `lockstep.yaml`, `off` when absent, so a repository runs it only after
setting it to `block` or `warn`; the template's `make check` SHALL call it, printing `maintainability: skipped (off)`
until then.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations"

#### Scenario: Maintainability: Off unless switched on

- **GIVEN** a branch adding a blind `except` and no `maintainability` in `lockstep.yaml`
- **WHEN** `lockstep check maintainability` runs, then runs again after `checks: {maintainability: block}`
- **THEN** the first prints `maintainability: skipped (off)` and exits 0; the second exits 1 with its RESULT line

Tested by: tests/lockstep/checks/test_lockstep_check_maintainability.py

Declares (typed signatures, from the plan):
  run(root: Path, base_rev: str='origin/main', folders: tuple[str, ...]=('src', 'scripts'), max_lines: int=800) -> int
  main(argv: list[str] | None=None) -> int
[[[end]]]
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import tokenize
from collections import Counter, defaultdict
from pathlib import Path

from lockstep.checks.changed import compare_with, extract

RUFF = ["uvx", "ruff@0.14.0", "check", "--isolated", "--select", "BLE,S110,S112,C901", "--output-format", "json", "--exit-zero"]
WINDOW = 6  # code lines in a duplicate window
SKIPPED = {tokenize.NL, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING, tokenize.ENDMARKER}
COMPLEX = re.compile(r"^`(?P<name>[^`]+)` is too complex \((?P<n>\d+) > \d+\)$")


class _ToolFailed(RuntimeError):
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
        if parts[i].startswith(("R", "C")):  # a copy is listed but keeps its original
            if parts[i].startswith("R"):
                renamed[parts[i + 1]] = parts[i + 2]
            i += 3
        else:
            i += 2
    return renamed


def _json_output(name: str, done: subprocess.CompletedProcess) -> list:
    try:
        found = json.loads(done.stdout)
    except json.JSONDecodeError as exc:
        raise _ToolFailed(f"{name} exit {done.returncode}: {(done.stderr or done.stdout).strip()[-300:]}") from exc
    if not isinstance(found, list):
        raise _ToolFailed(f"{name} printed JSON that is not a list")
    return found


def _ruff(cwd: Path, files: list[str]) -> list[dict]:
    if not files:
        return []
    done = subprocess.run([*RUFF, *files], cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:  # --exit-zero: findings exit 0, so anything else is a failed run
        raise _ToolFailed(f"ruff exit {done.returncode}: {done.stderr.strip()[-300:]}")
    found = _json_output("ruff", done)
    for item in found:
        item["filename"] = Path(item["filename"]).resolve().relative_to(cwd.resolve()).as_posix()
    return found


def _code_lines(text: str) -> list[str]:
    """Code lines as token text: no blank, comment, import or docstring lines (generated plan copies sit in
    docstrings, so the same requirement text in two files is not duplicate code)."""
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, SyntaxError):  # not parseable: fall back to the plain lines
        return [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    rows: dict = defaultdict(list)
    statement_start, in_import = True, False
    for tok in tokens:
        if tok.type == tokenize.NEWLINE:
            statement_start, in_import = True, False
        elif in_import or tok.type in SKIPPED or (tok.type == tokenize.STRING and statement_start):
            continue  # a whole import statement, or a string that starts one (docstring, bare string)
        elif statement_start and tok.string in ("import", "from"):
            in_import = True
        else:
            statement_start = False
            rows[tok.start[0]].append(tok.string)
    return [" ".join(row) for _, row in sorted(rows.items())]


def _duplicates(cwd: Path, files: list[str]) -> dict[str, list[str]]:
    """Each window of WINDOW code lines that occurs more than once, with the file of every occurrence.

    pylint duplicate-code was tried first and dropped: with three identical blocks it reports only one
    pair, so a third copy of existing code passed, and it took 6 to 13 seconds a tree (measured
    2026-11-24 on AES).
    """
    seen: dict = defaultdict(list)
    for name in files:
        lines = _code_lines((cwd / name).read_text(errors="replace"))
        for i in range(len(lines) - WINDOW + 1):
            seen[hashlib.sha1("\n".join(lines[i:i + WINDOW]).encode()).hexdigest()[:16]].append(name)
    return {key: sorted(where) for key, where in seen.items() if len(where) > 1}


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
    fd, temp = tempfile.mkstemp(dir=cached.parent, suffix=".tmp")
    os.close(fd)
    try:
        Path(temp).write_text(json.dumps(found))
        os.replace(temp, cached)
    except BaseException:
        Path(temp).unlink(missing_ok=True)
        raise
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


def _copies(windows: dict[str, list[str]]) -> int:
    """Repeated windows: every occurrence after the first of each window of code lines."""
    return sum(len(where) - 1 for where in windows.values())


def _duplicates_added(head: dict[str, list[str]], base: dict[str, list[str]]) -> list[str]:
    if _copies(head) <= _copies(base):
        return []
    grew = sorted({", ".join(sorted(set(where))) for key, where in head.items() if len(where) > len(base.get(key, [None]))})
    return [f"new duplicate code: {_copies(base)} repeated {WINDOW}-line windows on the base, {_copies(head)} now; in "
            + ("; ".join(grew) if grew else "files already sharing code")]


def _growth(head: dict, base: dict, renamed: dict, max_lines: int) -> list[str]:
    before = {renamed.get(p, p): n for p, n in base.items()}
    return [f"new file-growth {path}: {n} lines, over {max_lines} (base {before.get(path, 'absent')})"
            for path, n in sorted(head.items()) if n > max_lines and n > before.get(path, 0)]


def _compare(root: Path, base: str, folders: list[str], max_lines: int) -> tuple[list[str], int, int]:
    """Return the new findings as printable lines, and the base and head finding totals."""
    b = _base_findings(root, base, folders)
    h = _findings(root, _python_files(root, folders))
    new = _plain(h["plain"], b["plain"]) + _complexity(h["cx"], b["cx"]) + _duplicates_added(h["dup"], b["dup"])
    new += _growth(h["lines"], b["lines"], _renames(root, base), max_lines)
    return new, _total(b), _total(h)


def _total(found: dict) -> int:
    return sum(map(len, found["plain"].values())) + sum(map(len, found["cx"].values())) + _copies(found["dup"])


def run(root: Path, base_rev: str = "origin/main", folders: tuple[str, ...] = ("src", "scripts"),
        max_lines: int = 800) -> int:
    """Print the new findings and the RESULT line; return 0 (nothing new or no base), 1 (new) or 2 (a tool failed)."""
    root = root.resolve()
    kept = [f for f in folders if f]
    base = compare_with(root, base_rev)
    if base is None:
        print(f"RESULT maintainability skipped=base-missing base={base_rev} exit=0")
        return 0
    changed = [p for p in _git(root, "diff", "--name-only", "-z", base, "--", *kept).split("\0") if p.endswith(".py")]
    untracked = [p for p in _git(root, "ls-files", "-z", "--others", "--exclude-standard", "--", *kept).split("\0") if p.endswith(".py")]
    if not changed and not untracked:
        print("RESULT maintainability skipped=no-python-change exit=0")
        return 0
    try:
        new, base_total, head_total = _compare(root, base, kept, max_lines)
    except (_ToolFailed, subprocess.CalledProcessError, OSError) as exc:
        print(f"maintainability: a tool failed: {exc}")
        print("RESULT maintainability tool-failed exit=2")
        return 2
    for line in new:
        print(line)
    code = 1 if new else 0
    print(f"RESULT maintainability new={len(new)} base_findings={base_total} head_findings={head_total} exit={code}")
    return code


def main(argv: list[str] | None = None) -> int:
    """The same check with no `lockstep.yaml` mode applied: `python -m lockstep.checks.maintainability`."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=".")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--folders", default="src,scripts", help="comma-separated folders to read")
    parser.add_argument("--max-lines", type=int, default=800)
    args = parser.parse_args(argv)
    return run(Path(args.repo), args.base, tuple(args.folders.split(",")), args.max_lines)


if __name__ == "__main__":
    raise SystemExit(main())
