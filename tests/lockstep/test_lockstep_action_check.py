"""Behavior 5.4: a proposed non-code action is allowed only when it matches the declared action it names.

[[[cog import lockstep.cogtext as c; c.docstring("TST-ACTION-CHECK", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

SC-5.4: A proposal whose plan names a declared action with the same kind and
  target is allowed and the decision names that action and its purpose; a
  proposal with no plan, with a plan the side file does not declare, or with
  a different kind or target is held with a reason that says which; the side
  file is read at the base revision when one is given, so a change to it
  does not change the decision.
  Disproved if: A proposal naming no action, or an undeclared one, or
  differing from its action in kind or target is allowed; a matching
  proposal is held; a held decision has no reason; or an edit to the working
  tree's side file changes a decision made at a base revision.
Proven by: VS-5.4-a (tests/test_action_check.py)
[[[end]]] (sum: VZfAgw1yPp)
"""

import json

from lockstep_support import sh
from lockstep.action_check import action_decision, declared_actions, main

SIDE = """schema: lockstep.side.v1
actions:
  - id: ACT-BOARD-STATUS
    kind: board_update
    target: Inside-Success/Team-Brains#900
    purpose: post the status line on the tracking issue
    refs: [OUT-001]
"""
MATCH = {"plan": "ACT-BOARD-STATUS", "kind": "board_update", "target": "Inside-Success/Team-Brains#900",
         "body": "Status: the runner gate is live."}


def test_a_matching_proposal_is_allowed_and_names_its_action(tmp_path):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    d = action_decision(tmp_path, MATCH)
    assert d["decision"] == "allow"
    assert d["plan"] == "ACT-BOARD-STATUS" and d["purpose"] == "post the status line on the tracking issue"
    assert d["refs"] == ["OUT-001"]
    assert declared_actions(tmp_path) == {"ACT-BOARD-STATUS": {
        "kind": "board_update", "target": "Inside-Success/Team-Brains#900",
        "purpose": "post the status line on the tracking issue", "refs": ["OUT-001"]}}


def test_no_plan_an_undeclared_plan_another_target_or_kind_is_held_with_the_reason(tmp_path):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    cases = {
        "names no plan": {**MATCH, "plan": ""},
        "ACT-CLOSE-ISSUES, which is not an action declared": {**MATCH, "plan": "ACT-CLOSE-ISSUES"},
        "allows it on Inside-Success/Team-Brains#900, and this proposal acts on Inside-Success/Team-Brains#1":
            {**MATCH, "target": "Inside-Success/Team-Brains#1"},
        "allows kind board_update, and this proposal is kind issue_close": {**MATCH, "kind": "issue_close"},
    }
    for words, proposal in cases.items():
        d = action_decision(tmp_path, proposal)
        assert d["decision"] == "block", proposal
        assert words in d["reason"], d["reason"]
        assert d["summary"] == f"Held: {d['reason']}."


def test_a_project_with_no_side_file_holds_every_proposal(tmp_path):
    d = action_decision(tmp_path, MATCH)
    assert d["decision"] == "block" and "(declared: none)" in d["reason"]


def test_the_side_file_is_read_at_the_base_revision(tmp_path):
    (tmp_path / "lockstep.yaml").write_text("schema: lockstep.side.v1\nactions: []\n")
    sh("git init -q -b main && git add -A && git commit -q -m base", tmp_path)
    (tmp_path / "lockstep.yaml").write_text(SIDE)  # the change tries to declare its own action
    assert action_decision(tmp_path, MATCH)["decision"] == "allow"  # the working tree would allow it
    assert action_decision(tmp_path, MATCH, base="HEAD")["decision"] == "block"


def test_the_command_prints_the_decision_and_exits_by_it(tmp_path, capsys):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    (tmp_path / "p.json").write_text(json.dumps(MATCH))
    assert main(["--repo", str(tmp_path), "--proposal", str(tmp_path / "p.json")]) == 0
    assert json.loads(capsys.readouterr().out)["decision"] == "allow"
    (tmp_path / "p.json").write_text(json.dumps({**MATCH, "plan": ""}))
    assert main(["--repo", str(tmp_path), "--proposal", str(tmp_path / "p.json")]) == 1
    (tmp_path / "p.json").write_text("[]")
    assert main(["--repo", str(tmp_path), "--proposal", str(tmp_path / "p.json")]) == 2
