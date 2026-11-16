---
description: AES helps autonomous coding agents deliver software that stays true to its intent through linked plans, code, evidence, policy and feedback
doc_role: active_authority
status: current
---

# AES: purpose, scope and thesis

## Introduction and Goals

**North star (AES extension):** autonomous, effective coding agents, using the existing direction
and source quoted below.

### Stakeholders

Brian sets the product direction; coding agents and Project Brains consume the
planning, implementation, policy and feedback contracts described below.

### Quality Goals

Keep intended behavior present at implementation, status distinguishable from
evidence, drift visible and owning sources findable. These are the existing
architectural bet below; no numerical improvement threshold is adopted here.

### What is the project for?

AES is the engineering system for autonomous, effective coding agents. It connects
what software should do, how it is built, what the evidence shows, and what changes
after a failure. Code and documentation alignment is a means to that outcome.

Source: Brian, 2026-11-06, “the real driver which is autonomous effective coding agents”,
preserved in the [Lockstep goal at its last independent revision](https://github.com/BrianMills2718/lockstep/blob/14768712cf0c0fe97a347c28267291fa3c487349/wiki/goal.md#what-lockstep-is-in-brians-words-2026-11-06).
Brian, 2026-11-11, defines AES as the whole system, including Lockstep, feedback and
policy ([repository scope](../../CLAUDE.md#current-state-2026-11-13)). This page
reconciles that existing direction; it does not adopt a new product design.

## Requirements Overview

### What functions does the whole system need?

| Function and provider | Responsibility | Owning description |
| --- | --- | --- |
| Planning, supplied by Company Planning | Derive requirements, acceptance criteria, behavioral units, architecture, file structure, typed seams, tests and implementation slices from accepted intent | [Planning boundary](SYSTEM_BOUNDARY.md#aes-plan-002--planning-subsystem-split) |
| Lockstep | Link planned behavior, file structure, typed interfaces, code, tests and criteria; put normative context at the edit; project implementation status back; expose drift and navigate to owning sources | [Lockstep contract](LOCKSTEP.md) |
| Feedback loop | Turn corrections and observations into sourced dispositions, verified repairs and follow-up observations | [Feedback and policy](FEEDBACK_AND_POLICY.md) |
| Policy layer | Preserve the source and scope of rules, how they are enforced or advised, their recovery paths and the evidence for changing them | [Feedback and policy](FEEDBACK_AND_POLICY.md) |

The earlier three-part shorthand names Lockstep, feedback and policy; it is not
an exhaustive functional boundary. Planning is an essential AES layer, supplied
by Company Planning. Coding agents and Project Brains consume the contracts and
checks; they are not parts inside Lockstep.
Review websites and walkthroughs are presentation work owned by Company Planning
and representation tools, rather than Lockstep's product purpose.
See [AES-SYS-006 and the planning boundary](SYSTEM_BOUNDARY.md#aes-sys-006--parts-and-consumers).

## How should the whole system work?

Consider a password-reset feature. This is an illustrative behavioral example,
not a claim that this repository implements authentication.

1. Plan behavior and acceptance criteria, then identify files, typed interfaces
   and tests for issuing a token and rejecting an expired token. Organize the
   implementation into behavior that can be tested. Revise the plan when the
   structure needs to change.
2. Put the full applicable requirements and criteria into the code's docstrings.
   The agent editing token expiry sees the requirement beside the implementation.
3. If a requirement changes at the docstring, route it back through an explicit
   plan change with history. A change in the plan identifies linked code needing
   attention. Requirement changes and implementation edits stay visible.
4. Derive what exists, what was tested, what passed and what drifted from code
   and revision-bound evidence. Project current status into the documents that
   describe the feature. A typed status claim alone is not evidence.
5. Present concise descriptions and links in the navigational wiki. The reader
   can reach the requirement, implementation and proving test for the same concern.
6. If an agent misses expiry, record the correction and its evidence. Disposition
   it, verify a repair, and inspect later relevant opportunities for recurrence.
   Update policy when warranted.

These are intended relationships, not a claim that every automatic transition
has been demonstrated. The [Lockstep contract](LOCKSTEP.md) identifies existing
mechanisms and verification boundaries. The [discussion ledger](../../wiki/open-questions.md)
preserves open concerns.

## Thesis (AES extension)

An agent is more likely to preserve intent when the relevant intent is present
where it edits, every requirement links to implementation and proving tests,
and observed status flows back to that requirement. This follows AES-CTX-004
(truth lives where it is edited) in the [system boundary](SYSTEM_BOUNDARY.md#aes-ctx-004--truth-lives-where-it-is-edited). Behavior-oriented structure
and strong types support that linkage. The wiki makes context findable without
becoming another independently maintained authority.

Source: Brian's [2026-11-06 explanation](https://github.com/BrianMills2718/lockstep/blob/14768712cf0c0fe97a347c28267291fa3c487349/wiki/goal.md#what-lockstep-is-in-brians-words-2026-11-06),
[source-local context](SYSTEM_BOUNDARY.md#aes-ctx-002--source-local-context-after-realization)
and [truth at the place of editing](../decisions/0013-truth-lives-where-it-is-edited.md).

### Thesis disproof (AES extension)

The bet would be weakened if agents repeatedly miss requirements present at their
edits, projected documents conceal drift, or controls and upkeep cost more useful
work than they protect. Passing linkage checks alone cannot establish more
effective autonomous agents. No improvement rate is claimed here. These are
agent-derived falsification questions for discussion, not newly adopted numerical
acceptance thresholds.

## Where does truth live?

Current Lockstep behavior is specified in [OpenSpec](../../openspec/specs/lockstep-plan-format/spec.md);
planned layout lives in each consumer's `lockstep.yaml`. Code, tests and recorded
evidence own implementation observations. Descriptions belong in the artifact
they describe. Plans, decisions, research and evidence retain distinct lifecycles.
Wiki pages route to those sources. See [documentation roles](DOCUMENTATION.md).

## What is current, and what is history?

AES is active as this whole system. Lockstep ships from `src/lockstep/` here and
uses the retained `src/agentic_engineering_system/` library. The old `aes` command
and `.aes/target.yaml` retire consumer by consumer; compatibility is not the
definition of AES's current goal.

This repository's own `.aes/` target and earlier governance machinery were
[retired on 2026-11-12](../retired/2026-11-12.md). The v0.2 greenfield outcome
remains a [historical implementation contract](greenfield-v0.2/README.md).
It is not the whole system's entry point. The Hive implementation moved to
personal-vps; it is not this repository's present product definition.

## Non-goals

- This repair preserves existing intent. It does not restart retired governance,
  change runtime checks or enable feedback jobs.
- The system does not claim universal language/framework support or that an
  agent's completion statement proves conformance.
- Shared methodology stays owned by the [adopted methodology](https://github.com/BrianMills2718/wiki_methodology/tree/0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe).
- Operational and implementation claims need dated observations. Read
  [current state](../../.project-brain/now.md) and [open concerns](../../wiki/open-questions.md).

## Lineage (AES extension)

This is the existing AES canonical repository, retaining its history rather
than restarting it. The independent Lockstep package was consolidated here;
the legacy governance retirement and retained compatibility boundaries are
linked in the current/history account above.
