"""Tests for marked quotes of requirement text in Markdown documents, read by the trace check."""

from pathlib import Path
import subprocess

import pytest

from lockstep.checks.trace import check
from lockstep_checks_support import SPEC, write, repo  # noqa: F401  (fixture)

IMPL = '''
    """Core module.

    Implements: core/do-the-thing
    """
'''
TEST = '''
    import pytest

    @pytest.mark.req("core/it-works")
    def test_it():
        assert True
'''
DOC = """
    # Notes

    The rule: <!-- lockstep quote: {id} -->{passage}<!-- /lockstep quote --> and more.
"""


def git(root: Path, *args: str) -> None:
    """Run git in root."""
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


@pytest.fixture
def traced(repo: Path) -> Path:
    """The example repository with an implementer and a test, so trace has nothing else to report."""
    write(repo, "src/pkg/core.py", IMPL)
    write(repo, "tests/test_x.py", TEST)
    return repo


def quote_findings(root: Path) -> list[tuple[str, str, str]]:
    """Return (kind, ID, where) of every trace finding."""
    return [(f.kind, f.id, f.where) for f in check(root)]


def quotes_read(root: Path) -> list[tuple[str, str, int, str]]:
    """Return (path, ID, line, state) of every marked quote the quotes reader finds."""
    from lockstep.checks import quotes

    return [(q.path, q.id, q.line, q.state) for q in quotes.check(root)]


@pytest.mark.req("lockstep-checks/trace-a-quote-that-matches-passes")
def test_a_quote_that_matches_passes(traced):
    write(traced, "docs/notes.md", DOC.format(id="core/do-the-thing", passage="tool   SHALL\ndo the thing"))
    git(traced, "init", "-q")
    git(traced, "add", "-A")
    assert quote_findings(traced) == []
    assert quotes_read(traced) == [("docs/notes.md", "core/do-the-thing", 3, "current")]


@pytest.mark.req("lockstep-checks/trace-a-quote-left-behind-by-a-changed-requirement-fails")
def test_a_quote_left_behind_by_a_changed_requirement_fails(traced, capsys):
    from lockstep.checks.cli import run

    write(traced, "docs/notes.md", DOC.format(id="core/do-the-thing", passage="SHALL do the thing"))
    write(traced, "docs/untracked.md", DOC.format(id="core/nothing", passage="x"))
    git(traced, "init", "-q")
    git(traced, "add", "docs/notes.md", "src", "tests", "openspec")
    write(traced, "openspec/specs/core/spec.md", SPEC.replace("SHALL do the thing.", "SHALL do the other thing."))
    assert quote_findings(traced) == [("stale-quote", "core/do-the-thing", "docs/notes.md:3")]
    assert run(["trace", "--repo", str(traced)]) == 1
    out = capsys.readouterr().out
    assert "stale-quote" in out and "docs/notes.md:3" in out
    assert out.strip().splitlines()[-1] == "RESULT trace findings=1 exit=1"


@pytest.mark.req("lockstep-checks/trace-a-quote-of-a-scenario-s-text-passes")
def test_a_quote_of_a_scenarios_text_passes(traced):
    write(traced, "docs/notes.md", DOC.format(id="core/do-the-thing", passage="- **THEN** it works"))
    assert quote_findings(traced) == []
    assert quotes_read(traced) == [("docs/notes.md", "core/do-the-thing", 3, "current")]


@pytest.mark.req("lockstep-checks/trace-a-quote-of-an-unknown-requirement-fails")
def test_a_quote_of_an_unknown_requirement_fails(traced, capsys):
    from lockstep.checks.cli import run

    write(traced, "docs/notes.md", DOC.format(id="core/no-such-thing", passage="SHALL do the thing"))
    assert quote_findings(traced) == [("unknown", "core/no-such-thing", "docs/notes.md:3")]
    assert run(["trace", "--repo", str(traced)]) == 1
    assert capsys.readouterr().out.strip().endswith("exit=1")


@pytest.mark.req("lockstep-checks/trace-a-quote-matching-an-active-change-s-text-passes")
def test_a_quote_matching_an_active_changes_text_passes(traced):
    write(traced, "openspec/changes/reword/specs/core/spec.md", """
        ## MODIFIED Requirements
        ### Requirement: Do the thing
        The tool SHALL do the thing quickly.

        #### Scenario: It works
        - **THEN** it works
    """)
    write(traced, "docs/notes.md", DOC.format(id="core/do-the-thing", passage="do the thing quickly"))
    assert quote_findings(traced) == []
    assert quotes_read(traced) == [("docs/notes.md", "core/do-the-thing", 3, "current")]


@pytest.mark.req("lockstep-checks/trace-a-start-marker-with-no-end-marker-fails")
def test_a_start_marker_with_no_end_marker_fails(traced, capsys):
    from lockstep.checks.cli import run

    write(traced, "docs/notes.md", "# Notes\n\nText.\n<!-- lockstep quote: core/do-the-thing -->SHALL do the thing\n")
    write(traced, ".hidden/skip.md", DOC.format(id="core/nothing", passage="x"))
    write(traced, "openspec/notes.md", DOC.format(id="core/nothing", passage="x"))
    assert quote_findings(traced) == [("unclosed-quote", "core/do-the-thing", "docs/notes.md:4")]
    assert run(["trace", "--repo", str(traced)]) == 1
    out = capsys.readouterr().out
    assert "unclosed-quote" in out and out.strip().endswith("exit=1")
