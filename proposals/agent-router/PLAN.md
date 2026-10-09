---
schema_version: "1.0"
artifact_type: design_plan
id: agent-router
status: proposed
prior_method_conformance_receipt: proposals/agent-router/receipt.json
revision_status: proposal-only; structural checks required; fresh semantic adoption pending
goal:
  outcome: "An agent starting or handing out a job carries only the rules, subagent, model and effort that job needs, chosen by fixed layers plus a fast model, with every choice logged and judged by outcome."
  canonical_example: "Brian asks for a dashboard page fix: the router log shows frontend then reviewer subagents, the UI rules injected, model and effort chosen; when the frontend agent runs gh pr merge the hook injects the three merge rules; the outcome row records whether the check passed."
  forbidden_substitutes: "A design page alone; a hook tested only on a fixture; router proposals never compared with what agents actually chose; a token saving estimated from file sizes; a second model selector beside llm_client Plan #379."
  boundaries: "AES rules register and router log, client-specific adapters to the existing hook/handoff mechanisms with an off switch; no edits to llm_client or harness-context files by this lane; the workspace instruction file stays unchanged until the required-rule coverage and four-cell injection checks pass; no outbound messages."
  done_when: "Slice 1: every legacy rule has a disposition and every kept rule an applies_when tag, checked against its source. Slice 2: real parent and child transcripts in both Claude Code and Codex prove delivery and mandatory-rule fallback. Slice 3: all eligible real handoffs over two weeks are accounted for in observe mode. Slice 3b: a separately authorized bounded reversible canary checks candidate and incumbent outcomes independently. Slice 4: automatic fields are proposed only from those outcomes and retain a verified fallback."
  do_not_gate_on: "Brian reading the review page; the Codex sessions finishing Plan #379 or harness-context; unrelated historical baseline failures recorded in AES #460; affected checks still apply."
---

# Agents get only the rules, subagent, model and effort each job needs

Design, diagram and the dashboard example: [README.md](README.md). This is a revised proposal. The 2026-10-08 receipt and generated goal describe the earlier plan digest only; they do not adopt these edits. The current [revision goal](revision.goal.md), [revision route](revision-path-decision.json) and [verification trace](verification.log) cover this document-only task. Fresh semantic re-adoption is required before executing changed slices; this revision makes no model calls, changes no runtime or rules, and grants no new spend.

## Actor and result

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

**Actor:** Brian, and every Claude Code and Codex agent working for him. **Result:** an agent carries only the rules its job needs, and work is handed to the right specialist on the right model and effort, chosen by a fast model and fixed layers rather than by habit.

**Example (stable, user-visible):** Brian asks for a broken dashboard page to be fixed. The router log (`~/projects/data/agent-router/router-<date>.jsonl`, one line per handoff) shows: subagent `frontend` then `reviewer`; injected rules `ui-tooltips-default`, `ui-index-first`, `red-green-colorblind`; model and effort for each. When the frontend agent runs `gh pr merge`, its own transcript shows the hook's added context naming the three merge rules. The outcome row for that handoff records whether its check passed or the change was reverted. The design and diagram are in [README.md](README.md).

## Requirements and checks

> **CORE-REQUIREMENTS-TRACED** (blocking): Each requirement names its check and pending or verified status; deferred execution remains visible on completion records.

The five corrections below are Brian-approved design requirements. Their **document checks** are the source diff and full editing/validation trace in `verification.log`; their **execution checks** remain planned, not run by this revision. A passing document check establishes that the obligation is stated, not that the router works.

| ID | Required behavior | Execution check and status |
| --- | --- | --- |
| AR-OUTCOME | Shadow agreement does not prove the outcome of an unexecuted choice. Require an independently checked, bounded reversible canary before proposing automatic routing. | Slice 3b's frozen task criteria, both execution traces and independent check outputs; planned, not run. |
| AR-PARITY | Rule delivery reaches real parents and children in Claude Code and Codex. | Slice 2's four-cell matrix below, including unavailable-injection fallback; planned, not run. |
| AR-FALLBACK | Required rules remain covered and protected actions retain deterministic checks when injection or routing fails. | Per-rule coverage inventory plus off-switch, missing-hook and missing-context journeys; planned, not run. |
| AR-ACCOUNTING | Every eligible handoff remains in the reliability denominator, including capped, failed, invalid and unsupported proposals. | Joined handoff membership and terminal statuses, with independently reported outcome completeness; planned, not run. |
| AR-PROFILES | Colleagues can configure policy, specialists, native model/effort capabilities and budgets without editing engine code. | Two independently configured profiles, portable paths, rejected unsupported options and recorded effective configuration; planned, not run. |

