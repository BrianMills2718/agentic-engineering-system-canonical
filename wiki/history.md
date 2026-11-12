---
type: History
title: History
description: The timeline of AES from the canonical bootstrap through v0.2, the commit-rule era, the code2 move, the hold, Lockstep and decision 0009.
status: current
updated: 2026-11-11
sources: [README.md, CLAUDE.md, .project-brain/now.md, .project-brain/project.md, .project-brain/state.md, docs/architecture/GOAL.md, docs/architecture/INITIAL_GAP_LEDGER.md, docs/architecture/SYSTEM_BOUNDARY.md, docs/decisions/0001-canonical-convergence-boundary.md, docs/decisions/0010-greenfield-v0.2-accepted.md, docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md, docs/model/ODD.md, docs/planning/next.goal.md, docs/planning/SYSTEM_MODEL.md, evals/plan-002/README.md, evals/plan-002/P0_RUNBOOK.md, proposals/aes-v0.2-greenfield/README.md, proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md, proposals/aes-planning/README.md, proposals/aes-adopt-existing/README.md, proposals/aes-plan-scope/README.md, proposals/trace-review/README.md, proposals/aes-durable-docs/PLAN.md, proposals/doc-reach-new-docs/PLAN.md, proposals/worktree-lifecycle/PLAN.md, proposals/code2-ecosystem/PLAN.md, research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md]
---

# History

