# Plan 001 — Repository context resolution vertical

Status: design-ready; implementation not started
Origin gaps: GAP-AES-001, 002, 003, 004, 005, 006, 007, 009, 010, 011, 013, 014, 015, 017, 019, 020
External consumer: `BrianMills2718/data-contracts`
Execution profile: pilot

## User outcome

An agent entering an unfamiliar governed repository can ask AES for the repository's current context and receive one inspectable artifact that identifies the correct navigation and authority surfaces without guessing from folder names, so the agent can deepen into the right native source before planning or editing.

## Canonical behavioral example

Starting state: current `data-contracts` repository.

Action: resolve its repository context through the first AES context-resolution seam.

Expected result: the artifact must, at minimum:

1. identify `data-contracts` as the target repository and bind the observation to an exact revision;
2. report the current local navigation situation honestly rather than inventing `wiki/index.md` when absent;
3. identify `src/data_contracts/` as a native implementation and typed-contract authority surface;
4. distinguish the root `contracts/` directory from the repository's general contract authority;
5. route contract-ownership questions to the repository's native capability-decomposition authority;
6. preserve explicit `NONE`/unknown states for undeclared surfaces rather than treating absence as success;
7. retain source/evidence references sufficient to explain every resolved routing claim.

A result that says simply `contracts/ is the contract root`, claims a wiki entrypoint that does not exist, or silently infers missing declarations is a failure.

## Why this vertical

This is the smallest external-consumer slice that simultaneously exercises the new repository protocol, progressive-disclosure philosophy, Data Contracts boundary lesson, honest unknown-state policy, evidence binding, and ACA residual-capability process.

It does not require `data-contracts` to migrate its repository layout. The consumer remains an authentic external source whose existing authorities must be respected.

## Modality

Hybrid.

Deductive/plan-first:
- artifact schema and authority semantics;
- exact-revision binding;
- no-guessing / no-false-green rules;
- explicit native-surface declarations when available.

Exploratory:
- how much legacy repository context can be resolved safely when `.agentic/repo.yaml` is absent;
- which evidence/source adapters are sufficient without creating a generalized crawler.

## Capability requirement

Provisional semantic action: `repository.context.resolve`.

ACA discovery on 2026-09-16 found no current verified semantic export matching this behavior. The required action is therefore a residual capability requirement for this vertical. The plan does not grant it ecosystem-level capability status.

Disposition: `residual_local_candidate` pending implementation and evidence.

If a suitable provider is discovered before implementation begins, replace this disposition with `reuse`, `configure`, `compose`, or `extend` and record the provider binding.

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

Before creating an AES-local contract, inspect Data Contracts for an existing neutral contract that honestly represents this boundary. Reuse or extend it when semantics match. Do not add a generic contract merely because Data Contracts exists.

## Planned implementation topology

Not yet frozen to concrete files.

Company Planning output establishes these first-class subjects conceptually:

- **RepositoryContextResolver** — orchestration boundary for resolving one repository at one revision.
- **RepositoryContextArtifact** — typed, immutable result consumed by agent/context projections.
- **AuthoritySurfaceObservation** — evidence-backed observation of one native authority/navigation surface.
- **LegacyRepositoryAdapter** — bounded adapter for repositories without the pilot `.agentic/repo.yaml`; it may report unknown, but may not fabricate declarations.
- **PilotManifestAdapter** — reader for `.agentic/repo.yaml` when present.

The implementation root and exact file paths remain unresolved until the contract check and final incumbent search are complete.

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

Negative controls AC-006 and AC-007 must be observed before the resolver is described as evidenced.

## Policy triggers carried by the plan

Before implementation:
- verify ACA discovery result is still current;
- inspect Data Contracts for a suitable neutral typed boundary;
- freeze the exact `data-contracts` revision used by AC-001 through AC-005.

Before any new reusable helper is added:
- record why it is residual rather than supplied by an incumbent.

Before completion:
- execute the canonical external example through the actual user-facing entrypoint;
- execute both negative controls;
- characterize current implementation at the exact AES revision;
- recompute the initial gap ledger;
- update `wiki/index.md` from the resulting current/gap state.

## Explicit non-goals

- migrating `data-contracts` to the new repository layout;
- adding `wiki/index.md` or `.agentic/repo.yaml` to `data-contracts` in this plan;
- building a universal repository crawler;
- creating a new schema language;
- adding repository-context resolution to ACA before evidence exists;
- replacing Company Planning, Enforced Planning, Project Meta, or existing AES implementations.

## Stop/replan conditions

Replan rather than forcing implementation if:

- ACA already contains an equivalent verified action under a different semantic identity;
- Data Contracts already owns a semantically matching neutral result contract;
- resolving `data-contracts` honestly requires repo-specific hardcoding rather than a bounded legacy adapter;
- the required context cannot be evidenced without mutating the external consumer;
- the smallest implementation expands into generalized indexing, orchestration, or fleet rollout.

## Closure claim

This plan may claim `DELIVERED` only when the external canonical example and required negative controls have been observed through the real entrypoint, the evidence is retained, and fresh gap recomputation shows which originating gaps are actually closed or narrowed.