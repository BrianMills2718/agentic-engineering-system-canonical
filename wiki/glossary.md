---
type: Glossary
title: Glossary
description: The names a reader meets in this repository and what each means, with where it is defined.
status: current
updated: 2026-11-11
sources: [CLAUDE.md, docs/planning/DOMAIN.md, docs/architecture/SYSTEM_BOUNDARY.md, docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md, docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md, .project-brain/project.md, .project-brain/now.md, scripts/learning_loop/records.py, scripts/learning_loop/label_items.py, scripts/learning_loop/licences.py, scripts/learning_loop/fix_owner.py, src/agentic_engineering_system/records.py, docs/failure-modes.md, docs/rules/RULES.md, lefthook.yml, proposals/code2-ecosystem/PLAN.md, proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md, docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md, code2-workspace docs/decisions/0009-aes-and-lockstep-fate.md]
---

# Glossary

The v0.2 engine terms are defined in full, with their code locations, in [docs/planning/DOMAIN.md](../docs/planning/DOMAIN.md); Brian's reasoning vocabulary is in [docs/terms/ecosystem-terms.md](../docs/terms/ecosystem-terms.md). [docs/planning/DOMAIN.md:7-10](../docs/planning/DOMAIN.md#L7-L10)
- [Goal](goal.md) (related page)
- [System model](system-model.md) (related page)

