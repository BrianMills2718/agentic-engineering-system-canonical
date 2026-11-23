"""Tests for how the spec reader takes a requirement's statement text."""

import pytest

from lockstep.checks.spec import read_plan
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)

SOURCE_FIRST = """
    # core Specification

    ## Requirements
    ### Requirement: Do the thing
    Source: Brian, 2026-11-23, an example
    source line that wraps.

    The tool SHALL do the thing.

    #### Scenario: It works
    - **WHEN** called
"""


@pytest.mark.req("lockstep-checks/trace-a-quote-that-matches-passes")
def test_a_statement_after_its_source_line_is_still_the_statement(repo):
    write(repo, "openspec/specs/core/spec.md", SOURCE_FIRST)
    assert read_plan(repo).text["core/do-the-thing"] == "The tool SHALL do the thing."


@pytest.mark.req("lockstep-checks/trace-a-quote-that-matches-passes")
def test_a_statement_before_its_source_line_is_unchanged(repo):
    assert read_plan(repo).text["core/do-the-thing"] == "The tool SHALL do the thing."


@pytest.mark.req("lockstep-checks/trace-a-quote-that-matches-passes")
def test_notes_after_the_source_line_of_a_stated_requirement_are_not_the_statement(repo):
    write(repo, "openspec/specs/core/spec.md", """
        ## Requirements
        ### Requirement: Do the thing
        The tool SHALL do the thing.

        Source: Brian, 2026-11-23.

        Part two: inferred by agent.

        #### Scenario: It works
    """)
    assert read_plan(repo).text["core/do-the-thing"] == "The tool SHALL do the thing."
