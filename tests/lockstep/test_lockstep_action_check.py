"""Behavior 5.4: a proposed non-code action is allowed only when it matches the declared action it names.

[[[cog import lockstep.cogtext as c; c.docstring("tests:lockstep:test_lockstep_action_check.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Names no requirement; the layout row says why.
[[[end]]]
"""

import pytest

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


@pytest.mark.req("lockstep-plan-format/an-aes-plan-repository-s-checks-still-run", existing=True)
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


# Tightened against surviving mutants (code2-workspace #944): exact decisions, base reading, malformed entries, command line.
def test_decisions_are_exact(tmp_path):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    assert action_decision(tmp_path, MATCH) == {
        "plan": "ACT-BOARD-STATUS", "kind": "board_update", "target": "Inside-Success/Team-Brains#900",
        "decision": "allow", "purpose": "post the status line on the tracking issue", "refs": ["OUT-001"],
        "reason": "matches ACT-BOARD-STATUS: a board_update on Inside-Success/Team-Brains#900 "
                  "(post the status line on the tracking issue)",
        "summary": "Lockstep: the action follows ACT-BOARD-STATUS and matches it "
                   "(board_update on Inside-Success/Team-Brains#900)."}
    r = "the proposed action names no plan it follows, and every action must name one declared in lockstep.yaml"
    assert action_decision(tmp_path, {}) == {
        "plan": "", "kind": "", "target": "", "decision": "block", "reason": r, "summary": f"Held: {r}."}
    r = ("the proposed action names X, which is not an action declared in lockstep.yaml "
         "(declared: ACT-BOARD-STATUS)")
    assert action_decision(tmp_path, {"plan": "X"})["reason"] == r
    r = ("the proposed action goes against ACT-BOARD-STATUS: the plan allows kind board_update, "
         "and this proposal is kind (none)")
    assert action_decision(tmp_path, {"plan": "ACT-BOARD-STATUS"})["reason"] == r
    r = ("the proposed action goes against ACT-BOARD-STATUS: the plan allows it on Inside-Success/Team-Brains#900, "
         "and this proposal acts on no target")
    assert action_decision(tmp_path, {"plan": "ACT-BOARD-STATUS", "kind": "board_update"})["reason"] == r


def test_several_declared_actions_are_listed_comma_separated(tmp_path):
    two = SIDE + "  - {id: ACT-B, kind: k, target: t, purpose: p}\n"
    (tmp_path / "lockstep.yaml").write_text(two)
    d = action_decision(tmp_path, {"plan": "nope"})
    assert "(declared: ACT-B, ACT-BOARD-STATUS)" in d["reason"]


def test_malformed_entries_are_skipped_and_refs_default_to_empty(tmp_path):
    (tmp_path / "lockstep.yaml").write_text(
        "actions:\n  - just text\n  - {id: A, kind: k, target: t}\n  - {id: B, kind: k, target: t, purpose: p}\n"
        "  - {id: C, kind: k, target: t, purpose: p, refs: [x, '', y]}\n")
    assert declared_actions(tmp_path) == {
        "B": {"kind": "k", "target": "t", "purpose": "p", "refs": []},
        "C": {"kind": "k", "target": "t", "purpose": "p", "refs": ["x", "y"]}}


def test_a_base_revision_with_the_action_allows_it_even_if_the_tree_lost_it(tmp_path):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    sh("git init -q -b main && git add -A && git commit -q -m base", tmp_path)
    (tmp_path / "lockstep.yaml").write_text("schema: lockstep.side.v1\nactions: []\n")
    assert action_decision(tmp_path, MATCH)["decision"] == "block"
    assert action_decision(tmp_path, MATCH, base="HEAD")["decision"] == "allow"
    assert declared_actions(tmp_path, base="HEAD")["ACT-BOARD-STATUS"]["refs"] == ["OUT-001"]


def test_command_defaults_to_the_current_directory_requires_a_proposal_and_describes_itself(
        tmp_path, capsys, monkeypatch):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    (tmp_path / "p.json").write_text(json.dumps(MATCH))
    monkeypatch.chdir(tmp_path)
    assert main(["--proposal", "p.json"]) == 0
    capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        main([])
    assert e.value.code == 2
    capsys.readouterr()
    with pytest.raises(SystemExit):
        main(["--help"])
    out = " ".join(capsys.readouterr().out.split())
    assert "project root holding lockstep.yaml" in out and "the proposal, a JSON file" in out
    assert "read the side file as committed at this revision" in out


def test_a_non_string_value_counts_as_empty_text(tmp_path):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    d = action_decision(tmp_path, {"plan": 5, "kind": ["x"]})
    assert d["plan"] == "" and d["kind"] == ""


def test_the_side_file_is_read_as_utf8(tmp_path):
    (tmp_path / "lockstep.yaml").write_bytes(SIDE.replace("status line", "status – line").encode("utf-8"))
    assert "status – line" in declared_actions(tmp_path)["ACT-BOARD-STATUS"]["purpose"]


def test_command_help_and_errors_are_exact(tmp_path, capsys):
    with pytest.raises(SystemExit):
        main(["--help"])
    out = " ".join(capsys.readouterr().out.split())
    assert out.startswith("usage: ")
    for text in ("Judge a proposed non-code action against the actions Lockstep's side file declares (behavior 5.4).",
                 " project root holding lockstep.yaml ", " the proposal, a JSON file ",
                 " read the side file as committed at this revision"):
        assert text in out + " "
    assert out.endswith("read the side file as committed at this revision")
    p = tmp_path / "p.json"
    p.write_text("[]")
    assert main(["--repo", str(tmp_path), "--proposal", str(p)]) == 2
    assert json.loads(capsys.readouterr().out) == {
        "decision": "error", "error": "ValueError: the proposal must be a JSON object"}
    missing = tmp_path / ("d" * 200) / ("e" * 200) / "p.json"  # a long error message is cut to 300 characters
    assert main(["--repo", str(tmp_path), "--proposal", str(missing)]) == 2
    err = json.loads(capsys.readouterr().out)["error"]
    assert err.startswith("FileNotFoundError: ") and len(err) == len("FileNotFoundError: ") + 300


def test_command_passes_base_through(tmp_path, capsys):
    (tmp_path / "lockstep.yaml").write_text("actions: []\n")
    sh("git init -q -b main && git add -A && git commit -q -m base", tmp_path)
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    (tmp_path / "p.json").write_text(json.dumps(MATCH))
    assert main(["--repo", str(tmp_path), "--proposal", str(tmp_path / "p.json")]) == 0
    assert main(["--repo", str(tmp_path), "--proposal", str(tmp_path / "p.json"), "--base", "HEAD"]) == 1


def test_command_reads_the_proposal_as_utf8(tmp_path, capsys):
    (tmp_path / "lockstep.yaml").write_text(SIDE)
    (tmp_path / "p.json").write_bytes(json.dumps({**MATCH, "body": "–"}, ensure_ascii=False).encode("utf-8"))
    assert main(["--repo", str(tmp_path), "--proposal", str(tmp_path / "p.json")]) == 0
