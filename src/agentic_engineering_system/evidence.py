"""Observations, freshness and criterion standing (`RU-AES-EVIDENCE`,
`SC-GF-007`, `SC-GF-008`, decision D2).

Observation records follow `docs/architecture/greenfield-v0.2/16-record-shapes.yaml`. Assessments are
materialized inside the observation (option `retained_inside_observation_
assessment_receipt`), one per evidence requirement, never per criterion:
an observation does not claim criterion sufficiency.

Freshness is computed from Git. An observation names the commit it observed
(`subject_revision`), the repository paths its result depends on
(`dependency_paths`) and the target entries it depends on
(`dependency_target_refs`). It is CURRENT when none of those paths changed
between that commit and HEAD and every referenced entry of the target file is
the same at both, STALE when any path changed or any referenced entry changed
or disappeared, and UNKNOWN when it names no commit or no dependency at all
(external subjects, human review). Only CURRENT assessments count.

Reachability comes first: an observation whose commit is not an ancestor of
HEAD (`git merge-base --is-ancestor`) is UNREACHABLE, whatever its dependencies
say. A squash-merged and deleted branch leaves its commits in the recording
machine's object store, where they still resolve and diff, but in no fresh
clone; judging freshness from them would make standing depend on which clone
computed it. A commit this clone does not have at all is UNREACHABLE for the
same reason and with the same text, so every clone agrees.

`superseded_by: <observation_id>` marks an observation replaced by a later one
(re-recorded after a squash merge, say). Records are never deleted; a
superseded observation keeps its freshness for the record but never counts
toward standing, and reports count it separately.

Target dependencies are entry-level: an entry is its id's whole mapping
(a criterion with its nested evidence requirements, a verification subject,
...), compared after a strict load of the target at each revision, so an edit
elsewhere in the file does not stale the observation. Listing the target file
itself in `dependency_paths` still works and is the coarse form: any edit to
the file stales the observation. Existing records are never rewritten.

A negative control (`control: {kind: negative, ...}`) observes a deliberately
mutated revision that exists only to show a check detects the mutation. Its
`subject_revision` is that mutated commit, which may be on no branch; its
freshness is computed from `control.base_revision`, the unmodified commit on a
real branch the mutation was made from, because that is the state whose
dependencies the control speaks for; reachability applies to that base, while
the mutated commit only has to resolve (a tag keeps it). Its assessments follow its outcome:
`observed_outcome: detected` may SUPPORT, `missed` must REFUTE, and a result
whose `exit_code` is 0 (the tool reported passing) cannot claim `detected`.

Standing per criterion (D2, conjunction only):
- REFUTED when any evidence requirement has a CURRENT refuting assessment;
- SUPPORTED when every evidence requirement has a CURRENT supporting assessment;
- INSUFFICIENT otherwise, with the reason per requirement.
"""

from __future__ import annotations

import json
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
    TargetValidationError,
    _validate_model,
    load_project,
    load_target,
    load_yaml_mapping,
    parse_target,
    parse_yaml_mapping,
)

OBSERVATION_SCHEMA = "aes.v0_2.observation.probe0"
_COMMIT = re.compile(r"^[0-9a-f]{40}$")

Assessment = Literal["SUPPORTS", "REFUTES", "INCONCLUSIVE"]
Freshness = Literal["CURRENT", "STALE", "UNKNOWN", "UNREACHABLE"]
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


class NegativeControl(StrictModel):
    """The observation is of a deliberately broken revision (a "break it on purpose" run).

    `base_revision` is the unmodified commit, on a real branch, that the mutation
    was made from; freshness is computed from it. `mutation` says what was changed.
    `expected_outcome` is always `detected`; `observed_outcome` says whether the
    check under test detected the mutation, and fixes what the assessments may say.
    """

    kind: Literal["negative"]
    base_revision: str
    mutation: str
    expected_outcome: Literal["detected"]
    observed_outcome: Literal["detected", "missed"]

    @model_validator(mode="after")
    def _shape(self) -> NegativeControl:
        if not _COMMIT.fullmatch(self.base_revision):
            raise ValueError(f"control.base_revision must be a full 40-hex commit: {self.base_revision!r}")
        if not self.mutation:
            raise ValueError("control.mutation must say what was changed")
        return self


