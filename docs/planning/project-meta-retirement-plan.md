---
description: Plan to move what is valuable in Project Meta into AES, then switch off and archive the rest, one slice at a time
status: proposed
---

# Project Meta retirement plan

**Source.** Brian, 2026-11-14: "project meta is a legacy system that is being retired in exchange for aes
canonical" and "i do want to start migrating what is valuable into aes at least as a plan and ablating and
archiving the legacy system"; on the feedback timers: "i dont want to turn this stuff on". This is a plan.
Nothing below has been done, switched off, moved or deleted. Every slice needs Brian's yes to start
(inferred by agent: the retirement itself is Brian's decision, the slice order is a working default).

**Measured on** Project Meta `f1e27c906` (last commit 2026-11-11; 116 commits since 2026-10-14), AES
canonical `e8967a320`, and the machine on 2026-11-14.

## What Project Meta is today

| Part | Size (files) | What it does |
| --- | --- | --- |
| `scripts/` | 695 | one-off and shared tools: markdown size cap, concern filing, notifications, project graph, plan status, repair executor |
| `docs/`, `wiki/`, `vision/`, `roadmap/`, `research_*` | 2,758 + 130 + more | planning and knowledge records |
| `learnings/` and `learnings.md` | 2,728 | logged lessons and friction |
| `policy/` | 161 | the policy registry (263 rows), friction clusters, audits |
| `enforced_planning/` | 109 | vendored claims, session and worktree machinery (claims were retired 2026-11-05) |
| `tests/` | 590 | tests of the above |
| `systemd/` and `hooks/` | units, 5 hooks | scheduled jobs and git hooks |

The tree is 946 MB, of which `.git` is 312 MB.

## Who still uses it (the part that decides the order)

**Scheduled jobs.** 30 systemd units mention the Project Meta path. Nine of their timers are enabled today:
`failed-unit-watch`, `feedback-collector`, `feedback-labels`, `graph-checkout-sync`, `plan-status-refresh`,
`project-graph-refresh`, `project-meta-policy-audit`, `skill-review`, `workspace-map-check`. The other
timers are off, including `feedback-effects` and `feedback-fix-owner` (Brian: leave them off).
13 of the 177 commands in `~/.local/bin` mention it.

**Other repositories calling its files** (counted as mentions of `project-meta/<path>` in each repository):

| Called file | Callers (repositories) | Job |
| --- | --- | --- |
| `scripts/md_file_cap.py` | workspace (50), company-planning (17), agent-skills (9), llm_client (6), ecosystem-ops (5), personal-vps (4), AES (10) | blocks oversized markdown files at commit |
| `scripts/operator_notify_router.py` | ecosystem-ops (7), workspace (3), personal-vps (2) | sends "attention" notices to Brian |
| `scripts/concern_issue.py` | workspace (5), agent-skills, company-planning, personal-vps | files, reopens and closes a concern as a GitHub issue |
| `scripts/project_graph_refresh.py`, `PROJECT_GRAPH.json` | workspace (6) | the list of all repositories (workspace capabilities row "Which projects exist") |
| `scripts/meta/audit_governed_repo.py` | workspace, llm_client, enforced-planning, data-contracts | checks a repository against the governance rules |
| `scripts/sync_plan_status.py`, `knowledge_router.py`, `repository_authority_provider.py`, `discover_boundaries.py` | ecosystem-ops | plan status, knowledge routing, authority and boundary discovery |
| `scripts/log_learning.py`, `log_policy_friction.py`, `recall_learnings.py` | agent-skills, AES | lesson and friction logging |
| `scripts/capability_catalog.yaml`, `capability_ownership_registry.yaml` | AES, ecosystem-ops, llm_client, company-planning | the capability catalogue (60 entries) and ownership registry (24) |
| `policy/registry.yaml` | AES (7), llm_client | the 263-row policy registry |
| `scripts/check_markdown_links.py`, `generate_wiki_routing_stub.py`, `check_ahead_of_origin.py` | llm_client, enforced-planning, data-contracts | small checks |

AES's own feedback loop calls two of them (`concern_issue.py`, `operator_notify_router.py`) from
`problems.py`, so even the AES loop cannot run without Project Meta today.

## What is worth keeping, and where it goes

Dispositions are proposals. **Port** = AES (or the named owner) gets a working copy and the callers switch.
**Harvest** = read and keep the ideas and evidence, not the machinery. **Archive** = move aside, nothing
deleted. **Drop** = nothing in it is used or worth reading (still archived, never deleted).

| Part | Proposed | Why |
| --- | --- | --- |
| `md_file_cap.py`, `check_markdown_links.py`, `generate_wiki_routing_stub.py`, `check_ahead_of_origin.py` | Port to AES shared checks | most-called files; callers are commit checks in 7 repositories |
| `concern_issue.py`, `operator_notify_router.py` | Port to AES | AES's own loop needs them; the concern register is GitHub issues (Q42) |
| Concern repair executor and five-gate verifier (`concern_repair_*.py`) | Port the design to AES `scripts/learning_loop/` | the only closure check that runs the repair's test before and after the fix; bound to the Project Meta repo today (Q42) |
| Project graph (`PROJECT_GRAPH.json`, refresh, checkout sync) | Port, owner to be chosen | live: two enabled timers and a workspace capability row; the one record of every repository |
| Capability catalogue and ownership registry | Port into the AES alias table and ecosystem-ops view | already under way (Decision 0014, Q36–Q38) |
| Policy registry (263 rows) | Harvest: keep the rows still in force (those in `core.md` and `rule-sources.md`), archive the rest | AES already holds `docs/rules/`; a full audit is not needed to retire |
| `learnings/`, `policy_friction.md`, `friction_clusters.yaml` | Archive; keep the friction clusters of open concerns | history, plus one open concern (#1883, now repaired) |
| `enforced_planning/` | Archive | claims retired 2026-11-05 |
| `docs/`, `wiki/`, `vision/`, `roadmap/`, `research_*` | Harvest by reading tranche (as Q39 did for the older AES), archive the rest | large, mostly dated planning records |
| `project-meta-policy-audit` and `skill-review` timers, plan-status refresh | Decide per job: port, replace with an existing tool, or switch off | enabled today; each needs an owner |
| `tests/` | Archive with the code they test; port tests with each ported tool | |

## How each slice runs

Every slice is a thin vertical cut that ends in something Brian can see, and merges when it works.

1. **Port.** Copy the tool into AES with its tests marked to a requirement, unchanged in behavior.
2. **Prove equal.** Run the Project Meta copy and the AES copy on the same real inputs (the same files, the same
   issue, the same repositories) and keep both outputs side by side. A difference is a finding, not a pass.
3. **Switch.** Point each caller at the AES copy, one repository at a time. Each caller runs its own check.
4. **Ablate.** In Project Meta, rename the old file (or switch off the timer) so any caller still using it fails
   loudly. Watch for one cycle of every scheduled job that touched it. The failure list is the list of callers
   missed in step 3. Undo is renaming it back.
5. **Archive.** Once ablation shows no caller, move the old file into the archive with a log line saying what
   was compared, what was not and how to undo it. Nothing is deleted.

## Order

| Slice | What Brian sees when it is done | Depends on |
| --- | --- | --- |
| 0. Freeze and ledger | One table of every caller and every enabled timer (the tables above, kept current) | nothing; no change to Project Meta |
| 0b. Docs triage | [One table of the 2,734 files under `docs/`](project-meta-docs-triage.md) with a reviewed proposal per folder (written; nothing moved) | 0 |
| 1. Markdown cap and small checks | The same commit checks pass in all 7 repositories with no `project-meta` path in them | 0 |
| 2. Concern filing and notices | AES's feedback loop runs with no Project Meta path; one real concern is filed, reopened and closed through AES | 0 |
| 3. Repair verifier design | The five-gate check runs inside AES on a repair of any AES-tracked concern | 2 |
| 4. Project graph | The repository list is produced and refreshed from AES (or its chosen owner); the two timers point there | 0 |
| 5. Catalogue and registries | One catalogue source; the alias table has no Project Meta reader | Decision 0014 work |
| 6. Policy rows and enabled timers | Each of the nine enabled timers is ported, replaced or switched off, with a reason | 1 to 5 |
| 7. Archive | Project Meta moved aside as a whole, with the log; the GitHub repository archived (read-only) | 1 to 6, Brian's yes |

Slices 1, 2 and 4 do not depend on each other and can run in parallel in separate worktrees.

## Rules for this plan

- Nothing is deleted. "Archive" means a move to `~/archive/project-meta/<timestamp>/` with a rationale log, and
  the Git history stays.
- Nothing is called safe to remove on a name or count match. Each removal states what was compared with the copy
  that stays and what was not.
- The feedback timers (`feedback-effects`, `feedback-fix-owner`) stay off unless Brian says otherwise.
- Archiving the GitHub repository and any outward step needs Brian's yes for that step.
- Each slice names its source revisions and limits, and claims no migration or retirement without evidence tied
  to a revision.

## Open points

- **Owner of the project graph.** It is a list of every repository, not a governance rule. It could stay in the
  workspace repository instead of AES. Brian's call; see Q44.
- **Which policy rows are still in force.** Starting point: the rows named in `core.md` and `rule-sources.md`.
  Not audited here.
- **Learnings and docs.** Whether any reading tranche is worth doing before archiving is not decided.
- **Unmeasured.** Cost and time of each slice are not estimated; no measurement exists yet.
