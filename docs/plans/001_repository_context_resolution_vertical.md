# Plan 001 — Repository context resolution vertical

Status: design-ready; provider landscape complete; implementation not started
Origin gaps: GAP-AES-001, 002, 003, 004, 005, 006, 007, 009, 010, 011, 013, 014, 015, 017, 019, 020, 021, 022, 023, 024, 025, 026, 027
External consumer: `BrianMills2718/data-contracts`
Execution profile: pilot

## User outcome

A person or agent entering an unfamiliar governed repository can ask AES for the repository's current context and receive one directly usable, inspectable surface that identifies the correct navigation and authority surfaces without guessing from folder names, so they can deepen into the right native source before planning or editing.

## Canonical behavioral example

Starting state: current `data-contracts` repository.

Action: resolve its repository context through the first AES context-resolution seam and present the result through the actual human/agent entrypoint for this slice.

Expected result: the surface must, at minimum:

1. identify `data-contracts` as the target repository and bind the observation to an exact revision;
2. report the current local navigation situation honestly rather than inventing `wiki/index.md` when absent;
3. identify `src/data_contracts/` as a native implementation and typed-contract authority surface;
4. distinguish the root `contracts/` directory from the repository's general contract authority;
5. route contract-ownership questions to the repository's native capability-decomposition authority;
6. preserve explicit `NONE`/unknown states for undeclared surfaces rather than treating absence as success;
7. retain source/evidence references sufficient to explain every resolved routing claim;
8. let the intended reviewer understand where to start, which authority matters, and what remains unresolved without opening raw source/code first, while keeping exact source and revision reachable.

A result that says simply `contracts/ is the contract root`, claims a wiki entrypoint that does not exist, silently infers missing declarations, or requires the stakeholder to reconstruct the result from raw JSON/code is a failure.

## Why this vertical

This is the smallest external-consumer slice that simultaneously exercises the new repository protocol, progressive-disclosure philosophy, Data Contracts boundary lesson, honest unknown-state policy, evidence binding, provider sourcing, human-observable delivery, and ACA residual-capability process.

It does not require `data-contracts` to migrate its repository layout. The consumer remains an authentic external source whose existing authorities must be respected.

## Planning shape: gaps and graphs are inputs, not slices

The originating gap ledger tells us which target/current variances matter. Planned relationships and any later work-unit DAG can express prerequisites or coordination. Neither automatically defines a coherent implementation slice.

Company Planning must derive slices separately. For this plan, the first outcome-bearing vertical is the canonical `data-contracts` context experience itself: one path from exact repository revision through authority resolution to a human-usable source-bound result and its verification. Contract/provider decisions that block that path are dependency-resolution work, not substitute product slices. Enforced Planning may later add a work-unit graph if coordination requires it, but graph nodes must preserve the slice boundary rather than replace it.

## Delivery ambition, certainty, and north-star experience

Delivery maturity: `pilot`.

Current confidence:

- high confidence in the actor/job: orient correctly in a real repository before planning or editing;
- high confidence that exact revision, authority provenance, and honest unknown/error states are load-bearing;
- medium confidence in the best interaction/representation for repository context;
- low confidence that a reusable representation-routing subsystem is required for this first vertical.

Therefore this plan does **not** freeze a final AES UI. It freezes a directional north-star interaction:

```text
enter / select repository
        ↓
see the repository's role and current revision
        ↓
see the few navigation / authority surfaces relevant to the current concern
        ↓
see uncertainty, absence or error honestly
        ↓
open exact source / evidence when needed
        ↓
understand the next legitimate place to deepen
```

Slice 1 should be a faithful small version of that experience. D1 may choose the smallest suitable rendering/interaction technology after the contract and concrete topology are known. A temporary validated projection is preferred over a durable representation framework unless repeated use demonstrates a broader need.

## Modality

Hybrid.

Deductive/plan-first:
- artifact schema and authority semantics;
- exact-revision binding;
- no-guessing / no-false-green rules;
- explicit native-surface declarations when available;
- the minimum human-surface contract above.

Exploratory:
- how much legacy repository context can be resolved safely when `.agentic/repo.yaml` is absent;
- which evidence/source adapters are sufficient without creating a generalized crawler;
- which representation makes the context useful without inventing another authority or UI framework.

## Capability requirement

Provisional semantic action: `repository.context.resolve`.

ACA discovery on 2026-09-16 found no current verified semantic export matching this behavior. The action remains a capability requirement for this vertical; the plan does not grant it ecosystem-level capability status.

The external-first provider landscape is recorded in `research/investigations/2026-09-16-repository-context-provider-landscape.md`. No reviewed platform, standard, mature OSS package, or service provides the complete AES authority-resolution boundary.

Current provider disposition: **compose native substrate + residual AES semantics**.

