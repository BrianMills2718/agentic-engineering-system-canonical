# Plan 001 / D1 — Contract, surface, and topology freeze

Status: **CLOSED — design decisions frozen; implementation not started**.
Parent authority: [`001_repository_context_resolution_vertical.md`](001_repository_context_resolution_vertical.md).
Closed: 2026-09-16.

This is a subordinate execution brief for **Dependency subplan D1** in Plan 001. It does not create a second plan, add success criteria, or change the accepted outcome. If this brief conflicts with Plan 001, Plan 001 wins and this brief must be corrected or retired.

## Purpose

Close only the remaining design decisions that prevent Slice 1 from starting without hidden architectural choices:

1. determine the natural owner/shape of the repository-context result contract;
2. choose the smallest authentic human/agent entrypoint for Slice 1;
3. freeze concrete implementation and verification subjects;
4. record the exact provider/dependency disposition needed to execute Slice 1.

D1 is `dependency_resolution`, not an implementation slice. Its mandatory return path is **immediately to Plan 001 / Slice 1**.

## Accepted Slice 1 outcome

Do not redesign this outcome during D1:

> A person or agent entering the exact reviewed `data-contracts` revision can use one source-bound surface to identify the relevant navigation and authority surfaces, see uncertainty/absence/error honestly, reach the exact supporting source/evidence, and know the legitimate place to deepen next without reconstructing the repository from raw code or agent dialogue.

The surface is an actor boundary, not necessarily a graphical application.

## D1 inputs reviewed

- Plan 001 and AC-001 through AC-011;
- `docs/architecture/SYSTEM_BOUNDARY.md`;
- `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`;
- `research/investigations/2026-09-16-repository-context-provider-landscape.md`;
- current ACA discovery/provider knowledge;
- `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`, including `README.md`, `pyproject.toml`, `src/data_contracts/models.py`, `src/data_contracts/source_claims.py`, and `docs/ops/CAPABILITY_DECOMPOSITION.md`;
- current canonical AES repository conventions;
- Representation Router as a donor/provider candidate for the surface decision.

## Frozen external consumer revision

Slice 1 canonical consumer:

```text
BrianMills2718/data-contracts
revision: 90c38998e8141bd07e49a77a49ec417aa29beee0
```

The external integration check must refuse or clearly report a revision mismatch when it is intended to prove the canonical example.

## Decision 1 — Result-contract disposition

Disposition: **`aes_local_residual`**.

Owner: canonical AES.

Planned model home:

```text
src/agentic_engineering_system/repository_context/models.py
```

### Why

Data Contracts owns reusable boundary-model/compatibility substrate, but its current ownership declaration explicitly keeps repo-specific schema design and adapter semantics in consuming repositories. No current `data-contracts` contract expresses repository navigation/authority context, and its source-backed claim contracts are specialized for claim custody rather than repository-context evidence.

Slice 1 therefore does **not** add `data-contracts` as a runtime dependency merely to inherit `BoundaryModel`. The local contract uses stable external Pydantic directly. Promotion to a shared Data Contracts contract is reconsidered only after independent consumers demonstrate repeated provider-neutral semantics.

### Frozen contract shape

All models are strict and immutable (`extra=forbid`, frozen) unless a concrete implementation test proves that stricter behavior prevents the accepted slice.

```text
EvidenceRef
  evidence_id: str
  repository_id: str
  revision: str
  path: str
  line_start: int | None
  line_end: int | None
  source_url: str | None
  note: str | None

AuthoritySurfaceObservation
  role: navigation | normative | decision | plan | implementation |
        verification | contract | ownership
  state: OBSERVED | NONE | ERROR | UNRESOLVED
  locations: tuple[str, ...]
  summary: str
  evidence_refs: tuple[str, ...]

ConcernRootObservation
  concern: str
  state: OBSERVED | NONE | ERROR | UNRESOLVED
  path: str | None
  evidence_refs: tuple[str, ...]

UnresolvedSurface
  subject: str
  reason: str
  evidence_refs: tuple[str, ...]

RepositoryContextArtifact
  schema_version: "0.1"
  repository_id: str
  revision: str
  resolution_status: RESOLVED | PARTIAL | ERROR
  navigation: AuthoritySurfaceObservation
  authorities: tuple[AuthoritySurfaceObservation, ...]
  concern_roots: tuple[ConcernRootObservation, ...]
  unresolved: tuple[UnresolvedSurface, ...]
  evidence: tuple[EvidenceRef, ...]
```

Rules:

