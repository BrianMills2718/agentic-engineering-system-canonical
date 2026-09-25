# Agentic Engineering System — canonical development wiki

This is the progressive-disclosure front door for the canonical AES convergence project. It is a derived navigation surface, not a native authority. Follow links to the owning architecture, decision, plan, evidence, or code before making consequential claims.

## AES v0.2 (accepted) — start here

AES v0.2, the greenfield MVP, is accepted as realized by
[Decision 0010](../docs/decisions/0010-greenfield-v0.2-accepted.md) and governs
this repository's `src/agentic_engineering_system/` and `tests/greenfield/`
through its own `.aes/` target.

- Use it: [`docs/greenfield/GETTING_STARTED.md`](../docs/greenfield/GETTING_STARTED.md).
- Current state: run `aes status` (or `make aes`); the live authority is `.aes/target.yaml`.
- Accepted architecture: [`docs/architecture/greenfield-v0.2/`](../docs/architecture/greenfield-v0.2/README.md).
- What is not claimed (value beyond mechanism, single machine, two consumers, private repository) and the one criterion not currently supported (SC-GF-001, waiting on clean-user run 3): Decision 0010.
- History: [`proposals/aes-v0.2-greenfield/`](../proposals/aes-v0.2-greenfield/README.md) (lineage, not authority), especially `24-pre-probe-decisions.md` and `25-roadmap-to-mvp-acceptance.md`.

Everything below describes the v0.1 line, retained under Decision 0010's v0.1 disposition.

## Current orientation (v0.1)

**Target**

One coherent human+agent engineering lifecycle:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

The lifecycle preserves native authority, honest unknown/error states, direct stakeholder utility evidence, and fresh post-implementation characterization rather than equating plan completion with conformance.

**Current**

The component-aligned bootstrap architecture is adopted. Plan 001 / Repository Context is **DELIVERED for its bounded external-consumer Slice 1 claim**. [Plan 002 — Offline Policy-Decision Replay](../docs/plans/002_offline_policy_decision_replay.md) is the active **planned** vertical; it has not changed live policy behavior.

- Decisions 0001–0009 define the convergence boundary, planning/profile strategy, provider-independent verification, and modular product-design posture.
- Plan 001 closed with exact technical evidence and follow-up A1 `continue`; its final evidence remains under `evidence/plan-001/`.
- Plan 002 retains Enforced Planning as the deterministic completion/verification authority and treats an explicit OpenRouter model only as a candidate typed evaluator behind a replaceable adapter.
- The first Plan 002 decision is deliberately offline: compare one authentic event-time completion/verification decision against the incumbent control, produce a source-linked report, and decide whether OpenRouter model deserves a small shadow-only evaluation.
- No live hooks, warnings, enforcement, context ranking, policy self-modification, or broad observability platform are authorized by Plan 002.

**Gap**

Plan 001 leaves broader AES policy/evidence maturation deliberately unresolved. The selected Plan 002 outcome addresses only one bounded uncertainty: **whether contextual typed judgment adds decision value over an existing exact control on authentic AES completion/verification cases**. Provider availability, authentic replay-case custody, actual AES latency/cost, and disagreement quality remain unobserved.

**Next**

Execution coordination: [Issue #20](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/20). The Plan 002 document remains the authority for scope, stop rules, and acceptance.

```text
4 authentic completion/verification cases frozen
        +
confirm authenticated OpenRouter access + one explicit compatible model
        ↓
protocol-only structured-output smoke
        ↓
freeze first V1 case + event-time context contract
        ↓
V1: replay one authentic case offline
incumbent deterministic decision + OpenRouter model typed judgment
        ↓
render source-linked JSON/static HTML
        ↓
direct operator review: continue | change | stop
        ↓
V2: small frozen authentic case set
        ↓
provider disposition: adopt-for-shadow | revise | reject
```

P0's remaining real stop gate is OpenRouter model provider access. The four authentic cases are sufficient for this exploratory slice; they are not a generalization claim. If OpenRouter model access is unavailable, preserve that evidence and do not build a substitute policy platform. Historical ACA experiments and the broad OpenRouter model proposal PRs remain research donors, not fallback execution queues.

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

1. [`../docs/plans/002_offline_policy_decision_replay.md`](../docs/plans/002_offline_policy_decision_replay.md) — active planned vertical, P0 blockers, offline replay boundary, provider decision, and stop rules.
2. [`../docs/plans/001_repository_context_resolution_vertical.md`](../docs/plans/001_repository_context_resolution_vertical.md) — completed Plan 001 record and first-loop evidence.
3. [`../docs/architecture/SYSTEM_BOUNDARY.md`](../docs/architecture/SYSTEM_BOUNDARY.md) — canonical AES target clauses and subsystem boundaries.
4. [`../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md) — delivery, direct-use, uncertainty, feasibility, and attention-economics rules.
5. [`../docs/architecture/README.md`](../docs/architecture/README.md) — architecture navigation, authority boundaries, and machine-readable bootstrap entrypoints.
6. [`../docs/architecture/normative-component-alignment.bootstrap.yaml`](../docs/architecture/normative-component-alignment.bootstrap.yaml) — resolved bootstrap design record and next dogfood gate.
7. [`../docs/architecture/aes-company-planning-profile.bootstrap.yaml`](../docs/architecture/aes-company-planning-profile.bootstrap.yaml) — AES-local planning profile and reproducible bootstrap checks.
8. [`../docs/architecture/schemas/architecture-realization.bootstrap.schema.json`](../docs/architecture/schemas/architecture-realization.bootstrap.schema.json) — minimal architecture-realization contract.
9. [`../docs/architecture/INITIAL_GAP_LEDGER.md`](../docs/architecture/INITIAL_GAP_LEDGER.md) — originating target/current variance; do not close rows merely because implementation work completed.
10. [`../docs/decisions/`](../docs/decisions/) — accepted architecture/verification decisions, including Decision 0009's modular product-design integration. Decision 0007 is superseded by Decision 0008.

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
- **Plan 001 pinned external acceptance** — complete at exact AES `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1` against the pinned `data-contracts` consumer; historical evidence stays revision-bound.
- **Plan 002 policy replay** — offline only until a separate future plan authorizes any live intervention.
- **Stakeholder utility** — direct use and explicit dispositions remain separate from automated verification/provider output.
- **Gap closure** — fresh characterization plus target/current recomputation; a provider comparison does not close a gap by itself.

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
