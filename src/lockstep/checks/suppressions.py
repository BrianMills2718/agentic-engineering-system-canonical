"""Suppressions check: an added `# noqa`, `# type: ignore` or import-linter ignore names its reason.

Implements: lockstep-checks/suppressions-an-added-suppression-comment-names-its-reason,
    lockstep-checks/suppressions-an-added-import-linter-ignore-names-its-reason,
    lockstep-checks/suppressions-count-line-and-exit-status

Requirement text (generated):
    lockstep-checks/suppressions-an-added-suppression-comment-names-its-reason: `lockstep check
        suppressions --base <rev>` SHALL read the lines added between where the branch started (as
        for the changed check) and the working tree in tracked `.py` files, and report each added
        line holding `# noqa`, `# type: ignore`, `# pyright: ignore` or `# pylint: disable` that is
        not followed, later on the same line, by a further `#` comment of at least three words,
        printing `unreasoned <path>:<line> <directive>`. Lines present at the base SHALL never be
        reported.
    lockstep-checks/suppressions-an-added-import-linter-ignore-names-its-reason: The suppressions
        check SHALL report each entry added to an import-linter `ignore_imports` list with no
        reason, printing `unreasoned <path>:<line> ignore_imports`. In `.importlinter` and
        `setup.cfg` the reason SHALL be a `#` or `;` comment line of at least three words directly
        above the entry; in `pyproject.toml` it SHALL be a `#` comment of at least three words on
        the entry's line.
    lockstep-checks/suppressions-count-line-and-exit-status: The suppressions check SHALL end with
        `RESULT suppressions added=<n> reasoned=<n> unreasoned=<n> exit=<0|1>`, counting added
        suppressions, and exit 1 when `unreasoned` is above zero. When `<rev>` names no commit it
        SHALL check nothing, print `RESULT suppressions skipped="base <rev> not found" exit=0` and
        exit 0.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:suppressions.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/suppressions-an-added-suppression-comment-names-its-reason, lockstep-checks/suppressions-an-added-import-linter-ignore-names-its-reason, lockstep-checks/suppressions-count-line-and-exit-status

### Requirement: Suppressions: An added suppression comment names its reason

`lockstep check suppressions --base <rev>` SHALL read the lines added between where the branch started (as for the
changed check) and the working tree in tracked `.py` files, and report each added line holding `# noqa`,
`# type: ignore`, `# pyright: ignore` or `# pylint: disable` that is not followed, later on the same line, by a
further `#` comment of at least three words, printing `unreasoned <path>:<line> <directive>`. Lines present at the
base SHALL never be reported.

Source: Brian, 2026-11-24: "i approve adding the redit ideas to the plan and i will trust your jdugement on the
impelemtnation prirotiy" (this session; plan in `.project-brain/now.md`). The reason format and the three-word
minimum are inferred by agent: mypy rejects `# type: ignore[x] -- reason` and accepts a further `#` comment.

#### Scenario: Suppressions: An added noqa with no reason fails

- **GIVEN** a branch that adds the line `import os  # noqa: F401` to a tracked Python file
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it prints `unreasoned` with that file and line and exits 1

#### Scenario: Suppressions: A reason after the directive passes

- **GIVEN** a branch that adds `import os  # noqa: F401  # re-exported for the plugin loader` and `x = f()  # type: ignore[no-untyped-call]  # vendored stub has no types`
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it reports neither line and exits 0

#### Scenario: Suppressions: A suppression already at the base is not judged

- **GIVEN** a file that holds `import os  # noqa: F401` at the base and a branch that changes a different line of it
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it reports nothing and exits 0

### Requirement: Suppressions: An added import-linter ignore names its reason

The suppressions check SHALL report each entry added to an import-linter `ignore_imports` list with no reason,
printing `unreasoned <path>:<line> ignore_imports`. In `.importlinter` and `setup.cfg` the reason SHALL be a `#` or `;`
comment line of at least three words directly above the entry; in `pyproject.toml` it SHALL be a `#` comment of at
least three words on the entry's line.

Source: as the requirement above (Brian, 2026-11-24). Inferred by agent: import-linter reads `.importlinter` with
configparser, which strips a full-line comment and keeps an inline `#` as part of the value.

#### Scenario: Suppressions: An INI ignore needs a comment line above it

- **GIVEN** a branch that adds two entries under `ignore_imports` in `.importlinter`, one directly below `# the CLI wires the adapter in` and one with no comment above it
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it reports only the entry with no comment above it and exits 1

### Requirement: Suppressions: Count line and exit status

The suppressions check SHALL end with `RESULT suppressions added=<n> reasoned=<n> unreasoned=<n> exit=<0|1>`,
counting added suppressions, and exit 1 when `unreasoned` is above zero. When `<rev>` names no commit it SHALL
check nothing, print `RESULT suppressions skipped="base <rev> not found" exit=0` and exit 0.

Source: as the requirements above (Brian, 2026-11-24); the line shape follows the changed check's.

#### Scenario: Suppressions: A base that names no commit skips

- **GIVEN** a repository with no revision named `nope`
- **WHEN** `lockstep check suppressions --base nope` runs
- **THEN** it prints `RESULT suppressions skipped="base nope not found" exit=0` and exits 0

Tested by: tests/lockstep/checks/test_lockstep_check_suppressions.py

Declares (typed signatures, from the plan):
  Result
  check(root: Path, base: str) -> Result
[[[end]]]
"""

