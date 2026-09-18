# Plan 001 — Repository context resolution vertical

Status: **implementation partial; technical evidence adequate via authentic execution + exact-blob carry-forward; post-integration characterization/gap recomputation complete; follow-up utility review pending**
Origin gaps: GAP-AES-001, 002, 003, 004, 005, 006, 007, 009, 010, 011, 013, 014, 015, 017, 019, 020, 021, 022, 023, 024, 025, 026, 027
External consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`
Execution profile: pilot

## User outcome

A person or agent entering an unfamiliar governed repository can ask AES for the repository's current context and receive one directly usable, inspectable surface that identifies the correct navigation and authority surfaces without guessing from folder names, so they can deepen into the right native source before planning or editing.

## Canonical behavioral example

Starting state: local checkout of `BrianMills2718/data-contracts` exactly at `90c38998e8141bd07e49a77a49ec417aa29beee0`.

Action: run the Slice 1 actor entrypoint:

```text
aes-repo-context --repo <local-data-contracts-checkout> \
  --expect-revision 90c38998e8141bd07e49a77a49ec417aa29beee0
```

Expected result: the generated source-bound surface must, at minimum:

1. identify `data-contracts` and the exact reviewed revision;
2. report the current local navigation situation honestly: a physical `wiki/index.md` is not promoted to navigation authority without bounded positive routing evidence, and an absent/unrouted wiki is never invented;
3. identify `src/data_contracts/` as a native implementation and typed-contract authority surface using positive evidence;
4. distinguish root `contracts/` from repository-wide contract authority;
5. route contract-ownership questions to `docs/ops/CAPABILITY_DECOMPOSITION.md` with exact evidence;
6. preserve explicit `NONE` / `ERROR` / `UNRESOLVED` states rather than treating absence as success;
7. retain source/evidence references sufficient to explain every positive routing claim;
8. let the intended reviewer understand where to start, which authority matters, and what remains unresolved without opening raw source/code first, while keeping exact source and revision reachable.

A result that says simply `contracts/ is the contract root`, claims a wiki entrypoint that does not exist, silently infers missing declarations, or requires the stakeholder to reconstruct the result from raw JSON/code is a failure.

## Why this vertical

This is the smallest external-consumer slice that simultaneously exercises the new repository protocol, progressive-disclosure philosophy, Data Contracts boundary lesson, honest unknown-state policy, evidence binding, provider sourcing, human-observable delivery, and ACA residual-capability process.

It does not require `data-contracts` to migrate its repository layout. The consumer remains read-only and its existing native authorities remain authoritative.

## Planning shape: gaps and graphs are inputs, not slices

The originating gap ledger identifies target/current variance. Work/dependency graphs may later express coordination, but neither artifact defines a coherent implementation slice.

The first outcome-bearing vertical is the canonical `data-contracts` context experience itself:

```text
exact repository revision
  -> bounded source/declaration observations
  -> authority/navigation resolution
  -> RepositoryContextArtifact
  -> static source-bound HTML working surface
  -> direct stakeholder observation
```

Dependency-resolution work is not a substitute product slice. Enforced Planning may add a work graph only when execution coordination requires one.

## Delivery ambition, certainty, and north-star experience

Delivery maturity: `pilot`.

Confidence after D1:

- high confidence in actor/job and exact-revision/provenance/unknown-state semantics;
- high confidence that Slice 1 can use a static generated working surface without a frontend platform;
- medium confidence in the longer-term repository-context interaction model;
- low confidence that a reusable representation-routing subsystem is needed.

Directional north-star interaction:

```text
enter / select repository
        ↓
see repository role + exact revision
        ↓
see the few navigation / authority surfaces relevant to the concern
        ↓
see uncertainty, absence or error honestly
        ↓
open exact source / evidence when needed
        ↓
