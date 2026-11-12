---
description: AES canonical's system model for planning -- AES's parts across repositories, this repository's containers, every record type with what writes it, and what is outside the model
---

# AES canonical: system model (planning view)

AES is the whole agent system: Lockstep, the feedback loop and the policy layer (Brian, 2026-11-11: "to me aes
is the whole sysem lockstep is one part. aes include the whole feedback and policy system"; `~/.claude/history.jsonl`,
session a769ac09). Its parts live in four repositories (Lockstep moved into this one on 2026-11-11 and 2026-11-12, PRs #831 to #837). This page shows where each part is, what talks to it, and
which part of this repository does what. It extends the checked model of the v0.2 engine, [ODD.md](../model/ODD.md)
and [trace.yaml](../model/trace.yaml). Every code unit is on the [system map](system-map.md). Read at origin/main
`0395758` (2026-11-12).

## Context: AES's parts, where each lives, and what talks to them

Question answered: what is AES made of, which repository holds each part, and what talks to it? This is also the
cross-repository view: this repository, agentic-engineering-system-canonical, is one of four.

```mermaid
flowchart LR
  brian([Brian: approves plans, gives corrections, sets rules])
  agent([Coding agents: Claude Code, Codex])
  subgraph aesrepo[agentic-engineering-system-canonical: this repository]
    loop[Feedback loop<br/>scripts/learning_loop, nightly timers]
    register[Rules register<br/>docs/rules, scripts/rules]
    lib[Retained AES library<br/>src/agentic_engineering_system]
    onetool[Lockstep, the one tool<br/>src/lockstep: plan, docstrings, edit hook,<br/>commit checks, plan check, status; pcw is an alias]
  end
  oldls[lockstep repository<br/>kept as history]
  subgraph tpl[code2-template]
    c2c[code2check<br/>commit checks]
  end
  subgraph ws[code2-workspace]
    rules[Agent rules<br/>agents/core.md, topic files, rule-sources.md]
    map[Harness map<br/>docs/architecture/model.c4]
  end
  log[(agent-feedback-log<br/>private issues)]
  users[lifelike, Team-Brains runner,<br/>code2 repositories]
  brian -->|corrections in sessions| agent
  agent -->|transcripts| loop
  loop -->|one issue per report| log
  brian -->|rules, approved in words| rules
  register -.->|lists rules the loop licensed| rules
  onetool -->|imports| lib
  onetool -->|edit hook and lockstep check| users
  c2c -->|make check, until each repository switches| users
  oldls -.->|code moved from| onetool
  c2c -.->|checks ported into| onetool
  map -->|draws| aesrepo
```

Dotted arrows are history (code moved or ported) or partial (the register lists one rule; open question Q20). Users switched
but not all: lifelike is pinned to this repository, code2-template installs lockstep, and Team-Brains' runner vendors its wheel
(`wiki/lockstep.md:21-23`); existing code2 repositories switch when next changed.

## Containers: the parts of this repository

Question answered: which part does what, and which stores does each write?

```mermaid
flowchart TB
  subgraph v02[v0.2 product: governed roots]
    cli[aes CLI<br/>src/agentic_engineering_system/cli.py]
    plan[planning.py<br/>proposals and accepted plans]
    ev[evidence.py<br/>observations, freshness, standing]
    rec[reconcile.py + characterize.py + topology.py<br/>state, drift, orphans, gaps]
    ctx[context.py<br/>working-context packets]
    hk[hooks.py<br/>pre-commit hook writer<br/>not installed here: lefthook runs instead]
  end
  v01[repository_context/<br/>v0.1 Plan 001 resolver]
  ls[src/lockstep/<br/>Lockstep: layout, edit hook, checks, plan check, status<br/>src/pcw alias]
  lsy[(lockstep.yaml and openspec/specs/<br/>written in the repositories that install it)]
  ep[enforced_planning/<br/>vendored claims, sessions, worktrees<br/>44,556 lines; retired in ~/code2]
  ll[scripts/learning_loop/<br/>the feedback loop, nightly]
  rr[scripts/rules/ + docs/rules/<br/>rules register]
  scr[scripts/<br/>meta, hive: claims-era scripts and brain_fresh]
  docs[docs/, proposals/, research/, wiki/<br/>135 Markdown files]
  t[(.aes/target.yaml)]
  o[(.aes/observations/)]
  p[(.aes/plans/)]
  g[(.githooks/pre-commit<br/>dormant)]
  pj[(.aes/project.yaml)]
  lb[(.aes/legacy_baseline.json)]
  ad[adopt.py + project.py<br/>aes adopt, aes init]
  cli --> plan --> t
  plan --> p
  cli --> ev --> o
  cli --> rec
  rec -->|reads| t
  rec -->|reads| o
  cli --> ctx
  cli --> hk --> g
  cli --> ad --> pj
  ad --> lb
  ls -->|reads| lsy
  ls -->|imports| v02
  ls -->|writes first docstrings and wiki pages| docs
  scr -->|generate pages| docs
  rr -->|generates RULES.md| docs
  ll -->|files issues in agent-feedback-log| out[(outside: agent-feedback-log)]
```

## Record types the v0.2 code defines, and what writes each

The retained library's records. The `aes` command line that writes them retires one repository at a time
(code2-workspace decision 0009 (a)); Lockstep still imports the library.

| Type | Defined at | Written by | Stored in |
|---|---|---|---|
| `TargetRecord` with `Outcome`, `NormativeItem`, `SuccessCriterion`, `EvidenceRequirement`, `Component`, `PlannedArtifact`, `VerificationSubject`, `ExternalBoundary` | `src/agentic_engineering_system/records.py:137` (members from line 65) | `aes init` (`project.py:166`), `aes plan accept` (`planning.py:646`) | `.aes/target.yaml` |
| `ProjectRecord` with `AesInfo`, `Materialization`, `Ecosystem` | `records.py:194` | `aes init` (`project.py:159`) | `.aes/project.yaml` |
| `Proposal`, `TargetDelta`, `TraceReviewDeclaration` | `planning.py:168`, `:137`, `:148` | the agent, by hand, before `aes plan validate` | a proposal file anywhere |
| `AcceptedPlan` | `planning.py:197` | `aes plan accept` (`planning.py:643`) | `.aes/plans/<id>.yaml` |
| `ObservationRecord` with `Observer`, `ErAssessment`, `DependencyBasis`, `NegativeControl`, `DecisionCheck`, `TraceReview` | `evidence.py:184` (members from line 99) | `aes evidence record` (`evidence.py:613`); external observations by hand in the same shape | `.aes/observations/` |
| `EvidenceReport`, `CriterionStanding`, `ErStatus` | `evidence.py:427-441` | computed by `assess` (`evidence.py:510`), never stored | none |
| `Characterization`, `CharacterizedFile`, `Producer`, `Drift` | `characterize.py:61`, `:54`, `:49`, `:208` | computed by `aes characterize` | none (`--out` writes a copy, `cli.py:286`) |
| `Reconciliation` with `DriftFinding`, `ArtifactState`, `CriterionState`, `ObservationState`, `PlanState`, `Gap`, `ComponentState`, `MissingRequirement` | `reconcile.py:134` (members from line 69) | computed by `aes status` / `aes reconcile` (`reconcile.py:259`) | none |
| `TopologyReport` | `topology.py:38` | computed by `aes topology check` | none |
| `Baseline`, `LegacyState`, `AdoptResult` | `adopt.py:48`, `:67`, `:56` | `aes adopt` (`adopt.py:156`) | `.aes/legacy_baseline.json` |
| `WorkingContext`, `Provenance` | `context.py:72`, `:63` | computed by `aes context <subject>` | none |
| Helper and result types: `Locator` (`records.py:101`), `FamilyEntries`/`FamilyKeys`, `OutsideGovernedRoot` (`planning.py:107-143`), `CharacterizeReport` (`characterize.py:250`), `InitResult` (`project.py:66`) | as listed | computed or nested inside the records above | none |
| `ReviewCheck` | `trace_review.py:18` | computed while assessing a trace-review requirement | none |
| `RepositoryContextArtifact` and its observations (v0.1) | `repository_context/models.py:87` | `repository_context/cli.py` | a JSON context file and an HTML surface (`repository_context/render_html.py`) |
| Feedback loop: `Record` with `Link`, `Provenance` (one observation, claim or action line) | `scripts/learning_loop/records.py:49`, `:34`, `:39` (contract at line 25) | `feedback_log.py:94` and `:172`, called by the nightly `collect_feedback.py` | `reports-<date>.jsonl` in `~/projects/data/feedback-collector/` (`collect_feedback.py:69`), filed as agent-feedback-log issues |
| Feedback loop: `Turn`, `Transcript` | `scripts/learning_loop/transcripts.py:42`, `:51` | read from Claude Code and Codex session logs (`collect_feedback.py:127`) | none (read only) |
| Feedback loop: subagent `Check`, `Verification`, `Outcome` | `scripts/learning_loop/subagents.py:30`, `:38`, `:51` | the nightly collector (`collect_feedback.py:66` imports it) | turned into `Record` lines in `reports-<date>.jsonl` |
| Feedback loop: problem analysis `_Step`, `_Fix`, `_Analysis` | `scripts/learning_loop/problems.py:184`, `:191`, `:197` | `problems.py` (model answer schema, `problems.py:246`), reading `reports-*.jsonl` | `problems-<date>.jsonl`; with `--file`, one issue per recurring problem |
| Policy layer: `AgentRouterProfileV1`, `RouterProposal`, `HandoffRecordV1` (all `Contract`) | `scripts/rules/agent_router.py:51`, `:147`, `:176` (`Contract` at line 25) | the agent router (`scripts/rules/agent_router.py`) | `~/projects/data/agent-router/` (`agent_router.py:48`); handoffs counted by `account_handoffs` (line 227) |
| Policy layer: `Disposition` (keep, move or retire for one legacy rule) | `scripts/rules/sort_legacy.py:54` | `sort_legacy.py` (model answer, checked at line 94) | `legacy-sort.jsonl` and `legacy-dispositions.private.yaml` in the router's data folder (`sort_legacy.py:11`, `:328`) |

## Lockstep's records

Lockstep (package `src/lockstep/`, specs `openspec/specs/lockstep-*`) keeps no database of its own. It reads the plan from
OpenSpec requirements plus `layout:` rows in `lockstep.yaml` (`src/lockstep/layout_plan.py:29-30`, `:60`, `:101`), still reads
`.aes/target.yaml` (`wiki/lockstep.md:30`), and keeps a side file `lockstep.yaml` with schema `lockstep.side.v1`
(`src/lockstep/side_file.py:126-127`, `SideFile` at `:136`). Its commit checks and their block, warn or off modes come from
`src/lockstep/checks/config.py:23-24` (`Config` at `:33`). Its writes are source and test files that begin with a docstring
copy of the plan (`src/lockstep/scaffold.py`), the append-only change log (`src/lockstep/change_log.py`), generated wiki pages
(`src/lockstep/wiki.py`) and a hook log under `.pcw/` in the installing repository (`src/lockstep/hook.py:178`; the design says `.lockstep/`, proposals/one-planning-tool/DESIGN.md:48, open question Q23). These live in the repositories that
install Lockstep; none is stored here, except what the tests build under `tests/lockstep/`.

## Does AES execute typed rules?

No. AES's rules (drift, staleness, insufficient-not-green, trace-review declared) are fixed Python
functions such as `assess` (`src/agentic_engineering_system/evidence.py:510`) and `reconcile`
(`reconcile.py:259`). The target holds typed records that reference each other, but no record
defines a rule whose effect AES evaluates, so there is no type-level metamodel to map onto the
shared kernel. Open-questions entry Q9 records the reasoning.

## Outside this model

- `enforced_planning/` (vendored claims, sessions and worktree lanes) and the `scripts/meta/`
  coordination scripts that import it. `~/code2` replaced claims with `claude -w` worktrees
  (`~/code2/AGENTS.md`); they stay in place, unmodelled, and the one-tool plan does not use them (Q10).
- The rules register file `docs/rules/register.yaml` and the feedback loop's plans and pages in
  `proposals/aes-learning-loop/`: their record types are in the table above; the system map names each code unit.
- Lockstep's walkthrough pages and recorder: no page moved with the code, so acceptance A1 to A5 still have no page (open question Q22).
- The Company Planning profile files under `docs/architecture/` (ODD.md gap G1).