These requirements and their pending execution status must travel with every canary, promotion and completion record. No pilot or activation is required to finish this proposal revision.

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

## System model

> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: exempt -- <reason>`, which fits only a project with no stored state and no user-facing view. Unless exempt, the plan names each system-model element (entity, process, record or event, or view) that the work adds, changes, or relies on, and its trace review names, for each such element, what the examined run must show of it (for example an event of that record type with its id, or the view displaying that entity). A plan with neither a model link nor the exemption line fails this item, as does one that lists model elements without saying what the examined run must show of each, or one that names no element without stating that the work touches none and why.

Documentation entry point: [wiki/index.md](../../wiki/index.md) links [this proposal model](README.md). The diagram and layer table are a scoped model of the proposed routing concern, not the whole AES codebase. No complete AES model or live routing is claimed. The applicable views are the layered flow, client/agent delivery matrix and per-rule coverage inventory; deployment and domain-data views are omitted because this slice changes neither. Freshness check: reconcile PLAN, diagram, coverage inventory, client capability snapshots and trace requirements whenever a layer or contract changes; changed records require their existing schema/consumer checks. This revision reconciles PLAN and README together and retains verification evidence; implementation views and traces remain pending. Elements added, changed or relied on, and what the examined run must show of each:
- **Rule entry** (changed): `docs/rules/register.yaml` gains `applies_when` (`always` | `roles` | `actions` | `intent`) and, for migrated rules, `migrated_from`. Run must show: the sort's output row per legacy id, and the register entry with its tag.
- **Injection event** (added): one line per hook firing in `~/projects/data/agent-router/inject-<date>.jsonl` (session id, agent id, tool, matched rule ids). Run must show: an event with the subagent's id, not only the parent's.
- **Router proposal** (added): one line per handoff in `router-<date>.jsonl` (job text hash, proposed subagent, rules, model, effort, actual choice). Run must show: proposal and actual choice for the same handoff id.
- **Outcome** (relied on): the feedback loop's records and check results, via `scripts/learning_loop/` (AES). Run must show: an outcome joined to a proposal by handoff id.
- **Specialist role** (relied on, owned by harness-context): run must show the proposed `subagent` value is one of the specialist names present in the client's agent list at that moment (logged with the proposal).
- **Model and effort selection** (relied on, owned by llm_client Plan #379; slice 4 only): run must show the selector's decision id and returned model and effort recorded beside the dispatched values.

Additional proposed model elements: **effective profile** (profile/configuration digest and client capability snapshot), **required-rule coverage** (rule ID, scope, delivery route, deterministic gate and fallback), **handoff terminal status**, and **canary outcome** (task/check IDs and independent result). Their named profile, fallback, accounting and canary runs above must show the actual joined records. These are proposed extensions to the existing log/consumer contracts, not implemented schemas in this revision.

## Authority and non-goals

> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).

**Authority:** Brian asked for this (2026-10-08: "yes", then "we can also use a system 1 model for choosing subagents, any additional injected context, model and effort level"). The original implementation lane covered the AES rules register, router log and agent-skills hook. This proposal-only revision owns none of those runtime surfaces. llm_client Plan #379 (Codex session `codex:01a1124d…`) owns model and effort selection; AES harness-context (Codex session `codex:01a1198b…`) owns specialist definitions.

**Non-goals:** no second model selector; no edits to harness-context or llm_client files from this lane; no instruction shrinkage before required-rule coverage and four-cell delivery/fallback pass; no automatic routing based solely on the slice-3 log; no deletion of project-meta's legacy register; no outbound messages.

## Irreversible actions and spend

> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.

**Current revision:** proposal edits and offline structural checks only; no model calls, routing activation, rule removal or new spend. Historical execution caps below are not increased or renewed by this revision.

**Future execution spend:** model calls only, on the configured approved route through llm_client.
- Slice 1: one small-model call per legacy rule (263), and a second pass on disputed items; bounded at $5, authorized by Brian's "yes" (2026-10-08); contained by running once and caching each answer by rule id.
- Slice 3: one small-model call per handoff, about $0.001 each; authorized by Brian's "yes" (2026-10-08) up to $1 per day and $30 in total for the two-week log; any higher cap needs a new yes from Brian. Contained by the daily cap in the router, which stops proposing (and logs that it stopped) when reached.
- Slice 3b: the reversible canary is a proposed future step. Before executing, name its small job set, task checks, existing allowance and exact spend/dispatch authority; if the prior allowance does not cover it, obtain separate authorization. No spending or execution is authorized by this revision.
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

Still unresolved for execution: native delivery support for each client/agent cell, the selector's actual accepted interface, canary outcomes, and the effective profile schema at the owning configuration seam. Keep these visible; none is settled by this document revision or by another lane's historical status.

## Activation facts

> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend.

All four activation facts are declared true: `shared_mechanism` (a hook every session loads and a register field other agents read), `empirical_comparison_proposed` (slice 3 compares the router's proposals with agents' actual choices to decide whether to build slice 4), `llm_central` (the sort and the router are model calls), `irreversible_or_spend_action` (model spend; no irreversible action). None is declared false.

## Prior art and ownership

> **OV-PRIOR-ART-DISPOSITION** (blocking): Existing ownership, internal lineage, and relevant external prior art were searched, and each candidate found is dispositioned as reuse, extend, compose, supersede, or bounded exception.

> **OV-PRIOR-ART-PARALLEL-CHECK** (advisory): The plan names one concrete structural check or consumer-path observation that would detect a silent parallel implementation of the same concern.

Searched: AES proposals and rules register; llm_client plans; project-meta ideas register (`vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md`); agent-skills hooks; Claude Code's native subagent and hook features; the external routers already reviewed by Plan #379.

| Candidate | Disposition | Reason |
| --- | --- | --- |
| llm_client Plan #379 System 1 model and effort router (with ParetoBandit, reviewed RouteLLM and LiteLLM auto-router) | reuse | It already chooses model and effort and learns from checked outcomes; coding-agent handoffs become a second consumer |
| AES harness-context specialists | reuse | The role layer; the router chooses among them |
| AES rules register (#457) | extend | Add `applies_when`; it stays the one source |
| agent-skills Jev gate hook (rule M1) | compose | Same pre-tool hook mechanism, generalized to inject tagged rules |
| Claude Code skills (description-triggered loading) | compose | Already loads procedures on demand by intent; intent rules that are procedures stay skills |
| Claude Code Agent tool `subagent_type` / `model` / `effort` and Codex native agents | reuse | The router fills these fields; no new runtime |
| onto-canon sense router (ideas register: rules first, model for the rest) | compose | The router tries fixed matches first and calls a model only for the remainder |
| `vision/legacy/.../LOCAL_MODEL_AGENT_STRATEGY.md` (fixed model per role) | supersede | A static per-role model is replaced by #379's learned choice |
| project-meta policy register (263 rules) | bounded exception | Read only and migrated through the sort; not edited |

Structural check: `git grep -n "model_selection\|choose_model\|effort" -- 'scripts/rules' 'hooks'` in AES and agent-skills must return no selector code outside llm_client; inspect each hit: a second independent selection algorithm fails review; native field mapping, allowlists, logged selector outputs and references to llm_client are legitimate adapters/configuration, not a second selector.

## Evaluation design

> **OV-EVAL-DECISION** (blocking): Name the decision and actions under each result.
> **OV-EVAL-IRREDUCIBLE-UNCERTAINTY** (blocking): State what existing evidence cannot resolve.
> **OV-EVAL-PARITY** (blocking): Compare candidates on the same eligible tasks and capability boundary.
> **OV-EVAL-COST** (blocking): Use the smallest check that settles the named decision.

**Observe mode (slice 3)** measures proposal validity, disagreement, operational reliability, latency and cost. An incumbent's executed outcome does not establish the counterfactual result of the router's unexecuted proposal. Agreement or a critic preferring a proposal can select canary cases; neither licenses automatic routing.

**Bounded reversible canary (slice 3b)** resolves whether a proposed field preserves the actual task requirements. Before execution, freeze a small representative set of reversible jobs, both candidate configurations, the starting commit/input state, independently runnable task acceptance checks, permitted outcome differences, maximum cases/spend and a stop/revert rule. Use existing task tests and consumer checks; do not invent a broad benchmark. Run incumbent and candidate in isolated existing worktrees/sandboxes with the same starting state and evidence. Keep both outputs and full traces. The independent evaluator uses the predeclared task checks and examines the resulting artifact; it is not the proposing router, the parent's agreement or the field's own confidence. Blind choice labels where an unavoidable judgment is used. Mark missing or non-comparable outcomes inconclusive, never successful. Run no canary under this document-only revision.

**Promotion decision:** a field whose candidate output fails task criteria, misses required context or regresses a predeclared material condition stays manual/observe-only. Acceptable independently checked outcomes permit a separate proposal for a limited reversible rollout of that field, with fallback and monitoring; they do not activate it. If all fields fail, keep the router observational. Slice 4 retains its separate authority/spend boundary. First principles and shadow traces cannot settle specialist effectiveness on this workspace's actual jobs; this small canary tests that remaining uncertainty directly.

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

The document-only revision owner is Codex session `01a11cae-eadf-7192-9a72-ca2283a3ebc0`, lane `shaping/agent-router-review-corrections`, limited to this proposal's PLAN, README, revision goal/route and verification log. Brian authorized the five corrections. The frozen `rules-sort` lane's uncommitted implementation is preserved under an explicit dirty handoff; it is not part of this revision and is not claimed finished.

Future implementation still uses separate claimed lanes for AES rules/logs, agent-skills adapters, llm_client Plan #379's selector and harness-context's specialist contracts. Recheck their live owners and native contracts before assigning work; historical session IDs are lineage, not a current custody grant. No implementation owner is assigned new work by this revision. The revision's own integration owner is this Codex session.

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
| Client → hook | client-specific native hook input/context output or verified handoff-context route; no assumed parity | Anthropic; OpenAI; registration in agent-skills | https://docs.anthropic.com/en/docs/claude-code/hooks ; agent-skills `contracts/client-config/jev/codex-project-hooks.json` and `contracts/client-config/jev/jev-gate-hook` (the existing pattern) | no (a new hook entry is added beside Jev's) |
| Hook → log | injection event line | AES (this plan) | `~/projects/data/agent-router/inject-<date>.jsonl` | yes (new) |
| Router → model | `call_llm_structured` with a Pydantic result model; records in `calls_<date>.jsonl` | llm_client | llm_client `llm_client/core/client.py` (`call_llm_structured`, line 627 on 2026-10-08) | no |
| Router → selector | Plan #379 selector interface | llm_client | `docs/plans/379_system_one_feedback_router.md` | no (read; slice 4 only) |
| Profile → adapters/router | effective policy, role, native model/effort and budget configuration | AES / harness-context | existing harness-context configuration seam; exact schema chosen there before implementation | proposed extension only |
| Router → log | router proposal, terminal status, effective profile and independent outcome references | AES (this plan) | `~/projects/data/agent-router/router-<date>.jsonl` | yes (new) |

| Boundary | Producer | Consumer |
| --- | --- | --- |
| Legacy register → sort | project-meta (unchanged) | this plan's sort job |
| Register → page, hook, router | this plan (sort writes, people edit) | `scripts/rules/build_rules_page.py`, the hook, the router, optionally harness-context |
| Client → hook/handoff | native Claude Code and Codex adapters | verified same-client context delivery route; unsupported routes remain explicit |
| Hook → log | the hook | slice 3 reading, the feedback loop's effects step |
| Router → model | the router (request) | llm_client (executes, records the call) |
| Router → log | the router | slice 3 reading, slice 4 trace review |
| Router → selector | llm_client Plan #379 (exposes the interface) | the router, slice 4 only |

Landing order: (1) agree the effective profile/configuration seam and add optional register tags without breaking existing readers; (2) fill the source-supported sort and required-rule coverage inventory; (3) verify all four delivery/fallback cells before enabling an adapter, retaining baseline instructions; (4) run observe mode with complete reliability accounting; (5) separately authorize and run the bounded outcome canary; (6) propose only fields supported by canary outcomes for a separately authorized rollout. Model/effort fields depend on the selector's actual merged native consumer interface. This revision performs none of these runtime steps.
