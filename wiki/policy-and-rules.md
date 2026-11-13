---
type: Topic
title: Policy and rules
description: Where AES policy is owned, what the register represents, and how enforcement differs from instruction
status: current
last_checked: 2026-11-13
---

# Policy and rules

Policy states required behavior; mechanisms implement or observe it. AES's [rules register](../docs/rules/register.yaml) and [generated rules page](../docs/rules/RULES.md) describe enforcement status and feedback paths. Brian's shared agent instructions are owned in code2-workspace `agents/`, with client hooks and skills maintained at their own sources.

Read [Feedback and policy](../docs/architecture/FEEDBACK_AND_POLICY.md) for the intended correction-to-follow-up path, responsibilities and dated evidence limits. The register contains one advisory rule plus legacy dispositions; it does not demonstrate coverage of every shared instruction. The November 13 read-only policy check discovered zero policies, so its zero-gap result provides no such assurance.

Use the [operator guide](../scripts/learning_loop/systemd/README.md) for the retained rule-check job. The [open-questions ledger](open-questions.md) tracks discovery and coverage gaps. [Documentation architecture](../docs/architecture/DOCUMENTATION.md) explains why rules, decisions, research, generated pages and wiki summaries have distinct authority.

## Where are the hundreds of Project Meta policies?

The [original Project Meta registry](https://github.com/BrianMills2718/project-meta/blob/main/policy/registry.yaml)
still contains 263 entries as read on 2026-11-13. Its
[policy-system guide](https://github.com/BrianMills2718/project-meta/blob/main/docs/ops/POLICY_SYSTEM.md)
explains source, context delivery, enforcement, observation and feedback categories.
That guide includes older coordination mechanisms; read its dated claims against
the owning implementation rather than treating the entire page as current runtime.

AES's [legacy disposition manifest](../docs/rules/legacy-dispositions.yaml) covers
all 263 identifiers, proposing 229 keep, 27 covered and seven retirement candidates.
Every row has `activation: none`. These are proposals; they do not establish
retirement, migration or present enforcement. The source policies remain in
Project Meta. The [small AES register](../docs/rules/register.yaml) is separate:
its history is 33 → 12 → one entry in the November 10–11 cleanup.

The shared instructions actually loaded by agents have another explicit owning
route: [workspace core](https://github.com/BrianMills2718/code2-workspace/blob/main/agents/core.md),
[topic files](https://github.com/BrianMills2718/code2-workspace/tree/main/agents/topics)
and [rule sources](https://github.com/BrianMills2718/code2-workspace/blob/main/agents/rule-sources.md).
Client hook and skill delivery belongs to
[agent-skills](https://github.com/BrianMills2718/agent-skills/blob/main/README.md).
A complete policy account needs a per-policy relationship between these sources,
current disposition and observed enforcement. That relationship remains incomplete;
this navigation repair does not approve or activate migration candidates.
