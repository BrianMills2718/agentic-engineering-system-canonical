"""`aes plan prepare / validate / accept` (RU-AES-PLANNING, SC-GF-004 ER-01).

The repository under test is a temp Git repo holding the frozen whygame5
records plus stand-in files for every planned artifact except RUNNER, REPORT
and CLI (as in test_reconcile.py). The proposal under test is the one accepted
on a clone of the live consumer (fixtures/whygame5-proposal-runner.yaml).
Each rejection test mutates that proposal in exactly one way and asserts the
one violation it causes.
"""

from __future__ import annotations

import copy
import difflib
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest
from ruamel.yaml import YAML

from agentic_engineering_system.cli import main
from agentic_engineering_system.planning import (
    PlanError,
    Proposal,
    accept_proposal,
    load_plan,
    load_proposal,
    prepare,
    render_yaml,
    validate_proposal,
)
from agentic_engineering_system.project import initialize_project
from agentic_engineering_system.reconcile import reconcile
from agentic_engineering_system.records import load_target

FIXTURES = Path(__file__).parent / "fixtures"
WHYGAME5_AES = FIXTURES / "whygame5-54043e2" / ".aes"
RUNNER_PROPOSAL = FIXTURES / "whygame5-proposal-runner.yaml"
COMMENT = "# planning must keep this comment\n"

FILES = {
    "src/whygame5/__init__.py": '"""pkg"""\n',
    "src/whygame5/contracts.py": "class Proposal:\n    pass\n",
    "src/whygame5/graph.py": "def normalize(s):\n    return s\n",
    "src/whygame5/evaluator.py": "def select(findings):\n    return findings[:1]\n",
    "src/whygame5/prompts.py": "PROMPT = 'why?'\n",
    "tests/test_prompts.py": "def test_ok():\n    assert True\n",
    "tests/test_evaluator.py": "def test_ok():\n    assert True\n",
    "tests/test_replay.py": "def test_ok():\n    assert True\n",
    "pyproject.toml": "[project]\nname = 'whygame5'\n",
}


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
        cwd=root, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def root(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / ".aes").mkdir(parents=True)
    shutil.copy(WHYGAME5_AES / "project.yaml", repo / ".aes" / "project.yaml")
    target = (WHYGAME5_AES / "target.yaml").read_text(encoding="utf-8")
    (repo / ".aes" / "target.yaml").write_text(target.replace("\ncomponents:\n", f"\n{COMMENT}components:\n"))
    for rel, text in FILES.items():
        _write(repo, rel, text)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    return repo


def _proposal_data() -> dict[str, Any]:
    return YAML(typ="safe").load(RUNNER_PROPOSAL.read_text(encoding="utf-8"))


def _violations(root: Path, data: dict[str, Any]) -> list[str]:
    with pytest.raises(PlanError) as exc:
        validate_proposal(root, Proposal.model_validate(data))
    return exc.value.violations


def _snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


# --------------------------------------------------------------------------- #
# module identity
# --------------------------------------------------------------------------- #


def test_planning_is_the_module_and_the_v01_placeholder_directory_is_gone() -> None:
    import agentic_engineering_system.planning as planning

    assert planning.__file__ is not None and planning.__file__.endswith("planning.py")
    assert planning.accept_proposal is accept_proposal
    # archived to archive/v0.1-placeholders/planning/ in phase 7a; nothing shadows the module now
    assert not (Path(planning.__file__).parent / "planning").exists()


# --------------------------------------------------------------------------- #
# prepare
# --------------------------------------------------------------------------- #


def test_prepare_lists_open_gaps_ids_and_skeleton_deterministically(root: Path) -> None:
    first, second = prepare(root), prepare(root)
    assert first == second and render_yaml(first) == render_yaml(second)
    assert first["subject_revision"] == _git(root, "rev-parse", "HEAD")
    assert first["dirty"] is False
    assert {g["id"] for g in first["open_gaps"]} == {
        "unrealized:ART-WG5-RUNNER", "unrealized:ART-WG5-CLI", "unrealized:ART-WG5-REPORT",
        "insufficient:SC-WG5-001", "insufficient:SC-WG5-002", "insufficient:SC-WG5-003",
        "insufficient:SC-WG5-004", "insufficient:SC-WG5-005",
    }
    ids = first["target_ids"]
    assert "ER-WG5-001-02" in ids["evidence_requirements"] and "CMP-WG5-RUNNER" in ids["components"]
    assert ids["external_boundaries"] == [] and first["unrouted_evidence_requirements"] == []
    skeleton = first["proposal_skeleton"]
    assert skeleton["schema_version"] == "aes.v0_2.proposal.probe0"
    assert set(skeleton["target_delta"]["add"]) == set(skeleton["target_delta"]["change"])


