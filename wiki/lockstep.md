---
type: Topic
title: Lockstep
description: Navigate Lockstep purpose, planned behavioral structure, source-local context, implementation and evidence
status: current
last_checked: 2026-11-13
---

# Lockstep

Start with the [component architecture](../docs/architecture/LOCKSTEP.md): why
Lockstep exists, the planned behavioral units and typed seams, what moves down
into code and up into evidence, source ownership, and current implementation
limits. This wiki page is navigation; the architecture, specifications and recorded
observations retain their own roles.

Lockstep helps autonomous coding agents implement intended behavior effectively.
Its planning approach names the file structure and behavioral contracts before
implementation, linking requirements, success criteria, tests, files and symbols.
The planner supplies that decomposition; Lockstep represents, scaffolds, projects
and checks it. A module list by itself is not the whole intended plan.

Code: this repository, package `lockstep` in [src/lockstep/](../src/lockstep/__init__.py) (`pcw` kept as an alias package), spec [lockstep-package](../openspec/specs/lockstep-package/spec.md). The old repository [BrianMills2718/lockstep](https://github.com/BrianMills2718/lockstep) is kept as history.

## What it is

- Lockstep is a part of AES: it puts full normative context at an edit, projects plan changes into code and code changes back into the plan, links planned structure to typed symbols and checks, and renders evidence-bound status ([docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29)).
- Brian, 2026-11-06: "lockstep is meant to be part of aes canonical" ([docs/architecture/SYSTEM_BOUNDARY.md:33](../docs/architecture/SYSTEM_BOUNDARY.md#L33)).
- One config file, `lockstep.yaml`; commands `lockstep layout`, `lockstep check` (the whole-tree plan check, or `check <name>` for one commit check), `lockstep plan check`, `lockstep status`, `lockstep show`, and the edit hook `lockstep-hook` ([design](../proposals/one-planning-tool/DESIGN.md)).

## Who uses it

- lifelike, pinned to this repository, where its hook blocks off-plan edits under `PCW_MODE=block` ([lifelike#5](https://github.com/BrianMills2718/lifelike/pull/5)).
- Team-Brains' Project Brain pull request runner, from a vendored wheel of this repository ([Team-Brains#1183](https://github.com/Inside-Success/Team-Brains/pull/1183)); installed on the server 2026-11-12.
- New code2 repositories: code2-template installs it in place of code2check ([code2-template#29](https://github.com/BrianMills2718/code2-template/pull/29)); existing ones switch when next changed.

## Delivered mechanisms and recorded adoption (2026-11-12)

- Brian approved one tool, part of AES canonical, configurable and portable/shareable (2026-11-11, "i approve single tool desing re d4"), after withdrawing a wind-down the same day ("ok i didnt mean to approve abandoingn lockstep"); history in code2-workspace [decision 0009](https://github.com/BrianMills2718/code2-workspace/blob/main/docs/decisions/0009-aes-and-lockstep-fate.md).
- The six slices of the [design](../proposals/one-planning-tool/DESIGN.md) are merged:
  1. The code moved here ([#831](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/831)).
  2. The plan is OpenSpec plus `layout:` rows ([#835](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/835), [spec](../openspec/specs/lockstep-plan-format/spec.md)), with `.aes/target.yaml` still read.
  3. The guard uses code2check's shell-target parser ([#834](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/834), [spec](../openspec/specs/lockstep-guard/spec.md)).
  4. The commit checks ([#833](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/833), [spec](../openspec/specs/lockstep-checks/spec.md)).
  5. The plan check ([#832](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/832), [spec](../openspec/specs/lockstep-plan-check/spec.md)).
  6. Projection, status, show and the pytest plugin ([#836](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/836), [spec](../openspec/specs/lockstep-projection/spec.md)), then the users switch (above).
- Two projectors remain inside the one package. The cog one fills layout and AES-plan files. The code2check one fills `Implements:` docstrings in code2 repositories. Merging them is not yet planned.

## Changes made in this repository for Lockstep

- 2026-11-07: `evidence.assess` and `reconcile.reconcile` accept optional `required_dependency_paths`, so Lockstep can require declared inputs before evidence counts ([.project-brain/now.md:7](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/.project-brain/now.md#L7)); spec: [required-evidence-inputs](../openspec/specs/required-evidence-inputs/spec.md).
- 2026-11-08: characterization and producer-identity Git readers disable repository hooks and fsmonitor commands ([.project-brain/now.md:3](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/.project-brain/now.md#L3)); spec: [inert-characterization](../openspec/specs/inert-characterization/spec.md).
- Neither change restarts the retired self-governance program ([.project-brain/now.md:5](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/.project-brain/now.md#L5)).

## Boundaries and open integration questions

- Current code still carries legacy AES plan/proposal assumptions; the [implementation table](../docs/architecture/LOCKSTEP.md#current-mechanisms-and-their-limits) distinguishes those from the OpenSpec/layout route.
- No blanket claim is made that every native tool call is guarded, that every docstring carries synchronized evidence status, or that PostToolUse performs every plan projection. It refreshes declared source-owned facts.
- Editing a supported normative cog copy can [draft an accepted-plan change](../src/lockstep/docstring_up.py); the legacy draft-and-accept route is not established as a general OpenSpec round trip.
- Whether Company Planning's adoption gate should call `lockstep plan check` rather than its own copy (design, "What this does not decide"); slice 5 kept both, with the same checks.

## Source-local document projections

Descriptions, lifecycle fields, Python interfaces and native evidence values
can be declared once and projected into marked wiki/document sections. See the
[declaration and installed hook/check path](../README.md#project-source-owned-facts)
and the [source-local facts specification](../openspec/specs/lockstep-doc-facts/spec.md).
These generated copies do not certify arbitrary prose or consumer rollout.

## Read the mechanisms and their evidence

| Question | Source |
| --- | --- |
| How are files and behavior planned before implementation? | [Plan format](../openspec/specs/lockstep-plan-format/spec.md), [layout adapter](../src/lockstep/layout_plan.py), [scaffold](../src/lockstep/scaffold.py) |
| How does normative text move down and draft changes move up? | [Cog renderer](../src/lockstep/cogtext.py), [docstring drafts](../src/lockstep/docstring_up.py) |
| What is checked before committing? | [Whole-tree check](../src/lockstep/check.py), [named commit checks](../openspec/specs/lockstep-checks/spec.md) |
| What does current status mean? | [Status implementation](../src/lockstep/checks/status.py), [projection contract](../openspec/specs/lockstep-projection/spec.md) |
| Which examples exercise these mechanisms? | [Layout tests](../tests/lockstep/test_lockstep_layout_plan.py), [draft tests](../tests/lockstep/test_lockstep_docstring_up.py), [status tests](../tests/lockstep/checks/test_lockstep_check_status.py) |

The [retained acceptance page](../proposals/planning-package/review-page/lockstep-acceptance.html)
is a bounded review record. Its conclusions do not replace fresh checks of installed
hooks or establish universal consumer rollout.
