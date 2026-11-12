"""Behavior 5.5: an added undeclared public symbol or a changed declared signature is warned at edit and refused before commit.

[[[cog import lockstep.cogtext as c; c.docstring("TST-SYMBOL-GATE", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

SC-5.5: A change that adds an undeclared public function or class, changes a
  declared function's signature, or removes a declared export the file
  defined before, is reported with the symbol named; the edit hook warns
  about it by default and refuses it under PCW_MODE=block; `pcw check`
  blocks it; a change that adds only private or declared symbols with their
  declared signatures passes; an undeclared symbol already present before
  the change, or a declared export already missing before it, is not
  reported.
  Disproved if: An added undeclared public function or class, a changed
  declared signature, or a removed declared export passes the edit hook with
  no warning or passes `pcw check`; a change with only declared, matching
  symbols is refused; a symbol present before the change is reported against
  it; or a new file is refused only for a declared export it does not define
  yet.
Proven by: VS-5.5-a (tests/test_symbol_gate.py)
[[[end]]] (sum: MXOQ707TAq)
"""

import io
import json
import sys

import pytest

from lockstep_support import REPO as _TESTS

REPO = _TESTS / "lockstep-plan-sample"  # Lockstep's own plan, frozen (see its README)

from lockstep import hook
from lockstep.check import check
from lockstep.symbol_gate import added_symbol_problems, text_after

REL = "src/pcw/action_check.py"  # planned in Lockstep's own plan, with typed exports


def _text() -> str:
    return (REPO / REL).read_text()


def test_an_added_public_function_is_reported_and_a_private_one_is_not():
    before = _text()
    public = before + "\n\ndef extra_summary(page: str) -> str:\n    return page\n"
    private = before + "\n\ndef _extra_summary(page: str) -> str:\n    return page\n"
    found = added_symbol_problems(REPO, REL, public, before)
    assert len(found) == 1 and "extra_summary(page: str) -> str" in found[0] and "does not declare" in found[0]
    assert added_symbol_problems(REPO, REL, private, before) == []


def test_a_changed_declared_signature_is_reported_with_both_signatures():
    before = _text()
    after = before.replace("def declared_actions(root: Path, base: str | None = None)",
                           "def declared_actions(root: Path, base: str | None = None, strict: bool = False)")
    assert after != before
    found = added_symbol_problems(REPO, REL, after, before)
    assert len(found) == 1
    assert "strict: bool=False" in found[0] and "declares declared_actions(root: Path, base: str | None=None)" in found[0]


def test_a_problem_already_there_before_the_change_is_not_counted():
    drifted = _text() + "\n\ndef extra_summary(page: str) -> str:\n    return page\n"
    later = drifted + "\n# a comment added later\n"
    assert added_symbol_problems(REPO, REL, later, drifted) == []
    assert len(added_symbol_problems(REPO, REL, later, None)) == 1  # a new file is judged whole


def test_removing_a_declared_export_is_reported_and_one_never_written_is_not():
    """Q38: plan-to-code drift from an uncommitted edit shows at edit time, not only after the commit."""
    before = _text()
    start = before.index("def declared_actions(")
    end = before.index("\ndef ", start + 1)
    after = before[:start] + before[end + 1:]
    found = added_symbol_problems(REPO, REL, after, before)
    assert len(found) == 1 and "would no longer define declared_actions" in found[0]
    assert added_symbol_problems(REPO, REL, after, after) == []  # already missing before: not this change's
    assert added_symbol_problems(REPO, REL, after, None) == []  # a new file not yet complete: unwritten, not removed


def test_an_unplanned_or_non_python_path_is_not_judged():
    assert added_symbol_problems(REPO, "src/pcw/not_planned.py", "def x(): pass\n", None) == []
    assert added_symbol_problems(REPO, "wiki/index.md", "def x(): pass\n", None) == []


