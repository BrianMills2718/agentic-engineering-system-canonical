from __future__ import annotations

import subprocess
from pathlib import Path


class GitSourceError(RuntimeError):
    pass


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise GitSourceError(proc.stderr.strip() or "git command failed")
    return proc.stdout.strip()


def repository_root(path: Path) -> Path:
    return Path(_git(path, "rev-parse", "--show-toplevel")).resolve()


def revision(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD")


def repository_id(repo: Path) -> str:
    try:
        remote = _git(repo, "remote", "get-url", "origin")
    except GitSourceError:
        return repo.name
    tail = remote.rstrip("/").removesuffix(".git").split("/")[-1]
    return tail or repo.name
