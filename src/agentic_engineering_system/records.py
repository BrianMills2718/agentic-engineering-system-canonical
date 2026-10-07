"""Strict typed records for `.aes/project.yaml` and `.aes/target.yaml` (probe 0).

Shape follows the first authentic consumer (whygame5). Seven semantic families:
outcomes, normative items, success criteria (with nested evidence requirements),
components, planned artifacts, verification subjects; plus optional external
boundaries, which name an evidence requirement that no verification subject in
this repository can supply and say who or what does. Anything not declared here
is rejected (`extra='forbid'`); duplicate mapping keys and unresolved references
fail loudly with their location. There is no lenient mode.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError
from ruamel.yaml.error import YAMLError

# --------------------------------------------------------------------------- #
# Errors
# --------------------------------------------------------------------------- #


class RecordLoadError(ValueError):
    """The YAML file could not be read into the declared record shape."""


class TargetValidationError(ValueError):
    """The target loaded structurally but violates a semantic invariant.

    `violations` lists every problem found, each with the exact ref and the
    location (family[index].field[index]) where it occurs.
    """

    def __init__(self, path: Path, violations: list[str]) -> None:
        self.path = path
        self.violations = violations
        lines = "\n".join(f"  - {v}" for v in violations)
        super().__init__(
            f"{path}: {len(violations)} target validation violation(s):\n{lines}"
        )


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #

NormativeKind = Literal["constraint", "behavior", "invariant", "quality"]
# trace_review: someone other than the work's author read the full trace of a model, agent or pipeline
# run (what each step was shown, which model and settings, every output with its reason) and checked
# decisions against their sources; its observation carries a TraceReview record (evidence.py).
EvidenceKind = Literal["deterministic_test", "runtime_observation", "human_review", "trace_review"]
ArtifactKind = Literal["source", "test", "configuration"]
ProofRole = Literal["direct", "negative_control"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Outcome(StrictModel):
    id: str
    actor_or_consumer: str
    statement: str
    non_goals: list[str] = Field(default_factory=list)
    rationale: str | None = None


class NormativeItem(StrictModel):
    id: str
    kind: NormativeKind
    outcome_refs: list[str]
    statement: str


class EvidenceRequirement(StrictModel):
    id: str
    kind: EvidenceKind
    requirement: str


class SuccessCriterion(StrictModel):
    id: str
    statement: str
    target_refs: list[str]
    disproof: str
    evidence_requirements: list[EvidenceRequirement]


class Component(StrictModel):
    id: str
    responsibility: str
    target_refs: list[str]
    planned_artifact_refs: list[str]


class Locator(StrictModel):
    exact_path: str


class PlannedArtifact(StrictModel):
    id: str
    locator: Locator
    kind: ArtifactKind
    purpose: str
    semantic_justification_refs: list[str]
    # Symbol commitments (SC-GF-006): `name` or `name(args) -> ret`. Python
    # source artifacts only; `aes characterize` reports drift against them.
    exports: list[str] = Field(default_factory=list)


class VerificationSubject(StrictModel):
    id: str
    criterion_refs: list[str]
    evidence_requirement_refs: list[str]
    proof_kind: EvidenceKind
    proof_role: ProofRole
    locator: str
    purpose: str


class ExternalBoundary(StrictModel):
    """An evidence requirement whose route is outside the repository (SC-GF-004).

    `aes plan validate` accepts either this or a verification subject naming the
    requirement as its route; `boundary` says who or what supplies the evidence.
    """

    evidence_requirement_ref: str
    boundary: str


class TargetRecord(StrictModel):
    schema_version: str
    target_id: str
    outcomes: list[Outcome]
    normative_items: list[NormativeItem]
    success_criteria: list[SuccessCriterion]
    components: list[Component]
    planned_artifacts: list[PlannedArtifact]
    verification_subjects: list[VerificationSubject]
    external_boundaries: list[ExternalBoundary] = Field(default_factory=list)

    # -- indexes ----------------------------------------------------------- #

    def evidence_requirements(self) -> dict[str, tuple[SuccessCriterion, EvidenceRequirement]]:
        """ER id -> (owning criterion, ER). ERs are nested, so this is the only index."""
        out: dict[str, tuple[SuccessCriterion, EvidenceRequirement]] = {}
        for sc in self.success_criteria:
            for er in sc.evidence_requirements:
                out[er.id] = (sc, er)
        return out

    def families(self) -> dict[str, dict[str, Any]]:
        """Family name -> {id: record} for every declared ID, ERs included."""
        return {
            "outcomes": {o.id: o for o in self.outcomes},
            "normative_items": {n.id: n for n in self.normative_items},
            "success_criteria": {s.id: s for s in self.success_criteria},
            "evidence_requirements": {k: v[1] for k, v in self.evidence_requirements().items()},
            "components": {c.id: c for c in self.components},
            "planned_artifacts": {a.id: a for a in self.planned_artifacts},
            "verification_subjects": {v.id: v for v in self.verification_subjects},
        }

    def kind_of(self, record_id: str) -> str | None:
        for family, members in self.families().items():
            if record_id in members:
                return family
        return None


class AesInfo(StrictModel):
    architecture_line: str
    distribution_version: str
    initialized_at: datetime | None = None  # written by `aes init`; absent in hand-made projects


class Materialization(StrictModel):
    target_path: str
    plans_root: str
    observations_root: str
    generated_root: str


class Ecosystem(StrictModel):
    primary_language_or_runtime: str


class ProjectRecord(StrictModel):
    schema_version: str
    project_id: str
    aes: AesInfo
    governed_roots: list[str]
    materialization: Materialization
    ecosystem: Ecosystem

    @field_validator("governed_roots")
    @classmethod
    def _one_trailing_slash(cls, roots: list[str]) -> list[str]:
        # Consumers test containment with `path.startswith(root)`; a hand-written
        # "src" would also capture "src_backup/...". Normalize once, at the load
        # boundary, the same way `aes init` writes roots.
        out = []
        for root in roots:
            if root.startswith("/") or ".." in Path(root).parts or root.strip("/") == "":
                raise ValueError(f"governed root must be a relative subdirectory: {root!r}")
            out.append(root.rstrip("/") + "/")
        return out


# --------------------------------------------------------------------------- #
# YAML I/O
# --------------------------------------------------------------------------- #


def _yaml() -> YAML:
    yaml = YAML(typ="rt")  # YAML 1.2 round-trip loader
    yaml.allow_duplicate_keys = False  # explicit; the rt default is already False
    return yaml


def _to_plain(value: Any) -> Any:
    """Convert ruamel round-trip containers/scalars into plain Python values."""
    if isinstance(value, dict):
        return {str(k): _to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_plain(v) for v in value]
    if isinstance(value, str):
        return str(value)  # collapse FoldedScalarString / LiteralScalarString
    return value


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    """Load one YAML document as a mapping. Duplicate keys and non-mapping roots fail."""
    path = Path(path)
    if not path.is_file():
        raise RecordLoadError(f"{path}: file does not exist")
    return parse_yaml_mapping(path.read_text(encoding="utf-8"), str(path))


def parse_yaml_mapping(text: str, label: str) -> dict[str, Any]:
    """`load_yaml_mapping` for text that is not a file on disk (e.g. `git show REV:path`)."""
    try:
        data = _yaml().load(text)
    except DuplicateKeyError as exc:
        raise RecordLoadError(f"{label}: duplicate mapping key rejected: {exc}") from exc
    except YAMLError as exc:
        raise RecordLoadError(f"{label}: YAML parse error: {exc}") from exc
    if data is None:
        raise RecordLoadError(f"{label}: document is empty")
    if not isinstance(data, dict):
        raise RecordLoadError(f"{label}: root must be a mapping, got {type(data).__name__}")
    return _to_plain(data)


def _validate_model(model: type[BaseModel], data: dict[str, Any], path: Path) -> Any:
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise RecordLoadError(f"{path}: does not match {model.__name__}:\n{exc}") from exc


def load_project(path: Path) -> ProjectRecord:
    path = Path(path)
    return _validate_model(ProjectRecord, load_yaml_mapping(path), path)


def load_target(path: Path) -> TargetRecord:
    """Strict load + semantic validation. Raises RecordLoadError or TargetValidationError."""
    path = Path(path)
    return parse_target(load_yaml_mapping(path), path)


def parse_target(data: dict[str, Any], path: Path) -> TargetRecord:
    """`load_target` on an already-parsed mapping; `path` labels errors."""
    target: TargetRecord = _validate_model(TargetRecord, data, path)
    violations = validate_target_refs(target)
    if violations:
        raise TargetValidationError(path, violations)
    return target


# --------------------------------------------------------------------------- #
# Semantic validation
# --------------------------------------------------------------------------- #


def validate_target_refs(target: TargetRecord) -> list[str]:
    """Return every semantic violation as a human-readable line (empty = valid)."""
    violations: list[str] = []

    # 1. IDs unique across all families (nested ERs included).
    seen: dict[str, str] = {}
    declared: list[tuple[str, str]] = []
    for i, o in enumerate(target.outcomes):
        declared.append((o.id, f"outcomes[{i}]"))
    for i, n in enumerate(target.normative_items):
        declared.append((n.id, f"normative_items[{i}]"))
    for i, s in enumerate(target.success_criteria):
        declared.append((s.id, f"success_criteria[{i}]"))
        for j, er in enumerate(s.evidence_requirements):
            declared.append((er.id, f"success_criteria[{i}].evidence_requirements[{j}]"))
    for i, c in enumerate(target.components):
        declared.append((c.id, f"components[{i}]"))
    for i, a in enumerate(target.planned_artifacts):
        declared.append((a.id, f"planned_artifacts[{i}]"))
    for i, v in enumerate(target.verification_subjects):
        declared.append((v.id, f"verification_subjects[{i}]"))
    for record_id, location in declared:
        if record_id in seen:
            violations.append(
                f"duplicate id '{record_id}' at {location} (first declared at {seen[record_id]})"
            )
        else:
            seen[record_id] = location

    outcome_ids = {o.id for o in target.outcomes}
    ni_ids = {n.id for n in target.normative_items}
    sc_ids = {s.id for s in target.success_criteria}
    er_index = target.evidence_requirements()
    artifact_ids = {a.id for a in target.planned_artifacts}
    semantic_ids = outcome_ids | ni_ids | sc_ids  # what a target_ref may name

    def check_refs(refs: list[str], allowed: set[str], location: str, expected: str) -> None:
        for k, ref in enumerate(refs):
            if ref not in allowed:
                violations.append(
                    f"unresolved ref '{ref}' at {location}[{k}] (expected {expected})"
                )

    # 2. Every *_refs entry resolves.
    for i, n in enumerate(target.normative_items):
        loc = f"normative_items[{i}] ({n.id})"
        check_refs(n.outcome_refs, outcome_ids, f"{loc}.outcome_refs", "an outcome id")
        # 3. Every normative item reaches an outcome.
        if not any(r in outcome_ids for r in n.outcome_refs):
            violations.append(f"normative item '{n.id}' at {loc} reaches no declared outcome")

    for i, s in enumerate(target.success_criteria):
        loc = f"success_criteria[{i}] ({s.id})"
        check_refs(
            s.target_refs, semantic_ids, f"{loc}.target_refs",
            "an outcome, normative item, or criterion id",
        )
        # 4. Every criterion has at least one evidence requirement.
        if not s.evidence_requirements:
            violations.append(f"criterion '{s.id}' at {loc} has no evidence_requirements")

    for i, c in enumerate(target.components):
        loc = f"components[{i}] ({c.id})"
        check_refs(
            c.target_refs, semantic_ids, f"{loc}.target_refs",
            "an outcome, normative item, or criterion id",
        )
        check_refs(
            c.planned_artifact_refs, artifact_ids, f"{loc}.planned_artifact_refs",
            "a planned artifact id",
        )

    for i, a in enumerate(target.planned_artifacts):
        loc = f"planned_artifacts[{i}] ({a.id})"
        check_refs(
            a.semantic_justification_refs, semantic_ids,
            f"{loc}.semantic_justification_refs",
            "an outcome, normative item, or criterion id",
        )
        if a.exports:
            # Imported here: characterize_python imports this module.
            from .characterize_python import parse_export

            if a.kind != "source" or not a.locator.exact_path.endswith(".py"):
                violations.append(
                    f"exports at {loc} require kind 'source' and a .py exact_path "
                    f"(got kind '{a.kind}', path '{a.locator.exact_path}')"
                )
            names: set[str] = set()
            for k, entry in enumerate(a.exports):
                try:
                    name, _ = parse_export(entry)
                except ValueError as exc:
                    violations.append(f"{exc} at {loc}.exports[{k}]")
                    continue
                if name in names:
                    violations.append(f"duplicate export '{name}' at {loc}.exports[{k}]")
                names.add(name)

    for i, v in enumerate(target.verification_subjects):
        loc = f"verification_subjects[{i}] ({v.id})"
        check_refs(v.criterion_refs, sc_ids, f"{loc}.criterion_refs", "a criterion id")
        for k, ref in enumerate(v.evidence_requirement_refs):
            if ref not in er_index:
                violations.append(
                    f"unresolved ref '{ref}' at {loc}.evidence_requirement_refs[{k}] "
                    "(expected an evidence requirement id nested in a criterion)"
                )
                continue
            owner = er_index[ref][0].id
            if owner not in v.criterion_refs:
                violations.append(
                    f"evidence requirement '{ref}' at {loc}.evidence_requirement_refs[{k}] "
                    f"belongs to criterion '{owner}', which is not in criterion_refs {v.criterion_refs}"
                )

    for i, b in enumerate(target.external_boundaries):
        loc = f"external_boundaries[{i}]"
        if b.evidence_requirement_ref not in er_index:
            violations.append(
                f"unresolved ref '{b.evidence_requirement_ref}' at {loc}.evidence_requirement_ref "
                "(expected an evidence requirement id nested in a criterion)"
            )
        if not b.boundary:
            violations.append(f"external boundary at {loc} ({b.evidence_requirement_ref}) has empty boundary text")
    bounded = [b.evidence_requirement_ref for b in target.external_boundaries]
    for ref in sorted({r for r in bounded if bounded.count(r) > 1}):
        violations.append(f"evidence requirement '{ref}' has more than one external boundary")

    return violations
