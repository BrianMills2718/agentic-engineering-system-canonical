---
type: Glossary
title: Glossary
description: Names a reader meets in this repository and what each means, with the document that defines it
status: current
last_checked: 2026-11-13
---

# Glossary

Current concepts:

| Term | Meaning | Source |
| --- | --- | --- |
| AES | The whole system for autonomous effective coding agents: Lockstep, feedback and policy | [Goal](../docs/architecture/GOAL.md) |
| Lockstep | Planned behavioral structure, linked requirements/code/tests and projection between implementation and documentation | [Component contract](../docs/architecture/LOCKSTEP.md) |
| Normative | Accepted statements of what should be true; distinct from code and observations | [Document roles](../docs/architecture/DOCUMENTATION.md) |
| Projection | A view derived from an owning source; the copy does not acquire independent authority | [Document roles](../docs/architecture/DOCUMENTATION.md) |
| Behavioral unit | A planned piece of behavior with boundaries, interfaces and proving checks; not necessarily one function or one file | [Lockstep planning](../docs/architecture/LOCKSTEP.md#why-it-exists) |
| Standing/status | A derived account of current coverage or evidence, bounded to what was actually observed | [Lockstep status](../docs/architecture/LOCKSTEP.md#what-moves-down-and-what-moves-up) |
| Navigational wiki | Concise source-linked routes and synthesis across a concern | [Wiki role](../docs/architecture/DOCUMENTATION.md#what-belongs-in-a-wiki-summary) |

## Retained engine and earlier architecture vocabulary

The v0.2 engine terms (target, outcome, success criterion, observation, assessment, negative control, freshness, standing, characterization, drift, orphan, gap, legacy baseline, working context and the rest) are defined with their code locations in [docs/planning/DOMAIN.md](../docs/planning/DOMAIN.md) ([docs/planning/DOMAIN.md:7-10](../docs/planning/DOMAIN.md#L7-L10)); the code behind them is mapped on [system-model.md](system-model.md). Brian's reasoning vocabulary is in [docs/terms/ecosystem-terms.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/docs/terms/ecosystem-terms.md). The terms below are defined in no wiki page.

| Term | Meaning | Source |
| --- | --- | --- |
| Company Planning | the default AES planning and design derivation provider: it turns accepted intent and dispositioned gaps into success criteria, boundaries, capability requirements and execution-ready slices | [docs/architecture/SYSTEM_BOUNDARY.md:41](../docs/architecture/SYSTEM_BOUNDARY.md#L41) |
| Enforced Planning | the default execution-governance provider of the v0.1 line: delivers context, claims work, coordinates lanes, triggers checkpoints and runs controls | [docs/architecture/SYSTEM_BOUNDARY.md:41](../docs/architecture/SYSTEM_BOUNDARY.md#L41) |
| ACA | Agentic Capability Architecture; its capability catalogue is applied through AES, and no separate ACA platform is built | [docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md:42-45](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md#L42-L45) |
| Hive brain v1 | Brian's personal hive of agents with one brain per project (goal of 2026-10-02); its scripts and plans moved to personal-vps on 2026-10-07 | [.project-brain/project.md:9-11](../.project-brain/project.md#L9-L11) |
| Utility-discovery latency | the time and cost until the intended actor can say "I can use this enough to know whether I want more of it" | [docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md:20-26](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md#L20-L26) |
