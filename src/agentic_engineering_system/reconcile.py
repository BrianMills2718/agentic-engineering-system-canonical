"""Qualified current state and target/current gaps (`RU-AES-RECONCILE`,
`SC-GF-007`, `SC-GF-008` at the gap level).

`reconcile(root)` composes three existing derivations and adds no rule of its own
about what is true:
- characterization and drift (`characterize.characterize` + `characterize.drift`,
  whose orphan and unrealized findings come from `topology.compare_topology` over
  the files of HEAD): which planned artifacts exist, which drifted, which files
  are orphans;
- evidence standing (`evidence.assess`): per criterion SUPPORTED | INSUFFICIENT |
  REFUTED under decision D2, per evidence requirement its status, per observation
  its freshness (UNREACHABLE when its commit is not an ancestor of HEAD) and
  whether it is superseded;
- the target's own refs: which verification subjects route to an evidence
  requirement, and which artifacts and criteria concern each component;
- the accepted plans under the project's `plans_root`: each plan's
  `accepted_at_revision` is checked with `git merge-base --is-ancestor` against
  HEAD. An unreachable plan (accepted on a branch that was then squash-merged or
  deleted) is reported as a warning line, not a failure: the target already
  carries its delta, and only the plan's provenance commit is lost.

Everything is recomputed on every call and nothing is written: a gap closes only
through a new observation, a repository change, or a target change, never
through reconcile's own state.

Binding: `subject_revision` is HEAD, as for characterization. `dirty` is true
when a governed file or anything under `.aes/` (the target and the observations
this reconciliation read from disk) differs from HEAD, untracked files included.

Artifact status:
- DRIFTED: `drift` reports a failing finding for it (missing committed export,
  changed committed signature, or a missing file with committed exports);
- UNREALIZED: no file at its exact path at HEAD. Under a governed root this is
  `compare_topology`'s unrealized finding; outside one, the only fact is presence
  at HEAD (the file is not characterized), and `note` says so;
- REALIZED otherwise.

A component's gaps are its owned artifacts that are DRIFTED or UNREALIZED and the
criteria that concern it and are not SUPPORTED. A criterion concerns a component
when the component's `target_refs` name it or share a ref with its `target_refs`,
or when an artifact the component owns names it in `semantic_justification_refs`.
Orphans have no planned artifact, so no component; they are project-level, as are
gaps of artifacts no component owns and of criteria that concern no component.

`ok` is false on any REFUTED criterion, orphan or drift. INSUFFICIENT is the
normal state of work in progress and does not make it false.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Final, Literal

from pydantic import computed_field

from .characterize import Producer, _git, characterize, drift
from .evidence import Freshness, Standing, _reachable, assess
from .records import StrictModel, TargetRecord, load_project, load_target
from .running import check_running, inventory_path, load_inventory

RECONCILIATION_SCHEMA: Final = "aes.v0_2.reconciliation.probe0"

ArtifactStatus = Literal["REALIZED", "UNREALIZED", "DRIFTED"]
GapKind = Literal["drifted", "refuted", "unrealized", "insufficient", "orphan"]
_GAP_ORDER: tuple[GapKind, ...] = ("drifted", "refuted", "orphan", "unrealized", "insufficient")


class DriftFinding(StrictModel):
    kind: str
    detail: str


class ArtifactState(StrictModel):
    artifact_id: str
    path: str
    status: ArtifactStatus
    drift: list[DriftFinding]
    note: str | None = None


class MissingRequirement(StrictModel):
    """An evidence requirement without current support, and whether anything could supply it."""

    er_id: str
    status: Literal["REFUTED", "NO_CURRENT_SUPPORT"]
    detail: str
    verification_subject_refs: list[str]
    external_boundary: str | None = None  # the target's external_boundaries entry for it, if any
    has_route: bool  # false: no verification subject names it and no external boundary lists it
    # (SC-GF-004 "no route"; the same rule as planning.unrouted_requirements)


class CriterionState(StrictModel):
    criterion_id: str
    standing: Standing
    missing: list[MissingRequirement]


class ObservationState(StrictModel):
    observation_id: str
    freshness: Freshness
    detail: str
    superseded_by: str | None = None  # replaced by that observation; never counts, counted apart


class PlanState(StrictModel):
    plan_id: str
    accepted_at_revision: str
    reachable: bool  # accepted_at_revision is an ancestor of HEAD


class Gap(StrictModel):
    kind: GapKind
    ref: str
    detail: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> str:
        """`<kind>:<ref>`, the handle a plan proposal names in `closes_gaps`.

        The kind is part of it so a proposal written against an insufficient
        criterion no longer matches once that criterion is refuted.
        """
        return f"{self.kind}:{self.ref}"


class ComponentState(StrictModel):
    component_id: str
    gaps: list[Gap]


class RunningState(StrictModel):
    """What runs against the declared running pieces (hive hardening U4); see `running.py`."""

    snapshot: str
    collected_at: str | None
    in_scope: int
    undeclared: list[str]
    not_running: list[str]
    unreadable: list[str]


class Reconciliation(StrictModel):
    schema_version: Literal["aes.v0_2.reconciliation.probe0"]
    subject_revision: str
    dirty: bool
    producer: Producer
    target_id: str
    artifacts: list[ArtifactState]
    criteria: list[CriterionState]
    observations: list[ObservationState]
    plans: list[PlanState]
    orphans: list[str]
    components: list[ComponentState]
    unassigned_gaps: list[Gap]
    produced_at: datetime
    running: RunningState | None = None

    @property
    def failures(self) -> list[str]:
        return (
            [f"refuted: {c.criterion_id}" for c in self.criteria if c.standing == "REFUTED"]
            + [f"orphan: {p}" for p in self.orphans]
            + [f"drifted: {a.artifact_id}" for a in self.artifacts if a.status == "DRIFTED"]
            + [f"undeclared running: {u}" for u in (self.running.undeclared if self.running else [])]
        )

    @property
    def ok(self) -> bool:
        return not self.failures

    def open_gaps(self) -> list[Gap]:
        """Every open gap once, in report order (a criterion gap can appear under several components)."""
        seen: dict[str, Gap] = {}
        for g in [g for comp in self.components for g in comp.gaps] + self.unassigned_gaps:
            seen.setdefault(g.id, g)
        return list(seen.values())


def _present_at_head(root: Path, paths: list[str]) -> set[str]:
    if not paths:
        return set()
    out = _git(root, "ls-tree", "-r", "--name-only", "-z", "HEAD", "--", *paths).decode()
    return {p for p in out.split("\0") if p}


def _artifact_states(root: Path, target: TargetRecord, governed: tuple[str, ...], found) -> list[ArtifactState]:
    unrealized = {d.artifact_id for d in found if d.kind == "unrealized"}
    failing: dict[str, list[DriftFinding]] = {}
    for d in found:
        if d.failing and d.artifact_id is not None:
            failing.setdefault(d.artifact_id, []).append(DriftFinding(kind=d.kind, detail=d.detail))
    outside = [a.locator.exact_path for a in target.planned_artifacts
               if not any(a.locator.exact_path.startswith(r) for r in governed)]
    present_outside = _present_at_head(root, outside)

    states = []
    for a in target.planned_artifacts:
        path = a.locator.exact_path
        note = None
        if a.id in failing:
            status: ArtifactStatus = "DRIFTED"
        elif path in outside:
            note = "outside the governed roots: presence at HEAD only, not characterized"
            status = "REALIZED" if path in present_outside else "UNREALIZED"
        else:
            status = "UNREALIZED" if a.id in unrealized else "REALIZED"
        states.append(ArtifactState(artifact_id=a.id, path=path, status=status,
                                    drift=failing.get(a.id, []), note=note))
    return states


def _criterion_states(target: TargetRecord, report) -> list[CriterionState]:
    routes: dict[str, list[str]] = {}
    for v in target.verification_subjects:
        for er in v.evidence_requirement_refs:
            routes.setdefault(er, []).append(v.id)
    boundaries = {b.evidence_requirement_ref: " ".join(b.boundary.split()) for b in target.external_boundaries}
    return [
        CriterionState(
            criterion_id=c.criterion_id,
            standing=c.standing,
            missing=[
                MissingRequirement(er_id=s.er_id, status=s.status, detail=s.detail,
                                   verification_subject_refs=routes.get(s.er_id, []),
                                   external_boundary=boundaries.get(s.er_id),
                                   has_route=s.er_id in routes or s.er_id in boundaries)
                for s in c.requirements if s.status != "SUPPORTED"
            ],
        )
        for c in report.criteria
    ]


def _plan_states(root: Path, plans_root: str) -> list[PlanState]:
    from .planning import load_plan  # planning imports this module, so not at module level

    plans_dir = root / plans_root
    if not plans_dir.is_dir():
        return []
    states = []
    for path in sorted(plans_dir.glob("*.yaml")):
        plan = load_plan(path)
        states.append(PlanState(plan_id=plan.proposal_id, accepted_at_revision=plan.accepted_at_revision,
                                reachable=_reachable(root, plan.accepted_at_revision)))
    return states


def _artifact_gap(a: ArtifactState) -> Gap | None:
    if a.status == "DRIFTED":
        return Gap(kind="drifted", ref=a.artifact_id,
                   detail=f"{a.path}: " + "; ".join(f"{d.kind} {d.detail}" for d in a.drift))
    if a.status == "UNREALIZED":
        return Gap(kind="unrealized", ref=a.artifact_id, detail=f"{a.path}: planned, no file at HEAD")
    return None


def _criterion_gap(c: CriterionState) -> Gap | None:
    if c.standing == "SUPPORTED":
        return None
    parts = [f"{m.er_id} {m.status}{'' if m.has_route else ' (no route)'}" for m in c.missing]
    return Gap(kind="refuted" if c.standing == "REFUTED" else "insufficient",
               ref=c.criterion_id, detail="; ".join(parts))


def _ordered(gaps: list[Gap]) -> list[Gap]:
    return sorted(gaps, key=lambda g: _GAP_ORDER.index(g.kind))  # stable: target order within a kind


def reconcile(root: Path) -> Reconciliation:
    root = Path(root).resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / project.materialization.target_path)
    c = characterize(root)
    found = drift(target, c)
    evidence = assess(root)

    artifacts = _artifact_states(root, target, tuple(c.governed_roots), found)
    criteria = _criterion_states(target, evidence)
    orphans = [d.path for d in found if d.kind == "orphan"]
    artifact_gaps = {a.artifact_id: g for a in artifacts if (g := _artifact_gap(a))}
    criterion_gaps = {s.criterion_id: g for s in criteria if (g := _criterion_gap(s))}

    owned: set[str] = set()
    concerned: set[str] = set()
    components = []
    for comp in target.components:
        owned.update(comp.planned_artifact_refs)
        refs = set(comp.target_refs)
        justified = {r for a in target.planned_artifacts if a.id in comp.planned_artifact_refs
                     for r in a.semantic_justification_refs}
        sc_ids = [sc.id for sc in target.success_criteria
                  if sc.id in refs or sc.id in justified or refs & set(sc.target_refs)]
        concerned.update(sc_ids)
        gaps = [artifact_gaps[a] for a in comp.planned_artifact_refs if a in artifact_gaps]
        gaps += [criterion_gaps[s] for s in sc_ids if s in criterion_gaps]
        components.append(ComponentState(component_id=comp.id, gaps=_ordered(gaps)))

    unassigned = [Gap(kind="orphan", ref=p, detail="no planned artifact has this exact_path") for p in orphans]
    unassigned += [g for aid, g in artifact_gaps.items() if aid not in owned]
    unassigned += [g for sid, g in criterion_gaps.items() if sid not in concerned]

    aes_dirty = bool(_git(root, "status", "--porcelain", "--untracked-files=all", "--", ".aes",
                          ":(exclude).aes/running-inventory.json").strip())
    running = None
    snapshot = inventory_path(root)
    inventory = load_inventory(snapshot) if target.running_scopes else None
    if inventory is not None:
        rr = check_running(target, inventory)
        running = RunningState(snapshot=str(snapshot), collected_at=rr.collected_at, in_scope=rr.in_scope,
                               undeclared=rr.undeclared, not_running=rr.not_running, unreadable=rr.unreadable)
    return Reconciliation(
        schema_version=RECONCILIATION_SCHEMA,
        subject_revision=c.subject_revision,
        dirty=c.dirty or aes_dirty,
        producer=c.producer,
        target_id=target.target_id,
        artifacts=artifacts,
        criteria=criteria,
        observations=[ObservationState(observation_id=o, freshness=f, detail=why,
                                       superseded_by=dict(evidence.superseded).get(o))
                      for o, f, why in evidence.observations],
        plans=_plan_states(root, project.materialization.plans_root),
        orphans=orphans,
        components=components,
        unassigned_gaps=_ordered(unassigned),
        produced_at=datetime.now(UTC).replace(microsecond=0),
        running=running,
    )


# --------------------------------------------------------------------------- #
# Rendering (deterministic for one revision: no produced_at)
# --------------------------------------------------------------------------- #

INSUFFICIENT_NOTE = (
    "INSUFFICIENT criteria are normal while work is in progress and do not fail this command; "
    "a REFUTED criterion, an orphan or drift does."
)


def _counts(r: Reconciliation) -> list[str]:
    def n(items, attr, value):
        return sum(getattr(i, attr) == value for i in items)

    no_route = sum(not m.has_route for c in r.criteria for m in c.missing)
    live = [o for o in r.observations if o.superseded_by is None]
    return [
        f"  artifacts: {n(r.artifacts, 'status', 'REALIZED')} realized, "
        f"{n(r.artifacts, 'status', 'UNREALIZED')} unrealized, {n(r.artifacts, 'status', 'DRIFTED')} drifted; "
        f"{len(r.orphans)} orphan(s)",
        f"  criteria: {n(r.criteria, 'standing', 'SUPPORTED')} supported, "
        f"{n(r.criteria, 'standing', 'INSUFFICIENT')} insufficient, {n(r.criteria, 'standing', 'REFUTED')} refuted; "
        f"{no_route} unsupported evidence requirement(s) with no route",
        f"  observations: {n(live, 'freshness', 'CURRENT')} current, {n(live, 'freshness', 'STALE')} stale, "
        f"{n(live, 'freshness', 'UNKNOWN')} unknown, {n(live, 'freshness', 'UNREACHABLE')} unreachable; "
        f"{len(r.observations) - len(live)} superseded",
        f"  plans: {len(r.plans)} accepted, {sum(not p.reachable for p in r.plans)} unreachable",
    ] + ([f"  running: {r.running.in_scope} in scope, {len(r.running.undeclared)} undeclared, "
          f"{len(r.running.not_running)} declared but not running (snapshot {r.running.collected_at})"]
         + [f"    undeclared: {u}" for u in r.running.undeclared]
         + [f"    unreadable: {u}" for u in r.running.unreadable] if r.running else [])


def _plan_warnings(r: Reconciliation) -> list[str]:
    return [f"  warning: plan {p.plan_id} accepted_at_revision {p.accepted_at_revision[:8]} is not reachable "
            "from HEAD (squash-merged or deleted branch?); the target already carries its delta, so this "
            "does not fail" for p in r.plans if not p.reachable]


def _header(r: Reconciliation, word: str) -> str:
    dirty = " (dirty: working tree differs from HEAD under governed roots or .aes/)" if r.dirty else ""
    return f"{'OK' if r.ok else 'FAIL'} {word}: {r.target_id} at {r.subject_revision}{dirty}"


def _gap_line(g: Gap) -> str:
    return f"{g.kind} {g.ref} - {g.detail}"


def render_status(r: Reconciliation) -> str:
    """One screen: revision, counts, the first open gap per component."""
    lines = [_header(r, "status"), *_counts(r), "  first open gap per component:"]
    for comp in r.components:
        more = f" (+{len(comp.gaps) - 1} more)" if len(comp.gaps) > 1 else ""
        lines.append(f"    {comp.component_id}: " + (_gap_line(comp.gaps[0]) + more if comp.gaps else "no open gap"))
    if r.unassigned_gaps:
        more = f" (+{len(r.unassigned_gaps) - 1} more)" if len(r.unassigned_gaps) > 1 else ""
        lines.append(f"    (no component): {_gap_line(r.unassigned_gaps[0])}{more}")
    lines += _plan_warnings(r)
    lines += [f"  {f}" for f in r.failures]
    lines.append(f"  {INSUFFICIENT_NOTE}")
    return "\n".join(lines)


def render_report(r: Reconciliation) -> str:
    """Full report: every artifact, criterion, observation and gap."""
    lines = [_header(r, "reconcile"), f"  producer: {r.producer.identity} {r.producer.version}", *_counts(r)]
    lines.append("  artifacts:")
    for a in r.artifacts:
        extra = "".join(f"; {d.kind} {d.detail}" for d in a.drift) + (f" ({a.note})" if a.note else "")
        lines.append(f"    {a.artifact_id}: {a.status} {a.path}{extra}")
    lines.append("  criteria:")
    for c in r.criteria:
        lines.append(f"    {c.criterion_id}: {c.standing}")
        for m in c.missing:
            routes = [*m.verification_subject_refs]
            if m.external_boundary is not None:
                routes.append(f"external boundary ({m.external_boundary})")
            route = ", ".join(routes) if m.has_route else "NO ROUTE (no verification subject or external boundary)"
            lines.append(f"      {m.er_id}: {m.status} - {m.detail}; route: {route}")
    lines.append("  observations:")
    lines += [f"    {o.observation_id}: {o.freshness}"
              + (f" (superseded by {o.superseded_by})" if o.superseded_by else "") + f" - {o.detail}"
              for o in r.observations]
    lines.append("  plans:" + ("" if r.plans else " none"))
    lines += [f"    {p.plan_id}: accepted at {p.accepted_at_revision[:12]}, "
              + ("reachable" if p.reachable else "UNREACHABLE from HEAD") for p in r.plans]
    lines.append("  orphans:" + ("" if r.orphans else " none"))
    lines += [f"    {p}" for p in r.orphans]
    lines.append("  gaps by component:")
    for comp in r.components:
        lines.append(f"    {comp.component_id}:" + ("" if comp.gaps else " no open gap"))
        lines += [f"      {_gap_line(g)}" for g in comp.gaps]
    lines.append("    (no component):" + ("" if r.unassigned_gaps else " no open gap"))
    lines += [f"      {_gap_line(g)}" for g in r.unassigned_gaps]
    lines += _plan_warnings(r)
    lines += [f"  {f}" for f in r.failures]
    lines.append(f"  {INSUFFICIENT_NOTE}")
    return "\n".join(lines)
