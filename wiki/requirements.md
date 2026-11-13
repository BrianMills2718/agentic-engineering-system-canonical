---
type: Requirements
title: Required behavior and its evidence
description: Route to current Lockstep behavior contracts and distinguish them from retained engine and feedback requirements
status: current
last_checked: 2026-11-13
---

# Required behavior and its evidence

The [AES goal](../docs/architecture/GOAL.md) explains the outcome. The
[system boundary](../docs/architecture/SYSTEM_BOUNDARY.md) records system clauses.
Current executable Lockstep requirements are OpenSpec files; their scenarios define
what a test should demonstrate. The following is navigation, not a second copy of
the requirements or a claim that their tests passed today.

## Current Lockstep contracts

| Concern | Owning specification | Implementation and proving examples |
| --- | --- | --- |
| Package and compatibility entry points | [Package](../openspec/specs/lockstep-package/spec.md) | [Package configuration](../pyproject.toml) |
| Installation and hooks | [Initialization](../openspec/specs/lockstep-init/spec.md) | [Installer](../src/lockstep/init_repo.py) |
| Planned files, purpose, requirements, tests and typed exports | [Plan format](../openspec/specs/lockstep-plan-format/spec.md) | [Layout and tests](../docs/architecture/LOCKSTEP.md#evidence-and-change-discipline) |
| Edit-time boundaries | [Guard](../openspec/specs/lockstep-guard/spec.md) | [Hook](../src/lockstep/hook.py) |
| Commit-time checks | [Checks](../openspec/specs/lockstep-checks/spec.md) | [Check implementation](../src/lockstep/checks/cli.py) |
| Plan-package validation | [Plan check](../openspec/specs/lockstep-plan-check/spec.md) | [Plan checker](../src/lockstep/plan_check.py) |
| Requirement copies and implementation coverage | [Projection and status](../openspec/specs/lockstep-projection/spec.md) | [Projector](../src/lockstep/checks/project.py), [status](../src/lockstep/checks/status.py) |
| Source-owned descriptions, interfaces and evidence values | [Declared document facts](../openspec/specs/lockstep-doc-facts/spec.md) | [Fact projector](../src/lockstep/doc_projection.py) |

The [component contract](../docs/architecture/LOCKSTEP.md#current-mechanisms-and-their-limits)
explains how these mechanisms fit together and which intended guarantees remain
unverified. A specification's presence is not runtime evidence.

## Retained library and feedback contracts

- [Inert characterization](../openspec/specs/inert-characterization/spec.md) governs
  read-only repository inspection in the retained AES library.
- [Required evidence inputs](../openspec/specs/required-evidence-inputs/spec.md) governs
  qualification of evidence over declared dependencies.
- [Greenfield v0.2](../docs/architecture/greenfield-v0.2/README.md) preserves the
  accepted historical engine contract; it is not a replacement for the current goal.
- [Feedback and policy](../docs/architecture/FEEDBACK_AND_POLICY.md) identifies that
  path's native operator contract, implementation and dated observation limits.

## Where are observations and unresolved gaps?

- [Current state](../.project-brain/now.md) names the latest documentation and work context.
- [Retained acceptance observations](../docs/planning/runs/lockstep-acceptance/a1.json)
  are revision-bound records, with limits recorded in the
  [discussion ledger](open-questions.md).
- [Source-fact acceptance](../docs/planning/source-facts-acceptance.md) and its
  [bounded cold review](../docs/planning/cold-review.md) cover that particular slice.
- [Test commands](../tests/README.md) explain how to obtain fresh execution evidence.
  This documentation repair makes no new claim of full product test coverage.
