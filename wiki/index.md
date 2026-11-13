---
type: Index
title: AES canonical wiki
description: Navigate AES purpose, Lockstep planning and two-way projection, documentation roles, feedback, policy and evidence
status: current
last_checked: 2026-11-13
---

# Agentic Engineering System (AES)

## What AES is now

AES helps autonomous coding agents deliver software that stays true to its intent.
It combines **Lockstep**, the **feedback loop** and the **policy layer**.
Read the [owning goal and thesis](../docs/architecture/GOAL.md) for the full account.

Lockstep starts with planned behavioral units, file structure, typed interfaces and
tests. Requirements flow into code docstrings; implementation status flows back
into the documents. Source-local normative edits have an explicit change path.
This wiki provides concise navigation to those sources. These are the intended
relationships; [implementation limits](../docs/architecture/LOCKSTEP.md#current-mechanisms-and-their-limits)
and [open concerns](open-questions.md) remain visible.

## Start from your question

| Question | Read next | Owning source |
| --- | --- | --- |
| What is AES for, and what is its architectural bet? | [Purpose](goal.md) | [Goal and thesis](../docs/architecture/GOAL.md) |
| How does Lockstep plan behavior, structure and tests, then project both ways? | [Lockstep](lockstep.md) | [Component contract and example](../docs/architecture/LOCKSTEP.md) |
| Which documents are normative, research, plans, evidence, generated output or PRDs? | [Document roles](../docs/architecture/DOCUMENTATION.md) | [Authority and lifecycle](../docs/architecture/DOCUMENTATION.md#which-source-owns-what) |
| Where do wiki summaries come from, and what refreshes them? | [Wiki and source ownership](../docs/architecture/DOCUMENTATION.md#what-belongs-in-a-wiki-summary) | [Declared facts contract](../openspec/specs/lockstep-doc-facts/spec.md) |
| How should corrections become verified improvements? | [Feedback loop](feedback-loop.md) | [Feedback and policy contract](../docs/architecture/FEEDBACK_AND_POLICY.md) |
| Where are rules, their sources and their enforcement? | [Policy](policy-and-rules.md) | [Rules register](../docs/rules/register.yaml) |
| What is implemented, observed, unresolved or historical? | [Current state](../.project-brain/now.md) | [Discussion ledger](open-questions.md) |
| What are the detailed requirements? | [Requirement navigation](requirements.md) | [System clauses](../docs/architecture/SYSTEM_BOUNDARY.md) and [Lockstep behavior spec](../openspec/specs/lockstep-plan-format/spec.md) |
| Where are code, data and external boundaries? | [System model](system-model.md) | [Whole-system inventory](../docs/planning/SYSTEM_MODEL.md) |
| How do I install, check and operate it? | [Commands](run-and-deploy.md) | [README](../README.md) and [feedback operator guide](../scripts/learning_loop/systemd/README.md) |
| What does a term mean? | [Glossary](glossary.md) | [Domain model](../docs/planning/DOMAIN.md) |
| Which older designs and choices were retained or retired? | [History](history.md) | [Retirement record](../docs/retired/2026-11-12.md) |
| What prior research informed it? | [Research and lessons](research-and-lessons.md) | The retained source revisions linked on that page |

## How to read this wiki

This is navigation and source-linked synthesis, not another normative authority.
The pages combine related intent, implementation and evidence so a reader can
follow one concern. Individual document descriptions belong in those documents;
module descriptions belong in docstrings. Declared fact copies can be refreshed
by Lockstep. Curated page explanations and website builds are separate; this wiki
does not claim every paragraph is already generated or continuously updated.
See [documentation ownership and current mechanisms](../docs/architecture/DOCUMENTATION.md).

The [discussion ledger](open-questions.md) records questions, recommendations and
concerns found during the documentation repair. A historical PASS, a shipped
component or an active timer does not settle those questions.

## Full document catalog

[Documents by folder](documents.md) links every reader document from this page in
two hops, including detailed specifications and retained records. The short routes
above are the recommended orientation; the catalog is the coverage backstop.

## Decision record

This repository's decisions; code2-workspace decision 0009 (AES and Lockstep fate) is a different decision ([docs/decisions/0009-aes-and-lockstep-fate.md:27-28](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L27-L28)), summarised on [lockstep.md](lockstep.md).

- [0001](../docs/decisions/0001-canonical-convergence-boundary.md): clean canonical repository and convergence boundary (2026-09-16).
- [0002](../docs/decisions/0002-company-planning-aes-profile-before-fork.md): an AES profile over Company Planning before any fork (2026-09-17).
- [0003](../docs/decisions/0003-component-local-normative-context-and-symbol-inheritance.md): component-local normative context, symbols inherit scope (2026-09-17).
- [0004](../docs/decisions/0004-compact-structured-normative-records-and-generated-views.md): compact structured normative records with generated views (2026-09-17).
- [0005](../docs/decisions/0005-aes-component-scope-and-consequential-seam-typing.md): component is a governance scope; type only consequential seams (2026-09-17).
- [0006](../docs/decisions/0006-minimal-architecture-realization-json-schema.md): minimal architecture-realization JSON Schema (2026-09-17).
- [0007](../docs/decisions/0007-provider-independent-verification-and-blob-evidence-carry-forward.md): blob-level evidence carry-forward, superseded by 0008 (2026-09-18).
- [0008](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md): provider-independent verification over the transitive executed subject (2026-09-18).
- [0009](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md): modular product design without a parallel ACA platform (2026-09-22).
- [0010](../docs/decisions/0010-greenfield-v0.2-accepted.md): AES v0.2 greenfield MVP accepted as realized (2026-09-25), now history.
- [0011](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md): this repository is AES; the Inside Success repository is archived (2026-09-26).
- [0012](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md): capability reuse checked against one catalogue (2026-10-08).
- [0013](../docs/decisions/0013-truth-lives-where-it-is-edited.md): truth lives where it is edited (2026-10-10).

Where each earlier decision stands now:

- 0001 items 3 (incumbents as capability sources with retained ownership) and 6 (no local package until Company Planning derives topology) are superseded for the v0.2 governed roots by 0010 ([docs/decisions/0010-greenfield-v0.2-accepted.md:141-143](../docs/decisions/0010-greenfield-v0.2-accepted.md#L141-L143)). The rest of 0001 is the v0.1 line's history.
- 0002 is superseded as the planning route for that scope ([docs/decisions/0010-greenfield-v0.2-accepted.md:144-145](../docs/decisions/0010-greenfield-v0.2-accepted.md#L144-L145)).
- 0003 to 0006 and 0008 were carried forward into v0.2 under new names and are history with it; 0007 was already superseded by 0008 ([docs/decisions/0010-greenfield-v0.2-accepted.md:150-151](../docs/decisions/0010-greenfield-v0.2-accepted.md#L150-L151)).
- 0009 (local): its modular-design guidance (AES-CAP-003 to 005) stands; its rows giving Company Planning and Enforced Planning ownership were superseded for v0.2 ([docs/decisions/0010-greenfield-v0.2-accepted.md:146-148](../docs/decisions/0010-greenfield-v0.2-accepted.md#L146-L148)).
- 0011 is current on identity. Its condition for resuming the Inside Success rollout is met, but whether to resume is Brian's call and has not been made ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:79-81](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L79-L81)).
