"""Prove the layout wiki: pages per capability, stale check, no pages without the switch, unplanned exemption, python -m lockstep.wiki.

[[[cog import lockstep.cogtext as c; c.docstring("tests:lockstep:test_lockstep_layout_wiki.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-wiki/a-layout-repository-generates-one-wiki-page-per-capability, lockstep-wiki/project-check-fails-on-stale-or-unreachable-wiki-pages, lockstep-wiki/generated-wiki-pages-need-no-layout-row, lockstep-wiki/python-m-lockstep-wiki-prints-the-layout-wiki

### Requirement: A layout repository generates one wiki page per capability

In a layout repository whose `lockstep.yaml` says `generated_wiki: true`, `lockstep check project` SHALL write `generated/wiki/index.md`, with one line per OpenSpec capability (its summary and a link to its page), and `generated/wiki/<capability>.md` for each capability. A capability page SHALL list each requirement's text, the symbols whose docstrings implement it with their `file:line`, each scenario with the tests tagged with its ID, and the requirement's coverage state (unimplemented, untested, or implemented and tested). The pages SHALL hold no commit hash and no pass or fail result, so they are the same in every checkout; `lockstep status` gives pass or fail. A page for a capability that no longer exists SHALL be removed.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting. The `generated_wiki` switch, the coverage-only status and the page layout are inferred by agent.

#### Scenario: A capability page shows requirement, code and tests

- **GIVEN** a layout repository with `generated_wiki: true`, a requirement implemented by a function and a scenario with a tagged test
- **WHEN** `lockstep check project` runs
- **THEN** `generated/wiki/index.md` has one line for the capability and its page shows the requirement text, the function with its file and line, and the test

#### Scenario: A repository without the switch gets no pages

- **GIVEN** a layout repository without `generated_wiki`
- **WHEN** `lockstep check project` runs
- **THEN** no `generated/wiki/` folder is written

### Requirement: Project check fails on stale or unreachable wiki pages

`lockstep check project --check` SHALL name each `generated/wiki/` page that differs from what would be written, and SHALL exit 1. It SHALL also report each generated page that is more than two links from the index or whose link has no summary beside it, and exit 1.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting. Reusing the existing reachability rule inferred by agent.

#### Scenario: A stale page fails the check

- **GIVEN** committed generated pages and a test added after
- **WHEN** `lockstep check project --check` runs
- **THEN** it names the capability page and exits 1, and it writes nothing

### Requirement: Generated wiki pages need no layout row

A file under `generated/wiki/` SHALL NOT be reported as unplanned in a layout repository, and the Markdown file cap SHALL NOT count it.

Source: Brian, 2026-11-17, "skip generated" (the cap); the layout-row exemption inferred by agent, since the pages change with the specs.

#### Scenario: A generated page is not unplanned

- **GIVEN** a layout repository governing `.` and a file `generated/wiki/index.md` with no layout row
- **WHEN** the whole-tree rule judges it
- **THEN** it is not reported as unplanned, and a file `generated/other.md` with no row still is

### Requirement: Python m lockstep wiki prints the layout wiki

`python -m lockstep.wiki` in a layout repository SHALL print the generated wiki pages as plain text and exit 0, and `python -m lockstep.wiki_reach` there SHALL check them, instead of failing for want of `.aes/project.yaml`.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting.

#### Scenario: The wiki command works in a layout repository

- **GIVEN** a layout repository with no `.aes/` folder
- **WHEN** `python -m lockstep.wiki` runs
- **THEN** it prints the index and each capability page and exits 0
[[[end]]] (sum: Pe1lv+4tEX)
"""

from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from lockstep.checks.project import project, wiki_problems
from lockstep.unplanned_files import unplanned_reason
import textwrap

SPEC = "## Purpose\nExample.\n\n## Requirements\n### Requirement: Do the thing\nThe tool SHALL do the thing.\n\n#### Scenario: It works\n- **THEN** it works\n"


def write(root: Path, rel: str, text: str) -> Path:
    """Write dedented text to a file under root, creating parent folders."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip())
    return path


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository with one spec and nothing else."""
    write(tmp_path, "openspec/specs/core/spec.md", SPEC)
    (tmp_path / "src/pkg").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    return tmp_path

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


