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
import os
import subprocess
import sys
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


# project-meta's hooks/commit-msg template, reduced to its logic: a regex list with a lowercase-only Goal
# pattern (the divergence in #297/#414). Its docstring carries the marker the wrapper looks for.
PREFIX_ONLY_HOOK = f'''#!/usr/bin/env python3
"""Commit-msg hook that {inst.PREFIX_ONLY_MARK}."""
import re, sys
first = open(sys.argv[1], encoding="utf-8").read().splitlines()[0]
prefixes = [r"\\[Goal [a-z0-9][a-z0-9._:-]*\\]", r"\\[Plan #\\d+\\]", r"\\[Trivial\\]", r"\\[Docs\\]"]
if any(re.match(p, first) for p in prefixes):
    sys.exit(0)
print("ERROR: Commit message must start with a valid prefix.", file=sys.stderr)
sys.exit(1)
'''


def _prefix_only_repo(home: Path) -> Path:
    repo = home / "pm"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _exec(repo / "hooks" / "commit-msg", PREFIX_ONLY_HOOK)
    _git(repo, "config", "core.hooksPath", "hooks")
    inst.install_local(repo)
    return repo


def _real_aes(home: Path) -> Path:
    """An `aes` on PATH that is this checkout's CLI, so the wrapper asks the real commit-rule grammar."""
    src = Path(__file__).resolve().parents[2] / "src"
    bin_dir = home / "bin"
    _exec(bin_dir / "aes", f'#!/bin/sh\nPYTHONPATH="{src}" exec "{sys.executable}" -m agentic_engineering_system.cli "$@"\n')
    return bin_dir


def _commit(repo: Path, message: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    (repo / "f.txt").write_text(message, encoding="utf-8")
    _git(repo, "add", "f.txt")
    return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid",
                           "commit", "-q", "-m", message], cwd=repo, capture_output=True, text=True, env=env)


def test_tag_the_rule_recognises_passes_a_lagging_prefix_only_hook(home: Path) -> None:
    """#414: a valid [Goal <Upper-case id>] was refused by the chained copy of project-meta's prefix list."""
    repo = _prefix_only_repo(home)
    env = {**os.environ, "PATH": f"{_real_aes(home)}:{os.environ['PATH']}", "HOME": str(home)}
    done = _commit(repo, "[Goal PATH-Upper-1] work under a capitalised plan id", env)
    assert done.returncode == 0, done.stderr
    assert "valid prefix" not in done.stderr
    bogus = _commit(repo, "[Bogus] not a tag anywhere", env)
    assert bogus.returncode == 1 and "must start with a valid prefix" in bogus.stderr
    legacy = _commit(repo, "[Docs] a tag only this repository's list knows", env)
    assert legacy.returncode == 0, legacy.stderr


def test_without_aes_the_prefix_only_hook_still_decides(home: Path) -> None:
    """A missing aes must not open the gate: the repository's own list is then the only judge."""
    repo = _prefix_only_repo(home)
    path = ":".join(p for p in os.environ["PATH"].split(":") if not (Path(p) / "aes").exists())
    env = {**os.environ, "PATH": path, "HOME": str(home)}
    refused = _commit(repo, "[Goal PATH-Upper-1] capitalised id, no aes to ask", env)
    assert refused.returncode == 1 and "must start with a valid prefix" in refused.stderr
    done = _commit(repo, "[Goal lower-1] lowercase id the list accepts", env)
    assert done.returncode == 0, done.stderr
