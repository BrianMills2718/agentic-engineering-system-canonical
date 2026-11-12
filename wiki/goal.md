---
type: Goal
title: What AES is for
description: Purpose, users, scope and non-goals of the Agentic Engineering System as of 2026-11-11
status: current
last_checked: 2026-11-11
---

# What AES is for

## What AES is now

- AES is the name for the whole agent system: Lockstep, the feedback loop and the policy layer ([CLAUDE.md:14-16](../CLAUDE.md#L14-L16)).
- Brian, 2026-11-11: "aes is the whole sysem lockstep is one part. aes include the whole feedback and policy system" ([.project-brain/now.md:9](../.project-brain/now.md#L9)).
- The parts stay where they are, and the map of them is code2-workspace `docs/architecture/model.c4` ([docs/decisions/0009-aes-and-lockstep-fate.md:112-113](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L112-L113)).
- Part 1, Lockstep, is kept and actively developed as part of AES (Brian, 2026-11-11: "ok i didnt mean to approve abandoingn lockstep. ti is actively being developed."); its future is under question, pending Brian ([CLAUDE.md:18-22](../CLAUDE.md#L18-L22)); details on [lockstep.md](lockstep.md).
- Part 2, the feedback loop, is kept and runs nightly from this repository's `scripts/learning_loop` ([.project-brain/now.md:9](../.project-brain/now.md#L9)); details on [feedback-loop.md](feedback-loop.md).
- Part 3, the policy layer, is the rules register here (`scripts/rules`) plus Brian's agent rules (core.md and topic files) in code2-workspace `agents/` ([.project-brain/now.md:9](../.project-brain/now.md#L9)); details on [policy-and-rules.md](policy-and-rules.md).
- The `aes` command line and `.aes/target.yaml` files retire one repository at a time, when each repository is next changed ([docs/decisions/0009-aes-and-lockstep-fate.md:57-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L61)).
- AES no longer governs itself: its pre-commit refusal was removed on 2026-10-14 (#789), and no `aes plan accept` step is required before a change ([CLAUDE.md:22-23](../CLAUDE.md#L22-L23)).
- Behavior changes go through OpenSpec ([.project-brain/now.md:60-61](../.project-brain/now.md#L60-L61)).
- The two lasting ideas of the old regime, a planned file structure and evidence-computed status, are being carried into the AES structure section under OpenSpec and Lockstep ([CLAUDE.md:25-28](../CLAUDE.md#L25-L28)).
- The v0.2 regime is history; see [history.md](history.md) ([CLAUDE.md:31-32](../CLAUDE.md#L31-L32)).

## Who uses it

- Brian decides business, product and priority calls, anything outward, WSL restarts and more than trivial spend ([.project-brain/project.md:16-17](../.project-brain/project.md#L16-L17)).
- Agents make technical calls, verify them, and merge Brian's own pull requests themselves ([.project-brain/project.md:18-19](../.project-brain/project.md#L18-L19)).
- Coding agents (Claude Code and Codex) plan, implement and verify work under AES ([docs/architecture/GOAL.md:31](../docs/architecture/GOAL.md#L31)).
- Project Brains and coding agents are consumers of Lockstep and AES, not parts of them ([docs/architecture/SYSTEM_BOUNDARY.md:31](../docs/architecture/SYSTEM_BOUNDARY.md#L31)).
- Brian observes the feedback loop's ranked view and is notified; he is not an approver of its rules ([proposals/aes-learning-loop/PLAN.md:47](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/PLAN.md#L47)).

## Scope of each part

- Lockstep puts full normative context at an edit, projects plan changes into code and back, links planned structure to typed symbols and checks, and renders evidence-bound status ([docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29)).
- The feedback loop turns each lesson, friction, problem, experiment and research finding into a linked report, analyses problems that recur, turns licensed claims into enforced rules or checks, and observes whether the failure stops recurring ([proposals/aes-learning-loop/PLAN.md:9](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/PLAN.md#L9)).
- The policy layer publishes AES rules with their enforcement and evidence from one register ([docs/rules/RULES.md:3](../docs/rules/RULES.md#L3)).
- The retained engine library in `src/agentic_engineering_system/` stays because Lockstep pins it ([docs/architecture/greenfield-v0.2/README.md:15](../docs/architecture/greenfield-v0.2/README.md#L15)).

## Thesis (as written; partly superseded)

- GOAL.md's bet: agent-built software stays true to intent when every claim is checked against something an agent cannot talk its way past ([docs/architecture/GOAL.md:44-50](../docs/architecture/GOAL.md#L44-L50)).
- One of the boundaries it names, a commit refused without an adopted plan, was removed on 2026-10-14, so that part is superseded ([docs/architecture/GOAL.md:45-46](../docs/architecture/GOAL.md#L45-L46)) ([CLAUDE.md:22-23](../CLAUDE.md#L22-L23)).
- The other two boundaries remain: a criterion stays a gap until fresh revision-bound evidence supports it, and truth lives where it is edited ([docs/architecture/GOAL.md:46-49](../docs/architecture/GOAL.md#L46-L49)).
- The thesis disproof still names commit-rule bypasses, which no longer exist; this is listed on [open-questions.md](open-questions.md) ([docs/architecture/GOAL.md:54-57](../docs/architecture/GOAL.md#L54-L57)).
- Quality goals: ignorance never renders green, every control can be shown to fail, and off-the-shelf tools come first ([docs/architecture/GOAL.md:21-26](../docs/architecture/GOAL.md#L21-L26)).

## Utility and conformance

- Direct stakeholder use and technical conformance answer different questions and stay separately visible: automated green cannot override a stakeholder saying the result is low-value, and enthusiasm cannot turn missing, failed or stale evidence into conformance ([docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md:250-268](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md#L250-L268)).

## Non-goals

- Retrofitting an arbitrary existing repository ([docs/architecture/GOAL.md:61-62](../docs/architecture/GOAL.md#L61-L62)).
- Universal language support or a universal framework abstraction ([docs/architecture/GOAL.md:63](../docs/architecture/GOAL.md#L63)).
- Orchestrating an organization's portfolio of projects ([docs/architecture/GOAL.md:64](../docs/architecture/GOAL.md#L64)).
- New Lockstep users ([docs/decisions/0009-aes-and-lockstep-fate.md:67](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L67)).
- Restarting the former universal self-governance regime or the parked issue backlog ([.project-brain/now.md:5](../.project-brain/now.md#L5)).
- Restarting standalone ACA benchmarks or demonstration products from historical plans ([CLAUDE.md:115](../CLAUDE.md#L115)).
- Restating project-agnostic architecture, which stays in `wiki_methodology` ([CLAUDE.md:101](../CLAUDE.md#L101)).

## Lineage

- The repository began on 2026-09-16 as a clean convergence target so the integrated architecture would not become one more layer in an older repository ([docs/architecture/GOAL.md:68-72](../docs/architecture/GOAL.md#L68-L72)).
- It replaced `Inside-Success/agentic-engineering-system`, archived on 2026-09-26 ([docs/architecture/GOAL.md:72-78](../docs/architecture/GOAL.md#L72-L78)).
- It is a protocol-pilot consumer of `BrianMills2718/wiki_methodology` at revision `0cddc6b1` ([CLAUDE.md:10](../CLAUDE.md#L10)).