Most material in this repository describes the eras below; none of it is a rule now. [CLAUDE.md:31-32](../CLAUDE.md#L31-L32)
- [Rationale](rationale.md) (related page)
- [Proposals](proposals.md) (related page)

## Before: predecessor repositories (to 2026-09-16)

- `Inside-Success/agentic-engineering-system` and the archived `BrianMills2718/aes` were predecessor sources of mechanisms, decisions and lessons. [README.md:101](../README.md#L101)
- `BrianMills2718/aes` was a 2026-08-24 clean rewrite in a second repository, folded back into the Inside Success repository on 2026-08-26. [research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md:7](../research/synthesis/2026-09-28-legacy-idea-harvest/aes-archived.md#L7)

## v0.1 convergence, Plan 001 and Plan 002 (2026-09-16 to 2026-09-26)

- This repository began on 2026-09-16 as a clean convergence target, so the integrated architecture would not become one more layer inside the old repository. [docs/architecture/GOAL.md:68-72](../docs/architecture/GOAL.md#L68-L72)
- Decision 0001 set the boundary: adopt wiki_methodology by revision, treat incumbents as capability sources, and prove the first implementation across an external consumer. [docs/decisions/0001-canonical-convergence-boundary.md:22-29](../docs/decisions/0001-canonical-convergence-boundary.md#L22-L29)
- Main documents: [SYSTEM_BOUNDARY.md](../docs/architecture/SYSTEM_BOUNDARY.md), [HUMAN_OBSERVABLE_DELIVERY.md](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md), [INITIAL_GAP_LEDGER.md](../docs/architecture/INITIAL_GAP_LEDGER.md) and decisions 0001-0009. [docs/architecture/README.md:7-15](../docs/architecture/README.md#L7-L15)
- Plan 001 (Repository Context Slice 1) was delivered at AES `96fcf5e` on 2026-09-22 for its bounded claim: 15 tests against the pinned data-contracts consumer and a stakeholder "proceed". [README.md:79](../README.md#L79) [README.md:85](../README.md#L85)
- The gap ledger closed the Plan 001 frontier and authorized no next vertical merely because it closed. [docs/architecture/INITIAL_GAP_LEDGER.md:98-104](../docs/architecture/INITIAL_GAP_LEDGER.md#L98-L104)
- Plan 002 (offline policy-decision replay) froze four authentic cases and waited on OpenRouter provider access before its first offline comparison. [README.md:89](../README.md#L89) [evals/plan-002/README.md:9-16](../evals/plan-002/README.md#L9-L16)
- Plan 002's runbook allowed P0 success to authorize only one offline replay, never live hooks or enforcement. [evals/plan-002/P0_RUNBOOK.md:314-328](../evals/plan-002/P0_RUNBOOK.md#L314-L328)
- How it ended: Decision 0011 closed the two v0.1 PRs as superseded, including Plan 002; v0.1 code is retained, not deleted. [docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:95-96](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L95-L96) [docs/decisions/0010-greenfield-v0.2-accepted.md:54-57](../docs/decisions/0010-greenfield-v0.2-accepted.md#L54-L57)

## v0.2 greenfield (2026-09-24 to 2026-10-14)

- The v0.2 proposal re-derived AES from a clean sheet for new projects governed from inception; retrofit was out of scope. [proposals/aes-v0.2-greenfield/README.md:18-20](../proposals/aes-v0.2-greenfield/README.md#L18-L20)
- whygame5, a new WhyGame version, was chosen as the first greenfield consumer. [proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md:121-126](../proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md#L121-L126)
- Probe 0's context A/B on whygame5 could not tell the two arms apart. [proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md:205-212](../proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md#L205-L212)
- Decision 0010 accepted the MVP on 2026-09-25; AES governed its own `src/` and `tests/greenfield/` through `.aes/target.yaml`. [docs/decisions/0010-greenfield-v0.2-accepted.md:36-41](../docs/decisions/0010-greenfield-v0.2-accepted.md#L36-L41) [README.md:58](../README.md#L58)
- Decision 0011 made whygame5's result the next frontier; its value tally came back at 1 AES catch and 6 hand checks. [docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:64-77](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L64-L77)
- Main documents: [docs/architecture/greenfield-v0.2/](../docs/architecture/greenfield-v0.2/README.md), [GETTING_STARTED.md](../docs/greenfield/GETTING_STARTED.md), [planning_protocol.md](../src/agentic_engineering_system/planning_protocol.md). [docs/decisions/0010-greenfield-v0.2-accepted.md:43-53](../docs/decisions/0010-greenfield-v0.2-accepted.md#L43-L53)
- How it ended: AES no longer governs itself and no `aes plan accept` step is required; the engine remains as the library Lockstep pins. [CLAUDE.md:22-23](../CLAUDE.md#L22-L23) [.project-brain/now.md:9](../.project-brain/now.md#L9)

## Hive brain v1 (2026-10-02 to 2026-10-07)

- AES became the home of Brian's personal hive brain v1: Brian, his agents and one brain per project, built from off-the-shelf tools. [.project-brain/project.md:9-11](../.project-brain/project.md#L9-L11)
- Paperclip on personal-vps ran three agents taking jobs from the weekly plan. [.project-brain/state.md:9-12](../.project-brain/state.md#L9-L12)
- How it ended: the hive's scripts and plans moved to BrianMills2718/personal-vps on 2026-10-07; only `brain_fresh.py` stayed here. [.project-brain/now.md:80](../.project-brain/now.md#L80)

## The commit-rule era (2026-10-06 to 2026-10-14)

- Brian asked to lock down `[Unplanned]`: real implementation work only under a plan Company Planning adopted, trivial work decided by measured facts. [proposals/aes-planning/README.md:9](../proposals/aes-planning/README.md#L9) [proposals/aes-planning/README.md:31](../proposals/aes-planning/README.md#L31)
- The design: tags checked against facts and adoption receipts, `[Trivial]` limited by diff size, `[Unplanned]` for emergencies with an `Emergency:` line, observe mode for a week before enforce. [proposals/aes-planning/README.md:66-70](../proposals/aes-planning/README.md#L66-L70)
- Adopt existing: `aes adopt` writes a legacy baseline so an existing repository joins without planning its old files (2026-10-07). [.project-brain/now.md:73-77](../.project-brain/now.md#L73-L77) [proposals/aes-adopt-existing/README.md:23](../proposals/aes-adopt-existing/README.md#L23)
- Plan scope: a Company Planning plan's `conflict_surfaces` let its commits edit the legacy files it declares. [proposals/aes-plan-scope/README.md:23](../proposals/aes-plan-scope/README.md#L23)
- Trace review: every proposal declares whether its work runs a model, agent or pipeline, and traced work must be judged by a full trace read (2026-10-07). [.project-brain/now.md:64-72](../.project-brain/now.md#L64-L72) [proposals/trace-review/README.md:23](../proposals/trace-review/README.md#L23)
- Durable documents: every governed repository keeps a fixed set (goal, requirements, system model, decisions), rolled out to 22 repositories by 2026-10-11. [.project-brain/now.md:11](../.project-brain/now.md#L11) [proposals/aes-durable-docs/PLAN.md:11](../proposals/aes-durable-docs/PLAN.md#L11)
- New documents linked from the wiki: a commit adding a reader document unreachable from `wiki/index.md` was refused. [proposals/doc-reach-new-docs/PLAN.md:8](../proposals/doc-reach-new-docs/PLAN.md#L8)
- Worktree lifecycle: consistent worktree placement and recoverable closeout, merged in AES #481. [proposals/worktree-lifecycle/PLAN.md:12](../proposals/worktree-lifecycle/PLAN.md#L12) [.project-brain/now.md:157](../.project-brain/now.md#L157)
- [Commit-rule skip roots plan](../docs/plans/commit-rule-skip-roots.md): a machine-wide list of throwaway roots exempt from the commit rule.
- [Commit tag contract plan](../docs/plans/commit-tag-contract.md): `aes commit tag` exposing the tag grammar to copied hooks.
- [Shaping navigation and preflight plan](../docs/plans/shaping-nav-preflight.md): `[Shaping]` commits with their navigation, and a preflight verdict before committing.
- [Root-relative links plan](../docs/plans/commit-rule-root-relative-links.md): links starting with `/` resolved against the repository root.
- How it ended: Brian asked on 2026-10-13 to "turn off all the enforcement"; the commit rule and the plan-receipt check were removed on 2026-10-14 (#789). [docs/model/ODD.md:55-57](../docs/model/ODD.md#L55-L57) [CLAUDE.md:22-23](../CLAUDE.md#L22-L23)
- `aes commit`, the commit-msg hook writer, the rollout scripts and their timers are gone, and the machine-wide git hook no longer calls AES. [.project-brain/now.md:57-60](../.project-brain/now.md#L57-L60)

## Feedback loop, harness and router (2026-10-02 onward)

- The learning loop's original design (2026-10-02 to 2026-10-07) is kept as history; the adopted plan, its repair and the start page describe what runs. [proposals/aes-learning-loop/DESIGN.md:3-14](../proposals/aes-learning-loop/DESIGN.md#L3-L14)
- The harness audit and the agent-router design ran on 2026-10-08 and 2026-10-09. [.project-brain/now.md:22-27](../.project-brain/now.md#L22-L27) [.project-brain/now.md:48-52](../.project-brain/now.md#L48-L52)
- How it continues: the feedback loop is kept by decision 0009; see [Feedback loop](feedback-loop.md). [docs/decisions/0009-aes-and-lockstep-fate.md:59-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L59-L61)

## The code2 move (2026-10-13)

- Brian moved `~/code2` to off-the-shelf tools: OpenSpec for required behavior, lefthook and GitHub Issues. [CLAUDE.md:24-25](../CLAUDE.md#L24-L25)
- AES canonical joined code2 as an ordinary repository on 2026-10-13, and the phase 2 plan built on AES enforcement was superseded. [proposals/code2-ecosystem/PLAN.md:25-27](../proposals/code2-ecosystem/PLAN.md#L25-L27)

## The hold (2026-10-18)

- AES was put on hold on 2026-10-18 after the code2 move; the sections of the project brain from before then describe enforcement work that is not being continued. [.project-brain/now.md:9](../.project-brain/now.md#L9)
- A planning package on 2026-10-27 proposed a goal of making the repository's own checks and documents true while on hold, waiting on Brian's call. [docs/planning/next.goal.md:9](../docs/planning/next.goal.md#L9) [docs/planning/SYSTEM_MODEL.md:10-11](../docs/planning/SYSTEM_MODEL.md#L10-L11)

## Lockstep (2026-11-06 to 2026-11-08)

- Brian, 2026-11-06: "lockstep is meant to be part of aes canonical"; AES-SYS-006 records Lockstep as a part in its own repository that pins this library. [docs/architecture/SYSTEM_BOUNDARY.md:29-33](../docs/architecture/SYSTEM_BOUNDARY.md#L29-L33)
- Lockstep's delivery added two narrow library increments: required evidence inputs (2026-11-07) and inert Git inspection (2026-11-08). [.project-brain/now.md:3](../.project-brain/now.md#L3) [.project-brain/now.md:7](../.project-brain/now.md#L7)

## Decision 0009 (2026-11-10 and 2026-11-11)

- Brian approved retiring the `aes` command line repository by repository, keeping the feedback loop, and merging Lockstep's linkage into `code2check` in stages. [docs/decisions/0009-aes-and-lockstep-fate.md:3-7](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L3-L7)
- Amendment 1 (2026-11-11): Lockstep winds down, its edit-time refusal moves into `code2check`, and AES stays the name for the whole system. [docs/decisions/0009-aes-and-lockstep-fate.md:98-113](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L98-L113)
