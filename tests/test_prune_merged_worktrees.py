"""Tests for prune_merged_worktrees.py's `--exclude` veto.

Pins the defect this flag exists to close: a branch's merge proof is a fact
about the BRANCH, not the worktree checked out at that path -- it says nothing
about whether that worktree has unrelated live activity a coordination claim
still names. Before this flag, the docstring's own claim that "nothing vetoes"
a proven merge was literally true, and a scheduled caller (sweep_lifecycle_
residue.py) removed a worktree a not-yet-expired claim still pointed at
(2026-09-08; no work was actually lost that time, but the gap was real).

Uses a real, hermetic local git repo (no network, no `gh`) so the merge-proof
signal exercised here is Signal 2 (content equality via `git merge-tree`),
which needs no forge access.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "prune_merged_worktrees.py"


def _run_git(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)


def _commit_all(repo: Path, message: str) -> None:
    _run_git("add", "-A", cwd=repo)
    subprocess.run(
        ["git", "-c", "user.email=t@example.invalid", "-c", "user.name=T", "commit", "-m", message],
        cwd=repo, capture_output=True, text=True, check=True,
    )


def _make_repo_with_mergeable_worktree(tmp_path: Path) -> tuple[Path, Path, str]:
    """A repo whose sole linked worktree's branch merges into main adding nothing."""
    repo = tmp_path / "repo"
    _run_git("init", "-b", "main", str(repo), cwd=tmp_path)
    (repo / "README.md").write_text("# repo\n", encoding="utf-8")
    _commit_all(repo, "initial")
    # No real remote; point origin/main at local main so default_branch()/the
    # `origin/<default>` ref resolution this script relies on has something
    # to resolve, entirely offline.
    _run_git("update-ref", "refs/remotes/origin/main", "main", cwd=repo)
    _run_git("remote", "add", "origin", str(repo), cwd=repo)  # never fetched; ref already set above

    branch = "feature/no-op"
    _run_git("branch", branch, "main", cwd=repo)  # branch tip == main tip: merges add nothing
    worktree = tmp_path / "wt-feature"
    result = _run_git("worktree", "add", str(worktree), branch, cwd=repo)
    assert result.returncode == 0, result.stderr
    return repo, worktree, branch


@pytest.mark.req("prune-merged-worktrees/proven-merge-only", existing=True)  # ported unchanged from Project Meta
def test_exclude_keeps_a_provably_merged_worktree(tmp_path: Path) -> None:
    repo, worktree, branch = _make_repo_with_mergeable_worktree(tmp_path)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(repo), "--exclude", str(worktree)],
        capture_output=True, text=True, check=False,
    )
    assert worktree.is_dir(), "excluded worktree must survive even though its branch is proven merged"
    assert "excluded: caller protection" in result.stdout
    verify = _run_git("rev-parse", "--verify", "--quiet", branch, cwd=repo)
    assert verify.returncode == 0, "excluded branch must not be force-deleted either"


@pytest.mark.req("prune-merged-worktrees/proven-merge-only", existing=True)  # ported unchanged from Project Meta
def test_without_exclude_the_same_worktree_is_removed(tmp_path: Path) -> None:
    """Control: confirms the fixture actually proves a real removal absent --exclude,
    so the exclude test above is verifying a real veto, not an already-inert case."""
    repo, worktree, _branch = _make_repo_with_mergeable_worktree(tmp_path)

    subprocess.run(
        [sys.executable, str(SCRIPT), str(repo)],
        capture_output=True, text=True, check=False,
    )
    assert not worktree.exists(), "control case: without --exclude, a provably-merged worktree is removed"


@pytest.mark.req("prune-merged-worktrees/proven-merge-only", existing=True)  # ported unchanged from Project Meta
def test_help_and_unknown_flags_never_prune(tmp_path: Path) -> None:
    """Observed 2026-09-15: `--help` was silently ignored and ran a real prune, removing three worktrees.

    The control test above proves this fixture's worktree is removable, so its
    survival here is a real refusal.
    """
    repo, worktree, _branch = _make_repo_with_mergeable_worktree(tmp_path)

    helped = subprocess.run([sys.executable, str(SCRIPT), str(repo), "--help"], capture_output=True, text=True, check=False)
    typo = subprocess.run([sys.executable, str(SCRIPT), str(repo), "--dryrun"], capture_output=True, text=True, check=False)

    assert helped.returncode == 0 and "usage:" in helped.stdout
    assert typo.returncode == 2 and "--dryrun" in typo.stderr
    assert worktree.is_dir()
