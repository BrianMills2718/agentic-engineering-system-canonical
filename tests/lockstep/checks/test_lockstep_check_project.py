"""Tests for the projection of requirement text into docstrings and status into plans."""

from pathlib import Path
import ast

import pytest

from lockstep.checks.project import project
from lockstep.checks.status import report
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)


@pytest.mark.req("lockstep-projection/opening-quote-line-declarations-receive-canonical-text")
@pytest.mark.parametrize("literal", [
    '\"\"\"Implements: core/do-the-thing\n\"\"\"',
    '\"\"\"Implements: core/do-the-thing\"\"\"',
    "'Implements: core/do-the-thing'",
    'r\"\"\"Implements: core/do-the-thing\n\nA path: C:\\work\n\"\"\"',
])
def test_opening_quote_line_is_projected_without_losing_source(repo, literal):
    path = write(repo, "src/pkg/core.py", literal + "  # retained\nSENTINEL = 7\n")
    original = path.read_text()
    assert "src/pkg/core.py" in project(repo, check=True)
    assert path.read_text() == original
    project(repo)
    projected = path.read_text()
    assert "core/do-the-thing: The tool SHALL do the thing." in projected
    assert '# retained\nSENTINEL = 7\n' in projected
    assert "Implements: core/do-the-thing" in ast.get_docstring(ast.parse(projected))
    if literal.startswith("r"):
        assert "C:\\work" in ast.get_docstring(ast.parse(projected))
    assert project(repo, check=True) == []
    assert project(repo) == []


@pytest.mark.req("lockstep-projection/opening-quote-line-declarations-receive-canonical-text")
def test_inline_function_literal_keeps_unicode_prefix_and_following_statement(repo):
    path = write(repo, "src/pkg/core.py", 'def café(): "Implements: core/do-the-thing"; return 7\n')
    before = ast.parse(path.read_text()).body[0]
    project(repo)
    after = ast.parse(path.read_text()).body[0]
    assert before.name == after.name == "café"
    assert ast.dump(before.body[-1]) == ast.dump(after.body[-1])
    assert "The tool SHALL do the thing." in ast.get_docstring(after)
    assert project(repo, check=True) == []

IMPL = '''
    """Core module."""


    def run():
        """Run the thing.

        Implements: core/do-the-thing

        Returns:
            Nothing.
        """
'''
TEST = '''
    import pytest

    @pytest.mark.req("core/it-works")
    def test_works():
        assert True
'''


@pytest.fixture
def linked(repo: Path) -> Path:
    """The example repository with an implementer and a test."""
    write(repo, "src/pkg/mod.py", IMPL)
    write(repo, "tests/test_mod.py", TEST)
    return repo


def reword(root: Path, old: str, new: str) -> None:
    """Change the wording of the spec."""
    spec = root / "openspec/specs/core/spec.md"
    spec.write_text(spec.read_text().replace(old, new))


@pytest.mark.req("lockstep-projection/projection-rewrites-the-block")
def test_projection_writes_the_requirement_text_under_implements(linked):
    changed = project(linked)
    assert changed == ["src/pkg/mod.py"]
    text = (linked / "src/pkg/mod.py").read_text()
    assert "    Implements: core/do-the-thing\n\n    Requirement text (generated):\n" in text
    assert "        core/do-the-thing: The tool SHALL do the thing.\n\n    Returns:" in text
    assert project(linked, check=True) == []


@pytest.mark.req("lockstep-projection/stale-requirement-text-fails-the-check")
def test_stale_requirement_text_fails_the_check(linked):
    project(linked)
    reword(linked, "SHALL do the thing.", "SHALL do the thing twice.")
    before = (linked / "src/pkg/mod.py").read_text()
    assert project(linked, check=True) == ["src/pkg/mod.py"]
    assert (linked / "src/pkg/mod.py").read_text() == before


@pytest.mark.req("lockstep-projection/projection-rewrites-the-block")
def test_projection_rewrites_the_block(linked):
    project(linked)
    reword(linked, "SHALL do the thing.", "SHALL do the thing twice.")
    assert project(linked) == ["src/pkg/mod.py"]
    text = (linked / "src/pkg/mod.py").read_text()
    assert "core/do-the-thing: The tool SHALL do the thing twice." in text
    assert "SHALL do the thing.\n" not in text
    assert text.count("Requirement text (generated):") == 1
    assert project(linked, check=True) == []


