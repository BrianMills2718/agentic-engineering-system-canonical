from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


MANIFEST_PATH = ".agentic/repo.yaml"


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
        if value.get("schema_version") is None:
            raise ManifestError("schema_version is required")
        return value

    def navigation_path(self) -> str | None:
        value = self.load()
        navigation = value.get("navigation")
        if navigation is None:
            return None
        if not isinstance(navigation, dict):
            raise ManifestError("navigation must be a mapping")
        path = navigation.get("wiki_entrypoint")
        if path is None:
            return None
        if not isinstance(path, str) or not path:
            raise ManifestError("navigation.wiki_entrypoint must be a non-empty string when present")
        return path

    def role_entries(self) -> list[dict[str, Any]]:
        value = self.load()
        authorities = value.get("authorities")
        if authorities is None:
            return []
        if not isinstance(authorities, dict):
            raise ManifestError("authorities must be a mapping")
        mapping = {
            "normative_roots": "normative",
            "decision_roots": "decision",
            "plan_roots": "plan",
            "implementation_roots": "implementation",
            "verification_roots": "verification",
            "contract_roots": "contract",
            "ownership_roots": "ownership",
        }
        entries: list[dict[str, Any]] = []
        for key, role in mapping.items():
            paths = authorities.get(key)
            if paths is None:
                entries.append({"role": role, "path": None})
                continue
            if not isinstance(paths, list):
                raise ManifestError(f"authorities.{key} must be a list")
            if not paths:
                entries.append({"role": role, "path": None})
                continue
            for path in paths:
                if not isinstance(path, str) or not path:
                    raise ManifestError(f"authorities.{key} entries must be non-empty strings")
                entries.append({"role": role, "path": path})
        return entries