class DecisionCheck(StrictModel):
    """One output of the run, followed back to the source it was made from."""

    decision: str
    source: str
    verdict: Literal["correct", "wrong", "unclear"]
    note: str = ""


class TraceReview(StrictModel):
    """What a `trace_review` observation must say: the run read end to end, not judged by its output.

    The reviewer is not the author. Every step of the trace is read (`steps_read == steps_total`
    for SUPPORTS); the record says which model and settings each step used, what each step was
    shown, whether outputs carry reasons, and follows decisions back to their sources.
    """

    trace_refs: list[str] = Field(min_length=1, description="trace ids and where their records are stored")
    author: str
    reviewer: str
    steps_total: int = Field(ge=1)
    steps_read: int = Field(ge=0)
    models_and_settings: str
    context_per_step: str
    outputs_and_reasons: str
    decisions_checked: list[DecisionCheck] = Field(min_length=1)
    findings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _shape(self) -> TraceReview:
        if self.author.strip().lower() == self.reviewer.strip().lower():
            raise ValueError("trace_review.reviewer must not be the work's author")
        if self.steps_read > self.steps_total:
            raise ValueError(f"trace_review.steps_read {self.steps_read} exceeds steps_total {self.steps_total}")
        for name in ("models_and_settings", "context_per_step", "outputs_and_reasons"):
            if not getattr(self, name).strip():
                raise ValueError(f"trace_review.{name} must say what the trace showed")
        return self


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
    dependency_target_refs: list[str] = Field(
        default_factory=list,
        description="target entry ids the result depends on; compared entry by entry, not as a file",
    )
    control: NegativeControl | None = None
    observer: Observer
    method: str
    execution_state: Literal["COMPLETED", "ERROR"]
    result: dict[str, Any] | None = None
    error: str | None = None
    produced_at: datetime
    retained_artifact_refs: list[str] = Field(default_factory=list)
    assessments: list[ErAssessment] = Field(default_factory=list)
    trace_review: TraceReview | None = Field(
        default=None, description="required when any assessment is of a trace_review evidence requirement",
    )
    superseded_by: str | None = Field(
        default=None, description="observation_id of the record that replaces this one; it then never counts",
    )

    @model_validator(mode="after")
    def _shape(self) -> ObservationRecord:
        if self.superseded_by == self.observation_id:
            raise ValueError("an observation cannot be superseded_by itself")
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
        dup = sorted({r for r in self.dependency_target_refs if self.dependency_target_refs.count(r) > 1})
        if dup:
            raise ValueError(f"dependency_target_refs lists {dup} more than once")
        if self.control is not None:
            c = self.control
            if self.subject_revision is None:
                raise ValueError("a negative control needs subject_revision (the mutated commit)")
            if c.base_revision == self.subject_revision:
                raise ValueError("a negative control's base_revision must differ from its mutated subject_revision")
            if c.observed_outcome == "detected" and self.result is not None and self.result.get("exit_code") == 0:
                raise ValueError(
                    "negative control claims observed_outcome detected, but its result reports exit_code 0 "
                    "(the tool passed the mutated revision); record observed_outcome: missed with REFUTES"
                )
            allowed = {"detected": {"SUPPORTS", "INCONCLUSIVE"}, "missed": {"REFUTES"}}[c.observed_outcome]
            wrong = [f"{a.evidence_requirement_ref} {a.assessment}" for a in self.assessments
                     if a.assessment not in allowed]
            if wrong:
                raise ValueError(
                    f"negative control observed_outcome {c.observed_outcome} allows only {sorted(allowed)}; "
                    f"got {wrong}"
                )
        if self.dependency_basis is not None:
            b = self.dependency_basis
            union = sorted({b.locator, *b.discovered, *b.declared})
            if self.dependency_paths != union:
                raise ValueError(
                    f"dependency_paths {self.dependency_paths} is not the union of dependency_basis {union}"
                )
        return self


