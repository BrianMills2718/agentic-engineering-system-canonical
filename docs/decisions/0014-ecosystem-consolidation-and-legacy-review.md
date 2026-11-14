---
description: AES owns ecosystem consolidation and a source-backed review of predecessor systems while preserving native capability owners
status: accepted
doc_role: active_authority
date: 2026-11-13
accepted_by: Brian Mills, current conversation approval
---

# Decision 0014: Consolidate ecosystem discovery through AES and review legacy sources

Governs: docs/architecture/ECOSYSTEM.md

## Source and intent

Source: Brian, 2026-11-13, described an index of data types, programs using them,
and capabilities so projects can find each other and exchange information, with
reuse the default and capability growing across projects. He then said:
"i approve and then i want to start going througha nd reading the old parts ofthe system and finding what is best and docuemtning them in aes canonical along wiht any open quesitons, concerns, incosnstencies, recommendations etc".

This adopts the consolidation direction and source review. The approval is not
an observation that catalogue cutover, runtime integration or legacy retirement
has happened.

## Decision

1. AES owns the consolidation design and the review of predecessor ideas. The
   actor is a person or coding agent finding and composing existing capabilities
   before implementing new behavior, then feeding new capabilities and evidence
   back into the ecosystem.
2. Provide one discovery route connecting semantic jobs, providers, versioned
   input/output contracts, consumers and evidence. Each fact has one authoritative
   source; multiple generated views may answer different questions.
3. Source-local provider metadata, schemas, product code, observations and
   operating custody retain their natural owners. AES integrates those sources;
   it does not become a universal code or schema store.
4. Review legacy sources for their meaning and evidence. Record best ideas,
   limitations, inconsistencies, proposed dispositions and unanswered questions
   in the [ecosystem review](../architecture/ECOSYSTEM.md). Use the existing
   [question ledger](../planning/open-questions.json) for unresolved work.
5. Existing use informs migration impact. It does not by itself justify keeping
   a feature; lack of current use does not erase a useful requirement or idea.
6. Implement consolidation in bounded stages after source reconciliation. A
   source is replaced only after its unique information, readers and update
   paths are accounted for and the replacement is demonstrated.

## Reconciliation with earlier decisions

[Decision 0012](0012-capability-reuse-enforced-at-plan-adoption.md) selected ACA
as the catalogue, while the later workspace
[Decision 0004](https://github.com/BrianMills2718/code2-workspace/blob/main/docs/decisions/0004-one-capabilities-list.md)
selected a workspace jobs/tools list. Project Meta has an older semantic catalog.
These records are evidence of incomplete consolidation, not three permissions to
maintain competing copies of the same fact. The selected publication/storage
mechanism and cross-repository instruction changes remain Q36; no source is
silently declared migrated by this decision. The workspace's current read-before-
build rule continues to apply while its future derived role is designed.

Decision 0013's source-local truth principle applies to capability metadata.
Decision 0009's stop on speculative standalone ACA machinery remains in force:
this work addresses the concrete discovery inconsistency and uses existing
providers wherever sufficient. Reviewing older experiments does not resume them.

## Success and disproof

A reader can start from one route, find a capability, inspect an exact provider
and its contract references, distinguish declared consumers from observed use,
and open supporting evidence. A provider change makes an outdated projection
visibly stale or refreshes it. A newly useful capability becomes discoverable
without copying its code into AES.

The direction fails if it creates another independently edited catalogue, loses
legacy information, hides unavailable providers, or requires universal packaging
or orchestration before an ordinary project can publish a useful capability.

## Implementation status

Documentation direction adopted; first bounded source review recorded.
Catalogue implementation, upstream instruction reconciliation, runtime rollout
and retirement are not completed by this documentation change.
