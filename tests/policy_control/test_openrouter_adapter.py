from __future__ import annotations

from typing import Any

from agentic_engineering_system.policy_control.models import (
    EvidenceState,
    EvaluatorInputV1,
    EventTimeEvidenceV1,
    ProviderResultState,
    SourceIdentityV1,
)
from agentic_engineering_system.policy_control.providers.openrouter import (
    DEFAULT_PLAN002_MODEL,
    OpenRouterClient,
    OpenRouterProtocolError,
    OpenRouterUnavailableError,
    VerificationSupportOpenRouterEvaluator,
)


DIGEST = "a" * 64


class FakeTransport:
    def __init__(self, responses: list[dict[str, Any] | Exception]) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, Any]] = []

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any] | None,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "payload": payload,
                "timeout_seconds": timeout_seconds,
            }
        )
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def event_state() -> EvaluatorInputV1:
    return EvaluatorInputV1(
        case_id="case-1",
        source=SourceIdentityV1(
            repository="Inside-Success/agentic-engineering-system",
            revision="r1",
            source_record="evidence/example.json",
            origin="authentic_runtime",
            client="Claude Code",
            session_id="session-1",
            transcript_sha256=DIGEST,
        ),
        claim_text="The tests pass.",
        event_time_evidence=(
            EventTimeEvidenceV1(
                evidence_id="test-result",
                state=EvidenceState.MISSING,
                evidence_class="test",
                subject_scope="tests",
                summary="No test execution was observed.",
            ),
        ),
    )


def test_list_structured_models_filters_catalog_capabilities() -> None:
    transport = FakeTransport(
        [
            {
                "data": [
                    {
                        "id": "openai/gpt-6-luna",
                        "supported_parameters": [
                            "response_format",
                            "structured_outputs",
                            "seed",
                        ],
                    },
                    {
                        "id": "example/plain-model",
                        "supported_parameters": ["temperature"],
                    },
                ]
            }
        ]
    )
    client = OpenRouterClient(api_key="secret", transport=transport)

    assert client.list_structured_models() == ("openai/gpt-6-luna",)
    call = transport.calls[0]
    assert call["method"] == "GET"
    assert call["url"].endswith("/api/v1/models")
    assert call["headers"]["Authorization"] == "Bearer secret"
    assert call["payload"] is None


def test_evaluator_sends_only_event_time_state_with_strict_schema() -> None:
    transport = FakeTransport(
        [
            {
                "model": "openai/gpt-6-luna-20260922",
                "choices": [
                    {
                        "message": {
                            "content": (
                                '{"judgment":"unsupported",'
                                '"rationale":"No pre-decision test evidence was supplied."}'
                            )
                        }
                    }
                ],
                "usage": {
                    "prompt_tokens": 120,
                    "completion_tokens": 14,
                    "cost": 0.000019,
                },
            }
        ]
    )
    evaluator = VerificationSupportOpenRouterEvaluator(
        client=OpenRouterClient(api_key="secret", transport=transport)
    )
    state = event_state()

    result = evaluator.evaluate(state)

    call = transport.calls[0]
    assert call["method"] == "POST"
    assert call["url"].endswith("/api/v1/chat/completions")
    assert call["payload"]["model"] == DEFAULT_PLAN002_MODEL
    assert call["payload"]["provider"]["require_parameters"] is True
    assert call["payload"]["response_format"]["type"] == "json_schema"
    assert "later_outcome" not in call["payload"]["messages"][1]["content"]

    assert result.state == ProviderResultState.OBSERVED
    assert result.requested_model == DEFAULT_PLAN002_MODEL
    assert result.response_model == "openai/gpt-6-luna-20260922"
    assert result.answer == "unsupported"
    assert result.rationale == "No pre-decision test evidence was supplied."
    assert result.usage is not None
    assert result.usage.input_tokens == 120
    assert result.usage.output_tokens == 14
    assert result.usage.cost_usd == 0.000019


def test_provider_unavailable_stays_explicit() -> None:
    transport = FakeTransport([OpenRouterUnavailableError("network unavailable")])
    evaluator = VerificationSupportOpenRouterEvaluator(
        client=OpenRouterClient(api_key="secret", transport=transport)
    )

    result = evaluator.evaluate(event_state())

    assert result.state == ProviderResultState.UNAVAILABLE
    assert result.answer is None
    assert result.error_code == "provider_unavailable"


def test_provider_protocol_error_stays_explicit() -> None:
    transport = FakeTransport([OpenRouterProtocolError("bad response")])
    evaluator = VerificationSupportOpenRouterEvaluator(
        client=OpenRouterClient(api_key="secret", transport=transport)
    )

    result = evaluator.evaluate(event_state())

    assert result.state == ProviderResultState.ERROR
    assert result.answer is None
    assert result.error_code == "provider_protocol_error"


def test_malformed_structured_judgment_is_error_not_observed() -> None:
    transport = FakeTransport(
        [
            {
                "model": "openai/gpt-6-luna-20260922",
                "choices": [
                    {
                        "message": {
                            "content": '{"judgment":"maybe","rationale":"unclear"}'
                        }
                    }
                ],
                "usage": {
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "cost": 0.0,
                },
            }
        ]
    )
    evaluator = VerificationSupportOpenRouterEvaluator(
        client=OpenRouterClient(api_key="secret", transport=transport)
    )

    result = evaluator.evaluate(event_state())

    assert result.state == ProviderResultState.ERROR
    assert result.answer is None
    assert result.error_code == "provider_protocol_error"