@pytest.mark.req("lockstep-projection/projection-rewrites-the-block")
def test_module_docstring_and_long_text_wrap(repo):
    write(repo, "openspec/specs/core/spec.md", "## Requirements\n### Requirement: Do the thing\n" + "The tool SHALL do the thing " * 8 + "\nacross lines.\n\nSource: Brian\n\n#### Scenario: It works\n- **THEN** ok\n")
    write(repo, "src/pkg/core.py", '"""Core module.\n\nImplements: core/do-the-thing\n"""\n')
    project(repo)
    text = (repo / "src/pkg/core.py").read_text()
    assert "\n\nRequirement text (generated):\n    core/do-the-thing: The tool SHALL" in text
    assert "Source" not in text
    assert all(len(line) <= 100 for line in text.splitlines())
    words = " ".join(text.split("Requirement text (generated):")[1].split()).removesuffix('"""').strip()
    assert words == "core/do-the-thing: " + " ".join(("The tool SHALL do the thing " * 8 + "across lines.").split())
    assert project(repo, check=True) == []


@pytest.mark.req("lockstep-projection/plan-block-lists-coverage")
def test_plan_block_lists_coverage(linked):
    write(linked, "docs/plans/0001-x.md", "# Plan\n\nCloses: core/do-the-thing,\n    core/it-works\n\n## Goal\n\nText.\n")
    assert "docs/plans/0001-x.md" in project(linked)
    text = (linked / "docs/plans/0001-x.md").read_text()
    data = report(linked)
    assert data.requirements["core/do-the-thing"].links == ["pkg.mod.run"]
    assert data.scenarios["core/it-works"].links == ["tests/test_mod.py::test_works"]
    assert (
        "core/it-works\n\n<!-- lockstep status: generated by `lockstep check project`; do not edit -->\n\n"
        "- `core/do-the-thing`: implemented by `pkg.mod.run`; tests `tests/test_mod.py::test_works`\n"
        "- `core/it-works`: tests `tests/test_mod.py::test_works`\n\n<!-- /lockstep status -->\n\n## Goal"
    ) in text
    assert project(linked, check=True) == []


@pytest.mark.req("lockstep-projection/plan-block-lists-coverage")
def test_plan_block_goes_stale_and_is_rewritten(linked):
    write(linked, "docs/plans/0001-x.md", "Closes: core/do-the-thing\n")
    project(linked)
    write(linked, "tests/test_more.py", TEST.replace("test_works", "test_again"))
    assert project(linked, check=True) == ["docs/plans/0001-x.md", "docs/status.md"]
    project(linked)
    text = (linked / "docs/plans/0001-x.md").read_text()
    assert "tests `tests/test_mod.py::test_works`, `tests/test_more.py::test_again`" in text
    assert text.count("<!-- /lockstep status -->") == 1


@pytest.mark.req("lockstep-projection/plan-block-lists-coverage")
def test_plan_block_says_what_is_missing(repo):
    write(repo, "docs/plans/0001-x.md", "Closes: core/do-the-thing, core/gone\n")
    project(repo)
    text = (repo / "docs/plans/0001-x.md").read_text()
    assert "- `core/do-the-thing`: not implemented; no tests" in text
    assert "- `core/gone`: unknown ID" in text


@pytest.mark.req("lockstep-projection/stale-requirement-text-fails-the-check")
def test_cli_check_exits_1_when_stale(linked, capsys):
    from lockstep.checks.cli import run

    assert run(["project", "--repo", str(linked), "--check"]) == 1
    assert "stale         src/pkg/mod.py" in capsys.readouterr().out
    assert run(["project", "--repo", str(linked)]) == 0
    assert "rewrote src/pkg/mod.py" in capsys.readouterr().out
    assert run(["project", "--repo", str(linked), "--check"]) == 0
    assert "RESULT project stale=0 exit=0" in capsys.readouterr().out


@pytest.mark.req("lockstep-projection/plan-block-lists-coverage")
def test_markers_quoted_in_plan_prose_are_left_alone(linked):
    prose = "## Steps\n\nA block between `<!-- lockstep status -->` and `<!-- /lockstep status -->`.\n\nMore text.\n"
    write(linked, "docs/plans/0001-x.md", "Closes: core/do-the-thing\n\n" + prose)
    project(linked)
    project(linked)
    text = (linked / "docs/plans/0001-x.md").read_text()
    assert text.endswith("<!-- /lockstep status -->\n\n" + prose)
    assert text.count("implemented by") == 1
