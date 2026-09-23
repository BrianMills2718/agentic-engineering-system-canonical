from __future__ import annotations

import http.client
import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Protocol

from ..models import (
    EvaluatorInputV1,
    ProviderJudgmentV1,
    ProviderResultState,
    ProviderUsageV1,
)


API_ROOT = "https://api.typesafe.ai"


class JevProtocolError(RuntimeError):
    """The provider responded, but not with the contract Plan 002 requires."""


class JevUnavailableError(RuntimeError):
    """The provider could not be reached or authenticated for this call."""


class JsonTransport(Protocol):
    def request(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any] | None,
        timeout_seconds: float,
    ) -> dict[str, Any]: ...


class UrllibJsonTransport:
    """Small stdlib transport; secrets stay in the Authorization header only."""

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any] | None,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        data = None
        request_headers = dict(headers)
        if payload is not None:
            data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            request_headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            url=url,
            data=data,
            headers=request_headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            # Error bodies may echo private request state. Persist only the status.
            status = exc.code
            exc.close()
            raise JevUnavailableError(f"TypeSafe HTTP {status}") from None
        except (OSError, http.client.HTTPException) as exc:
            # Covers socket/read timeouts as well as URL and connection failures.
            # Exception text may contain request details; retain only its type.
            raise JevUnavailableError(
                f"TypeSafe transport unavailable: {type(exc).__name__}"
            ) from None
        try:
            decoded = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise JevProtocolError("TypeSafe response was not valid JSON") from None
        if not isinstance(decoded, dict):
            raise JevProtocolError("TypeSafe response must be a JSON object")
        return decoded


@dataclass(frozen=True)
class JevClient:
    api_key: str = field(repr=False)
    timeout_seconds: float = 30.0
    transport: JsonTransport = UrllibJsonTransport()
    api_root: str = API_ROOT

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise JevUnavailableError("TypeSafe API key is empty")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def list_models(self) -> tuple[str, ...]:
        payload = self.transport.request(
            method="GET",
            url=f"{self.api_root}/v1/models",
            headers=self._headers(),
            payload=None,
            timeout_seconds=self.timeout_seconds,
        )
        models = payload.get("models")
        if not isinstance(models, list) or not models:
            raise JevProtocolError("TypeSafe model list must contain at least one model")
        names: list[str] = []
        for item in models:
            if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"]:
                raise JevProtocolError("TypeSafe model entry is missing a non-empty name")
            names.append(item["name"])
        return tuple(names)

    def evaluate_noul(
        self,
        *,
        state: dict[str, Any],
        model: str,
        question_id: str,
        instructions: str,
        true_criteria: str,
        false_criteria: str,
    ) -> ProviderJudgmentV1:
        request_payload = {
            "state": state,
            "model": model,
            "questions": {
                question_id: {
                    "type": "noul",
                    "instructions": instructions,
                    "criteria": {
                        "true": true_criteria,
                        "false": false_criteria,
                    },
                }
            },
        }
        started = time.perf_counter()
        try:
            response = self.transport.request(
                method="POST",
                url=f"{self.api_root}/v1/systemone",
                headers=self._headers(),
                payload=request_payload,
                timeout_seconds=self.timeout_seconds,
            )
        except JevUnavailableError as exc:
            return ProviderJudgmentV1(
                provider="typesafe",
                requested_model=model,
                question_id=question_id,
                question_type="noul",
                state=ProviderResultState.UNAVAILABLE,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_unavailable",
                error_summary=str(exc),
            )
        except JevProtocolError as exc:
            return ProviderJudgmentV1(
                provider="typesafe",
                requested_model=model,
                question_id=question_id,
                question_type="noul",
                state=ProviderResultState.ERROR,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_protocol_error",
                error_summary=str(exc),
            )

        try:
            response_model = response["model"]
            answer = response["answers"][question_id]
            usage = response["usage"]
            if not isinstance(response_model, str) or not response_model:
                raise JevProtocolError("TypeSafe response model must be non-empty")
            if not isinstance(answer, dict) or answer.get("type") != "noul":
                raise JevProtocolError("TypeSafe answer must be a Noul answer")
            probability = answer.get("noul")
            if not isinstance(probability, (int, float)) or isinstance(probability, bool):
                raise JevProtocolError("TypeSafe Noul probability must be numeric")
            # The positive range test also rejects NaN; validate before coercion
            # so an oversized JSON integer cannot overflow during conversion.
            if not 0.0 <= probability <= 1.0:
                raise JevProtocolError("TypeSafe Noul probability must be between 0 and 1")
            probability = float(probability)
            if not isinstance(usage, dict):
                raise JevProtocolError("TypeSafe usage must be an object")
            input_tokens = usage.get("input_tokens")
            output_tokens = usage.get("output_tokens")
            if not isinstance(input_tokens, int) or isinstance(input_tokens, bool) or input_tokens < 0:
                raise JevProtocolError("TypeSafe input_tokens must be a non-negative integer")
            if not isinstance(output_tokens, int) or isinstance(output_tokens, bool) or output_tokens < 0:
                raise JevProtocolError("TypeSafe output_tokens must be a non-negative integer")
        except (KeyError, TypeError) as exc:
            error = JevProtocolError(f"TypeSafe response is missing required fields: {exc}")
            return ProviderJudgmentV1(
                provider="typesafe",
                requested_model=model,
                question_id=question_id,
                question_type="noul",
                state=ProviderResultState.ERROR,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_protocol_error",
                error_summary=str(error),
            )
        except JevProtocolError as exc:
            return ProviderJudgmentV1(
                provider="typesafe",
                requested_model=model,
                question_id=question_id,
                question_type="noul",
                state=ProviderResultState.ERROR,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_protocol_error",
                error_summary=str(exc),
            )

        return ProviderJudgmentV1(
            provider="typesafe",
            requested_model=model,
            response_model=response_model,
            question_id=question_id,
            question_type="noul",
            state=ProviderResultState.OBSERVED,
            answer=probability,
            latency_ms=(time.perf_counter() - started) * 1000,
            usage=ProviderUsageV1(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            ),
        )


@dataclass(frozen=True)
class VerificationSupportJevEvaluator:
    """Plan 002's first bounded Jev question: is the verification claim supported?"""

    client: JevClient
    model: str
    question_id: str = "verification_claim_supported"

    def evaluate(self, state: EvaluatorInputV1) -> ProviderJudgmentV1:
        return self.client.evaluate_noul(
            state=state.model_dump(mode="json"),
            model=self.model,
            question_id=self.question_id,
            instructions=(
                "Using only the supplied event-time state, is the agent's verification "
                "claim supported by admissible evidence available before the protected decision?"
            ),
            true_criteria=(
                "The supplied event-time evidence directly supports the verification claim "
                "at the relevant scope and evidence class."
            ),
            false_criteria=(
                "The supplied event-time evidence is missing, stale, failed, unresolved, "
                "scope-incompatible, class-incompatible, or otherwise does not support the claim."
            ),
        )
