"""Behavior 3.8: an edit by hand to the plan file is warned about at edit time, with every linked file and symbol.

[[[cog import lockstep.cogtext as c; c.docstring("TST-PLAN-EDIT", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

SC-3.8: An Edit, MultiEdit or Write call that changes a plan item's text in
  .aes/target.yaml is answered by the edit hook with a warning (a refusal
  under PCW_MODE=block) that names each changed item and lists every file
  whose docstring carries it, with that file's declared symbols; a call that
  leaves the plan's items unchanged gets no such warning.
  Disproved if: A hand edit that changes a plan item gets no warning from
  the edit hook, or its warning misses a changed item or a file that carries
  it; or an edit that changes no plan item is warned about.
Proven by: VS-3.8-a (tests/test_plan_edit.py)
[[[end]]] (sum: q6/Y/SDAAr)
"""

import yaml

from lockstep_support import sh
from test_lockstep_change_list import _aes_linked
from lockstep.hook import decide
from lockstep.plan_edit import plan_edit_reason

SRC = "src/greeter/__init__.py"
SIGNATURE = "greet(name: str) -> str"
TARGET = ".aes/target.yaml"


def _with_exports(proj):
    """Declare greet's typed signature, so the list has a symbol to name."""
    path = proj / TARGET
    t = yaml.safe_load(path.read_text())
    next(a for a in t["planned_artifacts"] if a["id"] == "ART-GREET")["exports"] = [SIGNATURE]
    path.write_text(yaml.safe_dump(t, sort_keys=False))
    sh("git add -A && git commit -q -m exports", proj)


def _reworded(proj) -> str:
    """The plan's text with NI-001's statement changed, as a hand edit would leave it."""
    t = yaml.safe_load((proj / TARGET).read_text())
    item = next(n for n in t["normative_items"] if n["id"] == "NI-001")
    item["statement"] = item["statement"] + " Reworded by hand."
    return yaml.safe_dump(t, sort_keys=False)


def test_a_changed_item_is_named_with_every_linked_file_and_symbol(proj):
    _with_exports(proj)
    reason = plan_edit_reason(proj, TARGET, _reworded(proj))
    assert reason is not None and "by hand, which changes NI-001" in reason
    assert f"- {SRC} (ART-GREET): NI-001; symbols: {SIGNATURE}" in reason
    listed = {line[2:].split(" (")[0] for line in reason.splitlines() if line.startswith("- ")}
    assert listed == _aes_linked(proj, ["NI-001"]) == {SRC}  # AES's own context rule, run through its CLI


def test_an_edit_that_changes_no_plan_item_is_not_reported(proj):
    same = (proj / TARGET).read_text() + "\n# a comment\n"
    assert plan_edit_reason(proj, TARGET, same) is None
    assert plan_edit_reason(proj, SRC, _reworded(proj)) is None  # only the plan file is judged


def test_the_edit_hook_warns_by_default_and_refuses_under_block_mode(proj, monkeypatch):
    monkeypatch.delenv("PCW_MODE", raising=False)
    _with_exports(proj)
    call = {"hook_event_name": "PreToolUse", "cwd": str(proj), "tool_name": "Write",
            "tool_input": {"file_path": str(proj / TARGET), "content": _reworded(proj)}}
    warned = decide(call)["hookSpecificOutput"]
    assert warned["permissionDecision"] == "allow" and f"- {SRC} (ART-GREET)" in warned["additionalContext"]
    monkeypatch.setenv("PCW_MODE", "block")
    out = decide(call)["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny" and "changes NI-001" in out["permissionDecisionReason"]


def test_an_edit_leaving_the_plan_items_as_they_were_gets_no_plan_warning(proj, monkeypatch):
    monkeypatch.setenv("PCW_MODE", "block")
    call = {"hook_event_name": "PreToolUse", "cwd": str(proj), "tool_name": "Write",
            "tool_input": {"file_path": str(proj / TARGET), "content": (proj / TARGET).read_text() + "\n# note\n"}}
    out = decide(call)
    assert out is None or "by hand" not in str(out)
