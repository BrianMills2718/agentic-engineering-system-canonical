"""AES profile and handoff accounting contracts consumed by native adapters.

Profiles narrow a caller-supplied authority and capability snapshot. These
contracts describe configuration and recorded evidence; native delivery and
outcome verification remain separate acceptance checks.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from typing import Literal, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ProposalStatus = Literal[
    "valid", "invalid", "capped", "call_failed", "input_unavailable", "unsupported"
]
STATUSES = ("valid", "invalid", "capped", "call_failed", "input_unavailable", "unsupported")


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BudgetLimits(Contract):
    daily_cap_usd: float
    total_cap_usd: float

    @field_validator("daily_cap_usd", "total_cap_usd")
    @classmethod
    def finite_nonnegative(cls, value: float) -> float:
        if not math.isfinite(value) or value < 0:
            raise ValueError("budget limits must be finite and nonnegative")
        return value


class NativeCapabilities(Contract):
    client: Literal["claude", "codex"]
    version: str
    roles: list[str]
    models: list[str] = Field(default_factory=list)
    efforts: list[str] = Field(default_factory=list)
    field_map: dict[str, str]
    evidence_ref: str


class AgentRouterProfileV1(BudgetLimits):
    schema_version: Literal["agent-router-profile.v1"] = "agent-router-profile.v1"
    extension_owner: Literal["AES"] = "AES"
    profile_id: str
    mode: Literal["off", "manual", "observe"] = "manual"
    allowed_rule_ids: list[str]
    required_rule_ids: list[str]
    specialist_aliases: dict[str, str]
    allowed_models: list[str] = Field(default_factory=list)
    allowed_efforts: list[str] = Field(default_factory=list)
    native_field_maps: dict[str, dict[str, str]]
    provider_route: str
    workspace_env: str = "WORKSPACE_ROOT"
    log_root_env: str = "AGENT_ROUTER_OUT"


class EffectiveProfile(Contract):
    profile_id: str
    profile_digest: str
    client: str
    client_version: str
    capability_evidence_ref: str
    capability_digest: str
    mode: Literal["off", "manual", "observe"]
    provider_route: str
    allowed_rule_ids: list[str]
    allowed_models: list[str]
    allowed_efforts: list[str]
    required_rule_ids: list[str]
    specialist_aliases: dict[str, str]
    native_field_map: dict[str, str]
    budgets: BudgetLimits
    workspace_root: str
    log_root: str


def digest(value: BaseModel | Mapping) -> str:
    data = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def resolve_profile(
    profile: AgentRouterProfileV1,
    capabilities: NativeCapabilities,
    *,
    registry_ids: set[str],
    mandatory_rule_ids: set[str],
    authority_limits: BudgetLimits,
    authorized_provider_routes: set[str],
    environment: Mapping[str, str],
) -> EffectiveProfile:
    """Resolve configuration against trusted inputs supplied by the owning caller."""
    allowed = set(profile.allowed_rule_ids)
    required = mandatory_rule_ids | set(profile.required_rule_ids)
    if not allowed <= registry_ids or not required <= registry_ids:
        raise ValueError("profile contains unknown rule IDs")
    if not required <= allowed:
        raise ValueError("profile removes a required rule")
    if not set(profile.specialist_aliases.values()) <= set(capabilities.roles):
        raise ValueError("profile names an unsupported native role")
    if not set(profile.allowed_models) <= set(capabilities.models):
        raise ValueError("profile names an unsupported native model")
    if not set(profile.allowed_efforts) <= set(capabilities.efforts):
        raise ValueError("profile names an unsupported native effort")
    fields = profile.native_field_maps.get(capabilities.client)
    if fields is None or "subagent" not in fields:
        raise ValueError("profile has no native role mapping for this client")
    if not set(fields) <= {"subagent", "model", "effort"}:
        raise ValueError("profile contains an unknown logical field")
    if not set(fields.items()) <= set(capabilities.field_map.items()):
        raise ValueError("profile names an unsupported native field")
    if profile.provider_route not in authorized_provider_routes:
        raise ValueError("profile cannot authorize a provider route")
    roots = []
    for key in (profile.workspace_env, profile.log_root_env):
        value = environment.get(key)
        if not value or not Path(value).is_absolute():
            raise ValueError(f"{key} must resolve to an explicit absolute path")
        roots.append(str(Path(value).resolve()))
    return EffectiveProfile(
        profile_id=profile.profile_id, profile_digest=digest(profile),
        client=capabilities.client, client_version=capabilities.version,
        capability_evidence_ref=capabilities.evidence_ref,
        capability_digest=digest(capabilities), mode=profile.mode,
        provider_route=profile.provider_route, allowed_rule_ids=sorted(allowed),
        allowed_models=profile.allowed_models, allowed_efforts=profile.allowed_efforts,
        required_rule_ids=sorted(required), specialist_aliases=profile.specialist_aliases,
        native_field_map=fields,
        budgets=BudgetLimits(
            daily_cap_usd=min(profile.daily_cap_usd, authority_limits.daily_cap_usd),
            total_cap_usd=min(profile.total_cap_usd, authority_limits.total_cap_usd),
        ), workspace_root=roots[0], log_root=roots[1],
    )


class RouterProposal(Contract):
    subagent: str
    rule_ids: list[str]
    model: str | None = None
    effort: str | None = None
    confidence: float

    @field_validator("confidence")
    @classmethod
    def probability(cls, value: float) -> float:
        if not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("confidence must be a finite probability")
        return value


class IndependentOutcome(Contract):
    status: Literal["pass", "fail", "inconclusive"]
    check_id: str
    check_output_ref: str


class ActualChoice(Contract):
    subagent: str
    model: str | None = None
    effort: str | None = None
    native_dispatch_ref: str
    choice_source: Literal["incumbent", "proposed", "fallback"]


class HandoffRecordV1(Contract):
    schema_version: Literal["agent-router-handoff.v1"] = "agent-router-handoff.v1"
    extension_owner: Literal["AES"] = "AES"
    handoff_id: str
    input_digest: str | None
    profile_digest: str | None
    capability_digest: str | None = None
    register_revision: str | None = None
    specialist_revision: str | None = None
    parent_session_id: str | None
    child_session_id: str | None = None
    full_trace_ref: str
    proposal_status: ProposalStatus
    failure_reason: str | None = None
    proposal: RouterProposal | None = None
    llm_attempted: bool = False
    llm_call_id: str | None = None
    actual_choice: ActualChoice | None = None
    actual_cost_usd: float | None = None
    latency_ms: float | None = None
    outcome: IndependentOutcome | None = None
    replayed: bool = False

    @field_validator("input_digest", "profile_digest", "capability_digest")
    @classmethod
    def sha256_digest(cls, value: str | None) -> str | None:
        if value is not None and (len(value) != 64 or any(c not in "0123456789abcdef" for c in value)):
            raise ValueError("digest must be a lowercase SHA256 or explicitly unavailable")
        return value

    @model_validator(mode="after")
    def coherent(self) -> HandoffRecordV1:
        if self.proposal_status == "valid" and self.proposal is None:
            raise ValueError("a valid proposal requires its actual structured proposal")
        if self.proposal_status == "valid" and any(value is None for value in (
            self.input_digest, self.profile_digest, self.capability_digest,
            self.register_revision, self.specialist_revision, self.parent_session_id,
        )):
            raise ValueError("a valid proposal requires its input, effective configuration and revisions")
        if self.proposal_status != "valid" and not self.failure_reason:
            raise ValueError("unsuccessful proposals require a concrete reason")
        if self.llm_call_id and not self.llm_attempted:
            raise ValueError("a recorded LLM call cannot be labelled not attempted")
        if self.actual_choice and self.actual_choice.choice_source == "proposed" and self.proposal_status != "valid":
            raise ValueError("an unsuccessful proposal cannot be recorded as the dispatched choice")
        for value in (self.actual_cost_usd, self.latency_ms):
            if value is not None and (not math.isfinite(value) or value < 0):
                raise ValueError("cost and latency must be finite and nonnegative")
        return self


def account_handoffs(eligible_ids: Sequence[str], records: Sequence[HandoffRecordV1]) -> dict:
    """Report exact membership and outcome coverage separately from proposal validity."""
    if len(set(eligible_ids)) != len(eligible_ids):
        raise ValueError("eligible handoff IDs contain duplicates")
    eligible = set(eligible_ids)
    seen = Counter(record.handoff_id for record in records)
    duplicates = sorted(key for key, count in seen.items() if count > 1)
    unexpected = sorted(set(seen) - eligible)
    missing = sorted(eligible - set(seen))
    accepted = [r for r in records if r.handoff_id in eligible and seen[r.handoff_id] == 1]
    counts = Counter(r.proposal_status for r in accepted)
    return {
        "eligible_ids": list(eligible_ids), "eligible_total": len(eligible),
        "accounting_complete": not (duplicates or unexpected or missing),
        "missing_ids": missing, "duplicate_ids": duplicates, "unexpected_ids": unexpected,
        "proposal_status_counts": {status: counts[status] for status in STATUSES},
        "missing_outcome_ids": sorted(r.handoff_id for r in accepted if r.outcome is None),
        "outcome_status_counts": dict(Counter(r.outcome.status for r in accepted if r.outcome)),
        "unknown_cost_ids": sorted(r.handoff_id for r in accepted
                                   if (r.llm_attempted or r.actual_choice) and r.actual_cost_usd is None),
        "missing_latency_ids": sorted(r.handoff_id for r in accepted if r.latency_ms is None),
        "known_cost_usd": sum(r.actual_cost_usd or 0 for r in accepted),
        "replayed_ids": sorted(r.handoff_id for r in accepted if r.replayed),
    }
