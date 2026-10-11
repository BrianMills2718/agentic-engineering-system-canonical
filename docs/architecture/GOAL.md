---
description: What the Agentic Engineering System is for, the bet behind it, what would disprove it, and the repository it replaces
---

# Agentic Engineering System: goal and thesis

## Introduction and Goals

### Requirements Overview

The requirements are the outcomes, normative items and success criteria (each with a
disproof) in [`.aes/target.yaml`](../../.aes/target.yaml): outcome `OUT-GF-001` (a new
project under AES governance, from intent to evidence-backed current/gap state) and
outcome `OUT-AP-001` (real work lands only under an adopted Company Planning plan;
trivial work is decided by measured facts). The rules that enforce them, with owners
and tests, are in the system model ([ODD.md](../model/ODD.md),
[trace.yaml](../model/trace.yaml)).

### Quality Goals

- Ignorance never renders green: a criterion without enough fresh evidence stays a
  gap ([AES-POL-002](SYSTEM_BOUNDARY.md#aes-pol-002--ignorance-cannot-render-green)).
- Every control can be shown to fail on a case it should refuse
  ([AES-POL-004](SYSTEM_BOUNDARY.md#aes-pol-004--controls-prove-they-can-fail)).
- Off-the-shelf first: AES adopts or configures existing tools before building its
  own ([AES-CAP-002](SYSTEM_BOUNDARY.md#aes-cap-002--external-first-provider-sourcing), Decision 0012).

### Stakeholders

- Brian, the planning authority for his repositories.
- Coding agents (Claude Code and Codex) that plan, implement and verify work under AES.
- A colleague starting a new project without access to Brian's private repositories
  (the `OUT-GF-001` actor).

## North star (AES extension)

From outcome `OUT-GF-001`: a colleague can start a genuinely new software project
under AES governance, move from accepted intent through planned realization and
implementation to evidence-backed current/gap state, and do so without access to
private historical repositories or undocumented AES lineage knowledge.

## Thesis (AES extension)

Agent-built software stays true to its intent when every claim about it is checked
against something an agent cannot talk its way past: a commit refused without an
adopted plan, a criterion that stays a gap until fresh evidence bound to the exact
revision supports it, and documents whose truth lives where it is edited, generated
or checked from the owning source rather than copied (AES-CTX-004,
[Decision 0013](../decisions/0013-truth-lives-where-it-is-edited.md)). Self-reported
completion, prose status and hand-maintained copies drift; checked boundaries do not.

## Thesis disproof (AES extension)

Work landed under AES needs its claims corrected after the fact about as often as work
landed without it; or `aes status` reports a criterion supported while a fresh run of
its named checks fails at the same revision; or agents route around the commit rule
(`[Unplanned]` commits, bypassed hooks) more often than they pass it.

## Non-goals

- Retrofitting an arbitrary existing repository (`OUT-GF-001` non-goal; `aes adopt`
  records a baseline but does not claim conformance).
- Universal language support or a universal framework abstraction.
- Orchestrating an organization's portfolio of projects.

## Lineage (AES extension)

Replaces `Inside-Success/agentic-engineering-system`. This repository began
2026-09-16 ("Bootstrap canonical AES repository") as a clean convergence target, so
the integrated architecture would not become one more layer inside an accumulated
repository carrying several lineages, plans and assumptions
([Decision 0001](../decisions/0001-canonical-convergence-boundary.md)). On 2026-09-26
the old repository was archived
([Decision 0011](../decisions/0011-inside-success-aes-archived-canonical-is-aes.md)):
it could not deliver its plan to absorb Company Planning and Enforced Planning into
one runtime, had grown to 96 documentation files with five stale pull requests, and
never showed an outcome improvement. AES v0.2 re-derived that work from a clean sheet
([Decision 0010](../decisions/0010-greenfield-v0.2-accepted.md)).
