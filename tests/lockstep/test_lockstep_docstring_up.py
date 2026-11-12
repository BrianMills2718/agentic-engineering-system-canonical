"""Behavior 3.6: an edit to a docstring's plan text becomes a draft plan change, accepted by the agent when it is confident or the change is not significant, otherwise by a person."""

import shutil

import yaml

from lockstep_support import EXAMPLE, REPO, sh
from lockstep.change_log import entries
from lockstep.docstring_up import draft_from_docstring, main

REL = "src/greeter/__init__.py"
OLD = 'NI-001: greet(name) returns "Hello, <name>!".'
NEW = 'NI-001: greet(name) returns "Hello, <name>!" and never shouts.'
EXPORTS = """\
schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-102-EXPORTS
title: Declare greet with its types
rationale: the test needs a declared signature to edit.
closes_gaps: []
trace_review:
  runs_traced_work: false
  reason: plain Python, judged by its tests.
target_delta:
  change:
    planned_artifacts:
      - id: ART-GREET
        locator: {exact_path: src/greeter/__init__.py}
        kind: source
        purpose: the greet function
        semantic_justification_refs: [NI-001]
        exports: ['greet(name: str) -> str']
"""


def _edit(proj, old, new):
    text = (proj / REL).read_text()
    assert old in text
    (proj / REL).write_text(text.replace(old, new, 1))


def test_an_edit_becomes_a_draft_and_the_plan_waits_for_acceptance(proj):
    plan_before = (proj / ".aes/target.yaml").read_text()
    copy_before = (proj / REL).read_text()
    _edit(proj, OLD, NEW)

    drafts, problems = draft_from_docstring(proj, REL, proj / "plans")
    assert problems == [] and len(drafts) == 1
    doc = yaml.safe_load(drafts[0].read_text())
    assert doc["proposal_id"].startswith("DOCSTRING-ART-GREET-")
    assert doc["target_delta"] == {"change": {"normative_items": [
        {"id": "NI-001", "kind": "behavior", "outcome_refs": ["OUT-001"],
         "statement": 'greet(name) returns "Hello, <name>!" and never shouts.'}]}}
    assert (proj / ".aes/target.yaml").read_text() == plan_before  # unchanged until accepted
    assert (proj / REL).read_text() == copy_before  # the copy is back to the plan, checksum and all
    sh(f"cog --check -c {REL}", proj)

    sh(f"aes plan accept {drafts[0].relative_to(proj)}", proj)
    sh("make project", proj)
    assert NEW in (proj / REL).read_text()
    sh("git add -A && git commit -q -m 'accept the docstring edit'", proj)
    assert entries(proj)[-1]["origin"] == "docstring"


def test_make_project_drafts_the_edit_before_it_regenerates_the_copy(proj):
    _edit(proj, OLD, NEW)
    out = sh("make project", proj)
    [draft] = sorted((proj / "plans").glob("DOCSTRING-*.yaml"))
    assert f"drafted plans/{draft.name} from the edit to {REL}" in out
    assert "never shouts" in draft.read_text() and NEW not in (proj / REL).read_text()
    sh(f"cog --check -c {REL}", proj)  # the copy is the plan's again; the edit lives in the draft


def test_a_copy_the_plan_moved_past_is_not_an_edit(proj):
    shutil.copy(EXAMPLE / "plans/plan-002.yaml", proj / "plans/plan-002.yaml")
    sh("aes plan accept plans/plan-002.yaml", proj)
    assert draft_from_docstring(proj, REL, proj / "plans") == ([], [])
    assert OLD in (proj / REL).read_text()  # left for `make project` to regenerate


def test_an_edit_to_a_copy_of_an_earlier_plan_is_reported_and_left_alone(proj):
    shutil.copy(EXAMPLE / "plans/plan-002.yaml", proj / "plans/plan-002.yaml")
    sh("aes plan accept plans/plan-002.yaml", proj)
    _edit(proj, OLD, NEW)
    edited = (proj / REL).read_text()
    drafts, [problem] = draft_from_docstring(proj, REL, proj / "plans")
    assert drafts == [] and "it was copied from an earlier plan" in problem
    assert (proj / REL).read_text() == edited


def test_an_edit_that_renames_an_item_is_reported_and_left_alone(proj):
    _edit(proj, "Proven by: VS-GREET", "Proven by: VS-OTHER")
    edited = (proj / REL).read_text()
    drafts, [problem] = draft_from_docstring(proj, REL, proj / "plans")
    assert drafts == [] and "changes a 'Proven by' line" in problem
    assert (proj / REL).read_text() == edited
    assert main(["--root", str(proj)]) == 1


def test_an_edited_signature_becomes_a_change_to_the_declared_exports(proj, tmp_path):
    (tmp_path / "p.yaml").write_text(EXPORTS)
    sh(f"aes plan accept {tmp_path / 'p.yaml'}", proj)
    sh("make project && git add -A && git commit -q -m exports", proj)
    _edit(proj, "    greet(name: str) -> str\n", "    greet(name: str, loud: bool = False) -> str\n")
    [draft], problems = draft_from_docstring(proj, REL, proj / "plans")
    assert problems == []
    [art] = yaml.safe_load(draft.read_text())["target_delta"]["change"]["planned_artifacts"]
    assert art["id"] == "ART-GREET" and art["exports"] == ["greet(name: str, loud: bool = False) -> str"]
