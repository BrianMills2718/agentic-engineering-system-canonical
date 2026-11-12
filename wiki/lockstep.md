---
type: Topic
title: Lockstep
description: What Lockstep is, who uses it, and its status: the one AES planning-and-checking tool, shipped from this repository as package lockstep (design built 2026-11-11)
status: current
last_checked: 2026-11-12
---

# Lockstep

Code: this repository, package `lockstep` in [src/lockstep/](../src/lockstep/__init__.py) (`pcw` kept as an alias package), spec [lockstep-package](../openspec/specs/lockstep-package/spec.md). The old repository [BrianMills2718/lockstep](https://github.com/BrianMills2718/lockstep) is kept as history.

## What it is

- Lockstep is a part of AES: it puts full normative context at an edit, projects plan changes into code and code changes back into the plan, links planned structure to typed symbols and checks, and renders evidence-bound status ([docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29)).
- Brian, 2026-11-06: "lockstep is meant to be part of aes canonical" ([docs/architecture/SYSTEM_BOUNDARY.md:33](../docs/architecture/SYSTEM_BOUNDARY.md#L33)).
- One config file, `lockstep.yaml`; commands `lockstep layout`, `lockstep check` (the whole-tree plan check, or `check <name>` for one commit check), `lockstep plan check`, `lockstep status`, `lockstep show`, and the edit hook `lockstep-hook` ([design](../proposals/one-planning-tool/DESIGN.md)).

## Who uses it

- lifelike, pinned to this repository, where its hook blocks off-plan edits under `PCW_MODE=block` ([lifelike#5](https://github.com/BrianMills2718/lifelike/pull/5)).
- Team-Brains' Project Brain pull request runner, from a vendored wheel of this repository ([Team-Brains#1183](https://github.com/Inside-Success/Team-Brains/pull/1183)); installed on the server 2026-11-12.
- New code2 repositories: code2-template installs it in place of code2check ([code2-template#29](https://github.com/BrianMills2718/code2-template/pull/29)); existing ones switch when next changed.

## Status (2026-11-12: built)

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

- 2026-11-07: `evidence.assess` and `reconcile.reconcile` accept optional `required_dependency_paths`, so Lockstep can require declared inputs before evidence counts ([.project-brain/now.md:7](../.project-brain/now.md#L7)); spec: [required-evidence-inputs](../openspec/specs/required-evidence-inputs/spec.md).
- 2026-11-08: characterization and producer-identity Git readers disable repository hooks and fsmonitor commands ([.project-brain/now.md:3](../.project-brain/now.md#L3)); spec: [inert-characterization](../openspec/specs/inert-characterization/spec.md).
- Neither change restarts the retired self-governance program ([.project-brain/now.md:5](../.project-brain/now.md#L5)).

## Not checked

- Whether Company Planning's adoption gate should call `lockstep plan check` rather than its own copy (design, "What this does not decide"); slice 5 kept both, with the same checks.
