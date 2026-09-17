from __future__ import annotations

import os
from pathlib import Path

import pytest

from agentic_engineering_system.repository_context.models import AuthorityRole, SurfaceState
from agentic_engineering_system.repository_context.resolver import resolve_repository_context

PIN = "90c38998e8141bd07e49a77a49ec417aa29beee0"


def test_pinned_data_contracts_external_consumer():
    raw = os.environ.get("DATA_CONTRACTS_REPO")
    if not raw:
        pytest.skip("set DATA_CONTRACTS_REPO to the pinned local data-contracts checkout")
    artifact = resolve_repository_context(Path(raw), expect_revision=PIN)
    impl = next(x for x in artifact.authorities if x.role is AuthorityRole.IMPLEMENTATION)
    contract = next(x for x in artifact.authorities if x.role is AuthorityRole.CONTRACT)
    ownership = next(x for x in artifact.authorities if x.role is AuthorityRole.OWNERSHIP)
    assert impl.state is SurfaceState.OBSERVED
    assert "src/data_contracts/" in impl.locations
    assert contract.state is SurfaceState.OBSERVED
    assert "contracts/" not in contract.locations
    assert ownership.locations == ("docs/ops/CAPABILITY_DECOMPOSITION.md",)
    assert artifact.navigation.locations == ("README.md",)
