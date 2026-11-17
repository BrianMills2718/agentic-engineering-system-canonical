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


@pytest.mark.req("lockstep-checks/test-first-pytest-that-cannot-run-fails-loudly")
def test_pytest_that_cannot_run_fails_loudly(repo, monkeypatch):
    make_base(repo)
    write(repo, "openspec/specs/core/spec.md", NEW_SPEC)
    write(repo, "tests/test_greet.py", GREET_TEST.format(expected="hello"))
    commit_all(repo, "new scenario")
    import lockstep.checks.test_first as tf
    monkeypatch.setattr(tf.sys, "executable", "/nonexistent/python")
    with pytest.raises(tf.PytestUnavailable, match="pytest could not run"):
        check(repo, base="HEAD~1")


@pytest.mark.req("lockstep-checks/test-first-pytest-that-cannot-run-fails-loudly")
def test_the_cli_exits_non_zero_when_pytest_cannot_run(repo, monkeypatch, capsys):
    make_base(repo)
    write(repo, "openspec/specs/core/spec.md", NEW_SPEC)
    write(repo, "tests/test_greet.py", GREET_TEST.format(expected="hello"))
    commit_all(repo, "new scenario")
    import lockstep.checks.test_first as tf
    from lockstep.checks.cli import run as run_check
    monkeypatch.setattr(tf.sys, "executable", "/nonexistent/python")
    code = run_check(["test-first", "--base", "HEAD~1", "--repo", str(repo)])
    out = capsys.readouterr().out
    assert code == 1 and "pytest could not run" in out and "accepted" not in out


CHANGED_SPEC = SPEC.replace("- **THEN** it works", "- **THEN** it says hello there")
WORKS_TEST = '''
    import pytest
    from pkg.core import greet

    @pytest.mark.req("core/it-works"{flag})
    def test_{name}():
        assert greet() == "{expected}"
'''


def make_base_with_test(repo, flag=""):
    """A base commit whose scenario core/it-works has one test that passes on the base source."""
    make_base(repo)
    write(repo, "tests/test_works.py", WORKS_TEST.format(flag=flag, name="works", expected="hello"))
    commit_all(repo, "base test")


@pytest.mark.req("lockstep-checks/test-first-a-changed-scenario-whose-tests-all-pass-on-the-base-fails-the-check")
def test_a_changed_scenario_whose_tests_all_pass_on_the_base_fails_the_check(repo):
    make_base_with_test(repo)
    write(repo, "openspec/specs/core/spec.md", CHANGED_SPEC)
    commit_all(repo, "reword the scenario")
    result = check(repo, base="HEAD~1")
    assert result.changed == ["core/it-works"]
    assert result.no_failing_test == ["core/it-works"]
    assert result.passed_before == []
    assert not result.ok


@pytest.mark.req("lockstep-checks/test-first-one-test-that-fails-on-the-base-is-enough-for-a-changed-scenario")
def test_one_test_that_fails_on_the_base_is_enough_for_a_changed_scenario(repo):
    make_base_with_test(repo)
    write(repo, "openspec/specs/core/spec.md", CHANGED_SPEC)
    write(repo, "src/pkg/core.py", 'def greet():\n    return "hello there"\n')
    write(repo, "tests/test_works.py", WORKS_TEST.format(flag="", name="works", expected="hello there") + """
    @pytest.mark.req("core/it-works")
    def test_still_starts_with_hello():
        assert greet().startswith("hello")
""")
    commit_all(repo, "reword the scenario and change the code")
    result = check(repo, base="HEAD~1")
    assert result.changed == ["core/it-works"]
    assert result.no_failing_test == []
    assert result.ok


@pytest.mark.req("lockstep-checks/test-first-a-wording-only-scenario-is-not-checked")
def test_a_wording_only_scenario_is_not_checked(repo):
    make_base_with_test(repo)
    write(repo, "openspec/specs/core/spec.md", CHANGED_SPEC)
    write(repo, "docs/plans/0001-reword.md", "# Reword\n\nWording-only: core/do-the-thing\n")
    commit_all(repo, "reword the scenario, wording only")
    result = check(repo, base="HEAD~1")
    assert result.changed == []
    assert result.no_failing_test == []
    assert result.ok


@pytest.mark.req("lockstep-checks/test-first-an-existing-behavior-mark-does-not-exempt-a-changed-scenario")
def test_an_existing_behavior_mark_does_not_exempt_a_changed_scenario(repo, capsys):
    make_base_with_test(repo, flag=", existing=True")
    write(repo, "openspec/specs/core/spec.md", CHANGED_SPEC)
    commit_all(repo, "reword the scenario")
    result = check(repo, base="HEAD~1")
    assert result.changed == ["core/it-works"]
    assert result.no_failing_test == ["core/it-works"]
    assert result.existing == []
    assert not result.ok
    from lockstep.checks.cli import run as run_check
    assert run_check(["test-first", "--base", "HEAD~1", "--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "no-failing-test core/it-works" in out
    assert "RESULT test-first checked=0 existing=0 passed_before=0 changed=1 no_failing_test=1 exit=1" in out


@pytest.mark.req(
    "lockstep-checks/test-first-a-scenario-reworded-on-the-base-branch-after-the-branch-started-is-not-checked"
)
def test_a_scenario_reworded_on_the_base_branch_after_the_branch_started_is_not_checked(repo):
    make_base_with_test(repo)
    git(repo, "checkout", "-q", "-b", "work")
    write(repo, "README.md", "work\n")
    commit_all(repo, "work that changes no scenario")
    git(repo, "checkout", "-q", "main")
    write(repo, "openspec/specs/core/spec.md", CHANGED_SPEC)
    commit_all(repo, "main moved: the scenario reworded after the branch started")
    git(repo, "checkout", "-q", "work")
    result = check(repo, base="main")
    assert result.changed == []
    assert result.no_failing_test == []
    assert result.ok


SKIPPED_TEST = '''
    import pytest
    from pkg.core import greet

    @pytest.mark.req("core/it-works")
    @pytest.mark.skipif(greet() == "hello", reason="not for the old greeting")
    def test_works():
        assert greet() == "hello there"
'''


@pytest.mark.req("lockstep-checks/test-first-a-changed-scenario-whose-tests-all-pass-on-the-base-fails-the-check")
def test_a_test_skipped_on_the_base_is_not_a_failing_test(repo):
    make_base_with_test(repo)
    write(repo, "openspec/specs/core/spec.md", CHANGED_SPEC)
    write(repo, "src/pkg/core.py", 'def greet():\n    return "hello there"\n')
    write(repo, "tests/test_works.py", SKIPPED_TEST)
    commit_all(repo, "reword the scenario; its only test is skipped on the base source")
    result = check(repo, base="HEAD~1")
    assert result.changed == ["core/it-works"]
    assert result.no_failing_test == ["core/it-works"]
    assert not result.ok
