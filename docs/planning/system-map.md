---
description: Every code unit in AES canonical on one map, grouped by the AES part it belongs to, with what calls what
---

# AES canonical: system map

Question answered: which code units make up this repository, which AES part does each belong to, and what calls what?

Every unit the planning package lists in `system_model.units` is named here. Read at origin/main `c44c408`
(2026-11-11). The one-tool build (slice 1) adds the `lockstep` package to this map; it is not here yet.
Back to the [system model](SYSTEM_MODEL.md).

```mermaid
flowchart LR
  subgraph FB[Feedback loop: runs nightly from ~/.hive-brain/aes]
    systemd[systemd: timer and service units]
    collect_feedback[collect_feedback: transcripts to filed reports]
    transcripts[transcripts: read Claude and Codex turns]
    feedback_log[feedback_log: write one issue per report]
    label_items[label_items: failure-mode family labels]
    subagents[subagents: child outcomes and parent checks]
    records_fb[records: feedback-report.v1 records]
    evidence_fb[evidence: count independent observations]
    problems[problems: weekly analysis, off]
    effects[effects: enforcement receipts, off]
    fix_owner[fix_owner: weekly fix owner, off]
    licences[licences: licences for proposed fixes]
    policies[policies: is each rule enforced and observed]
    relation_check[relation_check: S2 measurement]
    question_set_v2[question_set_v2: label questions]
  end
  subgraph PL[Policy layer]
    build_rules_page[build_rules_page: writes docs/rules/RULES.md]
    agent_router[agent_router: profile and handoff contracts]
    sort_legacy[sort_legacy: sort project-meta's legacy rules]
  end
  subgraph LIB[Retained AES library: Lockstep imports it; the aes command line retires]
    cli[cli: the aes command]
    planning[planning: plan prepare, validate, accept]
    planning_protocol[planning_protocol: planning text]
    records[records: target and project records]
    evidence[evidence: observations, freshness, standing]
    reconcile[reconcile: state and gaps]
    characterize[characterize: revision-bound file facts]
    characterize_python[characterize_python: Python AST provider]
    topology[topology: governed-root check]
    context[context: working-context packets]
    adopt[adopt: legacy baseline]
    project[project: aes init]
    hooks[hooks: pre-commit hook writer, not installed here]
    trace_review[trace_review: Company Planning review binding]
    repository_context[repository_context: v0.1 Plan 001 resolver]
  end
  subgraph OTHER[Project brain and retired coordination]
    brain_fresh[brain_fresh: is the project brain stale]
    meta[meta: scripts/meta coordination and session scripts]
    enforced_planning[enforced_planning: vendored claims machinery]
    artifact_creation[artifact_creation]
    audit_dead_code[audit_dead_code]
    check_dead_code[check_dead_code]
    check_doc_coupling[check_doc_coupling]
    check_markdown_links[check_markdown_links]
    check_push_safety[check_push_safety]
    check_reachability[check_reachability]
    check_required_reading[check_required_reading]
    coordination_hook[coordination_hook]
    coordination_inbox[coordination_inbox]
    coordination_messages[coordination_messages]
    coordination_operator_status[coordination_operator_status]
    hook_receipts[hook_receipts]
    refresh_prewrite_claim_projection[refresh_prewrite_claim_projection]
    repo_stats_block[repo_stats_block]
    sync_plan_status[sync_plan_status]
  end
  systemd --> collect_feedback
  systemd --> label_items
  systemd -.-> problems
  systemd -.-> effects
  systemd -.-> fix_owner
  collect_feedback --> transcripts
  collect_feedback --> feedback_log
  collect_feedback --> subagents
  feedback_log --> records_fb
  problems --> evidence_fb
  problems --> licences
  effects --> policies
  policies --> build_rules_page
  label_items --> question_set_v2
  relation_check --> records_fb
  sort_legacy --> build_rules_page
  cli --> planning --> records
  planning --> planning_protocol
  cli --> evidence
  cli --> reconcile --> characterize --> characterize_python
  reconcile --> evidence
  cli --> topology
  cli --> context
  cli --> adopt
  cli --> project
  cli --> hooks
  evidence --> trace_review
  meta --> enforced_planning
  coordination_hook --> enforced_planning
```

`records_fb` and `evidence_fb` are `scripts/learning_loop/records.py` and `evidence.py`, drawn apart from the
library's `records` and `evidence`. The unlabelled units in the last group are the claims-era scripts at
`scripts/*.py`; `~/code2` replaced claims with worktrees, and nothing in the one-tool plan uses them (open question Q10).
Dotted arrows are jobs whose timers are off (open question Q21).
