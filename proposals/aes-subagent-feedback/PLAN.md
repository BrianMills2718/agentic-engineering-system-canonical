---
schema_version: "1.0"
artifact_type: design_plan
id: aes-subagent-feedback
status: proposed
method_conformance_receipt: proposals/aes-subagent-feedback/PLAN.receipt.json
goal:
  outcome: "Native subagent assignments and checked outcomes feed the existing evidence-to-prevention loop"
  canonical_example: "A real development-investigator return is captured from native traces, checked by the parent, and filed as an attributable feedback report"
  forbidden_substitutes: "Child self-rating, fixture-only execution, guessed model or inherited rules, duplicate independent sightings"
  boundaries: "AES learning-loop adapter and prerequisite AES #460 fixture/guide gate repair; no runtime router, hook, permission, role or selector changes"
  done_when: "Review native canary trace, checker receipts, report issue and weekly record membership; pass required local checks"
  do_not_gate_on: "No further human approval for reversible implementation or merge; no benchmark or automatic model-policy promotion"
---

# Parent-verified subagent feedback

Each section below answers the checklist items quoted in it; the gate judges only that
section's text. Replace every `TODO(answer ...)` line before running `cli.py check`. Quote
values in the front matter: an unquoted ` #` starts a YAML comment and cuts the value.

## Actor and result

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

Brian and parent coding agents need reusable roles improved from actual outcomes. In native canary subagent-feedback-canary-v1, development-investigator diagnoses why current transcript parsing drops tool events; the parent checks its JSON schema and cited source facts. The same private feedback log receives a record carrying parent/child identities, assignment context and actual check results.

## Success and disproof

> **CORE-SUCCESS-DISPROOF** (blocking): The plan defines the evidence that would show success and a concrete condition that would disprove the approach.

> **CORE-TRACE-REVIEW** (blocking): Every success or acceptance criterion in the plan is judged from the full trace of a run, not only its final outcome: it names the run whose full trace is examined (for example the session, its tool and LLM calls, commits, check output, or messages), where that trace lives, and what must be seen in that trace beyond the final outcome. A criterion that names only an outcome, such as tests passing, a PR merged, a test fixture reproducing the journey, or a status reading succeeded, fails this item. A criterion for which no run exists, such as a pure document edit, passes only when the plan states that exemption and its reason explicitly.

Success: the native canary assignment and completion are captured; the parent verifier checks its exact returned bytes; its generated record IDs are members of problems.load_records output and its private issue contains the same metadata. Regression checks prove completed-without-checks stays unverified, failed/cancelled/inconclusive runs remain visible, mismatched child/result receipts cannot produce verified success, and rereading a parent gives stable report IDs. Required local make check passes. Disproof: any unchecked completion becomes verified_pass, any different child borrows a check, or the weekly reader drops the canary record.

Run subagent-feedback-canary-v1 in parent Codex session 01a11cac-2557-7dc0-8edd-8487ed5968d1. Review the complete native parent spawn/result and full child transcript under ~/.codex/sessions, including inputs, actual reads, returned citations, model/effort and limitations. Keep exact trace refs and hashes in the existing private repair-verification.jsonl, never commit raw transcripts. Review checker command argv/stdin hash/stdout/stderr/exit, filing request and issue readback, daily report JSONL, and weekly reader membership. Each negative regression run retains pytest assertion output for the opposite condition; inspect every failure and surprising pass. Review make check output and exit. Document edits have no separate behavioral run; structural links and source facts are checked.

## System model

> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: exempt -- <reason>`, which fits only a project with no stored state and no user-facing view. Unless exempt, the plan names each system-model element (entity, process, record or event, or view) that the work adds, changes, or relies on, and its trace review names, for each such element, what the examined run must show of it (for example an event of that record type with its id, or the view displaying that entity). A plan with neither a model link nor the exemption line fails this item, as does one that lists model elements without saying what the examined run must show of each, or one that names no element without stating that the work touches none and why.

System model: proposals/aes-subagent-feedback/SYSTEM_MODEL.md, extending proposals/aes-learning-loop/PLAN.md Record model. Elements: assignment (parent/session/call/role/context packet hash); native terminal event and child trace; parent verification receipt (exact result digest and executable checks); existing feedback report/record, daily JSONL and state.sqlite; private issue view and weekly problem reader. The canary trace must show the same call/child/result identity across each element, actual check exit and issue JSON metadata, and exact record membership in weekly input. Failed checks retain failure rather than a success grade. Per-element observations required: assignment call ID and packet digest in native trace; terminal child ID and returned-result digest; parent receipt with same digest, argv, stdout/stderr and exit status; report ID and record IDs in reports-YYYY-MM-DD.jsonl; state.sqlite reports row with that report ID and read-back issue URL; private issue JSON with matching subagent metadata; weekly load_records output containing those exact record IDs. Licence, enforcement and recurrence elements are unchanged and outside this new canary: current learning-loop regression traces must show independent-sighting rejection, explicit enforcement-time comparison and one-time reopen; no claim of an authentic post-enforcement subagent recurrence is made.

## Authority and non-goals

> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).

Brian approved 2026-10-08: wire parent-verified subagent outcomes into existing feedback path and verify one complete run. Root Codex session owns implementation/integration. Do not change model selection, agent-router adoption, child permissions, global hooks, readonly child JSON contracts, taxonomy intake or claim registry. The existing learned report contract and nightly/weekly/daily consumers remain owners.

## Irreversible actions and spend

> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.

Brian is the spend and action authority: his 2026-10-08 approval covers one native bounded canary and routine planning conformance under his standing configured-model authority. The parent contains this to one leaf assignment, readonly permitted paths and 12-turn role instructions, with no model override. Planning uses the existing approved OpenRouter client with 0.05 USD per-check limits and at most 1 USD for this adoption; stop on quota/billing errors and preserve their traces. No deletion, migration, publication of private data, outbound communication or paid comparative evaluation is proposed. Existing configured native Codex model executes one approved bounded canary. Planning conformance uses existing approved llm_client OpenRouter route and per-call budget. Git commits/push/merge and refreshing the private local AES collector deployment are recoverable and authorized by workspace policy.

## Uncertainties

> **CORE-UNCERTAINTIES** (blocking): The plan lists its material uncertainties, and each one has an owner or the evidence that would resolve it.

Parent owns native format variation: inspect real Codex and Claude Agent/Task tool events and child metadata, support only observed shapes and test fixture parity; unknown shapes remain unverified. Parent owns context/model attribution: record only observed runtime values, preserve unknowns, never infer installed source equals loaded rules. Parent owns terminal/verification correlation: require exact assignment and result digest. Existing llm_client router owner owns future selection use; this lane supplies evidence only.

## Activation facts

> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend.

shared_mechanism=true: reusable transcript/report adapter. llm_central=true: authentic native child reasoning plus existing semantic planning checks. empirical_comparison_proposed=false: acceptance/regression checks only, no model comparison or benchmark. irreversible_or_spend_action=true: already-authorized native canary and OpenRouter planning checks consume configured model usage; no batch, provider change, migration or irreversible action.

## Prior art and ownership

> **OV-PRIOR-ART-DISPOSITION** (blocking): Existing ownership, internal lineage, and relevant external prior art were searched, and each candidate found is dispositioned as reuse, extend, compose, supersede, or bounded exception.

> **OV-PRIOR-ART-PARALLEL-CHECK** (advisory): The plan names one concrete structural check or consumer-path observation that would detect a silent parallel implementation of the same concern.

Search performed 2026-10-08: bounded rg searches of AES collector/transcript/report code and agent-skills native definitions established existing ownership; native Codex and Claude traces established runtime lineage; web search of the official W3C PROV primer established relevant external prior art. Extend existing AES scripts/learning_loop/transcripts.py, feedback_log.py, collector daily reports and problems.load_records, retaining observation/claim/action and current enforcement receipts. Reuse agent-skills contracts/specialists/development-investigator.v1.json and native result schema without changing the leaf. Reuse native Codex/Claude tool traces instead of inventing runtime hooks. Reuse llm_client Plan379 outcome ownership; avoid its claimed files (native owner notified). Internal register vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md per-skill feedback and typed terminal outcomes searched: reuse its parent-reflection responsibility and compose terminal identifiers into the existing report envelope; do not adopt a parallel per-agent store. These are the only candidates found in that bounded search. W3C PROV source: https://www.w3.org/TR/prov-primer/. External W3C PROV entity/activity/agent attribution supports existing report provenance; compose identifiers/hashes only, no ontology service. The parent responsibility in design-subagents already requires verification; extend its existing feedback consumer rather than a parallel log.

Authentic consumer check: the generated canary report is filed by existing feedback_log.file_report into agent-feedback-log and its exact record IDs appear in existing problems.load_records over the same reports-YYYY-MM-DD.jsonl. No agent-feedback directory, alternate database or selector is created; git diff confirms only declared AES paths.

## LLM call boundary

> **OV-LLM-CALL-BOUNDARY** (blocking): The plan describes the model call graph, the structured result boundary each call returns, and how calls are traced.

> **OV-LLM-AUTHORITY-PROMOTION** (blocking): The plan names the provider and spend authority for model calls and one authentic-run condition that must hold before the behavior is promoted.

One native development-investigator call inherits the configured Codex model with a bounded explicit packet; returns DevelopmentInvestigationResultV1 JSON, validated by parent executable schema/citation checks. Native parent and child transcripts provide call/result traces. Collector adapter uses deterministic JSON/tool structure and hashes, no prose inference. Existing weekly Jev/strong-model graph stays unchanged and is not executed by this canary; its internal output boundaries remain the existing family, relation and causal-analysis Pydantic contracts in label_items.py, relation_check.py and problems.py. The native parent is the existing coordinator session, not a newly introduced model-call interface; its relevant outputs are native spawn/wait calls and the executable parent-check receipt, not a self-rated final answer. Company Planning semantic checks return its typed SemanticJudgment through llm_client with recorded task/trace IDs.

Spend authority is Brian, through his 2026-10-08 approval and standing permission for routine configured-model implementation checks. Parent controls one native canary and at most 1 USD of OpenRouter adoption checks (0.05 USD per call). Provider authority: existing configured native Codex route and approved shared llm_client OpenRouter conformance route; no model override or new benchmark spend. Promotion requires one actual installed-role invocation, full child trace inspection, parent checks on the exact result and private issue readback through the normal report path. Fixtures or child self-reported status alone cannot promote; missing model/context/rules are labelled unknown. This promotes capture only, never role trust or selector policy.

## Coordination

> **OV-COORD-OWNERSHIP** (blocking): The plan names exact ownership, dependencies, conflict surfaces, the integration owner, and the work-unit evidence for each concurrent writer.

Root session codex:01a11cac-2557-7dc0-8edd-8487ed5968d1 owns claimed AES worktrees/subagent-feedback: scripts/learning_loop, tests/learning, this proposal, REPAIR.md, .project-brain/now.md and execution cursor/history. Native canary is read-only, no writer claim or edited files. llm_client system-one-router owns selector/store source and tests; no dependency on its completion. AES agent-router-plan and rules-sort own router adoption/rules sorting; no overlap. No cross-lane dependencies: this lane can be merged without their changes. Conflict surfaces: llm_client/core/feedback_routing.py and its tests belong to system-one-router; proposals/agent-router/{PLAN.md,README.md,planning records} belong to agent-router-plan; scripts/rules and docs/rules register plus sorting tests belong to rules-sort. Their official claim records and native thread replies are the work-unit evidence, captured in private repair-verification.jsonl; there is no delegated implementation unit in this plan. Official claims check records healthy intact lane after registry reconciliation race. Root integrates via local make check, recoverable commit, merge commit and native session-close.

Prerequisite discovered by the required full local gate: AES issue #460 reproduces seven pre-existing distribution failures because fixture and Getting Started commits use messages refused by the installed commit rule. The same root session additionally owns tests/greenfield/test_distribution.py and docs/greenfield/GETTING_STARTED.md through a native claim refresh; the harness-gate-repair owner confirmed its project-meta repair does not cover AES. Both files are already planned exact artifacts in .aes/target.yaml. Reuse the existing installed commit hook and the guide's accepted AES plan; repair fixture/guide messages and bootstrap ordering, without changing or disabling runtime enforcement. Run the affected distribution tests, inspect every rejection receipt or unexpected pass, and then run make check once on the final committed subject. A valid tagged change must pass while an orphan/unrouted criterion still fails at its owning topology check. The canonical feedback capture example and its acceptance conditions are unchanged. Evidence: https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/460 and the existing private repair-verification.jsonl full-suite run (7 failed, 321 passed, 1 skipped; make exit 2).
