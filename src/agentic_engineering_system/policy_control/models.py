from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SHA256_PATTERN = r"^[0-9a-f]{64}$"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EvidenceState(StrEnum):
    OBSERVED = "OBSERVED"
    MISSING = "MISSING"
    STALE = "STALE"
    ERROR = "ERROR"
    UNRESOLVED = "UNRESOLVED"


class DecisionKind(StrEnum):
    ALLOW = "allow"
    BLOCK = "block"
    WARN = "warn"
    ERROR = "error"
    NOT_CHECKED = "not_checked"


class ProviderResultState(StrEnum):
    OBSERVED = "OBSERVED"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


class SourceIdentityV1(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    repository: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    source_record: str = Field(min_length=1)
    origin: Literal["authentic_runtime"]
    client: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    transcript_sha256: str = Field(pattern=SHA256_PATTERN)
    receipt_id: str | None = Field(default=None, min_length=1)
    receipt_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def receipt_identity_is_complete_or_absent(self) -> "SourceIdentityV1":
        if (self.receipt_id is None) != (self.receipt_sha256 is None):
            raise ValueError("receipt_id and receipt_sha256 must be supplied together")
        return self


class EventTimeEvidenceV1(StrictModel):
    evidence_id: str = Field(min_length=1)
    state: EvidenceState
    evidence_class: str = Field(min_length=1)
    subject_scope: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    payload_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def observed_evidence_requires_digest(self) -> "EventTimeEvidenceV1":
        if self.state == EvidenceState.OBSERVED and self.payload_sha256 is None:
            raise ValueError("OBSERVED event-time evidence requires payload_sha256")
        return self


class EventTimeContextFactV1(StrictModel):
    """One context fact proven to exist before the protected decision."""

    fact_id: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    payload_sha256: str = Field(pattern=SHA256_PATTERN)
    summary: str = Field(min_length=1)
    observed_before_decision: Literal[True] = True


class EvaluatorInputV1(StrictModel):
    """Complete state supplied to a candidate evaluator.

    This contract deliberately has no later-outcome, adjudication, or
    post-decision fields. Context facts must carry source identity plus a
    content digest and explicitly assert event-time availability.
    """

    schema_version: Literal["1.0"] = "1.0"
    case_id: str = Field(min_length=1)
    source: SourceIdentityV1
    claim_text: str = Field(min_length=1)
    event_time_evidence: tuple[EventTimeEvidenceV1, ...] = ()
    event_time_context: tuple[EventTimeContextFactV1, ...] = ()


class BaselineDecisionV1(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    decision: DecisionKind
    reason_code: str = Field(min_length=1)
    summary: str = Field(min_length=1)


class ProbabilityV1(StrictModel):
    label: str = Field(min_length=1)
    probability: float = Field(ge=0.0, le=1.0)


class ProviderUsageV1(StrictModel):
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)


class ProviderJudgmentV1(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    provider: str = Field(min_length=1)
    requested_model: str | None = Field(default=None, min_length=1)
    response_model: str | None = Field(default=None, min_length=1)
    question_id: str = Field(min_length=1)
    question_type: Literal["noul", "choice", "score"]
    state: ProviderResultState
    answer: str | int | float | None = None
    probabilities: tuple[ProbabilityV1, ...] = ()
    latency_ms: float | None = Field(default=None, ge=0.0)
    usage: ProviderUsageV1 | None = None
    error_code: str | None = Field(default=None, min_length=1)
    error_summary: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def result_state_is_explicit(self) -> "ProviderJudgmentV1":
        if self.state == ProviderResultState.OBSERVED:
            if self.response_model is None:
                raise ValueError("OBSERVED provider judgment requires response model identity")
            if self.answer is None and not self.probabilities:
                raise ValueError("OBSERVED provider judgment requires an answer or probabilities")
            if self.error_code is not None or self.error_summary is not None:
                raise ValueError("OBSERVED provider judgment cannot carry provider error fields")
        else:
            if self.answer is not None or self.probabilities:
                raise ValueError("UNAVAILABLE/ERROR provider judgment cannot carry an observed answer")
            if self.error_code is None or self.error_summary is None:
                raise ValueError("UNAVAILABLE/ERROR provider judgment requires explicit error fields")
        return self


class LaterOutcomeV1(StrictModel):
    """Outcome/adjudication retained for review but never supplied to evaluator."""

    summary: str = Field(min_length=1)
    evidence_refs: tuple[str, ...] = ()


class ReplayReportV1(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    evaluator_input_sha256: str = Field(pattern=SHA256_PATTERN)
    evaluator_input: EvaluatorInputV1
    baseline: BaselineDecisionV1
    candidate: ProviderJudgmentV1
    later_outcome: LaterOutcomeV1 | None = None


class ReplayCaseV1(StrictModel):
    """One frozen offline replay case.

    Later outcome is retained beside the evaluator input for review, but replay
    code passes only evaluator_input to the candidate evaluator.
    """

    schema_version: Literal["1.0"] = "1.0"
    evaluator_input: EvaluatorInputV1
    baseline: BaselineDecisionV1
    later_outcome: LaterOutcomeV1 | None = None
