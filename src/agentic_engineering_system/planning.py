"""`aes plan prepare / validate / accept` (`RU-AES-PLANNING`, `SC-GF-004`).

Bounded to the target acceptance transaction of `15-planning-contract.candidate.yaml`
(validate the proposed target delta, accept it; recharacterization and the new
gap set follow from `aes reconcile` on the next commit). No plan is generated here
and no model is called: a human or agent writes the proposal, following
`planning_protocol.md`.

A proposal (`aes.v0_2.proposal.probe0`) is a target delta plus the ids of the
open gaps it claims to close. The delta has an `add:` and a `change:` section,
each with one list per target family. `add` appends new entries; `change`
replaces the whole existing entry with the same key (`id`, or
`evidence_requirement_ref` for external boundaries). There is no `remove` in
this probe.

`validate_proposal` applies the delta to an in-memory copy of the target and
reports every violation, not the first:
- the delta itself: a `change` key the target does not declare, an `add` key it
  already declares, a key given twice in one section, an empty delta;
- the resulting target under `records.validate_target_refs` (ids unique across
  families, every ref resolves, every criterion has an evidence requirement);
- SC-GF-004: every evidence requirement in the resulting target has a route, a
  verification subject naming it in `evidence_requirement_refs` or an entry in
  `external_boundaries`;
- every id in `closes_gaps` is open in the current reconciliation
  (`<kind>:<ref>`, `reconcile.Gap.id`);
- every planned artifact the delta adds or changes lies under a governed root,
  or is not `kind: source` and is listed in `outside_governed_roots` with a
  reason.

`accept_proposal` refuses on a dirty working tree (tracked changes, or anything
untracked under `.aes/`), on any validation violation, and when
`<plans_root>/<proposal_id>.yaml` exists. Otherwise it edits the target through
ruamel round-trip, so comments, key order and scalar styles survive (new entries
appended at the end of their family in the style the proposal wrote them,
changed entries replaced in place), checks that the written text loads to
exactly the validated target, and writes the plan file: the proposal plus
`accepted_at_revision` (HEAD) and `accepted_at` (UTC). It does not commit; the
target and the plan are committed together by whoever accepted.
"""

from __future__ import annotations

import io
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, field_validator
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from .reconcile import reconcile
from .records import (
    Component,
    ExternalBoundary,
    NormativeItem,
    Outcome,
    PlannedArtifact,
    StrictModel,
    SuccessCriterion,
    TargetRecord,
    VerificationSubject,
    _to_plain,
    _validate_model,
    _yaml,
    load_project,
    load_target,
    load_yaml_mapping,
    validate_target_refs,
)

PROPOSAL_SCHEMA = "aes.v0_2.proposal.probe0"
PLAN_INPUT_SCHEMA = "aes.v0_2.plan_input.probe0"
FAMILIES = (
    "outcomes", "normative_items", "success_criteria", "components",
    "planned_artifacts", "verification_subjects", "external_boundaries",
)
_KEY = {f: "id" for f in FAMILIES} | {"external_boundaries": "evidence_requirement_ref"}
_PROPOSAL_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")  # also the plan file name
_HEX40 = re.compile(r"[0-9a-f]{40}")


class PlanError(ValueError):
    """A proposal was refused; `violations` lists every reason. Nothing was written."""

    def __init__(self, subject: str, violations: list[str]) -> None:
        self.violations = violations
        lines = "\n".join(f"  - {v}" for v in violations)
        super().__init__(f"{subject}: {len(violations)} violation(s):\n{lines}")


# --------------------------------------------------------------------------- #
# Records
# --------------------------------------------------------------------------- #


class FamilyEntries(StrictModel):
    outcomes: list[Outcome] = Field(default_factory=list)
    normative_items: list[NormativeItem] = Field(default_factory=list)
    success_criteria: list[SuccessCriterion] = Field(default_factory=list)
    components: list[Component] = Field(default_factory=list)
    planned_artifacts: list[PlannedArtifact] = Field(default_factory=list)
    verification_subjects: list[VerificationSubject] = Field(default_factory=list)
    external_boundaries: list[ExternalBoundary] = Field(default_factory=list)

    def entries(self) -> list[tuple[str, str, Any]]:
        """(family, key, entry) for every entry, in family then file order."""
        return [(f, getattr(e, _KEY[f]), e) for f in FAMILIES for e in getattr(self, f)]


