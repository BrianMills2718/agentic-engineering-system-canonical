"""`lockstep plan units`: the work-unit DAG (spec lockstep-plan-check/work-units-form-a-dag)."""

import json
from pathlib import Path

import pytest

from lockstep.work_units import analyse, units_cli


def unit(id: str, deps=(), touches=(), status="planned", **extra):
    return {"id": id, "title": id, "depends_on": list(deps), "touches": list(touches), "status": status, **extra}


def write(repo: Path, units: list) -> None:
    p = repo / "docs/planning/work-units.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"record_type": "work_units", "units": units}), encoding="utf-8")


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_independent_units_are_both_ready():
    r = analyse({"record_type": "work_units", "units": [unit("A", touches=["a.py"]), unit("B", touches=["b.py"])]})
    assert r["problems"] == [] and r["ready"] == ["A", "B"] and r["conflicts"] == []


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_cycle_fails():
    r = analyse({"record_type": "work_units", "units": [unit("A", ["B"]), unit("B", ["A"])]})
    assert any("cycle" in p for p in r["problems"])


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_missing_dependency_fails():
    r = analyse({"record_type": "work_units", "units": [unit("A", ["Z"])]})
    assert any("A" in p and "Z" in p for p in r["problems"])


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_independent_units_touching_one_file_conflict_but_dependent_ones_do_not():
    r = analyse({"record_type": "work_units", "units": [
        unit("A", touches=["src/x.py"]), unit("B", touches=["src/x.py"]), unit("C", ["A"], ["src/x.py"])]})
    assert r["conflicts"] == [{"units": ["A", "B"], "files": ["src/x.py"]},
                              {"units": ["B", "C"], "files": ["src/x.py"]}]


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_merged_needs_evidence_and_unlocks_dependents():
    bad = analyse({"record_type": "work_units", "units": [unit("A", status="merged")]})
    assert any("evidence" in p for p in bad["problems"])
    ok = analyse({"record_type": "work_units", "units": [unit("A", status="merged", evidence="PR 1"), unit("B", ["A"])]})
    assert ok["problems"] == [] and ok["ready"] == ["B"] and ok["critical_path"] == ["B"]


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_critical_path_is_longest_unmerged_chain():
    r = analyse({"record_type": "work_units", "units": [unit("A"), unit("B", ["A"]), unit("C", ["B"]), unit("D")]})
    assert r["critical_path"] == ["A", "B", "C"]


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_cli_exit_codes(tmp_path, capsys):
    assert units_cli(["--repo", str(tmp_path)]) == 2
    write(tmp_path, [unit("A"), unit("B", ["A"])])
    assert units_cli(["--repo", str(tmp_path)]) == 0
    write(tmp_path, [unit("A", ["A"])])
    assert units_cli(["--repo", str(tmp_path)]) == 1


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_malformed_json_is_exit_2(tmp_path):
    p = tmp_path / "docs/planning/work-units.json"
    p.parent.mkdir(parents=True)
    p.write_text("{not json", encoding="utf-8")
    assert units_cli(["--repo", str(tmp_path)]) == 2


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_cli_prints_ready_critical_path_and_conflicts(tmp_path, capsys):
    write(tmp_path, [unit("A", touches=["x.py"]), unit("B", touches=["x.py"]), unit("C", ["A"])])
    assert units_cli(["--repo", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "ready: A, B" in out and "critical path: A -> C" in out
    assert "conflict: A and B are independent but both touch x.py" in out


@pytest.mark.req("lockstep-plan-check/work-units-form-a-dag")
def test_plan_check_reports_work_unit_problems_when_file_present(tmp_path, capsys):
    from lockstep.plan_check import plan_cli
    write(tmp_path, [unit("A", ["Z"])])
    (tmp_path / "docs/planning/router").mkdir(parents=True, exist_ok=True)
    entry = {"id": "A1", "criterion": "c", "demonstration": ["s"], "expected": "e", "failure_example": "f",
             "representation": {"view": "table", "router_record": "docs/planning/router/a1.recommendation.json"},
             "entrypoint": "planned", "status": "not built"}
    (tmp_path / "docs/planning/router/a1.recommendation.json").write_text("{}", encoding="utf-8")
    (tmp_path / "docs/planning/acceptance-criteria.json").write_text(json.dumps(
        {"schema_version": "1.0", "record_type": "acceptance_criteria", "entries": [entry]}), encoding="utf-8")
    capsys.readouterr()
    assert plan_cli(["check", "--repo", str(tmp_path)]) == 1
    assert "work units: A: depends_on names Z" in capsys.readouterr().out
