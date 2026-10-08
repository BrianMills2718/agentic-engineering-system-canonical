"""S4: licence status comes from the Observation-to-Action evaluator (R-401), on the plan's fixtures."""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import licences as LC  # noqa: E402

pytestmark = pytest.mark.skipif(not (LC.METAMODEL / "evaluate.py").exists(),
                                reason="observation-to-action-metamodel checkout not present")

FIX = {"intent": "Prevent", "text": "fall back to a detached append when a lane step fails", "rests_on": ["r1"]}


def problem(sightings, basis="seen"):
    return {"id": "prob-stranded-lanes", "sightings": sightings,
            "analysis": {"cause_chain": [{"text": "the commit rule refused the tag", "basis": basis, "rests_on": ["r1"]}],
                         "fixes": [FIX]}}


def status(p, challenged=False, revoked=False):
    return LC.derive(LC.fixture_for(p, FIX, challenged, revoked))


def test_two_independent_sightings_and_a_seen_cause_license_the_fix():
    assert status(problem(2)) == "active"


def test_one_session_is_conditional():
    assert status(problem(1)) == "conditional"


def test_a_guessed_cause_never_licenses():
    assert status(problem(2, "guessed")) == "conditional"


def test_a_confirmed_challenge_unestablishes():
    assert status(problem(2), challenged=True) == "unestablished"


def test_recurrence_after_enforcement_revokes():
    assert status(problem(2), revoked=True) == "revoked"


def test_only_prevent_and_detect_fixes_get_licences():
    p = problem(2)
    p["analysis"]["fixes"].append({"intent": "Investigate", "text": "find out why", "rests_on": ["r1"]})
    assert [x["intent"] for x in LC.licences_for(p, False)] == ["Prevent"]