| Term | Meaning | Source |
| --- | --- | --- |
| AES | the whole agent system: Lockstep, the feedback loop and the policy layer | [CLAUDE.md:14-16](../CLAUDE.md#L14-L16) |
| AES canonical | this repository, which is the Agentic Engineering System; `Inside-Success/agentic-engineering-system` is archived | [docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:44-49](../docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L44-L49) |
| Lockstep | the AES component that puts normative context at an edit and links planned structure to code; its own repository; winding down | [docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29) [docs/decisions/0009-aes-and-lockstep-fate.md:105-106](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L105-L106) |
| pcw | Lockstep's package; Team-Brains runs `pcw check --json` from a vendored wheel | [docs/decisions/0009-aes-and-lockstep-fate.md:27-31](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L27-L31) |
| code2check | the code2 tool that writes requirement text under a docstring's `Implements:` line and fails on a stale copy; gains Lockstep's edit-time refusal | [docs/decisions/0009-aes-and-lockstep-fate.md:33-35](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L33-L35) [docs/decisions/0009-aes-and-lockstep-fate.md:107-108](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L107-L108) |
| code2 (`~/code2`) | Brian's fresh workspace on off-the-shelf tools since 2026-10-13 | [proposals/code2-ecosystem/PLAN.md:21-27](../proposals/code2-ecosystem/PLAN.md#L21-L27) |
| OpenSpec | the off-the-shelf tool for required behavior; behavior changes go through it | [CLAUDE.md:24-25](../CLAUDE.md#L24-L25) |
| lefthook | the git hook runner, configured from code2-workspace's shared `hooks/base.yml` | [lefthook.yml:1-7](../lefthook.yml#L1-L7) |
| Enforced Planning | the v0.1 execution-governance provider: claims, lanes, checkpoints, controls | [docs/architecture/SYSTEM_BOUNDARY.md:41](../docs/architecture/SYSTEM_BOUNDARY.md#L41) |
| Company Planning | the planning and design derivation provider and its adoption gate | [docs/architecture/SYSTEM_BOUNDARY.md:41](../docs/architecture/SYSTEM_BOUNDARY.md#L41) |
| ACA | Agentic Capability Architecture; its capability catalogue is applied through AES, not run as a separate platform | [CLAUDE.md:113](../CLAUDE.md#L113) [docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md:42-45](../docs/decisions/0012-capability-reuse-enforced-at-plan-adoption.md#L42-L45) |
| Project Brain | the `.project-brain/` files (now, state, truth, project) an agent reads first | [docs/planning/DOMAIN.md:43](../docs/planning/DOMAIN.md#L43) |
| Hive brain v1 | Brian's personal hive of agents and project brains (2026-10-02), moved to personal-vps | [.project-brain/project.md:9-11](../.project-brain/project.md#L9-L11) [.project-brain/now.md:80](../.project-brain/now.md#L80) |
| Governed root | a folder AES governed; only files there had to be planned | [docs/planning/DOMAIN.md:23](../docs/planning/DOMAIN.md#L23) |
| Target | the plan of record, `.aes/target.yaml` | [docs/planning/DOMAIN.md:14](../docs/planning/DOMAIN.md#L14) |
| Outcome, normative item, success criterion, evidence requirement | the target's intent families | [docs/planning/DOMAIN.md:15-18](../docs/planning/DOMAIN.md#L15-L18) |
| Component, planned artifact, verification subject, external boundary | the target's realization families | [docs/planning/DOMAIN.md:19-22](../docs/planning/DOMAIN.md#L19-L22) |
| Proposal, accepted plan | a target delta, and that delta once accepted into `.aes/plans/` | [docs/planning/DOMAIN.md:25-27](../docs/planning/DOMAIN.md#L25-L27) |
| Observation | an append-only evidence record bound to a commit and its dependencies | [docs/planning/DOMAIN.md:29](../docs/planning/DOMAIN.md#L29) |
| Assessment | an observation's verdict on one evidence requirement | [docs/planning/DOMAIN.md:30](../docs/planning/DOMAIN.md#L30) |
| Negative control | a case a control should refuse | [docs/planning/DOMAIN.md:31](../docs/planning/DOMAIN.md#L31) |
| Freshness | CURRENT, STALE, UNKNOWN or UNREACHABLE, computed from Git | [docs/planning/DOMAIN.md:32](../docs/planning/DOMAIN.md#L32) |
| Standing | SUPPORTED, REFUTED or INSUFFICIENT per criterion | [docs/planning/DOMAIN.md:33](../docs/planning/DOMAIN.md#L33) |
| Characterization | what HEAD contains under the governed roots | [docs/planning/DOMAIN.md:34](../docs/planning/DOMAIN.md#L34) |
| Drift, orphan, gap | changed committed symbols, an unplanned governed file, an unmet criterion | [docs/planning/DOMAIN.md:35-37](../docs/planning/DOMAIN.md#L35-L37) |
| Legacy baseline | `aes adopt`'s frozen list of existing governed files | [docs/planning/DOMAIN.md:39](../docs/planning/DOMAIN.md#L39) |
| Working context | `aes context <subject>`'s smallest complete packet | [docs/planning/DOMAIN.md:40](../docs/planning/DOMAIN.md#L40) |
| Commit rule | commit tags and plan adoption per commit; retired 2026-10-14 | [docs/planning/DOMAIN.md:49](../docs/planning/DOMAIN.md#L49) |
| Trace review | someone other than the author reads a run's full trace and checks decisions against sources | [src/agentic_engineering_system/records.py:53-56](../src/agentic_engineering_system/records.py#L53-L56) |
| Feedback report | a `feedback-report.v1` set of observation, claim and action records from a closeout | [scripts/learning_loop/records.py:1-9](../scripts/learning_loop/records.py#L1-L9) |
| Jev | `typesafe/jev-1.13`, the fast choice model used for labels and relations | [scripts/learning_loop/label_items.py:55](../scripts/learning_loop/label_items.py#L55) |
| Failure-mode family | one lettered family of the taxonomy, each with a detecting question | [docs/failure-modes.md:4-5](../docs/failure-modes.md#L4-L5) |
| Licence | the derived permission for a claim to justify a rule or check | [scripts/learning_loop/licences.py:1-5](../scripts/learning_loop/licences.py#L1-L5) |
| Fix owner | the job that hands licensed fixes to a headless Claude Code session and checks the results | [scripts/learning_loop/fix_owner.py:1-9](../scripts/learning_loop/fix_owner.py#L1-L9) |
| Rules register | `docs/rules/register.yaml`, rendered as `docs/rules/RULES.md` | [docs/rules/RULES.md:3](../docs/rules/RULES.md#L3) |
| Plan 001, Repository Context | the v0.1 first vertical resolving one checkout's authority surfaces | [docs/planning/DOMAIN.md:42](../docs/planning/DOMAIN.md#L42) |
| Plan 002 | the v0.1 offline policy-decision replay; stopped at provider access | [docs/planning/DOMAIN.md:47](../docs/planning/DOMAIN.md#L47) |
| whygame5 | the first greenfield consumer of v0.2 | [proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md:121-126](../proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md#L121-L126) |
| Value tally | Decision 0011's measure of AES catches against hand checks | [docs/planning/DOMAIN.md:46](../docs/planning/DOMAIN.md#L46) |
| Checked-boundary thesis | the v0.2 bet that checked boundaries keep agent-built software true to intent; unmeasured | [docs/planning/DOMAIN.md:44](../docs/planning/DOMAIN.md#L44) |
| wiki_methodology | the adopted project-agnostic architecture, pinned by revision | [CLAUDE.md:10](../CLAUDE.md#L10) |
| Utility-discovery latency | time and cost until the intended actor can judge whether they want more | [docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md:22-27](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md#L22-L27) |
