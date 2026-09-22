# Agentic Engineering System — canonical development wiki

This is the progressive-disclosure front door for the canonical AES convergence project. It is a derived navigation surface, not a native authority. Follow links to the owning architecture, decision, plan, evidence, or code before making consequential claims.

## Current orientation

**Target**

One coherent human+agent engineering lifecycle:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

The lifecycle preserves native authority, honest unknown/error states, direct stakeholder utility evidence, and fresh post-implementation characterization rather than equating plan completion with conformance.

**Current**

The component-aligned bootstrap architecture is adopted, and this branch has been refreshed onto that architecture.

- Decisions 0001–0008 define the convergence boundary, Company Planning profile strategy, component/context rules, compact normative-record direction, consequential-seam typing, minimal architecture-realization contract, and the corrected provider-independent verification boundary.
- All twelve bootstrap AQRs are resolved to explicit decisions.
- Existing accepted Markdown remains normative authority until an explicit single-authority migration.
- Generated bootstrap projections remain non-authoritative dogfood/probe artifacts.
- Reserved component/test homes remain topology only.

Plan 001 / Repository Context is **implementation partial** on this branch. D1 is closed. The branch contains the repository-context package, CLI, exact Git/revision adapter, authoritative pilot-manifest and bounded-legacy resolution, typed artifact, deterministic JSON/static HTML projection, focused tests, and installed execution-governance machinery.

Authentic technical execution has been observed on prior exact revisions: governed-repo audit, focused checks, exact pinned external-consumer check, real CLI run, and deterministic artifacts. The first direct stakeholder A1 returned `change` because the HTML required too much reconstruction. A bounded projection-only correction followed.

No delivery or gap-closure claim has been made.

**Gap**

Post-integration characterization and the initial gap-ledger recomputation now exist for canonical `main@320991b96a3e3aaa15aa8ba05817a7eee1c52603`.

Before Plan 001 can be treated as delivered:

- run the repaired focused suite, pinned private `data-contracts` test, and real CLI locally at one exact clean revision; Decision 0008 requires this because the current CLI/pinned path transitively executes the renderer changed after the earlier authentic run;
- bind that verification to the exact revision with the incumbent Enforced Planning verification-batch mechanism;
- keep hosted CI out of the acceptance path while funding is unavailable;
- directly review the corrected human-facing presentation through the separate Representation Router workstream;
- refresh characterization/gap state again only if those observations materially change current state.

**Next**

```text
run repaired focused + pinned-consumer + real CLI verification locally
        ↓
bind the verification command/result to the exact clean revision
        ↓
keep hosted CI optional/manual rather than an acceptance gate
        ↓
keep follow-up presentation work separate until a reviewable surface returns
        ↓
follow-up A1: directly use it and record continue | change | stop
        ↓
refresh characterization/gap state only if those observations materially change it
        ↓
perform final Plan 001 closure/reconciliation
        ↓
derive the next real component-specific design only from the resulting gap state
```

PR #5 was integrated into canonical `main` as implementation-partial under an explicit integration-readiness record; merge status is not delivery evidence.

## Modular product design in the engineering workflow

