# Agentic Engineering System (AES) wiki

AES is the name for the whole agent system: Lockstep, the feedback loop and the policy layer (Brian, 2026-11-11). [CLAUDE.md:14-16](../CLAUDE.md#L14-L16) [.project-brain/now.md:9](../.project-brain/now.md#L9)
Under code2-workspace decision 0009 the feedback loop keeps running, the `aes` command line and `.aes/target.yaml` retire one repository at a time, and Lockstep winds down into `code2check`. [docs/decisions/0009-aes-and-lockstep-fate.md:57-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L61) [docs/decisions/0009-aes-and-lockstep-fate.md:105-108](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L105-L108)
Most older material here (decisions 0001-0013, docs/architecture, docs/greenfield, most proposals, plans and research) describes the v0.1 line and the retired v0.2 self-governance regime: read it as history, not as rules. [CLAUDE.md:22-23](../CLAUDE.md#L22-L23) [CLAUDE.md:31-32](../CLAUDE.md#L31-L32)

## What AES is now

- [Goal](goal.md): what AES is, who uses it, scope, non-goals, where each part lives.
- [Glossary](glossary.md): the names a reader meets.
- [Open questions](open-questions.md): disagreements, unchecked claims, tests to write.
- [.project-brain/now.md](../.project-brain/now.md): current state; read first.
- [CLAUDE.md](../CLAUDE.md): instructions for agents in this repository; [AGENTS.md](../AGENTS.md) is its generated copy.

## The running parts

- [Feedback loop](feedback-loop.md): each job, when it runs, what it reads and writes.
- [Policy and rules](policy-and-rules.md): the rules register, agent router and boundary clauses.
- [Feedback jobs guide](../scripts/learning_loop/systemd/README.md): commands, outputs, failure behavior.
- [Rules agents follow](../docs/rules/RULES.md): the generated rules page.
- [Failure modes](../docs/failure-modes.md): the label taxonomy.

## How it is built and run

- [System model](system-model.md): packages, entry points, data flow, storage, dependencies.
- [Run and deploy](run-and-deploy.md): install, test, timers, retiring commands.
- [Requirements](requirements.md): every requirement with its test result.
- [README.md](../README.md): repository front page (history in parts).

## Decisions and history

- [Rationale](rationale.md): every decision with its standing now.
- [History](history.md): the eras from v0.1 to decision 0009.
- [Decision records](../docs/decisions/0010-greenfield-v0.2-accepted.md): see the full list below.

## Plans and proposals

- [Proposals and plans](proposals.md): every proposal folder and plan file.
- [proposals/README.md](../proposals/README.md): the proposals folder guide.
- [docs/plans/README.md](../docs/plans/README.md): the plans folder guide.

## Research

- [Research findings](research.md): findings that still matter and the investigations.
- [research/README.md](../research/README.md): the research folder guide.

## Status documents (status as last written, not verified)

#### docs/planning
- [cold-review.md](../docs/planning/cold-review.md)

#### evidence
- [README.md](../evidence/README.md)
- [clean-user-run-2026-09-25.md](../evidence/greenfield/clean-user-run-2026-09-25.md)
- [clean-user-run-2-2026-09-25.md](../evidence/greenfield/clean-user-run-2-2026-09-25.md)
- [clean-user-run-3-2026-09-25.md](../evidence/greenfield/clean-user-run-3-2026-09-25.md)
- [clean-user-run-4-2026-10-04.md](../evidence/greenfield/clean-user-run-4-2026-10-04.md)
- [context-ab preregistration](../evidence/greenfield/context-ab-2026-09-25/preregistration.md)
- [context-ab result](../evidence/greenfield/context-ab-2026-09-25/result.md)
- [modular-design-integration-2026-09-22.md](../evidence/modular-design-integration-2026-09-22.md)
- [plan-001 characterization 320991b](../evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/characterization.md)
- [plan-001 characterization 96fcf5e](../evidence/plan-001/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1/characterization.md)
- [plan-001 A1 53be16f](../evidence/plan-001/a1/53be16fa1159f31648773062531d751c85d7a011.md)
- [plan-001 A1 96fcf5e](../evidence/plan-001/a1/96fcf5e89ba98ad9ff278ec536a98c308cda3fe1.md)
- [pr5-integration-readiness-2026-09-18.md](../evidence/plan-001/pr5-integration-readiness-2026-09-18.md)

#### proposals
- [aes-durable-docs m4 AES cold reader](../proposals/aes-durable-docs/evidence/m4-aes-canonical-cold-reader-review.md)
- [aes-durable-docs m4 company-planning cold reader](../proposals/aes-durable-docs/evidence/m4-company-planning-cold-reader-review.md)
- [aes-durable-docs m5 rollout](../proposals/aes-durable-docs/evidence/m5-rollout.md)
- [aes-planning ROLLOUT.md](../proposals/aes-planning/ROLLOUT.md)
- [v0.2 review pass 1](../proposals/aes-v0.2-greenfield/07-semantic-clean-sheet-review-pass-1.md)
- [v0.2 review pass 2](../proposals/aes-v0.2-greenfield/08-semantic-clean-sheet-review-pass-2.md)
- [v0.2 review pass 3](../proposals/aes-v0.2-greenfield/09-semantic-clean-sheet-review-pass-3-topology.md)
- [v0.2 review pass 4](../proposals/aes-v0.2-greenfield/11-semantic-clean-sheet-review-pass-4-target-analysis.md)
- [v0.2 roadmap 25](../proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md)
- [v0.2 REVIEW.md](../proposals/aes-v0.2-greenfield/REVIEW.md)
- [code2 hooks-path review](../proposals/code2-ecosystem/hookspath-review.md)
- [commit-rule-notes-report goal](../proposals/commit-rule-notes-report/commit-rule-notes-report.goal.md)
- [commit-rule-notes-report plan](../proposals/commit-rule-notes-report/commit-rule-notes-report.md)
- [trace-review goal](../proposals/trace-review/trace-review.goal.md)

#### research/investigations
- [README.md](../research/investigations/README.md)
- [first vertical capability discovery](../research/investigations/2026-09-16-first-vertical-capability-discovery.md)
- [repository context provider landscape](../research/investigations/2026-09-16-repository-context-provider-landscape.md)
- [ACA/TOSCA capability fit](../research/investigations/2026-09-17-aca-tosca-capability-fit-test.md)
- [PROV/in-toto/SLSA fit](../research/investigations/2026-09-17-aes-evidence-prov-intoto-slsa-fit-test.md)
- [Backstage/TOSCA/SysML fit](../research/investigations/2026-09-17-backstage-tosca-sysml-topology-fit.md)
- [external provider deep dive round 2](../research/investigations/2026-09-17-external-provider-deep-dive-round-2.md)
- [external sourcing audit](../research/investigations/2026-09-17-external-sourcing-audit-before-canonical-stub.md)
- [OPA policy fit](../research/investigations/2026-09-17-opa-aes-policy-fit-test.md)
- [OPA Enforced Planning probe](../research/investigations/2026-09-17-opa-enforced-planning-policy-probe.md)
- [Open Workflow Spec vs Enforced Planning](../research/investigations/2026-09-17-open-workflow-spec-vs-enforced-planning.md)
- [OWS work-graph fit](../research/investigations/2026-09-17-ows-enforced-planning-work-graph-fit-test.md)
- [PROV/in-toto projection probe](../research/investigations/2026-09-17-prov-intoto-aes-verification-projection-probe.md)
- [SCIP planned-subject fit](../research/investigations/2026-09-17-scip-planned-subject-fit-test.md)
- [TOSCA/ACA projection probe](../research/investigations/2026-09-17-tosca-aca-capability-projection-probe.md)

#### research/synthesis
- [fresh-agent handoff 2026-09-17](../research/synthesis/2026-09-17-fresh-agent-handoff.md)
- [normative-component alignment checkpoint](../research/synthesis/2026-09-17-normative-component-alignment-dogfood-checkpoint.md)
- [source-local context dogfood result](../research/synthesis/2026-09-17-source-local-context-dogfood-result.md)
- [evidence, characterization and context suggestions](../research/synthesis/aes-evidence-characterization-and-context-suggestions.md)
- [incumbent capability inventory](../research/synthesis/incumbent-capability-inventory.md)
- [representation review and epistemic surface suggestions](../research/synthesis/representation-review-and-epistemic-surface-suggestions-for-aes.md)

## Documents that stay as written

#### Instruction and state files (named read-first by CLAUDE.md)
- [README.md](../README.md): repository front page.
- [.project-brain/now.md](../.project-brain/now.md), [project.md](../.project-brain/project.md), [state.md](../.project-brain/state.md), [truth.md](../.project-brain/truth.md): the project brain.

#### Architecture and decisions (named by CLAUDE.md or accepted records)
- [SYSTEM_BOUNDARY.md](../docs/architecture/SYSTEM_BOUNDARY.md): boundary clauses, including AES-SYS-006.
- [GOAL.md](../docs/architecture/GOAL.md): declared durable goal document.
- [HUMAN_OBSERVABLE_DELIVERY.md](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md): delivery constraints named by CLAUDE.md.
- [INITIAL_GAP_LEDGER.md](../docs/architecture/INITIAL_GAP_LEDGER.md): v0.1 gap record named by CLAUDE.md.
- [docs/architecture/README.md](../docs/architecture/README.md): folder guide.
- [greenfield-v0.2/README.md](../docs/architecture/greenfield-v0.2/README.md), [13 materialization](../docs/architecture/greenfield-v0.2/13-greenfield-materialization.md), [23 CLI contract](../docs/architecture/greenfield-v0.2/23-greenfield-cli-product-contract.md): accepted v0.2 architecture, kept as a record.
- [0001](../docs/decisions/0001-canonical-convergence-boundary.md), [0002](../docs/decisions/0002-company-planning-aes-profile-before-fork.md), [0003](../docs/decisions/0003-component-local-normative-context-and-symbol-inheritance.md), [0004](../docs/decisions/0004-compact-structured-normative-records-and-generated-views.md), [0005](../docs/decisions/0005-aes-component-scope-and-consequential-seam-typing.md), [0006](../docs/decisions/0006-minimal-architecture-realization-json-schema.md), [0007](../docs/decisions/0007-provider-independent-verification-and-blob-evidence-carry-forward.md), [0008](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md), [0009](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md), [0010](../docs/decisions/0010-greenfield-v0.2-accepted.md), [0011](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md), [0012](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md), [0013](../docs/decisions/0013-truth-lives-where-it-is-edited.md): decision records stay as written.
- [docs/model/ODD.md](../docs/model/ODD.md): declared durable system model, read by the planning build script.
- [docs/greenfield/GETTING_STARTED.md](../docs/greenfield/GETTING_STARTED.md): read by `tests/greenfield/test_distribution.py`.

#### Planning, specs, terms and generated pages
- [docs/planning/DOMAIN.md](../docs/planning/DOMAIN.md), [SYSTEM_MODEL.md](../docs/planning/SYSTEM_MODEL.md), [next.goal.md](../docs/planning/next.goal.md): planning package, stays per the brief.
- [openspec/specs/inert-characterization/spec.md](../openspec/specs/inert-characterization/spec.md), [openspec/specs/required-evidence-inputs/spec.md](../openspec/specs/required-evidence-inputs/spec.md): current required behavior.
- [docs/terms/ecosystem-terms.md](../docs/terms/ecosystem-terms.md): Brian's term list.
- [docs/rules/RULES.md](../docs/rules/RULES.md): generated by `scripts/rules/build_rules_page.py`.
- [docs/failure-modes.md](../docs/failure-modes.md): label taxonomy read by `scripts/learning_loop`.
- [planning_protocol.md](../src/agentic_engineering_system/planning_protocol.md): packaged with the library.

#### Feedback-loop documents read by code
- [proposals/aes-learning-loop/DESIGN.md](../proposals/aes-learning-loop/DESIGN.md), [PLAN.md](../proposals/aes-learning-loop/PLAN.md): named by the learning-loop scripts and services.
- [scripts/learning_loop/systemd/README.md](../scripts/learning_loop/systemd/README.md): named by the units.
- [proposals/agent-router/PLAN.md](../proposals/agent-router/PLAN.md): named by `scripts/rules/sort_legacy.py`.
- [proposals/code2-ecosystem/workspace/AGENTS.md](../proposals/code2-ecosystem/workspace/AGENTS.md): source of `~/code2/AGENTS.md`.

#### Lineage kept in place (Decision 0010)
- [proposals/aes-v0.2-greenfield/](../proposals/aes-v0.2-greenfield/README.md): [01](../proposals/aes-v0.2-greenfield/01-design-thesis.md), [05](../proposals/aes-v0.2-greenfield/05-donor-reentry.md), [06](../proposals/aes-v0.2-greenfield/06-open-questions.md), [10](../proposals/aes-v0.2-greenfield/10-greenfield-mvp-validation-profile.md), [13](../proposals/aes-v0.2-greenfield/13-greenfield-materialization.candidate.md), [18](../proposals/aes-v0.2-greenfield/18-provider-evaluation-round-1.md), [19](../proposals/aes-v0.2-greenfield/19-provider-evaluation-round-2-generic-dependencies.md), [22](../proposals/aes-v0.2-greenfield/22-portable-provider-boundaries.md), [23](../proposals/aes-v0.2-greenfield/23-greenfield-cli-product-contract.md), [24](../proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md).

#### Goal launchers (generated by Company Planning; edit the plan, not these)
- [aes-adopt-existing](../proposals/aes-adopt-existing/aes-adopt-existing.goal.md), [aes-brownfield-docs](../proposals/aes-brownfield-docs/aes-brownfield-docs.goal.md), [aes-durable-docs](../proposals/aes-durable-docs/aes-durable-docs.goal.md), [aes-feedback-prevention](../proposals/aes-feedback-prevention/aes-feedback-prevention.goal.md), [aes-learning-loop](../proposals/aes-learning-loop/aes-learning-loop.goal.md), [aes-plan-scope](../proposals/aes-plan-scope/aes-plan-scope.goal.md), [aes-planning](../proposals/aes-planning/aes-planning.goal.md), [aes-subagent-feedback](../proposals/aes-subagent-feedback/aes-subagent-feedback.goal.md), [agent-router](../proposals/agent-router/agent-router.goal.md), [agent-router revision](../proposals/agent-router/revision.goal.md), [code2-ecosystem](../proposals/code2-ecosystem/code2-ecosystem.goal.md), [commit-rule-followups](../proposals/commit-rule-followups/commit-rule-followups.goal.md), [commit-tag-case](../proposals/commit-tag-case/commit-tag-case.goal.md), [doc-reach-new-docs](../proposals/doc-reach-new-docs/doc-reach-new-docs.goal.md), [harness-context](../proposals/harness-context/harness-context.goal.md), [meeting-claims-true](../proposals/meeting-claims-true/meeting-claims-true.goal.md), [second-brain-evaluation](../proposals/second-brain-evaluation/second-brain-evaluation.goal.md), [worktree-lifecycle](../proposals/worktree-lifecycle/worktree-lifecycle.goal.md), [worktree-plan-lookup](../proposals/worktree-plan-lookup/worktree-plan-lookup.goal.md).

#### Folder guides (each describes only its own folder)
- [.agentic/events/README.md](../.agentic/events/README.md), [archive/v0.1-placeholders/README.md](../archive/v0.1-placeholders/README.md), [datasets/README.md](../datasets/README.md), [datasets/learning-loop/README.md](../datasets/learning-loop/README.md), [question-design experiment](../datasets/learning-loop/experiments/2026-10-02-question-design/README.md), [filing-gate experiment](../datasets/learning-loop/experiments/2026-10-07-filing-gate/README.md), [family-Z experiment](../datasets/learning-loop/experiments/2026-11-05-family-z/README.md), [deployment/README.md](../deployment/README.md), [evals/README.md](../evals/README.md), [evals/plan-002/README.md](../evals/plan-002/README.md), [experiments/README.md](../experiments/README.md), [human-facing/README.md](../human-facing/README.md), [operations/README.md](../operations/README.md), [proposals/README.md](../proposals/README.md), [research/README.md](../research/README.md), [research/sources/README.md](../research/sources/README.md), [legacy idea harvest README](../research/synthesis/2026-09-28-legacy-idea-harvest/README.md), [scripts/README.md](../scripts/README.md), [scripts/hive/README.md](../scripts/hive/README.md), [tests/README.md](../tests/README.md).

## Not read in this consolidation

- [.claude/](../.claude/): Claude Code OpenSpec commands and skills.
- [.agents/](../.agents/): Codex OpenSpec skills.
- [generated/](../generated/README.md): generated pages; [docstring wiki](../generated/docstring_wiki.md), [bootstrap view bundle](../generated/bootstrap-normative/view-bundle.md).
- [openspec/changes/archive/](../openspec/changes/archive/): archived OpenSpec changes, also linked from [Requirements](requirements.md).
- [docs/plans/](../docs/plans/README.md): plan files, each linked from [Proposals and plans](proposals.md).
- [proposals/harness-context/native-parity/input/](../proposals/harness-context/native-parity/input/task.json): frozen fixture inputs, linked from [Proposals and plans](proposals.md).
