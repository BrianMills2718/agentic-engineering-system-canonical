---
type: Index
title: AES canonical wiki
description: Front door for the Agentic Engineering System, what it is now and where to read next
status: current
last_checked: 2026-11-11
---

# Agentic Engineering System (AES)

This wiki is derived navigation, not an authority; follow links to the owning documents ([CLAUDE.md:106](../CLAUDE.md#L106)).

## What AES is now

- AES is the name for the whole agent system, with three parts ([CLAUDE.md:14-16](../CLAUDE.md#L14-L16)).
- Lockstep: its own repository, kept only for lifelike and Team-Brains, no new users, winding down into `code2check` ([CLAUDE.md:18-22](../CLAUDE.md#L18-L22)).
- The feedback loop: `scripts/learning_loop`, run nightly by systemd timers ([.project-brain/now.md:9](../.project-brain/now.md#L9)).
- The policy layer: the rules register in `docs/rules` and `scripts/rules`, with Brian's agent rules in code2-workspace `agents/` ([.project-brain/now.md:9](../.project-brain/now.md#L9)).
- The `aes` command line and `.aes/target.yaml` retire one repository at a time, and AES no longer governs itself ([CLAUDE.md:17-23](../CLAUDE.md#L17-L23)).
- Read [.project-brain/now.md](../.project-brain/now.md) first ([CLAUDE.md:5](../CLAUDE.md#L5)).

## Start from your question

| Question | Page | Grounded in |
| --- | --- | --- |
| What is AES for, who uses it, what is out of scope? | [goal.md](goal.md) | [CLAUDE.md:14-23](../CLAUDE.md#L14-L23) |
| What is Lockstep and how does it wind down? | [lockstep.md](lockstep.md) | [docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29) |
| How does the feedback loop work and what runs today? | [feedback-loop.md](feedback-loop.md) | [scripts/learning_loop/systemd/README.md:3-7](../scripts/learning_loop/systemd/README.md#L3-L7) |
| Where are the rules and standing policies? | [policy-and-rules.md](policy-and-rules.md) | [docs/rules/RULES.md:3](../docs/rules/RULES.md#L3) |
| What exists in the code and where is data stored? | [system-model.md](system-model.md) | [pyproject.toml:26-28](../pyproject.toml#L26-L28) |
| How do I install, test and run the jobs? | [run-and-deploy.md](run-and-deploy.md) | [Makefile:543-553](../Makefile#L543-L553) |
| Which requirements have tests? | [requirements.md](requirements.md) | [openspec/specs/required-evidence-inputs/spec.md:13](../openspec/specs/required-evidence-inputs/spec.md#L13) |
| What is unresolved or contradicts current state? | [open-questions.md](open-questions.md) | [docs/planning/DOMAIN.md:51-64](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/docs/planning/DOMAIN.md#L51-L64) |
| What happened before (v0.1, v0.2, the commit rule)? | [history.md](history.md) | [CLAUDE.md:31-32](../CLAUDE.md#L31-L32) |
| What did the research syntheses conclude? | [research-and-lessons.md](research-and-lessons.md) | [research/README.md:29](../research/README.md#L29) |

## Decision record

This repository's decisions; code2-workspace decision 0009 (AES and Lockstep fate) is a different decision ([docs/decisions/0009-aes-and-lockstep-fate.md:27-28](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L27-L28)), summarised on [lockstep.md](lockstep.md).

- [0001](../docs/decisions/0001-canonical-convergence-boundary.md): clean canonical repository and convergence boundary (2026-09-16).
- [0002](../docs/decisions/0002-company-planning-aes-profile-before-fork.md): an AES profile over Company Planning before any fork (2026-09-17).
- [0003](../docs/decisions/0003-component-local-normative-context-and-symbol-inheritance.md): component-local normative context, symbols inherit scope (2026-09-17).
- [0004](../docs/decisions/0004-compact-structured-normative-records-and-generated-views.md): compact structured normative records with generated views (2026-09-17).
- [0005](../docs/decisions/0005-aes-component-scope-and-consequential-seam-typing.md): component is a governance scope; type only consequential seams (2026-09-17).
- [0006](../docs/decisions/0006-minimal-architecture-realization-json-schema.md): minimal architecture-realization JSON Schema (2026-09-17).
- [0007](../docs/decisions/0007-provider-independent-verification-and-blob-evidence-carry-forward.md): blob-level evidence carry-forward, superseded by 0008 (2026-09-18).
- [0008](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md): provider-independent verification over the transitive executed subject (2026-09-18).
- [0009](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md): modular product design without a parallel ACA platform (2026-09-22).
- [0010](../docs/decisions/0010-greenfield-v0.2-accepted.md): AES v0.2 greenfield MVP accepted as realized (2026-09-25), now history.
- [0011](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md): this repository is AES; the Inside Success repository is archived (2026-09-26).
- [0012](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md): capability reuse checked against one catalogue (2026-10-08).
- [0013](../docs/decisions/0013-truth-lives-where-it-is-edited.md): truth lives where it is edited (2026-10-10).

### Status documents (status as last written, not verified)

- [.project-brain/state.md](../.project-brain/state.md)
- [docs/planning/cold-review.md](../docs/planning/cold-review.md)
- [proposals/aes-v0.2-greenfield/07-semantic-clean-sheet-review-pass-1.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-v0.2-greenfield/07-semantic-clean-sheet-review-pass-1.md)
- [proposals/aes-v0.2-greenfield/08-semantic-clean-sheet-review-pass-2.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-v0.2-greenfield/08-semantic-clean-sheet-review-pass-2.md)
- [proposals/aes-v0.2-greenfield/09-semantic-clean-sheet-review-pass-3-topology.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-v0.2-greenfield/09-semantic-clean-sheet-review-pass-3-topology.md)
- [proposals/aes-v0.2-greenfield/11-semantic-clean-sheet-review-pass-4-target-analysis.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-v0.2-greenfield/11-semantic-clean-sheet-review-pass-4-target-analysis.md)
- [proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md)
- [proposals/aes-v0.2-greenfield/REVIEW.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-v0.2-greenfield/REVIEW.md)
- [proposals/code2-ecosystem/hookspath-review.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/code2-ecosystem/hookspath-review.md)
- [proposals/trace-review/trace-review.goal.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/trace-review/trace-review.goal.md)
- [research/investigations/2026-09-16-first-vertical-capability-discovery.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-16-first-vertical-capability-discovery.md)
- [research/investigations/2026-09-16-repository-context-provider-landscape.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-16-repository-context-provider-landscape.md)
- [research/investigations/2026-09-17-aca-tosca-capability-fit-test.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-aca-tosca-capability-fit-test.md)
- [research/investigations/2026-09-17-aes-evidence-prov-intoto-slsa-fit-test.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-aes-evidence-prov-intoto-slsa-fit-test.md)
- [research/investigations/2026-09-17-backstage-tosca-sysml-topology-fit.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-backstage-tosca-sysml-topology-fit.md)
- [research/investigations/2026-09-17-external-provider-deep-dive-round-2.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-external-provider-deep-dive-round-2.md)
- [research/investigations/2026-09-17-external-sourcing-audit-before-canonical-stub.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-external-sourcing-audit-before-canonical-stub.md)
- [research/investigations/2026-09-17-opa-aes-policy-fit-test.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-opa-aes-policy-fit-test.md)
- [research/investigations/2026-09-17-open-workflow-spec-vs-enforced-planning.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-open-workflow-spec-vs-enforced-planning.md)
- [research/investigations/2026-09-17-ows-enforced-planning-work-graph-fit-test.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-ows-enforced-planning-work-graph-fit-test.md)
- [research/investigations/2026-09-17-scip-planned-subject-fit-test.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/investigations/2026-09-17-scip-planned-subject-fit-test.md)
- [research/synthesis/2026-09-17-fresh-agent-handoff.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/synthesis/2026-09-17-fresh-agent-handoff.md)
- [research/synthesis/incumbent-capability-inventory.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/synthesis/incumbent-capability-inventory.md)
- [research/synthesis/representation-review-and-epistemic-surface-suggestions-for-aes.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/synthesis/representation-review-and-epistemic-surface-suggestions-for-aes.md)

### Plans

- [docs/plans/](../docs/plans/): numbered and named plans, kept as written.
- [proposals/](../proposals/README.md): proposal folders, kept as written; [history.md](history.md) lists each by name.

### Documents that stay as written

- [CLAUDE.md](../CLAUDE.md) and [AGENTS.md](../AGENTS.md): instruction files; AGENTS.md is generated from CLAUDE.md.
- [.project-brain/now.md](../.project-brain/now.md), [project.md](../.project-brain/project.md), [truth.md](../.project-brain/truth.md): the project brain, read first.
- [docs/architecture/](../docs/architecture/README.md): normative target, including [SYSTEM_BOUNDARY.md](../docs/architecture/SYSTEM_BOUNDARY.md), [GOAL.md](../docs/architecture/GOAL.md), [HUMAN_OBSERVABLE_DELIVERY.md](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md), [INITIAL_GAP_LEDGER.md](../docs/architecture/INITIAL_GAP_LEDGER.md) and [greenfield-v0.2/](../docs/architecture/greenfield-v0.2/README.md).
- [docs/decisions/](../docs/decisions/): the decision record.
- [openspec/specs/required-evidence-inputs](../openspec/specs/required-evidence-inputs/spec.md) and [openspec/specs/inert-characterization](../openspec/specs/inert-characterization/spec.md): required behavior.
- [docs/rules/RULES.md](../docs/rules/RULES.md): generated from the register.
- [.claude/commands/opsx/](../.claude/commands/opsx/apply.md): OpenSpec commands read by Claude Code.
- [planning_protocol.md](../src/agentic_engineering_system/planning_protocol.md): planned artifact of the retained engine.
- [scripts/learning_loop/systemd/README.md](../scripts/learning_loop/systemd/README.md), [scripts/hive/README.md](../scripts/hive/README.md), [datasets/learning-loop/README.md](../datasets/learning-loop/README.md), [research/README.md](../research/README.md): folder guides.

### History

- [history.md](history.md): v0.1, v0.2 self-governance, the commit rule and its removal, the move to code2, the proposals by name.
- [docs/greenfield/GETTING_STARTED.md](../docs/greenfield/GETTING_STARTED.md): the v0.2 `aes` walkthrough.
- [docs/model/ODD.md](../docs/model/ODD.md): the v0.2 governance loop model.
- [docs/planning/SYSTEM_MODEL.md](../docs/planning/SYSTEM_MODEL.md), [DOMAIN.md](../docs/planning/DOMAIN.md), [next.goal.md](../docs/planning/next.goal.md): the 2026-10-27 planning package.
- [docs/plans/001_repository_context_resolution_vertical.md](../docs/plans/001_repository_context_resolution_vertical.md) and [docs/plans/002_offline_policy_decision_replay.md](../docs/plans/002_offline_policy_decision_replay.md): the v0.1 plans.
- [proposals/aes-durable-docs/review-page/modeling-review.html](../proposals/aes-durable-docs/review-page/modeling-review.html): the 2026-10-11 modeling work review.
- [proposals/planning-package/review-page/index.html](../proposals/planning-package/review-page/index.html): the planning package review page.
- [docs/terms/ecosystem-terms.md](../docs/terms/ecosystem-terms.md): Brian's reasoning vocabulary.
- [research-and-lessons.md](research-and-lessons.md): research syntheses.

### Every other document

- [documents.md](documents.md): every other document in the repository, by folder, kept as written.