- Git/GitHub facilities are candidate substrate for repository identity, exact revision, and source retrieval.
- Stable parsers/validators should be used for declared formats rather than inventing parser infrastructure.
- Sourcegraph/SCIP, Tree-sitter, Backstage, OpenRewrite, CodeQL, and internal code-map systems remain unselected for the first vertical because their useful capabilities do not match the complete boundary or are broader than required.
- Internal repositories are evidence/design donors by default, not runtime dependencies.
- Representation Router is a relevant donor/provider candidate if the human-surface need becomes a genuine representation-selection/composition capability; it is not selected merely because this slice needs a usable surface.
- The residual AES behavior is the bounded semantic mapping from explicit declarations and carefully evidenced legacy surfaces into repository navigation/authority roles.

This disposition justifies residual semantics, not a generalized framework or package hierarchy.

## Contract boundary

The first vertical needs one typed result representing repository context. The semantic fields should cover:

- repository identity;
- observed revision;
- navigation entrypoint state;
- native authority surfaces by role;
- concern roots and their declared/observed status;
- source references / evidence;
- unresolved or ambiguous surfaces;
- resolution status.

Before creating an AES-local contract, complete the Data Contracts check for an existing neutral contract that honestly represents this boundary. Reuse or extend it when semantics match. Do not add a generic contract merely because Data Contracts exists.

The human-facing projection is not automatically part of that provider-neutral data contract. Keep semantic result authority separate from representation unless the consumer seam demonstrates that a shared representation contract is genuinely required.

## Planned implementation topology

Not yet frozen to concrete files.

Company Planning establishes these first-class subjects conceptually:

- **RepositoryContextResolver** — orchestration boundary for resolving one repository at one revision.
- **RepositoryContextArtifact** — typed, immutable result consumed by agent/context projections.
- **AuthoritySurfaceObservation** — evidence-backed observation of one native authority/navigation surface.
- **LegacyRepositoryAdapter** — bounded adapter for repositories without the pilot `.agentic/repo.yaml`; it may report unknown, but may not fabricate declarations.
- **PilotManifestAdapter** — reader for `.agentic/repo.yaml` when present.
- **RepositoryContextWorkingSurface** — conceptual human/agent projection over the artifact for Slice 1; exact renderer/file ownership remains unresolved until D1 and must not become semantic authority.

The implementation root and exact file paths remain unresolved until the contract check and final topology freeze are complete.

## Slice horizon

### Dependency subplan D1 — freeze contract and concrete topology

This is on the critical path but is not the first product/outcome slice.

Executable brief: [`001_D1_contract_surface_topology_freeze.md`](001_D1_contract_surface_topology_freeze.md). The brief is subordinate to this plan and adds no new outcome or success criteria.

- blocks: first external vertical
- unknowns: contract owner, minimum artifact schema, exact concrete implementation/verification subjects, smallest authentic human-facing entrypoint
- instrument: inspect Data Contracts contract surfaces plus current repository/package conventions and available representation/provider seams
- readout: one contract disposition and one concrete topology with no duplicate authority
- promotion: update this plan and `.agentic/relationships.yaml` with exact subjects
- done-when: contract disposition recorded and the first vertical can be implemented without an unstated architectural decision
- return path: immediately into Slice 1; D1 must not expand into generalized context/indexing/representation infrastructure

### Slice 1 — external repository context resolution

This is the first authentic outcome-bearing vertical.

- advances: a person or agent can orient correctly in a real external repository before planning/editing
- vertical scope: exact `data-contracts` revision -> source/declaration observations -> authority resolution -> one `RepositoryContextArtifact` -> source-bound human/agent working surface
- de-risks: whether useful context can be resolved without repo-specific hardcoding or a generalized indexing/representation system, and whether the result is actually useful when directly inspected
- success: AC-001 through AC-011, including deliberate negative controls, recovery/escalation behavior, human usability, and direct stakeholder observation
- evidence: exact consumer revision, exact AES revision, source refs for positive claims, retained negative-control receipts, separate stakeholder observation receipt
- non-goal: migration of `data-contracts`
- done-when: the canonical external example passes through the real entrypoint, the negative/error/unknown paths behave honestly, and the intended reviewer has directly used the surface enough to disposition `continue | change | stop` for the next increment

### Attention checkpoint A1 — first utility observation

A1 occurs immediately after Slice 1's authentic surface exists. It is an information-value checkpoint, not a standing approval gate and not technical conformance by itself.

The intended reviewer uses the capability and records, at minimum:

- whether the context is understandable and useful for the real orientation job;
- whether important authority/uncertainty information is missing or overexposed;
- whether the interaction model should continue, change materially, or stop;
- which next increment, if any, now has the highest value.