def test_text_after_applies_edit_multiedit_write_and_openhands(tmp_path):
    f = tmp_path / "m.py"
    f.write_text("a = 1\nb = 2\n")
    assert text_after({"tool_name": "Write", "tool_input": {"content": "z"}}, f) == "z"
    assert text_after({"tool_name": "Edit", "tool_input": {"old_string": "a = 1", "new_string": "a = 3"}}, f) == "a = 3\nb = 2\n"
    multi = {"tool_name": "MultiEdit", "tool_input": {"edits": [{"old_string": "a", "new_string": "c"},
                                                                {"old_string": "b", "new_string": "d"}]}}
    assert text_after(multi, f) == "c = 1\nd = 2\n"
    oh = {"tool_name": "file_editor", "tool_input": {"command": "str_replace", "old_str": "b = 2", "new_str": "b = 5"}}
    assert text_after(oh, f) == "a = 1\nb = 5\n"
    assert text_after({"tool_name": "Edit", "tool_input": {"old_string": "missing", "new_string": "x"}}, f) is None


def _edit_call(proj, new_function: str) -> dict:
    path = proj / "src/greeter/__init__.py"
    text = path.read_text()
    return {"hook_event_name": "PreToolUse", "cwd": str(proj), "tool_name": "Edit",
            "tool_input": {"file_path": str(path), "old_string": text[-20:], "new_string": text[-20:] + new_function}}


def _run_hook(call, monkeypatch, capsys) -> dict:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(call)))
    monkeypatch.setattr(sys, "argv", ["pcw-hook"])
    assert hook.main() == 0
    return json.loads(capsys.readouterr().out)["hookSpecificOutput"]


NEW = "\n\ndef wave(name: str) -> str:\n    return name\n"


@pytest.mark.parametrize("mode", ["warn", "block"])
def test_the_edit_hook_warns_by_default_and_refuses_under_block_mode(proj, mode, monkeypatch, capsys):
    monkeypatch.delenv("PCW_MODE", raising=False)
    if mode == "block":
        monkeypatch.setenv("PCW_MODE", "block")
    out = _run_hook(_edit_call(proj, NEW), monkeypatch, capsys)
    if mode == "block":
        assert out["permissionDecision"] == "deny" and "wave(name: str) -> str" in out["permissionDecisionReason"]
    else:
        assert out["permissionDecision"] == "allow"
        assert out["additionalContext"].startswith(hook.WARN_PREFIX) and "wave(name: str) -> str" in out["additionalContext"]


def test_pcw_check_blocks_a_change_that_adds_an_undeclared_function(proj):
    path = proj / "src/greeter/__init__.py"
    path.write_text(path.read_text() + NEW)
    out = check(proj)
    assert out["decision"] == "block"
    assert [(f["path"], f["kind"]) for f in out["files"]] == [("src/greeter/__init__.py", "symbols")]
    assert "wave(name: str) -> str" in out["files"][0]["reason"] and out["counts"]["symbols"] == 1


def test_pcw_check_allows_a_change_that_adds_only_a_private_function(proj):
    path = proj / "src/greeter/__init__.py"
    path.write_text(path.read_text() + "\n\ndef _wave(name: str) -> str:\n    return name\n")
    assert check(proj)["decision"] == "allow"


def test_the_edit_hook_refuses_removing_a_declared_function_before_any_commit(monkeypatch):
    """Q38: an uncommitted edit that drops a planned export is answered at edit time (pcw check uses the same rule)."""
    monkeypatch.setenv("PCW_MODE", "block")
    text = _text()
    old = text[text.index("def declared_actions("):text.index("\ndef ", text.index("def declared_actions(") + 1) + 1]
    call = {"tool_name": "Edit", "cwd": str(REPO),
            "tool_input": {"file_path": str(REPO / REL), "old_string": old, "new_string": ""}}
    out = hook.decide(call)["hookSpecificOutput"]
    hook._PENDING.clear()  # decide() only queues its log line; nothing is written to this repository
    assert out["permissionDecision"] == "deny" and "would no longer define declared_actions" in out["permissionDecisionReason"]
