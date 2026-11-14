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

## Diagrams for the side pane

[aes.c4](aes.c4) is a LikeC4 model of the parts of AES (Brian, Planning, Lockstep, code and tests, evidence, the
feedback loop, the policy layer). `scripts/pane_diagrams.py` turns each view into a boxes-and-arrows text diagram
under [pane/](pane/aes_parts.txt) ([the feedback loop view](pane/aes_loop.txt)), and refuses a view that is wider
than 72 columns or whose labels overlap. The wording lives in the model; change it there and rerun the two commands in
the script's header. The side pane of Brian's Claude Code session reads these files. Source: Brian, 2026-11-14: "we
should use generated but make the basis of the generated files good enough that it projects well".
