"""Tests for the generated link file `docs/links.json` (spec lockstep-projection)."""

import json
from pathlib import Path

import pytest

from lockstep.checks.project import project
from lockstep.checks.status import LINKS_FILE
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


@pytest.mark.req("lockstep-projection/the-link-file-lists-the-whole-chain")
def test_the_link_file_lists_the_whole_chain(repo: Path):
    write(repo, "docs/index.md", "# Docs\n")
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, "tests/test_mod.py", TEST)
    assert "docs/links.json" in project(repo)
    data = json.loads((repo / LINKS_FILE).read_text())
    assert data["version"] == 1
    nodes = {n["id"]: n for n in data["nodes"]}
    assert {n["type"] for n in nodes.values()} == {"capability", "requirement", "scenario", "test", "symbol", "file"}
    assert "core/do-the-thing" in nodes["core"]["links"]
    requirement = nodes["core/do-the-thing"]
    assert requirement["file"] == "openspec/specs/core/spec.md"
    assert "core/it-works" in requirement["links"] and "pkg.mod.run" in requirement["links"]
    assert "tests/test_mod.py::test_works" in nodes["core/it-works"]["links"]
    symbol = nodes["pkg.mod.run"]
    assert symbol["file"] == "src/pkg/mod.py" and symbol["line"] == 4 and symbol["links"] == ["src/pkg/mod.py"]
    test = nodes["tests/test_mod.py::test_works"]
    assert test["file"] == "tests/test_mod.py" and test["line"] == 3 and test["links"] == ["tests/test_mod.py"]
    assert nodes["src/pkg/mod.py"]["type"] == "file"
    assert project(repo, check=True) == []


def test_an_ignored_link_file_is_not_reported_stale(repo: Path):
    import subprocess
    write(repo, "docs/index.md", "# Docs\n")
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, ".gitignore", "docs/links.json\ndocs/status.md\n")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    project(repo)
    write(repo, "tests/test_mod.py", TEST)  # the chain changes; the ignored file is build output
    assert "docs/links.json" not in project(repo, check=True)


def test_one_run_gives_the_lines_after_its_own_docstring_rewrite(repo: Path):
    """The requirement text written into a docstring moves the lines below it; one run must report the new lines."""
    write(repo, "docs/index.md", "# Docs\n")
    write(repo, "src/pkg/mod.py", IMPL + '''

    def later():
        """Also do the thing.

        Implements: core/do-the-thing
        """
''')
    project(repo)
    assert project(repo, check=True) == []
    line = next(i for i, text in enumerate((repo / "src/pkg/mod.py").read_text().splitlines(), 1)
                if text.startswith("def later"))
    nodes = {n["id"]: n for n in json.loads((repo / LINKS_FILE).read_text())["nodes"]}
    assert nodes["pkg.mod.later"]["line"] == line


@pytest.mark.req("lockstep-projection/the-link-file-reads-plans-sources-and-quotes")
def test_the_link_file_reads_plans_sources_and_quotes(repo: Path):
    import subprocess
    spec = (repo / "openspec/specs/core/spec.md").read_text().replace(
        "The tool SHALL do the thing.\n", "The tool SHALL do the thing.\n\nSource: Brian, 2026-11-23: \"yes\"\n")
    (repo / "openspec/specs/core/spec.md").write_text(spec)
    write(repo, "docs/index.md", "# Docs\n\n<!-- lockstep quote: core/do-the-thing -->do the thing<!-- /lockstep quote -->\n")
    write(repo, "docs/plans/next.md", "# Next\n\nCloses: core/do-the-thing\n")
    write(repo, "openspec/changes/archive/2026-01-01-old/proposal.md", "# Old\n\nCloses: core/it-works\n")
    write(repo, "src/pkg/mod.py", IMPL)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    project(repo)
    nodes = {n["id"]: n for n in json.loads((repo / LINKS_FILE).read_text())["nodes"]}
    active, archived = nodes["docs/plans/next.md"], nodes["openspec/changes/archive/2026-01-01-old/proposal.md"]
    assert active["type"] == "plan" and active["state"] == "active" and active["links"] == ["core/do-the-thing"]
    assert archived["type"] == "plan" and archived["state"] == "archived" and archived["links"] == ["core/it-works"]
    quote = nodes["docs/index.md:3"]
    assert quote["type"] == "quote" and quote["state"] == "current" and quote["links"] == ["core/do-the-thing"]
    requirement = nodes["core/do-the-thing"]
    assert requirement["source"] == 'Brian, 2026-11-23: "yes"' and requirement["source_kind"] == "brian"
    assert project(repo, check=True) == []
