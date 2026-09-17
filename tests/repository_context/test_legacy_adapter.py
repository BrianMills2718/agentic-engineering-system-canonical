import subprocess

from agentic_engineering_system.repository_context.models import AuthorityRole
from agentic_engineering_system.repository_context.resolver import resolve_repository_context


def test_package_and_contract_authority_require_positive_evidence(repo_factory):
    readme = "# pkg\nShared typed data contracts.\nSuggested: `docs/ops/CAPABILITY_DECOMPOSITION.md`\n"
    pyproject = "[project]\nname='demo_pkg'\n[tool.setuptools.packages.find]\nwhere=['src']\n"
    repo = repo_factory(readme=readme, pyproject=pyproject)
    (repo / "src" / "demo_pkg").mkdir(parents=True)
    (repo / "src" / "demo_pkg" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "contracts").mkdir()
    (repo / "contracts" / "README.md").write_text("not authority", encoding="utf-8")
    (repo / "docs" / "ops").mkdir(parents=True)
    (repo / "docs" / "ops" / "CAPABILITY_DECOMPOSITION.md").write_text("ownership", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "add surfaces"], check=True)
    artifact = resolve_repository_context(repo)
    implementation = next(item for item in artifact.authorities if item.role is AuthorityRole.IMPLEMENTATION)
    contract = next(item for item in artifact.authorities if item.role is AuthorityRole.CONTRACT)
    ownership = next(item for item in artifact.authorities if item.role is AuthorityRole.OWNERSHIP)
    assert implementation.locations == ("src/demo_pkg/",)
    assert contract.locations == ("src/demo_pkg/",)
    assert "contracts/" not in contract.locations
    assert ownership.locations == ("docs/ops/CAPABILITY_DECOMPOSITION.md",)
    assert artifact.navigation.locations == ("README.md",)
    assert any(item.subject == "wiki/index.md" for item in artifact.unresolved)
