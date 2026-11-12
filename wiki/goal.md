---
type: Goal
title: What AES is now
description: What the Agentic Engineering System is today, who uses it, its scope and non-goals, and where each part lives.
status: current
updated: 2026-11-11
sources: [CLAUDE.md, .project-brain/now.md, .project-brain/project.md, docs/architecture/SYSTEM_BOUNDARY.md, docs/architecture/GOAL.md, docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md, docs/decisions/0013-truth-lives-where-it-is-edited.md, scripts/hive/README.md, proposals/aes-learning-loop/PLAN.md, code2-workspace docs/decisions/0009-aes-and-lockstep-fate.md]
---

# What AES is now

AES is the name for the whole agent system: Lockstep, the feedback loop and the policy layer (Brian, 2026-11-11). [CLAUDE.md:14-16](../CLAUDE.md#L14-L16) [.project-brain/now.md:9](../.project-brain/now.md#L9)
The parts stay where they are, and the map of the whole system is code2-workspace `docs/architecture/model.c4`. [docs/decisions/0009-aes-and-lockstep-fate.md:112-113](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L112-L113)
This repository no longer governs itself: its pre-commit refusal was removed on 2026-10-14 (#789), and no `aes plan accept` step is required before a change. [CLAUDE.md:22-23](../CLAUDE.md#L22-L23)
The older v0.2 description (`.aes/target.yaml`, `aes plan`, `aes evidence`) is kept as a record of how the system worked, not as a rule; see [History](history.md) and [Rationale](rationale.md). [CLAUDE.md:31-32](../CLAUDE.md#L31-L32)

## Where each part lives

| Part | Where it lives | What happens to it | Source |
| --- | --- | --- | --- |
| Feedback loop | `scripts/learning_loop` in this repository, run every night from a clone of AES main at `~/.hive-brain/aes` | kept; keeps running | [.project-brain/now.md:9](../.project-brain/now.md#L9) [docs/decisions/0009-aes-and-lockstep-fate.md:21-23](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L21-L23) [docs/decisions/0009-aes-and-lockstep-fate.md:59-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L59-L61) |
| Rules register | `scripts/rules` and `docs/rules` in this repository | kept; the rest of the policy text (core.md, topic files) lives in code2-workspace `agents/` | [.project-brain/now.md:9](../.project-brain/now.md#L9) |
| Brain freshness check | `scripts/hive/brain_fresh.py` | stays here because other repositories call it by this path; outside decision 0009 | [scripts/hive/README.md:7-9](../scripts/hive/README.md#L7-L9) [docs/decisions/0009-aes-and-lockstep-fate.md:61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L61) |
| Retained library | `src/agentic_engineering_system` | Lockstep's `src/pcw` imports it in 7 files, so it stays while Lockstep runs | [docs/decisions/0009-aes-and-lockstep-fate.md:108-111](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L108-L111) [.project-brain/now.md:9](../.project-brain/now.md#L9) |
| `aes` command line and `.aes/target.yaml` | this repository and twelve consumer repositories | retire one repository at a time, when each is next changed | [docs/decisions/0009-aes-and-lockstep-fate.md:16-19](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L16-L19) [docs/decisions/0009-aes-and-lockstep-fate.md:57-60](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L60) |
| Lockstep | its own repository, BrianMills2718/lockstep, package `pcw` | only for lifelike and Team-Brains, no new users, winds down into `code2check` | [docs/decisions/0009-aes-and-lockstep-fate.md:27](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L27) [docs/decisions/0009-aes-and-lockstep-fate.md:105-108](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L105-L108) |
| Policy layer | code2-workspace `agents/` | outside this repository | [.project-brain/now.md:9](../.project-brain/now.md#L9) |

## Who uses it

- Brian decides business, product and priority calls and anything outward; agents make technical calls, verify them and merge Brian's own pull requests. [.project-brain/project.md:16-19](../.project-brain/project.md#L16-L19)
- Coding agents (Claude Code, Codex, OpenHands) and Project Brains are consumers of Lockstep and AES, not parts of them. [docs/architecture/SYSTEM_BOUNDARY.md:31](../docs/architecture/SYSTEM_BOUNDARY.md#L31)
- Lockstep has two users today: lifelike, whose hook blocks edits, and the Team-Brains Project Brain pull request runner. [docs/decisions/0009-aes-and-lockstep-fate.md:27-31](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L27-L31)
- The feedback loop serves every Claude and Codex agent working in Brian's repositories, the nightly and weekly runs, and Brian as an observer who is notified, not an approver. [proposals/aes-learning-loop/PLAN.md:22-25](../proposals/aes-learning-loop/PLAN.md#L22-L25)

## Scope now

- Keep the feedback loop (`collect_feedback.py`, `label_items.py`, `feedback_log.py`) running. [docs/decisions/0009-aes-and-lockstep-fate.md:59-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L59-L61)
- When a repository holding `.aes/` is next changed, move any live requirement to OpenSpec and remove its `.aes/` folder and `make aes` target with `git rm`, naming decision 0009. [docs/decisions/0009-aes-and-lockstep-fate.md:57-60](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L60)
- Behavior changes go through off-the-shelf tools: OpenSpec for required behavior, lefthook and GitHub Issues (Brian's move of `~/code2`, 2026-10-13). [CLAUDE.md:24-25](../CLAUDE.md#L24-L25)
- The two lasting ideas of the old system, a planned file structure and evidence-computed status, are being carried into the AES structure section under OpenSpec and Lockstep. [CLAUDE.md:25-28](../CLAUDE.md#L25-L28)
- Lockstep's edit-time refusal moves into `code2check` (decision 0009 amendment 1, code2-template#22). [CLAUDE.md:20-22](../CLAUDE.md#L20-L22) [docs/decisions/0009-aes-and-lockstep-fate.md:107-108](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L107-L108)
- Agents read `.project-brain/now.md` first and update it in the same pull request when a change moves where the project stands; `brain_fresh.py` exits 1 when the brain is stale. [CLAUDE.md:5-8](../CLAUDE.md#L5-L8)

## Non-goals

- No restart of the former universal self-governance regime or of its parked issue backlog. [.project-brain/now.md:5](../.project-brain/now.md#L5)
- Open AES issues carry the `on-hold` label; they are parked, not closed. [CLAUDE.md:28-29](../CLAUDE.md#L28-L29)
- No new Lockstep users; for code2 repositories the linkage job is `code2check`'s. [docs/decisions/0009-aes-and-lockstep-fate.md:67](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L67)
- History: v0.2 listed retrofitting arbitrary repositories, universal language support and portfolio orchestration as non-goals. [docs/architecture/GOAL.md:59-64](../docs/architecture/GOAL.md#L59-L64)

## Principles that still hold

- Off-the-shelf first: a capability that a mature standard, package or service could supply is sourced there before anything is built, and apparent novelty is search debt, not a reason to build. [docs/architecture/SYSTEM_BOUNDARY.md:73-75](../docs/architecture/SYSTEM_BOUNDARY.md#L73-L75) [.project-brain/now.md:153](../.project-brain/now.md#L153)
- Project-agnostic architecture stays in `wiki_methodology`; link to it, do not restate it. [CLAUDE.md:101](../CLAUDE.md#L101)
- A fact about one artifact is written inside that artifact; wiki pages route and link. [docs/decisions/0013-truth-lives-where-it-is-edited.md:37-41](../docs/decisions/0013-truth-lives-where-it-is-edited.md#L37-L41)
- Use AI autonomy to multiply human judgment, not to postpone it until its leverage has gone. [docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md:308](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md#L308)

## Related pages

- [Feedback loop](feedback-loop.md): the running part, job by job.
- [Policy and rules](policy-and-rules.md): the rules register, the agent router and the boundary clauses.
- [System model](system-model.md) and [Run and deploy](run-and-deploy.md): what the code is and how it runs.
- [Open questions](open-questions.md): where documents disagree with each other or with the facts above.
