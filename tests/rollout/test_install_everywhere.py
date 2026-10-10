"""The commit-rule installer reads a repository's commit-msg hook instead of trusting its config.

On 2026-10-10 observation-to-action-metamodel and whygame5 had `.aes/project.yaml` and
`core.hooksPath=.githooks`, so `install_everywhere.py check` called them wired, but their `.githooks`
held only the `pre-commit` written by an `aes hooks install` from before the commit rule existed: no
commit there was ever judged (metamodel d27d160, 54492b2, 4f62c97, 4f7f998). These tests build that
repository for real, run `git commit` through the generated wrapper, and use a stand-in for the rule
that records each run (the rule itself is tested in tests/greenfield/test_commit_rule.py).
"""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

INSTALLER = Path(__file__).resolve().parents[2] / "proposals" / "aes-planning" / "rollout" / "install_everywhere.py"
_spec = importlib.util.spec_from_file_location("install_everywhere", INSTALLER)
assert _spec and _spec.loader
inst = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(inst)

OLD_PRE_COMMIT = "#!/bin/sh\n# managed by aes hooks install\necho own-pre-commit >> \"$(git rev-parse --show-toplevel)/../ran.log\"\n"
AES_COMMIT_MSG = ("#!/bin/sh\n# managed by aes hooks install\n"
                  "echo own-aes-commit-msg >> \"$(git rev-parse --show-toplevel)/../ran.log\"\n"
                  ": aes commit check \"$1\"\n")


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
                          cwd=repo, capture_output=True, text=True, check=False)


def _exec(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)


@pytest.fixture()
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the installer's machine paths into tmp, with a stand-in rule that logs and refuses on REFUSE."""
    hooks = tmp_path / "config" / "git" / "hooks"
    monkeypatch.setattr(inst, "GLOBAL_HOOKS", hooks)
    monkeypatch.setattr(inst, "LOCAL_WRAPPERS", tmp_path / "config" / "git" / "hooks-local")
    snippet = hooks / "_aes_commit_rule.sh"
    monkeypatch.setattr(inst, "SNIPPET", snippet)
    _exec(snippet, "aes_commit_rule() {\n  echo rule >> \"$(git rev-parse --show-toplevel)/../ran.log\"\n"
                   "  if grep -q REFUSE \"$1\"; then echo 'stand-in rule: refuse' >&2; return 1; fi\n}\n")
    return tmp_path


def _aes_repo(home: Path, *, commit_msg: bool) -> Path:
    repo = home / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    (repo / ".aes").mkdir()
    (repo / ".aes" / "project.yaml").write_text("schema_version: 1\n", encoding="utf-8")
    _exec(repo / ".githooks" / "pre-commit", OLD_PRE_COMMIT)
    if commit_msg:
        _exec(repo / ".githooks" / "commit-msg", AES_COMMIT_MSG)
    _git(repo, "config", "core.hooksPath", ".githooks")
    return repo


def _ran(home: Path) -> list[str]:
    log = home / "ran.log"
    lines = log.read_text(encoding="utf-8").split() if log.exists() else []
    log.unlink(missing_ok=True)
    return lines


def test_aes_project_with_only_pre_commit_is_reported_unwired_then_wrapped(home: Path) -> None:
    repo = _aes_repo(home, commit_msg=False)
    kind, ok, detail = inst.wired(repo)
    assert (kind, ok) == ("local", False), detail  # before the fix: ("aes", True, "AES-generated hooks at .githooks")
    assert not inst.is_aes_native(repo)

    inst.install_local(repo)
    assert inst.wired(repo)[:2] == ("local", True)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _git(repo, "add", "a.txt")
    refused = _git(repo, "commit", "-m", "[Unplanned] REFUSE this")
    assert refused.returncode == 1 and "stand-in rule: refuse" in refused.stderr
    assert _ran(home) == ["own-pre-commit", "rule"]  # the repository's own pre-commit still runs
    done = _git(repo, "commit", "-m", "[Trivial] add a")
    assert done.returncode == 0, done.stderr
    assert _ran(home) == ["own-pre-commit", "rule"]


def test_aes_project_whose_commit_msg_runs_the_rule_is_native_and_not_judged_twice(home: Path) -> None:
    repo = _aes_repo(home, commit_msg=True)
    assert inst.is_aes_native(repo)
    assert inst.wired(repo)[:2] == ("aes", True)
    # A linked worktree of an AES project can sit behind a wrapper (its main checkout predates the
    # commit-msg hook); the wrapper then hands over to the checkout's own AES hook instead of running twice.
    inst.install_local(repo)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    _git(repo, "add", "a.txt")
    done = _git(repo, "commit", "-m", "[Trivial] add a")
    assert done.returncode == 0, done.stderr
    assert _ran(home) == ["own-pre-commit", "own-aes-commit-msg"]
