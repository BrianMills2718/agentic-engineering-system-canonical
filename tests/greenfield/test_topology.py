"""`aes topology check` on the real whygame5 target (`SC-GF-003`).

ER-SC-GF-003-01: an intentionally introduced orphan is rejected. The orphan
replayed here is the one probe 0 actually observed: setuptools wrote
`src/whygame5.egg-info/` under the governed `src/` root and it was committed.
ER-SC-GF-003-02: the unchanged planned topology is accepted.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.topology import TopologyError, check_topology

WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"

# whygame5's realized governed files at 9c9ee2a (git ls-files src tests).
REALIZED = (
    "src/whygame5/__init__.py",
    "src/whygame5/contracts.py",
    "src/whygame5/evaluator.py",
    "src/whygame5/graph.py",
    "tests/test_evaluator.py",
    "tests/test_replay.py",
)
EGG_INFO = ("src/whygame5.egg-info/PKG-INFO", "src/whygame5.egg-info/SOURCES.txt")


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
        cwd=root, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _touch(root: Path, *paths: str) -> None:
    for rel in paths:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {rel}\n", encoding="utf-8")


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """The real whygame5 .aes records plus its realized governed files, committed."""
    if not (WHYGAME5_AES / "target.yaml").is_file():
        pytest.fail(f"authentic consumer target missing: {WHYGAME5_AES / 'target.yaml'}")
    (tmp_path / ".aes").mkdir()
    shutil.copyfile(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
    _touch(tmp_path, *REALIZED, "ui/registry.yaml", "README.md")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "fixture")
    return tmp_path


def test_unchanged_planned_topology_is_accepted(project_root: Path) -> None:
    report = check_topology(project_root)
    assert report.ok
    assert report.orphans == ()
    assert set(report.governed_files) == set(REALIZED)
    # planned-but-unbuilt artifacts are reported, not failed
    assert ("ART-WG5-RUNNER", "src/whygame5/runner.py") in report.unrealized
    # pyproject.toml is planned but outside governed roots: not a topology concern
    assert all(path != "pyproject.toml" for _, path in report.unrealized)


def test_committed_egg_info_under_src_is_rejected(project_root: Path) -> None:
    _touch(project_root, *EGG_INFO)
    _git(project_root, "add", ".")
    _git(project_root, "commit", "-q", "-m", "accidentally commit build output")

    report = check_topology(project_root)
    assert not report.ok
    assert report.orphans == EGG_INFO


def test_ignored_egg_info_is_not_durable(project_root: Path) -> None:
    (project_root / ".gitignore").write_text("*.egg-info/\n", encoding="utf-8")
    _touch(project_root, *EGG_INFO)
    assert check_topology(project_root).ok


def test_staged_orphan_is_rejected_before_commit(project_root: Path) -> None:
    _touch(project_root, "src/whygame5/stray.py")
    assert check_topology(project_root).ok  # untracked: not yet durable
    _git(project_root, "add", "src/whygame5/stray.py")
    assert check_topology(project_root).orphans == ("src/whygame5/stray.py",)


def test_root_prefix_does_not_match_sibling_directory(project_root: Path) -> None:
    _touch(project_root, "srcgen/whygame5/x.py", "tests_data/fixture.json")
    _git(project_root, "add", ".")
    assert check_topology(project_root).ok


def test_not_a_git_repository_is_loud(tmp_path: Path) -> None:
    (tmp_path / ".aes").mkdir()
    shutil.copyfile(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
    with pytest.raises(TopologyError, match="git ls-files failed"):
        check_topology(tmp_path)


def test_cli_exit_codes(project_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["topology", "check", "--root", str(project_root)]) == 0
    assert capsys.readouterr().out.startswith("OK topology")

    _touch(project_root, *EGG_INFO)
    _git(project_root, "add", ".")
    assert main(["topology", "check", "--root", str(project_root)]) == 1
    err = capsys.readouterr().err
    assert "orphan: src/whygame5.egg-info/PKG-INFO" in err
    assert "fix:" in err
