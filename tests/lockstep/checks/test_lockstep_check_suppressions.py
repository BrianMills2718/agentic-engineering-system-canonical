"""Tests for the suppressions check: an added `# noqa`, `# type: ignore` or import-linter ignore names its reason."""

from pathlib import Path
import subprocess

import pytest

from lockstep.checks.cli import run


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


@pytest.fixture
def base_repo(tmp_path: Path) -> Path:
    """A repository on branch main with one Python file and an import-linter file committed."""
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "t")
    (tmp_path / "mod.py").write_text("import os  # noqa: F401\nx = 1\n")
    (tmp_path / ".importlinter").write_text(
        "[importlinter]\nroot_package = pkg\n\n[importlinter:contract:one]\nname = one\ntype = layers\n"
        "layers =\n    pkg.a\n    pkg.b\nignore_imports =\n    # the old entry has a reason\n    pkg.a -> pkg.b\n"
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")
    _git(tmp_path, "checkout", "-q", "-b", "work")
    return tmp_path


def _check(root: Path, capsys: pytest.CaptureFixture[str], base: str = "main") -> tuple[int, str]:
    status = run(["suppressions", "--repo", str(root), "--base", base])
    return status, capsys.readouterr().out


@pytest.mark.req("lockstep-checks/suppressions-an-added-noqa-with-no-reason-fails")
def test_added_noqa_without_reason_fails(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (base_repo / "new.py").write_text("import sys  # noqa: F401\n")
    _git(base_repo, "add", "new.py")
    status, out = _check(base_repo, capsys)
    assert status == 1
    assert "unreasoned new.py:1 # noqa" in out
    assert "RESULT suppressions added=1 reasoned=0 unreasoned=1 exit=1" in out


@pytest.mark.req("lockstep-checks/suppressions-a-reason-after-the-directive-passes")
def test_reason_after_directive_passes(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (base_repo / "mod.py").write_text(
        "import os  # noqa: F401\nx = 1\n"
        "import sys  # noqa: F401  # re-exported for the plugin loader\n"
        "y = f()  # type: ignore[no-untyped-call]  # vendored stub has no types\n"
    )
    status, out = _check(base_repo, capsys)
    assert status == 0, out
    assert "RESULT suppressions added=2 reasoned=2 unreasoned=0 exit=0" in out


@pytest.mark.req("lockstep-checks/suppressions-a-reason-after-the-directive-passes")
def test_short_reason_and_other_directives_fail(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (base_repo / "mod.py").write_text(
        "import os  # noqa: F401\nx = 1\n"
        "a = 1  # type: ignore  # why\n"
        "b = 2  # pyright: ignore[reportGeneralTypeIssues]\n"
        "c = 3  # pylint: disable=invalid-name\n"
    )
    status, out = _check(base_repo, capsys)
    assert status == 1
    for line in ("mod.py:3 # type: ignore", "mod.py:4 # pyright: ignore", "mod.py:5 # pylint: disable"):
        assert f"unreasoned {line}" in out
    assert "unreasoned=3" in out


@pytest.mark.req("lockstep-checks/suppressions-a-reason-after-the-directive-passes")
def test_directive_inside_a_string_is_not_a_suppression(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (base_repo / "mod.py").write_text('import os  # noqa: F401\nx = 1\ntext = "a  # noqa: F401"\n')
    status, out = _check(base_repo, capsys)
    assert status == 0, out
    assert "added=0" in out


@pytest.mark.req("lockstep-checks/suppressions-a-suppression-already-at-the-base-is-not-judged")
def test_existing_suppression_not_judged(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (base_repo / "mod.py").write_text("import os  # noqa: F401\nx = 2\n")
    _git(base_repo, "commit", "-qam", "change x")
    status, out = _check(base_repo, capsys)
    assert status == 0, out
    assert "RESULT suppressions added=0 reasoned=0 unreasoned=0 exit=0" in out


@pytest.mark.req("lockstep-checks/suppressions-an-ini-ignore-needs-a-comment-line-above-it")
def test_ini_ignore_needs_comment_above(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = base_repo / ".importlinter"
    path.write_text(path.read_text() + "    # the CLI wires the adapter in\n    pkg.cli -> pkg.adapter\n    pkg.b -> pkg.a\n")
    status, out = _check(base_repo, capsys)
    assert status == 1
    assert "unreasoned .importlinter:15 ignore_imports" in out
    assert ".importlinter:14" not in out
    assert "RESULT suppressions added=2 reasoned=1 unreasoned=1 exit=1" in out


@pytest.mark.req("lockstep-checks/suppressions-an-ini-ignore-needs-a-comment-line-above-it")
def test_pyproject_ignore_needs_same_line_comment(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (base_repo / "pyproject.toml").write_text(
        "[tool.importlinter]\nroot_package = 'pkg'\n\n[[tool.importlinter.contracts]]\nname = 'one'\n"
        "type = 'forbidden'\nignore_imports = [\n"
        "    'pkg.cli -> pkg.adapter',  # the CLI wires the adapter in\n"
        "    'pkg.b -> pkg.a',\n]\n"
    )
    _git(base_repo, "add", "pyproject.toml")
    status, out = _check(base_repo, capsys)
    assert status == 1
    assert "unreasoned pyproject.toml:9 ignore_imports" in out
    assert "added=2 reasoned=1 unreasoned=1" in out


@pytest.mark.req("lockstep-checks/suppressions-an-added-noqa-with-no-reason-fails")
def test_path_with_space_and_nested_config_are_read(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (base_repo / "my file.py").write_text("import sys  # noqa: F401\nz = 1  # noqa_style is not a directive\n")
    nested = base_repo / "sub" / ".importlinter"
    nested.parent.mkdir()
    nested.write_text("[importlinter:contract:one]\nname = one\nignore_imports =\n    pkg.a -> pkg.b\n")
    _git(base_repo, "add", "-A")
    status, out = _check(base_repo, capsys)
    assert status == 1
    assert "unreasoned my file.py:1 # noqa" in out
    assert "unreasoned sub/.importlinter:4 ignore_imports" in out
    assert "added=2 reasoned=0 unreasoned=2" in out


@pytest.mark.req("lockstep-checks/suppressions-an-ini-ignore-needs-a-comment-line-above-it")
def test_ini_unindented_and_semicolon_comments(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = base_repo / ".importlinter"
    path.write_text(path.read_text() + "# the CLI wires the adapter in\n    pkg.c -> pkg.d\n"
                    "    ; kept for the old loader\n    pkg.e -> pkg.f\n    pkg.g -> pkg.h\n")
    status, out = _check(base_repo, capsys)
    assert status == 1
    assert "unreasoned .importlinter:17 ignore_imports" in out
    assert "added=3 reasoned=2 unreasoned=1" in out


@pytest.mark.req("lockstep-checks/suppressions-a-base-that-names-no-commit-skips")
def test_missing_base_skips(base_repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    status, out = _check(base_repo, capsys, base="nope")
    assert status == 0
    assert 'RESULT suppressions skipped="base nope not found" exit=0' in out
