"""Helpers for explicit PROJECT_GRAPH branch-policy exceptions."""

from __future__ import annotations

from typing import Any


BRANCH_POLICY_SCOPES = frozenset(
    {
        "canonical_checkout",
        "default_branch",
        "wiki_publication",
    }
)


def branch_exception(record: dict[str, Any], scope: str) -> dict[str, Any] | None:
    """Return a validated branch exception mapping for a scope, if present."""
    policy = record.get("branch_policy")
    if not isinstance(policy, dict):
        return None
    exception = policy.get(scope)
    if not isinstance(exception, dict):
        return None
    return exception


def branch_exception_matches(record: dict[str, Any], scope: str, branch: str | None) -> bool:
    """Return whether a record explicitly permits this branch for this scope."""
    if branch is None:
        return False
    exception = branch_exception(record, scope)
    if exception is None:
        return False
    allowed_branch = exception.get("branch")
    reason = exception.get("reason")
    return allowed_branch == branch and isinstance(reason, str) and bool(reason.strip())
