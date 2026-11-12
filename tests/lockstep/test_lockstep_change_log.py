"""Behavior 4.2: every normative change has one entry in an append-only change log."""

from datetime import UTC, datetime, timedelta

import pytest
import yaml
from agentic_engineering_system.planning import accept_proposal

from lockstep_support import REPO, sh
from lockstep.change_log import entries, history_problems, main, render
from lockstep.hook import decide
from lockstep.wiki import pages
from lockstep.wiki_reach import reach_problems

HEAD = """\
schema_version: aes.v0_2.proposal.probe0
proposal_id: {pid}
title: {title}
rationale: a normative change made by the test.
closes_gaps: []
trace_review:
  runs_traced_work: false
  reason: plain Python, judged by its tests.
target_delta:
  change:
"""
PURPOSE = """\
    planned_artifacts:
      - id: ART-GREET
        locator: {exact_path: src/greeter/__init__.py}
        kind: source
        purpose: the greet function, which greets by name
        semantic_justification_refs: [NI-001]
"""
STATEMENT = """\
    normative_items:
      - id: NI-001
        kind: behavior
        outcome_refs: [OUT-001]
        statement: greet(name) returns "Hello, <name>!" for any name it is given.
"""


def _accept(proj, tmp_path, pid, title, body, minutes):
    """Accept one proposal at a stated time (so two accepts in one second keep their order), then commit."""
    path = tmp_path / f"{pid}.yaml"
    path.write_text(HEAD.format(pid=pid, title=title) + body)
    accept_proposal(proj, path, now=datetime.now(UTC) + timedelta(minutes=minutes))
    sh(f"git add -A && git commit -q -m 'plan: {pid}'", proj)


def test_two_normative_changes_add_two_entries_and_leave_earlier_ones_unchanged(proj, tmp_path):
    before = entries(proj)
    assert [e["id"] for e in before] == ["PLAN-001-GREET"]
    _accept(proj, tmp_path, "PLAN-101-PURPOSE", "Say what greet is for", PURPOSE, 1)
    after_one = entries(proj)
    _accept(proj, tmp_path, "DOCSTRING-ART-GREET-1", "greet's statement, edited in its docstring", STATEMENT, 2)
    after_two = entries(proj)

    assert len(after_one) == len(before) + 1 and len(after_two) == len(before) + 2
    assert after_two[:len(after_one)] == after_one  # earlier entries unchanged
    one, two = after_two[-2:]
    assert (one["id"], one["origin"], one["changes"]) == ("PLAN-101-PURPOSE", "plan", ["change planned_artifacts ART-GREET"])
    assert (two["id"], two["origin"], two["changes"]) == (
        "DOCSTRING-ART-GREET-1", "docstring", ["change normative_items NI-001"])
    assert two["record"] == ".aes/plans/DOCSTRING-ART-GREET-1.yaml"
    assert history_problems(proj) == []


def test_an_edited_or_removed_entry_is_reported(proj, capsys):
    rec = ".aes/plans/PLAN-001-GREET.yaml"
    path = proj / rec
    path.write_text(path.read_text().replace("title: Greet by name", "title: Greet anyone", 1))
    rule = "an entry is written once by `aes plan accept` and never changed afterwards. Restore it from git."
    assert history_problems(proj) == [f"the working tree edits the log entry {rec}; {rule}"]

    sh("git commit -qam 'retitle'", proj)
    edited = sh("git rev-parse HEAD", proj).strip()[:12]
    sh(f"git rm -q {rec} && git commit -qm 'drop'", proj)
    dropped = sh("git rev-parse HEAD", proj).strip()[:12]
    assert history_problems(proj) == [f"commit {edited} (retitle) edits the log entry {rec}; {rule}",
                                      f"commit {dropped} (drop) removes the log entry {rec}; {rule}"]
    assert main(["--root", str(proj)]) == 1
    assert capsys.readouterr().out.splitlines()[-1] == "change_log: entries=0 commits=4 problems=2"


