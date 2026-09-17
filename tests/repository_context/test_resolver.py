from pathlib import Path
import subprocess

from agentic_engineering_system.repository_context.models import EpistemicState, ResolutionStatus
from agentic_engineering_system.repository_context.resolver import RepositoryContextResolver


def git_repo(tmp_path: Path, files: dict[str, str]) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    for name, content in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
    return repo


def test_legacy_resolution_is_source_bound(tmp_path: Path):
    repo = git_repo(tmp_path, {
        "README.md": "# Example\n",
        "pyproject.toml": "[tool.setuptools]\npackage-dir = {\"\" = \"src\"}\n[tool.setuptools.packages.find]\nwhere = [\"src\"]\n",
        "docs/ops/CAPABILITY_DECOMPOSITION.md": "# Ownership\n",
    })
    artifact = RepositoryContextResolver(repo).resolve()
    assert artifact.navigation.state == EpistemicState.OBSERVED
    assert any(item.role.value == "implementation" for item in artifact.authorities)


def test_malformed_authoritative_manifest_blocks_legacy_fallback(tmp_path: Path):
    repo = git_repo(tmp_path, {
        "README.md": "# Example\n",
        ".agentic/repo.yaml": "authorities: [not-a-mapping]\n",
    })
    artifact = RepositoryContextResolver(repo).resolve()
    assert artifact.resolution_status == ResolutionStatus.ERROR
    assert artifact.navigation.state == EpistemicState.ERROR
    assert "legacy fallback is disabled" in artifact.navigation.summary


def test_valid_manifest_missing_navigation_stays_none(tmp_path: Path):
    repo = git_repo(tmp_path, {
        ".agentic/repo.yaml": "schema_version: '0.1-pilot'\nauthorities: {}\n",
        "README.md": "# Example\n",
    })
    artifact = RepositoryContextResolver(repo).resolve()
    assert artifact.navigation.state == EpistemicState.NONE
    assert artifact.resolution_status == ResolutionStatus.PARTIAL


def test_expected_revision_mismatch_is_error(tmp_path: Path):
    repo = git_repo(tmp_path, {"README.md": "# Example\n"})
    artifact = RepositoryContextResolver(repo).resolve("0000000")
    assert artifact.resolution_status == ResolutionStatus.ERROR
    assert "revision mismatch" in artifact.navigation.summary
