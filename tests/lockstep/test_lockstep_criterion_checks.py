"""Behavior 2.1: every success criterion names how it is checked: a test, a sign-off or an AI rubric."""

import yaml

from lockstep_support import REPO
from lockstep.aes_bridge import target
from lockstep.criterion_checks import criterion_problems, main


def _plan(**vs):
    return {"success_criteria": [{"id": "SC-1"}],
            "verification_subjects": [{"id": "VS-1", "criterion_refs": ["SC-1"], **vs}] if vs else []}


def test_a_test_or_a_sign_off_checks_a_criterion():
    assert criterion_problems(_plan(proof_kind="deterministic_test", locator="tests/test_a.py"), {}) == []
    assert criterion_problems(_plan(proof_kind="human_review", locator="Brian signs off"), {}) == []
    assert criterion_problems(_plan(proof_kind="trace_review", locator="trace"), {}) == []


def test_criterion_with_no_route_or_only_an_observation_is_reported():
    assert criterion_problems(_plan(), {}) == [
        "SC-1 names no way it is checked: give it a test file, a sign-off (human_review or trace_review) "
        "or an AI-graded rubric in lockstep.yaml."]
    [p] = criterion_problems(_plan(proof_kind="runtime_observation", locator="logs"), {})
    assert "its only routes: runtime_observation" in p
    [p] = criterion_problems(_plan(proof_kind="deterministic_test", locator=" "), {})
    assert "deterministic_test with no locator" in p


def test_an_ai_graded_rubric_can_be_declared_for_a_criterion():
    assert criterion_problems(_plan(), {"SC-1": "The answer cites the source line."}) == []
    assert criterion_problems(_plan(), {"SC-9": "x"})[-1] == (
        "lockstep.yaml declares a rubric for SC-9, which is not a success criterion in .aes/target.yaml.")


def test_rubric_in_the_side_file_reaches_the_check(proj):
    t = yaml.safe_load((proj / ".aes/target.yaml").read_text())
    t["verification_subjects"][0]["proof_kind"] = "runtime_observation"
    (proj / ".aes/target.yaml").write_text(yaml.safe_dump(t, sort_keys=False))
    assert main(["--root", str(proj)]) == 1
    (proj / "lockstep.yaml").write_text(yaml.safe_dump({
        "schema": "lockstep.side.v1",
        "rubrics": [{"criterion": "SC-001", "rubric": "The greeting names the person greeted."}]}))
    assert main(["--root", str(proj)]) == 0
