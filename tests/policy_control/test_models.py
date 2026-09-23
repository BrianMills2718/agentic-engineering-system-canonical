import pytest
from pydantic import ValidationError

from agentic_engineering_system.policy_control.models import (
    DecisionKind,
    EvidenceState,
    EvaluatorInputV1,
    EventTimeContextFactV1,
    EventTimeEvidenceV1,
    ProviderJudgmentV1,
    ProviderResultState,
    SourceIdentityV1,
)


DIGEST = "a" * 64


def source_identity() -> SourceIdentityV1:
    return SourceIdentityV1(
        repository="Inside-Success/agentic-engineering-system",
        revision="8e91acf5b2c6acf02f3f9a3c2a9be13c4a6e8a7c",
        source_record="evidence/propagation/example.json",
        origin="authentic_runtime",
        client="Claude Code 2.1.278",
        session_id="session-1",
        transcript_sha256=DIGEST,
    )


def test_evaluator_input_rejects_post_decision_label_leakage() -> None:
    payload = {
        "case_id": "case-1",
        "source": source_identity().model_dump(mode="json"),
        "claim_text": "The tests pass.",
        "event_time_evidence": [],
        "later_outcome": {"summary": "The later verifier accepted the change."},
    }

    with pytest.raises(ValidationError):
        EvaluatorInputV1.model_validate(payload)


def test_observed_event_time_evidence_requires_content_identity() -> None:
    with pytest.raises(ValidationError):
        EventTimeEvidenceV1(
            evidence_id="tool-result-1",
            state=EvidenceState.OBSERVED,
            evidence_class="test",
            subject_scope="tests:test_sample.py",
            summary="pytest passed",
        )


def test_missing_event_time_evidence_stays_explicit_without_digest() -> None:
    evidence = EventTimeEvidenceV1(
        evidence_id="tool-result-1",
        state=EvidenceState.MISSING,
        evidence_class="test",
        subject_scope="tests:test_sample.py",
        summary="No event-time test result was observed.",
    )

    assert evidence.state == EvidenceState.MISSING
    assert evidence.payload_sha256 is None


def test_provider_unavailable_cannot_carry_an_observed_answer() -> None:
    with pytest.raises(ValidationError):
        ProviderJudgmentV1(
            provider="typesafe",
            requested_model="jev-latest",
            question_id="supported",
            question_type="noul",
            state=ProviderResultState.UNAVAILABLE,
            answer=0.9,
            error_code="provider_unavailable",
            error_summary="provider unavailable",
        )


def test_provider_unavailable_requires_explicit_failure_information() -> None:
    with pytest.raises(ValidationError):
        ProviderJudgmentV1(
            provider="typesafe",
            requested_model="jev-latest",
            question_id="supported",
            question_type="noul",
            state=ProviderResultState.UNAVAILABLE,
        )


def test_decision_kind_does_not_collapse_not_checked_into_allow() -> None:
    assert DecisionKind.NOT_CHECKED != DecisionKind.ALLOW

def test_event_time_context_fact_requires_predecision_source_identity() -> None:
    with pytest.raises(ValidationError):
        EventTimeContextFactV1.model_validate(
            {
                "fact_id": "later-verdict",
                "source_ref": "later-review.json",
                "payload_sha256": DIGEST,
                "summary": "A later reviewer accepted the result.",
                "observed_before_decision": False,
            }
        )


def test_observed_provider_uses_response_model_and_probability_answer() -> None:
    result = ProviderJudgmentV1(
        provider="typesafe",
        requested_model="jev-latest",
        response_model="jev-1.13.0",
        question_id="supported",
        question_type="noul",
        state=ProviderResultState.OBSERVED,
        answer=0.93,
    )

    assert result.answer == 0.93
    assert result.response_model == "jev-1.13.0"
