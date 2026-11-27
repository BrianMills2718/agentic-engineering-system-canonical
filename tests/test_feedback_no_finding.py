"""Empty subagent lifecycle reports are kept locally and not filed as issues."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "learning_loop"))

import collect_feedback as CF  # noqa: E402  # the script folder joins sys.path just above


def _report(outcome, records=1, field="Subagent outcome"):
    return {"field": field, "records": [{}] * records, "subagent": {"outcome": outcome}}


def test_bare_lifecycle_states_have_no_finding():
    for outcome in CF.NO_FINDING:
        assert CF._has_no_finding(_report(outcome))


def test_failures_checks_and_feedback_are_still_filed():
    for outcome in ("failed", "cancelled", "verification_failed", "verified_fail", "verified_pass"):
        assert not CF._has_no_finding(_report(outcome))
    assert not CF._has_no_finding(_report("completed_unverified", records=2))
    assert not CF._has_no_finding({"field": "Feedback", "records": [{}]})
