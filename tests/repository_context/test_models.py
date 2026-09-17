import pytest

from agentic_engineering_system.repository_context.models import AuthorityRole, AuthoritySurfaceObservation, SurfaceState


def test_observed_authority_requires_evidence():
    with pytest.raises(ValueError):
        AuthoritySurfaceObservation(role=AuthorityRole.CONTRACT, state=SurfaceState.OBSERVED, summary="x")
