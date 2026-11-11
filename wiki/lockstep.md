---
type: Topic
title: Lockstep
description: What Lockstep is, who uses it, and its status: kept and actively developed as part of AES; its future is under question
status: current
last_checked: 2026-11-11
---

# Lockstep

Repository: [BrianMills2718/lockstep](https://github.com/BrianMills2718/lockstep), maintained in its own repository and pinning this repository's library ([docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29)).

## What it is

- Lockstep is a part of AES: it puts full normative context at an edit, projects plan changes into code and code changes back into the plan, links planned structure to typed symbols and checks, and renders evidence-bound status ([docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29)).
- It is maintained in its own repository and pins this repository's library ([docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29)).
- Brian, 2026-11-06: "lockstep is meant to be part of aes canonical" ([docs/architecture/SYSTEM_BOUNDARY.md:33](../docs/architecture/SYSTEM_BOUNDARY.md#L33)).
- Its package is `pcw`; it copies plan requirements into docstrings and hooks edits ([docs/decisions/0009-aes-and-lockstep-fate.md:27-28](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L27-L28)).
- Its `src/pcw` imports the AES library in 7 files: change_list, change_log, check, docstring_up, plan_to_code, requirement_status, unplanned_symbols ([docs/decisions/0009-aes-and-lockstep-fate.md:108-111](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L108-L111)).

## Who uses it

- lifelike, where its hook blocks edits under `PCW_MODE=block` ([docs/decisions/0009-aes-and-lockstep-fate.md:28-30](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L28-L30)).
- Team-Brains' Project Brain pull request runner, which runs `pcw check --json` from a vendored wheel ([docs/decisions/0009-aes-and-lockstep-fate.md:30-31](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L30-L31)).
- No code2 repository uses it, and both users read requirements from `.aes/target.yaml` ([docs/decisions/0009-aes-and-lockstep-fate.md:31-32](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L31-L32)).

## Overlap with code2check

- For a code2 repository, `code2check project` already writes the requirement text into the docstring under its `Implements:` line and fails on a stale copy ([docs/decisions/0009-aes-and-lockstep-fate.md:33-35](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L33-L35)).
- Only Lockstep's edit-time hook, change log and wiki have no counterpart ([docs/decisions/0009-aes-and-lockstep-fate.md:36-37](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L36-L37)).

## Status (wind-down withdrawn 2026-11-11)

- Decision 0009 (2026-11-10) kept Lockstep for lifelike and Team-Brains with no new users, retiring its AES path after both move off `.aes/target.yaml`; that stage is under question, pending Brian ([docs/decisions/0009-aes-and-lockstep-fate.md:63-68](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L63-L68)).
- Amendment 1 (2026-11-11) said Lockstep winds down; it is withdrawn. Brian, 2026-11-11: "ok i didnt mean to approve abandoingn lockstep. ti is actively being developed." Amendment 2 keeps Lockstep as part of AES ([docs/decisions/0009-aes-and-lockstep-fate.md](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md)).
- The port must replace the 7 files that import the AES library, not only the `.aes/target.yaml` reader ([docs/decisions/0009-aes-and-lockstep-fate.md:108-111](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L108-L111)).
- code2-template#22 is closed as completed for the edit-guard work; its wind-down steps are withdrawn ([CLAUDE.md:18-22](../CLAUDE.md#L18-L22)).
- Lockstep still imports this repository's library, and its linkage folds into `code2check` in stages ([.project-brain/now.md:9](../.project-brain/now.md#L9)).

## Changes made in this repository for Lockstep

- 2026-11-07: `evidence.assess` and `reconcile.reconcile` accept optional `required_dependency_paths`, so Lockstep can require declared inputs before evidence counts ([.project-brain/now.md:7](../.project-brain/now.md#L7)); spec: [required-evidence-inputs](../openspec/specs/required-evidence-inputs/spec.md).
- 2026-11-08: characterization and producer-identity Git readers disable repository hooks and fsmonitor commands ([.project-brain/now.md:3](../.project-brain/now.md#L3)); spec: [inert-characterization](../openspec/specs/inert-characterization/spec.md).
- Neither change restarts the retired self-governance program ([.project-brain/now.md:5](../.project-brain/now.md#L5)).

## Not checked

- Whether `code2check` can host an edit hook, and how the Team-Brains gate would move, were not checked when decision 0009 was taken ([docs/decisions/0009-aes-and-lockstep-fate.md:86-88](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L86-L88)).
- Decision 0009 is wrong if the Team-Brains gate cannot move to `code2check` ([docs/decisions/0009-aes-and-lockstep-fate.md:93-94](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L93-L94)).
