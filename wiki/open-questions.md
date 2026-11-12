---
type: OpenQuestions
title: Open questions
description: Open questions stated in intent documents, documents that disagree with each other or with current facts, claims not checked in this version, and tests to write.
status: current
updated: 2026-11-11
sources: [.project-brain/now.md, docs/planning/DOMAIN.md, docs/planning/next.goal.md, docs/architecture/GOAL.md, docs/architecture/greenfield-v0.2/README.md, README.md, .agentic/repo.yaml, .aes/target.yaml, docs/failure-modes.md, scripts/learning_loop/label_items.py, scripts/learning_loop/systemd/README.md, proposals/aes-learning-loop/PLAN.md, proposals/agent-router/README.md, proposals/harness-context/subagent-research.md, proposals/aes-durable-docs/PLAN.md, docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md, docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md, docs/decisions/0013-truth-lives-where-it-is-edited.md, code2-workspace docs/decisions/0009-aes-and-lockstep-fate.md]
---

# Open questions

These are for Brian; each names what disagrees or what was not checked. [CLAUDE.md:5-8](../CLAUDE.md#L5-L8)
- [Requirements](requirements.md) (related page)
- [History](history.md) (related page)

## Documents that disagree with the current facts

- The project brain still says Lockstep "component delivery is active" (2026-11-07) while its own summary and decision 0009 amendment 1 say Lockstep winds down. [.project-brain/now.md:5](../.project-brain/now.md#L5) [.project-brain/now.md:9](../.project-brain/now.md#L9)
- The accepted-architecture README still calls Lockstep "the active AES component". [docs/architecture/greenfield-v0.2/README.md:15](../docs/architecture/greenfield-v0.2/README.md#L15)
- README.md still says v0.2 governs this repository and names Plan 002 as the current frontier. [README.md:58](../README.md#L58) [README.md:89](../README.md#L89)
- `.agentic/repo.yaml` still names AES-v0.2 as the active line, Plan 002 as the v0.1 active plan, and Enforced Planning as execution governance. [.agentic/repo.yaml:24-41](../.agentic/repo.yaml#L24-L41)
- The goal document's thesis and disproof still rest on "a commit refused without an adopted plan" (Q5). [docs/architecture/GOAL.md:44-46](../docs/architecture/GOAL.md#L44-L46) [docs/planning/DOMAIN.md:53-55](../docs/planning/DOMAIN.md#L53-L55)
- `.aes/target.yaml` still holds the commit rule's outcome OUT-AP-001 (Q15). [.aes/target.yaml:12-21](../.aes/target.yaml#L12-L21)
- Decision 0010 accepted 9 supported criteria; `aes status` later read 2 of 12 (Q6). [docs/planning/DOMAIN.md:56-59](../docs/planning/DOMAIN.md#L56-L59)
- Twenty-three plan adoption receipts say "in progress" while nothing is being continued (Q4). [docs/planning/DOMAIN.md:63-64](../docs/planning/DOMAIN.md#L63-L64)
- The 2026-10-27 goal "AES on hold, checks honest" waits on Brian's call Q1; decision 0009 now retires the target it would repair. [docs/planning/next.goal.md:9](../docs/planning/next.goal.md#L9)
- The failure-mode list says it is the current taxonomy authority, but the labels job reads agent-skills' copy when present. [docs/failure-modes.md:18-20](../docs/failure-modes.md#L18-L20) [scripts/learning_loop/label_items.py:50-54](../scripts/learning_loop/label_items.py#L50-L54)
- The failure-mode list says grouping recurring problems (S3) is not built; the learning-loop plan records S3 demonstrated on 2026-10-08. [docs/failure-modes.md:50-52](../docs/failure-modes.md#L50-L52) [proposals/aes-learning-loop/PLAN.md:268](../proposals/aes-learning-loop/PLAN.md#L268)
- Decision 0013 says wiki catalogs are generated, but this wiki's index hand-writes one-line descriptions. [docs/decisions/0013-truth-lives-where-it-is-edited.md:39-41](../docs/decisions/0013-truth-lives-where-it-is-edited.md#L39-L41)

## Open questions stated in intent documents

- Who turned off the problems, effects and fix-owner timers, and should they run again? Q9's effect count needs the effects job. [scripts/learning_loop/systemd/README.md:9-10](../scripts/learning_loop/systemd/README.md#L9-L10) [proposals/aes-learning-loop/PLAN.md:432](../proposals/aes-learning-loop/PLAN.md#L432)
- Can `code2check` host an edit hook, and how would the Team-Brains gate move? Not checked in decision 0009. [docs/decisions/0009-aes-and-lockstep-fate.md:87-88](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L87-L88)
- Should the agent router continue? Its runtime acceptance was pending on 2026-10-09 and nothing later picks it up. [proposals/agent-router/README.md:3](../proposals/agent-router/README.md#L3)
- Complete Claude/Codex runtime parity remains unverified. [proposals/harness-context/subagent-research.md:176](../proposals/harness-context/subagent-research.md#L176)
- The durable-docs re-sample on 10 gated plans is open. [proposals/aes-durable-docs/PLAN.md:326](../proposals/aes-durable-docs/PLAN.md#L326)
- Whether to resume the Inside Success rollout is Brian's call and was not made. [docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:79-81](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L79-L81)
- Decision 0012 is wrong if the first three plans under the new checklist name no reused capability; that check is outside this repository. [docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md:66-70](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md#L66-L70)

## Not checked in this version

- not checked in this version: the collector ran on 2026-11-10 with 10,756 reports and 0 errors (systemd journal). [docs/decisions/0009-aes-and-lockstep-fate.md:21-23](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L21-L23)
- not checked in this version: Lockstep's `src/pcw` imports this library in 7 files (BrianMills2718/lockstep). [docs/decisions/0009-aes-and-lockstep-fate.md:108-111](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L108-L111)
- not checked in this version: six repositories run `aes` from Makefile targets and twelve hold `.aes/target.yaml` (other repositories). [docs/decisions/0009-aes-and-lockstep-fate.md:16-19](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L16-L19)
- not checked in this version: the pre-commit hook does not run in this checkout because `core.hooksPath` runs lefthook (`.githooks/pre-commit`, git config). [docs/planning/DOMAIN.md:41](../docs/planning/DOMAIN.md#L41)
- not checked in this version: the feedback units still read `~/code/llm_client` and `~/code/observation-to-action-metamodel` after the code2 move (systemd units on the machine). [scripts/learning_loop/systemd/feedback-problems.service:18-23](../scripts/learning_loop/systemd/feedback-problems.service#L18-L23)
- not checked in this version: the vendored `enforced_planning/` is 44,556 lines (`enforced_planning/`). [docs/planning/SYSTEM_MODEL.md:49](../docs/planning/SYSTEM_MODEL.md#L49)
- not checked in this version: which test file covers inert characterization (`tests/greenfield/test_characterize.py`). [.project-brain/now.md:3](../.project-brain/now.md#L3)

## Tests to write

- `scripts/hive/brain_fresh.py` has no test in this repository: write one for the fresh (0), stale (1) and no-brain (2) exits. [scripts/hive/brain_fresh.py:15-17](../scripts/hive/brain_fresh.py#L15-L17)
- A live check that the collector and labels timers are enabled and ran in the last day. [scripts/learning_loop/systemd/README.md:45-47](../scripts/learning_loop/systemd/README.md#L45-L47)
- LL-Q12: a test that a high-impact change produces a notification. [proposals/aes-learning-loop/PLAN.md:435](../proposals/aes-learning-loop/PLAN.md#L435)
- SC-GF-001, SC-GF-005 ER-02, SC-GF-009 and SC-TR-SOURCE-001 ER-02 need runtime or trace observations, not unit tests; with the target retiring, decide whether any moves to OpenSpec. [docs/decisions/0009-aes-and-lockstep-fate.md:58-59](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L58-L59)
- Agent-router AR-1 to AR-8 runtime checks remain planned. [proposals/agent-router/PLAN.md:45-54](../proposals/agent-router/PLAN.md#L45-L54)
- Per-file test results: the recorded run gives folder totals only; a per-file run would show which files hold the 20 skips. [Makefile:548](../Makefile#L548)
