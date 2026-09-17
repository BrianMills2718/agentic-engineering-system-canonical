from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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


class ConcernRootObservation(StrictModel):
    concern: str = Field(min_length=1)
    state: EpistemicState
    path: str | None = None
    evidence_refs: tuple[str, ...] = ()


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
