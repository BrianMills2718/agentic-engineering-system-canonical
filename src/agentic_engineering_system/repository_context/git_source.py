from __future__ import annotations

import subprocess
from pathlib import Path


class GitSourceError(RuntimeError):
    """Raised when a local repository cannot provide required Git evidence."""


class GitSource:
    def __init__(self, repo: Path):
        self.repo = repo.resolve()
        if not (self.repo / ".git").exists():
            raise GitSourceError(f"not a Git checkout: {self.repo}")

    def _run(self, *args: str) -> str:
        try:
            result = subprocess.run(
                ["git", *args], cwd=self.repo, text=True, capture_output=True, check=True
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            detail = getattr(exc, "stderr", "") or str(exc)
            raise GitSourceError(detail.strip()) from exc
        return result.stdout.strip()

    @property
    def repository_id(self) -> str:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )
        remote = result.stdout.strip() if result.returncode == 0 else ""
        if not remote:
            return self.repo.name
        value = remote.removesuffix(".git")
        if value.startswith("git@") and ":" in value:
            return value.split(":", 1)[1]
        for prefix in ("https://github.com/", "http://github.com/"):
            if value.startswith(prefix):
                return value.removeprefix(prefix)
        return value.rsplit("/", 1)[-1]

    @property
    def revision(self) -> str:
        return self._run("rev-parse", "HEAD")

    def assert_revision(self, expected: str | None) -> None:
        if expected and self.revision != expected:
            raise GitSourceError(
                f"revision mismatch: expected {expected}, observed {self.revision}"
            )

    def exists(self, relative: str) -> bool:
        path = (self.repo / relative).resolve()
        return path.exists() and (path == self.repo or self.repo in path.parents)

    def read_text(self, relative: str) -> str:
        path = (self.repo / relative).resolve()
        if not path.is_file() or self.repo not in path.parents:
            raise GitSourceError(f"missing source file: {relative}")
        return path.read_text(encoding="utf-8")

    def source_url(self, relative: str) -> str | None:
        rid = self.repository_id
        if "/" not in rid or not rid.startswith("http") and rid.count("/") != 1:
            return None
        if rid.startswith("http"):
            return f"{rid}/blob/{self.revision}/{relative}"
        return f"https://github.com/{rid}/blob/{self.revision}/{relative}"