class TargetDelta(StrictModel):
    add: FamilyEntries = Field(default_factory=FamilyEntries)
    change: FamilyEntries = Field(default_factory=FamilyEntries)


class OutsideGovernedRoot(StrictModel):
    artifact_ref: str
    reason: str


class Proposal(StrictModel):
    schema_version: Literal["aes.v0_2.proposal.probe0"]
    proposal_id: str
    title: str
    rationale: str
    closes_gaps: list[str]
    target_delta: TargetDelta
    outside_governed_roots: list[OutsideGovernedRoot] = Field(default_factory=list)

    @field_validator("proposal_id")
    @classmethod
    def _id_is_a_file_name(cls, value: str) -> str:
        if not _PROPOSAL_ID.fullmatch(value):
            raise ValueError(f"proposal_id must match {_PROPOSAL_ID.pattern} (it names the plan file): {value!r}")
        return value

    @field_validator("title", "rationale")
    @classmethod
    def _non_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("must be non-empty text")
        return value


class AcceptedPlan(Proposal):
    """What `.aes/plans/<proposal_id>.yaml` holds: the proposal and where it was accepted."""

    accepted_at_revision: str
    accepted_at: datetime


def load_proposal(path: Path) -> Proposal:
    path = Path(path)
    return _validate_model(Proposal, load_yaml_mapping(path), path)


def load_plan(path: Path) -> AcceptedPlan:
    path = Path(path)
    return _validate_model(AcceptedPlan, load_yaml_mapping(path), path)


# --------------------------------------------------------------------------- #
# Shared pieces
# --------------------------------------------------------------------------- #


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise PlanError(f"git {' '.join(args)}", [proc.stderr.strip() or f"exit {proc.returncode}"])
    return proc.stdout


def _target_path(root: Path) -> tuple[Path, list[str], Path]:
    """(target file, governed roots, plans directory) from `.aes/project.yaml`."""
    project = load_project(root / ".aes" / "project.yaml")
    return (root / project.materialization.target_path, project.governed_roots,
            root / project.materialization.plans_root)


def unrouted_requirements(target: TargetRecord) -> list[str]:
    """Evidence requirements no verification subject names and no external boundary lists."""
    routed = {r for v in target.verification_subjects for r in v.evidence_requirement_refs}
    routed |= {b.evidence_requirement_ref for b in target.external_boundaries}
    return [er for er in target.evidence_requirements() if er not in routed]


def route_violations(target: TargetRecord) -> list[str]:
    """One line per unrouted evidence requirement (SC-GF-004); used by `aes plan validate`
    on the resulting target and by `aes target validate` (the pre-commit hook) on the current one."""
    owners = target.evidence_requirements()
    return [
        f"evidence requirement '{er}' (criterion '{owners[er][0].id}') has no route: no verification "
        f"subject names it in evidence_requirement_refs and external_boundaries does not list it"
        for er in unrouted_requirements(target)
    ]


def apply_delta(target: TargetRecord, delta: TargetDelta) -> tuple[TargetRecord, list[str]]:
    """Apply `delta` to a copy of `target`; return the result and every delta-level violation.

    The result is structurally a TargetRecord (entries are typed) but is not
    semantically validated here; `validate_proposal` does that.
    """
    violations: list[str] = []
    data = target.model_dump()
    for section in ("change", "add"):  # changes index the target as it was
        seen: set[tuple[str, str]] = set()
        for family, key, entry in getattr(delta, section).entries():
            loc = f"target_delta.{section}.{family} ({key})"
            if (family, key) in seen:
                violations.append(f"'{key}' appears more than once at target_delta.{section}.{family}")
                continue
            seen.add((family, key))
            members = data.setdefault(family, [])
            index = next((i for i, m in enumerate(members) if m[_KEY[family]] == key), None)
            if section == "change":
                if index is None:
                    violations.append(f"{loc}: the target declares no {family} entry '{key}' to change "
                                      f"(new entries go under add)")
                    continue
                members[index] = entry.model_dump()
            else:
                if index is not None:
                    violations.append(f"{loc}: the target already declares {family} '{key}' "
                                      f"(replace it under change)")
                    continue
                members.append(entry.model_dump())
    if not delta.add.entries() and not delta.change.entries():
        violations.append("target_delta adds and changes nothing")
    return TargetRecord.model_validate(data), violations