def layout_repo(repo: Path, switch: bool = True) -> Path:
    """The example repository as a layout repository holding an implementer and a test, with or without the switch."""
    plan = {"schema": "lockstep.side.v1", "governed": ["."], "layout": [
        {"path": "src/pkg/mod.py", "purpose": "the module", "implements": ["core/do-the-thing"], "tests": []}]}
    if switch:
        plan["generated_wiki"] = True
    write(repo, "lockstep.yaml", yaml.safe_dump(plan))
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, "tests/test_mod.py", TEST)
    project(repo)
    project(repo)
    return repo


@pytest.mark.req("lockstep-wiki/a-capability-page-shows-requirement-code-and-tests")
def test_capability_page_shows_requirement_code_and_tests(repo):
    layout_repo(repo)
    index = (repo / "generated/wiki/index.md").read_text()
    assert "- [core](core.md) — Example." in index
    page = (repo / "generated/wiki/core.md").read_text()
    assert "The tool SHALL do the thing." in page
    assert "`pkg.mod.run` — [`src/pkg/mod.py:" in page
    assert "(../../src/pkg/mod.py#L" in page
    assert "tested by `tests/test_mod.py::test_works`" in page
    assert "Status: **implemented and tested**" in page
    assert project(repo, check=True) == []


@pytest.mark.req("lockstep-wiki/a-repository-without-the-switch-gets-no-pages")
def test_repository_without_the_switch_gets_no_pages(repo):
    layout_repo(repo, switch=False)
    assert not (repo / "generated").exists()


@pytest.mark.req("lockstep-wiki/a-capability-page-shows-requirement-code-and-tests")
def test_page_of_a_removed_capability_is_removed(repo):
    layout_repo(repo)
    write(repo, "openspec/specs/other/spec.md", "## Purpose\nOther.\n\n## Requirements\n### Requirement: Go\nIt SHALL go.\n\n#### Scenario: Goes\n- **THEN** go\n")
    project(repo)
    assert (repo / "generated/wiki/other.md").is_file()
    (repo / "openspec/specs/other/spec.md").unlink()
    assert "generated/wiki/other.md" in project(repo, check=True)
    project(repo)
    assert not (repo / "generated/wiki/other.md").exists()


@pytest.mark.req("lockstep-wiki/a-stale-page-fails-the-check")
def test_stale_page_fails_the_check_and_writes_nothing(repo):
    layout_repo(repo)
    write(repo, "tests/test_more.py", TEST.replace("test_works", "test_more"))
    before = (repo / "generated/wiki/core.md").read_text()
    assert "generated/wiki/core.md" in project(repo, check=True)
    assert (repo / "generated/wiki/core.md").read_text() == before


@pytest.mark.req("lockstep-wiki/a-stale-page-fails-the-check")
def test_link_without_summary_is_reported(repo, monkeypatch):
    from lockstep import layout_wiki

    layout_repo(repo)
    assert wiki_problems(repo) == []
    monkeypatch.setattr(layout_wiki, "_summary", lambda *a: "")
    assert any("no summary" in p for p in wiki_problems(repo))


@pytest.mark.req("lockstep-wiki/a-generated-page-is-not-unplanned")
def test_generated_page_is_not_unplanned(repo):
    layout_repo(repo)
    assert unplanned_reason(repo, "generated/wiki/core.md") is None
    assert unplanned_reason(repo, "generated/other.md") is not None


@pytest.mark.req("lockstep-wiki/the-wiki-command-works-in-a-layout-repository")
def test_python_m_wiki_prints_the_pages_in_a_layout_repository(repo):
    layout_repo(repo)
    done = subprocess.run([sys.executable, "-m", "lockstep.wiki"], cwd=repo, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert "===== generated/wiki/index.md" in done.stdout and "The tool SHALL do the thing." in done.stdout
    reach = subprocess.run([sys.executable, "-m", "lockstep.wiki_reach"], cwd=repo, capture_output=True, text=True)
    assert reach.returncode == 0 and "problems=0" in reach.stdout
