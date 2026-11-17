"""Tests for the changed check: requirements whose text differs from a base revision, run on throwaway git repositories."""

import json
from pathlib import Path
import subprocess

import pytest

from lockstep.checks.cli import run
from lockstep_checks_support import SPEC, write, repo  # noqa: F401  (fixture)

IMPL = '''
    """Core module."""


    def run():
        """Run the thing.

        Implements: core/do-the-thing
        """
'''
TEST = '''
    import pytest

    @pytest.mark.req("core/it-works")
    def test_works():
        assert {value}
'''
REWORDED = SPEC.replace("The tool SHALL do the thing.", "The tool SHALL do the other thing.")
SCENARIO_CHANGED = SPEC.replace("- **THEN** it works", "- **THEN** it works twice")
DELTA = """
    ## MODIFIED Requirements
    ### Requirement: Do the thing
    The tool SHALL do the thing {how}.

    #### Scenario: It works
    - **WHEN** called
    - **THEN** it works{then}
"""


def git(root: Path, *args: str) -> str:
    """Run git in root and return its output."""
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit_all(root: Path, msg: str = "x") -> None:
    """Commit everything in root, creating the repository on first use."""
    if not (root / ".git").exists():
        git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", msg)


@pytest.fixture
def base(repo: Path) -> Path:
    """The example repository with an implementer and a marked test, committed as the base."""
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, "tests/test_mod.py", TEST.format(value="True"))
    commit_all(repo, "base")
    return repo


def changed(root: Path, *extra: str, base: str = "HEAD", stdout_only: bool = False) -> tuple[int, str]:
    """Run `lockstep check changed` against base; return its exit status and output (stdout, then stderr)."""
    import contextlib
    import io

    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = run(["changed", "--base", base, "--repo", str(root), *extra])
    return code, out.getvalue() if stdout_only else out.getvalue() + err.getvalue()


def last(text: str) -> str:
    """Return the last non-empty line."""
    return [line for line in text.splitlines() if line.strip()][-1]


@pytest.mark.req("lockstep-checks/changed-a-reworded-requirement-is-listed-with-its-implementer-and-tests")
def test_a_reworded_requirement_is_listed_with_its_implementer_and_tests(base):
    write(base, "openspec/specs/core/spec.md", REWORDED)
    code, out = changed(base)
    assert "changed       core/do-the-thing" in out
    assert "pkg.mod.run" in out
    assert "tests/test_mod.py::test_works (unchanged)" in out
    code, out = changed(base, "--json", stdout_only=True)
    data = json.loads(out.split("\nRESULT")[0])
    assert last(out).startswith("RESULT changed requirements=1 ")
    [req] = data["requirements"]
    assert req["id"] == "core/do-the-thing" and req["kind"] == "changed"
    assert req["implementers"] == ["pkg.mod.run"]
    assert req["tests"] == [{"node": "tests/test_mod.py::test_works", "scenario": "core/it-works", "label": "unchanged"}]


@pytest.mark.req("lockstep-checks/changed-re-wrapped-text-is-not-a-change")
def test_re_wrapped_text_is_not_a_change(base):
    write(base, "openspec/specs/core/spec.md", SPEC.replace("The tool SHALL do the thing.", "The tool   SHALL\n    do the thing."))
    code, out = changed(base)
    assert code == 0
    assert last(out) == "RESULT changed requirements=0 unplanned=0 no_scenario=0 wording_only=0 exit=0"


@pytest.mark.req("lockstep-checks/changed-a-changed-scenario-marks-its-requirement-changed")
def test_a_changed_scenario_marks_its_requirement_changed(base):
    write(base, "openspec/specs/core/spec.md", SCENARIO_CHANGED)
    code, out = changed(base)
    assert "changed       core/do-the-thing" in out
    assert "scenario core/it-works (changed)" in out
    assert "statement" not in out.split("differs", 1)[1].splitlines()[0]


@pytest.mark.req("lockstep-checks/changed-text-in-an-active-change-counts-before-it-is-archived")
def test_text_in_an_active_change_counts_before_it_is_archived(base):
    write(base, "openspec/changes/reword/specs/core/spec.md", DELTA.format(how="better", then=" twice"))
    write(base, "openspec/changes/reword/proposal.md", "## Why\n\nBecause.\n")
    code, out = changed(base)
    assert "changed       core/do-the-thing" in out
    assert "plan        openspec/changes/reword" in out
    assert "unplanned" not in out.replace("unplanned=0", "")
    assert code == 0, out


@pytest.mark.req("lockstep-checks/changed-a-test-edited-since-the-base-is-labelled-changed")
def test_a_test_edited_since_the_base_is_labelled_changed(base):
    write(base, "openspec/specs/core/spec.md", REWORDED)
    write(base, "tests/test_mod.py", TEST.format(value="1 == 1"))
    code, out = changed(base)
    assert "tests/test_mod.py::test_works (changed)" in out


@pytest.mark.req("lockstep-checks/changed-a-spec-edited-with-no-plan-is-unplanned")
def test_a_spec_edited_with_no_plan_is_unplanned(base):
    write(base, "openspec/specs/core/spec.md", REWORDED)
    code, out = changed(base)
    assert code == 1
    assert "unplanned     core/do-the-thing" in out
    assert "plan        none" in out
    assert "unplanned=1" in last(out) and last(out).endswith("exit=1")


