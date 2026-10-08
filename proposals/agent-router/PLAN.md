---
schema_version: "1.0"
artifact_type: design_plan
id: agent-router
status: proposed
method_conformance_receipt: proposals/agent-router/receipt.json
goal:
  outcome: "An agent starting or handing out a job carries only the rules, subagent, model and effort that job needs, chosen by fixed layers plus a fast model, with every choice logged and judged by outcome."
  canonical_example: "Brian asks for a dashboard page fix: the router log shows frontend then reviewer subagents, the UI rules injected, model and effort chosen; when the frontend agent runs gh pr merge the hook injects the three merge rules; the outcome row records whether the check passed."
  forbidden_substitutes: "A design page alone; a hook tested only on a fixture; router proposals never compared with what agents actually chose; a token saving estimated from file sizes; a second model selector beside llm_client Plan #379."
  boundaries: "AES rules register and router log, one agent-skills pre-tool hook with an off switch; no edits to llm_client or harness-context files by this lane; the workspace instruction file stays unchanged until injection is proven; no outbound messages."
  done_when: "Slice 1: every legacy rule has a disposition and every kept rule an applies_when tag, checked against its source. Slice 2: a real Claude Code session and a real subagent each show the hook's injected rules in their transcript before a gh pr merge. Slice 3: two weeks of router proposals logged beside actual choices for real handoffs, read in full. Slice 4: decided from that log."
  do_not_gate_on: "Brian reading the review page; the Codex sessions finishing Plan #379 or harness-context; the 7 known AES distribution test failures (AES #460)."
---

# Agents get only the rules, subagent, model and effort each job needs

Design, diagram and the dashboard example: [README.md](README.md). This plan is the adopted-plan form of that design.

## Actor and result

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

**Actor:** Brian, and every Claude Code and Codex agent working for him. **Result:** an agent carries only the rules its job needs, and work is handed to the right specialist on the right model and effort, chosen by a fast model and fixed layers rather than by habit.

**Example (stable, user-visible):** Brian asks for a broken dashboard page to be fixed. The router log (`~/projects/data/agent-router/router-<date>.jsonl`, one line per handoff) shows: subagent `frontend` then `reviewer`; injected rules `ui-tooltips-default`, `ui-index-first`, `red-green-colorblind`; model and effort for each. When the frontend agent runs `gh pr merge`, its own transcript shows the hook's added context naming the three merge rules. The outcome row for that handoff records whether its check passed or the change was reverted. The design and diagram are in [README.md](README.md).

## Success and disproof

> **CORE-SUCCESS-DISPROOF** (blocking): The plan defines the evidence that would show success and a concrete condition that would disprove the approach.

> **CORE-TRACE-REVIEW** (blocking): Every success or acceptance criterion in the plan is judged from the full trace of a run, not only its final outcome: it names the run whose full trace is examined (for example the session, its tool and LLM calls, commits, check output, or messages), where that trace lives, and what must be seen in that trace beyond the final outcome. A criterion that names only an outcome, such as tests passing, a PR merged, a test fixture reproducing the journey, or a status reading succeeded, fails this item. A criterion for which no run exists, such as a pure document edit, passes only when the plan states that exemption and its reason explicitly.

**Success evidence:**
1. The sorted register: each of the 263 legacy rules carries a disposition (covered, keep, retire) with the source line that justifies it, and each kept rule an `applies_when` tag.
2. Hook injection observed in real transcripts, for a top-level session and for a subagent.
3. Router proposals logged beside actual choices for two weeks of real handoffs.
4. Over the following month, the feedback loop's recurrence count for rules moved from the instruction file to injection does not rise.

**Disproof:** the hook does not fire inside subagents and no native route makes it do so (then the action layer cannot reach subagents and the design changes to handoff-carried rules); or, in the two-week log, the router's proposals disagree with agents' choices in ways a reader judges worse in most sampled cases (then slice 4 is not built).

