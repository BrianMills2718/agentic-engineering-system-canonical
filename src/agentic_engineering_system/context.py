"""Bounded working-context compiler (probe 0): `aes context <subject>`.

Compiles the smallest complete packet for one declared subject ID. Every
included normative item, criterion and evidence requirement carries its FULL
text; nothing is referenced by ID alone. Everything deliberately left out is
listed under `not_included` so omission is visible rather than silent.

Inclusion rules (typed-ref closure, no free-text heuristics):

component  -> its planned artifacts; normative items and criteria named by its
              target_refs and by those artifacts' semantic_justification_refs;
              criteria whose target_refs name an included normative item; the
              outcomes those items/criteria/artifacts reach; verification
              subjects pointing at included criteria.
artifact   -> the artifact; components that plan it; items/criteria named by its
              semantic_justification_refs; criteria targeting those items;
              outcomes reached; verification subjects for included criteria or
              whose locator is the artifact's exact path.
criterion  -> the criterion; items/outcomes in its target_refs; artifacts
              justified by it; components planning those artifacts;
              verification subjects pointing at it.
normative  -> the item; its outcomes; criteria targeting it; artifacts justified
              by it; components targeting it or planning those artifacts;
              verification subjects for the included criteria.
outcome    -> the outcome; items reaching it; criteria/artifacts/components
              naming it directly; verification subjects for included criteria.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from .records import (
    Component,
    NormativeItem,
    Outcome,
    PlannedArtifact,
    ProjectRecord,
    SuccessCriterion,
    TargetRecord,
    VerificationSubject,
    load_project,
    load_target,
)

TOPOLOGY_RULE = (
    "Any durable file under a governed root that is not the exact_path of a "
    "planned artifact in target.yaml is a topology violation. Add the artifact "
    "to the target (with a semantic justification) before creating the file."
)


class ContextError(ValueError):
    """The context could not be compiled; the message names the exact cause."""


class Provenance(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_root: str
    project_path: str
    target_path: str
    target_sha256: str
    git_head: str


class WorkingContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_id: str
    subject_family: str
    subject: dict[str, Any]  # the subject record in full
    outcomes: list[Outcome]
    normative_items: list[NormativeItem]
    success_criteria: list[SuccessCriterion]
    components: list[Component]
    planned_artifacts: list[PlannedArtifact]
    verification_subjects: list[VerificationSubject]
    governed_roots: list[str]
    topology_rule: str
    not_included: dict[str, list[str]]  # family -> IDs deliberately omitted
    provenance: Provenance


# --------------------------------------------------------------------------- #
# Provenance
# --------------------------------------------------------------------------- #


def _git_head(project_root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ContextError(f"{project_root}: git executable not found; cannot record HEAD") from exc
    if proc.returncode != 0:
        raise ContextError(
            f"{project_root}: `git rev-parse HEAD` failed (exit {proc.returncode}): "
            f"{proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- #
# Compilation
# --------------------------------------------------------------------------- #


def _closure(target: TargetRecord, subject_family: str, subject_id: str) -> dict[str, set[str]]:
    fam = target.families()
    outcomes = fam["outcomes"]
    items = fam["normative_items"]
    criteria = fam["success_criteria"]
    components = fam["components"]
    artifacts = fam["planned_artifacts"]
    subjects = fam["verification_subjects"]

    inc: dict[str, set[str]] = {
        "outcomes": set(),
        "normative_items": set(),
        "success_criteria": set(),
        "components": set(),
        "planned_artifacts": set(),
        "verification_subjects": set(),
    }

    def add_semantic(ref: str) -> None:
        """A target_ref / justification ref names an outcome, item or criterion."""
        if ref in outcomes:
            inc["outcomes"].add(ref)
        elif ref in items:
            inc["normative_items"].add(ref)
        elif ref in criteria:
            inc["success_criteria"].add(ref)
        else:  # load_target already rejected this; keep the invariant loud
            raise ContextError(f"ref '{ref}' is not an outcome, normative item or criterion")

    def criteria_targeting_included_items() -> None:
        for sc in criteria.values():
            if any(r in inc["normative_items"] for r in sc.target_refs):
                inc["success_criteria"].add(sc.id)

    def criteria_targeting(ref: str) -> None:
        for sc in criteria.values():
            if ref in sc.target_refs:
                inc["success_criteria"].add(sc.id)

    def artifacts_justified_by(ref: str) -> None:
        for art in artifacts.values():
            if ref in art.semantic_justification_refs:
                inc["planned_artifacts"].add(art.id)

    def components_planning_included_artifacts() -> None:
        for cmp in components.values():
            if any(a in inc["planned_artifacts"] for a in cmp.planned_artifact_refs):
                inc["components"].add(cmp.id)

    if subject_family == "components":
        cmp = components[subject_id]
        inc["components"].add(cmp.id)
        for a in cmp.planned_artifact_refs:
            inc["planned_artifacts"].add(a)
        for r in cmp.target_refs:
            add_semantic(r)
        for a in cmp.planned_artifact_refs:
            for r in artifacts[a].semantic_justification_refs:
                add_semantic(r)
        criteria_targeting_included_items()

    elif subject_family == "planned_artifacts":
        art = artifacts[subject_id]
        inc["planned_artifacts"].add(art.id)
        components_planning_included_artifacts()
        for r in art.semantic_justification_refs:
            add_semantic(r)
        criteria_targeting_included_items()
        for vs in subjects.values():
            if vs.locator == art.locator.exact_path:
                inc["verification_subjects"].add(vs.id)

    elif subject_family == "success_criteria":
        sc = criteria[subject_id]
        inc["success_criteria"].add(sc.id)
        for r in sc.target_refs:
            add_semantic(r)
        artifacts_justified_by(sc.id)
        components_planning_included_artifacts()

    elif subject_family == "normative_items":
        ni = items[subject_id]
        inc["normative_items"].add(ni.id)
        criteria_targeting(ni.id)
        artifacts_justified_by(ni.id)
        for cmp in components.values():
            if ni.id in cmp.target_refs:
                inc["components"].add(cmp.id)
        components_planning_included_artifacts()

    elif subject_family == "outcomes":
        out = outcomes[subject_id]
        inc["outcomes"].add(out.id)
        for ni in items.values():
            if out.id in ni.outcome_refs:
                inc["normative_items"].add(ni.id)
        criteria_targeting(out.id)
        artifacts_justified_by(out.id)
        for cmp in components.values():
            if out.id in cmp.target_refs:
                inc["components"].add(cmp.id)

    else:
        raise ContextError(
            f"subject '{subject_id}' is a {subject_family} record; context is compiled only for "
            "components, planned_artifacts, success_criteria, normative_items and outcomes"
        )

    # Outcomes reached by every included item; verification subjects for every
    # included criterion. Applied uniformly so the outcome text is always present.
    for ni_id in inc["normative_items"]:
        inc["outcomes"].update(items[ni_id].outcome_refs)
    for sc_id in inc["success_criteria"]:
        for r in criteria[sc_id].target_refs:
            if r in outcomes:
                inc["outcomes"].add(r)
    for vs in subjects.values():
        if any(r in inc["success_criteria"] for r in vs.criterion_refs):
            inc["verification_subjects"].add(vs.id)

    return inc


def compile_context(
    project: ProjectRecord,
    target: TargetRecord,
    subject: str,
    provenance: Provenance,
) -> WorkingContext:
    family = target.kind_of(subject)
    if family is None:
        raise ContextError(
            f"subject '{subject}' is not a declared ID in {provenance.target_path}"
        )
    fam = target.families()
    inc = _closure(target, family, subject)

    def ordered(family_name: str) -> list[Any]:
        # preserve target.yaml declaration order
        return [rec for rid, rec in fam[family_name].items() if rid in inc[family_name]]

    not_included: dict[str, list[str]] = {}
    for family_name, members in fam.items():
        if family_name == "evidence_requirements":
            continue  # ERs travel inside their criterion; never listed separately
        omitted = [rid for rid in members if rid not in inc[family_name]]
        if omitted:
            not_included[family_name] = omitted

    return WorkingContext(
        subject_id=subject,
        subject_family=family,
        subject=fam[family][subject].model_dump(mode="json"),
        outcomes=ordered("outcomes"),
        normative_items=ordered("normative_items"),
        success_criteria=ordered("success_criteria"),
        components=ordered("components"),
        planned_artifacts=ordered("planned_artifacts"),
        verification_subjects=ordered("verification_subjects"),
        governed_roots=list(project.governed_roots),
        topology_rule=TOPOLOGY_RULE,
        not_included=not_included,
        provenance=provenance,
    )


def project_context(project_root: Path, subject: str) -> WorkingContext:
    """Load `.aes/project.yaml` + its target under `project_root` and compile the packet."""
    project_root = Path(project_root).resolve()
    project_path = project_root / ".aes" / "project.yaml"
    project = load_project(project_path)
    target_path = (project_root / project.materialization.target_path).resolve()
    target = load_target(target_path)
    provenance = Provenance(
        project_root=str(project_root),
        project_path=str(project_path),
        target_path=str(target_path),
        target_sha256=_sha256(target_path),
        git_head=_git_head(project_root),
    )
    return compile_context(project, target, subject, provenance)


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #


def render_json(ctx: WorkingContext) -> str:
    return json.dumps(ctx.model_dump(mode="json"), indent=2, sort_keys=False)


def _para(text: str) -> str:
    return " ".join(text.split())


def render_markdown(ctx: WorkingContext) -> str:
    L: list[str] = []
    L.append(f"# Working context: {ctx.subject_id} ({ctx.subject_family})")
    L.append("")
    L.append("## Provenance")
    L.append(f"- project root: `{ctx.provenance.project_root}`")
    L.append(f"- target: `{ctx.provenance.target_path}`")
    L.append(f"- target sha256: `{ctx.provenance.target_sha256}`")
    L.append(f"- git HEAD: `{ctx.provenance.git_head}`")
    L.append("")

    L.append("## Subject")
    L.append("```json")
    L.append(json.dumps(ctx.subject, indent=2))
    L.append("```")
    L.append("")

    L.append("## Outcomes")
    for o in ctx.outcomes:
        L.append(f"### {o.id}")
        L.append(f"- actor or consumer: {o.actor_or_consumer}")
        L.append(f"- statement: {_para(o.statement)}")
        if o.non_goals:
            L.append("- non-goals:")
            for ng in o.non_goals:
                L.append(f"  - {ng}")
        if o.rationale:
            L.append(f"- rationale: {_para(o.rationale)}")
        L.append("")
    if not ctx.outcomes:
        L.append("(none)")
        L.append("")

    L.append("## Normative items (full text)")
    for ni in ctx.normative_items:
        L.append(f"### {ni.id} ({ni.kind}; outcomes: {', '.join(ni.outcome_refs)})")
        L.append(_para(ni.statement))
        L.append("")
    if not ctx.normative_items:
        L.append("(none)")
        L.append("")

    L.append("## Success criteria (full text, disproof, evidence requirements)")
    for sc in ctx.success_criteria:
        L.append(f"### {sc.id} (targets: {', '.join(sc.target_refs)})")
        L.append(f"- statement: {_para(sc.statement)}")
        L.append(f"- disproof: {_para(sc.disproof)}")
        L.append("- evidence requirements:")
        for er in sc.evidence_requirements:
            L.append(f"  - {er.id} ({er.kind}): {_para(er.requirement)}")
        L.append("")
    if not ctx.success_criteria:
        L.append("(none)")
        L.append("")

    L.append("## Components")
    for c in ctx.components:
        L.append(f"### {c.id}")
        L.append(f"- responsibility: {_para(c.responsibility)}")
        L.append(f"- target refs: {', '.join(c.target_refs)}")
        L.append(f"- planned artifacts: {', '.join(c.planned_artifact_refs)}")
        L.append("")
    if not ctx.components:
        L.append("(none)")
        L.append("")

    L.append("## Planned artifacts (exact paths)")
    for a in ctx.planned_artifacts:
        L.append(
            f"- `{a.locator.exact_path}` — {a.id} ({a.kind}): {_para(a.purpose)}; "
            f"justified by {', '.join(a.semantic_justification_refs)}"
        )
    if not ctx.planned_artifacts:
        L.append("(none)")
    L.append("")

    L.append("## Verification subjects")
    for vs in ctx.verification_subjects:
        L.append(
            f"- {vs.id}: locator `{vs.locator}`, proof {vs.proof_kind}/{vs.proof_role}, "
            f"criteria {', '.join(vs.criterion_refs)}, evidence requirements "
            f"{', '.join(vs.evidence_requirement_refs)} — {_para(vs.purpose)}"
        )
    if not ctx.verification_subjects:
        L.append("(none)")
    L.append("")

    L.append("## Governed roots and topology rule")
    for root in ctx.governed_roots:
        L.append(f"- `{root}`")
    L.append("")
    L.append(ctx.topology_rule)
    L.append("")

    L.append("## Not included (deliberately omitted from this packet)")
    if not ctx.not_included:
        L.append("(nothing omitted; the packet is the whole target)")
    for family_name, ids in ctx.not_included.items():
        L.append(f"- {family_name}: {', '.join(ids)}")
    L.append("")
    return "\n".join(L)
