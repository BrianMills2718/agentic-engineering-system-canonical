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

The component-aligned bootstrap architecture is adopted. Plan 001 / Repository Context is **DELIVERED for its bounded external-consumer Slice 1 claim**.

- Decisions 0001–0009 define the convergence boundary, planning/profile strategy, provider-independent verification, and the current modular product-design posture.
- At AES `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1`, a fresh exact-revision verification batch against `data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` reported **15 passed**, real CLI `RESOLVED`, and a valid post-run batch on a clean repository.
- The first A1 utility observation was `change`; that evidence caused a bounded projection correction rather than a new UI/platform build.
- The exact corrected surface from the fresh bound run then received stakeholder response **"proceed"**, recorded as A1 `continue`.
- Final characterization and gap recomputation preserve remaining broader AES gaps rather than treating this one delivered vertical as full-system maturity.

**Gap**

No Plan 001 closure gate remains. Remaining gaps are broader system-maturation questions such as repeated authority-preserving composition, prospective planning/execution custody, generalized policy/context delivery, and more mechanical current-state projection. They are explicitly deferred or narrowed in `docs/architecture/INITIAL_GAP_LEDGER.md`; they are not a reason to invent a next implementation project.

**Next**

Execution coordination for this existing frontier is tracked in [Issue #17](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/17); the plan and architecture documents remain authoritative.

```text
start from the freshly recomputed remaining gap state
        ↓
name one concrete human/product outcome
        ↓
derive the next component-specific design through Company Planning
        ↓
apply provider sourcing + ACA evidence through the normal AES workflow
        ↓
execute through Enforced Planning
```

No next implementation vertical is authorized merely because Plan 001 closed. Historical research or ACA experiments are not fallback work queues.

## Modular product design in the engineering workflow

[Decision 0009](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md)
applies [AES-CAP-003 through AES-CAP-005](../docs/architecture/SYSTEM_BOUNDARY.md#aes-cap-003--established-modular-design-not-a-parallel-platform)
through the existing Company Planning profile and Enforced Planning workflow.
Adopt existing foundations, preserve cohesive reusable behavior, keep product
policy and adapters local, and verify actual product behavior and compatibility.
ACA's existing capabilities/evidence remain with their owners; no parallel ACA
platform or benchmark programme is required. Plan 001 is now closed by separate
exact verification, utility, characterization, and gap-reconciliation evidence.

## Read in this order

1. [`../docs/plans/001_repository_context_resolution_vertical.md`](../docs/plans/001_repository_context_resolution_vertical.md) — completed Plan 001 record, exact evidence state, A1 history, and closure decision.
2. [`../docs/architecture/SYSTEM_BOUNDARY.md`](../docs/architecture/SYSTEM_BOUNDARY.md) — canonical AES target clauses and subsystem boundaries.
3. [`../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md) — delivery, direct-use, uncertainty, feasibility, and attention-economics rules.
4. [`../docs/architecture/README.md`](../docs/architecture/README.md) — architecture navigation, authority boundaries, and machine-readable bootstrap entrypoints.
5. [`../docs/architecture/normative-component-alignment.bootstrap.yaml`](../docs/architecture/normative-component-alignment.bootstrap.yaml) — resolved bootstrap design record and next dogfood gate.
6. [`../docs/architecture/aes-company-planning-profile.bootstrap.yaml`](../docs/architecture/aes-company-planning-profile.bootstrap.yaml) — AES-local planning profile and reproducible bootstrap checks.
7. [`../docs/architecture/schemas/architecture-realization.bootstrap.schema.json`](../docs/architecture/schemas/architecture-realization.bootstrap.schema.json) — minimal architecture-realization contract.
8. [`../docs/architecture/INITIAL_GAP_LEDGER.md`](../docs/architecture/INITIAL_GAP_LEDGER.md) — originating target/current variance; do not close rows merely because implementation work completed.
9. [`../docs/decisions/`](../docs/decisions/) — accepted architecture/verification decisions, including Decision 0009's modular product-design integration. Decision 0007 is superseded by Decision 0008.

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