def _trace_review_problems(obs: ObservationRecord, ers: dict[str, Any]) -> list[str]:
    """A trace_review assessment needs a TraceReview record, and SUPPORTS needs the whole trace read
    with no decision found wrong."""
    refs = [a for a in obs.assessments if a.evidence_requirement_ref in ers
            and ers[a.evidence_requirement_ref][1].kind == "trace_review"]
    if not refs:
        return []
    tr = obs.trace_review
    if tr is None:
        return [f"assesses trace_review requirement(s) {[a.evidence_requirement_ref for a in refs]} "
                f"but carries no trace_review record"]
    problems = []
    for a in refs:
        if a.assessment != "SUPPORTS":
            continue
        if tr.steps_read < tr.steps_total:
            problems.append(f"{a.evidence_requirement_ref} SUPPORTS, but only {tr.steps_read} of "
                            f"{tr.steps_total} trace steps were read")
        wrong = [d.decision for d in tr.decisions_checked if d.verdict == "wrong"]
        if wrong:
            problems.append(f"{a.evidence_requirement_ref} SUPPORTS, but decisions were found wrong: {wrong}")
    return problems


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
        problems += _trace_review_problems(obs, ers)
        if problems:
            raise EvidenceError(f"{path}: " + "; ".join(problems))
        out.append(obs)
    dangling = [f"{o.observation_id} superseded_by {o.superseded_by!r}" for o in out
                if o.superseded_by is not None and o.superseded_by not in seen]
    if dangling:
        raise EvidenceError(f"{directory}: superseded_by names no loaded observation: " + "; ".join(dangling))
    return out


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise EvidenceError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def _target_entries_at(root: Path, revision: str, target_path: str) -> dict[str, str]:
    """Every id of the target at `revision` -> its entry, canonically serialized.

    Strict load, as for the live target: a target that does not load at an
    observed revision is an error, not a freshness verdict.
    """
    key = (str(root), revision, target_path)
    if key not in _ENTRY_CACHE:
        label = f"{target_path}@{revision[:12]}"
        text = _git(root, "show", f"{revision}:{target_path}")
        try:
            target = parse_target(parse_yaml_mapping(text, label), Path(label))
        except (RecordLoadError, TargetValidationError) as exc:
            raise EvidenceError(f"target at {revision[:12]} does not load strictly: {exc}") from exc
        _ENTRY_CACHE[key] = {
            rid: json.dumps(entry.model_dump(mode="json"), sort_keys=True, ensure_ascii=False)
            for members in target.families().values() for rid, entry in members.items()
        }
    return _ENTRY_CACHE[key]


_ENTRY_CACHE: dict[tuple[str, str, str], dict[str, str]] = {}


def _reachable(root: Path, commit: str) -> bool:
    """Whether `commit` is an ancestor of HEAD. A commit this clone lacks is not;
    any other git failure is an error."""
    proc = subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=root,
                          capture_output=True, text=True, check=False)
    if proc.returncode in (0, 1):
        return proc.returncode == 0
    if subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=root,
                      capture_output=True, check=False).returncode != 0:
        return False
    raise EvidenceError(f"git merge-base --is-ancestor {commit} HEAD failed: {proc.stderr.strip()}")


def _unreachable(commit: str) -> tuple[Freshness, str]:
    return "UNREACHABLE", f"subject commit {commit[:8]} is not reachable from HEAD (squash-merged or deleted branch?)"


def _check_control(root: Path, obs: ObservationRecord) -> str:
    """The revision a negative control's freshness is computed from, after checking its commits.

    Call only once `control.base_revision` is known to be reachable from HEAD.
    """
    assert obs.control is not None and obs.subject_revision is not None
    base, mutated = obs.control.base_revision, obs.subject_revision
    _git(root, "cat-file", "-e", f"{mutated}^{{commit}}")
    if not _git(root, "for-each-ref", "--contains", base, "--format=%(refname)", "refs/heads", "refs/remotes").strip():
        raise EvidenceError(
            f"{obs.observation_id}: control.base_revision {base[:12]} is on no branch; a negative control "
            "must be derived from a commit on a real branch"
        )
    if subprocess.run(["git", "merge-base", "--is-ancestor", base, mutated], cwd=root,
                      capture_output=True, check=False).returncode != 0:
        raise EvidenceError(
            f"{obs.observation_id}: control.base_revision {base[:12]} is not an ancestor of the mutated "
            f"subject_revision {mutated[:12]}"
        )
    return base


