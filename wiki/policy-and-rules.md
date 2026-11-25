---
type: Topic
title: Policy and rules
description: Where AES policy is owned (code2-workspace agents/), what AES keeps, and how enforcement differs from instruction
status: current
last_checked: 2026-11-25
---

# Policy and rules

Policy states required behavior; mechanisms implement or observe it. Rules have one home: Brian's shared agent instructions in code2-workspace `agents/` (core.md and the topic files, with his words behind each in rule-sources.md), with client hooks and skills maintained at their own sources. Each rule's text names the check or hook that enforces it. AES kept a second, one-rule register and a page generated from it until 2026-11-25; they were retired so there is one list ([retirement record](../docs/retired/2026-11-25.md); Brian, 2026-11-25, "ia prpove yourr ecommednations though").

Read [Feedback and policy](../docs/architecture/FEEDBACK_AND_POLICY.md) for the intended correction-to-follow-up path, responsibilities and dated evidence limits. The rule check `scripts/learning_loop/policies.py` reads the Policy ids named in core.md and the topic files and reports any with no entry in rule-sources.md; on 2026-11-25 it found 26 ids, 3 with no source entry. It does not show that a rule is enforced.

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
Project Meta. The text of the 229 proposed "keep" rows was never moved into
code2-workspace `agents/`; it exists only in the private Project Meta registry.
A separate small AES register (33 → 12 → one entry in the November 10–11 cleanup)
was retired on 2026-11-25; its one rule was already in the workspace closeout rules.

The shared instructions actually loaded by agents have another explicit owning
route: [workspace core](https://github.com/BrianMills2718/code2-workspace/blob/main/agents/core.md),
[topic files](https://github.com/BrianMills2718/code2-workspace/tree/main/agents/topics)
and [rule sources](https://github.com/BrianMills2718/code2-workspace/blob/main/agents/rule-sources.md).
Client hook and skill delivery belongs to
[agent-skills](https://github.com/BrianMills2718/agent-skills/blob/main/README.md).
A complete policy account needs a per-policy relationship between these sources,
current disposition and observed enforcement. That relationship remains incomplete;
this navigation repair does not approve or activate migration candidates.
