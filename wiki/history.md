---
type: History
title: History
description: History only. The v0.1 line, v0.2 self-governance, the commit rule and its removal, and the proposals by name
status: current
last_checked: 2026-11-11
---

# History

This page is history. Nothing here is a current rule; current state is on [goal.md](goal.md) ([CLAUDE.md:31-32](../CLAUDE.md#L31-L32)).

## v0.1 bootstrap (2026-09-16 to 2026-09-25)

- The repository began on 2026-09-16 as a clean convergence target ([docs/architecture/GOAL.md:68-72](../docs/architecture/GOAL.md#L68-L72)); see [Decision 0001](../docs/decisions/0001-canonical-convergence-boundary.md).
- Plan 001, Repository Context, was recorded as delivered for its bounded Slice 1 claim ([docs/architecture/INITIAL_GAP_LEDGER.md:90](../docs/architecture/INITIAL_GAP_LEDGER.md#L90)).
- Its remaining NARROWED/DEFER rows were broader maturation questions, not unfinished tasks ([docs/architecture/INITIAL_GAP_LEDGER.md:98-99](../docs/architecture/INITIAL_GAP_LEDGER.md#L98-L99)).
- Plan 002 (offline policy replay) was closed as superseded with Decision 0011 ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:95-96](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L95-L96)).
- The v0.1 bootstrap architecture files remain in `docs/architecture/` ([docs/architecture/README.md:5](../docs/architecture/README.md#L5)).

## v0.2 greenfield and self-governance (2026-09-24 to 2026-10-14)

- The v0.2 greenfield MVP was accepted as realized on 2026-09-25: ten components, the `aes` command and the `.aes/` materialization ([docs/decisions/0010-greenfield-v0.2-accepted.md:36-41](../docs/decisions/0010-greenfield-v0.2-accepted.md#L36-L41)).
- AES governed `src/agentic_engineering_system/` and `tests/greenfield/` through its own `.aes/target.yaml` ([CLAUDE.md:36-40](../CLAUDE.md#L36-L40)).
- Every file under a governed root had to be planned, or the pre-commit hook refused the commit ([CLAUDE.md:44-47](../CLAUDE.md#L44-L47)).
- Target changes went through `aes plan prepare / validate / accept` ([CLAUDE.md:48-50](../CLAUDE.md#L48-L50)).
- Evidence PRs had to merge with a merge commit, never squash ([CLAUDE.md:53-57](../CLAUDE.md#L53-L57)).
- Two consumers: whygame5 from its first commit, and AES itself as a retrofit ([docs/decisions/0010-greenfield-v0.2-accepted.md:26-29](../docs/decisions/0010-greenfield-v0.2-accepted.md#L26-L29)).
- Value beyond mechanism was not demonstrated ([docs/decisions/0010-greenfield-v0.2-accepted.md:160-164](../docs/decisions/0010-greenfield-v0.2-accepted.md#L160-L164)).
- The build is recorded phase by phase in [24-pre-probe-decisions.md](../proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md) ([proposals/aes-v0.2-greenfield/README.md:120](../proposals/aes-v0.2-greenfield/README.md#L120)).
- Superseded: `.project-brain/project.md` "AES governs itself" ([.project-brain/project.md:12-15](../.project-brain/project.md#L12-L15)), replaced by [CLAUDE.md:22-23](../CLAUDE.md#L22-L23).
- `aes adopt` (2026-10-07) wrote a legacy baseline so existing repositories could join without planning old files ([.project-brain/now.md:73-76](../.project-brain/now.md#L73-L76)).

## Inside Success archive (2026-09-26)

- This repository became the Agentic Engineering System and `Inside-Success/agentic-engineering-system` was archived ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:44-47](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L44-L47)).
- Its borrowable ideas were harvested with adoption triggers, not ported ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:54-58](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L54-L58)).
- whygame5's value tally came back at 0 AES catches and 4 hand checks, later 1 catch and 6 hand checks ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:75-77](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L75-L77)).

## The commit rule (2026-10-06 to 2026-10-14)

- Brian, 2026-10-06: "we need to lock down unplanned" ([proposals/aes-planning/README.md:31](../proposals/aes-planning/README.md#L31)).
- The rule checked commit tags against facts: `[Plan #N]`/`[Goal]` needed an adopted receipt, `[Trivial]` a small diff, `[Unplanned]` an `Emergency:` line ([proposals/aes-planning/README.md:66-69](../proposals/aes-planning/README.md#L66-L69)).
- A replay found 99% of commits in active repositories would be refused ([proposals/aes-planning/ROLLOUT.md:49-53](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-planning/ROLLOUT.md#L49-L53)).
- It was switched to enforce on the evening of 2026-10-08 ([proposals/aes-planning/ROLLOUT.md:214-219](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-planning/ROLLOUT.md#L214-L219)).
- On 2026-10-13 Brian asked to turn off the enforcement that made trivial agent tasks take an hour; `aes commit`, the commit-msg hook writer, the plan-receipt check and the rollout timers were removed on 2026-10-14 ([.project-brain/now.md:56-61](../.project-brain/now.md#L56-L61)) ([docs/model/ODD.md:55-57](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/model/ODD.md#L55-L57)).

## Move to code2 and hold (2026-10-13 to 2026-10-18)

- On 2026-10-13 Brian moved `~/code2` to off-the-shelf tools: OpenSpec, lefthook and GitHub Issues ([CLAUDE.md:24-25](../CLAUDE.md#L24-L25)).
- AES canonical joined code2 as an ordinary repository; the phase 2 plan built on AES enforcement was superseded ([proposals/code2-ecosystem/PLAN.md:21-27](../proposals/code2-ecosystem/PLAN.md#L21-L27)).
- AES was put on hold on 2026-10-18 ([.project-brain/now.md:9](../.project-brain/now.md#L9)).
- Its open issues carry the `on-hold` label; they are parked, not closed ([CLAUDE.md:28-29](../CLAUDE.md#L28-L29)).
- The hive scripts and plans moved to personal-vps on 2026-10-07 ([.project-brain/now.md:80](../.project-brain/now.md#L80)).

## Decision 0009 in code2-workspace (2026-11-10 and 2026-11-11)

- Accepted 2026-11-10: retire `aes` and `.aes/target.yaml` per repository, keep the feedback loop, fold Lockstep into `code2check` in stages ([docs/decisions/0009-aes-and-lockstep-fate.md:57-68](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L68)).
- Amendment 1, 2026-11-11: Lockstep winds down and AES is the name for the whole system ([docs/decisions/0009-aes-and-lockstep-fate.md:98-113](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L98-L113)).
- It is a different decision from this repository's own [Decision 0009](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md), which is about modular product design ([docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md:11](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md#L11)).

## Proposals by name (plan records, kept in place)

- [aes-adopt-existing](../proposals/aes-adopt-existing/README.md): `aes adopt` legacy baseline ([proposals/aes-adopt-existing/README.md:23](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-adopt-existing/README.md#L23)).
- [aes-plan-scope](../proposals/aes-plan-scope/README.md): plans may edit the legacy files their `conflict_surfaces` declare ([proposals/aes-plan-scope/README.md:23](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-plan-scope/README.md#L23)).
- [aes-planning](../proposals/aes-planning/README.md) and [ROLLOUT](../proposals/aes-planning/ROLLOUT.md): the commit rule ([proposals/aes-planning/README.md:24](../proposals/aes-planning/README.md#L24)).
- [commit-rule-followups](../proposals/commit-rule-followups/commit-rule-followups.md): quick-plan checks and wider running-thing list ([proposals/commit-rule-followups/commit-rule-followups.md:26](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/commit-rule-followups/commit-rule-followups.md#L26)).
- [commit-tag-case](../proposals/commit-tag-case/commit-tag-case.md): capitalised plan names read as tags ([proposals/commit-tag-case/commit-tag-case.md:26](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/commit-tag-case/commit-tag-case.md#L26)).
- [doc-reach-new-docs](../proposals/doc-reach-new-docs/PLAN.md): new documents must be linked from the wiki ([proposals/doc-reach-new-docs/PLAN.md:26](../proposals/doc-reach-new-docs/PLAN.md#L26)).
- [worktree-plan-lookup](../proposals/worktree-plan-lookup/worktree-plan-lookup.md): foreign Git context in plan admission ([proposals/worktree-plan-lookup/worktree-plan-lookup.md:26](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/worktree-plan-lookup/worktree-plan-lookup.md#L26)).
- [trace-review](../proposals/trace-review/README.md): plans declare traced work ([proposals/trace-review/README.md:23](../proposals/trace-review/README.md#L23)).
- [trace-review-enforcement](../proposals/trace-review-enforcement/plan.md): source-bound review records; first boundary only ([proposals/trace-review-enforcement/plan.md:130-132](../proposals/trace-review-enforcement/plan.md#L130-L132)).
- [evidence-recorder-counts](../proposals/evidence-recorder-counts/README.md): skipped tests must not support evidence ([proposals/evidence-recorder-counts/README.md:21-23](../proposals/evidence-recorder-counts/README.md#L21-L23)).
- [aes-durable-docs](../proposals/aes-durable-docs/PLAN.md): a fixed durable document set in 22 repositories; the disproof sample fired ([proposals/aes-durable-docs/PLAN.md:23](../proposals/aes-durable-docs/PLAN.md#L23)).
- [aes-brownfield-docs](../proposals/aes-brownfield-docs/PLAN.md) and [retrofit note](../proposals/aes-brownfield-docs/RETROFIT_NOTE.md): the AES documentation layout applied to existing repositories ([proposals/aes-brownfield-docs/RETROFIT_NOTE.md:45](../proposals/aes-brownfield-docs/RETROFIT_NOTE.md#L45)).
- [aes-learning-loop](../proposals/aes-learning-loop/PLAN.md), [aes-subagent-feedback](../proposals/aes-subagent-feedback/PLAN.md), [aes-feedback-prevention](../proposals/aes-feedback-prevention/PLAN.md): the feedback loop; see [feedback-loop.md](feedback-loop.md) ([proposals/aes-learning-loop/PLAN.md:9](../proposals/aes-learning-loop/PLAN.md#L9)).
- [agent-router](../proposals/agent-router/README.md) and [harness-context](../proposals/harness-context/README.md): see [policy-and-rules.md](policy-and-rules.md) ([proposals/agent-router/README.md:3](../proposals/agent-router/README.md#L3)).
- [worktree-lifecycle](../proposals/worktree-lifecycle/PLAN.md): consistent worktree placement and closeout; runtime requirements planned, not run ([proposals/worktree-lifecycle/VALIDATION.md:13](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/worktree-lifecycle/VALIDATION.md#L13)).
- [code2-ecosystem](../proposals/code2-ecosystem/PLAN.md): the `~/code2` move, redirected 2026-10-13 ([proposals/code2-ecosystem/PLAN.md:21-22](../proposals/code2-ecosystem/PLAN.md#L21-L22)).
- [meeting-claims-true](../proposals/meeting-claims-true/PLAN.md): make the 2026-10-08 meeting claims true ([proposals/meeting-claims-true/PLAN.md:18](../proposals/meeting-claims-true/PLAN.md#L18)).
- [second-brain-evaluation](../proposals/second-brain-evaluation/PLAN.md): measure the Inside Success second brain per feature ([proposals/second-brain-evaluation/PLAN.md:18](../proposals/second-brain-evaluation/PLAN.md#L18)).
- [vision-coverage](../proposals/vision-coverage/README.md): Brian's written vision material found and compiled ([proposals/vision-coverage/README.md:10](../proposals/vision-coverage/README.md#L10)).
- [aes-v0.2-greenfield](../proposals/aes-v0.2-greenfield/README.md): the v0.2 proposal lineage, not authority ([proposals/aes-v0.2-greenfield/README.md:1](../proposals/aes-v0.2-greenfield/README.md#L1)).