def freshness(root: Path, obs: ObservationRecord, target_path: str = ".aes/target.yaml") -> tuple[Freshness, str]:
    """CURRENT, STALE, UNKNOWN or UNREACHABLE, with the reason; see the module docstring."""
    if obs.subject_revision is None or not (obs.dependency_paths or obs.dependency_target_refs):
        return "UNKNOWN", "no subject_revision or no dependency_paths"
    anchor = obs.control.base_revision if obs.control is not None else obs.subject_revision
    if not _reachable(root, anchor):
        return _unreachable(anchor)
    if obs.control is not None:
        since = _check_control(root, obs)
        prefix = f"negative control of {since[:12]}: "
    else:
        since = obs.subject_revision
        prefix = ""
    reasons = []
    if obs.dependency_paths:
        changed = [
            p for p in _git(root, "diff", "--name-only", since, "HEAD", "--", *obs.dependency_paths)
            .splitlines() if p
        ]
        if changed:
            reasons.append("changed since observed: " + ", ".join(changed))
    if obs.dependency_target_refs:
        head = _git(root, "rev-parse", "HEAD").strip()
        then, now = _target_entries_at(root, since, target_path), _target_entries_at(root, head, target_path)
        absent = [r for r in obs.dependency_target_refs if r not in then]
        if absent:
            raise EvidenceError(
                f"{obs.observation_id}: dependency_target_refs {absent} are not declared in {target_path} "
                f"at the observed revision {since[:12]}"
            )
        removed = [r for r in obs.dependency_target_refs if r not in now]
        edited = [r for r in obs.dependency_target_refs if r in now and now[r] != then[r]]
        if edited:
            reasons.append("target entries changed since observed: " + ", ".join(edited))
        if removed:
            reasons.append("target entries removed since observed: " + ", ".join(removed))
    if reasons:
        return "STALE", prefix + "; ".join(reasons)
    what = "dependency" if not obs.dependency_target_refs else "dependency or target entry"
    return "CURRENT", f"{prefix}no {what} changed since {since[:12]}"


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
    superseded: tuple[tuple[str, str], ...] = ()  # (observation_id, superseded_by); never counted

    def counts(self) -> str:
        """`N current, N stale, N unknown, N unreachable; N superseded`: freshness over the
        observations that count, superseded ones apart."""
        gone = {oid for oid, _ in self.superseded}
        live = [f for oid, f, _ in self.observations if oid not in gone]
        return (", ".join(f"{live.count(f)} {f.lower()}" for f in ("CURRENT", "STALE", "UNKNOWN", "UNREACHABLE"))
                + f"; {len(gone)} superseded")


def assess(root: Path) -> EvidenceReport:
    from .trace_review import check_source_review
    root = Path(root).resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / project.materialization.target_path)
    observations = load_observations(root, project.materialization.observations_root, target)

    target_path = project.materialization.target_path
    fresh = {o.observation_id: freshness(root, o, target_path) for o in observations}
    by_er: dict[str, list[tuple[ObservationRecord, ErAssessment]]] = {}
    for o in observations:
        for a in o.assessments:
            by_er.setdefault(a.evidence_requirement_ref, []).append((o, a))

    criteria = []
    for sc in target.success_criteria:
        statuses = []
        for er in sc.evidence_requirements:
            entries = by_er.get(er.id, [])
            current = [(o, a) for o, a in entries
                       if fresh[o.observation_id][0] == "CURRENT" and o.superseded_by is None]
            refuting = [o.observation_id for o, a in current if a.assessment == "REFUTES"]
            blocked_reviews = []
            supporting = []
            for o, a in current:
                if a.assessment != "SUPPORTS":
                    continue
                if er.kind == "trace_review":
                    reviewed = check_source_review(root, o, sc.id)
                    if reviewed.status != "complete" or reviewed.run_outcome != "pass":
                        blocked_reviews.append(f"{o.observation_id}: {reviewed.reason}")
                        continue
                supporting.append(o.observation_id)
            if refuting:
                statuses.append(ErStatus(er.id, "REFUTED", "refuted by " + ", ".join(refuting)))
            elif supporting:
                statuses.append(ErStatus(er.id, "SUPPORTED", "supported by " + ", ".join(supporting)))
            elif entries:
                why = "; ".join(
                    f"{o.observation_id} {a.assessment} ({fresh[o.observation_id][0]}"
                    + (f", superseded by {o.superseded_by})" if o.superseded_by else ")")
                    for o, a in entries
                )
                if blocked_reviews:
                    why += "; " + "; ".join(blocked_reviews)
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
        superseded=tuple((o.observation_id, o.superseded_by) for o in observations if o.superseded_by),
    )


