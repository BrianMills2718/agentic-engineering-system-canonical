from pathlib import Path

from agentic_engineering_system.policy_control.models import (
    BaselineDecisionV1,
    DecisionKind,
    EvaluatorInputV1,
    LaterOutcomeV1,
    ProviderJudgmentV1,
    ProviderResultState,
    ProviderUsageV1,
    ReplayReportV1,
    SourceIdentityV1,
)
from agentic_engineering_system.policy_control.render import (
    render_report_html,
    write_report_bundle,
)


def sample_report() -> ReplayReportV1:
    return ReplayReportV1(
        evaluator_input_sha256="d" * 64,
        evaluator_input=EvaluatorInputV1(
            case_id="case-1",
            source=SourceIdentityV1(
                repository="Inside-Success/agentic-engineering-system",
                revision="abc123",
                source_record="evidence/example.json",
                origin="authentic_runtime",
                client="Claude Code",
                session_id="session-1",
                transcript_sha256="a" * 64,
            ),
            claim_text="The <watcher> test passes.",
        ),
        baseline=BaselineDecisionV1(
            decision=DecisionKind.BLOCK,
            reason_code="unbacked_assertion",
            summary="No current-turn evidence.",
        ),
        candidate=ProviderJudgmentV1(
            provider="openrouter",
            requested_model="openai/gpt-6-luna",
            response_model="openai/gpt-6-luna-20260922",
            question_id="verification_claim_supported",
            question_type="choice",
            state=ProviderResultState.OBSERVED,
            answer="unsupported",
            rationale="No event-time verification evidence supports the claim.",
            usage=ProviderUsageV1(
                input_tokens=10,
                output_tokens=4,
                cost_usd=0.000003,
            ),
        ),
        later_outcome=LaterOutcomeV1(
            summary="The test was run later and passed.",
            evidence_refs=("later",),
        ),
    )


def test_html_report_escapes_claim_and_separates_later_outcome() -> None:
    rendered = render_report_html(sample_report())

    assert "The &lt;watcher&gt; test passes." in rendered
    assert "This section was not supplied to the evaluator." in rendered
    assert "openai/gpt-6-luna" in rendered
    assert "unbacked_assertion" in rendered
    assert "No event-time verification evidence supports the claim." in rendered
    assert (
        "github.com/Inside-Success/agentic-engineering-system/blob/"
        "abc123/evidence/example.json"
    ) in rendered


def test_report_bundle_writes_json_and_html(tmp_path: Path) -> None:
    json_path, html_path = write_report_bundle(tmp_path, sample_report())

    assert json_path.name == "replay.json"
    assert html_path.name == "index.html"
    assert '"answer": "unsupported"' in json_path.read_text(encoding="utf-8")
    assert "<!doctype html>" in html_path.read_text(encoding="utf-8")
