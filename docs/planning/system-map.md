---
description: Every code unit in AES canonical on one map, grouped by the AES part it belongs to, with what calls what
---

# AES canonical: system map

Question answered: which code units make up this repository, which AES part does each belong to, and what calls what?

Every unit the planning package lists in `system_model.units` is named here. Read at origin/main `0395758`
(2026-11-12), then reduced on 2026-11-12 by the cleanup that retired the claims-era scripts, `repository_context` and the agent router (docs/retired/2026-11-12.md). The `lockstep` package moved in on 2026-11-11 and 2026-11-12 (PRs #831 to #837), so Lockstep is a group
on this map; `src/pcw/__init__.py:1` is its old-name alias.
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
    notify[notify: Telegram message, no Project Meta]
    timers[timers: job list to systemd units]
    failed_unit_watch[failed_unit_watch: failed units to concern issues]
    machine_manifest[machine_manifest: every unit, where its file comes from, repository copies of local-only files]
    client_manifest[client_manifest: Claude and Codex settings, who owns each, values of the unowned ones]
    hub_page[hub_page: the hub page, Needs you on top, pushed to a private data branch]
    graph_taxonomy[check_project_graph_taxonomy: shape of the project graph]
    project_activity[build_project_activity: last commit per registered repo]
    refresh_checkouts[refresh_canonical_checkouts: fast-forward registered checkouts]
    workspace_map_alert[workspace_map_alert: daily workspace check to one concern and one message]
    workspace_map[workspace_map: clutter check of ~/code, ~/projects, ~/code2]
    graph_refresh[project_graph_refresh: daily graph and page refresh]
    graph_sync[project_graph_sync: register new GitHub repositories]
    dependency_scan[check_capability_consumption: fill depends_on from real use]
    archive_map[archive_map: every ~/archive entry explained]
    repair_verifier[concern_repair_feedback: five-gate repair check]
    repair_contract[concern_repair_contract: report and record shapes]
    repair_agents[concern_repair_agents: reviewer client choice]
    alert[alert: loop failures as concerns]
    licences[licences: licences for proposed fixes]
    external_ideas[external_ideas: subreddit digest, on request]
    external_judge[external_judge: model decides how much to read]
    policies[policies: is each rule in agents/ documented and observed]
    relation_check[relation_check: S2 measurement]
    question_set_v2[question_set_v2: label questions]
  end
  subgraph PL[Policy layer]
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
  end
  subgraph LS[Lockstep: package src/lockstep, the one planning-and-checking tool]
    ls_cli[check: the lockstep command, whole-tree plan check]
    ls_hook[hook: the edit guard]
    shell_targets[shell_targets: which paths a shell command writes]
    stale_edit[stale_edit: refuse an edit while the docstring copy is stale]
    unplanned_files[unplanned_files: files the plan does not name]
    plan_run[plan_run: hidden acceptance tests, departure report, run-plan]
    unplanned_symbols[unplanned_symbols: symbols the plan does not declare]
    symbol_gate[symbol_gate: symbols a change adds]
    layout_plan[layout_plan: OpenSpec plus layout rows]
    openspec_text[openspec_text: read a requirement's text]
    decisions[decisions: read decision records' Governs and status lines]
    side_file[side_file: read lockstep.yaml]
    aes_bridge[aes_bridge: read the AES plan]
    scaffold[scaffold: create the planned files]
    init_repo[init_repo: lockstep init writes lockstep.yaml and the hook entries]
    doc_projection[doc_projection: declared source facts to document blocks and freshness checks]
    cogtext[cogtext: render plan text into docstrings]
    parent_text[parent_text: parent requirement text]
    signature_text[signature_text: typed signatures]
    docstring_up[docstring_up: docstring edit to plan change]
    plan_edit[plan_edit: items a plan-file edit changes]
    plan_to_code[plan_to_code: where code differs from the plan]
    change_list[change_list: files and symbols a plan change touches]
    change_log[change_log: append-only change log]
    requirement_status[requirement_status: status per requirement]
    wiki[wiki: pages from plan and evidence]
    wiki_reach[wiki_reach: every page within two links]
    action_check[action_check: judge a proposed action]
    behavior_check[behavior_check: behavior has one source file]
    criterion_checks[criterion_checks: criterion names its check]
    declared_reason[declared_reason: file declares a reason]
    linked_tests[linked_tests: tests and criteria link both ways]
    plan_check[plan_check: lockstep plan check]
    citation_anchor[citation_anchor: a citation that names its text]
    checks[checks: commit checks trace arch test_first sources docmeta, status, show, project, pytest plugin]
    pcw[pcw: alias of lockstep]
  end
  subgraph OTHER[Project brain]
    brain_fresh[brain_fresh: is the project brain stale]
  end
  subgraph MERGE[Merge path: src/lockstep since 2026-11-20, installed as the ship command; scripts/ keeps shims]
    ship[ship: run the check, merge only the checked commit]
    plan_content[plan_content: the plan-content question for the push hook]
    lane_sweep[lane_sweep: remove finished lanes, fast-forward clean checkouts]
    prior_art[prior_art: refuse an OpenSpec change with no decided prior-art record]
  end
  systemd --> collect_feedback
  systemd --> label_items
  systemd -.-> problems
  systemd -.-> effects
  systemd -.-> fix_owner
  problems -.-> notify
  problems -.-> alert
  systemd -.-> timers
  systemd --> failed_unit_watch
  ship --> lane_sweep
  ship --> prior_art
  ls_cli --> prior_art
  plan_content --> ship
  systemd -.-> lane_sweep
  systemd -.-> machine_manifest
  systemd -.-> project_activity
  systemd -.-> refresh_checkouts
  systemd -.-> workspace_map_alert
  workspace_map_alert --> workspace_map
  workspace_map --> archive_map
  workspace_map --> dependency_scan
  systemd -.-> graph_refresh
  graph_refresh --> graph_sync
  graph_refresh --> dependency_scan
  graph_refresh --> graph_taxonomy
  graph_refresh --> project_activity
  graph_sync --> workspace_map
  workspace_map_alert --> notify
  repair_verifier --> repair_contract
  repair_verifier -.-> repair_agents
  collect_feedback --> transcripts
  collect_feedback --> feedback_log
  collect_feedback --> subagents
  feedback_log --> records_fb
  problems --> evidence_fb
  problems --> licences
  effects --> policies
  label_items --> question_set_v2
  relation_check --> records_fb
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
  pcw --> ls_cli
  pcw --> ls_hook
  ls_cli --> layout_plan --> openspec_text
  ls_cli --> aes_bridge
  ls_cli --> declared_reason
  ls_cli --> unplanned_files
  ls_cli --> plan_run
  ls_cli --> symbol_gate
  ls_cli --> init_repo
  ls_cli --> doc_projection
  ls_cli --> scaffold
  ls_cli --> plan_check
  plan_check --> citation_anchor
  ls_cli --> checks
  checks --> doc_projection
  doc_projection --> ls_hook
  ls_cli --> cogtext
  ls_hook --> decisions
  ls_hook --> shell_targets
  ls_hook --> stale_edit
  ls_hook --> unplanned_files
  ls_hook --> openspec_text
  ls_hook --> side_file
  ls_hook --> change_list
  ls_hook --> change_log
  ls_hook --> cogtext
  stale_edit --> ls_cli
  scaffold --> cogtext
  cogtext --> parent_text
  cogtext --> signature_text
  docstring_up --> aes_bridge
  plan_edit --> change_list
  ls_hook --> plan_edit
  behavior_check --> aes_bridge
  criterion_checks --> aes_bridge
  linked_tests --> aes_bridge
  action_check --> aes_bridge
  unplanned_files --> layout_plan
  plan_to_code --> aes_bridge
  requirement_status --> change_log
  wiki --> requirement_status
  wiki_reach --> wiki
  aes_bridge --> layout_plan
  ls_cli --> evidence
  ls_cli --> planning
  docstring_up --> planning
  change_log --> planning
  plan_to_code --> characterize
  requirement_status --> evidence
  change_list --> context
  symbol_gate --> characterize_python
  unplanned_symbols --> characterize_python
```

The Lockstep group's `check` is `src/lockstep/check.py` and `hook` is `src/lockstep/hook.py`; its `checks` directory
holds `trace`, `arch`, `test_first`, `sources`, `docmeta`, `status`, `show`, `project`, `config`, `spec`, `markers`, `plugin` and `cli`.
The edges are the imports in `src/lockstep/*.py` (for example `src/lockstep/hook.py:107-116` imports `aes_bridge`, `change_log`,
`cogtext`, `change_list`, `openspec_text`, `shell_targets`, `side_file`, `stale_edit` and `unplanned_files`; `src/lockstep/check.py:404-413`
imports `scaffold`, `plan_check` and the `checks` directory on demand); only the main ones are drawn (`src/lockstep/hook.py:387` imports `plan_edit`, `src/lockstep/plan_edit.py:46` imports `change_list`). `records_fb` and `evidence_fb` are `scripts/learning_loop/records.py` and `evidence.py`, drawn apart from the
library's `records` and `evidence`. The claims-era scripts (`scripts/*.py`, `scripts/meta/`, `enforced_planning/` except `__init__.py`) were retired on 2026-11-12 and 2026-11-14 (open question Q10, resolved).
Dotted arrows are jobs whose timers are off (open question Q21).

Source-local documentation upkeep was added after the revision above:

| Code unit | Job | Source anchor |
| --- | --- | --- |
| `doc_projection` | Read declared Markdown metadata, Python AST interfaces and JSON/YAML evidence fields, render only their marked document blocks, and check freshness; native post-edit refresh appends daily run records. | [module contract](../../src/lockstep/doc_projection.py#L1), [projection](../../src/lockstep/doc_projection.py#L134) |
| `work_units` | Check the plan's work-unit DAG (`docs/planning/work-units.json`): cycles, missing dependencies, merged units without evidence; list ready units, the longest unmerged chain and independent units touching one file. | [module contract](../../src/lockstep/work_units.py#L1), [analysis](../../src/lockstep/work_units.py#L27) |
