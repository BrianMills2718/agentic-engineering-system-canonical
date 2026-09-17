from __future__ import annotations

import re
import tomllib
from pathlib import Path

from .models import AuthorityRole, AuthoritySurfaceObservation, EvidenceRef, SurfaceState, UnresolvedSurface

_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)|`([^`]+)`")


def _evidence(repo_id: str, revision: str, path: str, note: str) -> EvidenceRef:
    return EvidenceRef(evidence_id=f"evidence:{path}", repository_id=repo_id, revision=revision, path=path, note=note)


def resolve_legacy(repo: Path, repo_id: str, revision: str):
    evidence: list[EvidenceRef] = []
    authorities: list[AuthoritySurfaceObservation] = []
    unresolved: list[UnresolvedSurface] = []

    readme_path = repo / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    if readme:
        evidence.append(_evidence(repo_id, revision, "README.md", "root local-entrypoint/context document"))

    wiki = repo / "wiki" / "index.md"
    if wiki.exists():
        evidence.append(_evidence(repo_id, revision, "wiki/index.md", "observed local wiki entrypoint"))
        navigation = AuthoritySurfaceObservation(role=AuthorityRole.NAVIGATION, state=SurfaceState.OBSERVED, locations=("wiki/index.md",), summary="Local wiki entrypoint is present.", evidence_refs=("evidence:wiki/index.md",))
    elif readme:
        navigation = AuthoritySurfaceObservation(role=AuthorityRole.NAVIGATION, state=SurfaceState.OBSERVED, locations=("README.md",), summary="No local wiki/index.md is present; README.md is the bounded legacy starting point.", evidence_refs=("evidence:README.md",))
        unresolved.append(UnresolvedSurface(subject="wiki/index.md", reason="No local wiki entrypoint observed."))
    else:
        navigation = AuthoritySurfaceObservation(role=AuthorityRole.NAVIGATION, state=SurfaceState.NONE, summary="No bounded navigation entrypoint was observed.")

    pyproject = repo / "pyproject.toml"
    if pyproject.exists():
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        project_name = str((data.get("project") or {}).get("name") or "").replace("-", "_")
        where = (((data.get("tool") or {}).get("setuptools") or {}).get("packages") or {}).get("find") or {}
        roots = where.get("where") if isinstance(where, dict) else None
        src_root = roots[0] if isinstance(roots, list) and roots and isinstance(roots[0], str) else None
        if src_root and project_name:
            candidate = f"{src_root.rstrip('/')}/{project_name}/"
            if (repo / candidate).is_dir():
                evidence.append(_evidence(repo_id, revision, "pyproject.toml", "package root and project name"))
                authorities.append(AuthoritySurfaceObservation(role=AuthorityRole.IMPLEMENTATION, state=SurfaceState.OBSERVED, locations=(candidate,), summary=f"Package metadata identifies {candidate} as a native implementation surface.", evidence_refs=("evidence:pyproject.toml",)))

    ownership_path: str | None = None
    for match in _LINK_RE.finditer(readme):
        candidate = match.group(1) or match.group(2)
        if candidate and candidate.startswith("docs/") and "CAPABILITY_DECOMPOSITION" in candidate:
            ownership_path = candidate
            break
    if ownership_path and (repo / ownership_path).is_file():
        evidence.append(_evidence(repo_id, revision, ownership_path, "ownership document directly referenced by README"))
        authorities.append(AuthoritySurfaceObservation(role=AuthorityRole.OWNERSHIP, state=SurfaceState.OBSERVED, locations=(ownership_path,), summary="Repository ownership questions route to the explicitly referenced capability-decomposition authority.", evidence_refs=(f"evidence:{ownership_path}", "evidence:README.md")))

    implementation = next((a for a in authorities if a.role is AuthorityRole.IMPLEMENTATION), None)
    if implementation and readme and "typed" in readme.lower() and "contract" in readme.lower():
        authorities.append(AuthoritySurfaceObservation(role=AuthorityRole.CONTRACT, state=SurfaceState.OBSERVED, locations=implementation.locations, summary="README semantics plus package metadata identify the package implementation as the contract surface; directory names alone are not authority.", evidence_refs=("evidence:README.md", "evidence:pyproject.toml")))
    else:
        authorities.append(AuthoritySurfaceObservation(role=AuthorityRole.CONTRACT, state=SurfaceState.UNRESOLVED, summary="No bounded positive evidence established a contract authority."))

    unresolved.append(UnresolvedSurface(subject=".agentic/repo.yaml", reason="Pilot manifest absent; resolution used bounded legacy evidence only."))
    return navigation, tuple(authorities), tuple(unresolved), tuple(evidence)