- every positive `OBSERVED` routing claim references at least one `EvidenceRef`;
- `NONE`, `ERROR`, and `UNRESOLVED` remain explicit and never collapse to success;
- no model confidence scalar is used as conformance evidence;
- source references are revision-bound;
- a root named `contracts/` is not contract authority without positive evidence.

## Decision 2 — Slice 1 actor surface

Selected surface: **generated static local HTML working surface, produced by a thin CLI**.

Planned entrypoint:

```text
aes-repo-context --repo <local-checkout> [--expect-revision <sha>] [--output <dir>]
```

Default generated output:

```text
generated/repository-context/<repository-id>/<revision>/context.json
generated/repository-context/<repository-id>/<revision>/index.html
```

`context.json` is a deterministic serialization of `RepositoryContextArtifact`. `index.html` is a non-authoritative actor/review projection over the same artifact.

### Required surface behavior

The HTML surface must show, without requiring the reviewer to read JSON first:

- repository identity and exact revision;
- the legitimate local starting/navigation point;
- authority roles with explicit epistemic state;
- the warning that `contracts/` is not universal authority for the canonical consumer;
- unresolved/absent/error states;
- evidence/source links and exact paths/revision;
- the next legitimate place to deepen.

Use ordinary static HTML/CSS and progressive disclosure such as `<details>` where useful. No JavaScript framework, server runtime, graph library, or Representation Router runtime dependency is selected for Slice 1.

### Rejected alternatives

- **raw JSON as primary surface** — cheapest to emit but pushes reconstruction onto the stakeholder and fails the actor-surface intent;
- **terminal-only structured output** — viable future companion, but weaker for progressive disclosure/source inspection at A1;
- **Representation Router dependency** — useful donor/provider candidate, but Slice 1 needs one bounded projection rather than representation selection/composition;
- **React/SPA/general AES workbench** — premature framework commitment and unnecessary maintenance surface.

The CLI prints the generated HTML path and a compact status summary. Browser opening may be optional convenience, not a semantic requirement.

## Decision 3 — Concrete implementation topology

Planned implementation root:

```text
src/agentic_engineering_system/
```

Planned package/entrypoint files:

```text
pyproject.toml
src/agentic_engineering_system/__init__.py
src/agentic_engineering_system/repository_context/__init__.py
src/agentic_engineering_system/repository_context/models.py
src/agentic_engineering_system/repository_context/git_source.py
src/agentic_engineering_system/repository_context/manifest.py
src/agentic_engineering_system/repository_context/legacy.py
src/agentic_engineering_system/repository_context/resolver.py
src/agentic_engineering_system/repository_context/render_html.py
src/agentic_engineering_system/repository_context/cli.py
```

### Subject ownership

| Planned subject | Concrete home | Class |
| --- | --- | --- |
| `RepositoryContextArtifact`, evidence/observation models | `repository_context/models.py` | AES-local residual typed boundary |
| exact revision/source access | `repository_context/git_source.py` | adapter over Git |
| `PilotManifestAdapter` | `repository_context/manifest.py` | AES adapter using safe YAML parsing |
| `LegacyRepositoryAdapter` | `repository_context/legacy.py` | bounded evidence adapter |
| `RepositoryContextResolver` | `repository_context/resolver.py` | AES residual semantic orchestration |
| `RepositoryContextWorkingSurface` | `repository_context/render_html.py` | non-authoritative projection |
| actor entrypoint | `repository_context/cli.py` + `pyproject.toml` script `aes-repo-context` | thin application boundary |

### Legacy adapter boundary

The legacy adapter may use only bounded, inspectable evidence sources:

1. exact Git repository identity/revision/tree;
2. `pyproject.toml` packaging metadata for implementation/package roots;
3. root navigation/context documents such as `README.md`, `CLAUDE.md`, and `AGENTS.md`;
4. ownership/capability documents directly referenced by those root sources;
5. existence checks used only to validate an already evidenced path.

For the pinned `data-contracts` example, the relevant evidence includes its README local-entrypoint declaration, setuptools `where = ["src"]` package configuration, and the explicitly routed `docs/ops/CAPABILITY_DECOMPOSITION.md` ownership record.

The adapter must not:

- infer semantic authority from directory names alone;
- crawl the whole repository looking for plausible authority;
- hard-code the repository name `data-contracts`;
- treat a root `contracts/` directory as authority because it exists;
- use legacy inference when a pilot manifest exists but is malformed;
- fill a missing manifest declaration from legacy heuristics when a valid manifest is authoritative for that role.

A malformed authoritative manifest is `ERROR`/blocked. A valid manifest with an absent role yields `NONE`/unresolved for that role.

## Decision 4 — Provider/dependency bindings