A negative judgment is valid evidence. Do not hide or reinterpret it as a UI polish request if it shows the product direction or slice semantics are wrong. Conversely, positive stakeholder utility does not override failed, missing, stale, or insufficient required technical evidence.

### Later slice skeleton — declared pilot-manifest route

After Slice 1 and A1, a manifest-backed self-dogfood route may be specified if it closes a demonstrated remaining gap and still competes favorably with other next increments. It is not on the pre-observation critical path merely because the canonical repo already has `.agentic/repo.yaml`.

## Planned verification topology

Acceptance criteria are pre-code:

- AC-001 — current `data-contracts` resolves at an exact revision and names `src/data_contracts/` as a native implementation/contract surface.
- AC-002 — the resolver does not classify root `contracts/` as the universal contract authority.
- AC-003 — absence of a local `wiki/index.md` is represented as absence/legacy navigation, not success or invention.
- AC-004 — native capability-decomposition authority is surfaced as a route for ownership questions.
- AC-005 — every positive routing claim carries its source/evidence reference.
- AC-006 — deliberately malformed pilot manifest produces `ERROR` or `FAIL`, never fallback-green.
- AC-007 — deliberately absent required declaration in a pilot fixture produces `NONE`/unresolved, never inferred success.
- AC-008 — a policy block caused by malformed/ambiguous authoritative input returns an executable recovery for reversible cases or an explicit human escalation for authority-sensitive ambiguity.
- AC-009 — after implementation, a fresh revision-bound characterization recomputes the originating gaps; plan completion alone does not close them.
- AC-010 — the intended reviewer can use the actual Slice 1 surface to identify where to start, which authority matters, and what remains unresolved without opening raw code/data first, while exact sources/revisions remain directly reachable.
- AC-011 — direct stakeholder use is recorded separately from automated verification with an explicit `continue | change | stop` disposition and limitations; automated green alone cannot stand in for this utility observation.

Negative controls AC-006 and AC-007 must be observed before the resolver is described as evidenced.

## Policy triggers carried by the plan

Before implementation:
- verify the ACA discovery result is still current;
- complete the Data Contracts neutral-contract disposition;
- freeze the exact `data-contracts` revision used by AC-001 through AC-005;
- freeze the concrete implementation and verification topology from dependency subplan D1;
- choose only enough working-surface implementation to make Slice 1 directly usable; do not pre-build the final AES UI.

Before any new reusable helper or internal dependency is added:
- record the required semantic boundary;
- check whether a stable platform/off-the-shelf component already supplies it;
- treat internal repos as donors unless a positive runtime-provider decision is recorded;
- record the residual semantics that remain.

Before adding non-user-facing feasibility/infrastructure work:
- name the authentic Slice 1 boundary it protects;
- state the uncertainty/blocker being resolved;
- use the smallest discriminating probe;
- name the return path to Slice 1.

Before completion:
- execute the canonical external example through the actual user-facing entrypoint;
- execute both negative controls;
- perform Attention Checkpoint A1;
- characterize current implementation at the exact AES revision;
- recompute the initial gap ledger;
- update `wiki/index.md` from the resulting current/gap state.

## Explicit non-goals

- migrating `data-contracts` to the new repository layout;
- adding `wiki/index.md` or `.agentic/repo.yaml` to `data-contracts` in this plan;
- building a universal repository crawler, symbol index, code graph, characterization kernel, representation router, or final AES dashboard;
- creating a new schema language;
- adding repository-context resolution to ACA before evidence exists;
- making Code Map, Representation Router, Project Meta, old AES, current Inside-Success AES, or Fluid Governance runtime dependencies by default;
- replacing Company Planning, Enforced Planning, Project Meta, or existing AES implementations.

## Stop/replan conditions

Replan rather than forcing implementation if:

- ACA or the external landscape contains an equivalent provider under a different semantic identity;
- Data Contracts already owns a semantically matching neutral result contract;
- resolving `data-contracts` honestly requires repo-specific hardcoding rather than a bounded legacy adapter;
- the required context cannot be evidenced without mutating the external consumer;
- the smallest implementation expands into generalized indexing, orchestration, fleet rollout, broad characterization infrastructure, or a generalized representation framework;
- the first vertical cannot leave the intended reviewer with a useful directly inspectable context experience if work stops after it;
- D1 or another enabler grows without a concrete return path to Slice 1;
- stakeholder observation at A1 shows the interaction or outcome is materially low-value, in which case treat that as planning evidence rather than polishing around it.

## Closure claim

This plan may claim `DELIVERED` only when the external canonical example and required negative controls have been observed through the real entrypoint, the intended reviewer has directly used the human-observable surface, the automated and stakeholder evidence are retained separately, and fresh gap recomputation shows which originating gaps are actually closed or narrowed.
