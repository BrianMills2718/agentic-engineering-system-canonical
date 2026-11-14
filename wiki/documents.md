---
description: Every tracked AES file with a source-grounded purpose, role and review disposition, grouped for navigation
status: current
---

# Every file: purpose and review disposition

This catalog lists the reviewed inventory and subsequent records, including code,
tests, instructions, fixtures, archived changes, configuration and evidence. It
replaces the earlier reader-Markdown subset. Start with the [question-based wiki](index.md)
for the short reading path, then use this catalog for full coverage.

The [review inventory](../docs/planning/file-inventory.json) contains source
identities, content locators, assessment reasons, findings and consolidation
candidates. This is a dated content review, not proof of runtime behavior or an
installed universal automatic summarizer. Changed sources require re-review.
The [assessment](../docs/architecture/DOCUMENTATION.md#coverage-and-consolidation-assessment)
explains what can be consolidated and which unique information must survive.

**Coverage:** The dated inventory has 419 file entries. The merged tracked
trees contain 424 files; the five additional files are listed below. Changed
inventory entries require re-review; the count does not certify their current
descriptions.
Dispositions are assessment results: `keep` preserves a distinct role, `update`
flags a remaining correction, `consolidate` proposes a content-preserving merge,
and `generated` identifies derived/tool-owned material.
They do not authorize policy retirement, code removal or deletion of history.

## Subsequent archived change (2026-11-14)

These records were added after the 419-file inventory above. They record
the array projection change; the merged specification remains authoritative.

- [Array projection metadata](../openspec/changes/archive/2026-11-13-lockstep-array-fact-projection/.openspec.yaml) — archived change schema metadata.
- [Array projection proposal](../openspec/changes/archive/2026-11-13-lockstep-array-fact-projection/proposal.md) — motivation, scope and impact.
- [Array projection requirement delta](../openspec/changes/archive/2026-11-13-lockstep-array-fact-projection/specs/lockstep-doc-facts/spec.md) — retained change to the fact projection contract.
- [Array projection tasks](../openspec/changes/archive/2026-11-13-lockstep-array-fact-projection/tasks.md) — historical implementation checklist.

## Generated requirement coverage (2026-11-14)

- [Requirement status](../docs/status.md) — generated requirement-to-code and
  scenario-to-test coverage; it states when test results have not been recorded
  for the revision. It is a derived view, not evidence that tests passed.

## Owning external sources

- [BrianMills2718/project-meta/policy/registry.yaml](https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/policy/registry.yaml) — Original policy source with 263 entries; not replaced by the small AES register. Current disposition and live enforcement require per-policy reconciliation.

- [BrianMills2718/project-meta/docs/ops/POLICY_SYSTEM.md](https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/docs/ops/POLICY_SYSTEM.md) — Policy-system information map covering authority, context delivery, hooks, observation, feedback and lifecycle; dated runtime mechanisms need fresh verification.

- [BrianMills2718/code2-workspace/agents/core.md](https://github.com/BrianMills2718/code2-workspace/blob/e430021149b5f24dac1fd082f48dd93071899f8a/agents/core.md) — Shared agent rules covering authority, workflow, evidence, safety, documentation and session reporting; topic files provide detail.

- [BrianMills2718/code2-workspace/agents/rule-sources.md](https://github.com/BrianMills2718/code2-workspace/blob/e430021149b5f24dac1fd082f48dd93071899f8a/agents/rule-sources.md) — Dated stakeholder statements and incidents supporting shared rules, keyed by policy identifier.

- [BrianMills2718/code2-workspace/docs/architecture/model.c4](https://github.com/BrianMills2718/code2-workspace/blob/e430021149b5f24dac1fd082f48dd93071899f8a/docs/architecture/model.c4) — Harness implementation map connecting session startup, planning/checks, timers, services and owning repositories.

- [BrianMills2718/code2-workspace/docs/decisions/0006-planning-and-linkage.md](https://github.com/BrianMills2718/code2-workspace/blob/e430021149b5f24dac1fd082f48dd93071899f8a/docs/decisions/0006-planning-and-linkage.md) — Accepted planning/linkage decision and dated amendments describing Company Planning, repository checks and normative/docstring alignment.

- [BrianMills2718/company-planning/plugins/company-planning/skills/bounded-design/SKILL.md](https://github.com/BrianMills2718/company-planning/blob/497405299c68de0da8c3ac92e4c265d4d6c3403e/plugins/company-planning/skills/bounded-design/SKILL.md) — Planning method for deriving a bounded outcome through requirements, failure modes, capabilities, contracts, fixtures and thin implementation slices.

## Browse by folder

- [Repository root](#repository-root) (13 files)
- [.agentic](#agentic) (2 files)
- [.agentic/events](#agenticevents) (1 files)
- [.agents/skills](#agentsskills) (1 files)
- [.agents/skills/openspec-apply-change](#agentsskillsopenspec-apply-change) (1 files)
- [.agents/skills/openspec-archive-change](#agentsskillsopenspec-archive-change) (1 files)
- [.agents/skills/openspec-explore](#agentsskillsopenspec-explore) (1 files)
- [.agents/skills/openspec-propose](#agentsskillsopenspec-propose) (1 files)
- [.agents/skills/openspec-sync-specs](#agentsskillsopenspec-sync-specs) (1 files)
- [.agents/skills/openspec-update-change](#agentsskillsopenspec-update-change) (1 files)
- [.claude](#claude) (1 files)
- [.claude/commands/opsx](#claudecommandsopsx) (6 files)
- [.claude/skills/openspec-apply-change](#claudeskillsopenspec-apply-change) (1 files)
- [.claude/skills/openspec-archive-change](#claudeskillsopenspec-archive-change) (1 files)
- [.claude/skills/openspec-explore](#claudeskillsopenspec-explore) (1 files)
- [.claude/skills/openspec-propose](#claudeskillsopenspec-propose) (1 files)
- [.claude/skills/openspec-sync-specs](#claudeskillsopenspec-sync-specs) (1 files)
- [.claude/skills/openspec-update-change](#claudeskillsopenspec-update-change) (1 files)
- [.codex](#codex) (1 files)
- [.project-brain](#project-brain) (4 files)
- [contracts/learning-loop](#contractslearning-loop) (1 files)
- [docs](#docs) (2 files)
- [docs/architecture](#docsarchitecture) (6 files)
- [docs/architecture/greenfield-v0.2](#docsarchitecturegreenfield-v02) (11 files)
- [docs/decisions](#docsdecisions) (13 files)
- [docs/greenfield](#docsgreenfield) (1 files)
- [docs/history/consolidation-2026-11-11](#docshistoryconsolidation-2026-11-11) (2 files)
- [docs/model](#docsmodel) (2 files)
- [docs/planning](#docsplanning) (23 files)
- [docs/planning/router](#docsplanningrouter) (1 files)
- [docs/planning/runs](#docsplanningruns) (1 files)
- [docs/planning/runs/lockstep-acceptance](#docsplanningrunslockstep-acceptance) (6 files)
- [docs/retired](#docsretired) (1 files)
- [docs/rules](#docsrules) (3 files)
- [enforced_planning](#enforced_planning) (2 files)
- [evidence/runs](#evidenceruns) (3 files)
- [meta-process/templates](#meta-processtemplates) (1 files)
- [openspec](#openspec) (1 files)
- [openspec/changes/archive](#openspecchangesarchive) (1 files)
- [openspec/changes/archive/2026-11-07-inert-characterization](#openspecchangesarchive2026-11-07-inert-characterization) (2 files)
- [openspec/changes/archive/2026-11-07-inert-characterization/specs/inert-characterization](#openspecchangesarchive2026-11-07-inert-characterizationspecsinert-characterization) (1 files)
- [openspec/changes/archive/2026-11-07-required-evidence-inputs](#openspecchangesarchive2026-11-07-required-evidence-inputs) (3 files)
- [openspec/changes/archive/2026-11-07-required-evidence-inputs/specs/required-evidence-inputs](#openspecchangesarchive2026-11-07-required-evidence-inputsspecsrequired-evidence-inputs) (1 files)
- [openspec/changes/archive/2026-11-11-add-lockstep-checks](#openspecchangesarchive2026-11-11-add-lockstep-checks) (2 files)
- [openspec/changes/archive/2026-11-11-add-lockstep-checks/specs/lockstep-checks](#openspecchangesarchive2026-11-11-add-lockstep-checksspecslockstep-checks) (1 files)
- [openspec/changes/archive/2026-11-11-add-lockstep-package](#openspecchangesarchive2026-11-11-add-lockstep-package) (2 files)
- [openspec/changes/archive/2026-11-11-add-lockstep-package/specs/lockstep-package](#openspecchangesarchive2026-11-11-add-lockstep-packagespecslockstep-package) (1 files)
- [openspec/changes/archive/2026-11-11-add-lockstep-plan-check](#openspecchangesarchive2026-11-11-add-lockstep-plan-check) (2 files)
- [openspec/changes/archive/2026-11-11-add-lockstep-plan-check/specs/lockstep-plan-check](#openspecchangesarchive2026-11-11-add-lockstep-plan-checkspecslockstep-plan-check) (1 files)
- [openspec/changes/archive/2026-11-11-lockstep-guard](#openspecchangesarchive2026-11-11-lockstep-guard) (2 files)
- [openspec/changes/archive/2026-11-11-lockstep-guard/specs/lockstep-guard](#openspecchangesarchive2026-11-11-lockstep-guardspecslockstep-guard) (1 files)
- [openspec/changes/archive/2026-11-11-lockstep-plan-format](#openspecchangesarchive2026-11-11-lockstep-plan-format) (2 files)
- [openspec/changes/archive/2026-11-11-lockstep-plan-format/specs/lockstep-plan-format](#openspecchangesarchive2026-11-11-lockstep-plan-formatspecslockstep-plan-format) (1 files)
- [openspec/changes/archive/2026-11-12-add-lockstep-init](#openspecchangesarchive2026-11-12-add-lockstep-init) (2 files)
- [openspec/changes/archive/2026-11-12-add-lockstep-init/specs/lockstep-init](#openspecchangesarchive2026-11-12-add-lockstep-initspecslockstep-init) (1 files)
- [openspec/changes/archive/2026-11-12-add-lockstep-project-status-show](#openspecchangesarchive2026-11-12-add-lockstep-project-status-show) (2 files)
- [openspec/changes/archive/2026-11-12-add-lockstep-project-status-show/specs/lockstep-projection](#openspecchangesarchive2026-11-12-add-lockstep-project-status-showspecslockstep-projection) (1 files)
- [openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes](#openspecchangesarchive2026-11-12-lockstep-acceptance-fixes) (2 files)
- [openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/specs/lockstep-checks](#openspecchangesarchive2026-11-12-lockstep-acceptance-fixesspecslockstep-checks) (1 files)
- [openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/specs/lockstep-guard](#openspecchangesarchive2026-11-12-lockstep-acceptance-fixesspecslockstep-guard) (1 files)
- [openspec/changes/archive/2026-11-12-source-local-doc-facts](#openspecchangesarchive2026-11-12-source-local-doc-facts) (2 files)
- [openspec/changes/archive/2026-11-12-source-local-doc-facts/specs/lockstep-doc-facts](#openspecchangesarchive2026-11-12-source-local-doc-factsspecslockstep-doc-facts) (1 files)
- [openspec/changes/archive/2026-11-12-source-local-doc-facts/specs/lockstep-projection](#openspecchangesarchive2026-11-12-source-local-doc-factsspecslockstep-projection) (1 files)
- [openspec/changes/archive/2026-11-13-self-adopt-projection](#openspecchangesarchive2026-11-13-self-adopt-projection) (2 files)
- [openspec/changes/archive/2026-11-13-self-adopt-projection/specs/aes-documentation-projection](#openspecchangesarchive2026-11-13-self-adopt-projectionspecsaes-documentation-projection) (1 files)
- [openspec/specs](#openspecspecs) (1 files)
- [openspec/specs/aes-documentation-projection](#openspecspecsaes-documentation-projection) (1 files)
- [openspec/specs/inert-characterization](#openspecspecsinert-characterization) (1 files)
- [openspec/specs/lockstep-checks](#openspecspecslockstep-checks) (1 files)
- [openspec/specs/lockstep-doc-facts](#openspecspecslockstep-doc-facts) (1 files)
- [openspec/specs/lockstep-guard](#openspecspecslockstep-guard) (1 files)
- [openspec/specs/lockstep-init](#openspecspecslockstep-init) (1 files)
- [openspec/specs/lockstep-package](#openspecspecslockstep-package) (1 files)
- [openspec/specs/lockstep-plan-check](#openspecspecslockstep-plan-check) (1 files)
- [openspec/specs/lockstep-plan-format](#openspecspecslockstep-plan-format) (1 files)
- [openspec/specs/lockstep-projection](#openspecspecslockstep-projection) (1 files)
- [openspec/specs/required-evidence-inputs](#openspecspecsrequired-evidence-inputs) (1 files)
- [proposals](#proposals) (1 files)
- [proposals/aes-learning-loop/review-page](#proposalsaes-learning-loopreview-page) (7 files)
- [proposals/one-planning-tool](#proposalsone-planning-tool) (1 files)
- [proposals/planning-package/review-page](#proposalsplanning-packagereview-page) (11 files)
- [scripts](#scripts) (1 files)
- [scripts/acceptance](#scriptsacceptance) (8 files)
- [scripts/hive](#scriptshive) (2 files)
- [scripts/learning_loop](#scriptslearning_loop) (14 files)
- [scripts/learning_loop/systemd](#scriptslearning_loopsystemd) (11 files)
- [scripts/meta](#scriptsmeta) (2 files)
- [scripts/rules](#scriptsrules) (2 files)
- [src/agentic_engineering_system](#srcagentic_engineering_system) (15 files)
- [src/lockstep](#srclockstep) (32 files)
- [src/lockstep/checks](#srclockstepchecks) (14 files)
- [src/pcw](#srcpcw) (1 files)
- [tests](#tests) (6 files)
- [tests/greenfield](#testsgreenfield) (13 files)
- [tests/greenfield/fixtures](#testsgreenfieldfixtures) (1 files)
- [tests/greenfield/fixtures/whygame5-54043e2](#testsgreenfieldfixtureswhygame5-54043e2) (1 files)
- [tests/greenfield/fixtures/whygame5-54043e2/.aes](#testsgreenfieldfixtureswhygame5-54043e2aes) (2 files)
- [tests/learning](#testslearning) (13 files)
- [tests/lockstep](#testslockstep) (34 files)
- [tests/lockstep/checks](#testslockstepchecks) (13 files)
- [tests/lockstep/e2e](#testslockstepe2e) (2 files)
- [tests/lockstep/example](#testslockstepexample) (2 files)
- [tests/lockstep/example-layout](#testslockstepexample-layout) (1 files)
- [tests/lockstep/example-layout/openspec/specs/greeting](#testslockstepexample-layoutopenspecspecsgreeting) (1 files)
- [tests/lockstep/example-simple](#testslockstepexample-simple) (2 files)
- [tests/lockstep/example-simple/docs](#testslockstepexample-simpledocs) (1 files)
- [tests/lockstep/example-simple/plans](#testslockstepexample-simpleplans) (2 files)
- [tests/lockstep/example-simple/src/greeter](#testslockstepexample-simplesrcgreeter) (1 files)
- [tests/lockstep/example-simple/tests](#testslockstepexample-simpletests) (1 files)
- [tests/lockstep/example/.claude](#testslockstepexampleclaude) (1 files)
- [tests/lockstep/example/.codex](#testslockstepexamplecodex) (1 files)
- [tests/lockstep/example/docs](#testslockstepexampledocs) (1 files)
- [tests/lockstep/example/plans](#testslockstepexampleplans) (2 files)
- [tests/lockstep/example/src/people_finder](#testslockstepexamplesrcpeople_finder) (2 files)
- [tests/lockstep/example/tests](#testslockstepexampletests) (1 files)
- [tests/lockstep/lockstep-plan-sample](#testslocksteplockstep-plan-sample) (1 files)
- [tests/lockstep/lockstep-plan-sample/.aes](#testslocksteplockstep-plan-sampleaes) (2 files)
- [tests/lockstep/lockstep-plan-sample/.codex](#testslocksteplockstep-plan-samplecodex) (1 files)
- [tests/lockstep/lockstep-plan-sample/src/pcw](#testslocksteplockstep-plan-samplesrcpcw) (1 files)
- [wiki](#wiki) (13 files)

## Repository root

- **[.doc-reachability-ignore](../.doc-reachability-ignore)** — Excludes generated client instructions, archived OpenSpec changes and synthetic consumer fixtures from reader-document reachability. **Role:** native configuration or contract. **Disposition:** keep.

- **[.gitignore](../.gitignore)** — Ignores virtual environments, pytest/Python caches, package metadata and build output. **Role:** native configuration or contract. **Disposition:** keep.

- **[.markdownlint-cli2.yaml](../.markdownlint-cli2.yaml)** — Excludes worktrees and generated AGENTS.md from Markdown linting. **Role:** native configuration or contract. **Disposition:** keep.

- **[.md-file-cap.yaml](../.md-file-cap.yaml)** — Records the measured 130 Markdown file exception, preserving current contracts and archived lineage with complete catalog coverage. **Role:** native configuration or contract. **Disposition:** keep.

- **[AGENTS.md](../AGENTS.md)** — Defines current AES agent governance and authority routes, including bounded documentation self-adoption and native-proof limitations; AGENTS is generated from CLAUDE and relationships. **Role:** source document. **Disposition:** generated.

- **[CLAUDE.md](../CLAUDE.md)** — Defines current AES agent governance and authority routes, including bounded documentation self-adoption and native-proof limitations; AGENTS is generated from CLAUDE and relationships. **Role:** source document. **Disposition:** keep.

- **[Makefile](../Makefile)** — Defines tests and generated-instruction checks plus facts-only freshness and explicit refresh; make check includes declared-fact refusal. **Role:** native configuration or contract. **Disposition:** keep.

- **[README.md](../README.md)** — Introduces current AES, installs Lockstep through uvx init and explains planned structure, checks and source-owned fact projection. **Role:** source document. **Disposition:** keep.

- **[lefthook.yml](../lefthook.yml)** — Preserves shared workspace commit checks and adds the facts-only AES freshness command. **Role:** native configuration or contract. **Disposition:** keep.

- **[lockstep.yaml](../lockstep.yaml)** — Declares the projection module as source for architecture and wiki full-docstring assessment copies, without edit guards or unrelated policies. **Role:** native configuration. **Disposition:** keep.

- **[lychee.toml](../lychee.toml)** — Excludes worktree paths and GitHub line anchors from link checking, assigning file-and-line validation to a separate citation checker. **Role:** native configuration or contract. **Disposition:** keep.

- **[pyproject.toml](../pyproject.toml)** — Declares Python packaging, runtime/dev/wiki dependencies, AES/Lockstep commands, pytest plugin and Git-derived versions. **Role:** native configuration or contract. **Disposition:** keep.

- **[uv.lock](../uv.lock)** — Pins the editable AES dependency graph, including checks, tests, typing and wiki dependencies, with resolution markers and artifact hashes. **Role:** native configuration or contract. **Disposition:** generated.

## .agentic

- **[relationships.yaml](../.agentic/relationships.yaml)** — Records pilot clause, plan, implementation and evidence relationships for the retained history of repository-context resolution. **Role:** native configuration or contract. **Disposition:** update.

- **[repo.yaml](../.agentic/repo.yaml)** — Declares identity, adopted methodology and concern routing alongside older planning providers, repository-context implementation paths and acceptance state. **Role:** native configuration or contract. **Disposition:** update.

## .agentic/events

- **[README.md](../.agentic/events/README.md)** — Reserves append-only lifecycle events pending an accepted event contract and prohibits ad hoc bootstrap schemas. **Role:** source document. **Disposition:** keep.

## .agents/skills

- **[.openspec-target](../.agents/skills/.openspec-target)** — Selects Codex as the generated OpenSpec instruction target. **Role:** native configuration or contract. **Disposition:** keep.

## .agents/skills/openspec-apply-change

- **[SKILL.md](../.agents/skills/openspec-apply-change/SKILL.md)** — Implements tasks from a selected OpenSpec change and records completed or paused task state. **Role:** generated client instructions. **Disposition:** generated.

## .agents/skills/openspec-archive-change

- **[SKILL.md](../.agents/skills/openspec-archive-change/SKILL.md)** — Archives a completed change after checking artifacts, tasks and delta-spec synchronization. **Role:** generated client instructions. **Disposition:** generated.

## .agents/skills/openspec-explore

- **[SKILL.md](../.agents/skills/openspec-explore/SKILL.md)** — Provides investigation and design discussion while prohibiting implementation and allowing bounded planning artifacts. **Role:** generated client instructions. **Disposition:** generated.

## .agents/skills/openspec-propose

- **[SKILL.md](../.agents/skills/openspec-propose/SKILL.md)** — Creates proposal, delta specs, design and tasks for a change and stops at the explicit planning boundary. **Role:** generated client instructions. **Disposition:** generated.

## .agents/skills/openspec-sync-specs

- **[SKILL.md](../.agents/skills/openspec-sync-specs/SKILL.md)** — Merges added, modified, removed and renamed delta requirements into main specs without archiving. **Role:** generated client instructions. **Disposition:** generated.

## .agents/skills/openspec-update-change

- **[SKILL.md](../.agents/skills/openspec-update-change/SKILL.md)** — Revises existing planning artifacts coherently while prohibiting project-code edits. **Role:** generated client instructions. **Disposition:** generated.

## .claude

- **[settings.json](../.claude/settings.json)** — Registers pinned Claude post-edit fact refresh while preserving existing settings; the bounded native observation explicitly loads this configuration. **Role:** native configuration or contract. **Disposition:** keep.

## .claude/commands/opsx

- **[apply.md](../.claude/commands/opsx/apply.md)** — Implements tasks from a selected OpenSpec change and records completed or paused task state. **Role:** generated client instructions. **Disposition:** generated.

- **[archive.md](../.claude/commands/opsx/archive.md)** — Archives a completed change after checking artifacts, tasks and delta-spec synchronization. **Role:** generated client instructions. **Disposition:** generated.

- **[explore.md](../.claude/commands/opsx/explore.md)** — Provides investigation and design discussion while prohibiting implementation and allowing bounded planning artifacts. **Role:** generated client instructions. **Disposition:** generated.

- **[propose.md](../.claude/commands/opsx/propose.md)** — Creates proposal, delta specs, design and tasks for a change and stops at the explicit planning boundary. **Role:** generated client instructions. **Disposition:** generated.

- **[sync.md](../.claude/commands/opsx/sync.md)** — Merges added, modified, removed and renamed delta requirements into main specs without archiving. **Role:** generated client instructions. **Disposition:** generated.

- **[update.md](../.claude/commands/opsx/update.md)** — Revises existing planning artifacts coherently while prohibiting project-code edits. **Role:** generated client instructions. **Disposition:** generated.

## .claude/skills/openspec-apply-change

- **[SKILL.md](../.claude/skills/openspec-apply-change/SKILL.md)** — Implements tasks from a selected OpenSpec change and records completed or paused task state. **Role:** generated client instructions. **Disposition:** generated.

## .claude/skills/openspec-archive-change

- **[SKILL.md](../.claude/skills/openspec-archive-change/SKILL.md)** — Archives a completed change after checking artifacts, tasks and delta-spec synchronization. **Role:** generated client instructions. **Disposition:** generated.

## .claude/skills/openspec-explore

- **[SKILL.md](../.claude/skills/openspec-explore/SKILL.md)** — Provides investigation and design discussion while prohibiting implementation and allowing bounded planning artifacts. **Role:** generated client instructions. **Disposition:** generated.

## .claude/skills/openspec-propose

- **[SKILL.md](../.claude/skills/openspec-propose/SKILL.md)** — Creates proposal, delta specs, design and tasks for a change and stops at the explicit planning boundary. **Role:** generated client instructions. **Disposition:** generated.

## .claude/skills/openspec-sync-specs

- **[SKILL.md](../.claude/skills/openspec-sync-specs/SKILL.md)** — Merges added, modified, removed and renamed delta requirements into main specs without archiving. **Role:** generated client instructions. **Disposition:** generated.

## .claude/skills/openspec-update-change

- **[SKILL.md](../.claude/skills/openspec-update-change/SKILL.md)** — Revises existing planning artifacts coherently while prohibiting project-code edits. **Role:** generated client instructions. **Disposition:** generated.

## .codex

- **[hooks.json](../.codex/hooks.json)** — Registers pinned post-edit declared-fact refresh for Codex tool names; live Codex host execution remains unobserved. **Role:** native configuration. **Disposition:** keep.

## .project-brain

- **[now.md](../.project-brain/now.md)** — Routes the approved ecosystem consolidation and first donor review, then preserves independent projection, feedback and earlier dated records. **Role:** source document. **Disposition:** keep.

- **[project.md](../.project-brain/project.md)** — States the AES purpose and functions, including Company Planning, and links the owning intent, Lockstep contract, current work and retirement record. **Role:** source document. **Disposition:** keep.

- **[state.md](../.project-brain/state.md)** — Records November 13 scope and evidence limits, including incomplete synchronization proof and collector timeout observations. **Role:** source document. **Disposition:** keep.

- **[truth.md](../.project-brain/truth.md)** — Preserves dated choices and rejected alternatives for repository-local brains, Claude authentication, learning-loop scheduling and archived legacy learnings. **Role:** source document. **Disposition:** update.

## contracts/learning-loop

- **[feedback-report.v1.schema.json](../contracts/learning-loop/feedback-report.v1.schema.json)** — Defines observation, claim and action records with links, provenance, basis, confidence and action status, plus Link and Provenance definitions. **Role:** native configuration or contract. **Disposition:** keep.

## docs

- **[failure-modes.md](../docs/failure-modes.md)** — Defines AES feedback-label failure families and detecting questions, derivation and retraction limits, and the maintenance path through implemented labeling/analysis without claiming enabled or completed operation. **Role:** taxonomy. **Disposition:** keep.

- **[index.md](../docs/index.md)** — Lists the current source-linked reading order for purpose, components, documentation, feedback, state and questions, explicitly identifying itself as curated navigation. **Role:** navigation. **Disposition:** keep.

## docs/architecture

- **[ECOSYSTEM.md](../docs/architecture/ECOSYSTEM.md)** — Owns the adopted discovery direction, first bounded review of predecessor sources, proposed donor dispositions, concerns, source revisions and next reading sequence. **Role:** architecture review. **Disposition:** keep.

- **[DOCUMENTATION.md](../docs/architecture/DOCUMENTATION.md)** — Defines document authority and lifecycle, source-local summaries, generated and curated reading views, and the full-file coverage and consolidation assessment with preservation limits. **Role:** architecture. **Disposition:** keep.

- **[FEEDBACK\_AND\_POLICY.md](../docs/architecture/FEEDBACK_AND_POLICY.md)** — Explains correction-to-follow-up and policy ownership, distinguishes the original Project Meta inventory from the small AES register, and records dated runtime/evidence limitations. **Role:** architecture. **Disposition:** keep.

- **[GOAL.md](../docs/architecture/GOAL.md)** — Defines AES purpose and whole-system functions, including ecosystem integration alongside planning, Lockstep, feedback and policy. **Role:** normative. **Disposition:** keep.

- **[LOCKSTEP.md](../docs/architecture/LOCKSTEP.md)** — Explains planning and projection boundaries, retains the earlier worked assessment and records native AES self-adoption with a generated source-owned assessment. **Role:** architecture. **Disposition:** keep.

- **[README.md](../docs/architecture/README.md)** — Routes current architecture, ecosystem predecessor review and retained historical designs without transferring native ownership. **Role:** navigation. **Disposition:** keep.

- **[SYSTEM\_BOUNDARY.md](../docs/architecture/SYSTEM_BOUNDARY.md)** — Defines addressable clauses for AES scope, human-observable delivery, capability reuse, native boundaries, policy, context, documentation and learning; retains distinct historical first-vertical acceptance language. **Role:** normative. **Disposition:** keep.

## docs/architecture/greenfield-v0.2

- **[02-semantic-model.yaml](../docs/architecture/greenfield-v0.2/02-semantic-model.yaml)** — Defines v0.2 semantic families for targets, criteria, artifacts, plans, observations, assessments, current state and gaps; accepted amendments distinguish conceptual fields from realized MVP vocabulary. **Role:** historical contract. **Disposition:** update.

- **[03-lifecycle.yaml](../docs/architecture/greenfield-v0.2/03-lifecycle.yaml)** — Defines greenfield lifecycle states and transitions from intent through planning and evidence to reconciliation; records realized freshness/standing and deferred provider, retrofit and working-context capabilities. **Role:** historical contract. **Disposition:** update.

- **[04-greenfield-mvp.yaml](../docs/architecture/greenfield-v0.2/04-greenfield-mvp.yaml)** — Defines the greenfield MVP outcome, supported lifecycle and nine minimum criteria; explicitly excludes universal retrofit/languages and automatic gap closure from completed plans. **Role:** historical contract. **Disposition:** update.

- **[12-greenfield-mvp-semantic-instance.yaml](../docs/architecture/greenfield-v0.2/12-greenfield-mvp-semantic-instance.yaml)** — Instantiates nine greenfield requirements and criteria with evidence routes, failure analysis and capabilities; distinguishes analysis-only families from selected realization topology. **Role:** historical contract. **Disposition:** update.

- **[13-greenfield-materialization.md](../docs/architecture/greenfield-v0.2/13-greenfield-materialization.md)** — Explains .aes project/target/plan/observation storage, candidate analysis/generated records and source-local context; accepted amendments identify actually realized files and transaction behavior. **Role:** historical contract. **Disposition:** update.

- **[14-initialization-contract.yaml](../docs/architecture/greenfield-v0.2/14-initialization-contract.yaml)** — Specifies initialization phases, seed artifacts, minimum target, success and disproof; explains the realized two-file initialization boundary and separately installed hooks. **Role:** historical contract. **Disposition:** update.

- **[15-planning-contract.yaml](../docs/architecture/greenfield-v0.2/15-planning-contract.yaml)** — Defines design, target acceptance, execution planning, topology and verification contracts; amendments qualify actual prepare/validate/accept behavior and deferred provider machinery. **Role:** historical contract. **Disposition:** update.

- **[16-record-shapes.yaml](../docs/architecture/greenfield-v0.2/16-record-shapes.yaml)** — Defines strict project, target, accepted-plan and observation shapes, identities, dependencies and controls; separates realized Pydantic records from unrealized analysis/generated-state files. **Role:** historical contract. **Disposition:** update.

- **[20-realization-topology.yaml](../docs/architecture/greenfield-v0.2/20-realization-topology.yaml)** — Records ten historical implementation units, artifacts, fixtures, retained v0.1 files, selected exports and verification routes; accepted amendments reconcile candidates with the accepted target/code. **Role:** historical contract. **Disposition:** update.

- **[23-greenfield-cli-product-contract.md](../docs/architecture/greenfield-v0.2/23-greenfield-cli-product-contract.md)** — Documents aes commands, root discovery, exit codes and greenfield workflow; per-section realization notes distinguish implemented behavior from candidate commands and generated files never built. **Role:** historical contract. **Disposition:** update.

- **[README.md](../docs/architecture/greenfield-v0.2/README.md)** — Indexes accepted engine documents and copy/amendment lineage; adds narrow required-input and inert-Git policies while explaining that historical self-governance is not current AES workflow. **Role:** navigation. **Disposition:** update.

## docs/decisions

- **[0014-ecosystem-consolidation-and-legacy-review.md](../docs/decisions/0014-ecosystem-consolidation-and-legacy-review.md)** — Records Brian-approved AES consolidation and legacy review, one discovery route with native owners, historical decision reconciliation and success/disproof boundaries. **Role:** decision. **Disposition:** keep.

- **[0001-canonical-convergence-boundary.md](../docs/decisions/0001-canonical-convergence-boundary.md)** — Records clean canonical convergence, exact upstream methodology adoption and capability-by-capability dispositions; preserves bootstrap restrictions and the original first-vertical proof boundary. **Role:** decision. **Disposition:** keep.

- **[0002-company-planning-aes-profile-before-fork.md](../docs/decisions/0002-company-planning-aes-profile-before-fork.md)** — Chooses a local Company Planning profile before upstream change or fork; preserves provider scope and the distinction between structural conformance and executed planning evidence. **Role:** decision. **Disposition:** keep.

- **[0003-component-local-normative-context-and-symbol-inheritance.md](../docs/decisions/0003-component-local-normative-context-and-symbol-inheritance.md)** — Defines component-local verbatim normative projection, explicit applicability and symbol inheritance of context rather than conformance; gives criteria for component decomposition and narrower symbol links. **Role:** decision. **Disposition:** keep.

- **[0004-compact-structured-normative-records-and-generated-views.md](../docs/decisions/0004-compact-structured-normative-records-and-generated-views.md)** — Chooses compact system/component records and generated conventional views such as PRDs; preserves separate research/decision/plan/evidence lifecycles and explicit single-authority migration. **Role:** decision. **Disposition:** keep.

- **[0005-aes-component-scope-and-consequential-seam-typing.md](../docs/decisions/0005-aes-component-scope-and-consequential-seam-typing.md)** — Defines components as governance scopes rather than a universal runtime ontology; freezes only consequential seams and preserves unknown boundaries without speculative typing. **Role:** decision. **Disposition:** keep.

- **[0006-minimal-architecture-realization-json-schema.md](../docs/decisions/0006-minimal-architecture-realization-json-schema.md)** — Selects JSON Schema 2020-12 for the minimal bootstrap realization contract with extra semantic checks; identifies component/seam fields while excluding native product contract ownership. **Role:** decision. **Disposition:** keep.

- **[0007-provider-independent-verification-and-blob-evidence-carry-forward.md](../docs/decisions/0007-provider-independent-verification-and-blob-evidence-carry-forward.md)** — Preserves the superseded blob-level evidence carry-forward decision and the correction that individual unchanged files can omit dependencies of the executed subject. **Role:** decision. **Disposition:** keep.

- **[0008-provider-independent-verification-with-transitive-subjects.md](../docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md)** — Requires provider-independent verification bound to the transitive executed subject and environment; supersedes blob-only reuse and qualifies prior Plan 001 evidence. **Role:** decision. **Disposition:** keep.

- **[0009-modular-product-design-without-parallel-aca-platform.md](../docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md)** — Applies modular product design and external-first sourcing through AES rather than a parallel ACA platform; separates cohesive reusable behavior, product policy and adapters. **Role:** decision. **Disposition:** keep.

- **[0010-greenfield-v0.2-accepted.md](../docs/decisions/0010-greenfield-v0.2-accepted.md)** — Accepts the realized greenfield MVP with criterion evidence, standing design decisions and supersession of earlier choices; live-target/self-governance statements retain historical acceptance scope. **Role:** decision. **Disposition:** keep.

- **[0011-inside-success-aes-archived-canonical-is-aes.md](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md)** — Names this repository as AES and records archival/harvest of the earlier implementation, rollout conditions and whygame5 value tally with its later stale-evidence catch. **Role:** decision. **Disposition:** keep.

- **[0012-capability-reuse-enforced-at-plan-adoption.md](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md)** — Records the original ACA catalogue and planning reuse decision, qualified by Decision 0014 and unresolved publication/provider reconciliation. **Role:** decision. **Disposition:** update.

- **[0013-truth-lives-where-it-is-edited.md](../docs/decisions/0013-truth-lives-where-it-is-edited.md)** — Records Brian’s source-local description rule and generated wiki copies, with explicit wrong-when examples for inaccurate descriptions and failed reader routing. **Role:** decision. **Disposition:** keep.

## docs/greenfield

- **[GETTING\_STARTED.md](../docs/greenfield/GETTING_STARTED.md)** — Walks a Python/Git project through legacy aes setup, accepted plans, implementation and evidence standing, including existing-codebase adoption and a command reference. **Role:** instruction. **Disposition:** update.

## docs/history/consolidation-2026-11-11

- **[fold-report.json](../docs/history/consolidation-2026-11-11/fold-report.json)** — Records facts folded from each November 11 source into wiki pages and reasons for deliberate omissions; this historical accounting does not prove current complete navigation. **Role:** evidence. **Disposition:** keep.

- **[ledger.jsonl](../docs/history/consolidation-2026-11-11/ledger.jsonl)** — Records 241 files considered in the November 11 consolidation, kept/retired outcomes and totals; preserves old disposition reasons rather than authorizing new deletions. **Role:** evidence. **Disposition:** keep.

## docs/model

- **[ODD.md](../docs/model/ODD.md)** — Explains the narrow retained-engine target/evidence/reconciliation loop with a stale-evidence example, entities, processes and explicit model gaps; this is not the whole current AES model. **Role:** model. **Disposition:** update.

- **[trace.yaml](../docs/model/trace.yaml)** — Links v0.2 entities, processes and three rules to owner code, tests and decisions; records a November 12 review and excluded provider/profile scope. **Role:** model. **Disposition:** keep.

## docs/planning

- **[DOMAIN.md](../docs/planning/DOMAIN.md)** — Provides the generated project-local glossary with definitions, document/code locators and implemented, document-only or retired classifications. **Role:** generated. **Disposition:** generated.

- **[SYSTEM\_MODEL.md](../docs/planning/SYSTEM_MODEL.md)** — Models whole AES across repositories and this repository’s containers, record types, writers and external boundaries, extending the narrower checked engine model. **Role:** model. **Disposition:** consolidate.

- **[acceptance-criteria.json](../docs/planning/acceptance-criteria.json)** — Stores A1–A9 criteria, demonstrations, expected outcomes, failure examples, reader representations and goal coverage, with statuses/evidence distinct from fresh runtime proof. **Role:** acceptance contract. **Disposition:** keep.

- **[build\_domain\_model.py](../docs/planning/build_domain_model.py)** — Owns domain concept records and writes both glossary and typed graph with definitions, source/code locations and document-only classifications. **Role:** generator. **Disposition:** keep.

- **[build\_open\_questions\_graph.py](../docs/planning/build_open_questions_graph.py)** — Generates open-question, blocked-decision and affected-concept graph nodes from ledger/domain data; omits resolved questions and fails unknown concept references. **Role:** generator. **Disposition:** keep.

- **[capabilities.json](../docs/planning/capabilities.json)** — Maps one-tool capabilities to expected user outcomes, owning work and acceptance IDs, identifying the decomposition as agent-inferred from the adopted design. **Role:** planning record. **Disposition:** keep.

- **[checks.txt](../docs/planning/checks.txt)** — Retains five fresh planning checks: durable fields and wiki reachability pass; repository format remains tracked by Q17; navigation warnings and graph-schema results stay explicit. **Role:** evidence. **Disposition:** keep.

- **[cold-review.md](../docs/planning/cold-review.md)** — Records independent bounded self-adoption review with native trace, catalog, goal-field and check-count verification; preserves the prior source-fact review and excludes A1–A8 recertification. **Role:** evidence. **Disposition:** keep.

- **[coverage-trace.json](../docs/planning/coverage-trace.json)** — Retains model calls, messages, judgment and agreement/uncertainty for goal coverage, with trace identity and observability rather than product runtime certification. **Role:** evidence. **Disposition:** keep.

- **[decisions.json](../docs/planning/decisions.json)** — Records D1–D7 on whole-AES scope, retirement, Lockstep and the single-tool plan, distinguishing accepted decisions from the package’s working default. **Role:** planning record. **Disposition:** consolidate.

- **[domain.graph.json](../docs/planning/domain.graph.json)** — Materializes domain concepts and relations as typed graph nodes/edges with implementation and document-only distinctions from the domain generator. **Role:** generated. **Disposition:** generated.

- **[domain.implemented.json](../docs/planning/domain.implemented.json)** — Maps implemented domain IDs to concrete engine, feedback and Lockstep source locations; the package declares it a generated implementation locator map. **Role:** generated. **Disposition:** generated.

- **[domain.spectrum.json](../docs/planning/domain.spectrum.json)** — Defines domain-spectrum classes, vocabulary/thesaurus terms and ambiguous concepts, retaining semantic classifications beyond the rendered glossary and graph. **Role:** model. **Disposition:** keep.

- **[file-inventory.json](../docs/planning/file-inventory.json)** — Derived full-file review inventory: per-file purpose, source locator, role, disposition, input hashes, findings, consolidation candidates, external ownership routes and verification scope. **Role:** generated review inventory. **Disposition:** generated.

- **[investigation.json](../docs/planning/investigation.json)** — Retains a revision-bound investigation of whole-AES scope, one-tool design, corrections filing, policy coverage and engine dependencies, including then-failed findings later resolved. **Role:** evidence. **Disposition:** keep.

- **[next.goal.md](../docs/planning/next.goal.md)** — Records the adopted six-slice one-tool build and remaining review/follow-up work; identifies the design as authority and this document as its planning-package view. **Role:** plan. **Disposition:** update.

- **[open-questions.graph.json](../docs/planning/open-questions.graph.json)** — Generated graph of open ledger questions, responsible actors and domain relationships; it is a derived reading view rather than another question authority. **Role:** generated. **Disposition:** generated.

- **[open-questions.json](../docs/planning/open-questions.json)** — Owns AES unresolved questions and dispositions, including Q36–Q42 for ecosystem catalogue authority, identities, evidence, donor review and concern closure. **Role:** planning record. **Disposition:** keep.

- **[planning-package.json](../docs/planning/planning-package.json)** — Indexes package parts, recorded checks, system scope, spectrum sources and generated artifacts at a named revision; it is not a fresh operational certification. **Role:** planning record. **Disposition:** update.

- **[review-page.json](../docs/planning/review-page.json)** — Supplies review title/lead, reader actions, north star, thesis, disproof and architecture/domain/question links, repeating plan narrative alongside view configuration. **Role:** view configuration. **Disposition:** consolidate.

- **[run\_checks.sh](../docs/planning/run_checks.sh)** — Runs package validations and records individual exits/full outputs into checks.txt, explicitly excluding retired replay, self-governance and plan-adoption checks. **Role:** verification runner. **Disposition:** keep.

- **[source-facts-acceptance.md](../docs/planning/source-facts-acceptance.md)** — Lists A9 source-fact expected/observed cases with command, native-dispatch and stale-check evidence, excluding arbitrary narrative correctness and universal documentation organization. **Role:** acceptance evidence. **Disposition:** keep.

- **[system-map.md](../docs/planning/system-map.md)** — Maps listed code units into AES subsystems and calling/data relationships, including disabled analysis/effects stages, complementing the higher-level system model. **Role:** model. **Disposition:** keep.

## docs/planning/router

- **[acceptance-views.json](../docs/planning/router/acceptance-views.json)** — Records table/text representation choices for acceptance criteria and their router sources, distinguishing agent presentation decisions from choices left to Brian. **Role:** design. **Disposition:** keep.

## docs/planning/runs

- **[orientation-reader-20261113.json](../docs/planning/runs/orientation-reader-20261113.json)** — Records independent orientation findings, repairs, eight answered questions and source hashes; limits its conclusion to the inspected reading path, not every file/runtime transition. **Role:** evidence. **Disposition:** keep.

## docs/planning/runs/lockstep-acceptance

- **[a1.json](../docs/planning/runs/lockstep-acceptance/a1.json)** — Retains A1 fresh-install command, generated files and seven compared setup outcomes; written artifacts are narrower evidence than active hook enforcement. **Role:** evidence. **Disposition:** keep.

- **[a2.json](../docs/planning/runs/lockstep-acceptance/a2.json)** — Retains A2 heredoc/echo/Python writes, read-only copying and allowed-file refusal text; bounded replay cases do not establish all-patch-path guard coverage. **Role:** evidence. **Disposition:** keep.

- **[a3.json](../docs/planning/runs/lockstep-acceptance/a3.json)** — Retains A3 test-first, forbidden-import and source-attribution negative cases plus a clean case, with diagnostic import-linter and environment outputs. **Role:** evidence. **Disposition:** keep.

- **[a4.json](../docs/planning/runs/lockstep-acceptance/a4.json)** — Retains A4 approved requirement text, pre-layout file state and word-for-word docstring comparisons for requirement/scenario/test projection fixtures. **Role:** evidence. **Disposition:** keep.

- **[a5-readme-agent.jsonl](../docs/planning/runs/lockstep-acceptance/a5-readme-agent.jsonl)** — Retains the native README-following agent trace used by A5, including tool events and the global hooksPath installation boundary encountered by that agent. **Role:** evidence. **Disposition:** keep.

- **[a5.json](../docs/planning/runs/lockstep-acceptance/a5.json)** — Retains A5 fresh-install portability/configuration checks and README-agent report, separating path/configuration checks from the active-hook boundary. **Role:** evidence. **Disposition:** keep.

## docs/retired

- **[2026-11-12.md](../docs/retired/2026-11-12.md)** — Lists November 12 retired roots with counts, reasons, successors and pinned restoration command; records what stayed and related informational changes. **Role:** retirement record. **Disposition:** keep.

## docs/rules

- **[RULES.md](../docs/rules/RULES.md)** — Displays the one-rule register, enforcement statuses and 263-policy legacy proposal totals; old workspace routing text and totals do not establish current coverage. **Role:** generated. **Disposition:** generated.

- **[legacy-dispositions.yaml](../docs/rules/legacy-dispositions.yaml)** — Publishes identifiers, proposed dispositions and hashes for 263 legacy policy rows with no activation, separating private-text custody from adoption/removal. **Role:** historical inventory. **Disposition:** keep.

- **[register.yaml](../docs/rules/register.yaml)** — Owns enforcement-status definitions and the remaining advisory recommendations rule, but retains obsolete workspace source/coverage wording. **Role:** policy register. **Disposition:** update.

## enforced_planning

- **[\_\_init\_\_.py](../enforced_planning/__init__.py)** — Importable package surfaces for enforced-planning. Contains no executable definitions. **Role:** code. **Disposition:** keep.

- **[agents\_rendering.py](../enforced_planning/agents_rendering.py)** — Importable AGENTS.md rendering helpers for governed repos. **Role:** code. **Disposition:** keep.

## evidence/runs

- **[projection-native-20261113.jsonl](../evidence/runs/projection-native-20261113.jsonl)** — Retains all 17 successful Claude Read/Read/Edit events; an explicit redaction replaces private metadata from a prior unsuccessful invocation. **Role:** run evidence. **Disposition:** keep.

- **[projection-self-adoption-20261113.json](../evidence/runs/projection-self-adoption-20261113.json)** — Records Claude edit/hook attribution and hashes, read-only stale refusal, recovery and 27 focused test passes with explicit client-loading limits. **Role:** run evidence. **Disposition:** keep.

- **[projection-worked-20261113.json](../evidence/runs/projection-worked-20261113.json)** — Retained six-step CLI observation on a disposable copy of the real projector: normative-down and authored current/gap/plan fan-out, stale refusal, recovery, before/after hashes, two traces and focused pytest output. **Role:** retained run evidence. **Disposition:** keep.

## meta-process/templates

- **[agents.md.template](../meta-process/templates/agents.md.template)** — Defines generated AGENTS structure and provenance placeholders for canonical instructions, relationship digest, commands and workflow. **Role:** native configuration or contract. **Disposition:** keep.

## openspec

- **[config.yaml](../openspec/config.yaml)** — Selects OpenSpec’s spec-driven schema; optional context, artifact rules and operation guidance remain commented examples rather than active custom requirements. **Role:** configuration. **Disposition:** keep.

## openspec/changes/archive

- **[.gitkeep](../openspec/changes/archive/.gitkeep)** — Empty tracked placeholder retaining the directory in Git, with no substantive requirement or history. **Role:** placeholder. **Disposition:** keep.

## openspec/changes/archive/2026-11-07-inert-characterization

- **[proposal.md](../openspec/changes/archive/2026-11-07-inert-characterization/proposal.md)** — Archived proposal for the fsmonitor-execution counterexample during read-only inspection. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-07-inert-characterization/tasks.md)** — Completed archived task checklist for the fsmonitor-execution counterexample during read-only inspection. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-07-inert-characterization/specs/inert-characterization

- **[spec.md](../openspec/changes/archive/2026-11-07-inert-characterization/specs/inert-characterization/spec.md)** — Archived requirement delta: Requires inert Git characterization/producer identification preserving actual revision, dirty state and source facts. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-07-required-evidence-inputs

- **[.openspec.yaml](../openspec/changes/archive/2026-11-07-required-evidence-inputs/.openspec.yaml)** — Records the archived change’s spec-driven schema and November 7 creation date. **Role:** historical configuration. **Disposition:** keep.

- **[proposal.md](../openspec/changes/archive/2026-11-07-required-evidence-inputs/proposal.md)** — Archived proposal for weak historical subprocess observations masking later staleness. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-07-required-evidence-inputs/tasks.md)** — Completed archived task checklist for weak historical subprocess observations masking later staleness. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-07-required-evidence-inputs/specs/required-evidence-inputs

- **[spec.md](../openspec/changes/archive/2026-11-07-required-evidence-inputs/specs/required-evidence-inputs/spec.md)** — Archived requirement delta: Requires caller-declared dependency coverage, UNKNOWN for incomplete current observations and rejection of unsafe literal paths. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-add-lockstep-checks

- **[proposal.md](../openspec/changes/archive/2026-11-11-add-lockstep-checks/proposal.md)** — Archived proposal for porting code2check checks and configurable per-check modes. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-11-add-lockstep-checks/tasks.md)** — Completed archived task checklist for porting code2check checks and configurable per-check modes. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-add-lockstep-checks/specs/lockstep-checks

- **[spec.md](../openspec/changes/archive/2026-11-11-add-lockstep-checks/specs/lockstep-checks/spec.md)** — Archived requirement delta: Defines trace, architecture, test-first, attribution and docmeta checks with block/warn/off modes and honest unavailable-check failure. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-add-lockstep-package

- **[proposal.md](../openspec/changes/archive/2026-11-11-add-lockstep-package/proposal.md)** — Archived proposal for moving the package and compatibility entrypoints into AES canonical. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-11-add-lockstep-package/tasks.md)** — Completed archived task checklist for moving the package and compatibility entrypoints into AES canonical. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-add-lockstep-package/specs/lockstep-package

- **[spec.md](../openspec/changes/archive/2026-11-11-add-lockstep-package/specs/lockstep-package/spec.md)** — Archived requirement delta: Requires AES-canonical installation and compatibility for pcw commands, module paths and cog blocks. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-add-lockstep-plan-check

- **[proposal.md](../openspec/changes/archive/2026-11-11-add-lockstep-plan-check/proposal.md)** — Archived proposal for porting acceptance and stored-coverage checks from Company Planning. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-11-add-lockstep-plan-check/tasks.md)** — Completed archived task checklist for porting acceptance and stored-coverage checks from Company Planning. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-add-lockstep-plan-check/specs/lockstep-plan-check

- **[spec.md](../openspec/changes/archive/2026-11-11-add-lockstep-plan-check/specs/lockstep-plan-check/spec.md)** — Archived requirement delta: Defines acceptance-file validation and quoted-source/stored-coverage checks, including stale or absent judgment behavior. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-lockstep-guard

- **[proposal.md](../openspec/changes/archive/2026-11-11-lockstep-guard/proposal.md)** — Archived proposal for porting destination-aware shell-write detection. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-11-lockstep-guard/tasks.md)** — Completed archived task checklist for porting destination-aware shell-write detection. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-lockstep-guard/specs/lockstep-guard

- **[spec.md](../openspec/changes/archive/2026-11-11-lockstep-guard/specs/lockstep-guard/spec.md)** — Archived requirement delta: Requires destination-aware shell-write checks that allow reads and refusal messages listing permitted files. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-lockstep-plan-format

- **[proposal.md](../openspec/changes/archive/2026-11-11-lockstep-plan-format/proposal.md)** — Archived proposal for reading OpenSpec/layout without requiring the old AES target. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-11-lockstep-plan-format/tasks.md)** — Completed archived task checklist for reading OpenSpec/layout without requiring the old AES target. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-11-lockstep-plan-format/specs/lockstep-plan-format

- **[spec.md](../openspec/changes/archive/2026-11-11-lockstep-plan-format/specs/lockstep-plan-format/spec.md)** — Archived requirement delta: Defines OpenSpec plus governed/layout rows, requirement/test/export links and compatibility with legacy AES targets. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-add-lockstep-init

- **[proposal.md](../openspec/changes/archive/2026-11-12-add-lockstep-init/proposal.md)** — Archived proposal for providing portable additive one-command setup. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-12-add-lockstep-init/tasks.md)** — Completed archived task checklist for providing portable additive one-command setup. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-add-lockstep-init/specs/lockstep-init

- **[spec.md](../openspec/changes/archive/2026-11-12-add-lockstep-init/specs/lockstep-init/spec.md)** — Archived requirement delta: Defines additive idempotent native-hook/lefthook setup without machine paths, owner configuration and .lockstep decision logs. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-add-lockstep-project-status-show

- **[proposal.md](../openspec/changes/archive/2026-11-12-add-lockstep-project-status-show/proposal.md)** — Archived proposal for porting requirement projection, status/show and pytest integration. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-12-add-lockstep-project-status-show/tasks.md)** — Completed archived task checklist for porting requirement projection, status/show and pytest integration. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-add-lockstep-project-status-show/specs/lockstep-projection

- **[spec.md](../openspec/changes/archive/2026-11-12-add-lockstep-project-status-show/specs/lockstep-projection/spec.md)** — Archived requirement delta: Defines normative docstring projection, plan/status coverage, revision-qualified tests, show and pytest marker integration. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes

- **[proposal.md](../openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/proposal.md)** — Archived proposal for repairing acceptance-discovered refusal, import-check and pytest false-pass defects. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/tasks.md)** — Completed archived task checklist for repairing acceptance-discovered refusal, import-check and pytest false-pass defects. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/specs/lockstep-checks

- **[spec.md](../openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/specs/lockstep-checks/spec.md)** — Archived additions require actual import-linter execution and loud failure when pytest cannot produce a report, preserving acceptance-discovered false-pass counterexamples. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/specs/lockstep-guard

- **[spec.md](../openspec/changes/archive/2026-11-12-lockstep-acceptance-fixes/specs/lockstep-guard/spec.md)** — Archived addition requires refused writes to list allowed paths, same folder first with a 15-item cap and remainder count. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-source-local-doc-facts

- **[proposal.md](../openspec/changes/archive/2026-11-12-source-local-doc-facts/proposal.md)** — Archived proposal for extending the existing projector to source facts with native edit/merge upkeep. Preserves original rationale, approved scope and exclusions rather than current requirement authority. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-12-source-local-doc-facts/tasks.md)** — Completed archived task checklist for extending the existing projector to source facts with native edit/merge upkeep. Checked items record historical execution, not a fresh verification run. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-source-local-doc-facts/specs/lockstep-doc-facts

- **[spec.md](../openspec/changes/archive/2026-11-12-source-local-doc-facts/specs/lockstep-doc-facts/spec.md)** — Archived requirement delta: Defines declared Markdown/Python/JSON/YAML fact projection, invalid-input refusal, post-edit refresh and stale checking. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-12-source-local-doc-facts/specs/lockstep-projection

- **[spec.md](../openspec/changes/archive/2026-11-12-source-local-doc-facts/specs/lockstep-projection/spec.md)** — Archived modified requirement restricts status-page generation to recognized OpenSpec consumers, leaving fact-only consumers without empty coverage or historical-plan rewrites. **Role:** historical requirement delta. **Disposition:** keep.

## openspec/changes/archive/2026-11-13-self-adopt-projection

- **[proposal.md](../openspec/changes/archive/2026-11-13-self-adopt-projection/proposal.md)** — Preserves narrow self-adoption rationale: reuse the existing projector and hooks without reinstating retired universal governance. **Role:** historical proposal. **Disposition:** keep.

- **[tasks.md](../openspec/changes/archive/2026-11-13-self-adopt-projection/tasks.md)** — Records completed self-adoption tasks for configuration, source narrative, native observation, bypass refusal and focused verification. **Role:** historical task record. **Disposition:** keep.

## openspec/changes/archive/2026-11-13-self-adopt-projection/specs/aes-documentation-projection

- **[spec.md](../openspec/changes/archive/2026-11-13-self-adopt-projection/specs/aes-documentation-projection/spec.md)** — Preserves the archived delta for source-owned component assessment projection and a facts-only freshness gate. **Role:** historical normative delta. **Disposition:** keep.

## openspec/specs

- **[.gitkeep](../openspec/specs/.gitkeep)** — Empty tracked placeholder retaining the directory in Git, with no substantive requirement or history. **Role:** placeholder. **Disposition:** keep.

## openspec/specs/aes-documentation-projection

- **[spec.md](../openspec/specs/aes-documentation-projection/spec.md)** — Requires AES source-owned assessment projection and a read-only facts gate, with native-edit, bypass-refusal and recovery scenarios. **Role:** normative specification. **Disposition:** keep.

## openspec/specs/inert-characterization

- **[spec.md](../openspec/specs/inert-characterization/spec.md)** — Requires inert Git characterization/producer identification preserving actual revision, dirty state and source facts. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-checks

- **[spec.md](../openspec/specs/lockstep-checks/spec.md)** — Defines trace, architecture, test-first, attribution and docmeta checks with block/warn/off modes and honest unavailable-check failure. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-doc-facts

- **[spec.md](../openspec/specs/lockstep-doc-facts/spec.md)** — Defines declared Markdown/Python/JSON/YAML fact projection, invalid-input refusal, post-edit refresh and stale checking. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-guard

- **[spec.md](../openspec/specs/lockstep-guard/spec.md)** — Requires destination-aware shell-write checks that allow reads and refusal messages listing permitted files. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-init

- **[spec.md](../openspec/specs/lockstep-init/spec.md)** — Defines additive idempotent native-hook/lefthook setup without machine paths, owner configuration and .lockstep decision logs. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-package

- **[spec.md](../openspec/specs/lockstep-package/spec.md)** — Requires AES-canonical installation and compatibility for pcw commands, module paths and cog blocks. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-plan-check

- **[spec.md](../openspec/specs/lockstep-plan-check/spec.md)** — Defines acceptance-file validation and quoted-source/stored-coverage checks, including stale or absent judgment behavior. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-plan-format

- **[spec.md](../openspec/specs/lockstep-plan-format/spec.md)** — Defines OpenSpec plus governed/layout rows, requirement/test/export links and compatibility with legacy AES targets. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/lockstep-projection

- **[spec.md](../openspec/specs/lockstep-projection/spec.md)** — Defines normative docstring projection, plan/status coverage, revision-qualified tests, show and pytest marker integration. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## openspec/specs/required-evidence-inputs

- **[spec.md](../openspec/specs/required-evidence-inputs/spec.md)** — Requires caller-declared dependency coverage, UNKNOWN for incomplete current observations and rejection of unsafe literal paths. This is the merged current capability specification. **Role:** normative. **Disposition:** keep.

## proposals

- **[README.md](../proposals/README.md)** — Routes to the adopted design, bounded acceptance review, retirement record and current feedback account, directing new behavior changes through OpenSpec. **Role:** navigation. **Disposition:** keep.

## proposals/aes-learning-loop/review-page

- **[build\_requirements.py](../proposals/aes-learning-loop/review-page/build_requirements.py)** — Builds feedback requirements HTML from 19 authored quoted requirements/statuses/evidence/fixes; embedded October limits need reconciliation with later HTML amendments before rebuilding. **Role:** generator. **Disposition:** update.

- **[feedback-coverage.html](../proposals/aes-learning-loop/review-page/feedback-coverage.html)** — Shows the October 11 matrix of agent setup components, recorded feedback routes and change owners, separating capture from application with then-current counts. **Role:** historical review. **Disposition:** update.

- **[feedback-models.html](../proposals/aes-learning-loop/review-page/feedback-models.html)** — Shows October 12 domain/data-flow models for reports, records, problems, licences, dispositions and receipts, with historical schedule and analysis/fix limits. **Role:** historical review. **Disposition:** update.

- **[guide.html](../proposals/aes-learning-loop/review-page/guide.html)** — Provides the October 12 feedback guide, job schedules, page routes and document roles; presents repair/effects as running and an old filing limit unlike current operation. **Role:** historical navigation. **Disposition:** update.

- **[index.html](../proposals/aes-learning-loop/review-page/index.html)** — Explains observations/claims/actions, licences, enforcement and recurrence through the slice design, mixing historical built/planned labels and older requirement totals. **Role:** historical review. **Disposition:** update.

- **[requirements.html](../proposals/aes-learning-loop/review-page/requirements.html)** — Compares 19 feedback requirements against October evidence and includes later corrections-first/filing-limit amendments absent from portions of its builder table. **Role:** historical review. **Disposition:** update.

- **[whole-picture.html](../proposals/aes-learning-loop/review-page/whole-picture.html)** — Presents the historical feedback flow, queue/backlog counts and stalled transitions, including the October 12 analysis/fix-owner update rather than a fresh health reading. **Role:** historical review. **Disposition:** update.

## proposals/one-planning-tool

- **[DESIGN.md](../proposals/one-planning-tool/DESIGN.md)** — Records the adopted one-tool design, OpenSpec/layout format, guard/check consolidation, normative docstrings and portable installation, with a concrete example and six delivery slices. **Role:** design. **Disposition:** keep.

## proposals/planning-package/review-page

- **[diagram-domain.html](../proposals/planning-package/review-page/diagram-domain.html)** — Hosts the typed domain graph explaining implemented, document-only and external AES concepts, as a derived reader view of domain sources. **Role:** generated. **Disposition:** generated.

- **[diagram-open-questions.html](../proposals/planning-package/review-page/diagram-open-questions.html)** — Hosts the typed question graph of ownership, blockers and affected concepts, with an embedded population needing current-ledger regeneration. **Role:** generated. **Disposition:** generated.

- **[diagram-system-map.html](../proposals/planning-package/review-page/diagram-system-map.html)** — Renders the code-unit system map and links its Markdown owner, answering which units belong to each part and what calls what. **Role:** generated. **Disposition:** generated.

- **[diagram-system-model-2.html](../proposals/planning-package/review-page/diagram-system-model-2.html)** — Renders the cross-repository view of AES parts and what consolidation moved, linking the planning system-model source. **Role:** generated. **Disposition:** generated.

- **[diagram-system-model.html](../proposals/planning-package/review-page/diagram-system-model.html)** — Renders the context view of AES parts, owning repositories and communication paths from the planning system-model source. **Role:** generated. **Disposition:** generated.

- **[graph-viewer.js](../proposals/planning-package/review-page/graph-viewer.js)** — Bundles GraphViewer and browser rendering dependencies for the typed-graph views, exposing their mounting/configuration behavior rather than authored domain claims. **Role:** generated asset. **Disposition:** generated.

- **[index.html](../proposals/planning-package/review-page/index.html)** — Provides review navigation to goal, criteria, decisions, diagrams, rollout and evidence; its completion banner and eight-question count reflect an older source state. **Role:** generated. **Disposition:** generated.

- **[lockstep-acceptance.html](../proposals/planning-package/review-page/lockstep-acceptance.html)** — Displays A1–A5 historical expected/observed acceptance rows, commands and file previews; PASS labels remain bounded by each run and do not prove active installation enforcement. **Role:** generated evidence view. **Disposition:** generated.

- **[marked.min.js](../proposals/planning-package/review-page/marked.min.js)** — Vendors the MIT-licensed Marked v12.0.2 Markdown parser/renderer used by review pages, retaining dependency identity and licence notice. **Role:** generated asset. **Disposition:** generated.

- **[open-questions.html](../proposals/planning-package/review-page/open-questions.html)** — Displays expanded open and collapsed resolved ledger questions; still reports eight open items and obsolete corrections-filing blockers despite newer source resolutions/questions. **Role:** generated. **Disposition:** generated.

- **[review.html](../proposals/planning-package/review-page/review.html)** — Combines plan, capabilities, criteria, decisions, architecture, spectrum, rollout and evidence into review UI; completion/open-question summaries need regeneration or historical framing. **Role:** generated. **Disposition:** generated.

## scripts

- **[relationships.yaml](../scripts/relationships.yaml)** — Defines required-reading defaults and otherwise empty governance graphs, plus commented relationship and audit-policy examples. **Role:** native configuration or contract. **Disposition:** keep.

## scripts/acceptance

- **[\_common.py](../scripts/acceptance/_common.py)** — Shared helpers for the Lockstep acceptance run scripts (A1 to A5). **Role:** executable helper. **Disposition:** keep.

- **[\_install.py](../scripts/acceptance/_install.py)** — Shared pieces of the A1 and A5 runs: take the install command from the README text, install into fresh repos. **Role:** executable helper. **Disposition:** keep.

- **[a1.py](../scripts/acceptance/a1.py)** — A1 run: the README's one command in a fresh repository. Writes docs/planning/runs/lockstep-acceptance/a1.json. **Role:** executable helper. **Disposition:** keep.

- **[a2.py](../scripts/acceptance/a2.py)** — A2 run: the edit guard on lifelike's plan. Writes docs/planning/runs/lockstep-acceptance/a2.json. **Role:** executable helper. **Disposition:** keep.

- **[a3.py](../scripts/acceptance/a3.py)** — A3 run: the commit checks, on four real commits in a throwaway git repository. **Role:** executable helper. **Disposition:** keep.

- **[a4.py](../scripts/acceptance/a4.py)** — A4 run: `lockstep layout` on an approved plan, then each planned file's first docstring against the plan. **Role:** executable helper. **Disposition:** keep.

- **[a5.py](../scripts/acceptance/a5.py)** — A5 run: portability. Writes docs/planning/runs/lockstep-acceptance/a5.json and a5-readme-agent.jsonl. **Role:** executable helper. **Disposition:** keep.

- **[build\_page.py](../scripts/acceptance/build_page.py)** — Build proposals/planning-package/review-page/lockstep-acceptance.html from the A1-A5 run records. **Role:** executable helper. **Disposition:** keep.

## scripts/hive

- **[README.md](../scripts/hive/README.md)** — Explains that Hive moved to personal-vps while brain_fresh.py stays for existing callers. **Role:** source document. **Disposition:** keep.

- **[brain\_fresh.py](../scripts/hive/brain_fresh.py)** — Is a project's brain older than the work done since? (hive brain v1, C-CONTEXT) **Role:** executable helper. **Disposition:** keep.

## scripts/learning_loop

- **[collect\_feedback.py](../scripts/learning_loop/collect_feedback.py)** — Extracts feedback and human corrections from changed native transcripts into local report records; filing creates private feedback issues, while writing the older learnings register is opt-in. **Role:** executable helper. **Disposition:** update.

- **[effects.py](../scripts/learning_loop/effects.py)** — Effect boundaries are explicit enforcement receipts, never issue-close dates. **Role:** executable helper. **Disposition:** keep.

- **[evidence.py](../scripts/learning_loop/evidence.py)** — Resolve feedback references and count independent, verified observations. **Role:** executable helper. **Disposition:** keep.

- **[feedback\_log.py](../scripts/learning_loop/feedback_log.py)** — Closeout Feedback fields -> feedback-report.v1 records -> the private feedback log. **Role:** executable helper. **Disposition:** keep.

- **[fix\_owner.py](../scripts/learning_loop/fix_owner.py)** — Processes licensed feedback fixes through an agent and verifies outcomes against GitHub; its weekly module label is stale relative to the daily service timer. **Role:** executable helper. **Disposition:** update.

- **[label\_items.py](../scripts/learning_loop/label_items.py)** — Label lessons with Jev into failure-mode families (AES learning loop, slices 1-2). **Role:** executable helper. **Disposition:** keep.

- **[licences.py](../scripts/learning_loop/licences.py)** — S4: licences for proposed fixes, derived by the Observation-to-Action evaluator (PLAN.md, slice S4). **Role:** executable helper. **Disposition:** keep.

- **[policies.py](../scripts/learning_loop/policies.py)** — Is each workspace rule documented, enforced, observed and on a feedback path? (plan aes-learning-loop, S8) **Role:** executable helper. **Disposition:** update.

- **[problems.py](../scripts/learning_loop/problems.py)** — S3: group related feedback records into problems and analyse the recurring ones (PLAN.md, slice S3). **Role:** executable helper. **Disposition:** keep.

- **[question\_set\_v2.json](../scripts/learning_loop/question_set_v2.json)** — Defines a frozen failure-family choice question with 23 lettered families, inclusion/exclusion guidance and confidence thresholds. **Role:** native configuration or contract. **Disposition:** keep.

- **[records.py](../scripts/learning_loop/records.py)** — Feedback records (contract feedback-report.v1): observations, claims and actions with links. **Role:** executable helper. **Disposition:** keep.

- **[relation\_check.py](../scripts/learning_loop/relation_check.py)** — S2 measurement: does Jev judge how two feedback records relate well enough? (PLAN.md, "The S2 measurement"). **Role:** executable helper. **Disposition:** keep.

- **[subagents.py](../scripts/learning_loop/subagents.py)** — Native child lifecycle -> existing feedback reports; parent checks bind exact results. **Role:** executable helper. **Disposition:** keep.

- **[transcripts.py](../scripts/learning_loop/transcripts.py)** — Read Claude Code and Codex transcripts as plain turns, and split closeout fields. **Role:** executable helper. **Disposition:** keep.

## scripts/learning_loop/systemd

- **[README.md](../scripts/learning_loop/systemd/README.md)** — Documents feedback installation, private stores, collection, labeling, recurring analysis, enforcement receipts and verified fix-owner dispositions. **Role:** source document. **Disposition:** keep.

- **[feedback-collector.service](../scripts/learning_loop/systemd/feedback-collector.service)** — Configures the nightly transcript-feedback collection and issue-filing job with clone refresh, environment and timeout; its Description still names the older learnings-register destination. **Role:** systemd configuration. **Disposition:** update.

- **[feedback-collector.timer](../scripts/learning_loop/systemd/feedback-collector.timer)** — Nightly feedback collector. Schedules *-*-* 03:30:00 with persistent catch-up and randomized delay. **Role:** systemd configuration. **Disposition:** keep.

- **[feedback-effects.service](../scripts/learning_loop/systemd/feedback-effects.service)** — Observe feedback rule effects without drafting or adopting new rules. Executes the configured feedback script with per-job environment and timeout. **Role:** systemd configuration. **Disposition:** keep.

- **[feedback-effects.timer](../scripts/learning_loop/systemd/feedback-effects.timer)** — Nightly feedback rule effect observation. Schedules *-*-* 07:30:00 with persistent catch-up and randomized delay. **Role:** systemd configuration. **Disposition:** keep.

- **[feedback-fix-owner.service](../scripts/learning_loop/systemd/feedback-fix-owner.service)** — Configures agent execution of licensed fixes and outcome verification with per-job settings; its weekly Description differs from the daily timer and does not establish current enablement. **Role:** systemd configuration. **Disposition:** update.

- **[feedback-fix-owner.timer](../scripts/learning_loop/systemd/feedback-fix-owner.timer)** — Daily feedback fix owner (09:00). Schedules *-*-* 09:00 with persistent catch-up and randomized delay. **Role:** systemd configuration. **Disposition:** keep.

- **[feedback-labels.service](../scripts/learning_loop/systemd/feedback-labels.service)** — Daily feedback labels: sort each feedback issue into a failure-mode family, hand unmatched ones to an agent. Executes the configured feedback script with per-job environment and timeout. **Role:** systemd configuration. **Disposition:** keep.

- **[feedback-labels.timer](../scripts/learning_loop/systemd/feedback-labels.timer)** — Daily feedback labels (after the 03:30 collector). Schedules *-*-* 05:00:00 with persistent catch-up and randomized delay. **Role:** systemd configuration. **Disposition:** keep.

- **[feedback-problems.service](../scripts/learning_loop/systemd/feedback-problems.service)** — Weekly feedback loop: group recurring problems, analyse, license fixes, hand them to agents, count effects. Executes the configured feedback script with per-job environment and timeout. **Role:** systemd configuration. **Disposition:** keep.

- **[feedback-problems.timer](../scripts/learning_loop/systemd/feedback-problems.timer)** — Weekly feedback loop (problems, licences, effects). Schedules Sun *-*-* 05:00:00 with persistent catch-up and randomized delay. **Role:** systemd configuration. **Disposition:** keep.

## scripts/meta

- **[check\_agents\_sync.py](../scripts/meta/check_agents_sync.py)** — Check that generated AGENTS.md is in sync with canonical governance inputs. **Role:** executable helper. **Disposition:** keep.

- **[render\_agents\_md.py](../scripts/meta/render_agents_md.py)** — Render a generated AGENTS.md projection from canonical repo governance. **Role:** executable helper. **Disposition:** keep.

## scripts/rules

- **[build\_rules\_page.py](../scripts/rules/build_rules_page.py)** — Build docs/rules/RULES.md: every rule agents in Brian's workspace are expected to follow. **Role:** executable helper. **Disposition:** update.

- **[sort\_legacy.py](../scripts/rules/sort_legacy.py)** — Sort project-meta's legacy rules into covered / keep / retire, with checked quotes (agent-router slice 1). **Role:** executable helper. **Disposition:** keep.

## src/agentic_engineering_system

- **[\_\_init\_\_.py](../src/agentic_engineering_system/__init__.py)** — Canonical Agentic Engineering System package. Contains no executable definitions. **Role:** code. **Disposition:** keep.

- **[adopt.py](../src/agentic_engineering_system/adopt.py)** — `aes adopt`: bring an existing repository under AES without planning its old files (`RU-AES-ADOPT`). **Role:** code. **Disposition:** keep.

- **[characterize.py](../src/agentic_engineering_system/characterize.py)** — Revision-bound characterization and target drift (`RU-AES-CHARACTERIZE`, `SC-GF-006`). **Role:** code. **Disposition:** keep.

- **[characterize\_python.py](../src/agentic_engineering_system/characterize_python.py)** — Python AST characterization provider (`RU-AES-CHARACTERIZE`, `SC-GF-006`). **Role:** code. **Disposition:** keep.

- **[cli.py](../src/agentic_engineering_system/cli.py)** — Defines the retained aes parser and command dispatch for initialization, adoption, validation, context, topology, evidence, planning and reconciliation. **Role:** code. **Disposition:** keep.

- **[context.py](../src/agentic_engineering_system/context.py)** — Bounded working-context compiler (probe 0): `aes context <subject>`. **Role:** code. **Disposition:** keep.

- **[evidence.py](../src/agentic_engineering_system/evidence.py)** — Observations, freshness and criterion standing (`RU-AES-EVIDENCE`, `SC-GF-007`, `SC-GF-008`, decision D2). **Role:** code. **Disposition:** keep.

- **[hooks.py](../src/agentic_engineering_system/hooks.py)** — `aes hooks install`: ship the consumer's pre-commit gate (`RU-AES-DISTRIBUTION`). **Role:** code. **Disposition:** keep.

- **[planning.py](../src/agentic_engineering_system/planning.py)** — `aes plan prepare / validate / accept` (`RU-AES-PLANNING`, `SC-GF-004`). **Role:** code. **Disposition:** keep.

- **[planning\_protocol.md](../src/agentic_engineering_system/planning_protocol.md)** — Documents the legacy AES proposal workflow: prepare gaps, write target deltas and trace-review declarations, validate and explicitly accept before implementation. **Role:** instruction. **Disposition:** keep.

- **[project.py](../src/agentic_engineering_system/project.py)** — `aes init` and project discovery (`RU-AES-PROJECT`, `SC-GF-001`). **Role:** code. **Disposition:** keep.

- **[reconcile.py](../src/agentic_engineering_system/reconcile.py)** — Qualified current state and target/current gaps (`RU-AES-RECONCILE`, `SC-GF-007`, `SC-GF-008` at the gap level). **Role:** code. **Disposition:** keep.

- **[records.py](../src/agentic_engineering_system/records.py)** — Strict typed records for `.aes/project.yaml` and `.aes/target.yaml` (probe 0). **Role:** code. **Disposition:** keep.

- **[topology.py](../src/agentic_engineering_system/topology.py)** — Governed-root topology check (`RU-AES-TOPOLOGY`, `SC-GF-003`). **Role:** code. **Disposition:** keep.

- **[trace\_review.py](../src/agentic_engineering_system/trace_review.py)** — Thin AES binding to Company Planning's source-bound review provider. **Role:** code. **Disposition:** keep.

## src/lockstep

- **[\_\_init\_\_.py](../src/lockstep/__init__.py)** — Introduces Lockstep and retains projected legacy requirements explaining planned files, typed seams, normative context, evidence and wiki navigation. Its migration wording predates completed consolidation. **Role:** code. **Disposition:** update.

- **[action\_check.py](../src/lockstep/action_check.py)** — Judge a proposed non-code action against the actions Lockstep's side file declares (behavior 5.4). **Role:** code. **Disposition:** keep.

- **[aes\_bridge.py](../src/lockstep/aes_bridge.py)** — Adapts legacy AES targets and modern OpenSpec/layout plans to shared root discovery, artifact lookup, full context and committed configuration reads. **Role:** code. **Disposition:** keep.

- **[behavior\_check.py](../src/lockstep/behavior_check.py)** — Report a behavior that lacks exactly one source file of its own or a criterion with a test route. **Role:** code. **Disposition:** keep.

- **[change\_list.py](../src/lockstep/change_list.py)** — After a plan change, list every file and symbol whose plan text changed, as one list for the agent. **Role:** code. **Disposition:** keep.

- **[change\_log.py](../src/lockstep/change_log.py)** — The append-only change log: one entry per accepted plan change, never edited afterwards. **Role:** code. **Disposition:** keep.

- **[check.py](../src/lockstep/check.py)** — `pcw check --repo PATH [--base REF] [--json]`: is a whole working tree still on its plan?. **Role:** code. **Disposition:** keep.

- **[cogtext.py](../src/lockstep/cogtext.py)** — Render plan text for a docstring. Called from cog blocks. **Role:** code. **Disposition:** keep.

- **[criterion\_checks.py](../src/lockstep/criterion_checks.py)** — Check every success criterion names how it is checked: a test, a sign-off or an AI rubric (behavior 2.1). **Role:** code. **Disposition:** keep.

- **[declared\_reason.py](../src/lockstep/declared_reason.py)** — Refuse a planned file whose declaration gives no reason (behavior 1.3). **Role:** code. **Disposition:** keep.

- **[doc\_projection.py](../src/lockstep/doc_projection.py)** — Statically extracts declared facts and refreshes targets with daily traces; its module docstring owns the component assessment, gaps, linked plan and separate evidence links. **Role:** code. **Disposition:** keep.

- **[docstring\_up.py](../src/lockstep/docstring_up.py)** — Turn an edit to a docstring's plan text into a draft plan change, which the coding agent accepts. **Role:** code. **Disposition:** keep.

- **[hook.py](../src/lockstep/hook.py)** — Agent edit hook (Claude Code and Codex PreToolUse): warn about, or refuse, an edit to a file the plan does not declare (behavior 5.1). **Role:** code. **Disposition:** keep.

- **[init\_repo.py](../src/lockstep/init_repo.py)** — Initializes Lockstep config and merges Claude/Codex hooks, lefthook commands and log ignore entries while preserving existing custom policy. **Role:** code. **Disposition:** keep.

- **[layout\_plan.py](../src/lockstep/layout_plan.py)** — The layout plan: OpenSpec says what the code must do, `layout:` rows in lockstep.yaml say which files exist and why. **Role:** code. **Disposition:** keep.

- **[linked\_tests.py](../src/lockstep/linked_tests.py)** — Check tests and criteria link both ways: every named test file exists, every test file is named. **Role:** code. **Disposition:** keep.

- **[openspec\_text.py](../src/lockstep/openspec_text.py)** — Read the OpenSpec requirement a file implements, so the edit hook hands the agent that text instead of the AES plan text (behavior 3.7, issue #54). **Role:** code. **Disposition:** keep.

- **[parent\_text.py](../src/lockstep/parent_text.py)** — Put each parent requirement, word for word, before a behavior's own text in its docstring. **Role:** code. **Disposition:** keep.

- **[plan\_check.py](../src/lockstep/plan_check.py)** — `lockstep plan check [--repo PATH] [--acceptance PATH] [--json]`: is the plan itself well formed?. **Role:** code. **Disposition:** keep.

- **[plan\_edit.py](../src/lockstep/plan_edit.py)** — Name the plan items an edit by hand to the plan file changes, and every file and symbol linked to them (behavior 3.8). **Role:** code. **Disposition:** update.

- **[plan\_to\_code.py](../src/lockstep/plan_to_code.py)** — Report where the committed code differs from the plan: a missing file, export or signature. **Role:** code. **Disposition:** keep.

- **[requirement\_status.py](../src/lockstep/requirement_status.py)** — Status that comes up from the code, and one page per requirement: its text, its status and its change log. **Role:** code. **Disposition:** keep.

- **[scaffold.py](../src/lockstep/scaffold.py)** — `python -m lockstep.scaffold`: create every file the plan declares that does not exist yet. **Role:** code. **Disposition:** keep.

- **[shell\_targets.py](../src/lockstep/shell_targets.py)** — Which paths a shell command writes: the parser the edit hook judges shell commands by (behavior 5.1). **Role:** code. **Disposition:** keep.

- **[side\_file.py](../src/lockstep/side_file.py)** — Read and check Lockstep's side file, `lockstep.yaml` beside the plan (behaviors 1.1, 2.1 and 5.1). **Role:** code. **Disposition:** keep.

- **[signature\_text.py](../src/lockstep/signature_text.py)** — Copy the typed signatures the plan declares for a file into its docstring (behavior 3.2). **Role:** code. **Disposition:** keep.

- **[stale\_edit.py](../src/lockstep/stale_edit.py)** — Stop an edit to a planned file while its docstring copy of the plan is stale (behavior 3.4). **Role:** code. **Disposition:** keep.

- **[symbol\_gate.py](../src/lockstep/symbol_gate.py)** — Report the public functions and classes, and the declared signatures, that a change to a planned file adds against the plan (behavior 5.5). **Role:** code. **Disposition:** keep.

- **[unplanned\_files.py](../src/lockstep/unplanned_files.py)** — Report a file the plan does not declare (behavior 1.1). **Role:** code. **Disposition:** keep.

- **[unplanned\_symbols.py](../src/lockstep/unplanned_symbols.py)** — Report a top-level function or class the plan does not declare with its types (behavior 1.2). **Role:** code. **Disposition:** keep.

- **[wiki.py](../src/lockstep/wiki.py)** — Build wiki pages from the plan, the evidence standing and the code docstrings. **Role:** code. **Disposition:** keep.

- **[wiki\_reach.py](../src/lockstep/wiki_reach.py)** — Check every page of a generated wiki is within two links of its front page, each link with a summary (behavior 6.2). **Role:** code. **Disposition:** keep.

## src/lockstep/checks

- **[\_\_init\_\_.py](../src/lockstep/checks/__init__.py)** — Lockstep's commit checks, ported from code2check at code2-template 6ce00a9: `lockstep check <name>`. Contains no executable definitions. **Role:** code. **Disposition:** keep.

- **[arch.py](../src/lockstep/checks/arch.py)** — Turn the LikeC4 diagram into import-linter contracts, and check the committed ones are current. **Role:** code. **Disposition:** keep.

- **[cli.py](../src/lockstep/checks/cli.py)** — `lockstep check <name> [options]`: run one commit check and apply its mode from `lockstep.yaml`. **Role:** code. **Disposition:** keep.

- **[config.py](../src/lockstep/checks/config.py)** — Loads and validates commit-check modes, human-source patterns, owner and LikeC4 version from lockstep.yaml with explicit defaults. **Role:** code. **Disposition:** keep.

- **[docmeta.py](../src/lockstep/checks/docmeta.py)** — Docmeta check: the OKF front matter of every page under `wiki/` is complete, fresh and findable. **Role:** code. **Disposition:** keep.

- **[markers.py](../src/lockstep/checks/markers.py)** — Uses Python ASTs to find implementation requirement IDs and pytest scenario markers under configured source and test roots. **Role:** code. **Disposition:** keep.

- **[plugin.py](../src/lockstep/checks/plugin.py)** — pytest plugin that registers the `req` marker linking a test to an OpenSpec scenario. **Role:** code. **Disposition:** keep.

- **[project.py](../src/lockstep/checks/project.py)** — Projection: write each requirement's text into the docstrings that implement it, and each plan's coverage into the plan. **Role:** code. **Disposition:** keep.

- **[show.py](../src/lockstep/checks/show.py)** — Show what one source file must keep true: the requirements its docstrings implement, with their text and scenarios. **Role:** code. **Disposition:** keep.

- **[sources.py](../src/lockstep/checks/sources.py)** — Sources check: every requirement and decision record says where it came from. **Role:** code. **Disposition:** keep.

- **[spec.py](../src/lockstep/checks/spec.py)** — Parses OpenSpec headings into requirement/scenario IDs and parent relationships, including active change deltas when requested. **Role:** code. **Disposition:** keep.

- **[status.py](../src/lockstep/checks/status.py)** — Status report: each requirement's implementers, each scenario's tests and whether they passed at this revision, and the IDs each plan has still to close. **Role:** code. **Disposition:** keep.

- **[test\_first.py](../src/lockstep/checks/test_first.py)** — Test-first check: a test for a scenario new since the base revision must fail on the base source. **Role:** code. **Disposition:** keep.

- **[trace.py](../src/lockstep/checks/trace.py)** — Trace check: every requirement has an implementer, every scenario a test, and no ID is unknown. **Role:** code. **Disposition:** keep.

## src/pcw

- **[\_\_init\_\_.py](../src/pcw/__init__.py)** — Aliases the pcw package path to lockstep so old module invocations and cog imports resolve without duplicate implementations. **Role:** code. **Disposition:** keep.

## tests

- **[README.md](../tests/README.md)** — Explains test scope and check commands, and distinguishes fixture consumers from deployment evidence. **Role:** navigation. **Disposition:** keep.

- **[conftest.py](../tests/conftest.py)** — Every test runs as on a clean machine: no machine-wide Git config, so no machine-wide hooks. **Role:** test-support. **Disposition:** keep.

- **[test\_agents\_rendering.py](../tests/test_agents_rendering.py)** — Checks RendererRuntime emits POSIX repository-relative paths and never backslash separators. **Role:** test. **Disposition:** keep.

- **[test\_records\_governed\_roots.py](../tests/test_records_governed_roots.py)** — A governed root written without a trailing slash must not capture sibling paths. **Role:** test. **Disposition:** keep.

- **[test\_rules\_page.py](../tests/test_rules_page.py)** — The rules page lists every register rule and the legacy register, and survives table-breaking text. **Role:** test. **Disposition:** keep.

- **[test\_sort\_legacy.py](../tests/test_sort_legacy.py)** — The legacy sort's evidence check rejects answers its quote or the file facts do not support. **Role:** test. **Disposition:** keep.

## tests/greenfield

- **[test\_adopt.py](../tests/greenfield/test_adopt.py)** — SC-ADOPT-001: adopting an existing repository, through the real CLI and the installed hooks. **Role:** test. **Disposition:** keep.

- **[test\_characterize.py](../tests/greenfield/test_characterize.py)** — `aes characterize`: revision-bound facts, Python AST extraction, symbol drift (SC-GF-006) and dependency discovery for recorded evidence. **Role:** test. **Disposition:** keep.

- **[test\_context.py](../tests/greenfield/test_context.py)** — Probe 0: `aes context <subject>` on the real whygame5 target. **Role:** test. **Disposition:** keep.

- **[test\_distribution.py](../tests/greenfield/test_distribution.py)** — Distribution and the packaged pre-commit hook (`RU-AES-DISTRIBUTION`). **Role:** test. **Disposition:** keep.

- **[test\_evidence.py](../tests/greenfield/test_evidence.py)** — `aes evidence status` on the whygame5 target (SC-GF-007, SC-GF-008, D2). **Role:** test. **Disposition:** keep.

- **[test\_evidence\_controls.py](../tests/greenfield/test_evidence_controls.py)** — Entry-level target dependencies and negative-control observations (roadmap phase 6a). **Role:** test. **Disposition:** keep.

- **[test\_planning.py](../tests/greenfield/test_planning.py)** — `aes plan prepare / validate / accept` (RU-AES-PLANNING, SC-GF-004 ER-01). **Role:** test. **Disposition:** keep.

- **[test\_project.py](../tests/greenfield/test_project.py)** — `aes init` and project discovery (`RU-AES-PROJECT`, `SC-GF-001`). **Role:** test. **Disposition:** keep.

- **[test\_reconcile.py](../tests/greenfield/test_reconcile.py)** — `aes reconcile` / `aes status`: qualified current state and derived gaps (RU-AES-RECONCILE; SC-GF-007 and SC-GF-008 at the gap level; SC-GF-004 "no route"). **Role:** test. **Disposition:** keep.

- **[test\_records.py](../tests/greenfield/test_records.py)** — Probe 0: strict target/project loading against the real whygame5 records. **Role:** test. **Disposition:** keep.

- **[test\_source\_bound\_trace\_review.py](../tests/greenfield/test_source_bound_trace_review.py)** — Counterexamples cross the actual CP provider, not a fabricated passing receipt. **Role:** test. **Disposition:** keep.

- **[test\_topology.py](../tests/greenfield/test_topology.py)** — `aes topology check` on the real whygame5 target (`SC-GF-003`). **Role:** test. **Disposition:** keep.

- **[test\_trace\_review.py](../tests/greenfield/test_trace_review.py)** — Plans require trace reviews (Brian, 2026-10-07). **Role:** test. **Disposition:** keep.

## tests/greenfield/fixtures

- **[whygame5-proposal-runner.yaml](../tests/greenfield/fixtures/whygame5-proposal-runner.yaml)** — Retains the whygame5 runner proposal adding fail-stop criteria, a negative-control artifact and its verification route, with trace-review metadata. **Role:** fixture. **Disposition:** keep.

## tests/greenfield/fixtures/whygame5-54043e2

- **[README](../tests/greenfield/fixtures/whygame5-54043e2/README)** — Names the exact whygame5 revision supplying the frozen AES fixture and requires deliberate refresh alongside tests. **Role:** fixture. **Disposition:** keep.

## tests/greenfield/fixtures/whygame5-54043e2/.aes

- **[project.yaml](../tests/greenfield/fixtures/whygame5-54043e2/.aes/project.yaml)** — Frozen whygame5 AES project identity, governed Python roots and materialization paths. **Role:** fixture. **Disposition:** keep.

- **[target.yaml](../tests/greenfield/fixtures/whygame5-54043e2/.aes/target.yaml)** — Frozen whygame5 target containing causal-explanation constraints, outcomes, criteria, artifacts and verification routes. **Role:** fixture. **Disposition:** keep.

## tests/learning

- **[test\_feedback\_collector\_reuse.py](../tests/learning/test_feedback_collector_reuse.py)** — Checks deferred feedback reports reuse their previously parsed record split rather than giving stable IDs different payloads on retry. **Role:** test. **Disposition:** keep.

- **[test\_feedback\_evidence\_effects.py](../tests/learning/test_feedback_evidence_effects.py)** — Checks resolved evidence and effect counting using exact timestamps and enforcement receipts, including restated incidents, corrections and changed group identities. **Role:** test. **Disposition:** keep.

- **[test\_feedback\_filing\_gate.py](../tests/learning/test_feedback_filing_gate.py)** — Filing gate of the feedback collector: only closeout Learnings lines file, and a line already filed is not filed again (2026-10-07 spot check: 2 of 10 filed entries were exact repeats). **Role:** test. **Disposition:** keep.

- **[test\_feedback\_records.py](../tests/learning/test_feedback_records.py)** — feedback-report.v1 parsing: the plan's canonical example and its negative controls (https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/proposals/aes-learning-loop/PLAN.md, "Fixtures"). **Role:** test. **Disposition:** keep.

- **[test\_feedback\_report\_cap.py](../tests/learning/test_feedback_report_cap.py)** — Checks human-correction deduplication, hourly pacing, nightly caps and correction priority ahead of other reports. **Role:** test. **Disposition:** keep.

- **[test\_feedback\_transcripts.py](../tests/learning/test_feedback_transcripts.py)** — Synthetic-transcript tests for scripts/learning_loop/transcripts.py (no real transcript text here). **Role:** test. **Disposition:** keep.

- **[test\_fix\_owner.py](../tests/learning/test_fix_owner.py)** — Tests that handling a licensed fix is established from GitHub outcomes and enforcement receipts rather than the executing agent’s self-report. **Role:** test. **Disposition:** keep.

- **[test\_label\_items.py](../tests/learning/test_label_items.py)** — Feedback labels: every page of the feedback log is read, and unmatched failures reach an agent. **Role:** test. **Disposition:** keep.

- **[test\_licences.py](../tests/learning/test_licences.py)** — S4: licence status comes from the Observation-to-Action evaluator (R-401), on the plan's fixtures. **Role:** test. **Disposition:** keep.

- **[test\_policies.py](../tests/learning/test_policies.py)** — Checks policy IDs missing from the register or source documentation appear as gaps and defaults point at the AES register. **Role:** test. **Disposition:** keep.

- **[test\_problems.py](../tests/learning/test_problems.py)** — S3 recurrence rule: independent observations with links; echoes of the same evidence count once. **Role:** test. **Disposition:** keep.

- **[test\_relation\_check.py](../tests/learning/test_relation_check.py)** — S2 scoring rules: acceptable answers fixed with the labels, and the parity rule. **Role:** test. **Disposition:** keep.

- **[test\_subagents.py](../tests/learning/test_subagents.py)** — Native lifecycle capture and counterexamples to child self-rating as evidence. **Role:** test. **Disposition:** keep.

## tests/lockstep

- **[conftest.py](../tests/lockstep/conftest.py)** — Lockstep's tests: the example projects and end-to-end scripts are inputs the tests copy, not tests. Contains no executable definitions. **Role:** test-support. **Disposition:** keep.

- **[lockstep\_support.py](../tests/lockstep/lockstep_support.py)** — Shared fixtures: the smallest example (example-simple), adopted, planned and committed. **Role:** test-support. **Disposition:** keep.

- **[test\_lockstep\_action\_check.py](../tests/lockstep/test_lockstep_action_check.py)** — Tests a proposed non-code action is allowed only when it matches the declared action it names. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_behavior\_check.py](../tests/lockstep/test_lockstep_behavior_check.py)** — Tests every behavior has exactly one source file of its own and a criterion with a test route. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_change\_list.py](../tests/lockstep/test_lockstep_change_list.py)** — Tests after a plan change, the agent gets one list of every file and symbol linked to a changed item. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_change\_log.py](../tests/lockstep/test_lockstep_change_log.py)** — Tests every normative change has one entry in an append-only change log. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check.py](../tests/lockstep/test_lockstep_check.py)** — Tests `pcw check`, the whole-tree check the Project Brain runner calls before it commits. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_cogtext.py](../tests/lockstep/test_lockstep_cogtext.py)** — Tests cog copies the plan's text into the docstring, word for word (7.1 is tests/test_parent_text.py). **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_criterion\_checks.py](../tests/lockstep/test_lockstep_criterion_checks.py)** — Tests every success criterion names how it is checked: a test, a sign-off or an AI rubric. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_declared\_reason.py](../tests/lockstep/test_lockstep_declared_reason.py)** — Tests a planned file whose declaration gives no reason is refused. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_docstring\_up.py](../tests/lockstep/test_lockstep_docstring_up.py)** — Tests an edit to a docstring's plan text becomes a draft plan change, accepted by the agent when it is confident or the change is not significant, otherwise by a person. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_e2e.py](../tests/lockstep/test_lockstep_e2e.py)** — The whole example, end to end: every step's expected exit and key output. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_hook.py](../tests/lockstep/test_lockstep_hook.py)** — Tests at edit time the hook warns about an edit to a file the plan does not declare, and refuses it for a file the side file marks fixed (or everywhere under PCW_MODE=block). **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_init.py](../tests/lockstep/test_lockstep_init.py)** — `lockstep init` installs Lockstep in a repository: config, Claude Code and Codex hooks, lefthook. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_layout\_plan.py](../tests/lockstep/test_lockstep_layout_plan.py)** — Slice 2 of the one-tool design: the plan is OpenSpec plus `layout:` rows in lockstep.yaml, with no .aes/. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_linked\_tests.py](../tests/lockstep/test_lockstep_linked_tests.py)** — Tests every test file a criterion names exists, and every test file is named by a criterion. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_openspec\_text.py](../tests/lockstep/test_lockstep_openspec_text.py)** — Tests in a repository with OpenSpec specs, the text the hook hands the agent before an edit is the OpenSpec requirement the file implements (its `Implements: <capability>/<requirement>` docstring line); `.aes/target.yaml` stays the source for a repository without OpenSpec (issue #54). **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_package.py](../tests/lockstep/test_lockstep_package.py)** — Lockstep installs from AES canonical, and its old `pcw` names keep working (one-tool design, slice 1). **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_parent\_text.py](../tests/lockstep/test_lockstep_parent_text.py)** — Tests a behavior's docstring carries its parent requirement in full, before its own text. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_plan\_check.py](../tests/lockstep/test_lockstep_plan_check.py)** — `lockstep plan check`: the acceptance-criteria file and the plan's requirements (slice 5). **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_plan\_check\_requirements.py](../tests/lockstep/test_lockstep_plan_check_requirements.py)** — `lockstep plan check`, requirement coverage: the offline checks of a stored judgment. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_plan\_edit.py](../tests/lockstep/test_lockstep_plan_edit.py)** — Tests an edit by hand to the plan file is warned about at edit time, with every linked file and symbol. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_plan\_to\_code.py](../tests/lockstep/test_lockstep_plan_to_code.py)** — Tests a missing planned file, a missing export and a changed signature are each reported. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_requirement\_status.py](../tests/lockstep/test_lockstep_requirement_status.py)** — Tests one page per requirement, its status from the code and the evidence, none typed. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_scaffold.py](../tests/lockstep/test_lockstep_scaffold.py)** — Tests every declared file that does not exist yet is created with its cog block. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_shell\_targets.py](../tests/lockstep/test_lockstep_shell_targets.py)** — Tests the hook judges a shell command by the paths it writes, found the way code2check's guard finds them (ported from code2-template `src/code2check/guard.py` at 6ce00a9). **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_signature\_text.py](../tests/lockstep/test_lockstep_signature_text.py)** — Tests after `make project`, every export the plan declares for a file is in its docstring as declared. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_stale\_edit.py](../tests/lockstep/test_lockstep_stale_edit.py)** — Tests an edit to a planned file is warned about, or waits when the hook blocks, while its docstring copy is stale. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_symbol\_gate.py](../tests/lockstep/test_lockstep_symbol_gate.py)** — Tests an added undeclared public symbol or a changed declared signature is warned at edit and refused before commit. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_unplanned\_documents.py](../tests/lockstep/test_lockstep_unplanned_documents.py)** — Tests a document Lockstep's side file does not declare is reported. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_unplanned\_files.py](../tests/lockstep/test_lockstep_unplanned_files.py)** — Tests a file the plan does not declare is reported (code and tests under governed folders). **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_unplanned\_other\_files.py](../tests/lockstep/test_lockstep_unplanned_other_files.py)** — Tests with a `files` section in the side file, every tracked file outside the governed folders that is not a document must be declared there. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_unplanned\_symbols.py](../tests/lockstep/test_lockstep_unplanned_symbols.py)** — Tests a top-level function or class the plan does not declare with its types is reported. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_wiki\_reach.py](../tests/lockstep/test_lockstep_wiki_reach.py)** — Tests every page of a generated wiki is within two links of its front page, each link with a summary. **Role:** test. **Disposition:** keep.

## tests/lockstep/checks

- **[lockstep\_checks\_support.py](../tests/lockstep/checks/lockstep_checks_support.py)** — Helpers that build small throwaway repositories for the commit checks to run on (from code2check's conftest). **Role:** test-support. **Disposition:** keep.

- **[test\_lockstep\_check\_arch.py](../tests/lockstep/checks/test_lockstep_check_arch.py)** — Exercises LikeC4 contract generation, stale/invalid diagrams, forbidden/allowed imports and missing import-linter handling. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_docmeta.py](../tests/lockstep/checks/test_lockstep_check_docmeta.py)** — Checks wiki types, freshness, successors, duplicate topic ownership and navigation depth, with clean/no-wiki controls. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_plugin.py](../tests/lockstep/checks/test_lockstep_check_plugin.py)** — Tests for the pytest plugin, the top-level wiring and the modes of `lockstep check project`. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_project.py](../tests/lockstep/checks/test_lockstep_check_project.py)** — Exercises normative requirement and plan-coverage projection, stale detection and source-preserving docstring rewriting. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_show.py](../tests/lockstep/checks/test_lockstep_check_show.py)** — Checks show prints implemented requirements and reports files without implementation links. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_sources.py](../tests/lockstep/checks/test_lockstep_check_sources.py)** — Checks missing requirement/decision sources and classification of human and agent-derived attribution. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_status.py](../tests/lockstep/checks/test_lockstep_check_status.py)** — Checks status links, pass/fail/skip outcomes, revision/dirty-tree invalidation and open plan IDs. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_status\_page.py](../tests/lockstep/checks/test_lockstep_check_status_page.py)** — Checks generated docs/status.md coverage contents, stale rejection and behavior without a docs folder. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_test\_first.py](../tests/lockstep/checks/test_lockstep_check_test_first.py)** — Tests for the test-first check, run on real throwaway git repositories. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_check\_trace.py](../tests/lockstep/checks/test_lockstep_check_trace.py)** — Checks requirement/test trace completeness and unknown IDs across configured roots, wrapped implementation lines and active changes. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_checks\_config.py](../tests/lockstep/checks/test_lockstep_checks_config.py)** — `lockstep.yaml` sets each commit check to block, warn or off, and the other settings the checks read. **Role:** test. **Disposition:** keep.

- **[test\_lockstep\_doc\_projection.py](../tests/lockstep/checks/test_lockstep_doc_projection.py)** — Source-owned facts reach wiki blocks; stale copies fail without executing source. **Role:** test. **Disposition:** keep.

## tests/lockstep/e2e

- **[run.py](../tests/lockstep/e2e/run.py)** — Run the full example end to end in a fresh folder and record every step. **Role:** test. **Disposition:** keep.

- **[simple.py](../tests/lockstep/e2e/simple.py)** — The smallest example: one function, one requirement, every part shown. **Role:** test. **Disposition:** keep.

## tests/lockstep/example

- **[Makefile](../tests/lockstep/example/Makefile)** — Provides people-finder project/wiki/check commands using docstring drafts, cog, legacy AES validation, MkDocs and pytest. **Role:** fixture. **Disposition:** keep.

- **[mkdocs.yml](../tests/lockstep/example/mkdocs.yml)** — Configures the people-finder MkDocs fixture with generated pages and mkdocstrings reading Python under src. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example-layout

- **[lockstep.yaml](../tests/lockstep/example-layout/lockstep.yaml)** — Defines the modern greeting layout fixture with governed src, planned greeter/test files, OpenSpec links and a typed greet export. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example-layout/openspec/specs/greeting

- **[spec.md](../tests/lockstep/example-layout/openspec/specs/greeting/spec.md)** — Defines the fixture greeting requirement and Ada scenario expecting Hello, Ada!. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example-simple

- **[Makefile](../tests/lockstep/example-simple/Makefile)** — Provides minimal scaffold/project/wiki/check commands, drafting normative edits before cog regeneration and validating the legacy AES plan. **Role:** fixture. **Disposition:** keep.

- **[mkdocs.yml](../tests/lockstep/example-simple/mkdocs.yml)** — Configures the greeter MkDocs fixture with generated pages and mkdocstrings reading Python under src. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example-simple/docs

- **[gen\_pages.py](../tests/lockstep/example-simple/docs/gen_pages.py)** — Generates greeter fixture wiki pages at MkDocs build time using lockstep.wiki.pages. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example-simple/plans

- **[plan-001.yaml](../tests/lockstep/example-simple/plans/plan-001.yaml)** — Plans greeting behavior, the Ada criterion, source/test artifacts and verification route before implementation. **Role:** fixture. **Disposition:** keep.

- **[plan-002.yaml](../tests/lockstep/example-simple/plans/plan-002.yaml)** — Changes greeting behavior and criterion to reject empty names with ValueError, providing a normative-drift example. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example-simple/src/greeter

- **[\_\_init\_\_.py](../tests/lockstep/example-simple/src/greeter/__init__.py)** — Implements greet(name) with a normative cog block and a direct Hello, <name>! return. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example-simple/tests

- **[test\_greet.py](../tests/lockstep/example-simple/tests/test_greet.py)** — Asserts greet returns Hello, Ada! for Ada as the initial fixture proving test. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example/.claude

- **[settings.json](../tests/lockstep/example/.claude/settings.json)** — Registers the legacy pcw-hook PreToolUse matcher for the people-finder Claude fixture. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example/.codex

- **[hooks.json](../tests/lockstep/example/.codex/hooks.json)** — Registers the legacy pcw-hook PreToolUse matcher for the people-finder Codex fixture without the newer client-specific flag. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example/docs

- **[gen\_pages.py](../tests/lockstep/example/docs/gen_pages.py)** — Generates people-finder fixture wiki pages at MkDocs build time using lockstep.wiki.pages. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example/plans

- **[plan-001-find-people.yaml](../tests/lockstep/example/plans/plan-001-find-people.yaml)** — Plans case-insensitive current-employer search, blank-company rejection, invented profile data and source/test/evidence routes. **Role:** fixture. **Disposition:** keep.

- **[plan-002-sorted.yaml](../tests/lockstep/example/plans/plan-002-sorted.yaml)** — Changes people-finder behavior and criterion to require name-sorted results while retaining employer matching and blank-input rules. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example/src/people_finder

- **[\_\_init\_\_.py](../tests/lockstep/example/src/people_finder/__init__.py)** — People finder: find the people who work at a target company now. **Role:** fixture. **Disposition:** keep.

- **[profiles.json](../tests/lockstep/example/src/people_finder/profiles.json)** — Contains five invented profiles, employer case variation and a former employee for search inclusion/exclusion cases. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/example/tests

- **[test\_find\_people.py](../tests/lockstep/example/tests/test_find_people.py)** — Checks the exact current-employee handle set, excludes the former employee and rejects blank company input. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/lockstep-plan-sample

- **[README.md](../tests/lockstep/lockstep-plan-sample/README.md)** — Names the frozen Lockstep sample revision and its typed-plan hook/symbol regression use without importing fixture code. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/lockstep-plan-sample/.aes

- **[project.yaml](../tests/lockstep/lockstep-plan-sample/.aes/project.yaml)** — Frozen Lockstep project record specifying src/pcw and tests governed roots and legacy materialization paths. **Role:** fixture. **Disposition:** keep.

- **[target.yaml](../tests/lockstep/lockstep-plan-sample/.aes/target.yaml)** — Frozen legacy Lockstep target with seven outcomes, detailed behaviors, criteria, artifacts and typed exports for realistic regressions. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/lockstep-plan-sample/.codex

- **[hooks.json](../tests/lockstep/lockstep-plan-sample/.codex/hooks.json)** — Preserves frozen Lockstep Codex registration using uv run --quiet --frozen pcw-hook --client codex. **Role:** fixture. **Disposition:** keep.

## tests/lockstep/lockstep-plan-sample/src/pcw

- **[action\_check.py](../tests/lockstep/lockstep-plan-sample/src/pcw/action_check.py)** — Frozen legacy action-check module with projected contract and typed exports used as edit/symbol regression data. **Role:** fixture. **Disposition:** keep.

## wiki

- **[documents.md](../wiki/documents.md)** — Complete tracked-file navigation catalog grouped by folder, with a source-grounded summary, role and review disposition for each file plus owning external sources. **Role:** source document. **Disposition:** generated.

- **[feedback-loop.md](../wiki/feedback-loop.md)** — Routes correction-to-verified-change understanding to component architecture and operator guidance with evidence limits. **Role:** source document. **Disposition:** keep.

- **[glossary.md](../wiki/glossary.md)** — Defines current AES, Lockstep and evidence/projection concepts separately from retained engine vocabulary. **Role:** source document. **Disposition:** keep.

- **[goal.md](../wiki/goal.md)** — Concise navigation to AES purpose and the planning, Lockstep, feedback and policy functions, with current state and history routes. **Role:** source document. **Disposition:** keep.

- **[history.md](../wiki/history.md)** — Organizes bootstrap, greenfield self-governance, predecessor archive, commit-rule removal and retired proposals as source-linked history. **Role:** source document. **Disposition:** keep.

- **[index.md](../wiki/index.md)** — Question-based navigation to AES architecture, ecosystem predecessor review, implementation, complete source inventory and open concerns. **Role:** source document. **Disposition:** keep.

- **[lockstep.md](../wiki/lockstep.md)** — Routes contracts and limits, distinguishes earlier replay from native self-adoption and includes the generated source-owned component assessment. **Role:** source document. **Disposition:** keep.

- **[open-questions.md](../wiki/open-questions.md)** — Projects unresolved questions and recommendations from the owning ledger, including ecosystem consolidation and predecessor review. **Role:** source document. **Disposition:** keep.

- **[policy-and-rules.md](../wiki/policy-and-rules.md)** — Maps policy authority and enforcement concepts to the original 263-entry Project Meta registry, provisional migration manifest, small AES register and current shared instructions. **Role:** source document. **Disposition:** keep.

- **[requirements.md](../wiki/requirements.md)** — Routes current OpenSpec contracts, including assessment self-adoption, to implementation and bounded evidence. **Role:** source document. **Disposition:** keep.

- **[research-and-lessons.md](../wiki/research-and-lessons.md)** — Indexes retained research syntheses with non-normative descriptions and revision-bound source links. **Role:** source document. **Disposition:** keep.

- **[run-and-deploy.md](../wiki/run-and-deploy.md)** — Provides retained install/check and feedback operation commands, distinguishing command existence from active installed enforcement. **Role:** source document. **Disposition:** keep.

- **[system-model.md](../wiki/system-model.md)** — Maps current parts to code, contracts, configuration and storage while distinguishing retained compatibility from active ownership. **Role:** source document. **Disposition:** keep.
