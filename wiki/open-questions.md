---
type: Questions
title: Open questions
description: Open questions, document disagreements, unchecked claims and tests to write
status: current
last_checked: 2026-11-11
---

# Open questions

## Documents that disagree with the current state

1. GOAL.md's thesis and disproof still rest on the commit rule ([docs/architecture/GOAL.md:44-46](../docs/architecture/GOAL.md#L44-L46)) ([docs/architecture/GOAL.md:54-57](../docs/architecture/GOAL.md#L54-L57)), which was removed on 2026-10-14 ([CLAUDE.md:22-23](../CLAUDE.md#L22-L23)); DOMAIN.md records this as Q5 ([docs/planning/DOMAIN.md:53-55](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L53-L55)).
2. GOAL.md's requirements overview still names outcome OUT-AP-001, real work landing only under an adopted plan ([docs/architecture/GOAL.md:13-15](../docs/architecture/GOAL.md#L13-L15)); the rule enforcing it was removed (Q15) ([docs/planning/DOMAIN.md:60-61](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L60-L61)).
3. Decision 0010 says 9 criteria supported, while `aes status` reported 2 of 12 on 2026-10-27, because three criteria were added and 15 observations depended on deleted `commit_rule.py` (Q6) ([docs/planning/DOMAIN.md:56-59](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L56-L59)).
4. AGENTS.md and CLAUDE.md describe a pre-commit hook that refuses unplanned files, which does not run in this checkout (Q16) ([docs/planning/DOMAIN.md:62](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L62)) ([docs/planning/DOMAIN.md:41](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L41)); both files mark that text as history ([CLAUDE.md:31-32](../CLAUDE.md#L31-L32)).
5. `.project-brain/project.md` still lists "AES governs itself" as approved ([.project-brain/project.md:12-15](../.project-brain/project.md#L12-L15)), superseded by [CLAUDE.md:22-23](../CLAUDE.md#L22-L23); the brain owner should update it.
6. Adoption receipts say 23 plans are adopted and in progress while the project brain says nothing is continued (Q4) ([docs/planning/DOMAIN.md:63-64](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L63-L64)).
7. `docs/planning/next.goal.md` is a proposed goal waiting on Brian's Q1 ([docs/planning/next.goal.md:9](../docs/planning/next.goal.md#L9)); code2-workspace decision 0009 now retires `aes` per repository ([docs/decisions/0009-aes-and-lockstep-fate.md:57-60](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L60)), so whether that goal still applies is open.
8. `docs/failure-modes.md` says assigning families to log records "is not built yet" ([docs/failure-modes.md:50-52](../docs/failure-modes.md#L50-L52)), but the labels job now labels each feedback issue with a family ([scripts/learning_loop/systemd/README.md:20](../scripts/learning_loop/systemd/README.md#L20)).
9. `docs/greenfield/GETTING_STARTED.md` teaches the `aes` lifecycle ([docs/greenfield/GETTING_STARTED.md:3-9](../docs/greenfield/GETTING_STARTED.md#L3-L9)), which retires one repository at a time ([docs/decisions/0009-aes-and-lockstep-fate.md:57-60](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L60)).
10. `docs/model/ODD.md` models the v0.2 governance loop and leaves out the v0.1 line, `aes adopt` and vendored `enforced_planning/` ([docs/model/ODD.md:47-49](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/model/ODD.md#L47-L49)); it does not model the feedback loop, Lockstep or the policy layer.

## Open questions from intent documents

11. Feedback loop: the weekly analysis, effects and fix-owner timers are off and nobody recorded why; should they run again? ([scripts/learning_loop/systemd/README.md:4-10](../scripts/learning_loop/systemd/README.md#L4-L10)).
12. Feedback loop Q9: the 30-day effect count after the first enforced rule was due 2026-11-07 and no result is recorded ([proposals/aes-learning-loop/PLAN.md:432](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/PLAN.md#L432)).
13. Feedback loop Q12: nothing notifies Brian of a high-impact change yet ([proposals/aes-learning-loop/PLAN.md:435](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/PLAN.md#L435)).
14. Feedback loop Q13 last reported 9 workspace rules unregistered ([proposals/aes-learning-loop/PLAN.md:436](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/PLAN.md#L436)).
15. The fixed-core (level-3) list of the feedback loop is Brian's to set ([proposals/aes-learning-loop/DESIGN.md:207](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/DESIGN.md#L207)).
16. The acceptable-family judgments behind the 8/10 measurement are Claude's, and Brian has not spot-checked the labels ([proposals/aes-learning-loop/DESIGN.md:208-210](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/DESIGN.md#L208-L210)) ([datasets/learning-loop/README.md:31](../datasets/learning-loop/README.md#L31)).
17. Family Z's narrow wording was tuned once on the held-out set, so that set is no longer fully held out for Z ([datasets/learning-loop/experiments/2026-11-05-family-z/README.md:27-29](../datasets/learning-loop/experiments/2026-11-05-family-z/README.md#L27-L29)).
18. Durable-documents rule: the re-sample on the first 10 plans gated by `OV-DURABLE-DOCS-DECLARED` is pending ([proposals/aes-durable-docs/PLAN.md:96](../proposals/aes-durable-docs/PLAN.md#L96)) ([.project-brain/now.md:11](../.project-brain/now.md#L11)).
19. Lockstep: whether `code2check` can host an edit hook and how the Team-Brains gate moves were not checked ([docs/decisions/0009-aes-and-lockstep-fate.md:86-88](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L86-L88)).
20. Decision 0011 item 4: whether to resume the Inside Success team rollout is Brian's call and has not been made ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:79-81](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L79-L81)).
21. Agent router: runtime acceptance, native dispatch and observation periods remain pending ([proposals/agent-router/README.md:9](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/agent-router/README.md#L9)).
22. Harness parity: full child enforcement and hook parity remain unproved ([.project-brain/now.md:46-47](../.project-brain/now.md#L46-L47)).
23. Evidence recorder counts: the skip-only repair is reproduced but unimplemented ([.project-brain/now.md:53-54](../.project-brain/now.md#L53-L54)).

## Not checked in this version

24. Not checked in this version: that `code2check` gained Lockstep's edit-time refusal (code2-template#22) ([CLAUDE.md:20-22](../CLAUDE.md#L20-L22)).
25. Not checked in this version: which feedback timers are enabled today; the last record is 2026-11-10 ([scripts/learning_loop/systemd/README.md:5-7](../scripts/learning_loop/systemd/README.md#L5-L7)).
26. Not checked in this version: the module contents behind the generated glossary's file and line mappings (`src/agentic_engineering_system/*.py`) ([docs/planning/DOMAIN.md:7-8](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L7-L8)).

## Tests to run or write

27. Run the covering tests of REQ-01, REQ-02, REQ-04, REQ-05, REQ-07 to REQ-15 on [requirements.md](requirements.md), each by file ([pyproject.toml:38-41](../pyproject.toml#L38-L41)).
28. Write a test that characterization does not invoke a configured fsmonitor command (REQ-03) ([openspec/specs/inert-characterization/spec.md:15-19](../openspec/specs/inert-characterization/spec.md#L15-L19)).
29. Write or name a test that an observation at a squashed-away commit is UNREACHABLE (REQ-06) ([docs/decisions/0010-greenfield-v0.2-accepted.md:126](../docs/decisions/0010-greenfield-v0.2-accepted.md#L126)).
