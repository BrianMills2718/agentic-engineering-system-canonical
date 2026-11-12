---
type: SystemModel
title: System model
description: What code this repository holds, its entry points, data flow, storage and dependencies, and which parts retire under decision 0009.
status: current
updated: 2026-11-11
sources: [pyproject.toml, Makefile, lefthook.yml, .agentic/repo.yaml, .aes/target.yaml, src/agentic_engineering_system/cli.py, src/agentic_engineering_system/records.py, src/agentic_engineering_system/project.py, src/agentic_engineering_system/planning.py, src/agentic_engineering_system/topology.py, src/agentic_engineering_system/characterize.py, src/agentic_engineering_system/characterize_python.py, src/agentic_engineering_system/evidence.py, src/agentic_engineering_system/reconcile.py, src/agentic_engineering_system/context.py, src/agentic_engineering_system/hooks.py, src/agentic_engineering_system/adopt.py, src/agentic_engineering_system/trace_review.py, src/agentic_engineering_system/repository_context/cli.py, scripts/hive/brain_fresh.py, docs/planning/SYSTEM_MODEL.md, docs/planning/DOMAIN.md, docs/architecture/greenfield-v0.2/README.md]
---

# System model

This page describes code from the build files and the first lines of each module; behavior beyond those lines is not claimed here. [pyproject.toml:26-31](../pyproject.toml#L26-L31)
- [Goal](goal.md) (related page)
- [Run and deploy](run-and-deploy.md) (related page)

## Entry points

- The distribution `agentic-engineering-system` installs two console scripts: `aes` and `aes-repo-context`. [pyproject.toml:6](../pyproject.toml#L6) [pyproject.toml:26-28](../pyproject.toml#L26-L28)
- `aes` commands: init, adopt, target validate, context, topology check, evidence status and record, hooks install, characterize, reconcile, status, plan prepare, validate and accept. [src/agentic_engineering_system/cli.py:3-17](../src/agentic_engineering_system/cli.py#L3-L17)
- `aes` exits 0 on success, 1 on any load, validation or topology error, orphan, REFUTED criterion or drift, and 2 on usage errors. [src/agentic_engineering_system/cli.py:22-27](../src/agentic_engineering_system/cli.py#L22-L27)
- `aes-repo-context --repo PATH [--expect-revision SHA]` resolves one checkout's authority surfaces and writes `context.json` and an HTML surface. [src/agentic_engineering_system/repository_context/cli.py:10-34](../src/agentic_engineering_system/repository_context/cli.py#L10-L34)
- The feedback loop's scripts run under systemd, not as package entry points; see [Feedback loop](feedback-loop.md). [scripts/learning_loop/systemd/feedback-collector.service:20](../scripts/learning_loop/systemd/feedback-collector.service#L20)
- `scripts/hive/brain_fresh.py <repo>` exits 0 when a project brain is fresh, 1 when stale or behind origin, 2 when there is no brain. [scripts/hive/brain_fresh.py:11-17](../scripts/hive/brain_fresh.py#L11-L17)

## The retained library: `src/agentic_engineering_system`

| Module | Job | Source |
| --- | --- | --- |
| `records.py` | strict typed records for `.aes/project.yaml` and `.aes/target.yaml`; unknown fields, duplicate keys and unresolved refs fail | [src/agentic_engineering_system/records.py:1-9](../src/agentic_engineering_system/records.py#L1-L9) |
| `project.py` | `aes init` writes exactly `.aes/project.yaml` and `.aes/target.yaml`; `find_project_root` walks up to the nearest project | [src/agentic_engineering_system/project.py:1-28](../src/agentic_engineering_system/project.py#L1-L28) |
| `planning.py` | `aes plan prepare / validate / accept` over a target delta; accept edits the target in place and does not commit | [src/agentic_engineering_system/planning.py:1-45](../src/agentic_engineering_system/planning.py#L1-L45) |
| `topology.py` | every durable file under a governed root must be a planned artifact; orphans fail, unrealized and legacy are reported | [src/agentic_engineering_system/topology.py:1-21](../src/agentic_engineering_system/topology.py#L1-L21) |
| `characterize.py` | revision-bound characterization of HEAD under the governed roots and drift against the target | [src/agentic_engineering_system/characterize.py:1-24](../src/agentic_engineering_system/characterize.py#L1-L24) |
| `characterize_python.py` | Python AST facts (module, public symbols, signatures, import edges) without importing consumer code | [src/agentic_engineering_system/characterize_python.py:1-20](../src/agentic_engineering_system/characterize_python.py#L1-L20) |
| `evidence.py` | observations, Git-computed freshness (CURRENT, STALE, UNKNOWN, UNREACHABLE) and conjunction-only standing | [src/agentic_engineering_system/evidence.py:1-59](../src/agentic_engineering_system/evidence.py#L1-L59) |
| `reconcile.py` | composes characterization, evidence standing and accepted plans into current state and gaps; writes nothing | [src/agentic_engineering_system/reconcile.py:1-46](../src/agentic_engineering_system/reconcile.py#L1-L46) |
| `context.py` | `aes context <subject>`: the smallest complete packet with full text and an explicit not-included list | [src/agentic_engineering_system/context.py:1-26](../src/agentic_engineering_system/context.py#L1-L26) |
| `hooks.py` | `aes hooks install` writes `.githooks/pre-commit` running target validate and topology check | [src/agentic_engineering_system/hooks.py:1-30](../src/agentic_engineering_system/hooks.py#L1-L30) |
| `adopt.py` | `aes adopt` freezes an existing repository's governed files as a legacy baseline that only shrinks | [src/agentic_engineering_system/adopt.py:1-22](../src/agentic_engineering_system/adopt.py#L1-L22) |
| `trace_review.py` | thin binding to Company Planning's source-bound trace-review validator; missing configuration fails closed | [src/agentic_engineering_system/trace_review.py:1-4](../src/agentic_engineering_system/trace_review.py#L1-L4) |
| `repository_context/` | v0.1 Plan 001 resolver, retained with its console script and tests | [src/agentic_engineering_system/repository_context/__init__.py:1-6](../src/agentic_engineering_system/repository_context/__init__.py#L1-L6) [.aes/target.yaml:89-98](../.aes/target.yaml#L89-L98) |

- The planning protocol for writing proposals ships with the package as [planning_protocol.md](../src/agentic_engineering_system/planning_protocol.md). [.aes/target.yaml:505-513](../.aes/target.yaml#L505-L513)
- Since 2026-11-07, `evidence.assess` and `reconcile.reconcile` accept optional `required_dependency_paths`, so a consumer can require declared inputs before evidence counts. [src/agentic_engineering_system/evidence.py:18-24](../src/agentic_engineering_system/evidence.py#L18-L24) [docs/architecture/greenfield-v0.2/README.md:17](../docs/architecture/greenfield-v0.2/README.md#L17)
- Since 2026-11-08, characterization's Git reads disable repository hooks and fsmonitor commands. [src/agentic_engineering_system/characterize.py:3](../src/agentic_engineering_system/characterize.py#L3) [docs/architecture/greenfield-v0.2/README.md:21](../docs/architecture/greenfield-v0.2/README.md#L21)

## Other code in the repository

- `scripts/learning_loop/`: the feedback loop ([Feedback loop](feedback-loop.md)). [scripts/learning_loop/collect_feedback.py:2](../scripts/learning_loop/collect_feedback.py#L2)
- `scripts/rules/`: the rules register builder, legacy sort and agent-router contracts ([Policy and rules](policy-and-rules.md)). [scripts/rules/build_rules_page.py:2](../scripts/rules/build_rules_page.py#L2)
- `enforced_planning/` and `scripts/meta/`: the vendored Enforced Planning claims, sessions and worktree tooling, which `~/code2` replaced with `claude -w` worktrees. [docs/planning/SYSTEM_MODEL.md:101-103](../docs/planning/SYSTEM_MODEL.md#L101-L103)
- The Makefile's worktree, session and verification-batch targets were added by the Enforced Planning installer. [Makefile:1-2](../Makefile#L1-L2) [Makefile:76-86](../Makefile#L76-L86)

## Data flow (v0.2 engine)

- A target in `.aes/target.yaml` declares outcomes, normative items, criteria with evidence requirements, components, planned artifacts and verification subjects. [docs/planning/DOMAIN.md:14](../docs/planning/DOMAIN.md#L14)
- Proposals change the target only through `aes plan validate` and `accept`, which keep the accepted proposal under `.aes/plans/`. [src/agentic_engineering_system/planning.py:16-45](../src/agentic_engineering_system/planning.py#L16-L45)
- `aes evidence record` writes observations under `.aes/observations/`, bound to a commit and the paths and target entries the result depends on. [docs/planning/DOMAIN.md:29](../docs/planning/DOMAIN.md#L29)
- `aes status` and `aes reconcile` recompute standing, drift, orphans and gaps from target, HEAD and observations on every call and store nothing. [src/agentic_engineering_system/reconcile.py:22-24](../src/agentic_engineering_system/reconcile.py#L22-L24)

## Storage

- `.aes/project.yaml`, `.aes/target.yaml`, `.aes/plans/`, `.aes/observations/` and, after adoption, `.aes/legacy_baseline.json`. [docs/planning/SYSTEM_MODEL.md:74-85](../docs/planning/SYSTEM_MODEL.md#L74-L85)
- `.aes/commit_rule.yaml` remains but is read by no code since the commit rule's removal. [docs/planning/DOMAIN.md:49](../docs/planning/DOMAIN.md#L49)
- `datasets/learning-loop/` holds the labelled legacy learnings; the feedback loop's live outputs stay outside the repository in `$FEEDBACK_OUT`. [datasets/learning-loop/README.md:5-11](../datasets/learning-loop/README.md#L5-L11) [scripts/learning_loop/systemd/README.md:24-26](../scripts/learning_loop/systemd/README.md#L24-L26)
- `.agentic/repo.yaml` is the pilot repository protocol and declares the durable documents. [.agentic/repo.yaml:1-5](../.agentic/repo.yaml#L1-L5) [.agentic/repo.yaml:132-140](../.agentic/repo.yaml#L132-L140)

## Dependencies

- Runtime: Python 3.11 or newer, Pydantic 2.13.5, PyYAML 6.0.3 and ruamel.yaml. [pyproject.toml:9-14](../pyproject.toml#L9-L14)
- Development: pytest, mypy and pytest-xdist through the `[dev]` extra. [pyproject.toml:20-24](../pyproject.toml#L20-L24)
- The version comes from Git through setuptools-scm, with no fallback version. [pyproject.toml:33-36](../pyproject.toml#L33-L36)
- The feedback loop needs `llm_client`, OpenRouter (Jev), `gh`, Claude Code for the stronger model and the fix owner, and the Observation-to-Action metamodel checkout. [scripts/learning_loop/systemd/feedback-problems.service:18-23](../scripts/learning_loop/systemd/feedback-problems.service#L18-L23) [scripts/learning_loop/systemd/feedback-fix-owner.service:16-17](../scripts/learning_loop/systemd/feedback-fix-owner.service#L16-L17)
- Git hooks come from lefthook with a shared remote config in code2-workspace. [lefthook.yml:1-7](../lefthook.yml#L1-L7)

## What retires under decision 0009

- The `aes` command line and `.aes/target.yaml` retire one repository at a time; this repository's `.aes/` and `make aes` go when it is next changed. [docs/decisions/0009-aes-and-lockstep-fate.md:57-60](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L57-L60)
- The library stays while Lockstep imports it; Lockstep's AES path retires only after lifelike and Team-Brains move off `.aes/target.yaml`. [docs/decisions/0009-aes-and-lockstep-fate.md:68](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L68)
- The `aes hooks install` pre-commit hook does not run in this checkout since 2026-10-13, because `core.hooksPath` runs lefthook. [docs/planning/DOMAIN.md:41](../docs/planning/DOMAIN.md#L41)
- The feedback loop and `brain_fresh.py` do not retire. [docs/decisions/0009-aes-and-lockstep-fate.md:59-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L59-L61)

## Related pages

- [Requirements](requirements.md): what each module was required to do and its tests.
- [Open questions](open-questions.md): claims about this code not checked here.
