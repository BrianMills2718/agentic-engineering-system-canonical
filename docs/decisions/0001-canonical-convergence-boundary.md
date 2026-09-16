---
doc_role: active_authority
authority: canonical
status: accepted
accepted_by: Brian Mills
date: 2026-09-16
---

# Decision 0001 — Canonical AES convergence boundary

## Context

Several strong pieces of the intended Agentic Engineering System evolved separately: wiki/context and derived documentation, target/current/gap reconciliation, Company Planning, Enforced Planning, Agentic Capability Architecture, Data Contracts, Project Meta policy machinery, and multiple AES lineages.

The existing `Inside-Success/agentic-engineering-system` contains valuable working mechanisms and evidence, but also multiple historical lineages, plans, and architectural assumptions. The goal is to prevent the clearer integrated architecture from becoming another layer inside that accumulated structure.

## Decision

1. `BrianMills2718/agentic-engineering-system-canonical` is the clean canonical convergence and dogfood implementation target for the newly reconciled AES architecture.
2. The project-agnostic architecture remains owned by `BrianMills2718/wiki_methodology`; this repo adopts it by exact revision and does not fork its meaning.
3. `Inside-Success/agentic-engineering-system`, archived `BrianMills2718/aes`, Project Meta, Company Planning, Enforced Planning, ACA, Data Contracts, and other incumbents are capability/evidence sources. None is copied wholesale or silently superseded.
4. Existing capability ownership remains in place until an explicit disposition backed by authentic evidence changes it.
5. Migration is capability-by-capability. Allowed dispositions are `reuse`, `extend`, `adapt`, `supersede`, `salvage`, `historical`, `not_applicable`, and `unresolved`.
6. No local implementation package is created until Company Planning derives the first target implementation/verification topology from explicit gaps and ACA resolves relevant incumbent capabilities.
7. The repository protocol is a pilot. Friction discovered while dogfooding is recorded as a proposal back to the owning methodology rather than hidden by ad hoc structure.
8. The first implementation proof crosses an authentic external-consumer boundary and traverses the complete AES loop, not merely an infrastructure mechanism.

## Consequences

- The repo may begin with substantial architecture/navigation and no implementation code.
- The first plan is intentionally absent at bootstrap; it must be generated from target/current gap disposition.
- Existing AES mechanisms are candidates, not defaults. They can be reused when they satisfy the new architecture through their real seams.
- This repository is expected to change the standalone methodology when authentic dogfood reveals defects, through explicit proposals and accepted methodology revisions.
