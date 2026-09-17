import json
import pytest

from agentic_engineering_system.repository_context.resolver import resolve_repository_context


def test_revision_expectation_is_enforced(repo_factory):
    repo = repo_factory(readme="# x")
    with pytest.raises(ValueError, match="revision mismatch"):
        resolve_repository_context(repo, expect_revision="deadbeef")


def test_json_is_deterministic_parseable_artifact(repo_factory):
    repo = repo_factory(readme="# x")
    artifact = resolve_repository_context(repo)
    payload = json.loads(artifact.model_dump_json())
    assert payload["repository_id"].startswith("repo-")
    assert payload["schema_version"] == "0.1"