def render_report(report: EvidenceReport) -> str:
    counts = {s: sum(c.standing == s for c in report.criteria) for s in ("SUPPORTED", "INSUFFICIENT", "REFUTED")}
    lines = [
        f"evidence: {len(report.criteria)} criteria: {counts['SUPPORTED']} supported, "
        f"{counts['INSUFFICIENT']} insufficient, {counts['REFUTED']} refuted; "
        f"{len(report.observations)} observation(s): {report.counts()}"
    ]
    for c in report.criteria:
        lines.append(f"  {c.criterion_id}: {c.standing}")
        for s in c.requirements:
            lines.append(f"    {s.er_id}: {s.status} - {s.detail}")
    lines.append("  observations:")
    replaced = dict(report.superseded)
    for oid, f, why in report.observations:
        by = f" (superseded by {replaced[oid]})" if oid in replaced else ""
        lines.append(f"    {oid}: {f}{by} - {why}")
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
    branch_note: str | None  # squash-merge warning or unchecked note; see `branch_note`


def branch_note(root: Path, revision: str, consequence: str = "this evidence stays valid") -> str | None:
    """A warning when `revision` is not yet on the default branch, a note when that
    cannot be checked, None when it is already there.

    The default branch tip is `origin/HEAD`, else `origin/main`. Evidence recorded
    on a branch stays valid only if that exact commit reaches the default branch:
    a squash merge rewrites it and leaves the observation UNREACHABLE. `aes plan
    accept` prints the same warning for a plan's `accepted_at_revision`, with
    `consequence` naming the plan instead of the evidence.
    """
    tip = next((ref for ref in ("refs/remotes/origin/HEAD", "refs/remotes/origin/main")
                if subprocess.run(["git", "rev-parse", "--verify", "-q", ref], cwd=root,
                                  capture_output=True, check=False).returncode == 0), None)
    if tip is None:
        return ("note: no origin/HEAD or origin/main here, so whether the recorded commit is on the "
                "default branch was not checked")
    proc = subprocess.run(["git", "merge-base", "--is-ancestor", revision, tip], cwd=root,
                          capture_output=True, text=True, check=False)
    if proc.returncode == 0:
        return None
    if proc.returncode != 1:
        raise EvidenceError(f"git merge-base --is-ancestor {revision} {tip} failed: {proc.stderr.strip()}")
    name = _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    where = "a detached HEAD" if name == "HEAD" else f"branch {name}"
    return (f"warning: recorded at {revision[:8]} on {where}; {consequence} only if that commit "
            "reaches the default branch unchanged — merge with a merge commit (not squash), or re-record "
            "after merging")


def _aes_version() -> str:
    """The running AES code's version (`characterize.running_version`); fails if undeterminable."""
    from .characterize import CharacterizeError, running_version

    try:
        return running_version()
    except CharacterizeError as exc:
        raise EvidenceError(str(exc)) from exc


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
    apart. Target dependencies are entry-level (`dependency_target_refs`): the
    verification subject, the evidence requirements it assesses, and every
    planned artifact whose path is among the dependency paths; the target file
    itself is not a dependency path, so an unrelated target edit does not stale it.

    Exit 0 assesses every evidence requirement the subject proves as SUPPORTS
    (INCONCLUSIVE with `downgrade_basis`, for a test that covers only part of a
    requirement); any other exit assesses them as REFUTES. Refuses when a
    dependency has uncommitted changes, because the observation must name the
    commit that holds exactly what was run. Recording on a branch is normal and
    is not refused; `Recorded.branch_note` carries the squash-merge warning.
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
    target_path = project.materialization.target_path
    dirty = [p for p in _git(root, "status", "--porcelain", "--", *deps, target_path).splitlines() if p]
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
    by_path = {a.locator.exact_path: a.id for a in target.planned_artifacts}
    target_refs = [subject_id, *vs.evidence_requirement_refs, *sorted({by_path[d] for d in deps if d in by_path})]

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
        "dependency_target_refs": target_refs,
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
    return Recorded(path, observation, branch_note(root, revision))