from dataclasses import dataclass, field
from pathlib import Path
import io
import re
import subprocess
import tokenize

from lockstep.checks.changed import compare_with

DIRECTIVE = re.compile(
    r"#\s*(?P<name>noqa|type:\s*ignore|pyright:\s*ignore|pylint:\s*disable)(?![\w\-])"
    r"(?P<codes>\[[^\]]*\]|:\s*[A-Z]+[0-9]+(?:\s*,\s*[A-Z]+[0-9]+)*|=[\w\-]+(?:\s*,\s*[\w\-]+)*)?",
    re.IGNORECASE,
)
REASON_WORDS = 3
COMMENT = ("#", ";")
INI_FILES = (".importlinter", "setup.cfg")
TOML_FILE = "pyproject.toml"
PATHSPEC = ("*.py", "*.importlinter", "*setup.cfg", "*pyproject.toml")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(?P<start>\d+)(?:,(?P<count>\d+))? @@")


@dataclass
class Result:
    """What the suppressions check found."""

    skipped: str = ""
    added: int = 0
    unreasoned: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when every added suppression names its reason."""
        return not self.unreasoned


def _is_reason(comment: str) -> bool:
    """True when a `#` comment's text has at least three words."""
    return len(re.findall(r"[A-Za-z][\w'\-]*", comment.lstrip("# "))) >= REASON_WORDS


def _added_lines(root: Path, base: str) -> dict[str, set[int]]:
    """Map each tracked file changed since base to the line numbers the working tree added.

    Lists the changed files with `-z` (so names with spaces or quotes survive), then reads each file's hunks.

    Args:
        root: Repository root.
        base: Commit to compare the working tree with.

    Returns:
        Path relative to root -> added line numbers (1-based, in the working-tree file).
    """
    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout

    names = git("diff", "--name-only", "-z", "-M", "--diff-filter=AMR", base, "--", *PATHSPEC).split("\0")
    added: dict[str, set[int]] = {}
    for rel in filter(None, names):
        if not (rel.endswith(".py") or Path(rel).name in (*INI_FILES, TOML_FILE)):
            continue
        for line in git("diff", "-U0", "-M", "--no-color", "--no-ext-diff", base, "--", rel).splitlines():
            match = HUNK.match(line)
            if match:
                start, count = int(match["start"]), int(match["count"] if match["count"] is not None else 1)
                added.setdefault(rel, set()).update(range(start, start + count))
    return added


