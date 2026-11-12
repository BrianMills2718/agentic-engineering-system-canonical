"""Behavior 3.5: after a plan change, the agent gets one list of every file and symbol linked to a changed item."""

import json
import subprocess

import yaml

from lockstep_support import ENV, sh
from lockstep.change_list import change_list, render
from lockstep.hook import decide

SRC = "src/greeter/__init__.py"
SIGNATURE = "greet(name: str) -> str"


def _with_exports(proj):
    """Declare greet's typed signature, so the list has a symbol to name."""
    path = proj / ".aes/target.yaml"
    t = yaml.safe_load(path.read_text())
    next(a for a in t["planned_artifacts"] if a["id"] == "ART-GREET")["exports"] = [SIGNATURE]
    path.write_text(yaml.safe_dump(t, sort_keys=False))
    sh("git add -A && git commit -q -m exports", proj)


def _aes_linked(proj, changed):
    """The independent route: `aes context <artifact>` for every artifact, through the CLI."""
    t = yaml.safe_load((proj / ".aes/target.yaml").read_text())
    linked = set()
    for art in t["planned_artifacts"]:
        out = subprocess.run(["aes", "context", art["id"], "--format", "json"], cwd=proj, env=ENV,
                             capture_output=True, text=True, check=True).stdout
        ctx = json.loads(out)
        ids = {x["id"] for k in ("outcomes", "normative_items", "success_criteria", "verification_subjects")
               for x in ctx[k]}
        if ids & set(changed):
            linked.add(art["locator"]["exact_path"])
    return linked


def test_accepted_plan_change_lists_every_linked_file_and_symbol(proj):
    _with_exports(proj)
    sh("aes plan accept plans/plan-002.yaml && git add -A && git commit -q -m 'plan 2'", proj)
    listing = change_list(proj)
    assert listing["changed"] == ["NI-001", "SC-001"]
    assert {f["path"] for f in listing["files"]} == _aes_linked(proj, listing["changed"]) == {SRC, "tests/test_greet.py"}
    greet = next(f for f in listing["files"] if f["path"] == SRC)
    assert greet["items"] == ["NI-001", "SC-001"] and greet["symbols"] == [SIGNATURE]
    assert f"- {SRC} (ART-GREET): NI-001, SC-001; symbols: {SIGNATURE}" in render(listing)


def test_uncommitted_plan_change_is_compared_with_head(proj):
    sh("aes plan accept plans/plan-002.yaml", proj)
    listing = change_list(proj)
    assert listing["base"] == "HEAD" and listing["changed"] == ["NI-001", "SC-001"]


def test_no_plan_change_says_so(proj):
    sh("git commit -q --allow-empty -m nothing", proj)
    _with_exports(proj)  # a symbol, not plan text
    assert change_list(proj)["changed"] == []
    assert render(change_list(proj)).startswith("No plan text changed since commit ")


def test_the_hook_hands_the_whole_list_to_the_agent(proj, monkeypatch):
    monkeypatch.delenv("PCW_BLOCK_STALE", raising=False)
    monkeypatch.delenv("PCW_MODE", raising=False)
    _with_exports(proj)
    sh("aes plan accept plans/plan-002.yaml && git add -A && git commit -q -m 'plan 2'", proj)
    call = {"tool_name": "Edit", "tool_input": {"file_path": str(proj / SRC)}, "cwd": str(proj)}
    warned = decide(call)["hookSpecificOutput"]  # default (warn): the list rides on the warning
    assert warned["permissionDecision"] == "allow" and f"- {SRC} (ART-GREET)" in warned["additionalContext"]
    monkeypatch.setenv("PCW_MODE", "block")
    out = decide(call)["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny"
    reason = out["permissionDecisionReason"]
    assert "Plan text changed since commit " in reason and "NI-001, SC-001" in reason
    assert f"- {SRC} (ART-GREET)" in reason and "- tests/test_greet.py (ART-TEST)" in reason
