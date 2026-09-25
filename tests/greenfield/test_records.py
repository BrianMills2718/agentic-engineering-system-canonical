"""Probe 0: strict target/project loading against the real whygame5 records.

The fixture copies the authentic consumer's `.aes/project.yaml` and
`.aes/target.yaml` into a temp directory; broken variants are made by editing
that real text, so every negative case is a plausible hand-edit of a real file.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from agentic_engineering_system.records import (
    RecordLoadError,
    TargetValidationError,
    load_project,
    load_target,
)

WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"


@pytest.fixture
def aes_dir(tmp_path: Path) -> Path:
    if not (WHYGAME5_AES / "target.yaml").is_file():
        pytest.fail(f"authentic consumer target missing: {WHYGAME5_AES / 'target.yaml'}")
    dest = tmp_path / ".aes"
    dest.mkdir()
    shutil.copy(WHYGAME5_AES / "project.yaml", dest / "project.yaml")
    shutil.copy(WHYGAME5_AES / "target.yaml", dest / "target.yaml")
    return dest


def _rewrite(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"expected exactly one occurrence of {old!r} in {path}"
    path.write_text(text.replace(old, new), encoding="utf-8")


# --------------------------------------------------------------------------- #
# Happy path on the real consumer
# --------------------------------------------------------------------------- #


def test_real_whygame5_target_loads(aes_dir: Path) -> None:
    target = load_target(aes_dir / "target.yaml")
    assert target.target_id == "whygame5-target"
    assert [o.id for o in target.outcomes] == ["OUT-WG5-001"]
    assert [n.id for n in target.normative_items] == [f"NI-WG5-00{i}" for i in range(1, 8)]
    assert [s.id for s in target.success_criteria] == [f"SC-WG5-00{i}" for i in range(1, 6)]
    assert set(target.evidence_requirements()) == {
        "ER-WG5-001-01", "ER-WG5-001-02", "ER-WG5-001-03", "ER-WG5-002-01",
        "ER-WG5-003-01", "ER-WG5-004-01", "ER-WG5-005-01",
    }
    assert [c.id for c in target.components] == [
        "CMP-WG5-CONTRACTS", "CMP-WG5-GRAPH", "CMP-WG5-EVALUATOR",
        "CMP-WG5-PROMPTS", "CMP-WG5-RUNNER", "CMP-WG5-REPORT",
    ]
    evaluator_art = next(a for a in target.planned_artifacts if a.id == "ART-WG5-EVALUATOR")
    assert evaluator_art.locator.exact_path == "src/whygame5/evaluator.py"
    assert len(target.verification_subjects) == 7
    # folded scalars come back as plain, whitespace-stripped str
    ni2 = next(n for n in target.normative_items if n.id == "NI-WG5-002")
    assert type(ni2.statement) is str
    assert ni2.statement.startswith("The evaluator selects findings from graph structure alone")


def test_real_whygame5_project_loads(aes_dir: Path) -> None:
    project = load_project(aes_dir / "project.yaml")
    assert project.project_id == "whygame5"
    assert project.governed_roots == ["src/", "tests/"]
    assert project.materialization.target_path == ".aes/target.yaml"
    assert project.aes.architecture_line == "AES-v0.2"


# --------------------------------------------------------------------------- #
# Deliberately broken variants
# --------------------------------------------------------------------------- #


def test_duplicate_mapping_key_is_rejected(aes_dir: Path) -> None:
    path = aes_dir / "target.yaml"
    _rewrite(path, "target_id: whygame5-target\n", "target_id: whygame5-target\ntarget_id: again\n")
    with pytest.raises(RecordLoadError) as excinfo:
        load_target(path)
    msg = str(excinfo.value)
    assert "duplicate" in msg.lower()
    assert "target_id" in msg
    assert str(path) in msg


def test_unresolved_ref_names_the_ref_and_location(aes_dir: Path) -> None:
    path = aes_dir / "target.yaml"
    # CMP-WG5-REPORT is the only component whose target_refs is exactly [NI-WG5-007]
    _rewrite(path, "target_refs: [NI-WG5-007]\n    planned_artifact_refs: [ART-WG5-REPORT]",
             "target_refs: [NI-WG5-999]\n    planned_artifact_refs: [ART-WG5-REPORT]")
    with pytest.raises(TargetValidationError) as excinfo:
        load_target(path)
    err = excinfo.value
    assert len(err.violations) == 1
    assert "NI-WG5-999" in err.violations[0]
    assert "components[5] (CMP-WG5-REPORT).target_refs[0]" in err.violations[0]


def test_criterion_without_evidence_requirement_is_rejected(aes_dir: Path) -> None:
    path = aes_dir / "target.yaml"
    block = (
        "    evidence_requirements:\n"
        "      - id: ER-WG5-005-01\n"
        "        kind: human_review\n"
        "        requirement: >\n"
        "          Brian answers the four questions from report.html alone and records\n"
        "          whether he could.\n"
    )
    _rewrite(path, block, "    evidence_requirements: []\n")
    with pytest.raises(TargetValidationError) as excinfo:
        load_target(path)
    violations = excinfo.value.violations
    assert any(
        "criterion 'SC-WG5-005' at success_criteria[4] (SC-WG5-005) has no evidence_requirements" == v
        for v in violations
    ), violations
    # the verification subject that pointed at the removed ER is now dangling too
    assert any("ER-WG5-005-01" in v and "VS-WG5-BRIAN-REPORT" in v for v in violations), violations


def test_duplicate_id_across_families_is_rejected(aes_dir: Path) -> None:
    path = aes_dir / "target.yaml"
    _rewrite(path, "  - id: VS-WG5-REPLAY\n", "  - id: NI-WG5-004\n")
    with pytest.raises(TargetValidationError) as excinfo:
        load_target(path)
    assert any(
        "duplicate id 'NI-WG5-004' at verification_subjects[5] (first declared at normative_items[3])" == v
        for v in excinfo.value.violations
    ), excinfo.value.violations


def test_normative_item_must_reach_an_outcome(aes_dir: Path) -> None:
    path = aes_dir / "target.yaml"
    _rewrite(path, "  - id: NI-WG5-006\n    kind: constraint\n    outcome_refs: [OUT-WG5-001]\n",
             "  - id: NI-WG5-006\n    kind: constraint\n    outcome_refs: []\n")
    with pytest.raises(TargetValidationError) as excinfo:
        load_target(path)
    assert any("normative item 'NI-WG5-006'" in v and "reaches no declared outcome" in v
               for v in excinfo.value.violations), excinfo.value.violations


def test_unknown_field_is_rejected(aes_dir: Path) -> None:
    path = aes_dir / "target.yaml"
    _rewrite(path, "target_id: whygame5-target\n", "target_id: whygame5-target\nowner: brian\n")
    with pytest.raises(RecordLoadError) as excinfo:
        load_target(path)
    assert "owner" in str(excinfo.value)
    assert "extra" in str(excinfo.value).lower()


def test_missing_file_is_loud(tmp_path: Path) -> None:
    with pytest.raises(RecordLoadError) as excinfo:
        load_target(tmp_path / "nope.yaml")
    assert "does not exist" in str(excinfo.value)
