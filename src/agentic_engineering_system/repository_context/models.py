from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EpistemicState(StrEnum):
    OBSERVED = "OBSERVED"
    NONE = "NONE"
    ERROR = "ERROR"
    UNRESOLVED = "UNRESOLVED"


class ResolutionStatus(StrEnum):
    RESOLVED = "RESOLVED"
    PARTIAL = "PARTIAL"
    ERROR = "ERROR"


class AuthorityRole(StrEnum):
    NAVIGATION = "navigation"
    NORMATIVE = "normative"
    DECISION = "decision"
    PLAN = "plan"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"
    CONTRACT = "contract"
    OWNERSHIP = "ownership"


class EvidenceRef(StrictModel):
    evidence_id: str = Field(min_length=1)
    repository_id: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    path: str = Field(min_length=1)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    source_url: str | None = None
    note: str | None = None


class AuthoritySurfaceObservation(StrictModel):
    role: AuthorityRole
    state: EpistemicState
    locations: tuple[str, ...] = ()
    summary: str
    evidence_refs: tuple[str, ...] = ()

    @model_validator(mode="after")
    def observed_claim_requires_positive_evidence(self) -> "AuthoritySurfaceObservation":
        if self.state == EpistemicState.OBSERVED:
            if not self.locations:
                raise ValueError("OBSERVED authority claims require at least one location")
            if not self.evidence_refs:
                raise ValueError("OBSERVED authority claims require at least one evidence reference")
        return self


class ConcernRootObservation(StrictModel):
    concern: str = Field(min_length=1)
    state: EpistemicState
    path: str | None = None
    evidence_refs: tuple[str, ...] = ()

    @model_validator(mode="after")
    def observed_claim_requires_positive_evidence(self) -> "ConcernRootObservation":
        if self.state == EpistemicState.OBSERVED:
            if not self.path:
                raise ValueError("OBSERVED concern-root claims require a path")
            if not self.evidence_refs:
                raise ValueError("OBSERVED concern-root claims require at least one evidence reference")
        return self


class UnresolvedSurface(StrictModel):
    subject: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    evidence_refs: tuple[str, ...] = ()


class RepositoryContextArtifact(StrictModel):
    schema_version: Literal["0.1"] = "0.1"
    repository_id: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    resolution_status: ResolutionStatus
    navigation: AuthoritySurfaceObservation
    authorities: tuple[AuthoritySurfaceObservation, ...] = ()
    concern_roots: tuple[ConcernRootObservation, ...] = ()
    unresolved: tuple[UnresolvedSurface, ...] = ()
    evidence: tuple[EvidenceRef, ...] = ()

    @model_validator(mode="after")
    def positive_claim_references_resolve(self) -> "RepositoryContextArtifact":
        evidence_ids = {item.evidence_id for item in self.evidence}
        observations = (self.navigation, *self.authorities)
        for observation in observations:
            if observation.state == EpistemicState.OBSERVED:
                missing = set(observation.evidence_refs) - evidence_ids
                if missing:
                    raise ValueError(
                        f"OBSERVED {observation.role.value} claim references missing evidence: {sorted(missing)}"
                    )
        for concern in self.concern_roots:
            if concern.state == EpistemicState.OBSERVED:
                missing = set(concern.evidence_refs) - evidence_ids
                if missing:
                    raise ValueError(
                        f"OBSERVED concern {concern.concern} references missing evidence: {sorted(missing)}"
                    )
        return self
