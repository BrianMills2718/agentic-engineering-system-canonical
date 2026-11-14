---
title: Project Meta ledger
description: Measured list of what still calls Project Meta, its enabled timers and commands (slice 0 of the retirement plan)
---

# Project Meta ledger (slice 0)

Nothing in Project Meta was changed to make this. Produced by `scripts/project_meta_ledger.py` on 2026-11-14 at Project Meta f1e27c906; raw data in `evidence/runs/project-meta-ledger-20261114.json`.

Summary: 89 Project Meta files are named by code or configuration in other checkouts. 106 checkouts name them, which are 73 distinct repositories once checkouts sharing one origin (lanes, copies) are counted once. 46 systemd units mention Project Meta; 21 are timers and 10 are enabled. 15 commands in `~/.local/bin` mention it.

## Enabled timers

| Timer | State |
| --- | --- |
| brent-us-sources.timer | enabled |
| failed-unit-watch.timer | enabled |
| feedback-collector.timer | enabled |
| feedback-labels.timer | enabled |
| graph-checkout-sync.timer | enabled |
| plan-status-refresh.timer | enabled |
| project-graph-refresh.timer | enabled |
| project-meta-policy-audit.timer | enabled |
| skill-review.timer | enabled |
| workspace-map-check.timer | enabled |

Disabled timers that mention Project Meta: aes-gate-watch.timer, attention-page.timer, canonical-sync.timer, ecosystem-feedback-watchdog.timer, ecosystem-feedback-worker.timer, ecosystem-inbox.timer, ecosystem-ops-daily.timer, feedback-effects.timer, feedback-fix-owner.timer, feedback-problems.timer, project-meta-lifecycle-sweep.timer.

## Most-named Project Meta files (distinct repositories, code and configuration only)

| File | Distinct repositories | Examples |
| --- | ---: | --- |
| `scripts/md_file_cap.py` | 43 | Team-Brains-lanes, agent-skills, agentic-engineering-system-canonical, brent-chatgpt, claim-extraction … |
| `scripts/rollout_canonical_checkout_guard.py` | 22 | agent-skills, agent_ecology2, agent_ecology3, agent_ontology, agentic_scaffolding … |
| `PROJECT_GRAPH.json` | 19 | 2nd-brain-plan-repo, agentic-engineering-system, company-planning, ecosystem-mega, ecosystem-ops … |
| `scripts/concern_issue.py` | 12 | agent-skills, company-planning, ecosystem-ops, inquiry-graph, inside-success … |
| `scripts/check_wiki_manifest.py` | 8 | ecosystem-mega, graph-ontology-extraction, greer, inquiry-graph, inside-success … |
| `policy/registry.yaml` | 7 | agent-skills, agentic-engineering-system-canonical, ecosystem-mega, inquiry-graph, inside-success … |
| `scripts/capability_ownership_registry.yaml` | 6 | company-planning, ecosystem-mega, ecosystem-ops, inquiry-graph, inside-success … |
| `scripts/meta/check_coordination_claims.py` | 5 | ecosystem-ops, inquiry-graph, personal-file-infra, qc, workspace-harness-config |
| `scripts/notify_operator.py` | 5 | brent-chatgpt, ecosystem-ops, inquiry-graph, personal-root, personal-wiki |
| `scripts/log_learning.py` | 4 | agent-skills, agentic-engineering-system-canonical, ecosystem-mega, inquiry-graph |
| `scripts/operator_notify_router.py` | 4 | ecosystem-mega, ecosystem-ops, personal-vps, workspace |
| `policy/proposals/2026-08-18-planned-phase-boundary-context-checkpoint.yaml` | 3 | inquiry-graph, inside-success, second-brain-mega |
| `policy/wiki/AGENT_GUIDE.md` | 3 | inside-success, second-brain-mega, vision |
| `policy/wiki/SKILL_INDEX.md` | 3 | inside-success, second-brain-mega, vision |
| `scripts/authority_surfaces.yaml` | 3 | inquiry-graph, inside-success, second-brain-mega |
| `scripts/check_agent_surface_sync.py` | 3 | claude-team-infra, ecosystem-mega, inquiry-graph |
| `scripts/generate_wiki_routing_stub.py` | 3 | ecosystem-mega, inquiry-graph, second-brain-mega |
| `scripts/meta/render_agents_md.py` | 3 | agent-skills, claude-team-infra, ecosystem-mega |
| `scripts/refresh_canonical_checkouts.py` | 3 | ecosystem-mega, inquiry-graph, workspace |
| `policy/friction_clusters.yaml` | 2 | ecosystem-mega, inquiry-graph |

## Commands in `~/.local/bin` that mention it

`c-drive-guard`, `disk-maintenance`, `disk-maintenance-weekly`, `flyctl`, `free-disk-space`, `jev-gate-compliance-guard`, `jev-gate-hook`, `jev-gate-hook.bak-20261026-hook-audit`, `jev-gate-hook.bak-20261107`, `jev-gate-hook.prev`, `jev-gate-trace-review-guard`, `lane-sweep`, `proj`, `rr-public-export`, `ruff`

## Limits

- A mention is the text `project-meta/<path>` in a code or configuration file (not `.md`), read once per file; it is not proof the file runs. Files over 2 MB and folders named archive, data and runs were skipped.
- Timers count as related when the timer or its same-named service mentions the path. The plan's earlier count was nine enabled timers; this run finds ten, adding `brent-us-sources`, which the earlier count missed.
- Commands match the name `project-meta` anywhere in the file, including a comment or a directory listing, so some of the 15 do not call it.
- Systemd units were read from `~/.config/systemd/user` and the workspace `systemd` folder only.
