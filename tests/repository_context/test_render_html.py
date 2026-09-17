from agentic_engineering_system.repository_context.models import (
    AuthorityRole,
    AuthoritySurfaceObservation,
    ConcernRootObservation,
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
    assert "PARTIAL" in page
    assert "README.md" in page
    assert "Technical authority details and source evidence" in page


def test_html_surface_synthesizes_orientation_route_and_cautions():
    evidence = (
        EvidenceRef(
            evidence_id="abc:README.md",
            repository_id="example/repo",
            revision="abcdef123456",
            path="README.md",
        ),
        EvidenceRef(
            evidence_id="abc:ownership.md",
            repository_id="example/repo",
            revision="abcdef123456",
            path="docs/ownership.md",
        ),
        EvidenceRef(
            evidence_id="abc:pyproject.toml",
            repository_id="example/repo",
            revision="abcdef123456",
            path="pyproject.toml",
        ),
    )
    artifact = RepositoryContextArtifact(
        repository_id="example/repo",
        revision="abcdef123456",
        resolution_status=ResolutionStatus.RESOLVED,
        navigation=AuthoritySurfaceObservation(
            role=AuthorityRole.NAVIGATION,
            state=EpistemicState.OBSERVED,
            locations=("README.md",),
            summary="Repository-local entrypoint is README.md.",
            evidence_refs=("abc:README.md",),
        ),
        authorities=(
            AuthoritySurfaceObservation(
                role=AuthorityRole.OWNERSHIP,
                state=EpistemicState.OBSERVED,
                locations=("docs/ownership.md",),
                summary="Ownership is explicit here.",
                evidence_refs=("abc:ownership.md",),
            ),
            AuthoritySurfaceObservation(
                role=AuthorityRole.CONTRACT,
                state=EpistemicState.OBSERVED,
                locations=("src/example/",),
                summary="This package is the contract surface.",
                evidence_refs=("abc:pyproject.toml",),
            ),
            AuthoritySurfaceObservation(
                role=AuthorityRole.IMPLEMENTATION,
                state=EpistemicState.OBSERVED,
                locations=("src/example/",),
                summary="Implementation lives here.",
                evidence_refs=("abc:pyproject.toml",),
            ),
        ),
        concern_roots=(
            ConcernRootObservation(
                concern="contracts-root",
                state=EpistemicState.NONE,
                path="contracts/",
            ),
            ConcernRootObservation(
                concern="wiki-navigation",
                state=EpistemicState.NONE,
            ),
        ),
        evidence=evidence,
    )

    page = render_html(artifact)

    assert "What you need to know first" in page
    assert "Where do I start?" in page
    assert "Where is ownership decided?" in page
    assert "Where do contract questions go?" in page
    assert "Where does the code live?" in page
    assert "Recommended route" in page
    assert "Do not infer" in page
    assert "Do not treat <code>contracts/</code> as repository-wide contract authority" in page
    assert "Do not route through a local wiki by assumption" in page
    assert page.index("Recommended route") < page.index("Technical authority details and source evidence")
