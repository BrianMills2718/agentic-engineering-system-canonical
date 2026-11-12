"""Behavior 1.3: a planned file whose declaration gives no reason is refused."""

import yaml

from lockstep_support import REPO, sh
from lockstep.aes_bridge import target
from lockstep.check import check
from lockstep.declared_reason import main, reasonless_artifacts

NO_REASON_PLAN = """\
schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-009-NO-REASON
title: A file with no reason
rationale: AES accepts an empty reason list; Lockstep must not.
closes_gaps: []
trace_review:
  runs_traced_work: false
  reason: plain Python, judged by its tests.
target_delta:
  add:
    planned_artifacts:
      - id: ART-NOTE
        locator: {exact_path: src/greeter/note.py}
        kind: source
        purpose: a file with no reason
        semantic_justification_refs: []
  change:
    components:
      - id: CMP-GREETER
        responsibility: say hello
        target_refs: [NI-001]
        planned_artifact_refs: [ART-GREET, ART-TEST, ART-NOTE]
"""


def test_a_file_with_an_empty_reason_list_is_reported():
    plan = {"planned_artifacts": [
        {"id": "ART-A", "locator": {"exact_path": "src/a.py"}, "semantic_justification_refs": ["BEH-1"]},
        {"id": "ART-B", "locator": {"exact_path": "src/b.py"}, "semantic_justification_refs": []}]}
    assert reasonless_artifacts(plan) == [
        "ART-B (src/b.py) gives no reason for being in the plan: its semantic_justification_refs list is "
        "empty. Name the requirement, behavior or criterion it serves, through "
        "`aes plan prepare/validate/accept`."]


def test_make_check_refuses_a_plan_holding_a_file_with_no_reason(proj, capsys):
    assert main(["--root", str(proj)]) == 0
    t = yaml.safe_load((proj / ".aes/target.yaml").read_text())
    t["planned_artifacts"][0]["semantic_justification_refs"] = []
    (proj / ".aes/target.yaml").write_text(yaml.safe_dump(t, sort_keys=False))
    assert main(["--root", str(proj)]) == 1
    assert capsys.readouterr().out.splitlines()[-1] == "declared_reason: files=2 problems=1"


def test_aes_accepts_a_file_with_no_reason_and_pcw_check_refuses_it(proj):
    (proj / "plans/plan-009.yaml").write_text(NO_REASON_PLAN)
    sh("aes plan accept plans/plan-009.yaml", proj)  # AES lets the empty list through
    out = check(proj)
    assert out["decision"] == "block" and out["counts"]["reasonless"] == 1
    [held] = [f for f in out["files"] if f["blocks"]]
    assert held["path"] == ".aes/target.yaml"
    assert "accepts PLAN-009-NO-REASON" in held["reason"] and "ART-NOTE (src/greeter/note.py)" in held["reason"]
