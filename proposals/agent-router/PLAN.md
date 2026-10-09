---
schema_version: "1.0"
artifact_type: design_plan
id: agent-router
status: adopted
method_conformance_receipt: proposals/agent-router/receipt.json
revision_status: fresh semantic adoption 2026-10-09; runtime acceptance pending
goal:
  owner: "codex:01a11cac-2557-7dc0-8edd-8487ed5968d1"
  report_deadline: "PT30M"
  outcome: "An agent starting or handing out a job carries only the rules, subagent, model and effort that job needs, chosen by fixed layers plus a fast model, with every choice logged and judged by outcome."
  canonical_example: "Brian asks for a dashboard page fix: the router log shows frontend then reviewer subagents, the UI rules injected, model and effort chosen; when the frontend agent runs gh pr merge the hook injects the three merge rules; the outcome row records whether the check passed."
  forbidden_substitutes: "A design page alone; a hook tested only on a fixture; router proposals never compared with what agents actually chose; a token saving estimated from file sizes; a second model selector beside llm_client Plan #379."
  boundaries: "AES rules register and router log, client-specific adapters to the existing hook/handoff mechanisms with an off switch; no edits to llm_client or harness-context files by this lane; the workspace instruction file stays unchanged until the required-rule coverage and four-cell injection checks pass; no outbound messages."
  done_when: "Slice 1: every legacy rule has a source-supported disposition and every kept rule a validated applies_when tag. Slice 2: authentic Claude and Codex parent/child traces prove ordinary delivery and mandatory-rule fallback. Slice 3: all eligible real handoff IDs over two weeks join to terminal statuses and separately reported independent outcomes. Slice 3b: an authorized bounded reversible canary checks executed candidate and incumbent outcomes independently. Slice 4: automatic fields are proposed only from those outcomes with a verified fallback. Two independent portable profiles show actual effective dispatch without engine edits. Thirty days after slice 2 ships, full trace joins show migrated-rule recurrence does not rise; missing evidence remains pending."
  do_not_gate_on: "Brian reading the review page; the Codex sessions finishing Plan #379 or harness-context; unrelated historical baseline failures recorded in AES #460; affected checks still apply."
---

# Agents get only the rules, subagent, model and effort each job needs

Design, diagram and the dashboard example: [README.md](README.md). Brian activated the goal "finish all remaning work" on 2026-10-09, authorizing completion of this remaining feedback/router work. The earlier [revision goal](revision.goal.md), [revision route](revision-path-decision.json) and [verification trace](verification.log) remain evidence of the document-only correction task. The 2026-10-08 receipt and generated goal do not adopt the changed plan. Re-adopt this exact plan before implementation; retain the original outcome and all observation, parity, fallback and promotion obligations below.

## Current execution frontier

The feedback intake, one transport-scoped prevention case and installed cross-repository commit-guard repair are already landed; their completion records are in `proposals/aes-feedback-prevention/completion-evidence.json` and PRs #479, agent-skills #460 and #487. They are prerequisites, not proof of this router's acceptance criteria.

The immediate slice is the preserved rules inventory. Its cache contains 263 source IDs, including four unresolved answers. On 2026-10-09 its recorded attempts total $6.278699 in known costs and 27 attempts lack cost data; the earlier $5 sort allowance cannot be assumed to have a remainder. Reuse and inspect those authentic traces and current sources. Make no additional sort calls without separately established spend authority. A `retire` disposition is an inventory recommendation only: this slice removes or activates no mandatory rule and leaves the legacy register unchanged.

Completion of this goal still requires all slices and success checks below. The two-week handoff observation and 30-day recurrence check retain their actual observation periods. Implementing their collectors or installing a timer does not complete those observations. The coordinator keeps the goal active while useful work remains; an unavailable provider, unmet spend boundary or elapsed-time dependency receives an exact resume event rather than a fabricated pass.

## Actor and result

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

**Actor:** Brian, and every Claude Code and Codex agent working for him. **Result:** an agent carries only the rules its job needs, and work is handed to the right specialist on the right model and effort, chosen by a fast model and fixed layers rather than by habit.

**Example (stable, user-visible):** Brian asks for a broken dashboard page to be fixed. The router log (`~/projects/data/agent-router/router-<date>.jsonl`, one line per handoff) shows: subagent `frontend` then `reviewer`; injected rules `ui-tooltips-default`, `ui-index-first`, `red-green-colorblind`; model and effort for each. When the frontend agent runs `gh pr merge`, its own transcript shows the hook's added context naming the three merge rules. The outcome row for that handoff records whether its check passed or the change was reverted. The design and diagram are in [README.md](README.md).

## Requirements

> **CORE-REQUIREMENTS-TRACED** (blocking): Each requirement names its check and pending or verified status; deferred execution remains visible on completion records.

The five corrections below are Brian-approved design requirements. Their **document checks** are the source diff and full editing/validation trace in `verification.log`; their **execution checks** remain planned, not run by this revision. A passing document check establishes that the obligation is stated, not that the router works.

| ID | Required behavior | Execution check and status |
| --- | --- | --- |
| AR-OUTCOME | Shadow agreement does not prove the outcome of an unexecuted choice. Require an independently checked, bounded reversible canary before proposing automatic routing. | Slice 3b's frozen task criteria, both execution traces and independent check outputs; planned, not run. |
| AR-PARITY | Rule delivery reaches real parents and children in Claude Code and Codex. | Slice 2's four-cell matrix below, including unavailable-injection fallback; planned, not run. |
| AR-FALLBACK | Required rules remain covered and protected actions retain deterministic checks when injection or routing fails. | Per-rule coverage inventory plus off-switch, missing-hook and missing-context journeys; planned, not run. |
| AR-ACCOUNTING | Every eligible handoff remains in the reliability denominator, including capped, failed, invalid and unsupported proposals. | Joined handoff membership and terminal statuses, with independently reported outcome completeness; planned, not run. |
| AR-PROFILES | Colleagues can configure policy, specialists, native model/effort capabilities and budgets without editing engine code. | Two independently configured profiles, portable paths, rejected unsupported options and recorded effective configuration; planned, not run. |
| AR-INVENTORY | Every source legacy rule has a supported disposition and every kept rule a valid applicability tag. | Exact source-ID membership, cited-source review and authentic register/page checks; planned, not run. |
| AR-CONTRACT | Native hook/agent and existing specialist result artifacts satisfy the externally owned contracts listed in Standard conformance; AES additions are labelled extensions. | `tests/test_agent_router.py` contract cases plus native capability/delivery traces; planned, not run. |
| AR-RECURRENCE | Thirty days after slice 2 ships, mistakes covered by migrated rules do not recur more often. | Source-session/delivery joins and reviewed daily feedback sightings, separating delivered-and-ignored from never-delivered; planned, not run, observation starts at shipment. |

