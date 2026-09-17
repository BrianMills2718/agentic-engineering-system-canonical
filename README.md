# Agentic Engineering System — Canonical

This repository is the clean convergence and dogfood implementation of the Agentic Engineering System (AES) architecture.

Its purpose is to integrate separately evolved planning, capability, execution-governance, context, policy, evidence, and learning systems into one coherent engineering lifecycle without duplicating their authorities:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

## Current development state

**Plan 001 / Slice 1 is implementation-partial, not delivered.**

D1 is closed. The `slice-1/repository-context` branch and PR #5 contain the first repository-context implementation: typed artifact models, exact Git/revision resolution, authoritative pilot-manifest handling, bounded legacy resolution, static HTML/JSON projection, CLI entrypoint, and focused automated tests.

The remaining boundary is evidence and direct use, not more architecture invention:

1. run the governed-repository install/audit in a real local checkout;
2. run the focused tests and the exact pinned `data-contracts` external-consumer check;
3. execute `aes-repo-context` against `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`;
4. directly use the generated HTML at Attention Checkpoint A1 and record `continue | change | stop`;
5. produce fresh revision-bound characterization and recompute the originating gaps.

Passing tests alone do not establish stakeholder utility, and positive stakeholder utility cannot override missing or failed technical evidence.

Start at [`wiki/index.md`](wiki/index.md).

## Adopted project-agnostic architecture

This repo adopts the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`, starting at `docs/architecture/README.md` there.

The local repo owns only AES-specific intent, decisions, plans, evidence, and implementation. It must not copy the project-agnostic methodology into a second mutable authority.

## Lineage

`Inside-Success/agentic-engineering-system` and the archived `BrianMills2718/aes` are incumbent/predecessor sources of mechanisms, decisions, evidence, and lessons. They are not implicitly copied here. Existing capability owners remain authoritative until an explicit evidence-backed disposition says otherwise.
