"""Tests for the status report."""

import json
from pathlib import Path
import subprocess

import pytest

from lockstep.checks.status import report
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)

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
        assert True
'''


def junit(outcome: str = "pass") -> str:
    """A JUnit file in which tests/test_mod.py::test_works has the given outcome."""
    child = {"pass": "", "fail": '<failure message="boom"/>', "skip": '<skipped message="later"/>'}[outcome]
    return (
        '<?xml version="1.0" encoding="utf-8"?><testsuites><testsuite name="pytest">'
        f'<testcase classname="tests.test_mod" name="test_works" time="0.01">{child}</testcase>'
        "</testsuite></testsuites>"
    )


def git(root: Path, *args: str) -> str:
    """Run git in root and return its output."""
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit_all(root: Path) -> str:
    """Commit everything in root and return the new commit sha."""
    if not (root / ".git").exists():
        git(root, "init", "-q")
        git(root, "config", "user.email", "t@example.com")
        git(root, "config", "user.name", "t")
        write(root, ".gitignore", ".code2check/\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "x")
    return git(root, "rev-parse", "HEAD")


def record(root: Path, commit: str, outcome: str = "pass", clean: bool = True) -> None:
    """Write the test results and the run record `make check` would leave."""
    write(root, ".code2check/junit.xml", junit(outcome))
    write(root, ".code2check/run.json", json.dumps({"commit": commit, "clean": clean}))


@pytest.fixture
def linked(repo: Path) -> Path:
    """The example repository with an implementer and a test, committed."""
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, "tests/test_mod.py", TEST)
    return repo


@pytest.mark.req("lockstep-projection/status-lists-implementers-and-tests")
def test_status_lists_implementers_and_tests(linked):
    commit_all(linked)
    result = report(linked)
    req = result.requirements["core/do-the-thing"]
    assert req.links == ["pkg.mod.run"]
    assert result.scenarios["core/it-works"].links == ["tests/test_mod.py::test_works"]
    assert result.scenarios["core/it-works"].requirement == "core/do-the-thing"


@pytest.mark.req("lockstep-projection/status-lists-implementers-and-tests")
def test_unlinked_items_say_so(repo):
    commit_all(repo)
    result = report(repo)
    assert result.requirements["core/do-the-thing"].state == "unimplemented"
    assert result.scenarios["core/it-works"].state == "untested"


@pytest.mark.req("lockstep-projection/results-from-this-revision-set-pass-and-fail")
def test_results_from_this_revision_set_pass_and_fail(linked):
    sha = commit_all(linked)
    record(linked, sha, "pass")
    result = report(linked)
    assert result.results_valid
    assert result.scenarios["core/it-works"].state == "passing"
    assert result.requirements["core/do-the-thing"].state == "passing"
    record(linked, sha, "fail")
    result = report(linked)
    assert result.scenarios["core/it-works"].state == "failing"
    assert result.requirements["core/do-the-thing"].state == "failing"


@pytest.mark.req("lockstep-projection/results-from-this-revision-set-pass-and-fail")
def test_skipped_test_is_not_passing(linked):
    sha = commit_all(linked)
    record(linked, sha, "skip")
    assert report(linked).scenarios["core/it-works"].state == "skipped"


@pytest.mark.req("lockstep-projection/results-from-another-revision-are-not-used")
def test_results_from_another_revision_are_not_used(linked):
    old = commit_all(linked)
    write(linked, "README.md", "changed\n")
    commit_all(linked)
    record(linked, old, "pass")
    result = report(linked)
    assert not result.results_valid
    assert result.scenarios["core/it-works"].state == "not run at this revision"
    assert result.counts()["not_run"] == 1


@pytest.mark.req("lockstep-projection/results-from-another-revision-are-not-used")
def test_results_from_a_dirty_tree_are_not_used(linked):
    sha = commit_all(linked)
    record(linked, sha, "pass", clean=False)
    assert report(linked).scenarios["core/it-works"].state == "not run at this revision"


@pytest.mark.req("lockstep-projection/results-from-another-revision-are-not-used")
def test_uncommitted_edit_after_the_run_voids_results(linked):
    sha = commit_all(linked)
    record(linked, sha, "pass")
    write(linked, "src/pkg/other.py", "X = 1\n")
    assert report(linked).scenarios["core/it-works"].state == "not run at this revision"


@pytest.mark.req("lockstep-projection/open-ids-of-a-plan-are-listed")
def test_open_ids_of_a_plan_are_listed(linked):
    write(linked, "docs/plans/0001-x.md", "# Plan\n\nCloses: core/do-the-thing,\n    core/no-such-id\n\nText.\n")
    sha = commit_all(linked)
    record(linked, sha, "fail")
    plans = report(linked).plans
    assert [p.path for p in plans] == ["docs/plans/0001-x.md"]
    assert plans[0].closes == ["core/do-the-thing", "core/no-such-id"]
    assert plans[0].open == {"core/do-the-thing": "failing", "core/no-such-id": "unknown"}


@pytest.mark.req("lockstep-projection/open-ids-of-a-plan-are-listed")
def test_a_plan_with_passing_ids_has_none_open(linked):
    write(linked, "openspec/changes/next/proposal.md", "## Why\n\nCloses: core/do-the-thing, core/it-works\n")
    sha = commit_all(linked)
    record(linked, sha, "pass")
    plans = report(linked).plans
    assert [p.path for p in plans] == ["openspec/changes/next/proposal.md"]
    assert plans[0].open == {}


@pytest.mark.req("lockstep-projection/open-ids-of-a-plan-are-listed")
def test_an_archived_change_drops_out_and_its_ids_still_resolve(linked):
    write(linked, "openspec/changes/archive/2026-10-01-old/proposal.md", "Closes: core/do-the-thing\n")
    write(linked, "docs/plans/0002-y.md", "Closes: core/do-the-thing\n")
    sha = commit_all(linked)
    record(linked, sha, "pass")
    plans = report(linked).plans
    assert [p.path for p in plans] == ["docs/plans/0002-y.md"]
    assert plans[0].open == {}


@pytest.mark.req("lockstep-projection/status-lists-implementers-and-tests")
def test_requirements_of_a_change_in_progress_are_listed(linked):
    write(linked, "openspec/changes/next/specs/extra/spec.md", "## ADDED Requirements\n### Requirement: New one\nThe tool SHALL.\n\n#### Scenario: New works\n- **THEN** ok\n")
    commit_all(linked)
    result = report(linked)
    assert result.requirements["extra/new-one"].where == "openspec/changes/next/specs/extra/spec.md"
    assert result.scenarios["extra/new-works"].requirement == "extra/new-one"


@pytest.mark.req("lockstep-projection/status-lists-implementers-and-tests")
def test_cli_prints_table_json_and_result_line(linked, capsys):
    from lockstep.checks.cli import run_status

    write(linked, "docs/plans/0001-x.md", "Closes: core/do-the-thing\n")
    sha = commit_all(linked)
    record(linked, sha, "pass")
    assert run_status(["--repo", str(linked)]) == 0
    out = capsys.readouterr().out
    assert "core/do-the-thing" in out and "pkg.mod.run" in out and "tests/test_mod.py::test_works" in out
    assert "RESULT status requirements=1 passing=1 scenarios=1 scenarios_passing=1 not_run=0 plans=1 open=0 exit=0" in out
    assert run_status(["--repo", str(linked), "--json"]) == 0
    data = json.loads(capsys.readouterr().out.split("\nRESULT")[0])
    assert data["requirements"]["core/do-the-thing"]["state"] == "passing"
    assert data["results"]["valid"] is True
    assert data["plans"][0]["open"] == {}