# --------------------------------------------------------------------------- #
# prepare
# --------------------------------------------------------------------------- #


def skeleton() -> dict[str, Any]:
    families = {f: [] for f in FAMILIES}
    return {
        "schema_version": PROPOSAL_SCHEMA,
        "proposal_id": "",
        "title": "",
        "rationale": "",
        "closes_gaps": [],
        "target_delta": {"add": dict(families), "change": {f: [] for f in FAMILIES}},
        "outside_governed_roots": [],
    }


def prepare(root: Path) -> dict[str, Any]:
    """The input packet a proposal is written against. Deterministic for one revision and tree."""
    root = Path(root).resolve()
    target_file, governed, _ = _target_path(root)
    target = load_target(target_file)
    r = reconcile(root)
    ids: dict[str, list[str]] = {f: list(m) for f, m in target.families().items()}
    ids["external_boundaries"] = [b.evidence_requirement_ref for b in target.external_boundaries]
    return {
        "schema_version": PLAN_INPUT_SCHEMA,
        "target_id": target.target_id,
        "subject_revision": r.subject_revision,
        "dirty": r.dirty,
        "governed_roots": list(governed),
        "open_gaps": [{"id": g.id, "kind": g.kind, "ref": g.ref, "detail": g.detail} for g in r.open_gaps()],
        "unrouted_evidence_requirements": unrouted_requirements(target),
        "target_ids": ids,
        "proposal_skeleton": skeleton(),
    }


def render_yaml(data: dict[str, Any]) -> str:
    yaml = YAML()
    yaml.width = 4096  # one gap per line; no folded details
    yaml.indent(mapping=2, sequence=4, offset=2)
    out = io.StringIO()
    yaml.dump(data, out)
    return out.getvalue()


# --------------------------------------------------------------------------- #
# validate
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ValidatedProposal:
    proposal: Proposal
    target: TargetRecord  # the resulting target
    open_gaps: tuple[str, ...]


def _artifact_violations(proposal: Proposal, governed: list[str]) -> list[str]:
    violations: list[str] = []
    reasons = {o.artifact_ref: o.reason for o in proposal.outside_governed_roots}
    touched = {}
    for section in ("add", "change"):
        for a in getattr(proposal.target_delta, section).planned_artifacts:
            touched[a.id] = (section, a)
    for art_id, (section, a) in touched.items():
        path = a.locator.exact_path
        loc = f"target_delta.{section}.planned_artifacts ({art_id})"
        if any(path.startswith(g) for g in governed):
            if art_id in reasons:
                violations.append(f"outside_governed_roots names '{art_id}', but {path} is under a governed root")
            continue
        if a.kind == "source":
            violations.append(f"{loc}: source artifact {path} is outside the governed roots {governed}; "
                              f"source must be governed")
        elif not reasons.get(art_id):
            violations.append(f"{loc}: {a.kind} artifact {path} is outside the governed roots {governed} "
                              f"and outside_governed_roots gives no reason")
    for ref in reasons:
        if ref not in touched:
            violations.append(f"outside_governed_roots names '{ref}', which the delta does not add or change")
    return violations


