"""Prove the layout wiki: pages per capability, stale check, no pages without the switch, unplanned exemption, python -m lockstep.wiki.

[[[cog import lockstep.cogtext as c; c.docstring("tests:lockstep:test_lockstep_layout_wiki.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/a-layout-repository-generates-one-wiki-page-per-capability, lockstep-plan-format/project-check-fails-on-stale-or-unreachable-wiki-pages, lockstep-plan-format/generated-wiki-pages-need-no-layout-row, lockstep-plan-format/python-m-lockstep-wiki-prints-the-layout-wiki

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


@pytest.mark.req("lockstep-plan-format/a-capability-page-shows-requirement-code-and-tests")
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


@pytest.mark.req("lockstep-plan-format/a-repository-without-the-switch-gets-no-pages")
def test_repository_without_the_switch_gets_no_pages(repo):
    layout_repo(repo, switch=False)
    assert not (repo / "generated").exists()


@pytest.mark.req("lockstep-plan-format/a-capability-page-shows-requirement-code-and-tests")
def test_page_of_a_removed_capability_is_removed(repo):
    layout_repo(repo)
    write(repo, "openspec/specs/other/spec.md", "## Purpose\nOther.\n\n## Requirements\n### Requirement: Go\nIt SHALL go.\n\n#### Scenario: Goes\n- **THEN** go\n")
    project(repo)
    assert (repo / "generated/wiki/other.md").is_file()
    (repo / "openspec/specs/other/spec.md").unlink()
    assert "generated/wiki/other.md" in project(repo, check=True)
    project(repo)
    assert not (repo / "generated/wiki/other.md").exists()


@pytest.mark.req("lockstep-plan-format/a-stale-page-fails-the-check")
def test_stale_page_fails_the_check_and_writes_nothing(repo):
    layout_repo(repo)
    write(repo, "tests/test_more.py", TEST.replace("test_works", "test_more"))
    before = (repo / "generated/wiki/core.md").read_text()
    assert "generated/wiki/core.md" in project(repo, check=True)
    assert (repo / "generated/wiki/core.md").read_text() == before


@pytest.mark.req("lockstep-plan-format/a-stale-page-fails-the-check")
def test_link_without_summary_is_reported(repo, monkeypatch):
    from lockstep import layout_wiki

    layout_repo(repo)
    assert wiki_problems(repo) == []
    monkeypatch.setattr(layout_wiki, "_summary", lambda *a: "")
    assert any("no summary" in p for p in wiki_problems(repo))


@pytest.mark.req("lockstep-plan-format/a-generated-page-is-not-unplanned")
def test_generated_page_is_not_unplanned(repo):
    layout_repo(repo)
    assert unplanned_reason(repo, "generated/wiki/core.md") is None
    assert unplanned_reason(repo, "generated/other.md") is not None


@pytest.mark.req("lockstep-plan-format/the-wiki-command-works-in-a-layout-repository")
def test_python_m_wiki_prints_the_pages_in_a_layout_repository(repo):
    layout_repo(repo)
    done = subprocess.run([sys.executable, "-m", "lockstep.wiki"], cwd=repo, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert "===== generated/wiki/index.md" in done.stdout and "The tool SHALL do the thing." in done.stdout
    reach = subprocess.run([sys.executable, "-m", "lockstep.wiki_reach"], cwd=repo, capture_output=True, text=True)
    assert reach.returncode == 0 and "problems=0" in reach.stdout


@pytest.mark.req("lockstep-plan-format/a-capability-page-shows-requirement-code-and-tests")
def test_old_page_is_kept_when_writing_fails(repo, monkeypatch):
    layout_repo(repo)
    write(repo, "openspec/specs/other/spec.md", "## Purpose\nOther.\n\n## Requirements\n### Requirement: Go\nIt SHALL go.\n\n#### Scenario: Goes\n- **THEN** go\n")
    project(repo)
    (repo / "openspec/specs/other/spec.md").unlink()
    import lockstep.checks.project as proj

    def fail(*args, **kwargs):
        raise RuntimeError("render failed")
    monkeypatch.setattr(proj, "project_facts", fail)
    with pytest.raises(RuntimeError):
        project(repo)
    assert (repo / "generated/wiki/other.md").is_file()


@pytest.mark.req("lockstep-plan-format/a-capability-page-shows-requirement-code-and-tests")
def test_capability_named_index_is_refused(repo):
    layout_repo(repo)
    write(repo, "openspec/specs/index/spec.md", "## Purpose\nIdx.\n\n## Requirements\n### Requirement: Go\nIt SHALL go.\n\n#### Scenario: Goes\n- **THEN** go\n")
    with pytest.raises(ValueError, match="named `index`"):
        project(repo)


@pytest.mark.req("lockstep-plan-format/a-repository-without-the-switch-gets-no-pages")
def test_switch_that_is_not_a_boolean_is_refused(repo):
    layout_repo(repo, switch=False)
    plan = yaml.safe_load((repo / "lockstep.yaml").read_text())
    plan["generated_wiki"] = "true"
    write(repo, "lockstep.yaml", yaml.safe_dump(plan))
    with pytest.raises(ValueError, match="true or false"):
        project(repo)


TWO_TESTS = '''
    import pytest

    @pytest.mark.req("core/it-works")
    def test_works():
        assert True

    @pytest.mark.req("core/it-fails")
    def test_fails():
        assert False
'''
TWO_SCENARIOS = SPEC + "\n#### Scenario: It fails\n- **THEN** it fails\n"
JUNIT = ('<testsuites><testsuite><testcase classname="tests.test_mod" name="test_works"/>'
         '<testcase classname="tests.test_mod" name="test_fails"><failure message="x"/></testcase></testsuite></testsuites>')


def git(repo: Path, *args: str) -> str:
    """Run git in repo and return its output; fail the test if git fails."""
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def results_repo(repo: Path, ignore: bool = True) -> Path:
    """A committed layout repository with a passing and a failing scenario, a plan closing the failing one, and results at HEAD."""
    write(repo, "openspec/specs/core/spec.md", TWO_SCENARIOS)
    layout_repo(repo)
    write(repo, "tests/test_mod.py", TWO_TESTS)
    write(repo, "docs/plans/fix.md", "# Fix\n\nCloses: core/it-fails\n")
    write(repo, ".gitignore", ".code2check/\n" + ("generated/wiki/results.md\n" if ignore else ""))
    project(repo)
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    write(repo, ".code2check/junit.xml", JUNIT)
    write(repo, ".code2check/run.json", '{"commit": "%s", "clean": true}' % git(repo, "rev-parse", "HEAD"))
    return repo


@pytest.mark.req("lockstep-plan-format/results-at-this-commit-show-on-the-page")
def test_results_at_this_commit_show_on_the_page(repo):
    results_repo(repo)
    project(repo)
    page = (repo / "generated/wiki/results.md").read_text()
    head = git(repo, "rev-parse", "HEAD")[:12]
    assert head in page
    assert "`core/it-works` | passing" in page and "`core/it-fails` | failing" in page
    assert "docs/plans/fix.md" in page and "`core/it-fails`: failing" in page
    assert "`generated/wiki/results.md`" in (repo / "generated/wiki/index.md").read_text()
    assert "(results.md)" not in (repo / "generated/wiki/index.md").read_text()


@pytest.mark.req("lockstep-plan-format/results-from-another-commit-are-not-used")
def test_results_from_another_commit_are_not_used(repo):
    results_repo(repo)
    write(repo, ".code2check/run.json", '{"commit": "0123456789abcdef", "clean": true}')
    project(repo)
    page = (repo / "generated/wiki/results.md").read_text()
    assert "0123456789ab" in page
    assert "`core/it-works` | not run at this revision" in page


@pytest.mark.req("lockstep-plan-format/the-page-is-build-output")
def test_results_page_is_build_output(repo):
    results_repo(repo)
    project(repo)
    write(repo, ".code2check/junit.xml", JUNIT.replace('<failure message="x"/>', ""))
    assert "generated/wiki/results.md" not in project(repo, check=True)
    project(repo)
    assert (repo / "generated/wiki/results.md").is_file()


@pytest.mark.req("lockstep-plan-format/the-page-is-build-output")
def test_results_page_not_written_unless_ignored(repo):
    results_repo(repo, ignore=False)
    project(repo)
    assert not (repo / "generated/wiki/results.md").exists()
