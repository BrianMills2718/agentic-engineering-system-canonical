"""Tests for decisions read from their existing `Governs:` and status lines (spec lockstep-guard)."""

import json
from pathlib import Path

import pytest

from lockstep.decisions import governing, packet, read
from lockstep import hook
from lockstep.hook import decide

SPEC = """\
# ship Specification

## Purpose

Ship.

## Requirements

### Requirement: Merge only checked commits

`ship` SHALL merge only a checked commit.

Source: Brian, 2026-10-24, "i approve"

#### Scenario: A failing check merges nothing

- **THEN** nothing merges
"""
REQ = "ship/merge-only-checked-commits"

FRONT = """\
---
status: superseded
superseded_by: docs/decisions/0003-newer.md
---

# Old way to ship

Governs: scripts/ship.py, RULE-SOMETHING.
(Superseded by Decision 0003.)

Source: Brian, 2026-10-01: "ok"

## Decision

Ship the old way.
"""
MADR = """\
# Ship through one command

- Status: accepted
- Source: Brian, 2026-10-02: "yes"
- Governs: ship

## Decision outcome

Every merge goes through `ship`.
"""
NEWER = """\
# Newer way to ship

- Status: accepted
- Source: inferred by agent (test)
- Governs: scripts/, docs/notes.md#part

## Decision outcome

Ship the newer way.
"""


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def repo(tmp_path) -> Path:
    write(tmp_path / "openspec/specs/ship/spec.md", SPEC)
    write(tmp_path / "scripts/ship.py", f'"""Ship.\n\nImplements: {REQ}\n"""\n\nx = 1\n')
    write(tmp_path / "scripts/other.py", '"""Nothing implemented."""\n')
    write(tmp_path / "docs/notes.md", "# Notes\n")
    write(tmp_path / "docs/decisions/0001-old.md", FRONT)
    write(tmp_path / "docs/decisions/0002-one-command.md", MADR)
    write(tmp_path / "docs/decisions/0003-newer.md", NEWER)
    return tmp_path


def test_decisions_are_read_from_the_lines_they_already_carry(repo):
    old, madr, newer = read(repo, {REQ, "ship"})
    assert old.id == "decision/0001-old" and old.status == "superseded" and old.superseded
    assert old.superseded_by == "docs/decisions/0003-newer.md"
    assert old.raw == ["scripts/ship.py", "RULE-SOMETHING"] and old.paths == ["scripts/ship.py"] and old.ids == []
    assert old.statement == "Ship the old way." and old.source_kind == "brian"
    assert madr.status == "accepted" and not madr.superseded and madr.ids == ["ship"] and madr.paths == []
    assert newer.paths == ["scripts/", "docs/notes.md"] and newer.source_kind == "inferred"
    order = governing([old, madr, newer], "scripts/ship.py", [REQ])
    assert [d.id for d in order] == ["decision/0001-old", "decision/0002-one-command", "decision/0003-newer"]
    assert [d.id for d in governing([old, madr, newer], "scripts/other.py", [])] == ["decision/0003-newer"]


@pytest.mark.req("lockstep-guard/an-edit-to-a-governed-file-gets-its-decisions")
def test_an_edit_to_a_governed_file_gets_its_decisions(repo):
    out = decide({"tool_name": "Edit", "tool_input": {"file_path": str(repo / "scripts/ship.py")},
                  "cwd": str(repo)})["hookSpecificOutput"]
    context = out["additionalContext"]
    assert "`ship` SHALL merge only a checked commit." in context  # the requirement text still comes first
    assert context.index("SHALL merge only") < context.index("Decisions that govern scripts/ship.py")
    assert "decision/0001-old: Old way to ship (superseded" in context
    assert "SUPERSEDED by docs/decisions/0003-newer.md" in context
    assert "Every merge goes through `ship`." in context and "Ship the newer way." in context
    _, rec = hook._PENDING[-1]  # main() writes queued records to the log
    assert rec["why"] == "openspec_text" and rec["requirements"] == [REQ]
    assert rec["decisions"] == ["decision/0001-old", "decision/0002-one-command", "decision/0003-newer"]
    only = decide({"tool_name": "Edit", "tool_input": {"file_path": str(repo / "scripts/other.py")}, "cwd": str(repo)})
    assert "Ship the newer way." in only["hookSpecificOutput"]["additionalContext"]  # governed, implements nothing
    shell = decide({"tool_name": "Bash", "tool_input": {"command": "sed -i 's/1/2/' scripts/other.py"}, "cwd": str(repo)})
    assert "Ship the newer way." in shell["hookSpecificOutput"]["additionalContext"]
    write(repo / "free.py", '"""Nothing."""\n')
    assert decide({"tool_name": "Edit", "tool_input": {"file_path": str(repo / "free.py")}, "cwd": str(repo)}) is None


def test_the_hook_text_names_at_most_three_decisions_in_full(repo):
    for n in range(4, 7):
        write(repo / f"docs/decisions/000{n}-more.md", f"# More {n}\n\n- Status: accepted\n- Governs: scripts/\n")
    ids, text = packet(repo, "scripts/ship.py", [REQ])
    assert len(ids) == 6 and text.count("\ndecision/") == 3
    assert "Also governed by: decision/0004-more, decision/0005-more, decision/0006-more." in text


def test_no_decisions_folder_means_no_decision_text(tmp_path):
    write(tmp_path / "openspec/specs/ship/spec.md", SPEC)
    assert packet(tmp_path, "scripts/ship.py", [REQ]) == ([], "")


@pytest.mark.req("lockstep-projection/the-link-file-lists-decisions-and-what-they-govern")
def test_the_link_file_lists_decisions_and_what_they_govern(repo):
    from lockstep.checks.project import project
    from lockstep.checks.status import LINKS_FILE

    write(repo / "docs/index.md", "# Docs\n")
    project(repo)
    nodes = {n["id"]: n for n in json.loads((repo / LINKS_FILE).read_text())["nodes"]}
    old = nodes["decision/0001-old"]
    assert old["type"] == "decision" and old["status"] == "superseded"
    assert old["superseded_by"] == "docs/decisions/0003-newer.md" and old["file"] == "docs/decisions/0001-old.md"
    assert old["links"] == ["scripts/ship.py"] and old["governs"] == ["scripts/ship.py", "RULE-SOMETHING"]
    assert old["source_kind"] == "brian"
    assert nodes["decision/0002-one-command"]["links"] == ["ship"]
    assert nodes["decision/0003-newer"]["links"] == ["scripts/", "docs/notes.md"]
    assert nodes["scripts/"]["type"] == "file" and nodes["docs/notes.md"]["type"] == "file"
    assert project(repo, check=True) == []
