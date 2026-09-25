"""Observations, freshness and criterion standing (`RU-AES-EVIDENCE`,
`SC-GF-007`, `SC-GF-008`, decision D2).

Observation records follow `16-record-shapes.candidate.yaml`. Assessments are
materialized inside the observation (option `retained_inside_observation_
assessment_receipt`), one per evidence requirement, never per criterion:
an observation does not claim criterion sufficiency.

Freshness is computed from Git. An observation names the commit it observed
(`subject_revision`) and the repository paths its result depends on
(`dependency_paths`). It is CURRENT when none of those paths changed between
that commit and HEAD, STALE when any did, and UNKNOWN when it names no commit
or no paths (external subjects, human review). Only CURRENT assessments count.

Standing per criterion (D2, conjunction only):
- REFUTED when any evidence requirement has a CURRENT refuting assessment;
- SUPPORTED when every evidence requirement has a CURRENT supporting assessment;
- INSUFFICIENT otherwise, with the reason per requirement.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, model_validator

from .records import (
    RecordLoadError,
    StrictModel,
    TargetRecord,
    _validate_model,
    load_project,
    load_target,
    load_yaml_mapping,
)

OBSERVATION_SCHEMA = "aes.v0_2.observation.probe0"
_COMMIT = re.compile(r"^[0-9a-f]{40}$")

Assessment = Literal["SUPPORTS", "REFUTES", "INCONCLUSIVE"]
Freshness = Literal["CURRENT", "STALE", "UNKNOWN"]
Standing = Literal["SUPPORTED", "REFUTED", "INSUFFICIENT"]


class EvidenceError(ValueError):
    """Observations could not be loaded or checked against the target."""


class Observer(StrictModel):
    identity: str
    version: str | None = None


class ErAssessment(StrictModel):
    evidence_requirement_ref: str
    assessment: Assessment
    basis: str
    assessor: Observer


class DependencyBasis(StrictModel):
    """Where `dependency_paths` came from: the subject's own file, what AES
    discovered from its intra-repository imports, and what the recorder declared."""

    locator: str
    discovered: list[str] = Field(default_factory=list)
    declared: list[str] = Field(default_factory=list)


class ObservationRecord(StrictModel):
    schema_version: Literal["aes.v0_2.observation.probe0"]
    observation_id: str
    subject_refs: list[str]
    subject_revision: str | None = Field(
        default=None, description="40-hex commit the observation observed; None for external subjects",
    )
    external_identity: str | None = None
    dependency_paths: list[str] = Field(default_factory=list)
    dependency_basis: DependencyBasis | None = None
    observer: Observer
    method: str
    execution_state: Literal["COMPLETED", "ERROR"]
    result: dict[str, Any] | None = None
    error: str | None = None
    produced_at: datetime
    retained_artifact_refs: list[str] = Field(default_factory=list)
    assessments: list[ErAssessment] = Field(default_factory=list)

    @model_validator(mode="after")
    def _shape(self) -> ObservationRecord:
        if self.subject_revision is None and self.external_identity is None:
            raise ValueError("needs subject_revision or external_identity")
        if self.subject_revision is not None and not _COMMIT.fullmatch(self.subject_revision):
            raise ValueError(f"subject_revision must be a full 40-hex commit: {self.subject_revision!r}")
        if (self.result is None) == (self.error is None):
            raise ValueError("exactly one of result or error is required")
        if (self.execution_state == "ERROR") != (self.error is not None):
            raise ValueError("execution_state ERROR requires error, COMPLETED requires result")
        if self.execution_state == "ERROR" and self.assessments:
            raise ValueError("an ERROR observation cannot carry assessments")
        if self.dependency_basis is not None:
            b = self.dependency_basis
            union = sorted({b.locator, *b.discovered, *b.declared})
            if self.dependency_paths != union:
                raise ValueError(
                    f"dependency_paths {self.dependency_paths} is not the union of dependency_basis {union}"
                )
        return self


def load_observations(root: Path, observations_root: str, target: TargetRecord) -> list[ObservationRecord]:
    directory = root / observations_root
    if not directory.is_dir():
        return []
    ers = target.evidence_requirements()
    ids = {i for members in target.families().values() for i in members}
    out: list[ObservationRecord] = []
    seen: set[str] = set()
    for path in sorted(directory.glob("*.yaml")):
        obs: ObservationRecord = _validate_model(ObservationRecord, load_yaml_mapping(path), path)
        problems = []
        if obs.observation_id in seen:
            problems.append(f"duplicate observation_id {obs.observation_id!r}")
        seen.add(obs.observation_id)
        problems += [f"unknown subject_ref {r!r}" for r in obs.subject_refs if r not in ids]
        problems += [
            f"unknown evidence_requirement_ref {a.evidence_requirement_ref!r}"
            for a in obs.assessments if a.evidence_requirement_ref not in ers
        ]
        if problems:
            raise EvidenceError(f"{path}: " + "; ".join(problems))
        out.append(obs)
    return out


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise EvidenceError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def freshness(root: Path, obs: ObservationRecord) -> tuple[Freshness, str]:
    if obs.subject_revision is None or not obs.dependency_paths:
        return "UNKNOWN", "no subject_revision or no dependency_paths"
    _git(root, "cat-file", "-e", f"{obs.subject_revision}^{{commit}}")
    changed = [
        p for p in _git(root, "diff", "--name-only", obs.subject_revision, "HEAD", "--", *obs.dependency_paths)
        .splitlines() if p
    ]
    if changed:
        return "STALE", "changed since observed: " + ", ".join(changed)
    return "CURRENT", f"no dependency changed since {obs.subject_revision[:12]}"


@dataclass(frozen=True)
class ErStatus:
    er_id: str
    status: Literal["SUPPORTED", "REFUTED", "NO_CURRENT_SUPPORT"]
    detail: str


@dataclass(frozen=True)
class CriterionStanding:
    criterion_id: str
    standing: Standing
    requirements: tuple[ErStatus, ...]


@dataclass(frozen=True)
class EvidenceReport:
    criteria: tuple[CriterionStanding, ...]
    observations: tuple[tuple[str, Freshness, str], ...]


def assess(root: Path) -> EvidenceReport:
    root = Path(root).resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / project.materialization.target_path)
    observations = load_observations(root, project.materialization.observations_root, target)

    fresh = {o.observation_id: freshness(root, o) for o in observations}
    by_er: dict[str, list[tuple[ObservationRecord, ErAssessment]]] = {}
    for o in observations:
        for a in o.assessments:
            by_er.setdefault(a.evidence_requirement_ref, []).append((o, a))

    criteria = []
    for sc in target.success_criteria:
        statuses = []
        for er in sc.evidence_requirements:
            entries = by_er.get(er.id, [])
            current = [(o, a) for o, a in entries if fresh[o.observation_id][0] == "CURRENT"]
            refuting = [o.observation_id for o, a in current if a.assessment == "REFUTES"]
            supporting = [o.observation_id for o, a in current if a.assessment == "SUPPORTS"]
            if refuting:
                statuses.append(ErStatus(er.id, "REFUTED", "refuted by " + ", ".join(refuting)))
            elif supporting:
                statuses.append(ErStatus(er.id, "SUPPORTED", "supported by " + ", ".join(supporting)))
            elif entries:
                why = "; ".join(
                    f"{o.observation_id} {a.assessment} ({fresh[o.observation_id][0]})" for o, a in entries
                )
                statuses.append(ErStatus(er.id, "NO_CURRENT_SUPPORT", why))
            else:
                statuses.append(ErStatus(er.id, "NO_CURRENT_SUPPORT", "no observation assesses it"))
        if any(s.status == "REFUTED" for s in statuses):
            standing: Standing = "REFUTED"
        elif all(s.status == "SUPPORTED" for s in statuses):
            standing = "SUPPORTED"
        else:
            standing = "INSUFFICIENT"
        criteria.append(CriterionStanding(sc.id, standing, tuple(statuses)))
    return EvidenceReport(
        criteria=tuple(criteria),
        observations=tuple((oid, f[0], f[1]) for oid, f in fresh.items()),
    )


def render_report(report: EvidenceReport) -> str:
    counts = {s: sum(c.standing == s for c in report.criteria) for s in ("SUPPORTED", "INSUFFICIENT", "REFUTED")}
    lines = [
        f"evidence: {len(report.criteria)} criteria: {counts['SUPPORTED']} supported, "
        f"{counts['INSUFFICIENT']} insufficient, {counts['REFUTED']} refuted; "
        f"{len(report.observations)} observation(s)"
    ]
    for c in report.criteria:
        lines.append(f"  {c.criterion_id}: {c.standing}")
        for s in c.requirements:
            lines.append(f"    {s.er_id}: {s.status} - {s.detail}")
    lines.append("  observations:")
    for oid, f, why in report.observations:
        lines.append(f"    {oid}: {f} - {why}")
    return "\n".join(lines)


__all__ = [
    "EvidenceError", "ObservationRecord", "assess", "freshness", "load_observations", "render_report",
    "RecordLoadError",
]


# --------------------------------------------------------------------------- #
# Recording: run a verification subject and write the observation
# --------------------------------------------------------------------------- #

RECORDER = "aes evidence record"


def _discover_dependencies(root: Path, locator: str) -> list[str]:
    """Governed files a Python test's imports reach at HEAD, the test excluded.

    Non-Python subjects discover nothing. A Python subject that is not a
    governed file at HEAD cannot be analyzed, so recording it fails.
    """
    if not locator.endswith(".py"):
        return []
    from .characterize import CharacterizeError, characterize
    from .characterize_python import import_closure

    try:
        facts = characterize(root).python_facts()
    except CharacterizeError as exc:
        raise EvidenceError(f"cannot discover dependencies of {locator}: {exc}") from exc
    if locator not in facts:
        raise EvidenceError(
            f"cannot discover dependencies of {locator}: not a governed Python file at HEAD "
            "(commit it, or place it under a governed root)"
        )
    if facts[locator].parse_error:
        raise EvidenceError(f"cannot discover dependencies of {locator}: {facts[locator].parse_error}")
    return import_closure(locator, facts)
_OUTPUT_TAIL_LINES = 20


@dataclass(frozen=True)
class Recorded:
    path: Path
    observation: ObservationRecord


def _aes_version() -> str:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("agentic-engineering-system")
    except PackageNotFoundError:
        return "unknown"


def record(
    root: Path,
    subject_id: str,
    depends_on: list[str],
    command: list[str] | None = None,
    downgrade_basis: str | None = None,
) -> Recorded:
    """Run one deterministic-test verification subject at HEAD and write its observation.

    Dependency paths are the test file, plus, for a Python test, every governed
    file its imports reach at HEAD (discovered by `characterize`), plus
    `depends_on` (declared). The observation's `dependency_basis` keeps the three
    apart.

    Exit 0 assesses every evidence requirement the subject proves as SUPPORTS
    (INCONCLUSIVE with `downgrade_basis`, for a test that covers only part of a
    requirement); any other exit assesses them as REFUTES. Refuses when a
    dependency has uncommitted changes, because the observation must name the
    commit that holds exactly what was run.
    """
    import sys
    from datetime import UTC

    from ruamel.yaml import YAML

    root = Path(root).resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / project.materialization.target_path)
    subjects = {v.id: v for v in target.verification_subjects}
    if subject_id not in subjects:
        raise EvidenceError(f"unknown verification subject {subject_id!r}")
    vs = subjects[subject_id]
    if vs.proof_kind != "deterministic_test":
        raise EvidenceError(
            f"{subject_id} is {vs.proof_kind}; only deterministic_test subjects can be recorded by running them"
        )
    if vs.locator.startswith("external:") or not (root / vs.locator).exists():
        raise EvidenceError(f"{subject_id} locator {vs.locator!r} is not a path in this repository")

    discovered = _discover_dependencies(root, vs.locator)
    declared = sorted(set(depends_on))
    deps = sorted({vs.locator, *discovered, *declared})
    missing = [d for d in deps if not (root / d).exists()]
    if missing:
        raise EvidenceError(f"dependency paths do not exist: {missing}")
    dirty = [p for p in _git(root, "status", "--porcelain", "--", *deps).splitlines() if p]
    if dirty:
        raise EvidenceError("commit before observing; uncommitted dependency changes: " + "; ".join(dirty))
    revision = _git(root, "rev-parse", "HEAD").strip()

    if command is None:
        if project.ecosystem.primary_language_or_runtime != "python":
            raise EvidenceError("no default test command for this ecosystem; pass --command")
        command = [sys.executable, "-m", "pytest", "-q", vs.locator]
    proc = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    output = (proc.stdout + proc.stderr).strip().splitlines()[-_OUTPUT_TAIL_LINES:]

    if proc.returncode == 0:
        assessment, basis = ("INCONCLUSIVE", downgrade_basis) if downgrade_basis else (
            "SUPPORTS", f"{subject_id} ({vs.purpose}) passed: exit 0")
    else:
        assessment, basis = "REFUTES", f"{subject_id} failed: exit {proc.returncode}"
    assessor = {"identity": RECORDER, "version": _aes_version()}

    base = f"OBS-{subject_id.removeprefix('VS-')}-{revision[:8]}"
    obs_dir = root / project.materialization.observations_root
    obs_dir.mkdir(parents=True, exist_ok=True)
    oid, n = base, 1
    while (obs_dir / f"{oid}.yaml").exists():
        n += 1
        oid = f"{base}-{n}"
    data = {
        "schema_version": OBSERVATION_SCHEMA,
        "observation_id": oid,
        "subject_refs": [subject_id],
        "subject_revision": revision,
        "dependency_paths": deps,
        "dependency_basis": {"locator": vs.locator, "discovered": discovered, "declared": declared},
        "observer": assessor,
        "method": " ".join(command),
        "execution_state": "COMPLETED",
        "result": {"exit_code": proc.returncode, "output_tail": "\n".join(output)},
        "produced_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "assessments": [
            {"evidence_requirement_ref": er, "assessment": assessment, "basis": basis, "assessor": assessor}
            for er in vs.evidence_requirement_refs
        ],
    }
    observation = ObservationRecord.model_validate(data)
    path = obs_dir / f"{oid}.yaml"
    yaml = YAML()
    yaml.width = 100
    with path.open("x", encoding="utf-8") as fh:
        yaml.dump(data, fh)
    return Recorded(path, observation)