def validate_proposal(root: Path, proposal: Proposal) -> ValidatedProposal:
    """Every violation at once as PlanError, or the resulting target."""
    root = Path(root).resolve()
    target_file, governed, _ = _target_path(root)
    current = load_target(target_file)
    result, violations = apply_delta(current, proposal.target_delta)
    violations += [f"resulting target: {v}" for v in validate_target_refs(result)]

    violations += route_violations(result)

    open_gaps = tuple(g.id for g in reconcile(root).open_gaps())
    for i, gap in enumerate(proposal.closes_gaps):
        if proposal.closes_gaps.index(gap) != i:
            violations.append(f"closes_gaps[{i}] '{gap}' is listed twice")
        elif gap not in open_gaps:
            violations.append(f"closes_gaps[{i}] '{gap}' is not an open gap in the current reconciliation "
                              f"(open: {', '.join(open_gaps) or 'none'})")

    violations += _artifact_violations(proposal, governed)
    if violations:
        raise PlanError(f"proposal {proposal.proposal_id}", violations)
    return ValidatedProposal(proposal, result, open_gaps)


# --------------------------------------------------------------------------- #
# accept
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class AcceptResult:
    target_path: Path
    plan_path: Path
    changes: tuple[str, ...]  # "added <family> <key>" / "changed <family> <key>"
    revision: str


def _dirty(root: Path) -> list[str]:
    tracked = _git(root, "status", "--porcelain", "--untracked-files=no").splitlines()
    aes = _git(root, "status", "--porcelain", "--untracked-files=all", "--", ".aes").splitlines()
    return sorted(set(tracked) | set(aes))


def _sequence_offset(text: str) -> int:
    """Indentation of the file's block-sequence dashes, so appended entries match."""
    m = re.search(r"^( *)- ", text, re.MULTILINE)
    return len(m.group(1)) if m else 2


def _rt_dump(doc: Any, offset: int) -> str:
    yaml = _yaml()
    yaml.width = 4096  # never refold a long plain scalar the file already holds on one line
    yaml.indent(mapping=2, sequence=offset + 2, offset=offset)
    out = io.StringIO()
    yaml.dump(doc, out)
    return out.getvalue()


def _trailing_slot(node: Any) -> tuple[dict, Any, int] | None:
    """Where ruamel keeps the comment (blank lines included) that follows `node`.

    It hangs on the deepest last key or item: slot 2 of a mapping key, slot 0 of
    a sequence item. A flow collection holds its trailing comment on its parent key.
    """
    if isinstance(node, CommentedMap) and node:
        key, slot = list(node)[-1], 2
    elif isinstance(node, CommentedSeq) and node:
        key, slot = len(node) - 1, 0
    else:
        return None
    child = node[key]
    if isinstance(child, CommentedMap | CommentedSeq) and child and not child.fa.flow_style():
        return _trailing_slot(child)
    return node.ca.items, key, slot


def _take_trailing(node: Any) -> Any:
    found = _trailing_slot(node)
    if found is None or found[1] not in found[0]:
        return None
    items, key, slot = found
    token, items[key][slot] = items[key][slot], None
    return token


def _put_trailing(node: Any, token: Any) -> None:
    found = _trailing_slot(node)
    if token is None or found is None:
        return
    items, key, slot = found
    items.setdefault(key, [None, None, None, None])[slot] = token


def _edit_target(target_text: str, proposal_doc: CommentedMap) -> tuple[str, list[str]]:
    """Apply the proposal's delta, as written, to the round-trip target document."""
    doc = _yaml().load(target_text)
    changes: list[str] = []
    delta = proposal_doc.get("target_delta") or {}
    for section in ("change", "add"):
        entries = delta.get(section) or {}
        for family in FAMILIES:
            for entry in entries.get(family) or []:
                key = str(entry[_KEY[family]])
                if family not in doc:
                    doc[family] = CommentedSeq()
                seq = doc[family]
                _take_trailing(entry)  # spacing that followed it in the proposal file
                if section == "change":
                    index = next(i for i, m in enumerate(seq) if str(m[_KEY[family]]) == key)
                    _put_trailing(entry, _take_trailing(seq[index]))
                    seq[index] = entry
                    changes.append(f"changed {family} {key}")
                else:
                    seq.fa.set_block_style()  # `[]` from `aes init` becomes a block list
                    # the blank line that ended the family moves to its new last entry
                    _put_trailing(entry, _take_trailing(seq[-1]) if seq else None)
                    seq.append(entry)
                    changes.append(f"added {family} {key}")
    return _rt_dump(doc, _sequence_offset(target_text)), changes


