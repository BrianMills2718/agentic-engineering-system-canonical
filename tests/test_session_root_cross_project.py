"""A session's open lane in another project must not block a new lane here.

On 2026-10-13 a session holding an agentic-engineering-system-canonical lane
was refused a project-meta lane ("Runtime session already owns an unresolved
root lane") although the two lanes cannot share files. Brian asked for the
gates that slow agents to be cut; a second root in the same project still
needs an explicit --allow-parallel.
"""

from __future__ import annotations

import pytest

from enforced_planning import coordination_claims as cc


def _claim(project: str, scope: str) -> cc.ClaimRecord:
    return cc.ClaimRecord(
        agent="claude-code", claimed_at=None, expires_at=None, projects=[project],
        scope=scope, intent="probe", claim_type="write", write_paths=[f"{scope}.py"],
        read_paths=[], worktree_path=None, repo_root=None, branch=scope,
        session_name=None, broader_goal=None, tracker_path=None, session_id="s1",
        heartbeat_at=None, status=sorted(cc.LIVE_STATUSES)[0], updated_at=None,
        parent_scope=None, notes=None, plan_ref=None, source_file=None, schema_version=2,
    )


def test_root_in_other_project_does_not_block() -> None:
    held = _claim("agentic-engineering-system-canonical", "lane-a")
    cc.validate_session_root_for_creation(_claim("project-meta", "lane-b"), active_claims=[held])


def test_second_root_in_same_project_still_needs_allow_parallel() -> None:
    held = _claim("project-meta", "lane-a")
    with pytest.raises(ValueError, match="already owns an unresolved root lane"):
        cc.validate_session_root_for_creation(_claim("project-meta", "lane-b"), active_claims=[held])
