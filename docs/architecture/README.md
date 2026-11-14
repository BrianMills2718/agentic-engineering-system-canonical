---
description: Current AES architecture reading order and scope of retained v0.1 and v0.2 designs
status: current
---

# Architecture reading guide

Read the current whole-system account first:

1. [Purpose, scope and thesis](GOAL.md).
2. [Lockstep](LOCKSTEP.md): planned structure, typing, two-way projection and navigation.
3. [Documentation roles](DOCUMENTATION.md): source ownership, lifecycles and views.
4. [Feedback and policy](FEEDBACK_AND_POLICY.md): how observations should change future work.
5. [Detailed architecture clauses](SYSTEM_BOUNDARY.md).
6. [Ecosystem and predecessor review](ECOSYSTEM.md): capability discovery, source ownership and the continuing legacy reading sequence.
7. [Implementation map](../planning/SYSTEM_MODEL.md) and [open concerns](../../wiki/open-questions.md).

These pages reconcile recorded direction. OpenSpec supplies current executable
Lockstep behavior contracts. Read implementation and run evidence separately
before asserting that a requirement works.

## Retained implementation designs

- [greenfield-v0.2](greenfield-v0.2/README.md) describes the retained `aes` library,
  accepted by [Decision 0010](../decisions/0010-greenfield-v0.2-accepted.md).
  It is not the current definition of AES as the whole system.
- The v0.1 record design remains evidence for the origin of
  [source-local context](../decisions/0003-component-local-normative-context-and-symbol-inheritance.md)
  and [document roles and generated PRDs](../decisions/0004-compact-structured-normative-records-and-generated-views.md).
  It does not silently replace today's OpenSpec/layout format.
- [Retirement record](../retired/2026-11-12.md) names retired paths and recovery commands.
- [Decision 0013](../decisions/0013-truth-lives-where-it-is-edited.md) preserves the
  source-local summary principle used in the current whole-system account.

## Ownership

Project-agnostic methodology is owned by the
[pinned upstream methodology](https://github.com/BrianMills2718/wiki_methodology/tree/0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe).
AES-specific intent belongs here; accepted choices remain in `docs/decisions/`.
Research and evidence support decisions without becoming desired behavior.
The wiki is navigation, not another mutable authority.