@pytest.mark.req("lockstep-checks/changed-an-archived-change-in-the-same-change-set-is-its-plan")
def test_an_archived_change_in_the_same_change_set_is_its_plan(base):
    write(base, "openspec/specs/core/spec.md", SCENARIO_CHANGED.replace("do the thing.", "do the thing better."))
    write(base, "openspec/changes/archive/2026-11-17-reword/specs/core/spec.md", DELTA.format(how="better", then=" twice"))
    write(base, "openspec/changes/archive/2026-11-17-reword/proposal.md", "## Why\n\nBecause.\n")
    code, out = changed(base)
    assert "plan        openspec/changes/archive/2026-11-17-reword" in out
    assert "unplanned     " not in out
    assert code == 0, out


@pytest.mark.req("lockstep-checks/changed-a-plan-page-that-was-not-touched-does-not-count")
def test_a_plan_page_that_was_not_touched_does_not_count(repo):
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, "tests/test_mod.py", TEST.format(value="True"))
    write(repo, "docs/plans/0001-x.md", "# Plan\n\nCloses: core/do-the-thing\n")
    commit_all(repo, "base")
    write(repo, "openspec/specs/core/spec.md", SCENARIO_CHANGED.replace("do the thing.", "do the thing better."))
    code, out = changed(repo)
    assert "unplanned     core/do-the-thing" in out
    assert code == 1


@pytest.mark.req("lockstep-checks/changed-a-statement-changed-with-no-scenario-changed-fails")
def test_a_statement_changed_with_no_scenario_changed_fails(base):
    write(base, "openspec/changes/reword/specs/core/spec.md", DELTA.format(how="better", then=""))
    write(base, "openspec/changes/reword/proposal.md", "## Why\n\nBecause.\n")
    code, out = changed(base)
    assert "no-scenario-changed  core/do-the-thing" in out
    assert "unplanned     " not in out
    assert code == 1
    assert "no_scenario=1" in last(out)


@pytest.mark.req("lockstep-checks/changed-a-wording-only-declaration-is-accepted-and-printed")
def test_a_wording_only_declaration_is_accepted_and_printed(base):
    write(base, "openspec/changes/reword/specs/core/spec.md", DELTA.format(how="better", then=""))
    write(base, "openspec/changes/reword/proposal.md", "## Why\n\nBecause.\n\nWording-only: core/do-the-thing\n")
    code, out = changed(base)
    assert code == 0, out
    assert "wording-only  core/do-the-thing  (openspec/changes/reword/proposal.md)" in out
    assert last(out) == "RESULT changed requirements=1 unplanned=0 no_scenario=0 wording_only=1 exit=0"


@pytest.mark.req("lockstep-checks/changed-nothing-changed-gives-a-zero-count-and-exit-0")
def test_nothing_changed_gives_a_zero_count_and_exit_0(base):
    write(base, "README.md", "unrelated\n")
    code, out = changed(base)
    assert code == 0
    assert last(out) == "RESULT changed requirements=0 unplanned=0 no_scenario=0 wording_only=0 exit=0"


@pytest.mark.req("lockstep-checks/changed-a-missing-base-is-reported-not-crashed")
def test_a_missing_base_is_reported_not_crashed(base):
    write(base, "openspec/specs/core/spec.md", REWORDED)
    code, out = changed(base, base="origin/main")
    assert code == 0
    assert last(out) == 'RESULT changed skipped="base origin/main not found" exit=0'


@pytest.mark.req("lockstep-checks/changed-mode-off-skips-the-check")
def test_mode_off_skips_the_check(base):
    write(base, "openspec/specs/core/spec.md", REWORDED)
    write(base, "lockstep.yaml", "checks:\n  changed: off\n")
    code, out = changed(base)
    assert code == 0
    assert "skipped (off)" in out


@pytest.mark.req("lockstep-checks/changed-a-missing-base-is-reported-not-crashed")
def test_the_lockstep_entry_point_routes_changed_to_the_commit_check(base, monkeypatch, capsys):
    from lockstep.check import cli

    monkeypatch.setattr("sys.argv", ["lockstep", "check", "changed", "--base", "nope", "--repo", str(base)])
    assert cli() == 0
    assert 'RESULT changed skipped="base nope not found" exit=0' in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/changed-a-reworded-requirement-is-listed-with-its-implementer-and-tests")
def test_the_working_tree_is_not_touched(base):
    write(base, "openspec/specs/core/spec.md", REWORDED)
    before = git(base, "status", "--porcelain")
    code, out = changed(base)
    assert last(out).startswith("RESULT changed requirements=1 ")
    assert git(base, "status", "--porcelain") == before


@pytest.mark.req("lockstep-checks/changed-a-requirement-added-on-the-base-branch-after-the-branch-started-is-not-listed")
def test_a_requirement_added_on_the_base_branch_after_the_branch_started_is_not_listed(base):
    git(base, "checkout", "-q", "-b", "work")
    write(base, "README.md", "work\n")
    commit_all(base, "work that changes no requirement")
    git(base, "checkout", "-q", "main")
    write(base, "openspec/specs/core/spec.md", SPEC + """
    ### Requirement: Do another thing
    The tool SHALL do another thing.

    #### Scenario: It also works
    - **WHEN** called again
    - **THEN** it works again
""")
    commit_all(base, "main moved: a requirement added after the branch started")
    git(base, "checkout", "-q", "work")
    code, out = changed(base, base="main")
    assert code == 0
    assert last(out) == "RESULT changed requirements=0 unplanned=0 no_scenario=0 wording_only=0 exit=0"
