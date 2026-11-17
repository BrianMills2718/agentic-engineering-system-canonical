"""Tests for `lockstep check instructions` (the blocking instruction-file rules)."""

from pathlib import Path

import pytest

from lockstep.checks import instructions
from lockstep.checks.cli import run as main


def _repo(tmp_path: Path, root_text: str = "# Rules\n") -> Path:
    (tmp_path / "AGENTS.md").write_text(root_text)
    return tmp_path


def _kinds(result: instructions.Result) -> set[str]:
    return {f.kind for f in result.findings}


@pytest.mark.req("lockstep-checks/instructions-an-oversized-root-fails")
def test_oversized_root_fails(tmp_path: Path) -> None:
    repo = _repo(tmp_path, "x" * 13_000)
    result = instructions.check(repo, chain=[])
    assert "root_oversized" in _kinds(result)
    assert main(["instructions", "--repo", str(repo), "--chain", "none"]) == 1


@pytest.mark.req("lockstep-checks/instructions-a-chain-over-the-cap-fails")
def test_chain_over_cap_fails(tmp_path: Path) -> None:
    core = tmp_path / "core.md"
    core.write_text("c" * 30_000)
    repo = tmp_path / "repo"
    repo.mkdir()
    _repo(repo, "r" * 5_000)
    result = instructions.check(repo, chain=[core])
    assert "payload_over_cap" in _kinds(result)
    assert result.payload_bytes == 35_000
    assert "root_oversized" not in _kinds(result)


@pytest.mark.req("lockstep-checks/instructions-a-claude-md-with-content-fails")
def test_claude_md_with_content_fails(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / "CLAUDE.md").write_text("# Real rules that Codex never reads\n")
    sub = repo / "pkg"
    sub.mkdir()
    (sub / "CLAUDE.md").write_text("@AGENTS.md\n")
    result = instructions.check(repo, chain=[])
    flagged = [f.where for f in result.findings if f.kind == "claude_md_content"]
    assert flagged == ["CLAUDE.md"]


@pytest.mark.req("lockstep-checks/instructions-a-pointer-claude-md-passes")
def test_pointer_claude_md_passes(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / "CLAUDE.md").write_text("@AGENTS.md\n")
    ignored = repo / "worktrees" / "lane"
    ignored.mkdir(parents=True)
    (ignored / "CLAUDE.md").write_text("# a worktree copy with content\n")
    result = instructions.check(repo, chain=[])
    assert result.findings == []


@pytest.mark.req("lockstep-checks/instructions-a-repeated-parent-block-fails")
def test_repeated_parent_block_fails(tmp_path: Path) -> None:
    shared = "\n".join(f"This long rule number {i} applies to the whole repository and is stated once." for i in range(3))
    repo = _repo(tmp_path, "# Root\n" + shared + "\n")
    sub = repo / "api"
    sub.mkdir()
    (sub / "AGENTS.md").write_text("# API\n" + shared + "\nOnly the API's own rule lives here for the folder.\n")
    result = instructions.check(repo, chain=[])
    assert [(f.kind, f.where) for f in result.findings] == [("duplicated", "api/AGENTS.md")]


@pytest.mark.req("lockstep-checks/instructions-a-clean-repository-passes")
def test_clean_repository_passes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = _repo(tmp_path, "x" * 2_000)
    assert main(["instructions", "--repo", str(repo), "--chain", "none"]) == 0
    out = capsys.readouterr().out
    assert "instructions: files=1 payload_bytes=2000 payload_over_cap=0 root_oversized=0 claude_md_content=0 duplicated=0" in out


@pytest.mark.req("lockstep-checks/instructions-a-clean-repository-passes")
def test_repository_without_agents_md_passes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["instructions", "--repo", str(tmp_path), "--chain", "none"]) == 0
    assert "instructions: files=0" in capsys.readouterr().out
