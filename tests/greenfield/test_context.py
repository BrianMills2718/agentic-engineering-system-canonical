"""Probe 0: `aes context <subject>` on the real whygame5 target.

Asserts full applicable text (never IDs alone), provenance, boundedness (the
report item NI-WG5-007 is absent from the evaluator packet) and explicit
omission (the not-included list names what was left out).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.context import (
    ContextError,
    project_context,
    render_json,
    render_markdown,
)
from agentic_engineering_system.records import RecordLoadError, TargetValidationError, load_target

WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"

NI_002_TEXT = (
    "The evaluator selects findings from graph structure alone: two committed "
    "claims with the same normalized subject and object and opposed causal "
    "polarity, or a committed claim opposed to a source observation. Committed "
    "claims include those persisted by earlier runs on the same graph."
)
NI_003_TEXT = (
    "When the evaluator finds no conflict it reports NO_FINDING explicitly and "
    "the run ends without a revision call. It never manufactures a finding."
)
SC_003_DISPROOF = (
    "The evaluator returns a finding for an all-consistent proposal, or the "
    "runner calls the model a second time without a finding."
)
NI_007_TEXT = (
    "A static report lets a reader see what was proposed, what challenged it, "
    "what changed, and which claims remain active, without reading logs or "
    "source code."
)


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
        cwd=root, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """A git-initialised project root holding the real whygame5 .aes records."""
    if not (WHYGAME5_AES / "target.yaml").is_file():
        pytest.fail(f"authentic consumer target missing: {WHYGAME5_AES / 'target.yaml'}")
    dest = tmp_path / ".aes"
    dest.mkdir()
    shutil.copyfile(WHYGAME5_AES / "project.yaml", dest / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", dest / "target.yaml")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", ".aes")
    _git(tmp_path, "commit", "-q", "-m", "probe fixture")
    return tmp_path


def _rewrite(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"expected exactly one occurrence of {old!r} in {path}"
    path.write_text(text.replace(old, new), encoding="utf-8")


# --------------------------------------------------------------------------- #
# The evaluator packet
# --------------------------------------------------------------------------- #


def test_evaluator_packet_has_full_text_and_paths(project_root: Path) -> None:
    ctx = project_context(project_root, "CMP-WG5-EVALUATOR")
    md = render_markdown(ctx)

    assert ctx.subject_family == "components"
    assert ctx.subject["id"] == "CMP-WG5-EVALUATOR"

    # full normative text, not IDs alone
    assert NI_002_TEXT in md
    assert NI_003_TEXT in md
    assert SC_003_DISPROOF in md

    # exact planned paths
    assert "src/whygame5/evaluator.py" in md
    assert "tests/test_evaluator.py" in md
    assert {a.locator.exact_path for a in ctx.planned_artifacts} == {
        "src/whygame5/evaluator.py", "tests/test_evaluator.py",
    }

    # boundedness: the report item is NOT in the packet, but its omission is visible
    assert NI_007_TEXT not in md
    assert "NI-WG5-007" not in {n.id for n in ctx.normative_items}
    assert "NI-WG5-007" in ctx.not_included["normative_items"]
    assert "CMP-WG5-REPORT" in ctx.not_included["components"]
    assert "ART-WG5-REPORT" in ctx.not_included["planned_artifacts"]
    assert "SC-WG5-005" in ctx.not_included["success_criteria"]


def test_evaluator_packet_membership(project_root: Path) -> None:
    ctx = project_context(project_root, "CMP-WG5-EVALUATOR")
    assert [n.id for n in ctx.normative_items] == ["NI-WG5-002", "NI-WG5-003"]
    # SC-001 targets NI-002 (evaluator finding under clean prompts); SC-002/003 justify the test
    assert [s.id for s in ctx.success_criteria] == ["SC-WG5-001", "SC-WG5-002", "SC-WG5-003"]
    assert [o.id for o in ctx.outcomes] == ["OUT-WG5-001"]
    assert [c.id for c in ctx.components] == ["CMP-WG5-EVALUATOR"]
    assert {v.id for v in ctx.verification_subjects} == {
        "VS-WG5-PROMPTS", "VS-WG5-LIVE-RUN", "VS-WG5-BRIAN-FINDING",
        "VS-WG5-EVAL-CROSS-RUN", "VS-WG5-EVAL-NEGATIVE",
    }
    negative = next(v for v in ctx.verification_subjects if v.id == "VS-WG5-EVAL-NEGATIVE")
    assert negative.locator == "tests/test_evaluator.py"
    assert negative.proof_role == "negative_control"
    # every evidence requirement of every included criterion carries its text
    sc3 = next(s for s in ctx.success_criteria if s.id == "SC-WG5-003")
    assert sc3.evidence_requirements[0].requirement.startswith("Negative control:")
    # governed roots + rule
    assert ctx.governed_roots == ["src/", "tests/"]
    assert "topology violation" in ctx.topology_rule


def test_provenance_is_exact(project_root: Path) -> None:
    ctx = project_context(project_root, "CMP-WG5-EVALUATOR")
    import hashlib
    target_path = project_root / ".aes" / "target.yaml"
    assert ctx.provenance.target_path == str(target_path.resolve())
    assert ctx.provenance.target_sha256 == hashlib.sha256(target_path.read_bytes()).hexdigest()
    assert ctx.provenance.git_head == _git(project_root, "rev-parse", "HEAD")
    assert len(ctx.provenance.git_head) == 40


def test_json_form_round_trips(project_root: Path) -> None:
    ctx = project_context(project_root, "CMP-WG5-EVALUATOR")
    data = json.loads(render_json(ctx))
    assert data["subject_id"] == "CMP-WG5-EVALUATOR"
    assert [n["id"] for n in data["normative_items"]] == ["NI-WG5-002", "NI-WG5-003"]
    assert data["not_included"]["normative_items"] == [
        "NI-WG5-001", "NI-WG5-004", "NI-WG5-005", "NI-WG5-006", "NI-WG5-007",
    ]
    assert data["provenance"]["git_head"] == ctx.provenance.git_head


# --------------------------------------------------------------------------- #
# Other subject kinds
# --------------------------------------------------------------------------- #


def test_artifact_subject(project_root: Path) -> None:
    ctx = project_context(project_root, "ART-WG5-TEST-EVALUATOR")
    assert ctx.subject_family == "planned_artifacts"
    assert [c.id for c in ctx.components] == ["CMP-WG5-EVALUATOR"]
    assert [s.id for s in ctx.success_criteria] == ["SC-WG5-002", "SC-WG5-003"]
    assert {v.id for v in ctx.verification_subjects} == {"VS-WG5-EVAL-CROSS-RUN", "VS-WG5-EVAL-NEGATIVE"}
    assert NI_007_TEXT not in render_markdown(ctx)


def test_criterion_subject(project_root: Path) -> None:
    ctx = project_context(project_root, "SC-WG5-003")
    assert [n.id for n in ctx.normative_items] == ["NI-WG5-003"]
    assert [a.id for a in ctx.planned_artifacts] == ["ART-WG5-TEST-EVALUATOR"]
    assert [v.id for v in ctx.verification_subjects] == ["VS-WG5-EVAL-NEGATIVE"]
    assert NI_003_TEXT in render_markdown(ctx)


def test_normative_item_subject(project_root: Path) -> None:
    ctx = project_context(project_root, "NI-WG5-007")
    assert [s.id for s in ctx.success_criteria] == ["SC-WG5-005"]
    assert [c.id for c in ctx.components] == ["CMP-WG5-REPORT"]
    assert [a.id for a in ctx.planned_artifacts] == ["ART-WG5-REPORT"]
    assert NI_007_TEXT in render_markdown(ctx)
    assert NI_002_TEXT not in render_markdown(ctx)


def test_outcome_subject_includes_every_item(project_root: Path) -> None:
    ctx = project_context(project_root, "OUT-WG5-001")
    assert len(ctx.normative_items) == 7
    assert "normative_items" not in ctx.not_included


# --------------------------------------------------------------------------- #
# Failure modes are loud
# --------------------------------------------------------------------------- #


def test_unknown_subject_is_loud(project_root: Path) -> None:
    with pytest.raises(ContextError, match="'CMP-WG5-NOPE' is not a declared ID"):
        project_context(project_root, "CMP-WG5-NOPE")


def test_evidence_requirement_is_not_a_context_subject(project_root: Path) -> None:
    with pytest.raises(ContextError, match="evidence_requirements record"):
        project_context(project_root, "ER-WG5-003-01")


def test_context_refuses_invalid_target(project_root: Path) -> None:
    path = project_root / ".aes" / "target.yaml"
    _rewrite(path, "target_refs: [NI-WG5-007]\n    planned_artifact_refs: [ART-WG5-REPORT]",
             "target_refs: [NI-WG5-999]\n    planned_artifact_refs: [ART-WG5-REPORT]")
    with pytest.raises(TargetValidationError):
        project_context(project_root, "CMP-WG5-EVALUATOR")


def test_context_requires_git_head(tmp_path: Path) -> None:
    dest = tmp_path / ".aes"
    dest.mkdir()
    shutil.copyfile(WHYGAME5_AES / "project.yaml", dest / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", dest / "target.yaml")
    with pytest.raises(ContextError, match="git rev-parse HEAD"):
        project_context(tmp_path, "CMP-WG5-EVALUATOR")


# --------------------------------------------------------------------------- #
# CLI surface
# --------------------------------------------------------------------------- #


def test_cli_target_validate(project_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["target", "validate", "--root", str(project_root)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("OK ")
    assert "success_criteria=5 evidence_requirements=7" in out


def test_cli_context_markdown_and_json(project_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["context", "CMP-WG5-EVALUATOR", "--root", str(project_root)]) == 0
    md = capsys.readouterr().out
    assert md.startswith("# Working context: CMP-WG5-EVALUATOR (components)")
    assert NI_002_TEXT in md and NI_007_TEXT not in md

    assert main(["context", "CMP-WG5-EVALUATOR", "--root", str(project_root), "--format", "json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["subject_family"] == "components"


def test_cli_reports_errors_on_stderr(project_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = project_root / ".aes" / "target.yaml"
    _rewrite(path, "target_id: whygame5-target\n", "target_id: whygame5-target\ntarget_id: again\n")
    assert main(["target", "validate", "--root", str(project_root)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "duplicate" in captured.err.lower()
    with pytest.raises(RecordLoadError):
        load_target(path)
