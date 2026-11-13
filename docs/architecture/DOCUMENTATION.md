---
description: How AES separates document authority and lifecycle from the views used to read it
status: current
---

# Documentation: authorities and reading views

AES keeps each fact with its owning source and presents related facts together for a reader. A research finding, an accepted requirement, a plan and an execution receipt can concern the same feature without becoming interchangeable kinds of truth. This page reconciles existing architecture and decisions; it introduces no new document schema or enforcement.

Source: the methodology adopted in [.agentic/repo.yaml](../../.agentic/repo.yaml), specifically [documentation architecture](https://github.com/BrianMills2718/wiki_methodology/blob/0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe/docs/architecture/AGENTIC_CODING_DOCUMENTATION_ARCHITECTURE.md) and [concern-root vocabulary](https://github.com/BrianMills2718/wiki_methodology/blob/0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe/docs/architecture/REPOSITORY_CONCERN_ROOTS.md); AES [Decision 0004](../decisions/0004-compact-structured-normative-records-and-generated-views.md) and Brian's accepted [Decision 0013](../decisions/0013-truth-lives-where-it-is-edited.md).

## Which source owns what?

| Kind | Authority and lifecycle | Editing rule in AES |
| --- | --- | --- |
| Normative architecture and required behavior | What should be true; changed through an explicit design or requirement change | Architecture belongs in `docs/architecture/`; current required behavior belongs in `openspec/specs/`. Change those sources rather than inferring requirements from code. |
| Research | Sources, bounded investigations and reusable synthesis inform choices; findings do not become requirements by being cited | Preserve source provenance and uncertainty. Promote accepted conclusions through the owning requirement or decision. Historical research may be linked at its retained revision. |
| Decisions | Accepted choices, rationale and supersession | Keep the original choice attributable; record a replacement or amendment explicitly in `docs/decisions/`. |
| Proposals and plans | A proposal is non-binding until adopted; a plan owns bounded change, not timeless product truth | Current behavior changes use OpenSpec proposals and tasks. Planning-package documents describe their own scope. Do not revive retired `docs/plans/` or `.aes/target.yaml` as AES's workflow. |
| Evidence | What was observed at a particular revision, time and environment | Retain the observation and its provenance; revise the interpretation separately. Passing a test does not redefine intended behavior. Keep private evidence in its governed private store. |
| Generated material | Rebuildable output from named inputs; never an independent authority | Edit the inputs and regenerate. Identify the source and generator. A generated file need not physically live under `generated/`—`AGENTS.md` is an example. |
| Wiki | Derived navigation and synthesis across sources | Organize a reading path around the reader's concern; link native authorities and preserve uncertainty. Do not add a competing editable copy of a source-owned fact. |
| PRD and other conventional views | Decision 0004's design treats a PRD as a view of goals, actors, outcomes, journeys and requirements | That is the historical structured-record target, not a claim that a complete PRD generator or universal record schema operates today. Use the actual declared sources; do not invent a second PRD authority. |

The upstream concern-root vocabulary is explicitly a **candidate**, not a frozen mandate to create every folder. Its categories distinguish ownership, authority and lifecycle. Native code, typed contracts and tool configuration retain their native homes. AES's repository declaration records routing, but some older provider and implementation fields still describe retired work; use the [retirement record](../retired/2026-11-12.md) when interpreting them.

## What belongs in a wiki summary?

A reader investigating one concern should be able to move from its intended behavior to current evidence, remaining gap and next action without mentally joining unrelated document silos. The adopted architecture calls this a concern view: target, success criteria, current state, gap, plan, implementation and verification. Those are reading dimensions, not permission to merge their authorities.

Brian's [Decision 0013](../decisions/0013-truth-lives-where-it-is-edited.md) sharpens the editing boundary: a document's description belongs in that document; a code description belongs in its docstring. Catalogs and wiki views displaying those facts take them from that source. Rules applying to many artifacts remain authored once, with source-local projections where implemented. A hand-written description kept only in a remote wiki page cannot reliably follow edits to its subject.

Cross-source synthesis still helps readers understand relationships and conflicts. It should explain those relationships with links, rather than silently owning facts that belong elsewhere. This wiki is a navigation layer; its existence does not prove all summaries are generated or fresh. Current projection work is described on [Lockstep's page](../../wiki/lockstep.md); the old docstring-wiki generator was [retired](../retired/2026-11-12.md).

## Current workflow versus historical design

Decision 0004 proposed compact system/component records with generated conventional documents and an explicit single-authority migration. It expressly left accepted Markdown authoritative until a separate cutover. Decision 0010 carried those principles into the historical v0.2 line; AES subsequently retired its own `.aes/` governance. Current [repository instructions](../../CLAUDE.md) use OpenSpec for required behavior, and [.agentic/repo.yaml](../../.agentic/repo.yaml) names that requirements source. Do not interpret the old record design as a replacement for today's OpenSpec files.

Unresolved documentation and realization gaps belong in the [open-questions ledger](../../wiki/open-questions.md), rather than being hidden by a polished navigation page.
