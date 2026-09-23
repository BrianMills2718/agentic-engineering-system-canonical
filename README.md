# Agentic Engineering System — Canonical

This repository is the clean convergence and dogfood implementation of the Agentic Engineering System (AES) architecture.

Its purpose is to integrate separately evolved planning, capability, execution-governance, context, policy, evidence, and learning systems into one coherent engineering lifecycle without duplicating their authorities:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

## Status

**Bootstrap architecture adopted; Plan 001 / Repository Context Slice 1 is delivered at verified AES revision `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1`.**

The canonical architecture now includes the component-aligned planning/governance model, AES-local Company Planning profile, minimal architecture-realization schema, and reserved component/verification homes. Reserved homes remain topology only; they are not implementation or verification evidence.

This branch contains the first Repository Context implementation: typed artifact models, exact Git/revision resolution, authoritative pilot-manifest handling, bounded legacy resolution, static HTML/JSON projection, CLI entrypoint, and focused tests.

The first direct A1 returned `change`, causing a bounded projection correction rather than a broader UI/platform build. On 2026-09-22, AES `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1` then passed a fresh exact-revision technical batch against the pinned private `data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` consumer: **15 repository-context tests passed**, the real CLI returned `RESOLVED`, and the verification-batch check remained valid on a clean repository. The exact corrected HTML then received stakeholder response **"proceed"**, recorded as A1 `continue`.

The final revision-bound characterization and conservatively recomputed gap ledger are under `evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/` and `docs/architecture/INITIAL_GAP_LEDGER.md`. Plan 001 is therefore delivered for its bounded external Repository Context claim. This does not establish full AES maturity.

**Current planned frontier:** [Plan 002 — Offline Policy-Decision Replay](docs/plans/002_offline_policy_decision_replay.md). It asks one bounded question: whether a typed contextual evaluator adds enough value over the existing deterministic completion/verification control to merit later **shadow-only** use. Four authentic historical cases are frozen as the exploratory starting set. The remaining P0 gate is authenticated TypeSafe/Jev model access and one protocol smoke; then V1 runs the first offline comparison. No live policy behavior, hook, warning, or enforcement change is authorized by the plan.

Start at [`wiki/index.md`](wiki/index.md).

## Adopted project-agnostic architecture

This repo adopts the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`, starting at `docs/architecture/README.md` there.

The local repo owns only AES-specific intent, decisions, plans, evidence, and implementation. It must not copy the project-agnostic methodology into a second mutable authority.

## Lineage

`Inside-Success/agentic-engineering-system` and the archived `BrianMills2718/aes` are incumbent/predecessor sources of mechanisms, decisions, evidence, and lessons. They are not implicitly copied here. Existing capability owners remain authoritative until an explicit evidence-backed disposition says otherwise.