Each criterion is judged from a full run trace, not its outcome:
- **Slice 1 (sort):** the run is the sorting job (one model call per legacy rule through llm_client, traced in its `calls_<date>.jsonl`). Examine every `retire` and `keep` item's call: its input rule, the source document lines it cited, and the answer. A disposition whose cited lines do not exist in the source is a failure, whatever the count.
- **Slice 2 (hook):** the run is a real Claude Code session in this workspace that runs `gh pr merge` on a real PR, plus a subagent in that session doing the same in a test repository. Trace: the session JSONL under `~/.claude/projects/` and the subagent's own transcript. Must be seen: the hook's `additionalContext` naming the merge rules immediately before the merge call, in both transcripts. A hook unit test alone does not count.
- **Slice 3 (observe):** the run is every real handoff for two weeks. Trace: the router log line (job text, proposal, the agent's actual Agent-tool call) joined to the session transcript of that handoff and to its outcome. Read every disagreement and a sample of agreements.
- **Slice 4 (router chooses):** the run is every real handoff for the first two weeks after the switch. Trace: the router log line, the Agent-tool call it produced (subagent, model, effort as actually dispatched, read from the session JSONL), the subagent's transcript showing the injected rules at its start, and the joined outcome. Must be seen: the dispatched values equal the router's proposal for every routed field, and every failed or reverted job's trace is read to say whether the router's pick contributed.
- **Recurrence after injection (success criterion 4):** the run is the feedback loop's nightly collection and weekly problems run for the 30 days after slice 2 ships. Trace: `~/projects/data/feedback-collector/items-<date>.jsonl` and `problems-<date>.jsonl`, plus the injection log. For each new sighting of a mistake whose rule is now injected, read the source record and the session transcript it links, and check in the injection log whether the rule was injected into that session before the mistake. A count alone does not settle it: a recurrence where the rule was injected and ignored and one where it was never injected mean different things.

## System model

> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: exempt -- <reason>`, which fits only a project with no stored state and no user-facing view. Unless exempt, the plan names each system-model element (entity, process, record or event, or view) that the work adds, changes, or relies on, and its trace review names, for each such element, what the examined run must show of it (for example an event of that record type with its id, or the view displaying that entity). A plan with neither a model link nor the exemption line fails this item, as does one that lists model elements without saying what the examined run must show of each, or one that names no element without stating that the work touches none and why.

System model: the diagram and layer table in [README.md](README.md) are the model for this work (AES has no `docs/model/ODD.md`). Elements added, changed or relied on, and what the examined run must show of each:
- **Rule entry** (changed): `docs/rules/register.yaml` gains `applies_when` (`always` | `roles` | `actions` | `intent`) and, for migrated rules, `migrated_from`. Run must show: the sort's output row per legacy id, and the register entry with its tag.
- **Injection event** (added): one line per hook firing in `~/projects/data/agent-router/inject-<date>.jsonl` (session id, agent id, tool, matched rule ids). Run must show: an event with the subagent's id, not only the parent's.
- **Router proposal** (added): one line per handoff in `router-<date>.jsonl` (job text hash, proposed subagent, rules, model, effort, actual choice). Run must show: proposal and actual choice for the same handoff id.
- **Outcome** (relied on): the feedback loop's records and check results, via `scripts/learning_loop/` (AES). Run must show: an outcome joined to a proposal by handoff id.
- **Specialist role** (relied on, owned by harness-context): run must show the proposed `subagent` value is one of the specialist names present in the client's agent list at that moment (logged with the proposal).
- **Model and effort selection** (relied on, owned by llm_client Plan #379; slice 4 only): run must show the selector's decision id and returned model and effort recorded beside the dispatched values.

## Authority and non-goals

> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).

**Authority:** Brian asked for this (2026-10-08: "yes", then "we can also use a system 1 model for choosing subagents, any additional injected context, model and effort level"). This session owns the AES rules register, the router log and one agent-skills hook. llm_client Plan #379 (Codex session `codex:01a1124d…`) owns model and effort selection; AES harness-context (Codex session `codex:01a1198b…`) owns specialist definitions.

**Non-goals:** no second model selector; no edits to harness-context or llm_client files from this lane; no change to the workspace instruction file until slice 2 is proven; no router enforcement before the slice-3 log is read; no deletion of project-meta's legacy register; no outbound messages.

## Irreversible actions and spend

> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.

**Spend:** model calls only, on Brian's OpenRouter route through llm_client.
- Slice 1: one small-model call per legacy rule (263), and a second pass on disputed items; bounded at $5, authorized by Brian's "yes" (2026-10-08); contained by running once and caching each answer by rule id.
- Slice 3: one small-model call per handoff, about $0.001 each; authorized by Brian's "yes" (2026-10-08) up to $1 per day and $30 in total for the two-week log; any higher cap needs a new yes from Brian. Contained by the daily cap in the router, which stops proposing (and logs that it stopped) when reached.
- Slice 4: boundary $1 per day and $30 per month across router and selector calls; authorized only by a new yes from Brian when slice 4 is proposed; contained by the same daily cap in the router, which on reaching it falls back to the agent's own choice and logs the fallback, so no job is blocked by the cap.

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

This is the complete list for the four slices: the work adds a register field, a hook, two logs and one model call per handoff, and reuses the selector and specialists unchanged.

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

Structural check: `git grep -n "model_selection\|choose_model\|effort" -- 'scripts/rules' 'hooks'` in AES and agent-skills must return no selector code outside llm_client; any hit is a parallel model selector and fails review.

## Evaluation design

> **OV-EVAL-DECISION** (blocking): The plan names the specific decision that the proposed comparison or benchmark could change, and what would be done differently under each possible result.

> **OV-EVAL-IRREDUCIBLE-UNCERTAINTY** (blocking): The plan names the irreducibly empirical uncertainty the comparison resolves and explains why first principles and existing evidence or prior art cannot resolve it.

> **OV-EVAL-PARITY** (blocking): The plan states the minimum capability parity every compared candidate must meet before the comparison is meaningful.

> **OV-EVAL-COST** (blocking): The plan explains why running the comparison costs less than making a reversible choice now and correcting it later.

Decision: whether to build slice 4 (the router actually choosing subagent, rules, model and effort). If the router's proposals match or improve on agents' own choices in the slice-3 log, slice 4 is built for those fields. If they are worse for a field (for example model choice), that field stays with the agent and only the better fields are routed. If they are worse across the board, slice 4 is not built and the router stays a log.

Whether a small model, given only the job text and the list of specialists and rules, picks as well as the working agent does on Brian's real jobs. Prior art shows routers work for model choice on benchmark tasks (Plan #379's review), but not on this workspace's mix of jobs and specialists, and the specialists themselves are new. First principles cannot settle it because the answer depends on the actual distribution of Brian's jobs, how clearly agents write their handoffs and how distinct the new specialists turn out to be; none of these exist as data yet, and published router results measure model choice on benchmark tasks, not specialist choice on this workspace. Only real handoffs can show it.

Both sides see the same job: the router receives the same handoff text the agent wrote, the same specialist list and the same rules register at that moment. Minimum capability both must meet before a handoff counts: each side produces a complete, valid choice (a specialist name that exists, rule ids that exist in the register, a model on the allowed list, an effort level the client accepts). A handoff where either side falls short of that, or where the router lacked the input (cap reached, call failed), is logged and excluded, not counted as a disagreement.

The comparison is a log of decisions already being made, at about $0.001 per handoff and no extra agent work. Making the routing choice now without it would mean enforcing an unmeasured router on every job, where a bad pick costs a failed job or an over-sized model on many jobs; reverting that later is cheap, but the failed jobs are not.

## LLM call boundary

> **OV-LLM-CALL-BOUNDARY** (blocking): The plan describes the model call graph, the structured result boundary each call returns, and how calls are traced.

> **OV-LLM-AUTHORITY-PROMOTION** (blocking): The plan names the provider and spend authority for model calls and one authentic-run condition that must hold before the behavior is promoted.

Call graph:
- **Sort (slice 1):** for each legacy rule, one call: input is the rule's text, its source-document lines and the current AES register; output is a typed `LegacyDisposition` (disposition: covered | keep | retire, covered_by id or null, reason, cited source lines, applies_when). Disputed items (cited lines not found) get one second call on a larger model.
- **Router (slice 3):** at each handoff, one call: input is the handoff text, specialist list and register summaries; output is a typed `RouterProposal` (subagent, rule ids, model, effort, confidence). Rules matched by fixed patterns are added without a call.

All calls go through llm_client with Pydantic result models, so each is recorded in its `calls_<date>.jsonl` with prompt, response, model and cost; the router log stores the llm_client call id beside each proposal.

Provider: Brian's OpenRouter route (`OPENROUTER_API_KEY`) through llm_client; spend authority is Brian's "yes" (2026-10-08) within the bounds above. Promotion condition: the router may choose (slice 4) only after the two-week log of real handoffs has been read in full, with every disagreement classified, and the readout recorded in this plan.

## Coordination

> **OV-COORD-OWNERSHIP** (blocking): The plan names exact ownership, dependencies, conflict surfaces, the integration owner, and the work-unit evidence for each concurrent writer.

| Writer | Owns (conflict surface) | Depends on | Work-unit evidence |
| --- | --- | --- | --- |
| This session (claude-code, integration owner) | `docs/rules/register.yaml`, `scripts/rules/`, `proposals/agent-router/` (AES); one hook script and its registration in agent-skills; `~/projects/data/agent-router/` | the two below, read-only | commits on claimed branches, hook transcripts, router log |
| llm_client Plan #379 (codex:01a1124d…) | llm_client model selection and feedback store | none from this plan | its own plan and receipts; this plan reads its contract |
| AES harness-context (codex:01a1198b…) | specialist contracts and projections in agent-skills, `proposals/harness-context/` | register `applies_when` (optional) | its own plan; this plan reads its specialist list |

Integration owner: this session. Each slice is a separate claimed lane; no lane edits another writer's files.

## Contracts and dependencies

> **OV-CONTRACTS-SCHEMAS** (blocking): For each system boundary the plan crosses, it names every schema or contract the crossing uses or changes, with its owner and its file or URL, and says whether this plan changes it.

> **OV-CONTRACTS-DEPENDENCIES** (blocking): The plan names the dependencies on each side of every boundary it crosses (what produces and what consumes each schema or contract) and the order in which the changes land so no consumer breaks in between.

| Boundary | Schema or contract | Owner | File | Changed here? |
| --- | --- | --- | --- | --- |
| Register → page, hook, router | `aes-rules-register/v1` | AES (this plan) | `docs/rules/register.yaml` | yes: adds `applies_when`, `migrated_from` (v1 stays readable) |
| Legacy register → sort | project-meta policy registry | project-meta | `policy/registry.yaml` | no (read only) |
| Client → hook | Claude Code PreToolUse hook input and `additionalContext` output; Codex project hooks | Anthropic; OpenAI; registration in agent-skills | https://docs.anthropic.com/en/docs/claude-code/hooks ; agent-skills `contracts/client-config/jev/codex-project-hooks.json` and `contracts/client-config/jev/jev-gate-hook` (the existing pattern) | no (a new hook entry is added beside Jev's) |
| Hook → log | injection event line | AES (this plan) | `~/projects/data/agent-router/inject-<date>.jsonl` | yes (new) |
| Router → model | `call_llm_structured` with a Pydantic result model; records in `calls_<date>.jsonl` | llm_client | llm_client `llm_client/core/client.py` (`call_llm_structured`, line 627 on 2026-10-08) | no |
| Router → selector | Plan #379 selector interface | llm_client | `docs/plans/379_system_one_feedback_router.md` | no (read; slice 4 only) |
| Router → log | router proposal line | AES (this plan) | `~/projects/data/agent-router/router-<date>.jsonl` | yes (new) |

| Boundary | Producer | Consumer |
| --- | --- | --- |
| Legacy register → sort | project-meta (unchanged) | this plan's sort job |
| Register → page, hook, router | this plan (sort writes, people edit) | `scripts/rules/build_rules_page.py`, the hook, the router, optionally harness-context |
| Client → hook | Claude Code and Codex (send tool input) | the hook (returns `additionalContext` to the same client) |
| Hook → log | the hook | slice 3 reading, the feedback loop's effects step |
| Router → model | the router (request) | llm_client (executes, records the call) |
| Router → log | the router | slice 3 reading, slice 4 trace review |
| Router → selector | llm_client Plan #379 (exposes the interface) | the router, slice 4 only |

Landing order, so no consumer breaks: (1) `applies_when` added as optional, with the page builder updated in the same change; (2) the sort fills it; (3) the hook ships with its off switch defaulting to on only after it reads a tagged register; (4) the router ships logging only; (5) slice 4 calls the selector only after Plan #379 exposes a consumer interface.