The current [acceptance records](evidence.json) carry all eight requirements into separate canary, promotion and completion entries, each explicitly `planned`, not passed. They are pre-execution records, not results. Later writes retain this exact requirement membership and attach native trace/check references before a status can become passing; no release or completion omits a pending criterion. The record membership is checked during adoption and again by the implementation's acceptance-record consumer before promotion. No pilot or activation is claimed by this planning checkpoint.

## Success and disproof

> **CORE-SUCCESS-DISPROOF** (blocking): Success checks test the claimed property directly and name a concrete disproof.

> **CORE-TRACE-REVIEW** (blocking): Judge each criterion from its named full run trace, not only its final outcome.

**Success evidence:**
1. Each legacy rule has a source-supported disposition; each kept rule has an applicability tag. Verify actual membership against the source inventory, not only the historical count of 263.
2. Required-rule coverage and delivery pass all four client/agent cells below, including the off switch and failure fallback. A hook configuration or injection log alone is insufficient.
3. Two weeks of observe mode account for every eligible real handoff and exposes failures, cost, latency and missing outcomes. Agreement is diagnostic evidence only.
4. Before any automatic field is proposed, the bounded canary below demonstrates acceptable checked job outcomes against the incumbent. Read every failure and disagreement and a sample of passes. No claim about an unexecuted alternative is allowed.
5. A colleague profile changes allowed rules, roles, native model/effort choices and caps without a code fork; effective profile and client capability snapshots are recorded with every handoff.
6. Preserve the prior recurrence requirement: during the 30 days after slice 2 ships, recurrence of mistakes covered by migrated rules does not rise. Inspect each sighting against its source, session trace and actual rule delivery before attributing any difference.

**Disproof:** required context is absent before a protected action; a fallback bypasses its existing deterministic gate; one client/agent cell is silently treated as supported; eligible capped/invalid/failed calls disappear from reported reliability; or a proposed automatic field fails the canary's predeclared task criteria relative to the incumbent. Such a field stays manual/observe-only. Shadow agreement cannot override any of these failures.

**Named run traces and what they must show:**
- **Slice 1:** sort call traces in llm_client `calls_<date>.jsonl`, source lines, and the actual register entry for every retained or retired rule. Check the cited source and disposition, not the total count.
- **Slice 2:** four authentic journeys: Claude parent, Claude child, Codex parent, Codex child. Retain native session/child IDs, client/version and capability snapshot, the actual context seen before the matching action, the tool/action and check result. Each cell must exercise the ordinary path and a disabled/unavailable injection path. Configuration, parent-only context and a log saying injection happened do not prove child delivery. An unsupported hook is recorded as unsupported; verify explicit role/handoff delivery in that client's child transcript instead and retain always-loaded rules until that route passes.
- **Slice 3:** join every eligible handoff ID to its input/configuration snapshot, llm_client call (when attempted), typed proposal or terminal failure, actual dispatch and independent job-check result. Read all invalid/capped/failed/missing-outcome cases and all disagreements, plus a sample of agreements.
- **Slice 3b:** isolated, reversible executions of incumbent and proposed choices on the same frozen starting state and task criteria. Keep each full trace and the independent checks described below. A proposal that never executed has no candidate outcome.
- **Slice 4:** during the first two weeks after an authorized switch, for each routed field, verify the dispatched value, selected rule coverage, native client support, check output and any fallback/revert. Read every failing or surprising trace before attributing a cause. The 30-day recurrence check joins the nightly collector/problem records (`items-<date>.jsonl`, `problems-<date>.jsonl`) to the source session and actual delivery by session and rule ID. Classify delivered-and-ignored versus never-delivered; counts alone do not prove a rule was delivered or followed.
- **Profile checks:** run the same representative handoff through Brian's profile and a colleague's independently selected profile; inspect the effective configuration, native choices and distinct dispatch/fallback behavior, not only two configuration files.

**Trace locations:** slice 1 reuses `/home/brian/projects/data/agent-router/legacy-sort.jsonl` and the shared client's `calls_<date>.jsonl` under its configured project log root. For slices 2–4 and profile checks, the proposed `proposals/agent-router/evidence.json` is the durable index: each criterion links its native parent and child session IDs to the full original Claude `~/.claude/projects/<project>/<session>.jsonl` and subagent transcripts, or Codex `~/.codex/sessions/<year>/<month>/<day>/rollout-*.jsonl`, plus the actual check output. Debug/provider logs required to prove context delivery are linked too. Existing harness evidence lives in `proposals/harness-context/native-parity/verification.json`; its Claude refusal trace is `/home/brian/.codex/log/harness-fresh-parity-20261009-claude.jsonl`. These are evidence locations, not passing router results.

Observe/rollout events append to `AGENT_ROUTER_OUT/router-<date>.jsonl` and `inject-<date>.jsonl`; `AGENT_ROUTER_OUT` resolves from project/profile configuration. Canary and profile execution outputs are packed into the owning project's existing `artifacts.sqlite`; the evidence index keeps their run IDs and read commands. The recurrence check links the existing feedback collector's daily item/problem records to these exact original sessions. Every failing or surprising item and a pass sample gets a trace-review entry classifying never-returned evidence, returned-but-unused evidence, or an incorrect expected check. Missing traces are inconclusive.

## System model

> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: exempt -- <reason>`, which fits only a project with no stored state and no user-facing view. Unless exempt, the plan names each system-model element (entity, process, record or event, or view) that the work adds, changes, or relies on, and its trace review names, for each such element, what the examined run must show of it (for example an event of that record type with its id, or the view displaying that entity). A plan with neither a model link nor the exemption line fails this item, as does one that lists model elements without saying what the examined run must show of each, or one that names no element without stating that the work touches none and why.

Documentation entry point: [wiki/index.md](../../wiki/index.md) links [this proposal model](README.md). Source-linked views are the [layered flow and rule layers](README.md#four-layers-of-rules), the [client/agent delivery matrix](#required-rule-coverage-and-fallback), and the existing [rule register](../../docs/rules/register.yaml) and [generated rule page](../../docs/rules/RULES.md). The proposed per-rule coverage view is `proposals/agent-router/required-rule-coverage.json`, produced from that register and the actual native delivery traces; it does not yet exist. The diagram and layer table model this routing concern; deployment/domain-data views are omitted because this work changes neither. Reconcile these views, capability snapshots and trace requirements whenever a layer or contract changes. Elements and their required observations follow:
- **Rule entry** (changed): `docs/rules/register.yaml` gains `applies_when` (`always` | `roles` | `actions` | `intent`) and, for migrated rules, `migrated_from`. Run must show: the sort's output row per legacy id, and the register entry with its tag.
- **Injection event** (added): one line per hook firing in `~/projects/data/agent-router/inject-<date>.jsonl` (session id, agent id, tool, matched rule ids). Run must show: an event with the subagent's id, not only the parent's.
- **Router proposal** (added): one line per handoff in `router-<date>.jsonl` (job text hash, proposed subagent, rules, model, effort, actual choice). Run must show: proposal and actual choice for the same handoff id.
- **Outcome** (relied on): the feedback loop's records and check results, via `scripts/learning_loop/` (AES). Run must show: an outcome joined to a proposal by handoff id.
- **Specialist role** (relied on, owned by harness-context): run must show the proposed `subagent` value is one of the specialist names present in the client's agent list at that moment (logged with the proposal).
- **Model and effort selection** (relied on, owned by llm_client Plan #379; slice 4 only): run must show the selector's decision id and returned model and effort recorded beside the dispatched values.

Scope of this repository in the shared model: AES owns the rule register, disposition/coverage records, router/profile types and handoff accounting. Agent-skills owns native adapter registration and specialist definitions; llm_client owns model calls/selection. The diagram's cross-repository arrows describe these boundaries and do not imply AES owns the downstream runtime.

Additional AES model elements and explicit examined runs:
- **Effective profile:** the two-profile native dispatch run must show each resolved profile ID/digest, intersected caps/capabilities and actual role/field dispatch or fallback, joined to its handoff ID.
- **Required-rule coverage:** the four-cell ordinary/fallback run must show each applicable required rule ID, scope, observed delivery route before the action, deterministic gate result and fallback; an absent cell stays pending.
- **Handoff terminal status:** the observe-mode accounting run must show exactly one allowed terminal proposal status for each declared eligible ID, including failure reasons and missing-outcome indicators; inspect exact set membership and duplicates.
- **Canary outcome:** the frozen paired source-validation run must show task/check IDs, incumbent and candidate native session IDs, the actual returned artifacts and independent check outputs. A missing execution cannot supply a candidate outcome.

These are proposed AES extensions to existing log/consumer contracts, not implemented schemas or passing execution evidence in this planning checkpoint.

Concrete drift review `agent-router-model-source-review`: compare every README layer/record label and this matrix against the current register field names, adapter/profile/result schemas and the native versions/hashes in `evidence.json`; record the compared revisions and every discrepancy in `verification.log`. An absent contract or changed hash keeps the related view pending. The implementation adds `pytest tests/test_agent_router.py::test_model_views_match_contracts` to check schema field membership and exact four-cell view coverage at its merge gate. In the same change, reconcile PLAN, README, generated rule page, coverage view and evidence index; do not update a view's status merely because its input file exists.

## Authority and non-goals

> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).

**Authority:** Brian asked for this (2026-10-08: "yes", then "we can also use a system 1 model for choosing subagents, any additional injected context, model and effort level") and activated "finish all remaning work" on 2026-10-09. This grants ordinary reversible completion work under the existing design and limits; it does not grant new subscriptions, exceed stated spend caps, delete rules or bypass native custody. The implementation surfaces remain the AES rules register/router log and agent-skills adapters. llm_client Plan #379 owns model and effort selection; AES harness-context owns specialist definitions.

**Non-goals:** no second model selector; no edits to harness-context or llm_client files from this lane; no instruction shrinkage before required-rule coverage and four-cell delivery/fallback pass; no automatic routing based solely on the slice-3 log; no deletion of project-meta's legacy register; no outbound messages.

## Irreversible actions and spend

> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.

**Current execution:** finish the remaining reversible work under Brian's 2026-10-09 goal, following fresh plan adoption. Historical execution caps below are not increased or reset by this goal. Required planning verification uses the approved shared LLM route; new sort calls and new native-client funding require an available allowance or a new explicit grant. The paid Claude route question is pending; its subscription rejected the fresh canary with `usage_limit_reached`, with reset October 11 at 13:00 America/New_York. Preserve the logged refusal, and do not infer Claude child delivery from Codex evidence.

**Future execution spend:** model calls only, on the configured approved route through llm_client.
- Slice 1: one small-model call per legacy rule (263), and a second pass on disputed items; bounded at $5, authorized by Brian's "yes" (2026-10-08); contained by running once and caching each answer by rule id.
- Slice 3: one small-model call per handoff, about $0.001 each; authorized by Brian's "yes" (2026-10-08) up to $1 per day and $30 in total for the two-week log; any higher cap needs a new yes from Brian. Contained by the daily cap in the router, which stops proposing (and logs that it stopped) when reached.
- Slice 3b: first job set is exactly one paired, read-only source-validation job, `derived-project-workspace-views`, whose cached `tool_missing` retirement conflicts with currently existing linked tools. Execute one incumbent/manual choice and one proposed specialist choice against the same frozen source packet, at most two leaf executions. Brian's 2026-10-09 completion goal authorizes reversible native dispatch under an available subscription; paid API execution remains disabled until a separate explicit grant names this job and its maximum cost. The proposed maximum is $1 total, not an available allowance and not renewed sort funding. Record the grant and remaining cap before dispatch; a missing grant, unavailable subscription or cap exhaustion yields a terminal status without an execution. No broader comparison is authorized by this first job set.
- Slice 4: boundary $1 per day and $30 per month across router and selector calls; authorized only by a new yes from Brian when slice 4 is proposed; contained by the same daily cap in the router, which on reaching it falls back to the agent's own choice and logs the fallback, so a cap does not block ordinary work; required-rule delivery and protected-action gates still apply.

**Irreversible actions:** none. Legacy rules are copied, never deleted; the hook has an off switch; every change is a revertible commit.

## Uncertainties

> **CORE-UNCERTAINTIES** (blocking): The plan lists its material uncertainties, and each one has an owner or the evidence that would resolve it.

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether pre-tool hooks fire inside subagents in Claude Code and in Codex | Owner: this session; evidence: slice 2's first step, a real subagent transcript showing (or not showing) the hook's added context |
| Whether Plan #379's selector accepts coding-agent handoffs as a second consumer | Owner: llm_client Plan #379's Codex session (messaged msg_18a3dea8); evidence: its contract; until then slice 3 logs proposals without calling it |
| How many legacy rules survive the sort | Owner: this session; evidence: slice 1's output, every keep and retire read against its source |
| Whether injected rules are followed as well as rules in the big file | Owner: the feedback loop; evidence: recurrence counts per rule over the month after slice 2 |
| Router cost and latency per handoff | Owner: this session; evidence: llm_client call records for slice 3 |

| Whether routed choices hurt job outcomes once enforced (slice 4) | Owner: this session; evidence: slice 4's trace review of every failed or reverted job in its first two weeks |
| Whether Plan #379 exposes a consumer interface in time for slice 4 | Owner: Plan #379's Codex session; evidence: its merged interface; until then slice 4 routes subagent and rules only |

| Native delivery/fallback in each of four cells | Coordinator, with the current harness owner for its existing canary; resolving evidence: each ordinary and disabled/unavailable journey in `evidence.json` |
| Selector's actual accepted interface | llm_client owner `01a1124d-8de7-7d53-98c7-7b307b9b7ebe`; its 2026-10-09 committed-source check found Plan #379's learner unpublished. A merged typed API and supported pin resolve this; keep model/effort routing disabled meanwhile |
| Canary outcomes | Coordinator; resolving evidence: both frozen executions and independent source/result checks, not the router's recommendation |
| Effective profile behavior | Coordinator owns proposed `AgentRouterProfileV1` below; resolving evidence: both profiles' validated effective snapshots and actual native dispatch/fallback |

None of these execution uncertainties is settled by adopting this document.

## Activation facts

> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend.

All four activation facts are declared true: `shared_mechanism` (a hook every session loads and a register field other agents read), `empirical_comparison_proposed` (slice 3 compares the router's proposals with agents' actual choices to decide whether to build slice 4), `llm_central` (the sort and the router are model calls), `irreversible_or_spend_action` (model spend; no irreversible action). None is declared false.

Also declare `claims_external_standard=true`: the adapters implement externally owned native Claude hook and Codex agent configuration contracts identified below. This means checking those specific contracts, not claiming vendor certification. `aes_governed_target=true` follows from this repository's `.aes/target.yaml`; the AES target section records the current boundary.

## Prior art and ownership

> **OV-PRIOR-ART-DISPOSITION** (blocking): Existing ownership, internal lineage, and relevant external prior art were searched, and each candidate found is dispositioned as reuse, extend, compose, supersede, or bounded exception.

> **OV-PRIOR-ART-PARALLEL-CHECK** (advisory): The plan names one concrete structural check or consumer-path observation that would detect a silent parallel implementation of the same concern.

Searched: AES proposals and rules register; llm_client plans; project-meta ideas register (`vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md`); agent-skills hooks; Claude Code's native subagent and hook features; the external routers already reviewed by Plan #379.

| Candidate | Disposition | Reason |
| --- | --- | --- |
| llm_client Plan #379 System 1 model and effort router (with ParetoBandit, reviewed RouteLLM and LiteLLM auto-router) | reuse, pending merged API | It owns learned selection; 2026-10-09 source inspection found its learner uncommitted. Existing `core/model_selection.py` is static routing. No learned consumer or automatic model/effort choice is claimed until the owner lands the typed API |
| AES harness-context specialists | reuse | The role layer; the router chooses among them |
| AES rules register (#457) | extend | Add `applies_when`; it stays the one source |
| agent-skills Jev gate hook (rule M1) | compose | Same pre-tool hook mechanism, generalized to inject tagged rules |
| Claude Code skills (description-triggered loading) | compose | Already loads procedures on demand by intent; intent rules that are procedures stay skills |
| Claude Code Agent tool `subagent_type` / `model` / `effort` and Codex native agents | reuse | The router fills these fields; no new runtime |
| onto-canon sense router (ideas register: rules first, model for the rest) | compose | The router tries fixed matches first and calls a model only for the remainder |
| `vision/legacy/.../LOCAL_MODEL_AGENT_STRATEGY.md` (fixed model per role) | supersede | A static per-role model is replaced by #379's learned choice |
| project-meta policy register (263 rules) | bounded exception | Read only and migrated through the sort; not edited |

Structural check: `git grep -n "model_selection\|choose_model\|effort" -- 'scripts/rules' 'hooks'` in AES and agent-skills must return no selector code outside llm_client; inspect each hit: a second independent selection algorithm fails review; native field mapping, allowlists, logged selector outputs and references to llm_client are legitimate adapters/configuration, not a second selector.

## Capability reuse

> **CORE-CAPABILITY-REUSE** (blocking): Name catalogue reuse or a bounded residual with its first consumer.

The 2026-10-09 read of ACA canonical's `reuse_candidates.yml` found `approval_action_workflow`, `twitterapi_io_search_candidates_wrapper` and `documents_to_text`; `capability_registry.yml` exposes `core`, `approvals`, `notifications` and `scheduling`, including `state.transition.plan` and `approval.action.verify`. No catalogue entry fits, because this work needs source-supported rule applicability and native parent/child context delivery plus complete handoff/outcome accounting; those entries provide approval actions, search, document conversion, generic state transitions, notifications and appointments, not these agent-context or routing contracts. Do not introduce a parallel approval service: retain the existing native commit/claim/plan gates.

The bounded new capabilities extend the already selected owners: legacy rule disposition/applicability, first consumed by the AES register and `scripts/rules/build_rules_page.py`; required-rule delivery adapters, first consumed by the existing agent-skills client hooks/handoffs; and typed handoff accounting, first consumed by slice 3's observe-mode router and the existing feedback loop. Model/effort selection reuses llm_client Plan #379, never a second selector. Each new boundary is verified by that authentic consumer before promotion.

## AES target

> **OV-AES-TARGET-TRACE** (blocking): Map every requirement to existing target meaning and a verification subject; declare any target delta before governed implementation.

This plan changes none of `.aes/target.yaml`. Its current frontier changes legacy `scripts/rules/`, `docs/rules/` and proposal material outside the v0.2 governed roots declared in `.agentic/repo.yaml` (`src/agentic_engineering_system/` and `tests/greenfield/`), under Decision 0010's v0.1 disposition. It does not amend an accepted normative item or success criterion, and does not claim its adapter evidence completes an existing greenfield criterion. Any later implementation that needs a governed artifact or target change must first use `aes plan prepare/validate/accept`, with this exact adopted plan reference; no such delta is silently introduced by this adoption.

| Plan requirement | Existing normative item / criterion served | Existing target verification subject | Router-specific evidence |
| --- | --- | --- | --- |
| AR-OUTCOME | GF-REQ-007, GF-REQ-008 / SC-GF-007, SC-GF-008: adequacy and missing outcomes remain distinct | VS-GF-EVIDENCE, VS-GF-RECONCILE | Frozen canary tasks, both full execution traces and independent task checks |
| AR-PARITY | GF-REQ-005 / SC-GF-005: complete applicable context with provenance | VS-GF-CONTEXT-STRUCTURAL | Four native parent/child journeys, actual context and action outcomes |
| AR-FALLBACK | GF-REQ-005, AP-REQ-001 / SC-GF-005, SC-AP-001: context and deterministic commit controls | VS-GF-CONTEXT-STRUCTURAL, VS-AP-COMMIT-RULE | Required-rule inventory, disabled/unavailable delivery and protected-action gate results |
| AR-ACCOUNTING | GF-REQ-007, GF-REQ-008 / SC-GF-007, SC-GF-008: no insufficient state rendered green | VS-GF-EVIDENCE, VS-GF-RECONCILE | Exact eligible handoff-ID joins with every terminal failure and missing outcome retained |
| AR-PROFILES | GF-REQ-001, GF-REQ-005 / SC-GF-001, SC-GF-005: portable distribution and scoped context | VS-GF-DISTRIBUTION-INSTALL, VS-GF-CONTEXT-STRUCTURAL | Two independently configured effective profiles with real dispatch/fallback checks |
| AR-INVENTORY | GF-REQ-005 / SC-GF-005: applicable context with source provenance | VS-GF-CONTEXT-STRUCTURAL | Exact source/register membership and authentic generated-page consumer |
| AR-CONTRACT | GF-REQ-001, GF-REQ-005 / SC-GF-001, SC-GF-005: compatible distribution and context | VS-GF-DISTRIBUTION-INSTALL, VS-GF-CONTEXT-STRUCTURAL | Adapter-contract checks against native specimens and installed role/result schemas |
| AR-RECURRENCE | GF-REQ-007, GF-REQ-008 / SC-GF-007, SC-GF-008: adequate, fresh evidence | VS-GF-EVIDENCE, VS-GF-RECONCILE | Thirty-day full-trace feedback/delivery joins |

These existing verification subjects remain unchanged and are not substitutes for the named router evidence. The slice-1 inventory also serves GF-REQ-005/SC-GF-005 by retaining exact rule meaning/provenance; its verification subject is the actual register/page consumer and source-membership check. The two-week observation, field rollout checks and 30-day recurrence trace joins serve GF-REQ-007/GF-REQ-008 and remain pending until their own observations exist.

## Evaluation design

> **OV-EVAL-DECISION** (blocking): Name the decision and actions under each result.
> **OV-EVAL-IRREDUCIBLE-UNCERTAINTY** (blocking): State what existing evidence cannot resolve.
> **OV-EVAL-PARITY** (blocking): Compare candidates on the same eligible tasks and capability boundary.
> **OV-EVAL-COST** (blocking): Use the smallest check that settles the named decision.

**Observe mode (slice 3)** measures proposal validity, disagreement, operational reliability, latency and cost. An incumbent's executed outcome does not establish the counterfactual result of the router's unexecuted proposal. Agreement or a critic preferring a proposal can select canary cases; neither licenses automatic routing.

**Bounded reversible canary (slice 3b)** resolves whether a proposed field preserves the actual task requirements. Before execution, freeze a small representative set of reversible jobs, both candidate configurations, the starting commit/input state, independently runnable task acceptance checks, permitted outcome differences, maximum cases/spend and a stop/revert rule. Use existing task tests and consumer checks; do not invent a broad benchmark. Run incumbent and candidate in isolated existing worktrees/sandboxes with the same starting state and evidence. Keep both outputs and full traces. The independent evaluator uses the predeclared task checks and examines the resulting artifact; it is not the proposing router, the parent's agreement or the field's own confidence. Blind choice labels where an unavoidable judgment is used. Mark missing or non-comparable outcomes inconclusive, never successful. Run no canary under this document-only revision.

**Promotion decision:** a field whose candidate output fails task criteria, misses required context or regresses a predeclared material condition stays manual/observe-only. Acceptable independently checked outcomes permit a separate proposal for a limited reversible rollout of that field, with fallback and monitoring; they do not activate it. If all fields fail, keep the router observational. Slice 4 retains its separate authority/spend boundary. First principles and shadow traces cannot settle specialist effectiveness on this workspace's actual jobs; this small canary tests that remaining uncertainty directly.

**First frozen comparison:** the one paired `derived-project-workspace-views` source-validation job above can support only a source-investigation specialist choice. Freeze the current rule, all its source references, linked tool revisions and incumbent/proposed role configuration before dispatch. An independent deterministic checker verifies cited files/lines, actual linked-tool existence and valid result-schema membership; the coordinator then reads the full source-linked reasoning to ensure the disposition follows that evidence. Both executions must expose the same source packet and permission boundary. A failed or missing execution is inconclusive; stop after this pair rather than adding cases to obtain a favorable answer. It cannot certify UI, model, effort or all roles; those fields stay observational until a separately bounded real job checks them.

Existing evidence cannot resolve this decision: the cached sort contains the observed stale `tool_missing` answer, the harness canary tested another frozen investigation, and Plan #379's first consumer concerns OntoCanon rather than native source-investigation handoffs. Vendor docs and prior routers describe mechanisms, not these two choices' task outcomes. The pair is cheaper than a blind reversible rollout followed by correction because it uses two read-only leaf executions and existing source checks while avoiding cross-project adapter activation and any mandatory-context reduction. Its trace/check output directly decides whether to propose this one field; it is not a broad benchmark.

**Complete reliability accounting:** declare the eligible handoff set before observing results. For every eligible ID, record exactly one proposal status: `valid`, `invalid`, `capped`, `call_failed`, `input_unavailable` or `unsupported`. Unknown roles/rule IDs, malformed output and unsupported native model/effort values are unsuccessful proposals; log their concrete reason. Report each category and their sum against the same eligible membership, with duplicate/missing-ID checks. Retain invalid incumbent choices as a separate baseline-validity dimension; never remove the eligible job to improve a rate. A valid-pair disagreement rate may use a smaller named subset, but publish its membership and size beside total eligible reliability. Independently report dispatch fallback, unknown/missing outcomes, actual cost and latency for every attempt, including failures; an outcome coverage denominator is not a success denominator.

Minimum comparison parity requires the same task input, available evidence, selected policy profile, specialist/register snapshots and native capability list. Non-comparable cases stay visible with their reason. Fixed rules and mandatory gates are outside the learned choice and remain in force for both candidates.

## LLM call boundary

> **OV-LLM-CALL-BOUNDARY** (blocking): The plan describes the model call graph, the structured result boundary each call returns, and how calls are traced.

> **OV-LLM-AUTHORITY-PROMOTION** (blocking): The plan names the provider and spend authority for model calls and one authentic-run condition that must hold before the behavior is promoted.

Call graph:
- **Sort (slice 1):** for each legacy rule, one call: input is the rule's text, its source-document lines and the current AES register; output is a typed `LegacyDisposition` (disposition: covered | keep | retire, covered_by id or null, reason, cited source lines, applies_when). Disputed items (cited lines not found) get one second call on a larger model.
- **Router (slice 3):** at each handoff, one call: input is the handoff text, specialist list and register summaries; output is a typed `RouterProposal` (subagent, rule ids, model, effort, confidence). Rules matched by fixed patterns are added without a call.

All calls go through llm_client with Pydantic result models, so each is recorded in its `calls_<date>.jsonl` with prompt, response, model and cost; the router log stores the llm_client call id beside each proposal.

Provider: Brian's OpenRouter route (`OPENROUTER_API_KEY`) through llm_client; spend authority is Brian's "yes" (2026-10-08) within the bounds above. Promotion condition: the slice-3 log must be fully accounted for and read, the slice-3b candidate must execute and pass independent task checks, all applicable client/agent and fallback cells must pass, and slice-4 authority must exist. Shadow agreement alone cannot promote a field. Proposals carry the effective profile and client capability digests; unsupported choices are rejected before dispatch and remain reliability failures.

## Coordination

> **OV-COORD-OWNERSHIP** (blocking): Name exact ownership and conflict surfaces; claims control writes.

The completion coordinator is Codex session `01a11cac-2557-7dc0-8edd-8487ed5968d1`, claimed lane `agent-router-execution`, initially limited to `proposals/agent-router` for exact-plan adoption. The earlier document revision by `01a11cae-eadf-7192-9a72-ca2283a3ebc0` is complete. Its seven dirty `rules-sort` files remain a preserved handoff owned by that session until an explicit native transfer or retained-owner resume; the coordinator does not overwrite them or fence the shared app-server to obtain custody.

Implementation uses separate claimed lanes for AES rules/logs, agent-skills adapters, llm_client Plan #379's selector and harness-context's specialist contracts. The current harness owner `01a1198b-539e-7d32-8dc4-7fe62cc903d9` owns its native investigator canary; its parent/child traces do not claim disabled-injection fallback. Recheck all live owners and native contracts before writes. Each owned lane pushes its next expected evidence event and bounded deadline; on a missed event, make one runtime/claim probe and recover, reassign through explicit custody, or record the blocker. Claims alone never transfer authority. This coordinator owns integration of its completed slices.

| Writer / owned work unit | Exact conflict surface | Dependency and returned evidence |
| --- | --- | --- |
| Coordinator `01a11cac-2557-7dc0-8edd-8487ed5968d1`, current `agent-router-execution` | `proposals/agent-router/`; any later scope admitted natively before writes | Fresh receipt bound to exact PLAN, committed planning checkpoint, evidence index and integrated slice checks |
| Retained inventory owner `01a11cae-eadf-7192-9a72-ca2283a3ebc0`, `rules-sort` | The seven preserved files: `scripts/rules/{sort_legacy,build_rules_page}.py`, `tests/test_{sort_legacy,rules_page}.py`, `docs/rules/{register.yaml,RULES.md,legacy-dispositions.yaml}`; native claim must cover the seventh before writing | Depends on committed fresh adoption; returns exact source-ID membership, source-supported dispositions/tags, full trace reviews, authentic register/page checks and commit; no new sort calls |
| Harness owner `01a1198b-539e-7d32-8dc4-7fe62cc903d9` | `proposals/harness-context/native-parity`, `evidence.json`, `review-page` within harness-context | Returns native session/result evidence, installed contract hashes and permission observations; Claude quota refusal is not a pass. Root reads these before claiming router coverage |
| Coordinator `01a11cac-2557-7dc0-8edd-8487ed5968d1`, later AES router/log work unit | `scripts/rules/agent_router.py`, `contracts/agent-router/`, `tests/test_agent_router.py`; scope not yet admitted, no current write authority | Depends on adopted plan and inventory integration; returns typed event/schema checks, exact handoff-ID accounting, two profile dispatches and committed `evidence.json` references |
| Coordinator `01a11cac-2557-7dc0-8edd-8487ed5968d1`, later agent-skills adapter work unit | Existing client registration and adapter files, exact paths admitted in that repo first; no specialist-contract overwrite | Depends on source-supported register and existing specialist schemas; returns committed adapter checks plus four-cell ordinary/fallback transcripts and gate outcomes linked in `evidence.json` |
| llm_client owner `01a1124d-8de7-7d53-98c7-7b307b9b7ebe` | Plan #379 typed selector/outcome API, outside this lane | Returns merged API/version and authentic consumer contract; model/effort adapter waits for this evidence |

The native harness owner released shared `.company-planning` lifecycle paths after verified human-required CAS/retirement and narrowing; the root must separately admit those paths before starting its own cursor. No claim or runtime is fenced for this integration.

## Required-rule coverage and fallback

Before reducing always-loaded instructions, inventory **each required rule** by rule ID and applicable client/agent/action, then map its always-loaded/role/handoff/injection delivery, existing deterministic gate, expected transcript evidence and fallback. No unmapped rule or unobserved cell may be called covered. Retain the current instruction baseline until this inventory and all four authentic delivery/fallback cells pass, and any instruction-removal authority is separately satisfied. This revision removes no rule.

The probabilistic router cannot suppress required rules or grant permission. Reuse deterministic controls where the boundary is checkable: existing commit, claim, plan and publication/destructive-action gates stay in place. Injecting a reminder does not prove that a gate ran. If a hook is unsupported/disabled or a proposal is invalid, capped or fails, use the known baseline dispatch and deliver required context via the verified always-loaded/role/handoff route. If no verified route carries a required rule, retain the full baseline; if even that cannot satisfy a protected action's mandatory control, refuse that action with an explicit reason. Optional suggestions may be omitted with a logged fallback, never by weakening the selected profile's required controls. Exercise these paths in each client/agent cell and join the observed rule IDs and gate outcome to the handoff ID.

| Client | Agent | Required authentic evidence | Status in this revision |
| --- | --- | --- | --- |
| Claude Code | Parent | Seen rule IDs before the action; deterministic gate and disabled-injection fallback outcome | Planned, not run |
| Claude Code | Child | Child transcript/ID with the same delivery and fallback evidence; parent context is insufficient | Planned, not run |
| Codex | Parent | Native supported delivery route, seen rule IDs, gate and fallback outcome | Planned, not run |
| Codex | Child | Child transcript/ID proving delivery through the supported native or explicit handoff route, plus fallback | Planned, not run |

## Configurable colleague profiles

AES distributes reusable policy/configuration templates rather than Brian's personal paths or choices as engine constants. Extend the existing harness-context configuration and client adapters; llm_client remains the single model/effort selector. Define a validated effective profile with: enabled rule sets and required-rule floor; specialist allowlist/aliases; each client's supported model IDs, effort values and field mappings; approved provider route and daily/total caps; default manual/observe mode, permitted rollout fields, off switch and fallback; workspace/log roots resolved from environment or project configuration. A profile can narrow an existing grant but cannot authorize spend or an action the user has not granted.

Use two examples at implementation acceptance: Brian's selected policy/roles and a colleague's independent policy/roles and lower cap. Both must work without engine edits, user-name assumptions or copied secrets. Required controls are explicit for the selected profile and cannot silently disappear through an override. Resolve roles and model/effort support from the native client at dispatch; an unavailable alias or unsupported field produces a recorded failure and baseline fallback, never a fabricated equivalent. No hard-coded cross-client model-name equivalence is assumed. Log profile ID/digest, effective policy/register and specialist revisions, native client/capability snapshot and resolved caps with every proposal, dispatch and outcome so the behavior can be reproduced.

## Contracts and dependencies

> **OV-CONTRACTS-SCHEMAS** (blocking): For each system boundary the plan crosses, it names every schema or contract the crossing uses or changes, with its owner and its file or URL, and says whether this plan changes it.

> **OV-CONTRACTS-DEPENDENCIES** (blocking): The plan names the dependencies on each side of every boundary it crosses (what produces and what consumes each schema or contract) and the order in which the changes land so no consumer breaks in between.

| Boundary | Schema or contract | Owner | File | Changed here? |
| --- | --- | --- | --- | --- |
| Register → page, hook, router | `aes-rules-register/v1` | AES (this plan) | `docs/rules/register.yaml` | yes: adds `applies_when`, `migrated_from` (v1 stays readable) |
| Legacy register → sort | project-meta policy registry | project-meta | `policy/registry.yaml` | no (read only) |
| Claude → context adapter | `PreToolUse` stdin JSON; output `hookSpecificOutput.hookEventName=PreToolUse` and `additionalContext`; no permission grant in reminder output | Anthropic; registration owned by agent-skills | https://code.claude.com/docs/en/hooks#pretooluse | no native contract change; new adapter registration uses it only after live proof |
| Codex → context adapter | Native custom agent TOML `name`, `description`, `developer_instructions`, supported model/effort/sandbox fields; explicit handoff job/context through the native spawn tool | OpenAI; generated role owner agent-skills | https://developers.openai.com/codex/subagents ; agent-skills `contracts/specialists/development-investigator.v1.json`, `scripts/render_specialist_agents.py`, `distribution/agents/codex/development-investigator.toml` | no native/schema change; consume existing installed roles; do not assume a Codex hook can inject context |
| Specialist → parent | `DevelopmentInvestigationResultV1` and immutable role definition | agent-skills / harness-context | agent-skills `contracts/specialists/development-investigation-result.v1.schema.json` and `development-investigator.v1.json` | no |
| Hook → log | injection event line | AES (this plan) | `~/projects/data/agent-router/inject-<date>.jsonl` | yes (new) |
| Router → model | `call_llm_structured` with a Pydantic result model; records in `calls_<date>.jsonl` | llm_client | llm_client `llm_client/core/client.py` (`call_llm_structured`, line 627 on 2026-10-08) | no |
| Router → selector | Plan #379 future typed request/decision/outcome interface; unavailable in committed source, not inferred from plan prose | llm_client | `docs/plans/379_system_one_feedback_router.md`; current static `llm_client/core/model_selection.py` is not the learner | no; crossing disabled until merged API/pin supplied |
| Profile → adapters/router | Proposed `AgentRouterProfileV1`: rule sets/floor, specialist allowlist/aliases, native field maps, provider/caps, mode/off/fallback, portable roots; validated effective digest | AES (this plan), consumes immutable harness roles | Planned Pydantic type in `scripts/rules/agent_router.py`, schema `contracts/agent-router/profile.v1.schema.json`; examples under `proposals/agent-router/profiles/` | new, not implemented; does not change harness specialist schema |
| Router → log | router proposal, terminal status, effective profile and independent outcome references | AES (this plan) | `~/projects/data/agent-router/router-<date>.jsonl` | yes (new) |

| Boundary | Producer | Consumer |
| --- | --- | --- |
| Legacy register → sort | project-meta (unchanged) | this plan's sort job |
| Register → page, hook, router | this plan (sort writes, people edit) | `scripts/rules/build_rules_page.py`, the hook, the router, optionally harness-context |
| Claude → context adapter | Native Claude Code stdin event | Claude JSON context adapter implementing the hook contract above; unsupported routes remain explicit |
| Codex → context adapter | Native Codex spawn/handoff plus installed role TOML | Explicit handoff context/role configuration implementing the Codex contract above; unsupported routes remain explicit |
| Hook → log | the hook | slice 3 reading, the feedback loop's effects step |
| Router → model | the router (request) | llm_client (executes, records the call) |
| Router → log | the router | slice 3 reading, slice 4 trace review |
| Router → selector | llm_client Plan #379 (exposes the interface) | the router, slice 4 only |
| Profile → adapters/router | Profile author plus AES `AgentRouterProfileV1` validator resolves portable inputs and capability/cap intersection | Claude/Codex adapters and router read the same immutable effective snapshot; independent profile checks inspect dispatched values |
| Specialist → parent | Existing installed specialist and native runtime emit the schema-bound result and IDs | Parent/independent result validator joins it to the handoff and task checks |

Boundary-compatible landing order: (1) register consumers first accept optional `applies_when`/`migrated_from` without changing existing meaning; then the sort producer fills source-checked rows and page consumer checks them. (2) Land profile type/schema and validators before adapters/router consume an effective snapshot; invalid or unsupported options remain explicit failures. (3) Land typed injection/proposal/terminal-status/outcome consumers and ID-join checks before their producers append records. (4) Add disabled client registrations referencing existing role/result contracts, then prove all four ordinary/fallback journeys before enabling delivery; retain baseline instructions throughout. (5) Observe producers run with complete reliability accounting; execute the separately bounded canary only under its actual allowance, then propose supported fields without activating them. (6) The selector owner lands its typed API/version before any model/effort consumer binds it; absent that producer the crossing stays disabled. A separately authorized rollout follows proof, never schema installation alone.

## Standard conformance

The externally owned contracts are Claude Code's [native hook JSON contract](https://code.claude.com/docs/en/hooks#pretooluse) and Codex's [custom-agent TOML contract](https://developers.openai.com/codex/subagents), verified against installed Claude 2.1.295 and Codex 0.162.0 during the existing canary. These pages publish written field/type rules and examples, not a standalone machine-readable schema for these adapter crossings. Encode the used subset: Claude adapter accepts native session/tool/input identity, emits valid JSON with `hookSpecificOutput.hookEventName=PreToolUse` and string `additionalContext`, and never adds an `allow` permission decision; Codex role configuration has string `name`, `description`, `developer_instructions` and only capability-verified native model/effort/sandbox fields. Existing agent-skills role/result JSON schemas remain owned there and unchanged.

Machine-readable specialist rules live in agent-skills `contracts/specialists/development-investigator.v1.json` and `contracts/specialists/development-investigation-result.v1.schema.json`. Consume the installed immutable role's read-only, no-network, no-delegation capability floor. Validate returned `schema_version`, `task_id`, `specialist_id`, `status`, `root_cause`, `evidence`, `causal_chain`, `alternatives_ruled_out`, `limitations`, `recommended_parent_action` and `mutation_declaration` against that result schema, including its `supported`/`inconclusive`/`blocked` status enum; join task and specialist identities to the actual dispatched handoff, not just syntactic validity.

Planned `tests/test_agent_router.py` contract cases validate real native input/output specimens and generated effective profile mappings against those written rules. The merge gate runs `pytest tests/test_agent_router.py` as the explicit adapter-contract step, followed by the repository's local `make check`; no adapter merges without both commands passing. Native delivery/fallback journeys remain a separate activation gate because structural compatibility does not prove context delivery. Disproof includes any artifact labelled conforming that violates one of these named native rules. AES-only profile, coverage and event fields are explicitly labelled extensions in their schemas and records, never represented as native vendor fields; unsupported native options fail before dispatch.

Extensions in this plan: `AgentRouterProfileV1`, required-rule coverage, injection/router/accounting records and any AES-added role/type/field are AES extensions. Every addition beyond a native contract is labelled an extension both in this plan and in its generated artifact; no extra role, type or field is presented as part of the vendor standard.
