---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills (2026-09-22 integration instruction)
date: 2026-09-22
reversible: true
---

# Decision 0009 - Apply modular product design through AES

## Context and scope

Brian asked that ACA contribute to the Agentic Engineering System rather than
become a parallel research or infrastructure programme. At the inspected AES
baseline `996530de0d034687b49a1acb89d3261681eb6274`, AES-CAP-001/002 already
require capability resolution and external-first sourcing, but the workflow's
unqualified instruction to resolve behavior "through ACA" does not explain
how to apply modular design without starting another ACA experiment.

This is an authorized, documentation-only integration of that operating intent.
It is not a new implementation plan, framework selection, provider migration,
or claim that the incomplete Repository Context vertical is delivered.

## Decision

Apply [AES-CAP-003 through AES-CAP-005](../architecture/SYSTEM_BOUNDARY.md#aes-cap-003--established-modular-design-not-a-parallel-platform)
in the existing planning, implementation, and review workflow. The clauses,
not a new standalone checklist service, own the normative design guidance.

| Concern | Owner and disposition |
| --- | --- |
| Integrated engineering lifecycle and AES-local design policy | AES; extend existing capability clauses and operating instructions |
| Planning/design derivation | Company Planning; use the existing AES-local profile and referenced design packet, not a fork or new skill |
| Claims, execution governance, checks, verification batches | Enforced Planning; preserve its installed authority and mechanisms |
| Existing capability catalogue, implementations, provenance and reuse evidence | ACA and the relevant existing owners; consult real published boundaries, do not copy or silently retire them |
| Actual product behavior and reusable packages/services | Their natural product or module owner; not a universal AES/ACA code store |
| Project-agnostic methodology | `wiki_methodology` at the adopted revision; unchanged, with generic changes routed upstream |

The companion ACA update stops automatic continuation of its standalone
experiment agenda and points agents here for engineering workflow. It does not
archive the ACA repository, delete proofs, promote packages, or transfer
existing implementation ownership. Decisions 0001/0002 and AES-SYS-002/004
remain in force.

## How a normal task uses this

Use the existing design packet and review to answer: which sufficient existing
product/framework is selected; which native module/API boundary is consumed;
which cohesive behavior stays shared; which policies/dependencies actually
vary; what the consumer adapter and local residual own; and which product and
compatibility checks establish correct behavior. A small task can answer these
in a short design note. No additional mandatory form is introduced.

A useful example is keeping a collector's stable provider/error behavior
separate from a product's ranking policy. A digest may supply a recency policy
where a prospecting product supplies a prospect policy, but an adapter cannot
recover candidates already discarded by hidden prospect-specific truncation.
In that case change an appropriate owned seam, choose another boundary, or
keep the behavior local; do not invent a semantic translation platform.

Use established patterns where they solve those concrete boundaries, not a
pattern-count target. Framework-specific modules are legitimate. Dependency
closure and clean consumer-independent initialization matter more than
arbitrary portability or adapter line-count requirements.

## Delivery and evidence boundary

Ordinary product acceptance and compatibility checks continue. A/B studies
and demonstration products are not prerequisites for using modular architecture.
A new standalone experiment or ACA-specific mechanism needs separate explicit
authorization and a concrete product decision/blocker. Earlier narrow reuse
results remain evidence about their recorded cases, not a verdict on modularity.

This change makes the instructions and profile references consistent. It does
not demonstrate that every agent will follow them, that AES automatically
verifies architecture quality, or that Plan 001's utility and closure gaps are
resolved. Those require authentic product execution and existing verification.
