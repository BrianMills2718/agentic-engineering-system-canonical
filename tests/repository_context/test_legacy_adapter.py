import subprocess

from agentic_engineering_system.repository_context.models import AuthorityRole, EpistemicState
from agentic_engineering_system.repository_context.resolver import RepositoryContextResolver


def test_package_and_contract_authority_require_positive_evidence(repo_factory):
    readme = (
        "# demo_pkg\n"
        "Shared typed data contracts.\n"
        "Ownership source: `docs/ops/CAPABILITY_DECOMPOSITION.md`.\n"
    )
    pyproject = (
        "[project]\n"
        "name='demo_pkg'\n"
        "[tool.setuptools.packages.find]\n"
        "where=['src']\n"
    )
    repo = repo_factory(readme=readme, pyproject=pyproject)
    (repo / "src" / "demo_pkg").mkdir(parents=True)
    (repo / "src" / "demo_pkg" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "contracts").mkdir()
    (repo / "contracts" / "README.md").write_text("not authority", encoding="utf-8")
    (repo / "docs" / "ops").mkdir(parents=True)
    (repo / "docs" / "ops" / "CAPABILITY_DECOMPOSITION.md").write_text(
        "# Ownership\nThis is the source of record for demo_pkg ownership.\n"
        "demo_pkg owns shared typed contract models.\n",
        encoding="utf-8",
    )
    # Physical existence alone must not promote a wiki to semantic navigation authority.
    (repo / "wiki").mkdir()
    (repo / "wiki" / "index.md").write_text("# Unrouted wiki\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "add surfaces"], check=True)

    artifact = RepositoryContextResolver(repo).resolve()

    implementation = next(item for item in artifact.authorities if item.role == AuthorityRole.IMPLEMENTATION)
    contract = next(item for item in artifact.authorities if item.role == AuthorityRole.CONTRACT)
    ownership = next(item for item in artifact.authorities if item.role == AuthorityRole.OWNERSHIP)
    assert implementation.locations == ("src/demo_pkg/",)
    assert contract.locations == ("src/demo_pkg/",)
    assert contract.state == EpistemicState.OBSERVED
    assert "contracts/" not in contract.locations
    assert ownership.locations == ("docs/ops/CAPABILITY_DECOMPOSITION.md",)
    assert artifact.navigation.locations == ("README.md",)
    assert not any(
        item.role == AuthorityRole.NAVIGATION and "wiki/index.md" in item.locations
        for item in artifact.authorities
    )
    wiki = next(item for item in artifact.concern_roots if item.concern == "wiki-navigation")
    assert wiki.state == EpistemicState.NONE
    contracts_root = next(item for item in artifact.concern_roots if item.concern == "contracts-root")
    assert contracts_root.state == EpistemicState.NONE
