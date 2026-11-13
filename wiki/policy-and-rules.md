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
