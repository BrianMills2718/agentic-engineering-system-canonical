from agentic_engineering_system.policy_control.models import (
    BaselineDecisionV1,
    DecisionKind,
    EvidenceState,
    EvaluatorInputV1,
    EventTimeEvidenceV1,
    LaterOutcomeV1,
    ProbabilityV1,
    ProviderJudgmentV1,
    ProviderResultState,
    SourceIdentityV1,
)
from agentic_engineering_system.policy_control.replay import (
    evaluator_input_sha256,
    run_offline_replay,
)


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


def evaluator_input() -> EvaluatorInputV1:
    return EvaluatorInputV1(
        case_id="p10-s4-unsupported-verification-block",
        source=SourceIdentityV1(
            repository="Inside-Success/agentic-engineering-system",
            revision="6d3b802463c653f7f43dfdf7abcf6b2da20b4d27",
            source_record="evidence/propagation/2026-09-09-plan-10-s4-native-retained.json",
            origin="authentic_runtime",
            client="Claude Code 2.1.266",
            session_id="7d32a420-39fb-41d2-a8f8-f7362efddffe",
            transcript_sha256=DIGEST_A,
            receipt_id="eaf13fcf8acd40f4aca07efc2fd908aa",
            receipt_sha256=DIGEST_B,
        ),
        claim_text="The watcher acceptance test passes.",
        event_time_evidence=(
            EventTimeEvidenceV1(
                evidence_id="turn-tool-state",
                state=EvidenceState.MISSING,
                evidence_class="test",
                subject_scope="tests:test_check_gate_reaches_judgement.py",
                summary="No test execution was observed before the protected claim.",
            ),
        ),
    )


class RecordingEvaluator:
    def __init__(self) -> None:
        self.seen: EvaluatorInputV1 | None = None

    def evaluate(self, state: EvaluatorInputV1) -> ProviderJudgmentV1:
        self.seen = state
        return ProviderJudgmentV1(
            provider="fake-typesafe",
            model="fake-jev-exact",
            question_id="claim_supported",
            state=ProviderResultState.OBSERVED,
            answer=False,
            probabilities=(
                ProbabilityV1(label="true", probability=0.02),
                ProbabilityV1(label="false", probability=0.98),
            ),
            latency_ms=1.0,
        )


def test_replay_evaluator_receives_only_event_time_input() -> None:
    state = evaluator_input()
    evaluator = RecordingEvaluator()
    later = LaterOutcomeV1(
        summary="The agent later ran the focused test and the identical claim was allowed.",
        evidence_refs=("later-receipt",),
    )

    report = run_offline_replay(
        evaluator_input=state,
        baseline=BaselineDecisionV1(
            decision=DecisionKind.BLOCK,
            reason_code="unbacked_assertion",
            summary="The claim lacked current-turn verification evidence.",
        ),
        evaluator=evaluator,
        later_outcome=later,
    )

    assert evaluator.seen == state
    assert not hasattr(evaluator.seen, "later_outcome")
    assert report.later_outcome == later


def test_later_outcome_cannot_change_evaluator_input_digest() -> None:
    state = evaluator_input()
    digest_before = evaluator_input_sha256(state)
    evaluator = RecordingEvaluator()

    first = run_offline_replay(
        evaluator_input=state,
        baseline=BaselineDecisionV1(
            decision=DecisionKind.BLOCK,
            reason_code="unbacked_assertion",
            summary="blocked",
        ),
        evaluator=evaluator,
        later_outcome=LaterOutcomeV1(summary="later accepted"),
    )
    second = run_offline_replay(
        evaluator_input=state,
        baseline=BaselineDecisionV1(
            decision=DecisionKind.BLOCK,
            reason_code="unbacked_assertion",
            summary="blocked",
        ),
        evaluator=evaluator,
        later_outcome=LaterOutcomeV1(summary="later rejected"),
    )

    assert first.evaluator_input_sha256 == digest_before
    assert second.evaluator_input_sha256 == digest_before
