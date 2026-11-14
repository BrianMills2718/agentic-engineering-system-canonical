---
type: Model
title: AES implementation map
description: Find the current whole-system map, component code, entry points, stores and retained library boundaries
status: current
last_checked: 2026-11-13
---

# Where are the parts and their implementation?

Use the [whole-system model](../docs/planning/SYSTEM_MODEL.md) for relationships
between Lockstep, feedback, policy, their consumers and stores. It is an inventory,
not proof that every transition runs. The [current architecture](../docs/architecture/GOAL.md)
and [component contracts](../docs/architecture/LOCKSTEP.md) explain intended behavior.

| Part | Implementation | Contract and evidence boundary |
| --- | --- | --- |
| Lockstep | [Package](../src/lockstep/__init__.py), [entry points](../pyproject.toml) | [Component account](../docs/architecture/LOCKSTEP.md), [OpenSpec navigation](requirements.md) |
| Retained AES library and command | [Engine](../src/agentic_engineering_system/__init__.py) | [Retained v0.2 design](../docs/architecture/greenfield-v0.2/README.md); `aes` compatibility is not current self-governance |
| Feedback collection, analysis and repair mechanisms | [Operator guide](../scripts/learning_loop/systemd/README.md) | [Intended loop and dated runtime limits](../docs/architecture/FEEDBACK_AND_POLICY.md) |
| Policy register and instruction sources | [Register](../docs/rules/register.yaml), [rules page](../docs/rules/RULES.md) | [Policy ownership](policy-and-rules.md); the register is not complete shared-instruction coverage |
| Agent instructions | [AGENTS.md](../AGENTS.md) | Hand-maintained; [CLAUDE.md](../CLAUDE.md) imports it with `@AGENTS.md`. The generator was retired (see docs/retired/2026-11-14.md) |

## Execution and storage boundaries

- [Package configuration](../pyproject.toml) owns Python dependencies and commands.
- [Makefile](../Makefile) owns this repository's check commands.
- [Lefthook configuration](../lefthook.yml) selects shared Git hooks. Its presence
  does not establish active Lockstep enforcement in this checkout.
- Each installing consumer owns its OpenSpec files, `lockstep.yaml` and recorded
  results. [Source ownership](../docs/architecture/DOCUMENTATION.md) separates those
  from generated docstrings, reports and navigation.
- The feedback operator guide names the private stores. This wiki does not copy
  transcript or feedback contents into public documentation.
- [brain_fresh.py](../scripts/hive/brain_fresh.py) remains here for callers; the Hive
  implementation moved to personal-vps.

Current integration gaps are in the [discussion ledger](open-questions.md).
The [retirement record](../docs/retired/2026-11-12.md) explains old claims,
worktree and `.aes/` machinery; do not infer active ownership from a retained path.
