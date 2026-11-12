"""Tests for `lockstep show`."""

from pathlib import Path

import pytest

from lockstep.checks.cli import run_show
from lockstep.checks.show import show
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)

IMPL = '''
    """Core module."""


    def run():
        """Run the thing.

        Implements: core/do-the-thing
        """


    def other():
        """Not linked."""
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


@pytest.mark.req("lockstep-projection/show-lists-a-file-s-requirements")
def test_show_lists_a_file_s_requirements(linked):
    text = show(linked, linked / "src/pkg/mod.py")
    assert "core/do-the-thing" in text
    assert "The tool SHALL do the thing." in text
    assert "pkg.mod.run" in text
    assert "core/it-works" in text and "tests/test_mod.py::test_works" in text
    assert "not run at this revision" in text


@pytest.mark.req("lockstep-projection/show-lists-a-file-s-requirements")
def test_show_says_when_a_file_implements_nothing(linked):
    write(linked, "src/pkg/plain.py", '"""Nothing linked."""\n')
    assert show(linked, linked / "src/pkg/plain.py") == ""
    assert show(linked, "src/pkg/plain.py") == ""


@pytest.mark.req("lockstep-projection/show-lists-a-file-s-requirements")
def test_cli_show(linked, capsys):
    assert run_show(["--repo", str(linked), "src/pkg/mod.py"]) == 0
    out = capsys.readouterr().out
    assert "core/do-the-thing" in out
    assert "RESULT show requirements=1 exit=0" in out
    write(linked, "src/pkg/plain.py", '"""Nothing linked."""\n')
    assert run_show(["--repo", str(linked), "src/pkg/plain.py"]) == 0
    assert "implements no requirement" in capsys.readouterr().out
