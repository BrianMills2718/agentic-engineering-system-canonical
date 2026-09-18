from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def repo_factory(tmp_path: Path):
    counter = 0

    def make(*, readme: str = "", pyproject: str = "", manifest: str | None = None) -> Path:
        nonlocal counter
        counter += 1
        repo = tmp_path / f"repo-{counter}"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
        if readme:
            (repo / "README.md").write_text(readme, encoding="utf-8")
        if pyproject:
            (repo / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        if manifest is not None:
            (repo / ".agentic").mkdir()
            (repo / ".agentic" / "repo.yaml").write_text(manifest, encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "fixture"], check=True)
        return repo

    return make
