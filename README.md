# Agentic Engineering System — Canonical

This repository is the clean convergence and dogfood implementation of the Agentic Engineering System (AES) architecture.

Its purpose is to integrate a set of separately evolved systems into one coherent engineering lifecycle without duplicating their authorities:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

## Status

**Bootstrap architecture established; first implementation vertical remains separate.**

The canonical architecture now includes the component-aligned planning/governance model, AES-local Company Planning profile, minimal architecture-realization schema, and reserved component/verification homes. Reserved homes are topology only; they are not implementation or verification evidence.

Plan 001 / Repository Context implementation exists on the separate `slice-1/repository-context` line (PR #5) and is not part of this branch/main until separately reviewed and merged. Its technical execution evidence and first A1=`change` observation do not by themselves establish delivery or gap closure.

Start at [`wiki/index.md`](wiki/index.md).

## Adopted project-agnostic architecture

This repo adopts the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`, starting at `docs/architecture/README.md` there.

The local repo owns only AES-specific intent, decisions, plans, evidence, and implementation. It must not copy the project-agnostic methodology into a second mutable authority.

## Lineage

`Inside-Success/agentic-engineering-system` and the archived `BrianMills2718/aes` are incumbent/predecessor sources of mechanisms, decisions, evidence, and lessons. They are not implicitly copied here. Existing capability owners remain authoritative until an explicit evidence-backed disposition says otherwise.
