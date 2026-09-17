from __future__ import annotations

from pathlib import Path

from .git_source import GitSource, GitSourceError
from .legacy import LegacyRepositoryAdapter, _evidence
from .manifest import MANIFEST_PATH, ManifestError, PilotManifestAdapter
from .models import (
    AuthorityRole,
    AuthoritySurfaceObservation,
    EpistemicState,
    RepositoryContextArtifact,
    ResolutionStatus,
    UnresolvedSurface,
)


class RepositoryContextResolver:
    def __init__(self, repo: Path):
        self.repo = Path(repo).resolve()

    def resolve(self, expected_revision: str | None = None) -> RepositoryContextArtifact:
        try:
            source = GitSource(self.repo)
            source.assert_revision(expected_revision)
        except GitSourceError as exc:
            return RepositoryContextArtifact(
                repository_id=self.repo.name,
                revision=expected_revision or "UNKNOWN",
                resolution_status=ResolutionStatus.ERROR,
                navigation=AuthoritySurfaceObservation(
                    role=AuthorityRole.NAVIGATION,
                    state=EpistemicState.ERROR,
                    summary=str(exc),
                ),
                unresolved=(UnresolvedSurface(
                    subject="repository",
                    reason=f"Resolve the local Git checkout before retrying: {exc}",
                ),),
            )

        manifest = PilotManifestAdapter(self.repo)
        if manifest.present:
            return self._resolve_manifest(source, manifest)
        return self._resolve_legacy(source)

    def _resolve_manifest(
        self, source: GitSource, manifest: PilotManifestAdapter
    ) -> RepositoryContextArtifact:
        try:
            entries = manifest.role_entries()
            nav_path = manifest.navigation_path()
        except ManifestError as exc:
            return RepositoryContextArtifact(
                repository_id=source.repository_id,
                revision=source.revision,
                resolution_status=ResolutionStatus.ERROR,
                navigation=AuthoritySurfaceObservation(
                    role=AuthorityRole.NAVIGATION,
                    state=EpistemicState.ERROR,
                    summary="Authoritative .agentic/repo.yaml is malformed; legacy fallback is disabled.",
                ),
                unresolved=(UnresolvedSurface(
                    subject=MANIFEST_PATH,
                    reason=f"Correct the authoritative manifest and retry: {exc}",
                ),),
            )

        ev = _evidence(source, MANIFEST_PATH, "authoritative pilot repository manifest")
        evidence = [ev]
        if nav_path is None:
            navigation = AuthoritySurfaceObservation(
                role=AuthorityRole.NAVIGATION,
                state=EpistemicState.NONE,
                summary="The authoritative manifest does not declare a wiki navigation surface.",
                evidence_refs=(ev.evidence_id,),
            )
        elif not source.exists(nav_path):
            navigation = AuthoritySurfaceObservation(
                role=AuthorityRole.NAVIGATION,
                state=EpistemicState.UNRESOLVED,
                locations=(nav_path,),
                summary="Manifest declares a navigation path that is absent at this revision.",
                evidence_refs=(ev.evidence_id,),
            )
        else:
            navigation = AuthoritySurfaceObservation(
                role=AuthorityRole.NAVIGATION,
                state=EpistemicState.OBSERVED,
                locations=(nav_path,),
                summary="Navigation surface declared by the authoritative manifest.",
                evidence_refs=(ev.evidence_id,),
            )

        authorities = []
        unresolved = []
        for entry in entries:
            role = entry["role"]
            try:
                enum_role = AuthorityRole(role)
            except ValueError:
                unresolved.append(UnresolvedSurface(
                    subject=f"authority:{role}",
                    reason="Manifest role is not one of the governed authority roles.",
                    evidence_refs=(ev.evidence_id,),
                ))
                continue
            path = entry.get("path")
            if path is None:
                authorities.append(AuthoritySurfaceObservation(
                    role=enum_role,
                    state=EpistemicState.NONE,
                    summary="Role is explicitly declared absent by the authoritative manifest.",
                    evidence_refs=(ev.evidence_id,),
                ))
            elif source.exists(path):
                authorities.append(AuthoritySurfaceObservation(
                    role=enum_role,
                    state=EpistemicState.OBSERVED,
                    locations=(path,),
                    summary=f"{role} authority is declared by the authoritative manifest.",
                    evidence_refs=(ev.evidence_id,),
                ))
            else:
                authorities.append(AuthoritySurfaceObservation(
                    role=enum_role,
                    state=EpistemicState.UNRESOLVED,
                    locations=(path,),
                    summary="Manifest-declared authority path is absent at this revision.",
                    evidence_refs=(ev.evidence_id,),
                ))

        status = ResolutionStatus.RESOLVED
        if unresolved or navigation.state != EpistemicState.OBSERVED or any(
            item.state in {EpistemicState.ERROR, EpistemicState.UNRESOLVED} for item in authorities
        ):
            status = ResolutionStatus.PARTIAL
        return RepositoryContextArtifact(
            repository_id=source.repository_id,
            revision=source.revision,
            resolution_status=status,
            navigation=navigation,
            authorities=tuple(authorities),
            unresolved=tuple(unresolved),
            evidence=tuple(evidence),
        )

    def _resolve_legacy(self, source: GitSource) -> RepositoryContextArtifact:
        adapter = LegacyRepositoryAdapter(source)
        navigation, nav_evidence = adapter.navigation()
        authorities, concerns, evidence = adapter.authorities()
        all_evidence = tuple(nav_evidence + evidence)
        unresolved = []
        if navigation.state != EpistemicState.OBSERVED:
            unresolved.append(UnresolvedSurface(
                subject="navigation",
                reason="No explicit root navigation authority was observed; inspect repository-native sources manually.",
                evidence_refs=navigation.evidence_refs,
            ))
        status = ResolutionStatus.RESOLVED if navigation.state == EpistemicState.OBSERVED else ResolutionStatus.PARTIAL
        return RepositoryContextArtifact(
            repository_id=source.repository_id,
            revision=source.revision,
            resolution_status=status,
            navigation=navigation,
            authorities=tuple(authorities),
            concern_roots=tuple(concerns),
            unresolved=tuple(unresolved),
            evidence=all_evidence,
        )
