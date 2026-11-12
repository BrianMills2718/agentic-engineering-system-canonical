"""Tests for the trace check."""

import pytest

from lockstep.checks.trace import check
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)


@pytest.mark.req("lockstep-checks/trace-configured-test-folders-feed-trace")
def test_configured_test_folders_feed_trace(repo):
    from lockstep.checks.markers import req_markers

    write(repo, "pyproject.toml", '[tool.lockstep]\nsource = ["knowledge"]\ntests = ["knowledge/tests"]\n')
    write(repo, "knowledge/core.py", IMPL)
    write(repo, "knowledge/tests/test_core.py", TEST)
    assert check(repo) == []
    assert [node for _, _, node in req_markers(repo)] == ["knowledge/tests/test_core.py::test_it"]


@pytest.mark.req("lockstep-checks/trace-overlapping-test-folders-do-not-duplicate-markers")
def test_overlapping_test_folders_do_not_duplicate_markers(repo):
    from lockstep.checks.markers import req_markers

    write(repo, "pyproject.toml", '[tool.lockstep]\ntests = ["checks", "checks/nested"]\n')
    write(repo, "checks/nested/test_core.py", TEST)
    assert len(req_markers(repo)) == 1

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


@pytest.mark.req("lockstep-checks/trace-requirement-without-implementer-fails")
def test_requirement_without_implementer_fails(repo):
    write(repo, "tests/test_x.py", TEST)
    findings = check(repo)
    assert [f.id for f in findings] == ["core/do-the-thing"]
    assert findings[0].kind == "unimplemented"


@pytest.mark.req("lockstep-checks/trace-implemented-requirement-passes")
def test_implemented_requirement_passes(repo):
    write(repo, "src/pkg/core.py", IMPL)
    write(repo, "tests/test_x.py", TEST)
    assert check(repo) == []


@pytest.mark.req("lockstep-checks/trace-scenario-without-test-fails")
def test_scenario_without_test_fails(repo):
    write(repo, "src/pkg/core.py", IMPL)
    findings = check(repo)
    assert [(f.kind, f.id) for f in findings] == [("untested", "core/it-works")]


@pytest.mark.req("lockstep-checks/trace-stale-marker-fails")
def test_stale_marker_fails(repo):
    write(repo, "src/pkg/core.py", IMPL)
    write(repo, "tests/test_x.py", TEST + '''
    @pytest.mark.req("core/renamed-away")
    def test_old():
        pass
    ''')
    findings = check(repo)
    assert [(f.kind, f.id) for f in findings] == [("unknown", "core/renamed-away")]
    assert findings[0].where.endswith("tests/test_x.py:7")


@pytest.mark.req("lockstep-checks/trace-implemented-requirement-passes")
def test_implements_line_may_wrap(repo):
    write(repo, "openspec/specs/extra/spec.md", "## Requirements\n### Requirement: Second one\nThe tool SHALL.\n")
    write(repo, "src/pkg/core.py", '''
        """Core module.

        Implements: core/do-the-thing,
            extra/second-one
        """
    ''')
    write(repo, "tests/test_x.py", TEST)
    assert check(repo) == []


@pytest.mark.req("lockstep-checks/trace-test-written-for-an-active-change-passes-trace")
def test_test_written_for_an_active_change_passes_trace(repo):
    write(repo, "src/pkg/core.py", IMPL)
    write(repo, "tests/test_x.py", TEST)
    write(repo, "openspec/changes/more/specs/core/spec.md", """
        ## ADDED Requirements
        ### Requirement: Also do it
        The tool SHALL also do it.

        #### Scenario: It also works
        - **WHEN** called
        - **THEN** it also works
    """)
    write(repo, "tests/test_more.py", TEST.replace("core/it-works", "core/it-also-works"))
    assert check(repo) == []


@pytest.mark.req("lockstep-checks/trace-implementer-outside-src-is-found")
def test_implementer_outside_src_is_found(repo):
    write(repo, "pyproject.toml", '[tool.lockstep]\nsource = ["scripts"]\n')
    write(repo, "scripts/tool.py", IMPL)
    write(repo, "tests/test_x.py", TEST)
    assert check(repo) == []