def accept_proposal(root: Path, proposal_path: Path, *, now: datetime | None = None) -> AcceptResult:
    root = Path(root).resolve()
    proposal_path = Path(proposal_path)
    dirty = _dirty(root)
    if dirty:
        raise PlanError(f"{root}: working tree is dirty; commit or remove these first",
                        dirty)
    proposal = load_proposal(proposal_path)
    target_file, _, plans_dir = _target_path(root)
    plan_path = plans_dir / f"{proposal.proposal_id}.yaml"
    if plan_path.exists():
        raise PlanError(f"proposal {proposal.proposal_id}",
                        [f"{plan_path.relative_to(root)} already exists; a plan id is accepted once"])
    validated = validate_proposal(root, proposal)

    revision = _git(root, "rev-parse", "HEAD").strip()
    if not _HEX40.fullmatch(revision):
        raise PlanError("git rev-parse HEAD", [f"expected a 40-hex revision, got {revision!r}"])
    proposal_doc = _yaml().load(proposal_path.read_text(encoding="utf-8"))
    new_text, changes = _edit_target(target_file.read_text(encoding="utf-8"), proposal_doc)
    written = TargetRecord.model_validate(_to_plain(_yaml().load(new_text)))
    if written.model_dump() != validated.target.model_dump():
        raise PlanError(f"proposal {proposal.proposal_id}",
                        ["internal: the round-trip edit of the target does not load to the validated "
                         "target; nothing was written"])

    plan_doc = _yaml().load(proposal_path.read_text(encoding="utf-8"))
    plan_doc["accepted_at_revision"] = revision
    plan_doc["accepted_at"] = (now or datetime.now(UTC)).replace(microsecond=0).isoformat()
    plan_text = _rt_dump(plan_doc, 2)
    _validate_model(AcceptedPlan, _to_plain(_yaml().load(plan_text)), plan_path)

    plans_dir.mkdir(parents=True, exist_ok=True)
    with plan_path.open("x", encoding="utf-8") as fh:
        fh.write(plan_text)
    staging = target_file.with_name(f".{target_file.name}.accept")
    try:
        staging.write_text(new_text, encoding="utf-8")
        staging.replace(target_file)
        load_target(target_file)  # what is on disk validates, or we undo
    except BaseException:
        staging.unlink(missing_ok=True)
        plan_path.unlink(missing_ok=True)
        _git(root, "checkout", "--", str(target_file.relative_to(root)))
        raise
    return AcceptResult(target_file, plan_path, tuple(changes), revision)


def render_validated(v: ValidatedProposal) -> str:
    d = v.proposal.target_delta
    t = v.target
    return (
        f"OK proposal {v.proposal.proposal_id}: {len(d.add.entries())} addition(s), "
        f"{len(d.change.entries())} change(s)\n"
        f"  closes: {', '.join(v.proposal.closes_gaps) or 'no current gap (target extension)'}\n"
        f"  resulting target: success_criteria={len(t.success_criteria)} "
        f"evidence_requirements={len(t.evidence_requirements())} "
        f"verification_subjects={len(t.verification_subjects)} "
        f"external_boundaries={len(t.external_boundaries)}; every evidence requirement has a route"
    )


def render_accepted(root: Path, a: AcceptResult) -> str:
    root = Path(root).resolve()
    target_rel, plan_rel = a.target_path.relative_to(root), a.plan_path.relative_to(root)
    return "\n".join([
        f"accepted at {a.revision}",
        *(f"  {c}" for c in a.changes),
        f"  updated {target_rel}",
        f"  wrote {plan_rel}",
        f"  next: git add {target_rel} {plan_rel} && git commit, then implement",
    ])

