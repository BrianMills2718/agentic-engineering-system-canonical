"""Typed contracts for root-cause concern repair (ADR-2026-09-14 slice 3).

A concern issue in the GitHub concern register is repaired by a full-harness
coding agent (Claude Code or Codex). Closure is verifier-owned: the agent's
report is a claim, and every field that can be checked mechanically is checked
by ``concern_repair_feedback.py verify`` rather than trusted.

Three records cross process boundaries:

- ``RootCauseRepairReport`` -- written and committed by the repairing agent.
- ``RepairBinding`` -- written by the executor adapter (never the agent) into
  the runtime state root, keyed by repair branch. It pins the issue, concern
  key, observed revision, and which client actually ran.
- ``RootCauseReview`` -- structured verdict from an independent reviewer that
  sees only the issue, the diff, and the report.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

REPORT_SCHEMA = "concern-root-cause-repair/v2"
BINDING_SCHEMA = "concern-repair-binding/v1"
VERIFICATION_SCHEMA = "concern-repair-verification/v1"
REPORT_DIR = "feedback/concern-repair/reports"
REPO = "BrianMills2718/agentic-engineering-system-canonical"
CONCERN_LABEL = "concern:feedback"
REPAIR_LABEL = "agent:repair"
BRANCH_PREFIX = "feedback-repair/"

ClientName = Literal["claude-code", "codex"]
CLIENTS: tuple[ClientName, ...] = ("claude-code", "codex")


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _relative_path(value: str) -> str:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not value.strip():
        raise ValueError(f"path must be repository-relative without '..': {value!r}")
    return value.rstrip("/")


class ClassSweep(StrictModel):
    """Other instances of the same failure class, not just the reported one."""

    search_method: str = Field(min_length=10, description="How other instances were searched for (commands, scope).")
    instances_found: list[str] = Field(description="Every instance of the failure class found, including the reported one.")
    instances_fixed: list[str] = Field(description="Instances repaired in this change.")
    instances_deferred: list[str] = Field(default_factory=list, description="Instances not fixed, each with the reason.")


class PreventionMechanism(StrictModel):
    """The executable control that makes recurrence fail loudly."""

    kind: Literal["test", "check_script", "hook", "ci_gate", "validator", "policy_gate"]
    paths: list[str] = Field(min_length=1, description="Repository-relative files that implement the control.")
    description: str = Field(min_length=20)

    @field_validator("paths")
    @classmethod
    def paths_are_relative(cls, value: list[str]) -> list[str]:
        return [_relative_path(item) for item in value]


class RecurrenceProof(StrictModel):
    """A command the verifier executes on both revisions; never trusted as text."""

    command: list[str] = Field(min_length=1, description="argv run from the repository root with no shell.")
    harness_paths: list[str] = Field(
        description=(
            "Files the command needs that exist only in the fix (for example a new regression test), "
            "copied onto the observed revision before running there. Never list the files that "
            "implement the fix itself: copying them would make the observed revision identical to the "
            "fix, so the proof could not fail. May be empty."
        ),
    )
    fails_on_observed_revision: Literal[True]
    passes_on_fix: Literal[True]
    explanation: str = Field(min_length=20)

    @field_validator("harness_paths")
    @classmethod
    def harness_paths_are_relative(cls, value: list[str]) -> list[str]:
        return [_relative_path(item) for item in value]


class RootCauseRepairReport(StrictModel):
    schema_version: Literal["concern-root-cause-repair/v2"]
    concern_key: str = Field(min_length=1)
    issue_number: int = Field(ge=1)
    symptom: str = Field(min_length=20)
    root_cause: str = Field(min_length=40)
    why_existing_controls_missed_it: str = Field(min_length=20)
    failure_class: str = Field(min_length=10)
    class_sweep: ClassSweep
    prevention_mechanism: PreventionMechanism
    recurrence_proof: RecurrenceProof
    source_signal_resolution: str = Field(
        min_length=20, description="How the concern's own source signal was made green (e.g. cluster resolved with closure_verification)."
    )
    residual_risk: str = Field(min_length=1)


class RepairBinding(StrictModel):
    schema_version: Literal["concern-repair-binding/v1"] = "concern-repair-binding/v1"
    run_id: str = Field(min_length=1)
    branch: str = Field(min_length=1)
    issue_number: int = Field(ge=1)
    concern_key: str = Field(min_length=1)
    observed_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    repair_client: ClientName
    unavailable_clients: list[str] = Field(default_factory=list)
    report_path: str
    trace_id: str
    recorded_at: datetime


class RootCauseReview(StrictModel):
    """Independent semantic judgment; the verifier requires root_cause_fixed."""

    verdict: Literal["root_cause_fixed", "patch_only", "insufficient_evidence"] = Field(
        description=(
            "root_cause_fixed only if the diff removes the underlying cause AND adds a control that "
            "would fail if the failure class recurred. patch_only if it silences, special-cases, or "
            "repairs only the reported instance. insufficient_evidence if the diff and report do not "
            "let you tell."
        )
    )
    root_cause_addressed: bool
    failure_class_addressed: bool
    prevention_would_catch_recurrence: bool
    reasons: list[str] = Field(min_length=1, description="Concrete, diff-grounded reasons for the verdict.")


class GateResult(StrictModel):
    gate: Literal[
        "report_contract",
        "prevention_in_diff",
        "recurrence_proof_executed",
        "source_signal_green",
        "independent_root_cause_review",
    ]
    passed: bool
    detail: str


class VerificationRecord(StrictModel):
    schema_version: Literal["concern-repair-verification/v1"] = "concern-repair-verification/v1"
    concern_key: str
    issue_number: int
    repair_tree: str = Field(pattern=r"^[0-9a-f]{40}$")
    repair_client: ClientName
    reviewer_client: ClientName
    gates: list[GateResult]
    passed: bool
    recorded_at: datetime


def concern_slug(concern_key: str) -> str:
    """Stable, filesystem-safe name for a concern key."""
    readable = re.sub(r"[^a-zA-Z0-9._-]+", "-", concern_key).strip("-.")[:80]
    digest = hashlib.sha256(concern_key.encode("utf-8")).hexdigest()[:10]
    return f"{readable}-{digest}" if readable else digest


def report_path_for(concern_key: str) -> str:
    return f"{REPORT_DIR}/{concern_slug(concern_key)}.json"


def other_client(client: ClientName) -> ClientName:
    return "codex" if client == "claude-code" else "claude-code"