def test_cli_prepare_writes_the_packet_and_leaves_the_repository_alone(root: Path, tmp_path: Path) -> None:
    before = _snapshot(root)
    out = tmp_path / "packet.yaml"
    assert main(["plan", "prepare", "--root", str(root), "--out", str(out)]) == 0
    assert "unrealized:ART-WG5-RUNNER" in out.read_text()
    assert _snapshot(root) == before


# --------------------------------------------------------------------------- #
# validate
# --------------------------------------------------------------------------- #


def test_validate_accepts_the_consumer_proposal(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    v = validate_proposal(root, load_proposal(RUNNER_PROPOSAL))
    assert "VS-WG5-RUNNER-FAIL-STOP" in {s.id for s in v.target.verification_subjects}
    assert [c.planned_artifact_refs for c in v.target.components if c.id == "CMP-WG5-RUNNER"] == [
        ["ART-WG5-RUNNER", "ART-WG5-CLI", "ART-WG5-TEST-RUNNER"]]
    assert main(["plan", "validate", str(RUNNER_PROPOSAL), "--root", str(root)]) == 0
    assert "OK proposal PLAN-WG5-RUNNER" in capsys.readouterr().out


def test_rejects_criterion_without_evidence_requirement(root: Path) -> None:
    data = _proposal_data()
    sc = copy.deepcopy(data["target_delta"]["add"]["success_criteria"][0])
    sc.update(id="SC-WG5-008", evidence_requirements=[])
    data["target_delta"]["add"]["success_criteria"].append(sc)
    [v] = _violations(root, data)
    assert "criterion 'SC-WG5-008'" in v and "has no evidence_requirements" in v


def test_rejects_evidence_requirement_without_route_or_boundary(root: Path) -> None:
    data = _proposal_data()
    del data["target_delta"]["add"]["verification_subjects"]
    [v] = _violations(root, data)
    assert "'ER-WG5-007-01'" in v and "has no route" in v


def test_external_boundary_is_a_route(root: Path) -> None:
    data = _proposal_data()
    del data["target_delta"]["add"]["verification_subjects"]
    data["target_delta"]["add"]["external_boundaries"] = [
        {"evidence_requirement_ref": "ER-WG5-007-01", "boundary": "a reviewer runs the stubbed run by hand"}]
    v = validate_proposal(root, Proposal.model_validate(data))
    assert [b.evidence_requirement_ref for b in v.target.external_boundaries] == ["ER-WG5-007-01"]


def test_rejects_closing_a_gap_that_is_not_open(root: Path) -> None:
    data = _proposal_data()
    data["closes_gaps"].append("unrealized:ART-WG5-GRAPH")  # graph.py exists at HEAD
    [v] = _violations(root, data)
    assert "'unrealized:ART-WG5-GRAPH' is not an open gap" in v


def test_rejects_unresolved_ref_in_delta(root: Path) -> None:
    data = _proposal_data()
    data["target_delta"]["add"]["planned_artifacts"][0]["semantic_justification_refs"] = ["NI-WG5-999"]
    [v] = _violations(root, data)
    assert v.startswith("resulting target: unresolved ref 'NI-WG5-999'")


def test_rejects_add_of_an_id_the_target_already_declares(root: Path) -> None:
    data = _proposal_data()
    data["target_delta"]["add"]["planned_artifacts"][0]["id"] = "ART-WG5-RUNNER"
    data["target_delta"]["add"]["success_criteria"][0]["id"] = "OUT-WG5-001"  # another family's id
    data["target_delta"]["add"]["verification_subjects"][0]["criterion_refs"] = ["OUT-WG5-001"]
    violations = _violations(root, data)
    assert any("already declares planned_artifacts 'ART-WG5-RUNNER'" in v for v in violations)
    assert any("duplicate id 'OUT-WG5-001'" in v for v in violations)


def test_rejects_change_of_an_id_the_target_does_not_declare(root: Path) -> None:
    data = _proposal_data()
    data["target_delta"]["change"]["components"][0]["id"] = "CMP-WG5-NOPE"
    violations = _violations(root, data)
    assert any("declares no components entry 'CMP-WG5-NOPE'" in v for v in violations)


def test_rejects_source_outside_governed_roots_and_needs_a_reason_for_other_kinds(root: Path) -> None:
    data = _proposal_data()
    art = data["target_delta"]["add"]["planned_artifacts"][0]
    art["locator"]["exact_path"] = "scripts/run.py"
    art["kind"] = "source"
    [v] = _violations(root, data)
    assert "source artifact scripts/run.py is outside the governed roots" in v

    art["kind"] = "configuration"
    [v] = _violations(root, data)
    assert "outside_governed_roots gives no reason" in v

    data["outside_governed_roots"] = [{"artifact_ref": "ART-WG5-TEST-RUNNER", "reason": "a runner config"}]
    validate_proposal(root, Proposal.model_validate(data))


def test_validate_reports_every_violation_not_the_first(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    data = _proposal_data()
    del data["target_delta"]["add"]["verification_subjects"]
    data["closes_gaps"].append("insufficient:SC-WG5-999")
    assert len(_violations(root, data)) == 2
    bad = root.parent / "bad.yaml"
    bad.write_text(render_yaml(data))
    assert main(["plan", "validate", str(bad), "--root", str(root)]) == 1
    assert "2 violation(s)" in capsys.readouterr().err


# --------------------------------------------------------------------------- #
# accept
# --------------------------------------------------------------------------- #


def test_accept_applies_delta_preserves_target_text_and_writes_plan(root: Path) -> None:
    head = _git(root, "rev-parse", "HEAD")
    before_target = (root / ".aes" / "target.yaml").read_text()
    proposal = root / "proposal.yaml"  # untracked outside .aes/: not dirty
    shutil.copy(RUNNER_PROPOSAL, proposal)
    before = set(_snapshot(root))

    assert main(["plan", "accept", str(proposal), "--root", str(root)]) == 0

    after_target = (root / ".aes" / "target.yaml").read_text()
    assert COMMENT in after_target
    removed = [line for line in difflib.ndiff(before_target.splitlines(), after_target.splitlines())
               if line.startswith("- ")]
    assert removed == ["-     planned_artifact_refs: [ART-WG5-RUNNER, ART-WG5-CLI]"]  # the changed entry only
    target = load_target(root / ".aes" / "target.yaml")
    assert target.success_criteria[-1].id == "SC-WG5-007"
    assert target.verification_subjects[-1].id == "VS-WG5-RUNNER-FAIL-STOP"
    assert [c.id for c in target.components].index("CMP-WG5-RUNNER") == 4  # replaced in place

    plan = load_plan(root / ".aes" / "plans" / "PLAN-WG5-RUNNER.yaml")
    assert plan.accepted_at_revision == head and plan.accepted_at.tzinfo is not None
    assert plan.closes_gaps == ["unrealized:ART-WG5-RUNNER", "unrealized:ART-WG5-CLI"]
    assert set(_snapshot(root)) - before == {".aes/plans/PLAN-WG5-RUNNER.yaml"}
    assert _git(root, "rev-parse", "HEAD") == head  # no commit

    _git(root, "add", ".aes")
    _git(root, "commit", "-q", "-m", "accept")
    gaps = {g.id for g in reconcile(root).open_gaps()}
    # acceptance closes nothing: the claimed gaps stay open, the new artifact is a new gap
    assert {"unrealized:ART-WG5-RUNNER", "unrealized:ART-WG5-TEST-RUNNER", "insufficient:SC-WG5-007"} <= gaps


def test_accept_refuses_dirty_tree_and_writes_nothing(root: Path) -> None:
    _write(root, "src/whygame5/graph.py", "def normalize(s):\n    return s.lower()\n")
    before = _snapshot(root)
    with pytest.raises(PlanError, match="working tree is dirty"):
        accept_proposal(root, RUNNER_PROPOSAL)
    assert _snapshot(root) == before

    _git(root, "checkout", "--", "src/whygame5/graph.py")
    _write(root, ".aes/observations/OBS-UNRECORDED.yaml", "x: 1\n")
    before = _snapshot(root)
    with pytest.raises(PlanError, match="working tree is dirty"):
        accept_proposal(root, RUNNER_PROPOSAL)
    assert _snapshot(root) == before


def test_accept_refuses_failing_validation_and_writes_nothing(root: Path) -> None:
    data = _proposal_data()
    del data["target_delta"]["add"]["verification_subjects"]
    bad = root.parent / "bad.yaml"
    bad.write_text(render_yaml(data))
    before = _snapshot(root)
    assert main(["plan", "accept", str(bad), "--root", str(root)]) == 1
    assert _snapshot(root) == before


def test_accept_refuses_a_plan_id_already_accepted(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    accept_proposal(root, RUNNER_PROPOSAL)
    _git(root, "add", ".aes")
    _git(root, "commit", "-q", "-m", "accept")
    before = _snapshot(root)
    assert main(["plan", "accept", str(RUNNER_PROPOSAL), "--root", str(root)]) == 1
    assert "already exists; a plan id is accepted once" in capsys.readouterr().err
    assert _snapshot(root) == before


def test_accept_on_a_freshly_initialized_target(tmp_path: Path) -> None:
    """The getting-started path: `aes init` writes `[]` families; accepted entries become block lists."""
    _git(tmp_path, "init", "-q")
    initialize_project(tmp_path, project_id="greeter", outcome="greet returns a greeting",
                       actor="a script author")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "init")
    assert prepare(tmp_path)["open_gaps"] == []
    proposal = tmp_path.parent / "first.yaml"
    proposal.write_text("""schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-001
title: first chain
rationale: plan the greeter before writing it
closes_gaps: []
target_delta:
  add:
    normative_items:
      - {id: NI-001, kind: behavior, outcome_refs: [OUT-001], statement: "greet(name) returns Hello, name"}
    success_criteria:
      - id: SC-001
        statement: greet greets
        target_refs: [NI-001]
        disproof: the name is missing
        evidence_requirements:
          - {id: ER-001-01, kind: deterministic_test, requirement: a test checks greet("Ada")}
    planned_artifacts:
      - {id: ART-PKG, locator: {exact_path: src/greeter/__init__.py}, kind: source, purpose: greet,
         semantic_justification_refs: [NI-001]}
    verification_subjects:
      - {id: VS-GREET, criterion_refs: [SC-001], evidence_requirement_refs: [ER-001-01],
         proof_kind: deterministic_test, proof_role: direct, locator: tests/test_greet.py, purpose: prove it}
""")
    accept_proposal(tmp_path, proposal)
    text = (tmp_path / ".aes" / "target.yaml").read_text()
    assert "normative_items:\n- {id: NI-001" in text  # block list, entry in the style it was written
    target = load_target(tmp_path / ".aes" / "target.yaml")
    assert [s.id for s in target.success_criteria] == ["SC-001"]


def test_protocol_example_is_the_accepted_consumer_proposal() -> None:
    protocol = Path(__file__).parents[2] / "src" / "agentic_engineering_system" / "planning_protocol.md"
    example = protocol.read_text(encoding="utf-8").split("```yaml\n", 1)[1].split("```", 1)[0]
    assert YAML(typ="safe").load(example) == _proposal_data()


# --------------------------------------------------------------------------- #
# remove
# --------------------------------------------------------------------------- #


def _removal(remove: dict[str, list[str]], change: dict[str, list[dict[str, Any]]] | None = None) -> dict[str, Any]:
    return {
        "schema_version": "aes.v0_2.proposal.probe0", "proposal_id": "PLAN-REMOVE", "title": "remove",
        "rationale": "drop entries the target no longer plans", "closes_gaps": [],
        "target_delta": {"remove": remove, "change": change or {}},
    }


REPORT_COMPONENT = {  # CMP-WG5-REPORT without ART-WG5-REPORT
    "id": "CMP-WG5-REPORT", "responsibility": "static HTML report", "target_refs": ["NI-WG5-007"],
    "planned_artifact_refs": [],
}


def test_remove_rejects_a_key_the_target_does_not_declare_and_a_key_in_two_sections(root: Path) -> None:
    data = _removal({"planned_artifacts": ["ART-WG5-NOPE"], "components": ["CMP-WG5-REPORT"]},
                    {"components": [REPORT_COMPONENT]})
    violations = _violations(root, data)
    assert ("target_delta.remove.planned_artifacts (ART-WG5-NOPE): the target declares no planned_artifacts "
            "entry 'ART-WG5-NOPE' to remove") in violations
    assert any("'CMP-WG5-REPORT' is also under target_delta.remove.components" in v for v in violations)


def test_remove_reports_every_dangling_reference_once(root: Path) -> None:
    # SC-WG5-003 is named by VS-WG5-EVAL-NEGATIVE (criterion and its ER) and by
    # ART-WG5-TEST-EVALUATOR; ART-WG5-REPORT by CMP-WG5-REPORT.
    violations = _violations(root, _removal({"success_criteria": ["SC-WG5-003"],
                                             "planned_artifacts": ["ART-WG5-REPORT"]}))
    at = "is still referenced by the resulting target at"
    assert sorted(violations) == sorted([
        f"target_delta.remove.success_criteria (SC-WG5-003): removed 'SC-WG5-003' {at} "
        "planned_artifacts[8] (ART-WG5-TEST-EVALUATOR).semantic_justification_refs[1]",
        f"target_delta.remove.success_criteria (SC-WG5-003): removed 'SC-WG5-003' {at} "
        "verification_subjects[4] (VS-WG5-EVAL-NEGATIVE).criterion_refs[0]",
        f"evidence requirement of removed criterion 'SC-WG5-003': removed 'ER-WG5-003-01' {at} "
        "verification_subjects[4] (VS-WG5-EVAL-NEGATIVE).evidence_requirement_refs[0]",
        f"target_delta.remove.planned_artifacts (ART-WG5-REPORT): removed 'ART-WG5-REPORT' {at} "
        "components[5] (CMP-WG5-REPORT).planned_artifact_refs[0]",
    ])  # no second "unresolved ref" line for the same references


def test_remove_rejects_a_planned_artifact_whose_file_is_still_indexed(root: Path) -> None:
    prompts = {"id": "CMP-WG5-PROMPTS", "responsibility": "prompt text", "target_refs": ["NI-WG5-001"],
               "planned_artifact_refs": ["ART-WG5-TEST-PROMPTS"]}
    data = _removal({"planned_artifacts": ["ART-WG5-PROMPTS"]}, {"components": [prompts]})
    assert _violations(root, data) == [
        "target_delta.remove.planned_artifacts (ART-WG5-PROMPTS): src/whygame5/prompts.py is still in the Git "
        "index under a governed root; the file must be moved or deleted in the same change, or the topology "
        "check will orphan it"
    ]
    _git(root, "mv", "src/whygame5/prompts.py", "prompts.py")  # moved out of the governed roots
    assert validate_proposal(root, Proposal.model_validate(data)).target is not None


def test_accept_removes_entries_and_keeps_every_other_line(root: Path) -> None:
    before_target = (root / ".aes" / "target.yaml").read_text()
    proposal = root.parent / "remove.yaml"
    # the last component (its trailing blank line ends the family) and a middle artifact
    proposal.write_text(render_yaml(_removal({"components": ["CMP-WG5-REPORT"],
                                              "planned_artifacts": ["ART-WG5-REPORT"]})))
    assert main(["plan", "accept", str(proposal), "--root", str(root)]) == 0

    after_target = (root / ".aes" / "target.yaml").read_text()
    diff = [line for line in difflib.ndiff(before_target.splitlines(), after_target.splitlines())
            if line[:2] in ("- ", "+ ")]
    assert diff == [
        "-   - id: CMP-WG5-REPORT",
        "-     responsibility: static HTML report of proposal, challenge, change and active state",
        "-     target_refs: [NI-WG5-007]",
        "-     planned_artifact_refs: [ART-WG5-REPORT]",
        "-   - id: ART-WG5-REPORT",
        "-     locator: {exact_path: src/whygame5/report.py}",
        "-     kind: source",
        "-     purpose: static HTML report renderer",
        "-     semantic_justification_refs: [NI-WG5-007]",
    ]
    assert "planned_artifact_refs: [ART-WG5-RUNNER, ART-WG5-CLI]\n\nplanned_artifacts:" in after_target
    target = load_target(root / ".aes" / "target.yaml")
    assert "CMP-WG5-REPORT" not in {c.id for c in target.components}
    plan = load_plan(root / ".aes" / "plans" / "PLAN-REMOVE.yaml")
    assert plan.target_delta.remove.components == ["CMP-WG5-REPORT"]
