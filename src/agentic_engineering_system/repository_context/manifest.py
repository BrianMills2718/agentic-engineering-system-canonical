from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


class ManifestError(ValueError):
    pass


@dataclass(frozen=True)
class PilotManifest:
    navigation_entrypoint: str | None
    authority_roots: dict[str, tuple[str, ...]]
    concern_roots: dict[str, str]


def load_pilot_manifest(repo: Path) -> PilotManifest | None:
    path = repo / ".agentic" / "repo.yaml"
    if not path.exists():
        return None
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ManifestError(f"invalid authoritative manifest {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ManifestError(f"invalid authoritative manifest {path}: expected mapping")

    navigation = raw.get("navigation") or {}
    authorities = raw.get("authorities") or {}
    concerns = raw.get("concerns") or {}
    if not isinstance(navigation, dict) or not isinstance(authorities, dict) or not isinstance(concerns, dict):
        raise ManifestError(f"invalid authoritative manifest {path}: navigation/authorities/concerns must be mappings")

    entry = navigation.get("wiki_entrypoint")
    if entry is not None and not isinstance(entry, str):
        raise ManifestError(f"invalid authoritative manifest {path}: wiki_entrypoint must be a string")

    authority_roots: dict[str, tuple[str, ...]] = {}
    for role, value in authorities.items():
        if not isinstance(role, str):
            raise ManifestError(f"invalid authoritative manifest {path}: authority role must be a string")
        if isinstance(value, str):
            roots = (value,)
        elif isinstance(value, list) and all(isinstance(x, str) for x in value):
            roots = tuple(value)
        else:
            raise ManifestError(f"invalid authoritative manifest {path}: authority roots must be strings/lists")
        authority_roots[role] = roots

    concern_roots: dict[str, str] = {}
    for name, value in concerns.items():
        if not isinstance(name, str) or not isinstance(value, dict) or not isinstance(value.get("root"), str):
            raise ManifestError(f"invalid authoritative manifest {path}: concern entries require a root string")
        concern_roots[name] = value["root"]

    return PilotManifest(entry, authority_roots, concern_roots)
