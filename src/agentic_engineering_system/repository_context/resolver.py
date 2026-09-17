from __future__ import annotations

from pathlib import Path

from .git_source import repository_id, repository_root, revision
from .legacy import resolve_legacy
from .manifest import ManifestError, load_pilot_manifest
from .models import AuthorityRole, AuthoritySurfaceObservation, ConcernRootObservation, EvidenceRef, RepositoryContextArtifact, ResolutionStatus, SurfaceState, UnresolvedSurface

ROLE_MAP = {
    "normative_roots": AuthorityRole.NORMATIVE,
    "decision_roots": AuthorityRole.DECISION,
    "plan_roots": AuthorityRole.PLAN,
    "implementation_roots": AuthorityRole.IMPLEMENTATION,
    "verification_roots": AuthorityRole.VERIFICATION,
    "contract_roots": AuthorityRole.CONTRACT,
    "ownership_roots": AuthorityRole.OWNERSHIP,
}


def resolve_repository_context(path: str | Path, *, expect_revision: str | None = None) -> RepositoryContextArtifact:
    root = repository_root(Path(path))
    repo_id = repository_id(root)
    rev = revision(root)
    if expect_revision and rev != expect_revision:
        raise ValueError(f"revision mismatch: expected {expect_revision}, observed {rev}")

    try:
        manifest = load_pilot_manifest(root)
    except ManifestError as exc:
        manifest_path = ".agentic/repo.yaml"
        evidence = EvidenceRef(evidence_id=f"evidence:{manifest_path}", repository_id=repo_id, revision=rev, path=manifest_path, note="authoritative pilot manifest failed parsing")
        return RepositoryContextArtifact(
            repository_id=repo_id,
            revision=rev,
            resolution_status=ResolutionStatus.ERROR,
            navigation=AuthoritySurfaceObservation(role=AuthorityRole.NAVIGATION, state=SurfaceState.ERROR, summary=f"Authoritative manifest is invalid; correct it and retry. {exc}", evidence_refs=(evidence.evidence_id,)),
            unresolved=(UnresolvedSurface(subject=manifest_path, reason="Correct the authoritative manifest and retry; legacy inference is intentionally blocked.", evidence_refs=(evidence.evidence_id,)),),
            evidence=(evidence,),
        )

    if manifest is None:
        navigation, authorities, unresolved, evidence = resolve_legacy(root, repo_id, rev)
        status = ResolutionStatus.PARTIAL if unresolved else ResolutionStatus.RESOLVED
        return RepositoryContextArtifact(repository_id=repo_id, revision=rev, resolution_status=status, navigation=navigation, authorities=authorities, unresolved=unresolved, evidence=evidence)

    manifest_evidence = EvidenceRef(evidence_id="evidence:.agentic/repo.yaml", repository_id=repo_id, revision=rev, path=".agentic/repo.yaml", note="authoritative pilot repository declaration")
    nav_path = manifest.navigation_entrypoint
    if nav_path:
        nav_state = SurfaceState.OBSERVED if (root / nav_path).exists() else SurfaceState.ERROR
        nav = AuthoritySurfaceObservation(role=AuthorityRole.NAVIGATION, state=nav_state, locations=(nav_path,), summary=("Declared navigation entrypoint." if nav_state is SurfaceState.OBSERVED else "Declared navigation entrypoint is missing."), evidence_refs=(manifest_evidence.evidence_id,) if nav_state is SurfaceState.OBSERVED else ())
    else:
        nav = AuthoritySurfaceObservation(role=AuthorityRole.NAVIGATION, state=SurfaceState.NONE, summary="No navigation entrypoint declared.")

    authorities = []
    for manifest_name, role in ROLE_MAP.items():
        roots = manifest.authority_roots.get(manifest_name)
        if roots:
            authorities.append(AuthoritySurfaceObservation(role=role, state=SurfaceState.OBSERVED, locations=roots, summary=f"Declared {role.value} authority surface(s).", evidence_refs=(manifest_evidence.evidence_id,)))
        else:
            authorities.append(AuthoritySurfaceObservation(role=role, state=SurfaceState.NONE, summary=f"No {role.value} authority surface declared."))
    concerns = tuple(ConcernRootObservation(concern=name, state=SurfaceState.OBSERVED, path=path, evidence_refs=(manifest_evidence.evidence_id,)) for name, path in sorted(manifest.concern_roots.items()))
    unresolved = []
    if nav.state in {SurfaceState.ERROR, SurfaceState.NONE}:
        unresolved.append(UnresolvedSurface(subject="navigation", reason=nav.summary))
    return RepositoryContextArtifact(repository_id=repo_id, revision=rev, resolution_status=ResolutionStatus.PARTIAL if unresolved else ResolutionStatus.RESOLVED, navigation=nav, authorities=tuple(authorities), concern_roots=concerns, unresolved=tuple(unresolved), evidence=(manifest_evidence,))
