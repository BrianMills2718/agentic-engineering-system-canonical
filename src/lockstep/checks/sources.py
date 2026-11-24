"""Sources check: every requirement and decision record says where it came from.

A `Source:` line is either `Source: Brian, <date>: "<quote>"` or `Source: inferred by agent (<basis>)`;
a decision record may give `Decider:` instead. Items an agent inferred stay visible as such until Brian
accepts or cuts them.

Implements: lockstep-checks/sources-every-normative-item-names-its-source

Requirement text (generated):
    lockstep-checks/sources-every-normative-item-names-its-source: The sources check SHALL fail when
        an OpenSpec requirement (in `openspec/specs` or an active change delta) or a decision record
        in `docs/decisions/` has no `Source:` line, so nobody mistakes an agent's guess for Brian's
        rule. A decision record may give a `Decider:` line instead.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:sources.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/sources-every-normative-item-names-its-source, lockstep-checks/sources-the-statement-comes-before-its-source-line

### Requirement: Sources: Every normative item names its source

The sources check SHALL fail when an OpenSpec requirement (in `openspec/specs` or an active change delta)
or a decision record in `docs/decisions/` has no `Source:` line, so nobody mistakes an agent's guess for
Brian's rule. A decision record may give a `Decider:` line instead.

Source: Brian, 2026-10-15: "this applies much more to normative docuemntation. i dont ingeneral care as much abotu the implemetnation"; "i approve" Ported from code2-template `openspec/specs/sources/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Sources: Requirement without source fails

- **GIVEN** a spec whose requirement "Do the thing" has no `Source:` line
- **WHEN** the sources check runs
- **THEN** it reports `core/do-the-thing` as missing a source and exits 1

#### Scenario: Sources: Decision without source fails

- **GIVEN** a decision record `docs/decisions/0001-x.md` with neither `Source:` nor `Decider:`
- **WHEN** the sources check runs
- **THEN** it reports `decision/0001-x` as missing a source and exits 1

#### Scenario: Sources: Labeled items pass and are classified

- **GIVEN** one requirement with `Source: Brian, 2026-10-15: "..."` and one with `Source: inferred by agent (...)`
- **WHEN** the sources check runs with `--json`
- **THEN** it exits 0 and lists the first as `brian` and the second as `inferred`

### Requirement: Sources: The statement comes before its Source line

The sources check SHALL fail when an OpenSpec requirement's first paragraph is its `Source:` line, printing
`source-first <id>` with the file, so every requirement reads statement first and the spec reader never takes an
empty statement.

Source: Brian, 2026-11-23: "i approve", to Q49 in `docs/planning/open-questions.json` ("Should every requirement put
its statement first and its `Source:` line after it, checked by `lockstep check`?").

#### Scenario: Sources: A Source line before the statement fails

- **GIVEN** a requirement whose first line under its heading is `Source: Brian, 2026-11-23: "yes"` and whose statement follows
- **WHEN** `lockstep check sources` runs
- **THEN** it prints `source-first` with that requirement's ID and exits 1, and once the statement comes first it reports nothing for it

Tested by: tests/lockstep/checks/test_lockstep_check_sources.py
[[[end]]]
"""

from dataclasses import asdict, dataclass
from pathlib import Path
import re

from lockstep.checks.spec import slug

DEFAULT_HUMAN_PATTERN = "brian"
_REQ = re.compile(r"^###\s+Requirement:\s*(.+?)\s*$")
_SOURCE = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?(Source|Decider)(?:\*\*)?:\s*(.+?)\s*$")
_SKIPPED_SECTIONS = ("## REMOVED", "## RENAMED")


@dataclass(frozen=True)
class Item:
    """One normative item: its ID, title, file, source class (brian, inferred, other, missing), the
    source line's text, the item's first paragraph (what it requires or decides), and whether its `Source:`
    line came before that paragraph."""

    id: str
    title: str
    where: str
    source: str
    text: str
    statement: str = ""
    source_first: bool = False


def classify(text: str, human_pattern: str = DEFAULT_HUMAN_PATTERN) -> str:
    """Name the kind of source a `Source:` or `Decider:` value gives.

    Args:
        text: The value after the colon; empty when there is no line.
        human_pattern: Regex (case-insensitive, matched at the start) for a source that names the
            human owner; defaults to `brian`, what code2check hardcoded.

    Returns:
        `missing`, `inferred`, `brian` or `other`.
    """
    low = text.lower()
    if not low:
        return "missing"
    if low.startswith("inferred"):
        return "inferred"
    if re.match(human_pattern, text, re.IGNORECASE):
        return "brian"
    return "other"


def _spec_items(root: Path, spec: Path, pattern: str) -> list[Item]:
    """Read the requirements of one spec or change delta with their source lines."""
    items: list[Item] = []
    capability = spec.parent.name
    current: dict | None = None
    skipping = False

    def close() -> None:
        """Record the requirement being read, if any."""
        if current is not None:
            items.append(Item(current["id"], current["title"], str(spec.relative_to(root)),
                              classify(current["text"], pattern), current["text"], " ".join(current["body"]),
                              current["source_first"]))

    for line in spec.read_text().splitlines():
        if line.startswith("## "):
            close()
            current = None
            skipping = line.startswith(_SKIPPED_SECTIONS)
            continue
        m = _REQ.match(line)
        if m:
            close()
            current = None if skipping else {"id": f"{capability}/{slug(m.group(1))}", "title": m.group(1), "text": "", "body": [],
                                         "done": False, "source_first": False}
            continue
        s = _SOURCE.match(line)
        if s and current is not None and s.group(1) == "Source" and not current["text"]:
            current["text"] = s.group(2)
            current["source_first"] = not current["body"]
        elif current is not None and not current["done"] and not line.startswith("#"):
            if line.strip():
                current["body"].append(line.strip())
            elif current["body"]:
                current["done"] = True
    close()
    return items


def _decision_item(root: Path, record: Path, pattern: str) -> Item:
    """Read one decision record's title and its `Source:` or `Decider:` line."""
    title, text, body, section = record.stem, "", [], ""
    for line in record.read_text().splitlines():
        if line.startswith("# ") and title == record.stem:
            title = line[2:].strip()
        if line.startswith("## "):
            section = line[3:].strip().lower()
            continue
        s = _SOURCE.match(line)
        if s and not text:
            text = s.group(2)
        elif section.startswith("decision"):
            if line.strip() and not line.startswith(("#", "|")):
                body.append(line.strip())
            elif body:
                section = "done"
    return Item(f"decision/{record.stem}", title, str(record.relative_to(root)), classify(text, pattern), text, " ".join(body))


def check(root: Path, human_pattern: str = DEFAULT_HUMAN_PATTERN) -> list[Item]:
    """List every requirement and decision record under root with its source.

    Args:
        root: Repository root.
        human_pattern: See `classify`.

    Returns:
        Items from `openspec/specs`, then active change deltas, then `docs/decisions/*.md`.
    """
    specs = sorted((root / "openspec" / "specs").glob("*/spec.md"))
    changes = sorted(f for f in (root / "openspec" / "changes").glob("*/specs/*/spec.md") if f.parts[-4] != "archive")
    items = [i for spec in specs + changes for i in _spec_items(root, spec, human_pattern)]
    items += [_decision_item(root, r, human_pattern) for r in sorted((root / "docs" / "decisions").glob("[0-9]*.md"))]
    return items


def as_dicts(items: list[Item]) -> list[dict]:
    """Turn items into plain dictionaries for JSON output.

    Args:
        items: Items from `check`.

    Returns:
        One dictionary per item.
    """
    return [asdict(i) for i in items]
