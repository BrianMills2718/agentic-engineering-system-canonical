# Agentic Engineering System — Canonical

This repository is the clean convergence and dogfood implementation of the Agentic Engineering System (AES) architecture.

Its purpose is to integrate separately evolved planning, capability, execution-governance, context, policy, evidence, and learning systems into one coherent engineering lifecycle without duplicating their authorities:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

## Status

**Bootstrap architecture adopted; Plan 001 / Slice 1 is implementation-partial and not delivered.**

The canonical architecture now includes the component-aligned planning/governance model, AES-local Company Planning profile, minimal architecture-realization schema, and reserved component/verification homes. Reserved homes remain topology only; they are not implementation or verification evidence.

This branch contains the first Repository Context implementation: typed artifact models, exact Git/revision resolution, authoritative pilot-manifest handling, bounded legacy resolution, static HTML/JSON projection, CLI entrypoint, and focused tests.

Authentic technical execution has been observed on prior exact revisions, including the governed-repo audit, focused tests, exact pinned `data-contracts` check, real CLI execution, and deterministic generated artifacts. The first direct A1 returned `change` because the human-facing surface required too much reconstruction. A bounded projection correction followed; follow-up utility review, fresh revision-bound characterization, and explicit gap recomputation remain pending.

A completed implementation plan, passing regression suite, or useful presentation does not by itself establish delivery or close the originating gaps.

Start at [`wiki/index.md`](wiki/index.md).

## Adopted project-agnostic architecture

This repo adopts the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`, starting at `docs/architecture/README.md` there.

The local repo owns only AES-specific intent, decisions, plans, evidence, and implementation. It must not copy the project-agnostic methodology into a second mutable authority.

## Lineage

`Inside-Success/agentic-engineering-system` and the archived `BrianMills2718/aes` are incumbent/predecessor sources of mechanisms, decisions, evidence, and lessons. They are not implicitly copied here. Existing capability owners remain authoritative until an explicit evidence-backed disposition says otherwise.
