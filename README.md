# Agentic Engineering System — Canonical

**This repository is the Agentic Engineering System** ([Decision 0011](docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md), 2026-09-26). `Inside-Success/agentic-engineering-system` is archived; the ideas worth borrowing from it are in [`research/synthesis/2026-09-26-inside-success-aes-harvest.md`](research/synthesis/2026-09-26-inside-success-aes-harvest.md), each with the consumer trigger that would bring it in. Next frontier: whygame5 realizes its runner and records the first value measure (Decision 0011, item 5).

## AES v0.2 (accepted, Decision 0010)

AES v0.2 is a small command-line tool, `aes`, that governs a software project
from its first commit: you write down the outcome and the success criteria in
`.aes/target.yaml`, every file under the project's governed roots must be
planned there (a pre-commit hook refuses anything else), evidence is recorded
by running the tests (`aes evidence record`) and stays bound to the exact
commit and files it exercised, and `aes status` shows on one screen which
criteria are supported, which evidence went stale, and the first open gap per
component. Target changes go through `aes plan prepare / validate / accept`.

- **Start here:** [`docs/greenfield/GETTING_STARTED.md`](docs/greenfield/GETTING_STARTED.md)
  — install, `aes init`, and the lifecycle on a new project.
- **Where things stand:** in a clone of this repository, install first —
  `python3 -m venv .venv && .venv/bin/python -m pip install -e .` (Python 3.11 or
  newer) — then run `aes status`, or `make aes`, which finds that `.venv` itself.
- **What is accepted, on what evidence, and what is not claimed:**
  [Decision 0010](docs/decisions/0010-greenfield-v0.2-accepted.md).
- **Accepted architecture:** [`docs/architecture/greenfield-v0.2/`](docs/architecture/greenfield-v0.2/README.md).
  The proposal lineage (`proposals/aes-v0.2-greenfield/`) is history, not authority.

**AES v0.2 governs this repository (2026-09-25).** `.aes/target.yaml` holds the Greenfield MVP target (outcome `OUT-GF-001`, criteria `SC-GF-001`..`009`) over the governed roots `src/agentic_engineering_system/` and `tests/greenfield/`; `.aes/observations/` holds the evidence and `.aes/plans/` the accepted plans. Run `aes status` (or `make aes`) for the current standing and the first open gap per component; the v0.2 proposal lineage is `proposals/aes-v0.2-greenfield/` and the user-facing start is `docs/greenfield/GETTING_STARTED.md`. The v0.1 material below is retained under Decision 0010's v0.1 disposition.

## v0.1 (retained)

The material below describes the v0.1 line (the convergence architecture, Plan
001's Repository Context provider `aes-repo-context`, and Plan 002). It is
retained, not superseded wholesale; Decision 0010 states which parts v0.2
supersedes for its governed roots.

This repository is the clean convergence and dogfood implementation of the Agentic Engineering System (AES) architecture.

Its purpose is to integrate separately evolved planning, capability, execution-governance, context, policy, evidence, and learning systems into one coherent engineering lifecycle without duplicating their authorities:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

### Status (v0.1)

**Bootstrap architecture adopted; Plan 001 / Repository Context Slice 1 is delivered at verified AES revision `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1`.**

The canonical architecture now includes the component-aligned planning/governance model, AES-local Company Planning profile, minimal architecture-realization schema, and reserved component/verification homes. Reserved homes remain topology only; they are not implementation or verification evidence.

This branch contains the first Repository Context implementation: typed artifact models, exact Git/revision resolution, authoritative pilot-manifest handling, bounded legacy resolution, static HTML/JSON projection, CLI entrypoint, and focused tests.

The first direct A1 returned `change`, causing a bounded projection correction rather than a broader UI/platform build. On 2026-09-22, AES `96fcf5e89ba98ad9ff278ec536a98c308cda3fe1` then passed a fresh exact-revision technical batch against the pinned private `data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` consumer: **15 repository-context tests passed**, the real CLI returned `RESOLVED`, and the verification-batch check remained valid on a clean repository. The exact corrected HTML then received stakeholder response **"proceed"**, recorded as A1 `continue`.

The final revision-bound characterization and conservatively recomputed gap ledger are under `evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/` and `docs/architecture/INITIAL_GAP_LEDGER.md`. Plan 001 is therefore delivered for its bounded external Repository Context claim. This does not establish full AES maturity.

**Current planned frontier:** [Plan 002 — Offline Policy-Decision Replay](docs/plans/002_offline_policy_decision_replay.md). It asks one bounded question: whether a contextual model evaluator adds enough value over the existing deterministic completion/verification control to merit later **shadow-only** use. Four authentic historical cases are frozen as the exploratory starting set. The remaining P0 gate is authenticated OpenRouter access, one explicit compatible model ID, and one structured-output protocol smoke; then V1 runs the first offline comparison. No live policy behavior, hook, warning, or enforcement change is authorized by the plan.

Start at [`wiki/index.md`](wiki/index.md).

### Adopted project-agnostic architecture

This repo adopts the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`, starting at `docs/architecture/README.md` there.

The local repo owns only AES-specific intent, decisions, plans, evidence, and implementation. It must not copy the project-agnostic methodology into a second mutable authority.

### Lineage

`Inside-Success/agentic-engineering-system` and the archived `BrianMills2718/aes` are incumbent/predecessor sources of mechanisms, decisions, evidence, and lessons. They are not implicitly copied here. Existing capability owners remain authoritative until an explicit evidence-backed disposition says otherwise.
