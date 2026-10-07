"""Plans require trace reviews (Brian, 2026-10-07).

Every proposal declares whether its work runs a model, agent or pipeline. If it
does, the delta must carry a `trace_review` evidence requirement, and the
observation that assesses one must carry a TraceReview record: a reviewer who is
not the author, every step read, decisions followed back to their sources.

Planning cases mutate the whygame5 runner proposal used by test_planning.py.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from agentic_engineering_system.evidence import (
    EvidenceError,
    ObservationRecord,
    TraceReview,
    load_observations,
)
from agentic_engineering_system.planning import Proposal, validate_proposal
from agentic_engineering_system.records import load_target, parse_yaml_mapping

from test_planning import WHYGAME5_AES, _proposal_data, _violations, root  # noqa: F401  (fixture)


def _with_trace_review_er(data: dict[str, Any]) -> dict[str, Any]:
    """The runner proposal declaring a real run and carrying a routed trace_review requirement."""
    data["trace_review"] = {"runs_traced_work": True}
    sc = data["target_delta"]["add"]["success_criteria"][0]
    sc["evidence_requirements"].append({
        "id": "ER-WG5-007-02", "kind": "trace_review",
        "requirement": "A reviewer who did not write the runner reads one real run's trace end to end.",
    })
    data["target_delta"]["add"]["external_boundaries"] = [
        {"evidence_requirement_ref": "ER-WG5-007-02", "boundary": "an independent reviewer agent reads the trace"}]
    return data


# --------------------------------------------------------------------------- #
# planning
# --------------------------------------------------------------------------- #


def test_a_proposal_must_declare_whether_its_work_runs(root: Path) -> None:
    data = _proposal_data()
    del data["trace_review"]
    [v] = _violations(root, data)
    assert v.startswith("trace_review is missing")


def test_declaring_nothing_runs_needs_a_reason() -> None:
    data = _proposal_data()
    data["trace_review"] = {"runs_traced_work": False}
    with pytest.raises(ValidationError, match="needs a reason"):
        Proposal.model_validate(data)


def test_work_that_runs_needs_a_trace_review_requirement(root: Path) -> None:
    data = _proposal_data()
    data["trace_review"] = {"runs_traced_work": True}
    [v] = _violations(root, data)
    assert "no success criterion the delta adds or changes has an evidence requirement of kind trace_review" in v


def test_work_that_runs_validates_with_a_routed_trace_review_requirement(root: Path) -> None:
    v = validate_proposal(root, Proposal.model_validate(_with_trace_review_er(_proposal_data())))
    ers = v.target.evidence_requirements()
    assert ers["ER-WG5-007-02"][1].kind == "trace_review"


def test_a_trace_review_requirement_without_a_route_is_still_refused(root: Path) -> None:
    data = _with_trace_review_er(_proposal_data())
    del data["target_delta"]["add"]["external_boundaries"]
    [v] = _violations(root, data)
    assert "'ER-WG5-007-02'" in v and "has no route" in v


# --------------------------------------------------------------------------- #
# observations
# --------------------------------------------------------------------------- #

REVIEW: dict[str, Any] = {
    "trace_refs": ["qualitative_coding/project/0cbd41e8 (calls_2026-10-06.jsonl)"],
    "author": "session-a",
    "reviewer": "session-b",
    "steps_total": 6,
    "steps_read": 6,
    "models_and_settings": "deepseek-v4-flash, no reasoning, about 23 passages per call",
    "context_per_step": "one passage plus one neighbouring line before and after",
    "outputs_and_reasons": "code ids only; no reason or quote per decision",
    "decisions_checked": [
        {"decision": "turn 20 OUTCOME_NO_GAIN", "source": "Danziger p.24", "verdict": "correct"},
    ],
    "findings": [],
}


def _target_with_trace_review_er(tmp_path: Path):
    """The frozen whygame5 target with its first evidence requirement turned into a trace review."""
    text = (WHYGAME5_AES / "target.yaml").read_text(encoding="utf-8")
    target = load_target(WHYGAME5_AES / "target.yaml")
    er_id = target.success_criteria[0].evidence_requirements[0].id
    old_kind = target.success_criteria[0].evidence_requirements[0].kind
    path = tmp_path / "target.yaml"
    # Swap the kind of exactly that requirement (its id line is followed by its kind line).
    marker = f"id: {er_id}"
    head, tail = text.split(marker, 1)
    tail = tail.replace(f"kind: {old_kind}", "kind: trace_review", 1)
    path.write_text(head + marker + tail, encoding="utf-8")
    t = load_target(path)
    assert t.evidence_requirements()[er_id][1].kind == "trace_review"
    return t, er_id


def _observation(er_id: str, assessment: str, review: dict[str, Any] | None) -> str:
    import json

    obs: dict[str, Any] = {
        "schema_version": "aes.v0_2.observation.probe0",
        "observation_id": "OBS-TRACE-1",
        "subject_refs": [],
        "external_identity": "trace qualitative_coding/project/0cbd41e8",
        "observer": {"identity": "session-b"},
        "method": "read every call of the run's trace",
        "execution_state": "COMPLETED",
        "result": {"read": True},
        "produced_at": "2026-10-07T00:00:00+00:00",
        "assessments": [{"evidence_requirement_ref": er_id, "assessment": assessment,
                         "basis": "trace read end to end", "assessor": {"identity": "session-b"}}],
    }
    if review is not None:
        obs["trace_review"] = review
    return json.dumps(obs)  # JSON is YAML


def _load(tmp_path: Path, er_id: str, target, assessment: str, review: dict[str, Any] | None):
    d = tmp_path / "obs"
    d.mkdir(exist_ok=True)
    (d / "OBS-TRACE-1.yaml").write_text(_observation(er_id, assessment, review), encoding="utf-8")
    return load_observations(tmp_path, "obs", target)


def test_a_trace_review_assessment_without_a_record_is_refused(tmp_path: Path) -> None:
    target, er_id = _target_with_trace_review_er(tmp_path)
    with pytest.raises(EvidenceError, match="carries no trace_review record"):
        _load(tmp_path, er_id, target, "SUPPORTS", None)


def test_a_complete_review_with_no_wrong_decision_supports(tmp_path: Path) -> None:
    target, er_id = _target_with_trace_review_er(tmp_path)
    [obs] = _load(tmp_path, er_id, target, "SUPPORTS", REVIEW)
    assert obs.trace_review is not None and obs.trace_review.steps_read == 6


def test_supports_needs_every_step_read(tmp_path: Path) -> None:
    target, er_id = _target_with_trace_review_er(tmp_path)
    review = dict(REVIEW, steps_read=4)
    with pytest.raises(EvidenceError, match="only 4 of 6 trace steps were read"):
        _load(tmp_path, er_id, target, "SUPPORTS", review)


def test_supports_is_refused_when_a_checked_decision_was_wrong(tmp_path: Path) -> None:
    target, er_id = _target_with_trace_review_er(tmp_path)
    review = copy.deepcopy(REVIEW)
    review["decisions_checked"].append(
        {"decision": "turn 22 OUTCOME_NO_GAIN", "source": "Danziger p.25", "verdict": "wrong",
         "note": "a complaint about heavy boxes; Danziger counts her as succeeding"})
    with pytest.raises(EvidenceError, match="decisions were found wrong"):
        _load(tmp_path, er_id, target, "SUPPORTS", review)
    # The same review may refute.
    [obs] = _load(tmp_path, er_id, target, "REFUTES", review)
    assert obs.assessments[0].assessment == "REFUTES"


def test_the_reviewer_is_not_the_author() -> None:
    with pytest.raises(ValidationError, match="must not be the work's author"):
        TraceReview.model_validate(dict(REVIEW, reviewer="Session-A"))


def test_other_kinds_need_no_trace_review_record(tmp_path: Path) -> None:
    target = load_target(WHYGAME5_AES / "target.yaml")
    er_id = target.success_criteria[0].evidence_requirements[0].id
    assert target.evidence_requirements()[er_id][1].kind != "trace_review"
    [obs] = _load(tmp_path, er_id, target, "INCONCLUSIVE", None)
    assert obs.trace_review is None


def test_observation_schema_accepts_the_record_round_trip() -> None:
    obs = ObservationRecord.model_validate(parse_yaml_mapping(_observation("ER-X", "SUPPORTS", REVIEW), "obs"))
    assert obs.trace_review == TraceReview.model_validate(REVIEW)
