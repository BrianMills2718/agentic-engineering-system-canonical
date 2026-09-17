from agentic_engineering_system.repository_context.models import AuthorityRole, EpistemicState, ResolutionStatus
from agentic_engineering_system.repository_context.resolver import RepositoryContextResolver


def test_malformed_manifest_blocks_without_legacy_fallback(repo_factory):
    repo = repo_factory(
        readme="# repo\n",
        manifest="schema_version: '0.1-pilot'\nauthorities: [bad\n",
    )
    artifact = RepositoryContextResolver(repo).resolve()
    assert artifact.resolution_status == ResolutionStatus.ERROR
    assert artifact.navigation.state == EpistemicState.ERROR
    assert any("retry" in item.reason.lower() for item in artifact.unresolved)
    assert not any(item.state == EpistemicState.OBSERVED for item in artifact.authorities)


def test_valid_manifest_missing_contract_role_stays_none(repo_factory):
    repo = repo_factory(
        manifest="schema_version: '0.1-pilot'\nnavigation: {}\nauthorities:\n  normative_roots: []\n"
    )
    artifact = RepositoryContextResolver(repo).resolve()
    contract = next(item for item in artifact.authorities if item.role == AuthorityRole.CONTRACT)
    assert contract.state == EpistemicState.NONE
    assert contract.locations == ()
