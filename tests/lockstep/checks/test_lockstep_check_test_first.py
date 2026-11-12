"""Tests for the test-first check, run on real throwaway git repositories."""

import subprocess

import pytest

from lockstep.checks.test_first import check
from lockstep_checks_support import SPEC, write, repo  # noqa: F401  (fixture)

NEW_SPEC = SPEC + """
    #### Scenario: It also greets
    - **WHEN** greeted
    - **THEN** it says hello
"""


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def commit_all(repo, msg):
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", msg)


def make_base(repo):
    git(repo, "init", "-q", "-b", "main")
    write(repo, "src/pkg/__init__.py", "")
    write(repo, "src/pkg/core.py", 'def greet():\n    return "hello"\n')
    commit_all(repo, "base")


@pytest.mark.req("lockstep-checks/test-first-configured-test-folders-run-against-the-base-source")
def test_configured_test_root_runs_current_tests_against_base_source(repo):
    make_base(repo)
    write(repo, "pyproject.toml", '[tool.lockstep]\ntests = ["unused", "checks"]\n')
    write(repo, "openspec/specs/core/spec.md", NEW_SPEC)
    write(repo, "checks/test_greet.py", GREET_TEST.format(expected="hello"))
    commit_all(repo, "scenario under configured tests")
    result = check(repo, base="HEAD~1")
    assert result.checked == ["checks/test_greet.py::test_greets"]
    assert result.passed_before == ["checks/test_greet.py::test_greets"]
    assert not result.ok


GREET_TEST = '''
    import pytest
    from pkg.core import greet

    @pytest.mark.req("core/it-also-greets")
    def test_greets():
        assert greet() == "{expected}"
'''


@pytest.mark.req("lockstep-checks/test-first-test-that-already-passed-is-reported")
def test_test_that_already_passed_is_reported(repo):
    make_base(repo)
    write(repo, "openspec/specs/core/spec.md", NEW_SPEC)
    write(repo, "tests/test_greet.py", GREET_TEST.format(expected="hello"))
    commit_all(repo, "add scenario")
    result = check(repo, base="HEAD~1")
    assert result.passed_before == ["tests/test_greet.py::test_greets"]
    assert not result.ok


@pytest.mark.req("lockstep-checks/test-first-test-that-failed-before-passes-the-check")
def test_test_that_failed_before_passes_the_check(repo):
    make_base(repo)
    write(repo, "openspec/specs/core/spec.md", NEW_SPEC)
    write(repo, "src/pkg/core.py", 'def greet():\n    return "hello there"\n')
    write(repo, "tests/test_greet.py", GREET_TEST.format(expected="hello there"))
    commit_all(repo, "add scenario")
    result = check(repo, base="HEAD~1")
    assert result.ok
    assert result.checked == ["tests/test_greet.py::test_greets"]


@pytest.mark.req("lockstep-checks/test-first-new-repository-without-a-base-passes-with-a-skip-notice")
def test_new_repository_without_a_base_passes_with_a_skip_notice(repo):
    make_base(repo)
    result = check(repo, base="origin/main")
    assert result.ok
    assert result.skipped == "base origin/main not found"
    assert result.checked == []


@pytest.mark.req("lockstep-checks/test-first-existing-behavior-test-is-skipped-and-counted")
def test_existing_behavior_test_is_skipped_and_counted(repo):
    make_base(repo)
    write(repo, "openspec/specs/core/spec.md", NEW_SPEC)
    test = GREET_TEST.format(expected="hello").replace('"core/it-also-greets")', '"core/it-also-greets", existing=True)')
    write(repo, "tests/test_greet.py", test)
    commit_all(repo, "add scenario")
    result = check(repo, base="HEAD~1")
    assert result.ok
    assert result.existing == ["tests/test_greet.py::test_greets"]
    assert result.checked == []


CHANGE_SPEC = """
    ## ADDED Requirements
    ### Requirement: Greet twice
    The tool SHALL greet.

    #### Scenario: It also greets
    - **WHEN** greeted
    - **THEN** it says hello
"""


@pytest.mark.req("lockstep-checks/test-first-a-scenario-in-an-active-change-is-checked")
def test_a_scenario_in_an_active_change_is_checked(repo):
    make_base(repo)
    write(repo, "openspec/changes/more/specs/core/spec.md", CHANGE_SPEC)
    write(repo, "tests/test_greet.py", GREET_TEST.format(expected="hello"))
    commit_all(repo, "add scenario in a change")
    result = check(repo, base="HEAD~1")
    assert result.passed_before == ["tests/test_greet.py::test_greets"]
    assert not result.ok


@pytest.mark.req("lockstep-checks/test-first-archiving-a-change-makes-no-scenario-new")
def test_archiving_a_change_makes_no_scenario_new(repo):
    make_base(repo)
    write(repo, "openspec/changes/more/specs/core/spec.md", CHANGE_SPEC)
    write(repo, "tests/test_greet.py", GREET_TEST.format(expected="hello"))
    commit_all(repo, "add scenario in a change")
    (repo / "openspec/changes/archive").mkdir(parents=True)
    git(repo, "mv", "openspec/changes/more", "openspec/changes/archive/2026-10-26-more")
    write(repo, "openspec/specs/core/spec.md", NEW_SPEC)
    commit_all(repo, "archive the change")
    result = check(repo, base="HEAD~1")
    assert result.ok
    assert result.checked == []
