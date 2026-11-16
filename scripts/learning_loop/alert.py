"""File one agent-fixable failure of the loop itself as a keyed concern (no push).

Implements: feedback-loop-notices/loop-failures-are-concerns

Replaces the loop's agent-severity alerts that went through the Project Meta notice scripts (retirement plan, slice 2).
"""
from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

CONCERN_ISSUE = Path(__file__).resolve().parents[1] / "concern_issue.py"
RULE_REPO = os.environ.get("FEEDBACK_RULE_REPO", "BrianMills2718/agentic-engineering-system-canonical")


def file_alert(key: str, source: str, title: str, body: str, runner=subprocess.run) -> int:
    """Open or update the concern ``key``; return the adapter's exit code (the loop does not stop on it)."""
    cp = runner([sys.executable, str(CONCERN_ISSUE), "open", "--repo", RULE_REPO, "--key", key, "--source", source,
                 "--title", title, "--body", body, "--occurrence", dt.date.today().isoformat(),
                 "--no-run-claim", "failure of the loop itself; diagnoses no run"],
                capture_output=True, text=True, timeout=120)
    return cp.returncode
