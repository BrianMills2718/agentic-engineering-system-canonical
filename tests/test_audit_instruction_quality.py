"""Tests for the instruction-surface quality auditor.

Each case pins a detector against a failure that already occurred in practice:
markdown bullets read as directory trees, archived lineage variants drowning
live findings, and one non-UTF-8 file aborting an ecosystem-wide run.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_instruction_quality.py"
_MODULE_NAME = "audit_instruction_quality"


def _module():
    """Load the auditor without requiring a package import path.

    The module must be registered in ``sys.modules`` before execution: it uses
    dataclasses under ``from __future__ import annotations``, and resolving
    those annotations looks the defining module up by name.
    """

    if _MODULE_NAME in sys.modules:
        return sys.modules[_MODULE_NAME]
    spec = importlib.util.spec_from_file_location(_MODULE_NAME, _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def audit():
    return _module()


def _kinds(report) -> set[str]:
    return {finding.kind for finding in report.findings}


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_oversized_flags_only_files_past_the_guidance(audit, tmp_path: Path):
    """A long file is flagged; a short one is not."""

    (tmp_path / ".git").mkdir()
    (tmp_path / "CLAUDE.md").write_text("rule\n" * (audit.LINE_GUIDANCE + 5), encoding="utf-8")
    assert "oversized" in _kinds(audit.audit_repo(tmp_path))

    other = tmp_path / "small"
    (other / ".git").mkdir(parents=True)
    (other / "CLAUDE.md").write_text("short\n", encoding="utf-8")
    assert "oversized" not in _kinds(audit.audit_repo(other))


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_agents_only_repo_audits_root_and_nested_instructions(audit, tmp_path: Path):
    """An AGENTS-only repository must not disappear from the quality audit."""

    (tmp_path / ".git").mkdir()
    (tmp_path / "AGENTS.md").write_text("short\n", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "AGENTS.md").write_text(
        "rule\n" * (audit.LINE_GUIDANCE + 5), encoding="utf-8"
    )
    report = audit.audit_repo(tmp_path)
    assert report.files == 2
    assert any(
        finding.kind == "oversized" and finding.path == "nested/AGENTS.md"
        for finding in report.findings
    )


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_markdown_bullets_are_not_directory_trees(audit, tmp_path: Path):
    """A bulleted list is a list. Treating it as a tree produced 13 false findings."""

    (tmp_path / ".git").mkdir()
    bullets = "\n".join(f"- item number {index}" for index in range(30))
    (tmp_path / "CLAUDE.md").write_text(f"# Index\n\n{bullets}\n", encoding="utf-8")
    assert "derivable" not in _kinds(audit.audit_repo(tmp_path))


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_rendered_tree_is_flagged_as_derivable(audit, tmp_path: Path):
    """Box-drawing glyphs are a real tree an agent should read from disk."""

    (tmp_path / ".git").mkdir()
    tree = "\n".join("├── module_%d.py" % index for index in range(8))
    (tmp_path / "CLAUDE.md").write_text(f"# Layout\n\n```\n{tree}\n```\n", encoding="utf-8")
    assert "derivable" in _kinds(audit.audit_repo(tmp_path))


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_markdown_table_is_not_a_directory_tree(audit, tmp_path: Path):
    """`|-----|-----|` opens with a pipe and dashes; deleting it breaks the table."""

    (tmp_path / ".git").mkdir()
    rows = "\n".join(f"| `mod_{i}.py` | does thing {i} |" for i in range(10))
    (tmp_path / "CLAUDE.md").write_text(
        f"# Index\n\n| File | Purpose |\n|------|---------|\n{rows}\n", encoding="utf-8"
    )
    assert "derivable" not in _kinds(audit.audit_repo(tmp_path))


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_flow_diagram_is_not_a_directory_tree(audit, tmp_path: Path):
    """Box-drawing glyphs also draw pipelines, which no checkout can supply."""

    (tmp_path / ".git").mkdir()
    flow = "\n".join(f"├─ [Stage {i} LLM] → next stage" for i in range(10))
    (tmp_path / "CLAUDE.md").write_text(f"# Flow\n\n{flow}\n", encoding="utf-8")
    assert "derivable" not in _kinds(audit.audit_repo(tmp_path))


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_misplaced_block_is_attributed_to_the_owning_child(audit, tmp_path: Path):
    """A parent block referencing only one instruction-owning child belongs there."""

    (tmp_path / ".git").mkdir()
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "CLAUDE.md").write_text("# Scripts\n\nlocal rules\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text(
        "# Root\n\n## Script usage\n\nRun `scripts/one.py` then `scripts/two.py` in order.\n",
        encoding="utf-8",
    )
    findings = [f for f in audit.audit_repo(tmp_path).findings if f.kind == "misplaced"]
    assert findings, "expected the single-child block to be flagged"
    assert "scripts" in findings[0].detail


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_routing_pointer_is_not_misplaced_content(audit, tmp_path: Path):
    """Parents are supposed to route. One pointer is routing, not content."""

    (tmp_path / ".git").mkdir()
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "CLAUDE.md").write_text("# Scripts\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text(
        "# Root\n\nFor script details see `scripts/CLAUDE.md`.\n", encoding="utf-8"
    )
    assert "misplaced" not in _kinds(audit.audit_repo(tmp_path))


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_child_repeating_ancestor_lines_is_duplication(audit, tmp_path: Path):
    """The ancestor is always in context when the child is."""

    (tmp_path / ".git").mkdir()
    shared = "Always run the full verification suite before pushing any change.\n"
    (tmp_path / "CLAUDE.md").write_text(f"# Root\n\n{shared}", encoding="utf-8")
    child = tmp_path / "child"
    child.mkdir()
    (child / "CLAUDE.md").write_text(f"# Child\n\n{shared}", encoding="utf-8")
    assert "duplicated" in _kinds(audit.audit_repo(tmp_path))


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_archived_trees_are_excluded(audit, tmp_path: Path):
    """Retired lineage variants once supplied 138 of one repo's 150 findings."""

    (tmp_path / ".git").mkdir()
    for name in ("archive", "archive_full_record", "legacy", "deprecated_runs"):
        retired = tmp_path / name / "nested"
        retired.mkdir(parents=True)
        (retired / "CLAUDE.md").write_text("rule\n" * (audit.LINE_GUIDANCE + 5), encoding="utf-8")
    report = audit.audit_repo(tmp_path)
    assert report.files == 0
    assert report.findings == []


@pytest.mark.req("instruction-audit/quality-findings-are-advisory", existing=True)  # ported unchanged from Project Meta
def test_non_utf8_file_is_skipped_not_fatal(audit, tmp_path: Path, capsys):
    """One bad file must not abort an audit spanning 77 repositories."""

    (tmp_path / ".git").mkdir()
    (tmp_path / "CLAUDE.md").write_bytes(b"# Rules\n\xff\xfe bad bytes\n")
    good = tmp_path / "good"
    good.mkdir()
    (good / "CLAUDE.md").write_text("fine\n", encoding="utf-8")

    report = audit.audit_repo(tmp_path)
    assert report.files == 2
    assert "skipping" in capsys.readouterr().err
