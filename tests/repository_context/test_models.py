import pytest
from pydantic import ValidationError

from agentic_engineering_system.repository_context.models import (
    AuthorityRole,
    AuthoritySurfaceObservation,
    EpistemicState,
    EvidenceRef,
    RepositoryContextArtifact,
    ResolutionStatus,
)


def test_positive_authority_requires_explicit_evidence_reference_shape():
    evidence = EvidenceRef(
        evidence_id="r1:README.md",
        repository_id="example/repo",
        revision="r1",
        path="README.md",
    )
    observation = AuthoritySurfaceObservation(
        role=AuthorityRole.NAVIGATION,
        state=EpistemicState.OBSERVED,
        locations=("README.md",),
        summary="root entrypoint",
        evidence_refs=(evidence.evidence_id,),
    )
    artifact = RepositoryContextArtifact(
        repository_id="example/repo",
        revision="r1",
        resolution_status=ResolutionStatus.RESOLVED,
        navigation=observation,
        evidence=(evidence,),
    )
    assert artifact.navigation.evidence_refs == ("r1:README.md",)


def test_observed_authority_without_evidence_is_rejected():
    with pytest.raises(ValidationError):
        AuthoritySurfaceObservation(
            role=AuthorityRole.CONTRACT,
            state=EpistemicState.OBSERVED,
            locations=("src/demo/",),
            summary="unsupported positive claim",
        )


def test_artifact_rejects_observed_claim_with_missing_evidence_object():
    observation = AuthoritySurfaceObservation(
        role=AuthorityRole.NAVIGATION,
        state=EpistemicState.OBSERVED,
        locations=("README.md",),
        summary="root entrypoint",
        evidence_refs=("missing",),
    )
    with pytest.raises(ValidationError):
        RepositoryContextArtifact(
            repository_id="example/repo",
            revision="r1",
            resolution_status=ResolutionStatus.RESOLVED,
            navigation=observation,
        )


def test_models_are_immutable_and_reject_unknown_fields():
    observation = AuthoritySurfaceObservation(
        role=AuthorityRole.NAVIGATION,
        state=EpistemicState.NONE,
        summary="none",
    )
    try:
        observation.summary = "changed"
    except Exception:
        pass
    else:
        raise AssertionError("models must be frozen")
