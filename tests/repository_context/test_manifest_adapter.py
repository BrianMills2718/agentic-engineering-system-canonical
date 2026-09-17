from agentic_engineering_system.repository_context.models import AuthorityRole, SurfaceState
from agentic_engineering_system.repository_context.resolver import resolve_repository_context


def test_malformed_manifest_blocks_without_legacy_fallback(repo_factory):
    repo = repo_factory(readme="Contracts are here", manifest="authorities: [bad")
    artifact = resolve_repository_context(repo)
    assert artifact.resolution_status.value == "ERROR"
    assert artifact.navigation.state.value == "ERROR"
    assert any("retry" in item.reason.lower() for item in artifact.unresolved)
    assert not any(item.state.value == "OBSERVED" for item in artifact.authorities)


def test_valid_manifest_missing_contract_role_stays_none(repo_factory):
    repo = repo_factory(manifest="navigation: {}\nauthorities:\n  normative_roots: [docs/]\nconcerns: {}\n")
    artifact = resolve_repository_context(repo)
    contract = next(item for item in artifact.authorities if item.role is AuthorityRole.CONTRACT)
    assert contract.state is SurfaceState.NONE
