"""Tests for the sources check."""

import json

import pytest

from lockstep.checks.cli import run as run_check
from lockstep.checks.sources import check
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)

LABELED = """
    # core Specification

    ## Purpose
    Example.

    ## Requirements
    ### Requirement: Do the thing
    The tool SHALL do the thing.

    Source: Brian, 2026-10-15: "do the thing"

    #### Scenario: It works
    - **WHEN** called
    - **THEN** it works

    ### Requirement: Guess
    The tool SHALL guess.

    Source: inferred by agent (seemed useful)

    #### Scenario: It guesses
    - **WHEN** called
    - **THEN** it guesses
"""


@pytest.mark.req("lockstep-checks/sources-requirement-without-source-fails")
def test_requirement_without_source_fails(repo, capsys):
    items = check(repo)
    assert [(i.id, i.source) for i in items] == [("core/do-the-thing", "missing")]
    assert run_check(["sources", "--repo", str(repo)]) == 1
    assert "exit=1" in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/sources-decision-without-source-fails")
def test_decision_without_source_fails(repo):
    write(repo, "openspec/specs/core/spec.md", LABELED)
    write(repo, "docs/decisions/0001-x.md", "# 0001 X\n\n- Status: accepted\n")
    missing = [i.id for i in check(repo) if i.source == "missing"]
    assert missing == ["decision/0001-x"]


@pytest.mark.req("lockstep-checks/sources-labeled-items-pass-and-are-classified")
def test_labeled_items_pass_and_are_classified(repo, capsys):
    write(repo, "openspec/specs/core/spec.md", LABELED)
    write(repo, "docs/decisions/0001-x.md", '# 0001 X\n\n- Decider: Brian ("yes", 2026-10-15)\n')
    assert run_check(["sources", "--repo", str(repo), "--json"]) == 0
    out = capsys.readouterr().out
    data = json.loads(out[: out.rindex("RESULT")])
    by_id = {d["id"]: d["source"] for d in data}
    assert by_id == {"core/do-the-thing": "brian", "core/guess": "inferred", "decision/0001-x": "brian"}
    assert {d["id"]: d["statement"] for d in data}["core/guess"] == "The tool SHALL guess."
