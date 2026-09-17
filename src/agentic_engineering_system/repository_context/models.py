from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SurfaceState(str, Enum):
    OBSERVED = "OBSERVED"
    NONE = "NONE"
    ERROR = "ERROR"
    UNRESOLVED = "UNRESOLVED"


class ResolutionStatus(str, Enum):
    RESOLVED = "RESOLVED"
    PARTIAL = "PARTIAL"
    ERROR = "ERROR"


class AuthorityRole(str, Enum):
    NAVIGATION = "navigation"
    NORMATIVE = "normative"
    DECISION = "decision"
    PLAN = "plan"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"
    CONTRACT = "contract"
    OWNERSHIP = "ownership"


class EvidenceRef(FrozenModel):
    evidence_id: str = Field(min_length=1)
    repository_id: str = Field(min_length=1)
    revision: str = Field(min_length=1)
    path: str = Field(min_length=1)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    source_url: str | None = None
    note: str | None = None


class AuthoritySurfaceObservation(FrozenModel):
    role: AuthorityRole
    state: SurfaceState
    locations: tuple[str, ...] = ()
    summary: str = Field(min_length=1)
    evidence_refs: tuple[str, ...] = ()

    @model_validator(mode="after")
    def observed_has_evidence(self) -> "AuthoritySurfaceObservation":
        if self.state is SurfaceState.OBSERVED and not self.evidence_refs:
            raise ValueError("OBSERVED authority claims require evidence_refs")
        return self


class ConcernRootObservation(FrozenModel):
    concern: str = Field(min_length=1)
    state: SurfaceState
    path: str | None = None
    evidence_refs: tuple[str, ...] = ()

    @model_validator(mode="after")
    def observed_has_evidence(self) -> "ConcernRootObservation":
        if self.state is SurfaceState.OBSERVED and not self.evidence_refs:
            raise ValueError("OBSERVED concern roots require evidence_refs")
        return self


class UnresolvedSurface(FrozenModel):
    subject: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    evidence_refs: tuple[str, ...] = ()


class RepositoryContextArtifact(FrozenModel):
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
    def referenced_evidence_exists(self) -> "RepositoryContextArtifact":
        ids = {item.evidence_id for item in self.evidence}
        refs: set[str] = set(self.navigation.evidence_refs)
        for item in self.authorities:
            refs.update(item.evidence_refs)
        for item in self.concern_roots:
            refs.update(item.evidence_refs)
        for item in self.unresolved:
            refs.update(item.evidence_refs)
        missing = sorted(refs - ids)
        if missing:
            raise ValueError(f"unknown evidence refs: {missing}")
        return self