def test_a_plan_change_with_no_entry_is_reported(proj):
    t = yaml.safe_load((proj / ".aes/target.yaml").read_text())
    t["planned_artifacts"][0]["purpose"] = "changed by hand"
    (proj / ".aes/target.yaml").write_text(yaml.safe_dump(t, sort_keys=False))
    rule = ("changes the plan (.aes/target.yaml) without adding a log entry under .aes/plans/: make the change a "
            "proposal and accept it with `aes plan accept`.")
    assert history_problems(proj) == [f"the working tree {rule}"]
    sh("git commit -qam 'by hand'", proj)
    rev = sh("git rev-parse HEAD", proj).strip()[:12]
    assert history_problems(proj) == [f"commit {rev} (by hand) {rule}"]


def test_the_wiki_shows_the_log_newest_first(proj, tmp_path):
    _accept(proj, tmp_path, "DOCSTRING-ART-GREET-1", "greet's statement, edited in its docstring", STATEMENT, 1)
    page = render(entries(proj))
    lines = [line for line in page.splitlines() if line.startswith("- **")]
    assert len(lines) == 2 and "`DOCSTRING-ART-GREET-1` (from a docstring" in lines[0]
    assert "`PLAN-001-GREET` (from the plan" in lines[1] and lines[1].endswith(
        "Greet by name. It added behavior NI-001, success criterion SC-001, component CMP-GREETER, "
        "planned files ART-GREET and ART-TEST, and test VS-GREET.")  # plain words, not the plan's field names
    wiki = pages(proj, "greeter")
    assert wiki["change-log.md"] == page
    assert "- [Change log](change-log.md) — every accepted change to the plan, newest first (2 entries)" in wiki["index.md"]
    assert reach_problems(wiki) == []


def test_the_page_shows_the_agent_call_line_of_an_entry_that_ends_with_one(proj, tmp_path):
    call = "Agent call: confidence=high; significant=no; decision=accept; reason=a small change."
    path = tmp_path / "DOCSTRING-ART-GREET-2.yaml"
    path.write_text((HEAD.format(pid="DOCSTRING-ART-GREET-2", title="with a call") + STATEMENT).replace(
        "rationale: a normative change made by the test.", f"rationale: >-\n  Why it changed.\n  {call}"))
    accept_proposal(proj, path, now=datetime.now(UTC) + timedelta(minutes=1))
    log = entries(proj)
    assert [e["agent_call"] for e in log] == [None, call]
    lines = render(log).splitlines()
    at = next(i for i, line in enumerate(lines) if "`DOCSTRING-ART-GREET-2`" in line)
    assert lines[at + 1] == f"  - {call}"
    assert "Agent call" not in "\n".join(lines[at + 2:])  # the entry without a call adds nothing


def _hook(proj, tool, tool_input):
    out = decide({"tool_name": tool, "tool_input": tool_input, "cwd": str(proj)})
    return out and out["hookSpecificOutput"]


def test_the_edit_hook_refuses_any_write_to_a_log_entry_and_allows_reading_one(proj):
    rec = proj / ".aes/plans/PLAN-001-GREET.yaml"
    before = rec.read_text()
    for tool, tool_input in [("Edit", {"file_path": str(rec), "old_string": "Greet", "new_string": "Hi"}),
                             ("Write", {"file_path": str(rec), "content": "x"}),
                             ("Write", {"file_path": str(proj / ".aes/plans/PLAN-999-FORGED.yaml"), "content": "x"}),
                             ("Bash", {"command": "rm .aes/plans/PLAN-001-GREET.yaml"}),
                             ("Bash", {"command": f"git rm -q {rec}"}),
                             ("Bash", {"command": "echo x > ./.aes/plans/PLAN-001-GREET.yaml"}),
                             ("Bash", {"command": "sed -i s/Greet/Hi/ .aes/plans/PLAN-001-GREET.yaml"}),
                             ("Bash", {"command": "rm -rf .aes"})]:
        out = _hook(proj, tool, tool_input)
        assert out["permissionDecision"] == "deny", (tool, tool_input)
        assert "written once, automatically, by `aes plan accept`" in out["permissionDecisionReason"]
    assert rec.read_text() == before
    for command in ["cat .aes/plans/PLAN-001-GREET.yaml",
                    "git add .aes/plans/PLAN-001-GREET.yaml && git commit -qm 'the hook refuses rm of an entry'",
                    "uv run aes plan accept plans/DOCSTRING-ART-GREET-1.yaml"]:
        assert _hook(proj, "Bash", {"command": command}) is None, command
    assert _hook(proj, "Write", {"file_path": str(proj / "plans/DOCSTRING-ART-GREET-1.yaml"), "content": "x"}) is None