[Decision 0009](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md)
applies [AES-CAP-003 through AES-CAP-005](../docs/architecture/SYSTEM_BOUNDARY.md#aes-cap-003--established-modular-design-not-a-parallel-platform)
through the existing Company Planning profile and Enforced Planning workflow.
Adopt existing foundations, preserve cohesive reusable behavior, keep product
policy and adapters local, and verify actual product behavior and compatibility.
ACA's existing capabilities/evidence remain with their owners; no parallel ACA
platform or benchmark programme is required. This policy integration does not
close Plan 001 or change its verification/utility frontier.

## Read in this order

1. [`../docs/plans/001_repository_context_resolution_vertical.md`](../docs/plans/001_repository_context_resolution_vertical.md) — active Plan 001 execution contract, evidence state, A1, and stop/replan conditions.
2. [`../docs/architecture/SYSTEM_BOUNDARY.md`](../docs/architecture/SYSTEM_BOUNDARY.md) — canonical AES target clauses and subsystem boundaries.
3. [`../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md) — delivery, direct-use, uncertainty, feasibility, and attention-economics rules.
4. [`../docs/architecture/README.md`](../docs/architecture/README.md) — architecture navigation, authority boundaries, and machine-readable bootstrap entrypoints.
5. [`../docs/architecture/normative-component-alignment.bootstrap.yaml`](../docs/architecture/normative-component-alignment.bootstrap.yaml) — resolved bootstrap design record and next dogfood gate.
6. [`../docs/architecture/aes-company-planning-profile.bootstrap.yaml`](../docs/architecture/aes-company-planning-profile.bootstrap.yaml) — AES-local planning profile and reproducible bootstrap checks.
7. [`../docs/architecture/schemas/architecture-realization.bootstrap.schema.json`](../docs/architecture/schemas/architecture-realization.bootstrap.schema.json) — minimal architecture-realization contract.
8. [`../docs/architecture/INITIAL_GAP_LEDGER.md`](../docs/architecture/INITIAL_GAP_LEDGER.md) — originating target/current variance; do not close rows merely because implementation work completed.
9. [`../docs/decisions/0001-canonical-convergence-boundary.md`](../docs/decisions/0001-canonical-convergence-boundary.md) through [`../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md`](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md) — accepted architecture/verification decisions and rationale. Decision 0007 is superseded.

## Slice 1 in one picture

```text
exact repository revision
        ↓
bounded source/declaration observations
        ↓
authority + navigation resolution
        ↓
RepositoryContextArtifact
        ↓
context.json + source-bound human presentation
        ↓
direct stakeholder use
        ↓
fresh characterization + gap recomputation
```

First external consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`. The consumer remains read-only.

The surface must not invent a wiki, infer semantic authority from folder names, or collapse `NONE`, `ERROR`, or `UNRESOLVED` into success. Positive routing claims require evidence.

## Authority rules that matter most

- One mutable fact has one owning authority or is explicitly a derived projection.
- Planning proposes and structures change; it does not manufacture current state or close gaps.
- Existing providers remain authoritative until an evidence-backed disposition changes that.
- External standards/OSS/providers are considered before bespoke local implementations when they plausibly fit.
- Native typed contracts remain with their natural authorities.
- Component-local context may repeat normative wording only as a generated, source-identified projection.
- Structural validity is not provider conformance, runtime verification, stakeholder utility, or gap closure.
- A completed plan is not evidence that the target is satisfied.

## What remains intentionally separate

- **Hosted regression CI** — optional/manual convenience only; funding or runner availability is not conformance evidence.
- **Local/external execution** — first-class verification when fresh execution is required.
- **Historical execution reuse** — claim-specific only when the complete transitive executed subject and relevant environment assumptions remain adequate under Decision 0008.
- **Pinned external acceptance** — exact `data-contracts` checkout and real entrypoint behavior; current end-to-end acceptance requires one repaired fresh local run because the renderer changed after the earlier authentic execution.
- **Stakeholder utility** — direct use and `continue | change | stop`.
- **Gap closure** — fresh characterization plus target/current recomputation.

A green automated check cannot prove the surface is useful. A useful surface cannot excuse missing or failed technical evidence.

## Machine execution readiness

Machine execution has an explicit preflight so a missing chat tool is not misdiagnosed as a machine, network, or WSL failure.

For substantial machine-dependent AES work, prefer a ChatGPT Work task/session when that surface is available. Normal Chat remains suitable for research and GitHub-only work, but AES does not assume that a long-lived normal conversation will retain a custom Remote MCP toolset indefinitely.

In either surface, the agent must first verify that the current conversation exposes Remote MCP `devices_list`, `devices_ping`, and `process_start`. If `devices_list` itself is absent, stop machine-dependent work immediately and classify the state as `SESSION_TOOL_NOT_EXPOSED`; GitHub-only work may continue when appropriate. For required machine work, prefer a fresh Work task/session rather than repeatedly reconnecting an otherwise healthy connector; use a fresh normal chat as fallback when Work is unavailable.

If the tools are exposed, the agent must confirm the intended device is `execution_ready` with `devices_list`, then `devices_ping`, before filesystem/process operations. Only after a successful ping should the guarded WSL path be attempted.

Canonical details and the full failure taxonomy live in [`../CLAUDE.md`](../CLAUDE.md) under **Execution readiness preflight**.

## Provider and donor posture

- Company Planning — planning/design provider through the AES-local profile.
- Enforced Planning — execution-governance incumbent/provider.
- Agentic Capability Architecture — capability/provider-resolution incumbent.
- Data Contracts — shared typed-boundary authority where provider-neutral semantics fit; not automatically an AES runtime dependency.
- Representation Router — concern-specific working-surface provider/workstream for the follow-up presentation; no authority transfer implied.
- Backstage, TOSCA, SysML v2/KerML, Open Workflow Specification, OPA/Rego, W3C PROV, in-toto/SLSA, SCIP, Code Map, predecessor AES repositories, and other donors remain concern-specific references/candidates unless positively selected by a real design.

Nothing becomes a runtime dependency merely because it appears in research or can model part of AES.
