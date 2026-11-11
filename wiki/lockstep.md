---
type: Topic
title: Lockstep
description: What Lockstep is, who uses it, and its status: the core of the single AES planning-and-checking tool to come (direction approved, design to come)
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

## Status (2026-11-11: one AES planning-and-checking tool, direction approved, design to come)

- Decision 0009 (2026-11-10) kept Lockstep for lifelike and Team-Brains with no new users, retiring its AES path after both move off `.aes/target.yaml`; amendment 3 withdraws that stage ([docs/decisions/0009-aes-and-lockstep-fate.md](https://github.com/BrianMills2718/code2-workspace/blob/main/docs/decisions/0009-aes-and-lockstep-fate.md)).
- Amendment 1 (2026-11-11) said Lockstep winds down; amendment 2 withdrew it. Brian, 2026-11-11: "ok i didnt mean to approve abandoingn lockstep. ti is actively being developed."
- Amendment 3, part 1 (Brian, 2026-11-11: "ok and on this "A person approves it, and only then does an agent lay out the files' it also writes the firs tdoc strings. which incldues the nroamtive sutff on what his sis uppoed to do and it success critieria test stuff. i approve d3. and d2"): Lockstep does the upfront plan of the whole file structure; once a person approves it, an agent lays out the files with their first docstrings (the normative text of what each file must do, its success criteria and tests); Lockstep keeps them aligned and guides and refuses at edit time. code2check runs the commit checks (tests first, LikeC4 import rules, Source lines, docmeta). Both read one plan format; `code2check project` and code2check's edit guard (code2-template #24 to #26) hand off to Lockstep.
- Amendment 3, part 2 (Brian, 2026-11-11, on the Lockstep session's Decision 4, relayed by that session: "on dcision 4 it seems liek youa re poitn otu that htis should be combined into one single thing not a bunch of differnt things which i agree with. and it should preusmably be part of aes canonicale which is configurable and protable/sharebale"): these become one tool, part of AES canonical, configurable and portable/shareable. Direction approved; design to come (the Lockstep session proposes it to Brian). Part 1 describes today's parts, not a lasting split.
- D2: lifelike, Lockstep's demonstration project, runs Lockstep's edit hook again (`PCW_MODE=block`).
- Lockstep still imports this repository's library ([.project-brain/now.md:9](../.project-brain/now.md#L9)).

## Changes made in this repository for Lockstep

- 2026-11-07: `evidence.assess` and `reconcile.reconcile` accept optional `required_dependency_paths`, so Lockstep can require declared inputs before evidence counts ([.project-brain/now.md:7](../.project-brain/now.md#L7)); spec: [required-evidence-inputs](../openspec/specs/required-evidence-inputs/spec.md).
- 2026-11-08: characterization and producer-identity Git readers disable repository hooks and fsmonitor commands ([.project-brain/now.md:3](../.project-brain/now.md#L3)); spec: [inert-characterization](../openspec/specs/inert-characterization/spec.md).
- Neither change restarts the retired self-governance program ([.project-brain/now.md:5](../.project-brain/now.md#L5)).

## Not checked

- Whether `code2check` can host an edit hook, and how the Team-Brains gate would move, were not checked when decision 0009 was taken ([docs/decisions/0009-aes-and-lockstep-fate.md:86-88](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L86-L88)).
- Decision 0009 is wrong if the Team-Brains gate cannot move to `code2check` ([docs/decisions/0009-aes-and-lockstep-fate.md:93-94](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L93-L94)).