def _comments(text: str) -> dict[int, str]:
    """Map each line number to the text of the comment on it, reading Python tokens so strings are not comments.

    Falls back to everything from the first `#` on each line when the text does not tokenize.
    """
    found: dict[int, str] = {}
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type == tokenize.COMMENT:
                found[token.start[0]] = token.string
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return {n: line[line.index("#"):] for n, line in enumerate(text.split("\n"), 1) if "#" in line}
    return found


def _python_findings(text: str, lines: set[int]) -> tuple[int, list[tuple[int, str]]]:
    """Count added suppression comments in Python text and list those with no reason.

    Returns:
        (number of added suppressions, [(line number, directive)] for those with no reason).
    """
    count, bad = 0, []
    for number, comment in sorted(_comments(text).items()):
        if number not in lines:
            continue
        for match in DIRECTIVE.finditer(comment):
            count += 1
            rest = comment[match.end():]
            reason = rest[rest.find("#"):] if "#" in rest else ""
            if not _is_reason(reason):
                bad.append((number, "# " + re.sub(r"\s+", " ", match["name"].lower())))
    return count, bad


def _ini_entries(text: str) -> list[tuple[int, bool]]:
    """List each `ignore_imports` entry in configparser text with whether the line above is a reason comment.

    As configparser does, comment lines (`#` or `;`, indented or not) and blank lines do not end the value; an
    unindented line that is not a comment (the next key or section) does.
    """
    rows: list[str] = text.split("\n")
    entries: list[tuple[int, bool]] = []
    inside = False
    for index, line in enumerate(rows):
        stripped = line.strip()
        if re.match(r"^ignore_imports\s*[=:]", line):
            inside = True
            value = re.split(r"[=:]", line, maxsplit=1)[1]
            if value.strip() and not value.strip().startswith(COMMENT):
                entries.append((index + 1, False))
            continue
        if not inside or not stripped or stripped.startswith(COMMENT):
            continue
        if line[:1] not in (" ", "\t"):
            inside = False
            continue
        above = rows[index - 1].strip() if index else ""
        entries.append((index + 1, above.startswith(COMMENT) and _is_reason(above.lstrip(";"))))
    return entries


def _toml_entries(text: str) -> list[tuple[int, bool]]:
    """List each `ignore_imports` entry in pyproject text with whether its own line carries a reason comment."""
    entries: list[tuple[int, bool]] = []
    inside = False
    for number, line in enumerate(text.split("\n"), 1):
        code, _, comment = line.partition("#")
        if not inside and re.match(r"^\s*ignore_imports\s*=\s*\[", code):
            inside = True
            code = code.split("[", 1)[1]
        if inside:
            if re.search(r"['\"]", code):
                entries.append((number, _is_reason(comment)))
            if "]" in code:
                inside = False
    return entries


def check(root: Path, base: str) -> Result:
    """Judge every suppression added since where the branch started.

    Args:
        root: Repository root.
        base: Git revision given as `--base`.

    Returns:
        The added count and each unreasoned finding as `<path>:<line> <directive>`; `skipped` when base names no
        commit.
    """
    start = compare_with(root, base)
    if start is None:
        return Result(skipped=f"base {base} not found")
    result = Result()
    for rel, lines in sorted(_added_lines(root, start).items()):
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_bytes().decode(errors="replace")
        name = Path(rel).name
        if rel.endswith(".py"):
            count, bad = _python_findings(text, lines)
            result.added += count
            result.unreasoned += [f"{rel}:{number} {directive}" for number, directive in bad]
            continue
        if name in INI_FILES:
            entries = _ini_entries(text)
        elif name == TOML_FILE:
            entries = _toml_entries(text)
        else:
            continue
        for number, reasoned in entries:
            if number in lines:
                result.added += 1
                if not reasoned:
                    result.unreasoned.append(f"{rel}:{number} ignore_imports")
    return result