understand the next legitimate place to deepen
```

Slice 1 is a faithful small version of this experience, not the final AES UI.

## Modality

Hybrid.

Deductive/plan-first:
- strict typed artifact semantics;
- exact-revision binding;
- no-guessing / no-false-green rules;
- explicit manifest precedence and failure behavior;
- minimum actor-surface contract.

Exploratory:
- how much useful legacy context can be resolved from bounded explicit repository evidence;
- whether the static HTML surface is sufficient for the orientation job at Attention Checkpoint A1.

## Capability requirement and provider disposition

Provisional semantic action: `repository.context.resolve`.

ACA discovery found no verified semantic export matching this behavior. The external provider landscape found useful substrate but no complete provider.

Current disposition: **compose native/external substrate + bounded residual AES semantics**.

Selected Slice 1 bindings:

- local Git CLI / checkout — repository identity, exact revision, source/tree access;
- Pydantic `2.13.5` — strict immutable local typed models;
- PyYAML `6.0.3` — safe parsing of pilot `.agentic/repo.yaml`;
- Python standard library — JSON, paths/subprocess, and static HTML generation;
- pytest — verification harness; exact compatible release is implementation/tooling.

Not selected as Slice 1 runtime dependencies:

- Data Contracts;
- Representation Router;
- Code Map V4;
- Sourcegraph/SCIP;
- Tree-sitter;
- Backstage;
- OpenRewrite;
- CodeQL;
- predecessor AES implementations.

The first A1 later demonstrated a presentation/reconstruction gap, and follow-up presentation work is now handled separately through the Representation Router workstream. Representation Router is still not a Slice 1 Repository Context runtime dependency; this plan does not transfer Repository Context authority or semantics to it.

## Frozen contract disposition

Disposition: **`aes_local_residual`**.

Owner/model home:

```text
src/agentic_engineering_system/repository_context/models.py
```

Data Contracts remains the ecosystem typed-boundary authority where shared provider-neutral semantics fit, but its current ownership record explicitly keeps repo-specific schemas/adapters in consumers. No existing Data Contracts contract expresses this repository-context result.

Frozen model family:

- `EvidenceRef` — exact repository/revision/path and optional line/source URL;
- `AuthoritySurfaceObservation` — authority role, explicit epistemic state, locations, summary, evidence refs;
- `ConcernRootObservation` — concern/path/state/evidence refs;
- `UnresolvedSurface` — unresolved subject/reason/evidence refs;
- `RepositoryContextArtifact` — schema version, repository identity/revision, resolution status, navigation, authorities, concern roots, unresolved surfaces, and evidence.

Rules:

- strict + immutable models;
- every positive routing claim has positive evidence;
- `NONE`, `ERROR`, `UNRESOLVED` never collapse to green;
- no confidence scalar is conformance evidence;
- directory names alone establish no semantic authority.

Full D1 contract detail: [`001_D1_contract_surface_topology_freeze.md`](001_D1_contract_surface_topology_freeze.md).

## Frozen Slice 1 actor surface

Selected: **static local HTML generated by a thin CLI**.

Entrypoint:

```text
aes-repo-context --repo <local-checkout> [--expect-revision <sha>] [--output <dir>]
```

Default output:

```text
generated/repository-context/<repository-id>/<revision>/context.json
generated/repository-context/<repository-id>/<revision>/index.html
```

`context.json` is the deterministic artifact serialization; `index.html` is a non-authoritative progressive-disclosure projection. Use static HTML/CSS only for Slice 1. No SPA/framework/server/graph dependency is authorized by this plan.

## Frozen implementation topology

Planned implementation root:

```text
src/agentic_engineering_system/
```

Concrete Slice 1 files:

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

Subject roles:

| Subject | Path | Role |
| --- | --- | --- |
| Repository context/evidence models | `repository_context/models.py` | AES-local residual contract |
| exact Git source/revision | `repository_context/git_source.py` | adapter over Git |
| `PilotManifestAdapter` | `repository_context/manifest.py` | authoritative pilot-manifest reader |
| `LegacyRepositoryAdapter` | `repository_context/legacy.py` | bounded explicit-evidence adapter |
| `RepositoryContextResolver` | `repository_context/resolver.py` | residual semantic orchestration |
| `RepositoryContextWorkingSurface` | `repository_context/render_html.py` | non-authoritative projection |
| actor entrypoint | `repository_context/cli.py` / `pyproject.toml` | thin CLI boundary |

### Legacy-repository boundary

When `.agentic/repo.yaml` is absent, the adapter may use only:

1. exact Git identity/revision/tree;
2. `pyproject.toml` package metadata;
3. root navigation/context docs (`README.md`, `CLAUDE.md`, `AGENTS.md`);
4. ownership/capability docs directly referenced by those root sources;
5. existence checks only to validate an already evidenced path.

It may not infer authority from folder names, crawl for plausible authority, hard-code `data-contracts`, or treat `contracts/` as authoritative by existence.

When a pilot manifest exists, it is the authority for its declared repository context. A malformed manifest yields `ERROR`/block with correction/retry or explicit escalation; it never silently falls back to legacy inference. A valid manifest with an absent role yields `NONE`/unresolved.

## Slice horizon

### Dependency subplan D1 — CLOSED

Executable record: [`001_D1_contract_surface_topology_freeze.md`](001_D1_contract_surface_topology_freeze.md).

D1 froze:

- exact `data-contracts` revision;
- AES-local contract ownership/shape;
- static HTML + CLI actor surface;
- concrete implementation and verification paths;
- runtime provider/dependency bindings;
- legacy/manifest precedence rules.

D1 closes no originating gap. Its return path is Slice 1.

### Slice 1 — external repository context resolution — IMPLEMENTATION PARTIAL / FOLLOW-UP A1 PENDING

- advances: person/agent can orient correctly in real external repository before editing;
- vertical scope: pinned `data-contracts` revision -> bounded observations -> resolution -> typed artifact -> static source-bound HTML surface;
- de-risks: utility without repo hardcoding/generalized indexing/representation framework;
- success: AC-001 through AC-011;
- current implementation: package, resolver, renderer, CLI, and automated tests are present on the implementation branch;
- observed technical execution: the governed-repo audit passed, focused repository-context checks passed locally, the exact pinned external-consumer check passed, the real CLI resolved the pinned consumer, and deterministic revision-scoped JSON/HTML were retained;
- observed utility: the first direct A1 at AES revision `53be16fa1159f31648773062531d751c85d7a011` returned `change` because the HTML required too much reconstruction; the retained A1 receipt remains utility evidence rather than a technical-conformance reversal;
- bounded response: a projection-only correction was made afterward; per stakeholder instruction, further presentation iteration is handled separately through the Representation Router workstream rather than expanded here;
- post-integration characterization: canonical `main@320991b96a3e3aaa15aa8ba05817a7eee1c52603` is characterized at `evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/characterization.md`;
- gap state: `docs/architecture/INITIAL_GAP_LEDGER.md` has been conservatively recomputed from that characterization;
- verification disposition: Decision 0007 allows prior authentic execution to carry forward across exact relevant blob identity. Current resolver/model/adapters/CLI, focused core tests, pinned-consumer test, package declaration, and pinned `context.json` are byte-identical to the authentic execution revision; corrected renderer/test/HTML are byte-identical to the corrected projection revision. See `evidence/plan-001/evidence-carry-forward-2026-09-18.json`;
- hosted CI disposition: GitHub Actions funding is exhausted, automatic workflow triggers are disabled, and hosted CI is not a Plan 001 acceptance gate;
- evidence still outstanding for delivery: follow-up direct utility review of the corrected presentation;
- done-when: the intended reviewer has directly used the corrected presentation enough to disposition `continue | change | stop`, technical evidence remains adequate under Decision 0007, and the resulting observation does not reveal an unaddressed Plan 001 closure gap.

### Attention checkpoint A1 — first utility observation

A1 occurs immediately after the authentic Slice 1 surface exists. It is an information-value checkpoint, not technical conformance or a standing approval gate.

Record:

- usefulness/understandability for the real orientation job;
- missing/overexposed authority or uncertainty information;
- `continue | change | stop` for the interaction direction;
- next highest-value increment if continuing.

Negative utility is valid evidence. Positive utility cannot override failed/missing/stale technical evidence.

## Frozen verification topology

Verification root:

```text
tests/repository_context/
```

Concrete planned subjects:

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

Current verification status:

- model/resolver/rendering tests are present;
- technical execution has been observed locally, including the exact pinned external-consumer check and real CLI run;
- Decision 0007 carries that evidence forward only across exact relevant blob identity; the current core/pinned-consumer subjects satisfy that rule;
- GitHub Actions is optional/manual hosted convenience and is currently unavailable due funding; it is neither required nor counted as a failure;
- the pinned external-consumer test remains the command for fresh execution whenever relevant blobs change or carry-forward is insufficient;
- first A1 direct-use evidence is retained with disposition `change`; follow-up utility review of the corrected presentation remains pending.

Acceptance mapping:

- AC-001 — pinned external integration test at `90c389...` proves exact revision and package/contract authority evidence;
- AC-002 — external + fixture tests prove root `contracts/` is never universal authority by existence;
- AC-003 — the pinned external test proves a physical local wiki is not promoted by path existence alone, while a bounded fixture preserves absent/unrouted wiki navigation as `NONE` rather than inventing success;
- AC-004 — external test routes ownership to `docs/ops/CAPABILITY_DECOMPOSITION.md`;
- AC-005 — model/resolver tests enforce evidence refs on every positive claim;
- AC-006 — malformed pilot fixture yields `ERROR`/blocked with no legacy fallback;
- AC-007 — missing manifest declaration yields `NONE`/unresolved with no inferred success;
- AC-008 — resolver/CLI test proves concrete correction/retry or explicit escalation on block;
- AC-009 — revision-bound characterization receipt under `evidence/plan-001/` followed by explicit gap-ledger recomputation;
- AC-010 — rendered HTML tests establish required visible content/source reachability; direct A1 use remains additional evidence;
- AC-011 — `evidence/plan-001/a1/<aes-revision>.md` records reviewed revisions, `continue | change | stop`, limitations, and stakeholder utility separately from automation.

Planned evidence outputs:

```text
evidence/plan-001/<aes-revision>/verification-summary.json
evidence/plan-001/<aes-revision>/characterization.md
evidence/plan-001/a1/<aes-revision>.md
```

## Policy triggers carried by the plan

Before implementation:
- verify ACA/provider landscape remains materially unchanged;
- use the frozen consumer revision for the canonical external case;
- use only the frozen Slice 1 topology/dependencies unless a stop/replan condition fires;
- use only enough surface implementation to satisfy the accepted actor outcome.

Before any new reusable helper or internal dependency is added:
- record the required semantic boundary;
- re-run proportionate external/provider sourcing;
- treat internal repos as donors unless positively selected;
- record residual semantics.

Before adding non-user-facing work:
- name the Slice 1 boundary it protects;
- state the blocker;
- use the smallest discriminating probe;
- name the return path to Slice 1.

Before completion:
- execute pinned external canonical example through real entrypoint;
- execute both negative controls;
- retain revision-bound verification evidence;
- perform Attention Checkpoint A1;
- characterize current implementation at exact AES revision;
- recompute initial gap ledger;
- update `wiki/index.md` from resulting current/gap state.

## Explicit non-goals

- migrating `data-contracts` or adding `.agentic/repo.yaml`/local wiki to it;
- generalized repository crawler, symbol index, code graph, graph store, characterization platform, representation router, or final AES dashboard;
- new schema language or shared repository-context package;
- promotion into ACA before repeated evidence;
- automatic dependency on Data Contracts, Representation Router, Code Map, Project Meta, predecessor AES, or Fluid Governance;
- replacing Company Planning or Enforced Planning.

## Stop/replan conditions

Replan rather than forcing implementation if:

- an equivalent verified provider appears;
- the frozen consumer revision cannot be resolved without repo-name hardcoding or repository mutation;
- Pydantic/PyYAML/Git substrate proves semantically insufficient;
- the bounded legacy adapter starts requiring generalized crawling/indexing or bespoke source-string catalogs;
- static HTML cannot satisfy the actor observation without a materially different representation capability;
- implementation expands into generalized orchestration/fleet/characterization/representation infrastructure;
- stakeholder observation at A1 shows the outcome/interaction is materially low-value.

## Closure claim

This plan may claim `DELIVERED` only when the external canonical example and negative controls have been observed through the real entrypoint, required evidence is adequate, the intended reviewer has directly used the source-bound surface, automated and stakeholder evidence remain separate, and fresh gap recomputation shows which originating gaps are closed or narrowed.
