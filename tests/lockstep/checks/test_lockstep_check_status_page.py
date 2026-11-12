"""Tests for the generated docs status page."""

from pathlib import Path

import pytest

from lockstep.checks.project import project
from lockstep.checks.status import STATUS_PAGE, report
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


@pytest.fixture
def documented(repo: Path) -> Path:
    """The example repository with a docs folder, an implementer and a test."""
    write(repo, "docs/index.md", "# Docs\n")
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, "tests/test_mod.py", TEST)
    return repo


@pytest.mark.req("lockstep-projection/status-page-lists-every-requirement-with-its-coverage-state")
def test_status_page_lists_every_requirement_with_its_coverage_state(documented):
    assert "docs/status.md" in project(documented)
    page = (documented / STATUS_PAGE).read_text()
    data = report(documented, use_results=False)
    assert "| `core/do-the-thing` | not run at this revision | `pkg.mod.run` |" in page
    assert "| `core/it-works` | `core/do-the-thing` | not run at this revision | `tests/test_mod.py::test_works` |" in page
    for ident, row in {**data.requirements, **data.scenarios}.items():
        assert f"| `{ident}` |" in page and row.state in page
    assert "tests not run at this revision" in page
    assert project(documented, check=True) == []


@pytest.mark.req("lockstep-projection/stale-status-page-fails-the-check")
def test_stale_status_page_fails_the_check(documented):
    project(documented)
    write(documented, "tests/test_more.py", TEST.replace("test_works", "test_again"))
    assert project(documented, check=True) == ["docs/status.md"]
    project(documented)
    assert "`tests/test_mod.py::test_works`, `tests/test_more.py::test_again`" in (documented / STATUS_PAGE).read_text()


@pytest.mark.req("lockstep-projection/status-page-lists-every-requirement-with-its-coverage-state")
def test_no_page_without_a_docs_folder(repo):
    write(repo, "src/pkg/mod.py", IMPL)
    project(repo)
    assert not (repo / STATUS_PAGE).exists()


@pytest.mark.req("lockstep-projection/status-page-lists-every-requirement-with-its-coverage-state")
def test_cli_status_md(documented, capsys):
    from lockstep.checks.cli import run_status

    assert run_status(["--repo", str(documented), "--md"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("# Requirement status")
    assert "| `core/do-the-thing` |" in out
