"""Read decision records and what each one governs, from the lines they already carry.

A decision record in `docs/decisions/` names what it governs on a `Governs:` line (paths, folders, requirement or
capability IDs, or other names such as rule IDs) and its state on a `status:` front-matter field or a MADR
`- Status:` bullet; a superseded record names its successor in `superseded_by:` or after "superseded by". This
module reads those lines; it adds no new one.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

from lockstep.checks.sources import DEFAULT_HUMAN_PATTERN, _decision_item

_GOVERNS = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?Governs(?:\*\*)?:\s*(.+?)\s*$")
_STATUS = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?Status(?:\*\*)?:\s*(.+?)\s*$", re.IGNORECASE)
_FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_SUPERSEDED_BY = re.compile(r"superseded by\s+(.+)", re.IGNORECASE)
MAX_HANDED = 3
MAX_CHARS = 600


@dataclass
class Decision:
    """One decision record: ID, title, file, status, successor, statement, source, and its `Governs:` targets.

    `paths` are repository paths the record governs (a folder ends in `/`), `ids` are requirement or capability
    IDs, and `raw` is every target as written.
    """

    id: str
    title: str
    file: str
    status: str
    superseded_by: str
    statement: str
    source: str
    source_kind: str
    raw: list[str] = field(default_factory=list)
    paths: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)

    @property
    def superseded(self) -> bool:
        return self.status.lower().startswith("superseded") or bool(self.superseded_by)


def _front(text: str) -> dict[str, str]:
    m = _FRONT.match(text)
    if not m:
        return {}
    found = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t", "-")):
            found[key.strip().lower()] = value.strip().strip("'\"")
    return found


def read(root: Path, known_ids: set[str] | None = None, human_pattern: str = DEFAULT_HUMAN_PATTERN) -> list[Decision]:
    """Read every `docs/decisions/[0-9]*.md` record under root.

    Args:
        root: Repository root.
        known_ids: Requirement and capability IDs the plan defines; a target that is not a path and is in this set
            goes in `ids`.
        human_pattern: See `sources.classify`.

    Returns:
        The records in file order; none when there is no `docs/decisions/` folder.
    """
    root = Path(root)
    known = known_ids or set()
    found = []
    for record in sorted((root / "docs" / "decisions").glob("[0-9]*.md")):
        text = record.read_text(errors="replace")
        front = _front(text)
        opening = _FRONT.match(text)
        body = text[opening.end():] if opening else text
        status, successor = front.get("status", ""), front.get("superseded_by", "")
        raw: list[str] = []
        for line in body.splitlines():
            if not raw and (m := _GOVERNS.match(line)):
                raw = [t.strip().rstrip(".").strip() for t in m.group(1).split(",") if t.strip().rstrip(".").strip()]
            elif not status and (m := _STATUS.match(line)):
                status = m.group(1)
        if not successor and (m := _SUPERSEDED_BY.search(status)):
            successor = m.group(1).strip().rstrip(".")
        item = _decision_item(root, record, human_pattern)
        decision = Decision(item.id, item.title, item.where, status.split()[0].lower() if status else "",
                            successor, item.statement, item.text, item.source, raw)
        for target in raw:
            plain = target.split("#", 1)[0].strip("`")
            path = root / plain
            if plain and path.exists() and path.resolve().is_relative_to(root.resolve()):
                decision.paths.append(plain.rstrip("/") + ("/" if path.is_dir() else ""))
            elif target in known:
                decision.ids.append(target)
        found.append(decision)
    return found


def governing(decisions: list[Decision], rel: str, implemented: list[str]) -> list[Decision]:
    """The decisions that govern file rel, most direct first: by its own path, then through a requirement or
    capability it implements, then through a folder above it."""
    caps = {i.split("/", 1)[0] for i in implemented}
    direct = [d for d in decisions if rel in d.paths]
    by_id = [d for d in decisions if d not in direct and any(i in implemented or i in caps for i in d.ids)]
    folder = [d for d in decisions if d not in direct and d not in by_id
              and any(p.endswith("/") and rel.startswith(p) for p in d.paths)]
    return direct + by_id + folder


def packet(root: Path, rel: str, implemented: list[str]) -> tuple[list[str], str]:
    """What the edit hook hands over about decisions before rel is edited: (decision IDs, text).

    Implements: lockstep-guard/agents-get-the-decisions-that-govern-a-file

    Requirement text (generated):
        lockstep-guard/agents-get-the-decisions-that-govern-a-file: In a repository with OpenSpec
            specs and a `docs/decisions/` folder, the edit hook SHALL hand an agent that edits a
            file, or names it in a shell command, each decision record whose `Governs:` line names
            that file, a folder above it (a target ending in `/` or naming an existing folder), or a
            requirement or capability the file implements, after any requirement text and without a
            `permissionDecision`. It SHALL read the record's existing lines only: `Governs:` (or `-
            Governs:`, comma separated, anchors ignored for paths), `status:` front matter or a
            `Status:` line, and `superseded_by:` or the text after "superseded by". Each decision
            SHALL be given as its ID, title, status, file and decision paragraph cut at 600
            characters, at most three in full (own path first, then requirement or capability, then
            folder) and the rest by ID; a superseded decision SHALL be flagged with its successor.
            The hook SHALL log the decision IDs as `decisions` on the `openspec_text` record. No
            check SHALL fail on a `Governs:` target that names nothing.
    """
    from lockstep.checks.spec import read_plan

    root = Path(root)
    if not (root / "docs" / "decisions").is_dir():
        return [], ""
    known: set[str] = set()
    for plan in (read_plan(root), read_plan(root, changes=True)):
        known |= set(plan.requirements) | {i.split("/", 1)[0] for i in plan.requirements}
    found = governing(read(root, known), rel, implemented)
    if not found:
        return [], ""
    blocks = []
    for d in found[:MAX_HANDED]:
        state = d.status or "no status line"
        flag = (f" SUPERSEDED by {d.superseded_by or 'a later decision'}: check this code still follows that "
                "decision, and move the `Governs:` line to it." if d.superseded else "")
        statement = d.statement if len(d.statement) <= MAX_CHARS else d.statement[:MAX_CHARS].rstrip() + " ..."
        blocks.append(f"{d.id}: {d.title} ({state}; {d.file}).{flag}\n{statement}".rstrip())
    more = [d.id for d in found[MAX_HANDED:]]
    tail = f"\n\nAlso governed by: {', '.join(more)}." if more else ""
    header = f"Decisions that govern {rel} (their `Governs:` lines):"
    return [d.id for d in found], header + "\n\n" + "\n\n".join(blocks) + tail
