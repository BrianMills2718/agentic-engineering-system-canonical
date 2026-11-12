"""`lockstep plan check`: the acceptance-criteria file and the plan's requirements (slice 5).

Ported from company-planning at b8a53a0: tests/test_planning_compliance_skill.py (the acceptance tests) and
tests/test_goal_coverage.py (the offline checks of a stored judgment).
"""

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from lockstep.plan_check import plan_cli

ENTRY = {
    "id": "A1", "criterion": "Brian can see which sources back each claim on the report page",
    "demonstration": ["Open the report page", "Click the first claim", "Read the evidence panel"],
    "expected": "Each claim opens a panel listing its sources with links that resolve",
    "failure_example": "Claim 3 cites a page that does not mention it: the panel shows no matching quote",
    "representation": {"view": "table", "router_record": "docs/planning/router/a1.recommendation.json"},
    "entrypoint": "planned", "status": "not built"}


def write(repo: Path, rel: str, content: object) -> Path:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
    return path


def acceptance(repo: Path, entries: list, **extra: object) -> Path:
    write(repo, "docs/planning/router/a1.recommendation.json", {})
    return write(repo, "docs/planning/acceptance-criteria.json",
                 {"schema_version": "1.0", "record_type": "acceptance_criteria", "entries": entries, **extra})


def run(repo: Path, capsys, *args: str) -> tuple[int, str]:
    code = plan_cli(["check", "--repo", str(repo), *args])
    out = capsys.readouterr()
    return code, out.out + out.err


@pytest.mark.req("lockstep-plan-check/a-complete-acceptance-file-passes")
def test_a_complete_acceptance_file_passes(tmp_path, capsys):
    acceptance(tmp_path, [ENTRY])
    code, out = run(tmp_path, capsys)
    assert code == 0, out
    assert "1 criteria: 1 not built, 0 built, 0 judged pass, 0 judged fail" in out


@pytest.mark.req("lockstep-plan-check/an-entry-missing-a-field-fails")
@pytest.mark.parametrize("field", ["criterion", "demonstration", "expected", "failure_example", "representation",
                                   "entrypoint", "status"])
def test_an_entry_missing_a_field_fails(tmp_path, capsys, field):
    entry = copy.deepcopy(ENTRY)
    del entry[field]
    acceptance(tmp_path, [entry])
    code, out = run(tmp_path, capsys)
    assert code == 1 and f"A1: no {field}" in out, out


@pytest.mark.req("lockstep-plan-check/a-malformed-entry-fails")
@pytest.mark.parametrize("expected, change", [
    ("A1: demonstration must be a list of steps", {"demonstration": "open it and look"}),
    ("A1: demonstration must be a list of steps", {"demonstration": ["ok", " "]}),
    ("A1: representation.router_record docs/none.json: docs/none.json does not exist",
     {"representation": {"view": "table", "router_record": "docs/none.json"}}),
    ("A1: representation has no view", {"representation": {"router_record": "docs/planning/router/a1.recommendation.json"}}),
    ("A1: representation must be {view, router_record}", {"representation": "table"}),
    ("A1: representation.variants must name an existing sketch-set file",
     {"representation": {"view": "t", "router_record": "docs/planning/router/a1.recommendation.json",
                         "variants": "docs/nope.json"}}),
    ("A1: entrypoint must be a URL or planned", {"entrypoint": "later"}),
    ("A1: status must be one of", {"status": "done"}),
    ("A1: criterion must be text", {"criterion": ["a"]}),
])
def test_a_malformed_entry_fails(tmp_path, capsys, expected, change):
    acceptance(tmp_path, [{**ENTRY, **change}])
    code, out = run(tmp_path, capsys)
    assert code == 1 and expected in out, out


@pytest.mark.req("lockstep-plan-check/a-built-entry-that-still-says-planned-fails")
def test_a_built_entry_that_still_says_planned_fails(tmp_path, capsys):
    acceptance(tmp_path, [{**ENTRY, "status": "built"}])
    code, out = run(tmp_path, capsys)
    assert code == 1 and "A1: status built but entrypoint is planned" in out, out


@pytest.mark.req("lockstep-plan-check/a-judged-status-without-the-judge-s-words-fails")
def test_a_judged_status_without_the_judges_words_fails(tmp_path, capsys):
    judged = {**ENTRY, "status": "judged pass", "entrypoint": "https://example.invalid/page"}
    acceptance(tmp_path, [judged])
    code, out = run(tmp_path, capsys)
    assert code == 1 and "A1: judged pass needs judgment {by, source}" in out, out
    acceptance(tmp_path, [{**judged, "judgment": {"by": "brian", "source": 'chat 2026-10-27: "yes that works"'}}])
    code, out = run(tmp_path, capsys)
    assert code == 0 and "1 judged pass" in out, out
    acceptance(tmp_path, [{**judged, "status": "judged fail", "judgment": {"by": "brian"}}])
    code, out = run(tmp_path, capsys)
    assert code == 1 and "judged fail needs judgment" in out, out


@pytest.mark.req("lockstep-plan-check/duplicate-ids-and-an-empty-list-fail")
def test_duplicate_ids_and_an_empty_list_fail(tmp_path, capsys):
    acceptance(tmp_path, [ENTRY, ENTRY])
    code, out = run(tmp_path, capsys)
    assert code == 1 and "A1: duplicate id" in out, out
    acceptance(tmp_path, [])
    code, out = run(tmp_path, capsys)
    assert code == 1 and "entries: none listed" in out, out
    write(tmp_path, "docs/planning/acceptance-criteria.json", {"record_type": "nope", "entries": [ENTRY]})
    code, out = run(tmp_path, capsys)
    assert code == 1 and "record_type is not acceptance_criteria" in out, out


@pytest.mark.req("lockstep-plan-check/a-missing-or-unreadable-file-cannot-be-checked")
def test_a_missing_or_unreadable_file_cannot_be_checked(tmp_path, capsys):
    code, out = run(tmp_path, capsys)
    assert code == 2 and "not found" in out, out
    write(tmp_path, "docs/planning/acceptance-criteria.json", "{not json")
    code, out = run(tmp_path, capsys)
    assert code == 2 and "not JSON" in out, out


@pytest.mark.req("lockstep-plan-check/the-acceptance-path-can-be-overridden")
def test_the_acceptance_path_can_be_overridden(tmp_path, capsys):
    path = acceptance(tmp_path, [ENTRY])
    other = tmp_path / "elsewhere.json"
    other.write_text(path.read_text().replace('"not built"', '"done"'), encoding="utf-8")
    path.unlink()
    code, out = run(tmp_path, capsys, "--acceptance", "elsewhere.json")
    assert code == 1 and "A1: status must be one of" in out, out


def test_json_output_is_one_object(tmp_path, capsys):
    acceptance(tmp_path, [ENTRY])
    code, out = run(tmp_path, capsys, "--json")
    data = json.loads(out)
    assert code == 0 and data["ok"] is True and data["problems"] == []


def test_the_command_is_reached_through_lockstep_plan(tmp_path):
    acceptance(tmp_path, [ENTRY])
    p = subprocess.run([sys.executable, "-c", "import sys; sys.argv=['lockstep','plan','check','--repo',sys.argv[1]];"
                        "from lockstep.check import cli; raise SystemExit(cli())", str(tmp_path)],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
