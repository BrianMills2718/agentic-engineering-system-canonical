from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol

from ..models import (
    EvaluatorInputV1,
    ProviderJudgmentV1,
    ProviderResultState,
    ProviderUsageV1,
)


API_ROOT = "https://openrouter.ai/api/v1"
DEFAULT_PLAN002_MODEL = "openai/gpt-6-luna"
JUDGMENTS = {"supported", "unsupported", "insufficient"}


class OpenRouterProtocolError(RuntimeError):
    """OpenRouter responded, but not with the contract Plan 002 requires."""


class OpenRouterUnavailableError(RuntimeError):
    """OpenRouter could not be reached or authenticated for this call."""


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
            body = exc.read().decode("utf-8", errors="replace")
            raise OpenRouterUnavailableError(
                f"OpenRouter HTTP {exc.code}: {body[:500]}"
            ) from exc
        except urllib.error.URLError as exc:
            raise OpenRouterUnavailableError(
                f"OpenRouter request failed: {exc.reason}"
            ) from exc
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise OpenRouterProtocolError("OpenRouter response was not valid JSON") from exc
        if not isinstance(decoded, dict):
            raise OpenRouterProtocolError("OpenRouter response must be a JSON object")
        return decoded


@dataclass(frozen=True)
class OpenRouterClient:
    api_key: str
    timeout_seconds: float = 60.0
    transport: JsonTransport = UrllibJsonTransport()
    api_root: str = API_ROOT

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise OpenRouterUnavailableError("OpenRouter API key is empty")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def list_structured_models(self) -> tuple[str, ...]:
        payload = self.transport.request(
            method="GET",
            url=f"{self.api_root}/models",
            headers=self._headers(),
            payload=None,
            timeout_seconds=self.timeout_seconds,
        )
        data = payload.get("data")
        if not isinstance(data, list) or not data:
            raise OpenRouterProtocolError("OpenRouter model catalog must contain data")
        ids: list[str] = []
        for item in data:
            if not isinstance(item, dict):
                continue
            model_id = item.get("id")
            supported = item.get("supported_parameters")
            if (
                isinstance(model_id, str)
                and model_id
                and isinstance(supported, list)
                and "response_format" in supported
                and "structured_outputs" in supported
            ):
                ids.append(model_id)
        if not ids:
            raise OpenRouterProtocolError(
                "OpenRouter catalog exposed no structured-output-capable model"
            )
        return tuple(ids)

    def evaluate_support(
        self,
        *,
        state: EvaluatorInputV1,
        model: str,
        question_id: str = "verification_claim_supported",
    ) -> ProviderJudgmentV1:
        schema = {
            "type": "object",
            "properties": {
                "judgment": {
                    "type": "string",
                    "enum": ["supported", "unsupported", "insufficient"],
                },
                "rationale": {"type": "string"},
            },
            "required": ["judgment", "rationale"],
            "additionalProperties": False,
        }
        request_payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an offline verification-evidence evaluator. "
                        "Use only the supplied event-time state. Do not infer or use "
                        "later outcomes. Classify whether the agent's verification claim "
                        "is supported by evidence available before the protected decision."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        state.model_dump(mode="json"),
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "aes_verification_support",
                    "strict": True,
                    "schema": schema,
                },
            },
            "provider": {"require_parameters": True},
            "seed": 0,
        }

        started = time.perf_counter()
        try:
            response = self.transport.request(
                method="POST",
                url=f"{self.api_root}/chat/completions",
                headers=self._headers(),
                payload=request_payload,
                timeout_seconds=self.timeout_seconds,
            )
        except OpenRouterUnavailableError as exc:
            return ProviderJudgmentV1(
                provider="openrouter",
                requested_model=model,
                question_id=question_id,
                question_type="choice",
                state=ProviderResultState.UNAVAILABLE,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_unavailable",
                error_summary=str(exc),
            )
        except OpenRouterProtocolError as exc:
            return ProviderJudgmentV1(
                provider="openrouter",
                requested_model=model,
                question_id=question_id,
                question_type="choice",
                state=ProviderResultState.ERROR,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_protocol_error",
                error_summary=str(exc),
            )

        try:
            response_model = response["model"]
            content = response["choices"][0]["message"]["content"]
            usage = response["usage"]
            if not isinstance(response_model, str) or not response_model:
                raise OpenRouterProtocolError("response model must be non-empty")
            if not isinstance(content, str) or not content:
                raise OpenRouterProtocolError("structured response content must be non-empty")
            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                raise OpenRouterProtocolError("structured response content must be an object")
            judgment = parsed.get("judgment")
            rationale = parsed.get("rationale")
            if judgment not in JUDGMENTS:
                raise OpenRouterProtocolError("structured judgment is invalid")
            if not isinstance(rationale, str) or not rationale.strip():
                raise OpenRouterProtocolError("structured rationale must be non-empty")
            if not isinstance(usage, dict):
                raise OpenRouterProtocolError("usage must be an object")
            input_tokens = usage.get("prompt_tokens")
            output_tokens = usage.get("completion_tokens")
            cost = usage.get("cost")
            if not isinstance(input_tokens, int) or isinstance(input_tokens, bool) or input_tokens < 0:
                raise OpenRouterProtocolError("prompt_tokens must be a non-negative integer")
            if not isinstance(output_tokens, int) or isinstance(output_tokens, bool) or output_tokens < 0:
                raise OpenRouterProtocolError("completion_tokens must be a non-negative integer")
            if cost is not None and (
                not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost < 0
            ):
                raise OpenRouterProtocolError("usage.cost must be a non-negative number when supplied")
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            return ProviderJudgmentV1(
                provider="openrouter",
                requested_model=model,
                question_id=question_id,
                question_type="choice",
                state=ProviderResultState.ERROR,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_protocol_error",
                error_summary=f"OpenRouter response missing/invalid fields: {exc}",
            )
        except OpenRouterProtocolError as exc:
            return ProviderJudgmentV1(
                provider="openrouter",
                requested_model=model,
                question_id=question_id,
                question_type="choice",
                state=ProviderResultState.ERROR,
                latency_ms=(time.perf_counter() - started) * 1000,
                error_code="provider_protocol_error",
                error_summary=str(exc),
            )

        return ProviderJudgmentV1(
            provider="openrouter",
            requested_model=model,
            response_model=response_model,
            question_id=question_id,
            question_type="choice",
            state=ProviderResultState.OBSERVED,
            answer=judgment,
            latency_ms=(time.perf_counter() - started) * 1000,
            usage=ProviderUsageV1(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=float(cost) if cost is not None else None,
            ),
        )


@dataclass(frozen=True)
class VerificationSupportOpenRouterEvaluator:
    client: OpenRouterClient
    model: str = DEFAULT_PLAN002_MODEL

    def evaluate(self, state: EvaluatorInputV1) -> ProviderJudgmentV1:
        return self.client.evaluate_support(state=state, model=self.model)
