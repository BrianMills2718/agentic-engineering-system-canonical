---
type: Topic
title: Lockstep
description: Navigate Lockstep purpose, planned behavioral structure, source-local context, implementation and evidence
status: current
last_checked: 2026-11-17
---

# Lockstep

Start with the [component architecture](../docs/architecture/LOCKSTEP.md): why
Lockstep exists, the planned behavioral units and typed seams, what moves down
into code and up into evidence, source ownership, and current implementation
limits. This wiki page is navigation; the architecture, specifications and recorded
observations retain their own roles.

Lockstep helps autonomous coding agents implement intended behavior effectively.
Its planning approach names the file structure and behavioral contracts before
implementation, linking requirements, success criteria, tests, files and symbols.
The planner supplies that decomposition; Lockstep represents, scaffolds, projects
and checks it. A module list by itself is not the whole intended plan.

Code: this repository, package `lockstep` in [src/lockstep/](../src/lockstep/__init__.py) (`pcw` kept as an alias package), spec [lockstep-package](../openspec/specs/lockstep-package/spec.md). The old repository [BrianMills2718/lockstep](https://github.com/BrianMills2718/lockstep) is kept as history.

## What it is

- Lockstep is a part of AES: it puts full normative context at an edit, projects plan changes into code and is intended to carry code-side normative changes back through explicit plan changes (the retained implementation is a legacy draft-and-accept route), links planned structure to typed symbols and checks, and renders evidence-bound status ([docs/architecture/SYSTEM_BOUNDARY.md:29](../docs/architecture/SYSTEM_BOUNDARY.md#L29)).
- Brian, 2026-11-06: "lockstep is meant to be part of aes canonical" ([docs/architecture/SYSTEM_BOUNDARY.md:33](../docs/architecture/SYSTEM_BOUNDARY.md#L33)).
- One config file, `lockstep.yaml`; commands `lockstep layout`, `lockstep check` (the whole-tree plan check, or `check <name>` for one commit check), `lockstep plan check`, `lockstep status`, `lockstep show`, `lockstep accept write|check` and `lockstep run-plan` (hidden acceptance tests and a departure report for one OpenSpec plan, [spec](../openspec/specs/plan-run/spec.md)), `lockstep check prior-art` ([spec](../openspec/specs/prior-art-check/spec.md)), the merge command `ship` ([spec](../openspec/specs/ship/spec.md)), and the edit hook `lockstep-hook` ([design](../proposals/one-planning-tool/DESIGN.md)).

## Who uses it

- lifelike, pinned to this repository, where its hook blocks off-plan edits under `PCW_MODE=block` ([lifelike#5](https://github.com/BrianMills2718/lifelike/pull/5)).
- Team-Brains' Project Brain pull request runner, from a vendored wheel of this repository ([Team-Brains#1183](https://github.com/Inside-Success/Team-Brains/pull/1183)); installed on the server 2026-11-12.
- New code2 repositories: code2-template installs it in place of code2check ([code2-template#29](https://github.com/BrianMills2718/code2-template/pull/29)); existing ones switch when next changed.

## Delivered mechanisms and recorded adoption (2026-11-12)

- Brian approved one tool, part of AES canonical, configurable and portable/shareable (2026-11-11, "i approve single tool desing re d4"), after withdrawing a wind-down the same day ("ok i didnt mean to approve abandoingn lockstep"); history in code2-workspace [decision 0009](https://github.com/BrianMills2718/code2-workspace/blob/main/docs/decisions/0009-aes-and-lockstep-fate.md).
- The six slices of the [design](../proposals/one-planning-tool/DESIGN.md) are merged:
  1. The code moved here ([#831](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/831)).
  2. The plan is OpenSpec plus `layout:` rows ([#835](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/835), [spec](../openspec/specs/lockstep-plan-format/spec.md)), with `.aes/target.yaml` still read.
  3. The guard uses code2check's shell-target parser ([#834](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/834), [spec](../openspec/specs/lockstep-guard/spec.md)).
  4. The commit checks ([#833](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/833), [spec](../openspec/specs/lockstep-checks/spec.md)).
  5. The plan check ([#832](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/832), [spec](../openspec/specs/lockstep-plan-check/spec.md)).
  6. Projection, status, show and the pytest plugin ([#836](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/836), [spec](../openspec/specs/lockstep-projection/spec.md)), then the users switch (above).
- 2026-11-20: `ship` and the lane sweep moved into `src/lockstep/` and install with the package (`uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical ship`); the prior-art check moved here from code2-workspace as `lockstep check prior-art`, and `ship` runs this copy, so neither needs a private checkout ([change](../openspec/changes/archive/2026-11-20-portable-ship/proposal.md)). `scripts/ship.py` and `scripts/lane_sweep.py` remain as shims.
- 2026-11-20: `lockstep accept write <change>` has a separate headless Claude or Codex session write pytest files from the plan into `${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/<run id>/accept/`, outside every worktree, and runs them once before implementation; `lockstep accept check <change>`, after the implementer's last commit, copies them in, runs them, removes them, runs `make check` and reports files changed outside `tasks.md` and unticked tasks; `lockstep run-plan <change> --agent claude|codex` does both around one headless implementer session and prints the `ship` command without merging ([change](../openspec/changes/archive/2026-11-20-run-plan/proposal.md), [spec](../openspec/specs/plan-run/spec.md)). Hiding is by placement plus a `peek_reads` count from the implementer's transcript, not a sandbox. Minimal core steps 2 and 4 ([minimal-core-2026-11-20.md](../docs/planning/minimal-core-2026-11-20.md)).
- 2026-11-17: `lockstep check changed --base <rev>` lists each requirement whose statement or scenario text differs from the base revision (whitespace runs count as one space), with its code, its tests labelled changed/unchanged/new, and the plan that names it; it fails on `unplanned` (no plan added or edited since the base names it) and `no-scenario-changed` (statement reworded, no scenario changed, no `Wording-only:` line). `test-first` now needs one failing-on-base test per changed scenario; `status` shows `changed, not archived` for text an active change rewords ([change](../openspec/changes/archive/2026-11-17-lockstep-changed-requirements/proposal.md), [spec](../openspec/specs/lockstep-checks/spec.md)). It does not find hand-typed copies of requirement text in documents, and it takes a `Wording-only:` declaration as typed, without checking it. No test is run by `changed`; it reads the base with `git archive` and leaves the working tree alone.
- 2026-11-17: `changed` and `test-first` compare with the merge base of `--base` and HEAD (where the branch started), so merges into the base branch after the branch started are not counted; a test skipped on the base source is not a failing test ([change](../openspec/changes/archive/2026-11-17-lockstep-base-is-branch-start/proposal.md)). Not done by these checks: nothing is listed for a requirement whose text did not change, and a `Wording-only:` line is taken on trust (it is printed and counted).
- 2026-11-17: a document can mark a passage it copies from a requirement: `<!-- lockstep quote: <requirement id> -->the passage<!-- /lockstep quote -->` (the markers are HTML comments, so a rendered page does not show them; the passage may span lines or sit inside a sentence or table cell). `lockstep check trace` reads every marked quote in Markdown tracked by git outside `openspec/` and fails with `stale-quote` when the passage, whitespace runs as one space, is not in the text of that requirement or one of its scenarios (specs or an active change's delta), `unknown` for an ID no spec defines, and `unclosed-quote` <!-- lockstep quote: lockstep-checks/trace-a-marked-quote-matches-its-requirement -->when a start marker has no end marker after it in the same file<!-- /lockstep quote -->. `lockstep check changed` lists, under each requirement it lists, the documents that quote it as `<path>:<line>` labelled `current` or `stale` ([change](../openspec/changes/archive/2026-11-17-lockstep-document-quotes/proposal.md), code [quotes.py](../src/lockstep/checks/quotes.py)). A copy that is not marked is not checked: finding unmarked copies of a requirement's wording needs a reader, not this check. The check verifies the passage; it never rewrites it.
- 2026-11-18: every plan that names a requirement `lockstep check changed` lists must state its size in one line outside a fenced code block, `Plan size: small` or `Plan size: full` (in an OpenSpec change's `proposal.md` or a `docs/plans/` page). The check fails with `no-plan-size`, naming the file to add the line to, when no plan naming the requirement states one, and with `no-planning-package` when the size is `full` and no plan naming it has a `Planning package: <path>` line naming a file that exists. Small in one plan and full in another counts as full. Each requirement's block prints its `size`, and the count line adds `small`, `full`, `no_plan_size` and `no_planning_package` ([change](../openspec/changes/archive/2026-11-18-lockstep-plan-size/proposal.md); Brian's Decision 7A, 2026-11-17). The size is the author's statement: the check does not judge whether a change deserves it, and it checks only that the package file exists, not that the package is valid.
- Two projectors remain inside the one package. The cog one fills layout and AES-plan files. The code2check one fills `Implements:` docstrings in code2 repositories. Merging them is not yet planned.

## Changes made in this repository for Lockstep

- 2026-11-07: `evidence.assess` and `reconcile.reconcile` accept optional `required_dependency_paths`, so Lockstep can require declared inputs before evidence counts ([.project-brain/now.md:7](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/.project-brain/now.md#L7)); spec: [required-evidence-inputs](../openspec/specs/required-evidence-inputs/spec.md).
- 2026-11-08: characterization and producer-identity Git readers disable repository hooks and fsmonitor commands ([.project-brain/now.md:3](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/.project-brain/now.md#L3)); spec: [inert-characterization](../openspec/specs/inert-characterization/spec.md).
- Neither change restarts the retired self-governance program ([.project-brain/now.md:5](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/b0d4cbd174e78c075eed5248beb00509d636d0b0/.project-brain/now.md#L5)).

## Boundaries and open integration questions

- Current code still carries legacy AES plan/proposal assumptions; the [implementation table](../docs/architecture/LOCKSTEP.md#current-mechanisms-and-their-limits) distinguishes those from the OpenSpec/layout route.
- No blanket claim is made that every native tool call is guarded, that every docstring carries synchronized evidence status, or that PostToolUse performs every plan projection. It refreshes declared source-owned facts.
- Editing a supported normative cog copy can [draft an accepted-plan change](../src/lockstep/docstring_up.py); the legacy draft-and-accept route is not established as a general OpenSpec round trip.
- Whether Company Planning's adoption gate should call `lockstep plan check` rather than its own copy (design, "What this does not decide"); slice 5 kept both, with the same checks.

## Source-local document projections

Descriptions, lifecycle fields, Python interfaces and native evidence values
can be declared once and projected into marked wiki/document sections. See the
[declaration and installed hook/check path](../README.md#project-source-owned-facts)
and the [source-local facts specification](../openspec/specs/lockstep-doc-facts/spec.md).
These generated copies do not certify arbitrary prose or consumer rollout.

## Read the mechanisms and their evidence

| Question | Source |
| --- | --- |
| How are files and behavior planned before implementation? | [Plan format](../openspec/specs/lockstep-plan-format/spec.md), [layout adapter](../src/lockstep/layout_plan.py), [scaffold](../src/lockstep/scaffold.py) |
| How does normative text move down and draft changes move up? | [Cog renderer](../src/lockstep/cogtext.py), [docstring drafts](../src/lockstep/docstring_up.py) |
| What is checked before committing? | [Whole-tree check](../src/lockstep/check.py), [named commit checks](../openspec/specs/lockstep-checks/spec.md) |
| What does current status mean? | [Status implementation](../src/lockstep/checks/status.py), [projection contract](../openspec/specs/lockstep-projection/spec.md) |
| Which examples exercise these mechanisms? | [Layout tests](../tests/lockstep/test_lockstep_layout_plan.py), [draft tests](../tests/lockstep/test_lockstep_docstring_up.py), [status tests](../tests/lockstep/checks/test_lockstep_check_status.py) |

The [retained acceptance page](../proposals/planning-package/review-page/lockstep-acceptance.html)
is a bounded review record. Its conclusions do not replace fresh checks of installed
hooks or establish universal consumer rollout.

## Worked example on Lockstep itself

The [projection-component assessment](../docs/architecture/LOCKSTEP.md#worked-assessment-the-projection-component)
shows an actual authored current/gap/plan narrative carried by the existing
projector into two documents. It includes the ownership map, configuration,
six-step replay, measured evidence and gap-backed next plan. The
[retained run](../evidence/runs/projection-worked-20261113.json) exposes the complete
CLI observations. That earlier disposable replay did not observe native-host
execution. The later [AES self-adoption observation](../docs/architecture/LOCKSTEP.md#aes-self-adoption-observation)
records the bounded installed Claude path.

## Source-owned component assessment

The following block is generated from the implementing module. Edit its authored
assessment there; measured evidence and the earlier worked replay retain their
own observation boundaries.

<!-- lockstep facts: projection-component-wiki -->

Generated from [src/lockstep/doc_projection.py](../src/lockstep/doc_projection.py); edit the source, not this block.

| Field | Value |
| --- | --- |
| docstring | Project declared source-local facts into Markdown; never execute source or repository code.<br><br>Implements: lockstep-doc-facts/declared-source-facts-have-one-authority,<br>    lockstep-doc-facts/invalid-input-is-not-a-pass,<br>    lockstep-doc-facts/installed-edit-and-merge-paths-maintain-facts,<br>    lockstep-doc-facts/declared-record-arrays-project-as-rows<br><br>Requirement text (generated):<br>    lockstep-doc-facts/declared-source-facts-have-one-authority: `lockstep check project` SHALL<br>        generate Markdown fact blocks declared by `projections` in `lockstep.yaml`, each with id,<br>        source, target and fields, with an optional Python symbol. It SHALL read Markdown YAML front<br>        matter, JSON/YAML mapping fields and Python AST descriptions and signatures without<br>        importing or executing source. `--check` SHALL report stale target paths and exit 1 without<br>        writing. Generation SHALL preserve unrelated target content, include a relative source link<br>        (or an HTTP(S) source_base_url link when configured), escape HTML and table delimiters in<br>        projected scalar values, and remain idempotent. Consumers with no recognized OpenSpec<br>        requirement text SHALL project only declared facts, without creating an empty coverage page<br>        or rewriting historical plans.<br>    lockstep-doc-facts/invalid-input-is-not-a-pass: Projection SHALL reject missing sources or<br>        fields, invalid or duplicate marker pairs and paths escaping the repository, including<br>        symlinks. It SHALL validate all declared fact projections before any projection write and<br>        report invalid input with exit 2. Targets SHALL NOT also be sources.<br>    lockstep-doc-facts/installed-edit-and-merge-paths-maintain-facts: `lockstep refresh` SHALL<br>        refresh only declared source-local fact blocks without regenerating requirement docstrings<br>        or coverage. `lockstep init` SHALL install it as a PostToolUse hook for Claude Code and<br>        Codex while preserving existing hooks. It SHALL include `lockstep check project --check` in<br>        the pre-commit command so edits bypassing hooks are still checked. Refresh SHALL append one<br>        trace per run to a daily projection log with source/target hashes and rewritten paths. No<br>        declarations SHALL be a no-op.<br>    lockstep-doc-facts/declared-record-arrays-project-as-rows: A projection MAY declare `items` as<br>        the name of a top-level JSON or YAML array. Its `fields` SHALL include `id` and identify<br>        scalar fields in each record. The projector SHALL render one escaped Markdown table row per<br>        source record in source order and preserve the source link and markers. Each record SHALL<br>        have a distinct nonempty string `id` and each selected field SHALL be a non-null scalar.<br>        Missing arrays, invalid records, missing fields and duplicate IDs SHALL fail before any<br>        target write. The check and installed refresh paths SHALL apply the same validation and<br>        freshness rules as ordinary projections; refresh traces SHALL record selected array facts<br>        and source identity.<br><br><br>Current assessment (agent-authored):<br>    Static source extraction, declared target fan-out, refresh traces and read-only<br>    comparison are implemented. AES declares this module as the source for its<br>    architecture and wiki assessment blocks. This narrative is an assessment,<br>    not a substitute for measured test or native-host evidence.<br><br>Gap G-NATIVE:<br>    Closed for the retained API-authenticated Claude path: one native Edit<br>    invoked the installed hook and refreshed both targets. Codex host execution<br>    and blanket default-session loading remain unobserved.<br><br>Plan P-NATIVE (addresses G-NATIVE):<br>    Completed for the retained Claude path: host transcript and trace identify<br>    one source Edit and both target writes; bypass refusal and recovery passed.<br><br>Gap G-CONCISE:<br>    The first adoption projects the full docstring; a compact wiki narrative and<br>    typed gap/plan relationship validation remain separate improvements.<br><br>Evidence:<br>    See evidence/runs/projection-worked-20261113.json for the earlier disposable<br>    CLI example. See evidence/runs/projection-self-adoption-20261113.json and<br>    evidence/runs/projection-native-20261113.jsonl for the bounded native run.<br><br>Native edit marker: observed-host-edit |

<!-- /lockstep facts: projection-component-wiki -->
