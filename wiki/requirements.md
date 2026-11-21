---
type: Requirements
title: Required behavior and its evidence
description: Route to current Lockstep behavior contracts and distinguish them from retained engine and feedback requirements
status: current
last_checked: 2026-11-13
---

# Required behavior and its evidence

The [AES goal](../docs/architecture/GOAL.md) explains the outcome. The
[system boundary](../docs/architecture/SYSTEM_BOUNDARY.md) records system clauses.
Current executable Lockstep requirements are OpenSpec files; their scenarios define
what a test should demonstrate. The following is navigation, not a second copy of
the requirements or a claim that their tests passed today.

## Current Lockstep contracts

| Concern | Owning specification | Implementation and proving examples |
| --- | --- | --- |
| Package and compatibility entry points | [Package](../openspec/specs/lockstep-package/spec.md) | [Package configuration](../pyproject.toml) |
| Installation and hooks | [Initialization](../openspec/specs/lockstep-init/spec.md) | [Installer](../src/lockstep/init_repo.py) |
| Planned files, purpose, requirements, tests and typed exports | [Plan format](../openspec/specs/lockstep-plan-format/spec.md) | [Layout and tests](../docs/architecture/LOCKSTEP.md#evidence-and-change-discipline) |
| Edit-time boundaries | [Guard](../openspec/specs/lockstep-guard/spec.md) | [Hook](../src/lockstep/hook.py) |
| Commit-time checks | [Checks](../openspec/specs/lockstep-checks/spec.md) | [Check implementation](../src/lockstep/checks/cli.py) |
| Plan-package validation | [Plan check](../openspec/specs/lockstep-plan-check/spec.md) | [Plan checker](../src/lockstep/plan_check.py) |
| Requirement copies and implementation coverage | [Projection and status](../openspec/specs/lockstep-projection/spec.md) | [Projector](../src/lockstep/checks/project.py), [status](../src/lockstep/checks/status.py) |
| Source-owned descriptions, interfaces and evidence values | [Declared document facts](../openspec/specs/lockstep-doc-facts/spec.md) | [Fact projector](../src/lockstep/doc_projection.py) |
| AES source-owned assessment and facts-only gate | [Documentation self-adoption](../openspec/specs/aes-documentation-projection/spec.md) | [Declarations](../lockstep.yaml), [native observation](../evidence/runs/projection-self-adoption-20261113.json) |

The [component contract](../docs/architecture/LOCKSTEP.md#current-mechanisms-and-their-limits)
explains how these mechanisms fit together and which intended guarantees remain
unverified. A specification's presence is not runtime evidence.

## Retained library and feedback contracts

- [Inert characterization](../openspec/specs/inert-characterization/spec.md) governs
  read-only repository inspection in the retained AES library.
- [Required evidence inputs](../openspec/specs/required-evidence-inputs/spec.md) governs
  qualification of evidence over declared dependencies.
- [Greenfield v0.2](../docs/architecture/greenfield-v0.2/README.md) preserves the
  accepted historical engine contract; it is not a replacement for the current goal.
- [Feedback and policy](../docs/architecture/FEEDBACK_AND_POLICY.md) identifies that
  path's native operator contract, implementation and dated observation limits.

## Where are observations and unresolved gaps?

- [Current state](../.project-brain/now.md) names the latest documentation and work context.
- [Retained acceptance observations](../docs/planning/runs/lockstep-acceptance/a1.json)
  are revision-bound records, with limits recorded in the
  [discussion ledger](open-questions.md).
- [Source-fact acceptance](../docs/planning/source-facts-acceptance.md) and its
  [bounded cold review](../docs/planning/cold-review.md) cover that particular slice.
- [Test commands](../tests/README.md) explain how to obtain fresh execution evidence.
  This documentation repair makes no new claim of full product test coverage.
- [Feedback loop notices](../openspec/specs/feedback-loop-notices/spec.md) governs the loop's concern filing and phone push, which no longer call Project Meta.
- [Learnings register frozen](../openspec/specs/learnings-register-frozen/spec.md) governs the collector's read-only use of the old learnings register, kept in a private repository.
- [Project graph config](../openspec/specs/project-graph-config/spec.md) governs where the graph and owner come from for `md_file_cap.py`: the person's own files, never a default owner.
- [Timer config](../openspec/specs/timer-config/spec.md) governs the job list and the installer that writes systemd timer units from it.
- [Failed unit watch](../openspec/specs/failed-unit-watch/spec.md) governs the 30-minute sweep that turns failed systemd user units into concern issues.
- [Machine manifest](../openspec/specs/machine-manifest/spec.md) governs the list of every systemd user unit with where its file comes from, and the check that names units a clean machine would lose.
- [Client manifest](../openspec/specs/client-manifest/spec.md) governs the list of every Claude Code and Codex setting on the machine with who owns it (agent-skills, the client at run time, or the manifest itself, which then holds the value), and the check that names settings that changed or that nobody records.
- [Hub page](../openspec/specs/hub-page/spec.md) governs the hub page: "Needs you" first, holding only what the owner must decide or do, each listed once (waiting issues and AES concerns for the owner); then broken services grouped by cause, records-request status notices as FYI, what changed since the last run, a link to each source page, and the inferred approvals as a footer count; issues are sorted by labels and fixed title prefixes from the settings and by each issue's concern-key marker, a source it cannot read is shown as not checked, and the page goes only to a private data branch.
- [Operator notify](../openspec/specs/operator-notify/spec.md) governs the operator notice router: every notice is recorded first, then routed by who must act (a concern, an ntfy push, or for Brian a toast, Telegram and a `waiting:brian` concern once per state); the concern repository comes from the private settings, and an open concern in the old Project Meta repository is updated there, not duplicated (ported from Project Meta).
- [Instruction audit](../openspec/specs/instruction-audit/spec.md) governs the two report-only audits of agent instruction files (size, placement, duplication, derivable inventories, and staleness from git history) that code2-workspace's nightly rule audit runs; the project graph comes from the private settings (ported from Project Meta).
- [Prune merged worktrees](../openspec/specs/prune-merged-worktrees/spec.md) governs removing a worktree only when the forge or its content proves the branch landed, keeping and naming every other one (ported from Project Meta; run weekly across every repository).
- [Ship](../openspec/specs/ship/spec.md) governs the merge command: run the repository's check, merge only the commit that passed, hold planning and plan-size rules, then sweep finished lanes; the planning and one-page-plan gates switch off from `.copier-answers.yml`, and a recorded hidden acceptance run must pass (ported from code2-workspace; the installed command runs this copy from `~/.hive-brain/aes`).
- [Lane sweep](../openspec/specs/lane-sweep/spec.md) governs removing finished worktrees and branches without losing local work, and fast-forwarding clean primary checkouts (ported from code2-workspace; the installed command and timer still run that copy).
- [Project graph taxonomy](../openspec/specs/project-graph-taxonomy/spec.md) governs the shape check of the project graph (the graph path is configuration).
- [Project activity snapshot](../openspec/specs/project-activity-snapshot/spec.md) governs the snapshot of each registered repository's last commit, branch and open pull requests.
- [Graph checkout refresh](../openspec/specs/graph-checkout-refresh/spec.md) governs the fast-forward of registered checkouts that never discards local work, and the concern for checkouts stuck far behind.
- [Workspace map check](../openspec/specs/workspace-map-check/spec.md) governs the daily clutter check of `~/code`, `~/projects`, `~/code2` and `~/archive`, filed as one keyed concern and one phone message per change.
- [Project graph sync](../openspec/specs/project-graph-sync/spec.md) governs registering GitHub repositories the graph does not yet record (homes, id prefixes, tags and sources are settings).
- [Project graph dependency scan](../openspec/specs/project-graph-dependency-scan/spec.md) governs filling `depends_on` from real imports, paths and commands; it only adds.
- [Project graph refresh](../openspec/specs/project-graph-refresh/spec.md) governs the daily job that refreshes the graph, lands it in the private settings repository and publishes the "My projects" page to its data branch.
- [Concern repair verifier](../openspec/specs/concern-repair-verifier/spec.md) governs the five-gate check that must pass before a repaired concern closes.
- [External idea intake](../openspec/specs/external-idea-intake/spec.md) governs the configurable subreddit watch list and the ranked digest command (Brian, 2026-11-16).
