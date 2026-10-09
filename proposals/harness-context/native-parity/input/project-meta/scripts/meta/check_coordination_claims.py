#!/usr/bin/env python3
"""Compatibility facade for package-backed coordination claims."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any


def _find_repo_root() -> Path:
    """Resolve the nearest ancestor that contains the installed support package."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "enforced_planning").is_dir():
            return parent
    import importlib.util
    if importlib.util.find_spec("enforced_planning") is not None:
        for _ancestor in Path(__file__).resolve().parents:
            if (_ancestor / ".git").exists():
                return _ancestor
        return Path(__file__).resolve().parents[1]
    raise RuntimeError("Unable to locate repo root containing enforced_planning/")


repo_root = _find_repo_root()
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from enforced_planning import coordination_claims as _impl  # noqa: E402


CLAIMS_DIR = _impl.CLAIMS_DIR
DEFAULT_TTL_HOURS = _impl.DEFAULT_TTL_HOURS
LIVE_STATUSES = _impl.LIVE_STATUSES
COMPLETED_STATUSES = _impl.COMPLETED_STATUSES
CLAIM_TYPES = _impl.CLAIM_TYPES
STRICT_LIVE_METADATA_CLAIM_TYPES = _impl.STRICT_LIVE_METADATA_CLAIM_TYPES

ClaimRecord = _impl.ClaimRecord
ClaimInteraction = _impl.ClaimInteraction
ClaimCheckResult = _impl.ClaimCheckResult

_claim_filename = _impl._claim_filename
_normalize_repo_path = _impl._normalize_repo_path
_paths_overlap = _impl._paths_overlap
requires_work_graph = _impl.requires_work_graph


def _sync_runtime_config() -> None:
    """Keep the package module aligned with script-level monkeypatches."""
    _impl.CLAIMS_DIR = CLAIMS_DIR


def _cli_value(argv: list[str], flag: str) -> str | None:
    """Return one long-option value without trying to replace argparse."""
    for index, item in enumerate(argv):
        if item == flag:
            return argv[index + 1] if index + 1 < len(argv) else None
        prefix = f"{flag}="
        if item.startswith(prefix):
            return item[len(prefix) :]
    return None


def _git_common_dir(path: Path) -> Path | None:
    """Return the absolute Git common dir for one checkout/worktree."""
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return Path(result.stdout.strip()).expanduser().resolve(strict=False)


def _validate_claim_repo_root(argv: list[str]) -> None:
    """Reject the worktree-as-repo-root ambiguity before a claim is persisted.

    For a linked worktree, ``--worktree-path`` names the physical lane while
    ``--repo-root`` must name the canonical checkout whose ``.git`` directory is
    the shared common directory. Passing the worktree path for both fields used
    to create a claim that later failed every edit with opaque ``no_exact_claim``.
    """
    if "--claim" not in argv:
        return
    repo_value = _cli_value(argv, "--repo-root")
    worktree_value = _cli_value(argv, "--worktree-path")
    if not repo_value or not worktree_value:
        return

    supplied_repo = Path(repo_value).expanduser().resolve(strict=False)
    supplied_worktree = Path(worktree_value).expanduser().resolve(strict=False)
    repo_common = _git_common_dir(supplied_repo)
    worktree_common = _git_common_dir(supplied_worktree)
    if repo_common is None or worktree_common is None:
        return

    expected_common = (supplied_repo / ".git").resolve(strict=False)
    if repo_common != expected_common or worktree_common != repo_common:
        raise ValueError(
            "--repo-root must name the canonical checkout root, not the linked worktree. "
            f"Received repo_root={supplied_repo} and worktree_path={supplied_worktree}; "
            f"the worktree's shared Git common dir is {worktree_common}. "
            "Use the canonical checkout containing that .git directory as --repo-root."
        )


def normalize_claim(data: dict[str, Any], *, source_file: str | None = None) -> ClaimRecord | None:
    """Delegate normalized claim loading to the package module."""
    return _impl.normalize_claim(data, source_file=source_file)


def check_claims(project: str | None = None, *, claims_dir: Path | None = None) -> list[ClaimRecord]:
    """Delegate live-claim loading with an optional explicit registry."""
    _sync_runtime_config()
    return _impl.check_claims(project, claims_dir=claims_dir)


