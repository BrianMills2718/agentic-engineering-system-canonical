"""Offline contract review of AES PR #29; synthetic data, no network or credentials.

Run with the PR checkout's src on PYTHONPATH. These tests intentionally express
expected transport-boundary behavior, rather than changing production policy.
"""
from __future__ import annotations

import io
import math
import urllib.error
import urllib.request
from unittest.mock import patch

import pytest

from agentic_engineering_system.policy_control.models import ProviderResultState
from agentic_engineering_system.policy_control.providers.jev import JevClient


class FakeResponse:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


def evaluate(client: JevClient):
    return client.evaluate_noul(
        state={"claim": "synthetic review input"},
        model="jev-review-alias",
        question_id="support",
        instructions="Is the supplied claim supported by this evidence?",
        true_criteria="Supported by the evidence.",
        false_criteria="Not supported by the evidence.",
    )


@pytest.fixture(autouse=True)
def never_contact_network(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("Network forbidden in this offline review")
    monkeypatch.setattr(urllib.request, "urlopen", blocked)


def test_valid_probability_preserves_model_identity():
    raw = b'{"model":"jev-review-resolved","answers":{"support":{"type":"noul","noul":0.7}},"usage":{"input_tokens":10,"output_tokens":1}}'
    with patch("urllib.request.urlopen", return_value=FakeResponse(raw)):
        result = evaluate(JevClient(api_key="synthetic-key"))
    assert result.state == ProviderResultState.OBSERVED
    assert result.requested_model == "jev-review-alias"
    assert result.response_model == "jev-review-resolved"
    assert math.isfinite(result.answer)
    assert result.answer == 0.7


def test_out_of_range_probability_is_protocol_error():
    raw = b'{"model":"jev-review-resolved","answers":{"support":{"type":"noul","noul":2.0}},"usage":{"input_tokens":10,"output_tokens":1}}'
    with patch("urllib.request.urlopen", return_value=FakeResponse(raw)):
        result = evaluate(JevClient(api_key="synthetic-key"))
    assert result.state == ProviderResultState.ERROR
    assert result.answer is None


def test_socket_timeout_becomes_explicit_unavailable():
    with patch("urllib.request.urlopen", side_effect=TimeoutError("synthetic socket timeout")):
        result = evaluate(JevClient(api_key="synthetic-key"))
    assert result.state == ProviderResultState.UNAVAILABLE
    assert result.answer is None


def test_nan_cannot_be_an_observed_judgment():
    raw = b'{"model":"jev-review-resolved","answers":{"support":{"type":"noul","noul":NaN}},"usage":{"input_tokens":10,"output_tokens":1}}'
    with patch("urllib.request.urlopen", return_value=FakeResponse(raw)):
        result = evaluate(JevClient(api_key="synthetic-key"))
    assert result.state == ProviderResultState.ERROR
    assert result.answer is None


def test_http_error_echo_is_not_persisted_as_feedback():
    marker = "SYNTHETIC_PRIVATE_STATE_DO_NOT_RETAIN"
    error = urllib.error.HTTPError(
        "https://api.typesafe.ai/v1/systemone", 422, "synthetic failure", {},
        io.BytesIO(("request echoed: " + marker).encode()),
    )
    with patch("urllib.request.urlopen", side_effect=error):
        result = evaluate(JevClient(api_key="synthetic-key"))
    assert result.state != ProviderResultState.OBSERVED
    assert marker not in result.model_dump_json()


def test_client_representation_does_not_disclose_credential():
    marker = "SYNTHETIC_CREDENTIAL_DO_NOT_RETAIN"
    assert marker not in repr(JevClient(api_key=marker))
