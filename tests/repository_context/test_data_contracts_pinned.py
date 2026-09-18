import os
from pathlib import Path
import subprocess

import pytest

from agentic_engineering_system.repository_context.models import AuthorityRole, EpistemicState
from agentic_engineering_system.repository_context.render_html import render_html
from agentic_engineering_system.repository_context.resolver import RepositoryContextResolver


PINNED_REVISION = "90c38998e8141bd07e49a77a49ec417aa29beee0"


def test_pinned_data_contracts_revision_when_checkout_is_available():
    checkout = os.environ.get("AES_DATA_CONTRACTS_CHECKOUT")
    if not checkout:
        pytest.skip(
            "requires AES_DATA_CONTRACTS_CHECKOUT; this is intentionally not replaced by a synthetic fixture"
        )
    path = Path(checkout)
    observed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, text=True, capture_output=True, check=True
    ).stdout.strip()
    assert observed == PINNED_REVISION
    assert (path / "README.md").is_file()
    assert (path / "src" / "data_contracts").is_dir()
    assert (path / "docs" / "ops" / "CAPABILITY_DECOMPOSITION.md").is_file()

    artifact = RepositoryContextResolver(path).resolve(PINNED_REVISION)
    evidence_ids = {item.evidence_id for item in artifact.evidence}

    assert artifact.revision == PINNED_REVISION
    assert artifact.navigation.state == EpistemicState.OBSERVED
    assert artifact.navigation.locations == ("README.md",)

    implementation = next(item for item in artifact.authorities if item.role == AuthorityRole.IMPLEMENTATION)
    contract = next(item for item in artifact.authorities if item.role == AuthorityRole.CONTRACT)
    ownership = next(item for item in artifact.authorities if item.role == AuthorityRole.OWNERSHIP)

    assert implementation.locations == ("src/data_contracts/",)
    assert contract.locations == ("src/data_contracts/",)
    assert ownership.locations == ("docs/ops/CAPABILITY_DECOMPOSITION.md",)
    assert all(ref in evidence_ids for ref in implementation.evidence_refs)
    assert all(ref in evidence_ids for ref in contract.evidence_refs)
    assert all(ref in evidence_ids for ref in ownership.evidence_refs)
    assert "contracts/" not in contract.locations

    # This exact revision physically contains wiki/index.md, but no bounded root source
    # positively routes to it as the local semantic navigation authority. Existence alone
    # therefore does not promote it.
    assert (path / "wiki" / "index.md").is_file()
    assert not any(
        item.role == AuthorityRole.NAVIGATION and "wiki/index.md" in item.locations
        for item in artifact.authorities
    )
    wiki = next(item for item in artifact.concern_roots if item.concern == "wiki-navigation")
    assert wiki.state == EpistemicState.NONE

    page = render_html(artifact)
    assert "Do not infer" in page
    assert "<code>contracts/</code>" in page
    assert "repository-wide contract authority" in page
    assert "local wiki" in page
    assert "navigation authority" in page