Initial Slice 1 runtime dependencies:

```text
Python >= 3.11
Git CLI / local Git checkout
pydantic == 2.13.5
PyYAML == 6.0.3
Python standard library HTML/path/subprocess/JSON facilities
```

Verification dependency: `pytest` (implementation may choose a current compatible release without an architecture decision).

Not selected as Slice 1 runtime dependencies:

- `data-contracts`;
- Representation Router;
- Code Map V4;
- Sourcegraph/SCIP;
- Tree-sitter;
- Backstage;
- OpenRewrite;
- CodeQL;
- predecessor AES implementations.

The dependency decision is reconsidered if implementation exposes semantics that cannot be represented safely by these bounded primitives.

## Decision 5 — Verification topology

Planned verification root:

```text
tests/repository_context/
```

Planned subjects:

```text
tests/repository_context/test_models.py
tests/repository_context/test_manifest_adapter.py
tests/repository_context/test_legacy_adapter.py
tests/repository_context/test_resolver.py
tests/repository_context/test_render_html.py
tests/repository_context/test_data_contracts_pinned.py
tests/repository_context/fixtures/pilot_valid/
tests/repository_context/fixtures/pilot_malformed/
tests/repository_context/fixtures/pilot_missing_declaration/
```

Criterion mapping:

| Criterion | Planned proof/check |
| --- | --- |
| AC-001 | `test_data_contracts_pinned.py` against local checkout exactly at `90c389...`; assert package/contract surface evidence |
| AC-002 | pinned external test + legacy fixture asserts root `contracts/` never becomes universal contract authority without evidence |
| AC-003 | pinned external test asserts local `wiki/index.md` absence is `NONE`/legacy navigation, never invented |
| AC-004 | pinned external test routes ownership to `docs/ops/CAPABILITY_DECOMPOSITION.md` with evidence |
| AC-005 | model/resolver tests require evidence refs for every positive claim |
| AC-006 | `pilot_malformed` fixture yields `ERROR`/blocked and no legacy fallback |
| AC-007 | `pilot_missing_declaration` fixture yields `NONE`/unresolved for absent role and no inferred success |
| AC-008 | manifest/resolver/CLI test asserts blocked output includes concrete correction/retry path or authority-sensitive escalation |
| AC-009 | post-implementation revision-bound characterization receipt under `evidence/plan-001/` plus explicit gap-ledger recomputation; no generalized characterization engine |
| AC-010 | rendered HTML test proves required visible information/source reachability; direct stakeholder use at A1 remains required evidence beyond the automated check |
| AC-011 | stakeholder observation receipt under `evidence/plan-001/a1/` records `continue | change | stop`, limitations, reviewed AES revision, and reviewed consumer revision |

Automated HTML assertions establish rendering/content properties only. They do not establish stakeholder utility.

## Planned evidence outputs after Slice 1

```text
evidence/plan-001/<aes-revision>/verification-summary.json
evidence/plan-001/<aes-revision>/characterization.md
evidence/plan-001/a1/<aes-revision>.md
```

These are append-only/revision-bound receipts. The current gap ledger/wiki remain derived current projections.

## D1 exit test — PASS

A fresh implementation agent can now answer without making a new architecture/product decision:

- **Outcome:** resolve the pinned external repository into one directly usable source-bound context surface.
- **Entrypoint:** `aes-repo-context`, producing revision-scoped static HTML + JSON.
- **Contract owner:** AES-local `RepositoryContextArtifact` in `repository_context/models.py`.
- **Permitted code subjects:** the exact package/files listed above plus their tests/fixtures and `pyproject.toml` packaging metadata.
- **Selected dependencies:** Git, Pydantic 2.13.5, PyYAML 6.0.3, standard library; pytest for verification.
- **Residual AES semantics:** authority/navigation resolution, explicit epistemic-state handling, legacy evidence rules, and artifact-to-working-surface projection.
- **Verification:** concrete tests/observations mapped above.
- **Recovery:** invalid authoritative manifest blocks with correction/retry or explicit escalation; it never silently falls back green.
- **Do not generalize:** no crawler, code index, graph store, characterization platform, representation framework, fleet rollout, or new shared contract package.

## Handoff after D1

```text
D1 CLOSED
   ↓
Plan 001 topology frozen
   ↓
Enforced Planning execution contract
   ↓
Slice 1 TDD / governed implementation
   ↓
authentic actor surface
   ↓
Attention Checkpoint A1
```

D1 itself closes no originating AES gap. Only implementation, fresh evidence, direct utility observation where required, re-characterization, and gap recomputation can do that.
