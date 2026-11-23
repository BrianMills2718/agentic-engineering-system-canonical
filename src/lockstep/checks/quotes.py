"""Marked quotes: passages of requirement text copied into Markdown documents, compared with the specs.

Implements: lockstep-checks/trace-a-marked-quote-matches-its-requirement

Requirement text (generated):
    lockstep-checks/trace-a-marked-quote-matches-its-requirement: The trace check SHALL read, in
        every Markdown file tracked by git outside `openspec/`, each passage between `<!-- lockstep
        quote: <requirement id> -->` and `<!-- /lockstep quote -->`. It SHALL report `stale-quote`
        and fail when the passage, with runs of whitespace counting as one space, does not appear in
        the text of that requirement or of one of its scenarios, in `openspec/specs/` or in an
        active change's spec delta. It SHALL report `unknown` when no spec or active change defines
        the ID, and `unclosed-quote` when a start marker has no end marker after it in the same
        file. Each finding SHALL name the file and line of the start marker. A marker inside a code
        span or a fenced code block is shown as code, not used as a marker, and SHALL be skipped; a
        passage SHALL be compared with its code words kept. In a folder that is not a git repository
        it SHALL read every Markdown file outside `openspec/` and folders whose name starts with a
        dot.

A quote is marked `<!-- lockstep quote: <requirement id> -->passage<!-- /lockstep quote -->`; the
passage may span lines and sit inside a sentence or a table cell. Raw Markdown is compared with raw
requirement text, runs of whitespace counting as one space. A passage that is not marked is not read.
Nothing is stored; the comparison is made on every run.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess

from lockstep.checks.spec import Plan, normal, read_plan

START = re.compile(r"<!--[ \t]*lockstep quote:[ \t]*(\S+?)[ \t]*-->")
END = re.compile(r"<!--[ \t]*/lockstep quote[ \t]*-->")


@dataclass(frozen=True)
class Quote:
    """One marked quote: its file, the line of its start marker, the ID, the passage and its state.

    `state` is `current` (the passage appears in the requirement's or a scenario's text), `stale`
    (it does not), `unknown` (no plan defines the ID) or `unclosed` (no end marker follows).
    """

    path: str
    line: int
    id: str
    passage: str
    state: str


def markdown_files(root: Path) -> list[Path]:
    """Return the Markdown files whose quotes are read, outside `openspec/`.

    Args:
        root: Repository root.

    Returns:
        The `*.md` files git tracks under root; in a folder that is not a git repository, every
        `*.md` file outside folders whose name starts with a dot. Sorted; `openspec/` left out.
    """
    listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", "*.md"], capture_output=True)
    if listed.returncode == 0:
        rels = [Path(p) for p in listed.stdout.decode().split("\0") if p]
    else:
        rels = [p.relative_to(root) for p in root.rglob("*.md")
                if not any(part.startswith(".") for part in p.relative_to(root).parts[:-1])]
    return sorted(root / r for r in rels if r.parts[0] != "openspec" and (root / r).is_file())


def _texts(ident: str, plan: Plan) -> list[str]:
    """Return the requirement's statement and its scenarios' text (or a scenario's own text) in plan."""
    if ident in plan.requirements:
        return [plan.text.get(ident, "")] + [plan.scenario_text.get(s, "") for s, p in plan.parent.items() if p == ident]
    if ident in plan.scenarios:
        return [plan.scenario_text.get(ident, "")]
    return []


def _state(ident: str, passage: str, plans: list[Plan]) -> str:
    """Say whether passage appears in the text plans give ident: current, stale or unknown."""
    if not any(ident in p.requirements or ident in p.scenarios for p in plans):
        return "unknown"
    wanted = normal(passage)
    return "current" if any(wanted in normal(t) for p in plans for t in _texts(ident, p)) else "stale"


_CODE = re.compile(r"^```.*?^```[^\n]*$|(`+)[^\n]+?\1", re.MULTILINE | re.DOTALL)


def _blank_code(text: str) -> str:
    """Return text with fenced blocks and inline code spans blanked, so a marker shown as code is not a marker.

    Line breaks are kept, so line numbers stay right.
    """
    return _CODE.sub(lambda m: "".join(c if c == "\n" else " " for c in m.group(0)), text)


def check(root: Path, plans: list[Plan] | None = None) -> list[Quote]:
    """Find every marked quote in the Markdown files and compare it with its requirement.

    Implements: lockstep-checks/trace-a-marked-quote-matches-its-requirement

    Requirement text (generated):
        lockstep-checks/trace-a-marked-quote-matches-its-requirement: The trace check SHALL read, in
            every Markdown file tracked by git outside `openspec/`, each passage between `<!--
            lockstep quote: <requirement id> -->` and `<!-- /lockstep quote -->`. It SHALL report
            `stale-quote` and fail when the passage, with runs of whitespace counting as one space,
            does not appear in the text of that requirement or of one of its scenarios, in
            `openspec/specs/` or in an active change's spec delta. It SHALL report `unknown` when no
            spec or active change defines the ID, and `unclosed-quote` when a start marker has no
            end marker after it in the same file. Each finding SHALL name the file and line of the
            start marker. A marker inside a code span or a fenced code block is shown as code, not
            used as a marker, and SHALL be skipped; a passage SHALL be compared with its code words
            kept. In a folder that is not a git repository it SHALL read every Markdown file outside
            `openspec/` and folders whose name starts with a dot.

    Args:
        root: Repository root.
        plans: The plans whose text counts; default `openspec/specs/` and the active change deltas.

    Returns:
        Each quote in file order, then by position in its file.
    """
    root = Path(root)
    if plans is None:
        plans = [read_plan(root), read_plan(root, changes=True)]
    found = []
    for path in markdown_files(root):
        text = path.read_text(errors="replace")
        if "lockstep quote" not in text:
            continue
        rel = str(path.relative_to(root))
        markers = _blank_code(text)  # find markers here; read passages from text
        at = 0
        while (start := START.search(markers, at)) is not None:
            line = text.count("\n", 0, start.start()) + 1
            end = END.search(markers, start.end())
            if end is None:
                found.append(Quote(rel, line, start.group(1), text[start.end():], "unclosed"))
                break
            passage = text[start.end():end.start()]
            found.append(Quote(rel, line, start.group(1), passage, _state(start.group(1), passage, plans)))
            at = end.end()
    return found
