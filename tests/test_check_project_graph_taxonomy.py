"""Tests for PROJECT_GRAPH.json taxonomy validation."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


AES_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = AES_ROOT / "scripts" / "check_project_graph_taxonomy.py"


def _record(**overrides: object) -> dict:
    """Build a valid minimal project graph record."""
    record = {
        "id": "sample",
        "name": "Sample",
        "path": None,
        "github_repo": None,
        "status": "deleted",
        "domains": [],
        "tech": [],
        "capabilities": [],
        "depends_on": [],
        "superseded_by": None,
        "supersedes": [],
        "tags": [],
        "one_liner": "A concise sample project record.",
        "portfolio_area": "data-reference",
        "utility_tags": [
            "area:data-reference",
            "status:deleted",
            "pointer-record",
            "local-only",
        ],
    }
    record.update(overrides)
    return record


def _run(graph_path: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    """Run the taxonomy checker against a fixture graph path."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--project-graph", str(graph_path), "--json", *extra_args],
        cwd=AES_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_valid_fixture(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([_record()]), encoding="utf-8")

    result = _run(graph)

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["errors"] == []


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_human_project_with_repository_manifest_pointer(tmp_path: Path) -> None:
    """Plan 251 permits non-filesystem project identity without pointer semantics."""
    graph = tmp_path / "PROJECT_GRAPH.json"
    records = [
        _record(
            id="owner",
            path=str(tmp_path / "owner"),
            status="active",
            record_kind="repository",
            utility_tags=["area:data-reference", "status:active"],
        ),
        _record(
            id="human-project",
            path=None,
            status="active",
            record_kind="project",
            workspace_slug="human-project",
            membership_manifest={"repository_id": "owner", "path": "project-membership.yaml"},
            utility_tags=["area:data-reference", "status:active"],
        ),
    ]
    graph.write_text(json.dumps(records), encoding="utf-8")

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["hard_errors"] == []


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_unsafe_human_project_pointer(tmp_path: Path) -> None:
    """Plan 251 keeps machine paths out of durable project composition pointers."""
    graph = tmp_path / "PROJECT_GRAPH.json"
    records = [
        _record(
            id="owner",
            path=str(tmp_path / "owner"),
            status="active",
            record_kind="repository",
            utility_tags=["area:data-reference", "status:active"],
        ),
        _record(
            id="human-project",
            path=None,
            status="active",
            record_kind="project",
            workspace_slug="human-project",
            membership_manifest={"repository_id": "owner", "path": "../outside.yaml"},
            utility_tags=["area:data-reference", "status:active"],
        ),
    ]
    graph.write_text(json.dumps(records), encoding="utf-8")

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 1
    assert "membership_manifest path must be repository-relative" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_unknown_portfolio_area(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([_record(portfolio_area="misc")]), encoding="utf-8")

    result = _run(graph)

    assert result.returncode == 1
    assert "unknown portfolio_area" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_unknown_organization_metadata(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    path=str(tmp_path / "missing-project"),
                    source="somewhere",
                    physical_bucket="junk",
                    organization_status="maybe",
                    portfolio_tier="excellent",
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 1
    assert "unknown source" in result.stdout
    assert "unknown physical_bucket" in result.stdout
    assert "unknown organization_status" in result.stdout
    assert "unknown portfolio_tier" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_invalid_repository_governance(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    repository_governance={
                        "owner_class": "unknown",
                        "approved_remote_owners": "BrianMills2718",
                        "mutation_authority": "rewrite_everything",
                        "publication_authority": "always",
                        "review": {
                            "reviewed_by": "",
                            "reviewed_at": "July 25",
                            "evidence": [],
                        },
                    }
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 1
    assert "unknown repository_governance.owner_class" in result.stdout
    assert "approved_remote_owners must be a list" in result.stdout
    assert "unknown repository_governance.mutation_authority" in result.stdout
    assert "unknown repository_governance.publication_authority" in result.stdout
    assert "review.reviewed_by must be a non-empty string" in result.stdout
    assert "review.reviewed_at must be an ISO date" in result.stdout
    assert "review.evidence must be a non-empty list" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_reviewed_repository_governance(tmp_path: Path) -> None:
    """A repository grant includes explicit ownership-review evidence."""
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    repository_governance={
                        "owner_class": "brian",
                        "approved_remote_owners": ["BrianMills2718"],
                        "mutation_authority": "normal_push",
                        "publication_authority": "recoverable_git",
                        "review": {
                            "reviewed_by": "brian",
                            "reviewed_at": "2026-07-25",
                            "evidence": ["Brian confirmed ownership and publication authority."],
                        },
                    }
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["errors"] == []


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_contained_repository_topology(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps([_record(repository_topology={"mode": "contained"})]),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["hard_errors"] == []


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_reviewed_portable_repository_metadata(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    path=str(tmp_path / "missing-project"),
                    record_kind="repository",
                    workspace_home="code-active",
                    workspace_slug="sample-project",
                    default_branch="main",
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 0
    assert json.loads(result.stdout)["hard_errors"] == []


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_unsafe_or_ambiguous_portable_repository_metadata(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    id="first",
                    record_kind="repository",
                    workspace_home="code-active",
                    workspace_slug="same-name",
                    default_branch="main",
                ),
                _record(
                    id="second",
                    record_kind="repository",
                    workspace_home="code-active",
                    workspace_slug="same-name",
                    default_branch="bad branch",
                ),
                _record(
                    id="unsafe",
                    record_kind="data",
                    workspace_slug="../escape",
                    default_branch="-invalid",
                ),
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert any("duplicate portable destination" in error for error in payload["hard_errors"])
    assert any("workspace_slug must be" in error for error in payload["hard_errors"])
    assert any("workspace_slug requires record_kind" in error for error in payload["hard_errors"])
    assert any("default_branch must be" in error for error in payload["hard_errors"])


@pytest.mark.req("project-graph-taxonomy/hard-errors-block")
def test_hard_mode_rejects_malformed_repository_topology(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(id="not-object", repository_topology="contained"),
                _record(
                    id="unknown-mode",
                    repository_topology={"mode": "containned", "exception": True},
                ),
                _record(id="missing-mode", repository_topology={}),
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["blocking_ok"] is False
    assert "not-object: repository_topology must be an object" in payload["hard_errors"]
    assert "unknown-mode: unknown repository_topology.mode 'containned'" in payload["hard_errors"]
    assert "unknown-mode: unknown repository_topology.exception" in payload["hard_errors"]
    assert "missing-mode: unknown repository_topology.mode None" in payload["hard_errors"]


@pytest.mark.req("project-graph-taxonomy/hard-errors-block")
def test_hard_mode_blocks_unreviewed_repository_governance(tmp_path: Path) -> None:
    """Governance grants without review evidence fail the hard check."""
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    repository_governance={
                        "owner_class": "brian",
                        "approved_remote_owners": ["BrianMills2718"],
                        "mutation_authority": "normal_push",
                        "publication_authority": "recoverable_git",
                    }
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["blocking_ok"] is False
    assert "repository_governance.review must be an object" in result.stdout


@pytest.mark.req("project-graph-taxonomy/hard-errors-block")
def test_hard_mode_reports_unknown_organization_metadata_without_blocking(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    path=str(tmp_path / "missing-project"),
                    source="somewhere",
                    physical_bucket="junk",
                    organization_status="maybe",
                    portfolio_tier="excellent",
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["blocking_ok"] is True
    assert payload["hard_errors"] == []
    assert len(payload["measured_errors"]) == 4


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_pointer_only_record_without_physical_bucket(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    source="pointer",
                    record_kind="pointer",
                    organization_status="pointer-only",
                    portfolio_tier="none",
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph)

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["errors"] == []


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_workspace_home_contract_errors_are_measured(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    id="pointer-home",
                    source="pointer",
                    record_kind="pointer",
                    workspace_home="code-active",
                    organization_status="pointer-only",
                ),
                _record(
                    id="data-home",
                    path=str(tmp_path / "data"),
                    status="dormant",
                    record_kind="data",
                    workspace_home="code-inactive",
                    organization_status="needs-move",
                    utility_tags=["area:data-reference", "status:dormant"],
                    minimal_record_ok=True,
                ),
                _record(
                    id="nested-home",
                    path=str(tmp_path / "nested"),
                    status="dormant",
                    record_kind="nested-project",
                    workspace_home="central-archive",
                    organization_status="needs-move",
                    utility_tags=["area:data-reference", "status:dormant"],
                    minimal_record_ok=True,
                ),
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["blocking_ok"] is True
    assert "pointer-home: pointer record must omit workspace_home" in payload["measured_errors"]
    assert "pointer-home: code workspace_home requires record_kind 'repository'" in payload["measured_errors"]
    assert "data-home: code workspace_home requires record_kind 'repository'" in payload["measured_errors"]
    assert "nested-home: nested-project record must inherit its parent workspace home" in payload["measured_errors"]


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_needs_move_requires_explicit_move_metadata(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    id="missing-kind",
                    path=str(tmp_path / "missing-kind"),
                    status="dormant",
                    organization_status="needs-move",
                    utility_tags=["area:data-reference", "status:dormant"],
                    minimal_record_ok=True,
                ),
                _record(
                    id="missing-home",
                    path=str(tmp_path / "missing-home"),
                    status="dormant",
                    record_kind="repository",
                    organization_status="needs-move",
                    utility_tags=["area:data-reference", "status:dormant"],
                    minimal_record_ok=True,
                ),
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["blocking_ok"] is True
    assert "missing-kind: needs-move requires explicit record_kind" in payload["measured_errors"]
    assert "missing-home: needs-move repository requires workspace_home" in payload["measured_errors"]


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_pointer_only_record_with_physical_bucket_is_measured(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    source="pointer",
                    physical_bucket="archives/data-reference",
                    organization_status="pointer-only",
                    portfolio_tier="none",
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["blocking_ok"] is True
    assert payload["hard_errors"] == []
    assert payload["measured_errors"] == [
        "sample: pointer-only/null-path record must omit physical_bucket"
    ]


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_valid_branch_policy(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    branch_policy={
                        "canonical_checkout": {
                            "branch": "feature/published",
                            "reason": "Intentional publication snapshot.",
                        },
                        "default_branch": {
                            "branch": "20251008_mvp",
                            "reason": "Dated MVP branch is intentional until migration.",
                        },
                        "wiki_publication": {
                            "branch": "feature/published",
                            "reason": "Wiki artifacts are intentionally sourced here.",
                        },
                    },
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 0


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_malformed_branch_policy(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    branch_policy={
                        "unknown_scope": {"branch": "x", "reason": "No."},
                        "canonical_checkout": {"branch": "", "reason": ""},
                    },
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 1
    assert "unknown branch_policy scope" in result.stdout
    assert "branch_policy.canonical_checkout.branch must be non-empty" in result.stdout
    assert "branch_policy.canonical_checkout.reason must be non-empty" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_missing_required_utility_tags(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([_record(utility_tags=["pointer-record"])]), encoding="utf-8")

    result = _run(graph)

    assert result.returncode == 1
    assert "utility_tags missing area:data-reference, status:deleted" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_overlong_one_liner(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([_record(one_liner="x" * 221)]), encoding="utf-8")

    result = _run(graph)

    assert result.returncode == 1
    assert "one_liner exceeds 220 chars" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_dangling_depends_on(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps([_record(depends_on=["nonexistent-project"])]),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 1
    assert "depends_on references unknown id" in result.stdout


@pytest.mark.req("project-graph-taxonomy/hard-errors-block")
def test_hard_mode_blocks_dangling_depends_on(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps([_record(depends_on=["nonexistent-project"])]),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["blocking_ok"] is False
    assert payload["hard_errors"] == ["sample: depends_on references unknown id 'nonexistent-project'"]


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_dangling_supersedes(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps([_record(supersedes=["missing-old-project"])]),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 1
    assert "supersedes references unknown id" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_dangling_superseded_by(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps([_record(superseded_by="no-such-project")]),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 1
    assert "superseded_by references unknown id" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_valid_cross_references(tmp_path: Path) -> None:
    old = _record(id="old-proj", superseded_by="new-proj")
    new = _record(
        id="new-proj",
        supersedes=["old-proj"],
        utility_tags=["area:data-reference", "status:deleted"],
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([old, new]), encoding="utf-8")

    result = _run(graph)

    payload = json.loads(result.stdout)
    dangling = [e for e in payload["errors"] if "unknown id" in e]
    assert dangling == [], f"Unexpected dangling errors: {dangling}"


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_sparse_active_record(tmp_path: Path) -> None:
    sparse = _record(
        status="active",
        one_liner="Short.",
        capabilities=[],
        tags=["area:data-reference"],
        utility_tags=["area:data-reference", "status:active"],
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([sparse]), encoding="utf-8")

    result = _run(graph)

    assert result.returncode == 1
    assert "capabilities" in result.stdout or "tags" in result.stdout or "one_liner" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_minimal_record_ok_tag_exempts_sparse_check(tmp_path: Path) -> None:
    exempt = _record(
        status="active",
        one_liner="Short.",
        capabilities=[],
        tags=["area:data-reference", "status:active", "minimal-record-ok"],
        utility_tags=["area:data-reference", "status:active"],
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([exempt]), encoding="utf-8")

    result = _run(graph)

    payload = json.loads(result.stdout)
    sparse_errors = [e for e in payload["errors"] if "capabilities" in e or "tags (need" in e or "one_liner" in e]
    assert sparse_errors == [], f"Unexpected sparse errors on exempt record: {sparse_errors}"


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_stale_github_remote(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "remote", "add", "origin", "https://github.com/BrianMills2718/right.git"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(
                    path=str(repo),
                    github_repo="BrianMills2718/wrong",
                    status="active",
                    utility_tags=[
                        "area:data-reference",
                        "status:active",
                        "git-backed",
                        "github-linked",
                    ],
                )
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph)

    assert result.returncode == 1
    assert "github_repo does not match origin remote" in result.stdout


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_rejects_mojibake_in_any_graph_string(tmp_path: Path) -> None:
    """#2308: cp1252-garbled UTF-8 (em dash -> 'a-hat euro quote') is a hard error."""
    garbled = "Research engine â€” multi-model; arrow Oâ†’A"
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(
        json.dumps(
            [
                _record(one_liner=garbled),
                _record(
                    id="nested",
                    repository_governance={"review": {"evidence": ["Weâ€™d"]}},
                ),
            ]
        ),
        encoding="utf-8",
    )

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 1, result.stdout
    hard = json.loads(result.stdout)["hard_errors"]
    assert any(e.startswith("sample: mojibake in one_liner") and "—" in e for e in hard), hard
    assert any(e.startswith("nested: mojibake in repository_governance.review.evidence[0]") for e in hard), hard


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_accepts_correct_unicode_and_accented_text(tmp_path: Path) -> None:
    """Negative fixture: real em dash, arrows, emoji, and accents are not mojibake."""
    clean = "Research engine — multi-model → synthesis \U0001f64c café École naïve Ã"
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([_record(one_liner=clean)]), encoding="utf-8")

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["hard_errors"] == []


def _git_checkout_with_origin(path: Path, origin_url: str) -> Path:
    """Create a real git repository whose origin remote is ``origin_url``."""
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "remote", "add", "origin", origin_url], check=True)
    return path


@pytest.mark.req("project-graph-taxonomy/hard-errors-block")
def test_hard_mode_blocks_github_repo_that_mismatches_origin(tmp_path: Path) -> None:
    """A stale github_repo (AES#672) must block `--fail-on hard`, not just be measured."""
    checkout = _git_checkout_with_origin(
        tmp_path / "workbench", "git@github.com-personal:BrianMills2718/workbench.git"
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    record = _record(
        path=str(checkout),
        status="active",
        github_repo="BrianMills2718/projects-backup-workbench-cdfee35f",
    )
    graph.write_text(json.dumps([record]), encoding="utf-8")

    result = _run(graph, "--fail-on", "hard")

    assert result.returncode == 1
    hard_errors = json.loads(result.stdout)["hard_errors"]
    assert any(
        "github_repo does not match origin remote" in error and "BrianMills2718/workbench" in error
        for error in hard_errors
    ), hard_errors


@pytest.mark.req("project-graph-taxonomy/hard-errors-block")
def test_hard_mode_accepts_github_repo_matching_origin(tmp_path: Path) -> None:
    """The same checkout with a matching github_repo produces no origin hard error."""
    checkout = _git_checkout_with_origin(
        tmp_path / "workbench", "https://github.com/BrianMills2718/workbench.git"
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    record = _record(path=str(checkout), status="active", github_repo="BrianMills2718/workbench")
    graph.write_text(json.dumps([record]), encoding="utf-8")

    result = _run(graph, "--fail-on", "hard")

    hard_errors = json.loads(result.stdout)["hard_errors"]
    assert not any("origin remote" in error for error in hard_errors), hard_errors


@pytest.mark.req("project-graph-taxonomy/hard-errors-block")
def test_hard_mode_accepts_ssh_url_with_host_alias(tmp_path: Path) -> None:
    """tbench-task-study's origin is ssh://git@github-personal/owner/repo.git; it was misread as a mismatch."""
    checkout = _git_checkout_with_origin(
        tmp_path / "workbench", "ssh://git@github-personal/BrianMills2718/workbench.git"
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    record = _record(path=str(checkout), status="active", github_repo="BrianMills2718/workbench")
    graph.write_text(json.dumps([record]), encoding="utf-8")

    result = _run(graph, "--fail-on", "hard")

    hard_errors = json.loads(result.stdout)["hard_errors"]
    assert not any("origin remote" in error for error in hard_errors), hard_errors


@pytest.mark.req("project-graph-taxonomy/records-are-validated")
def test_origin_check_ignores_git_dir_inherited_from_a_hook(tmp_path: Path) -> None:
    """Under a pre-commit hook GIT_DIR names the committing repo; each checkout must still be read."""
    checkout = _git_checkout_with_origin(
        tmp_path / "workbench", "https://github.com/BrianMills2718/workbench.git"
    )
    committing = _git_checkout_with_origin(
        tmp_path / "committing", "https://github.com/BrianMills2718/project-meta.git"
    )
    graph = tmp_path / "PROJECT_GRAPH.json"
    record = _record(path=str(checkout), status="active", github_repo="BrianMills2718/workbench")
    graph.write_text(json.dumps([record]), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--project-graph", str(graph), "--json", "--fail-on", "hard"],
        cwd=AES_ROOT,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "GIT_DIR": str(committing / ".git"), "GIT_WORK_TREE": str(committing)},
    )

    hard_errors = json.loads(result.stdout)["hard_errors"]
    assert not any("origin remote" in error for error in hard_errors), hard_errors


@pytest.mark.req("project-graph-taxonomy/graph-path-is-configured")
def test_default_graph_path_comes_from_the_environment(tmp_path: Path) -> None:
    graph = tmp_path / "PROJECT_GRAPH.json"
    graph.write_text(json.dumps([_record()]), encoding="utf-8")
    env = {**os.environ, "PROJECT_GRAPH": str(graph)}

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"], cwd=tmp_path, capture_output=True, text=True, env=env, check=False
    )

    assert json.loads(result.stdout)["records"] == 1
