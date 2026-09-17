from agentic_engineering_system.repository_context.models import (
    AuthorityRole,
    AuthoritySurfaceObservation,
    EpistemicState,
    EvidenceRef,
    RepositoryContextArtifact,
    ResolutionStatus,
)
from agentic_engineering_system.repository_context.render_html import render_html


def test_html_surface_keeps_revision_and_epistemic_state_visible():
    evidence = EvidenceRef(
        evidence_id="abc:README.md",
        repository_id="example/repo",
        revision="abcdef123456",
        path="README.md",
    )
    artifact = RepositoryContextArtifact(
        repository_id="example/repo",
        revision="abcdef123456",
        resolution_status=ResolutionStatus.PARTIAL,
        navigation=AuthoritySurfaceObservation(
            role=AuthorityRole.NAVIGATION,
            state=EpistemicState.OBSERVED,
            locations=("README.md",),
            summary="start here",
            evidence_refs=(evidence.evidence_id,),
        ),
        evidence=(evidence,),
    )
    page = render_html(artifact)
    assert "abcdef123456" in page
    assert "OBSERVED" in page
    assert "README.md" in page
    assert "Evidence" in page
