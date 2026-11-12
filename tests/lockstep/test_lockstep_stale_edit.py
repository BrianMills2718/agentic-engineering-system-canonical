"""Behavior 3.4: an edit to a planned file is warned about, or waits when the hook blocks, while its docstring copy is stale."""

import pytest

from lockstep_support import sh

from lockstep.hook import WARN_PREFIX, decide


def edit(proj) -> dict:
    call = {"tool_name": "Edit", "tool_input": {"file_path": str(proj / "src/greeter/__init__.py")}, "cwd": str(proj)}
    return decide(call)["hookSpecificOutput"]


def test_edit_waits_until_the_copy_is_regenerated(proj, monkeypatch):
    monkeypatch.delenv("PCW_BLOCK_STALE", raising=False)
    monkeypatch.setenv("PCW_MODE", "block")
    assert edit(proj)["permissionDecision"] == "allow"
    sh("aes plan accept plans/plan-002.yaml && git add -A && git commit -q -m 'plan 2'", proj)
    out = edit(proj)
    assert out["permissionDecision"] == "deny"
    assert "out of date with the plan" in out["permissionDecisionReason"] and "make project" in out["permissionDecisionReason"]
    sh("make project", proj)
    assert edit(proj)["permissionDecision"] == "allow"


def test_by_default_a_stale_edit_is_warned_about(proj, monkeypatch):
    monkeypatch.delenv("PCW_BLOCK_STALE", raising=False)
    monkeypatch.delenv("PCW_MODE", raising=False)
    sh("aes plan accept plans/plan-002.yaml && git add -A && git commit -q -m 'plan 2'", proj)
    out = edit(proj)
    assert out["permissionDecision"] == "allow" and out["additionalContext"].startswith(WARN_PREFIX)
    assert "out of date with the plan" in out["additionalContext"]


def test_turned_off_it_only_warns(proj, monkeypatch):
    sh("aes plan accept plans/plan-002.yaml && git add -A && git commit -q -m 'plan 2'", proj)
    monkeypatch.setenv("PCW_MODE", "block")
    monkeypatch.setenv("PCW_BLOCK_STALE", "0")
    assert edit(proj)["permissionDecision"] == "allow"


@pytest.mark.parametrize("mode,decision", [("warn", "allow"), ("block", "deny"), ("fixed", "deny")])
def test_missing_projection_obeys_hook_policy(proj, monkeypatch, mode, decision):
    from lockstep.stale_edit import projection_stale

    monkeypatch.delenv("PCW_BLOCK_STALE", raising=False)
    monkeypatch.setenv("PCW_MODE", "block" if mode == "block" else "warn")
    if mode == "fixed":
        (proj / "lockstep.yaml").write_text("schema: lockstep.side.v1\nfixed: [src/greeter/__init__.py]\n")
    (proj / "src/greeter/__init__.py").write_text("def greet(name): return name\n")
    assert projection_stale(proj, "src/greeter/__init__.py") is not None
    out = edit(proj)
    assert out["permissionDecision"] == decision
    if mode == "warn":
        assert out["additionalContext"].startswith(WARN_PREFIX)
