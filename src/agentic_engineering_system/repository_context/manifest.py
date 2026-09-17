from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


MANIFEST_PATH = ".agentic/repository-context.yaml"


class ManifestError(ValueError):
    """Raised when the authoritative pilot manifest is malformed."""


class PilotManifestAdapter:
    def __init__(self, repo: Path):
        self.repo = repo.resolve()
        self.path = self.repo / MANIFEST_PATH

    @property
    def present(self) -> bool:
        return self.path.is_file()

    def load(self) -> dict[str, Any]:
        if not self.present:
            raise FileNotFoundError(MANIFEST_PATH)
        try:
            value = yaml.safe_load(self.path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise ManifestError(f"cannot parse {MANIFEST_PATH}: {exc}") from exc
        if not isinstance(value, dict):
            raise ManifestError(f"{MANIFEST_PATH} must contain a mapping")
        return value

    def role_entries(self) -> list[dict[str, Any]]:
        value = self.load()
        authorities = value.get("authorities")
        if not isinstance(authorities, list):
            raise ManifestError("authorities must be a list")
        entries: list[dict[str, Any]] = []
        for entry in authorities:
            if not isinstance(entry, dict):
                raise ManifestError("each authority entry must be a mapping")
            role = entry.get("role")
            path = entry.get("path")
            if not isinstance(role, str) or not role:
                raise ManifestError("authority entry role must be a non-empty string")
            if path is not None and (not isinstance(path, str) or not path):
                raise ManifestError("authority entry path must be a non-empty string when present")
            entries.append(entry)
        return entries
