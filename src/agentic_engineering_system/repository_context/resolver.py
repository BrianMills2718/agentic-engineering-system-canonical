from __future__ import annotations

from pathlib import Path

from .git_source import GitSource, GitSourceError
from .legacy import LegacyRepositoryAdapter
from .manifest import ManifestError, PilotManifestAdapter
from .models import (
    AuthorityRole,
    AuthoritySurfaceObservation,
    ConcernRootObservation,
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

    def _resolve_manifest(self, source: GitSource, manifest: PilotManifestAdapter) -> RepositoryContextArtifact:
        try:
            value = manifest.load()
            entries = manifest.role_entries()
        except ManifestError as exc:
            return RepositoryContextArtifact(
                repository_id=source.repository_id,
                revision=source.revision,
                resolution_status=ResolutionStatus.ERROR,
                navigation=AuthoritySurfaceObservation(
                    role=AuthorityRole.NAVIGATION,
                    state=EpistemicState.ERROR,
                    summary="Authoritative repository-context manifest is malformed; legacy fallback is disabled.",
                ),
                unresolved=(UnresolvedSurface(
                    subject=MANIFEST_PATH,
                    reason=f"Correct the authoritative manifest and retry: {exc}",
                ),),
            )

        evidence = []
        manifest_evidence_id = f"{source.revision[:12]}:{MANIFEST_PATH}"
        from .legacy import _evidence
        ev = _evidence(source, MANIFEST_PATH, "authoritative repository-context manifest")
        evidence.append(ev)

        nav_path = value.get("navigation")
        if nav_path is None:
            navigation = AuthoritySurfaceObservation(
                role=AuthorityRole.NAVIGATION,
                state=EpistemicState.NONE,
                summary="The authoritative manifest does not declare a navigation surface.",
                evidence_refs=(ev.evidence_id,),
            )
        elif not isinstance(nav_path, str) or not nav_path:
            return RepositoryContextArtifact(
                repository_id=source.repository_id,
                revision=source.revision,
                resolution_status=ResolutionStatus.ERROR,
                navigation=AuthoritySurfaceObservation(
                    role=AuthorityRole.NAVIGATION,
                    state=EpistemicState.ERROR,
                    summary="Manifest navigation must be a non-empty path when declared.",
                    evidence_refs=(ev.evidence_id,),
                ),
                unresolved=(UnresolvedSurface(
                    subject="navigation",
                    reason="Correct the authoritative manifest and retry.",
                    evidence_refs=(ev.evidence_id,),
                ),),
                evidence=(ev,),
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
        if any(item.state == EpistemicState.ERROR for item in authorities):
            status = ResolutionStatus.ERROR
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


MANIFEST_PATH = ".agentic/repository-context.yaml"