def evaluate_claim(candidate: ClaimRecord, *, active_claims: list[ClaimRecord] | None = None) -> ClaimCheckResult:
    """Delegate candidate evaluation while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.evaluate_claim(candidate, active_claims=active_claims)


def build_candidate_claim(**kwargs: Any) -> ClaimRecord:
    """Delegate candidate claim construction to the package module."""
    return _impl.build_candidate_claim(**kwargs)


def validate_native_session_binding(agent: str, session_id: str | None) -> None:
    """Expose native runtime/session binding through the legacy facade."""

    _impl.validate_native_session_binding(agent, session_id)


def claim_health_issues(claim: ClaimRecord) -> list[str]:
    """Expose claim health diagnostics through the legacy script surface."""
    return _impl.claim_health_issues(claim)


def claim_health_status(claim: ClaimRecord) -> str:
    """Expose claim health classification through the legacy script surface."""
    return _impl.claim_health_status(claim)


def normalize_plan_identity(plan_ref: str | None) -> str | None:
    """Expose normalized numbered-plan identity through the legacy surface."""

    return _impl.normalize_plan_identity(plan_ref)


def claim_hierarchy_issues(
    claim: ClaimRecord,
    *,
    active_claims: list[ClaimRecord],
) -> list[str]:
    """Expose root/child hierarchy diagnostics through the legacy surface."""

    return _impl.claim_hierarchy_issues(claim, active_claims=active_claims)


def claim_lifecycle_issues(claim: ClaimRecord) -> list[str]:
    """Expose stale-lifecycle diagnostics through the legacy script surface."""
    return _impl.claim_lifecycle_issues(claim)


def claim_runtime_status(
    claim: ClaimRecord,
    *,
    active_claims: list[ClaimRecord] | None = None,
) -> str:
    """Expose combined stale/weak/healthy runtime classification."""
    return _impl.claim_runtime_status(claim, active_claims=active_claims)


def claim_enforcement_issues(claim: ClaimRecord) -> list[dict[str, str]]:
    """Expose blocking merged-ownership diagnostics through the legacy script surface."""

    return _impl.claim_enforcement_issues(claim)


def claim_liveness_issues(claim: ClaimRecord, *, now: Any | None = None) -> list[str]:
    """Expose heartbeat-backed liveness diagnostics."""
    return _impl.claim_liveness_issues(claim, now=now)


def hydrate_missing_session_ids(*args: Any, **kwargs: Any) -> tuple[int, list[str], str]:
    """Delegate session-id hydration while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.hydrate_missing_session_ids(*args, **kwargs)


def create_claim(*args: Any, **kwargs: Any) -> tuple[bool, str]:
    """Delegate claim creation while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.create_claim(*args, **kwargs)


def release_claim(*args: Any, **kwargs: Any) -> tuple[bool, str]:
    """Delegate claim release while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.release_claim(*args, **kwargs)


def unregistered_claim_files() -> list[str]:
    """Delegate unregistered-format claim detection while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.unregistered_claim_files()


def prune_expired(*args: Any, **kwargs: Any) -> tuple[int, list[str]]:
    """Delegate claim pruning while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.prune_expired(*args, **kwargs)


def prune_stale(*args: Any, **kwargs: Any) -> tuple[int, list[str]]:
    """Delegate stale-claim pruning while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.prune_stale(*args, **kwargs)


def prune_completed(*args: Any, **kwargs: Any) -> tuple[int, list[str]]:
    """Delegate completed-claim pruning while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.prune_completed(*args, **kwargs)


def heartbeat_claims(*args: Any, **kwargs: Any) -> tuple[int, list[str], str, str]:
    """Delegate heartbeat refresh while honoring script-level CLAIMS_DIR overrides."""
    _sync_runtime_config()
    return _impl.heartbeat_claims(*args, **kwargs)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Expose CLI argument parsing through the legacy script surface."""
    return _impl.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the package-backed coordination-claims CLI."""
    _sync_runtime_config()
    resolved_argv = list(sys.argv[1:] if argv is None else argv)
    _validate_claim_repo_root(resolved_argv)
    return _impl.main(resolved_argv)


if __name__ == "__main__":
    raise SystemExit(main())
