from __future__ import annotations

from typing import Any

from agentic_engineering_system.policy_control.models import (
    EvidenceState,
    EvaluatorInputV1,
    EventTimeEvidenceV1,
    ProviderResultState,
    SourceIdentityV1,
)
from agentic_engineering_system.policy_control.providers.jev import (
    JevClient,
    JevProtocolError,
    JevUnavailableError,
    VerificationSupportJevEvaluator,
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


def test_list_models_uses_bearer_auth_and_returns_names() -> None:
    transport = FakeTransport(
        [
            {
                "models": [
                    {
                        "name": "jev-latest",
                        "description": "latest",
                        "release_date": "2026-09-15",
                    },
                    {
                        "name": "jev-1.13.0",
                        "description": "exact",
                        "release_date": "2026-09-15",
                    },
                ]
            }
        ]
    )
    client = JevClient(api_key="secret", transport=transport)

    assert client.list_models() == ("jev-latest", "jev-1.13.0")
    call = transport.calls[0]
    assert call["method"] == "GET"
    assert call["url"].endswith("/v1/models")
    assert call["headers"]["Authorization"] == "Bearer secret"
    assert call["payload"] is None


def test_verification_evaluator_sends_only_event_time_state_and_noul_question() -> None:
    transport = FakeTransport(
        [
            {
                "model": "jev-1.13.0",
                "answers": {
                    "verification_claim_supported": {
                        "type": "noul",
                        "noul": 0.08,
                    }
                },
                "usage": {
                    "input_tokens": 120,
                    "output_tokens": 12,
                },
            }
        ]
    )
    evaluator = VerificationSupportJevEvaluator(
        client=JevClient(api_key="secret", transport=transport),
        model="jev-latest",
    )
    state = event_state()

    result = evaluator.evaluate(state)

    call = transport.calls[0]
    assert call["method"] == "POST"
    assert call["url"].endswith("/v1/systemone")
    assert call["payload"]["state"] == state.model_dump(mode="json")
    assert "later_outcome" not in call["payload"]["state"]
    assert call["payload"]["model"] == "jev-latest"
    question = call["payload"]["questions"]["verification_claim_supported"]
    assert question["type"] == "noul"

    assert result.state == ProviderResultState.OBSERVED
    assert result.requested_model == "jev-latest"
    assert result.response_model == "jev-1.13.0"
    assert result.answer == 0.08
    assert result.usage is not None
    assert result.usage.input_tokens == 120
    assert result.usage.output_tokens == 12


def test_provider_unavailable_stays_explicit() -> None:
    transport = FakeTransport([JevUnavailableError("network unavailable")])
    evaluator = VerificationSupportJevEvaluator(
        client=JevClient(api_key="secret", transport=transport),
        model="jev-latest",
    )

    result = evaluator.evaluate(event_state())

    assert result.state == ProviderResultState.UNAVAILABLE
    assert result.answer is None
    assert result.error_code == "provider_unavailable"
    assert "network unavailable" in result.error_summary


def test_provider_protocol_error_stays_explicit() -> None:
    transport = FakeTransport([JevProtocolError("bad response")])
    evaluator = VerificationSupportJevEvaluator(
        client=JevClient(api_key="secret", transport=transport),
        model="jev-latest",
    )

    result = evaluator.evaluate(event_state())

    assert result.state == ProviderResultState.ERROR
    assert result.answer is None
    assert result.error_code == "provider_protocol_error"
    assert "bad response" in result.error_summary


def test_malformed_noul_response_is_error_not_observed() -> None:
    transport = FakeTransport(
        [
            {
                "model": "jev-1.13.0",
                "answers": {
                    "verification_claim_supported": {
                        "type": "noul",
                        "noul": 2.0,
                    }
                },
                "usage": {
                    "input_tokens": 1,
                    "output_tokens": 1,
                },
            }
        ]
    )
    evaluator = VerificationSupportJevEvaluator(
        client=JevClient(api_key="secret", transport=transport),
        model="jev-latest",
    )

    result = evaluator.evaluate(event_state())

    assert result.state == ProviderResultState.ERROR
    assert result.answer is None
    assert result.error_code == "provider_protocol_error"
