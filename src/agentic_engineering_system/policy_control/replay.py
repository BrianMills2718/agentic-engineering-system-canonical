from __future__ import annotations

import hashlib
import json
from typing import Protocol

from .models import (
    BaselineDecisionV1,
    EvaluatorInputV1,
    LaterOutcomeV1,
    ProviderJudgmentV1,
    ReplayReportV1,
)


class TypedEvaluator(Protocol):
    """Replaceable offline evaluator boundary for Plan 002."""

    def evaluate(self, state: EvaluatorInputV1) -> ProviderJudgmentV1: ...


def evaluator_input_sha256(state: EvaluatorInputV1) -> str:
    payload = json.dumps(
        state.model_dump(mode="json"),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def run_offline_replay(
    *,
    evaluator_input: EvaluatorInputV1,
    baseline: BaselineDecisionV1,
    evaluator: TypedEvaluator,
    later_outcome: LaterOutcomeV1 | None = None,
) -> ReplayReportV1:
    """Evaluate one frozen event-time state without exposing later outcome data."""

    candidate = evaluator.evaluate(evaluator_input)
    return ReplayReportV1(
        evaluator_input_sha256=evaluator_input_sha256(evaluator_input),
        evaluator_input=evaluator_input,
        baseline=baseline,
        candidate=candidate,
        later_outcome=later_outcome,
    )
