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
    source line's text, and the item's first paragraph (what it requires or decides)."""

    id: str
    title: str
    where: str
    source: str
    text: str
    statement: str = ""


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
                              classify(current["text"], pattern), current["text"], " ".join(current["body"])))

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
                                         "done": False}
            continue
        s = _SOURCE.match(line)
        if s and current is not None and s.group(1) == "Source" and not current["text"]:
            current["text"] = s.group(2)
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
