---
plan_id: second-brain-evaluation
status: shaping
method_conformance_receipt: proposals/second-brain-evaluation/conformance.receipt.json
planning_path_decision: proposals/second-brain-evaluation/PLANNING_PATH.json
goal:
  outcome: For the Inside Success second brain, each feature in the feature register shows whether it works today, whether people use it, and whether its answers are good, each reading backed by a reviewed run trace; the first measure (Tyler's positions from the June gold set) is fixed, traced and re-measured after the Slack retrieval fix.
  canonical_example: asked "someone from another department is trying to set up a meeting directly with one of our team members, what should we do?", Brian's assistant returns Tyler's 2026-06-16 Slack answer ("add me to DMs ... there is politics in this stuff") with its link, and the trace shows which search returned it
  forbidden_substitutes: a score without the traces of its failures read and classified; a gold answer that is not something Tyler said; a usage count that counts agents' tool calls as people's use; a search phrased with the gold answer's own words; posting to company Slack (ask_person_brain) without Brian's approval of the exact posts
  boundaries: pull requests to Inside-Success/brians-2nd-brain-integration-work, Inside-Success/Team-Brains and Inside-Success/2nd-brain-plan-repo plus this plan folder; deploys only through the transactional deploy scripts under the shared server lock, announced to session code-c1 first; code-c1's lanes (Brain value page, no-repeat, tracing and thumbs feedback, brain-decision routing) are not changed here
  done_when: the June gold set is fixed (every gold answer cites something Tyler said) and re-run before and after the #369 Slack retrieval change, with every miss's trace read and classified on Inside-Success/2nd-brain-plan-repo#358; Tyler's pilot pack runs with each case's trace classified (#357); a weekly per-person count of delivered answers and feedback exists that excludes agent tool calls (#360); and the feature register lists every feature with a dated works/used/good reading and the trace behind it (#362)
  do_not_gate_on: Brian reading this plan; Tyler confirming his pack; teammates' private usage beyond counts; code-c1's lanes
  owner: claude-code:second-brain-evaluation
---

# Second Brain Evaluation: Living Plan

**Authority:** Brian, 2026-10-08: "the fact that we basically dont know what works, what is used, and whether it is good for anything is really concerning"; "we need to document as issues and resolve throughout this conversation"; reading the trace "should be part of company planning and be enforced as part of the tests/success criteria for any step in the plan"; and, asked why the 22-question run had no plan, "if we are doing something like the 22 question run then there shouldnt there have been a plan for this?"
**Selected controls:** coordination (session code-c1 writes Team-Brains in the same area); shared runtime (the Inside Success server teammates use); continuity across sessions; spend (LLM judge calls; assistant turns).
**Artifact consumer / decision value:** Brian, to know which second-brain features to keep, fix or drop; the agents that continue the work.
**Execution profile:** continuous-coordinated
**Stage / investment boundary:** measurement for the existing system; no new product features beyond the #369 retrieval fix.
**Last outcome-bearing update:** 2026-10-08: first live gold-set run, 56-57% position accuracy (target 65%); traces classify the six lowest as three retrieval misses (#369), two gold-set flaws, one open (Inside-Success/2nd-brain-plan-repo#358).

## Outcome And Boundaries

<a id="outcome"></a>
**Outcome:** see the goal block. The measure is per feature: works today (a live check), used (counts of people's use, not agents'), good (graded answers), each reading tied to the run trace that produced it.

**Example.** Gold question G003 (above) failed on 2026-10-08. Its trace (session `20261008_105120_b52505`) shows four searches phrased in the question's words; Slack search is keyword-only and the governed passages do not hold the message, so the evidence never came back. After #369 the same question must retrieve it and the trace must show the search that did.

**Actor and recurring job:** Brian (and agents on his behalf) deciding whether the second brain is worth using and what to fix next.

**System model:** exempt: measurement over the deployed system; the feature register (M5) is the model.

<a id="canonical-probe"></a>
**Canonical probe:** Starting state: integration main 30c286dc (harness and adapter, #940); live gold-set run 2026-10-08 at 57%. Action: the active slice. Inspectable result: G003 retrieves Tyler's message by meaning, and the trace shows it.

<a id="success-disproof"></a>
### Success Evidence

Each criterion names the run whose full trace is examined, where that trace lives, and what must be seen in it beyond the final outcome (Policy read-the-trace; Company Planning CORE-TRACE-REVIEW).

1. *Gold set fixed and re-measured.* Run: `plan/eval/eval_runner.py` through `brain_retrieve_adapter.py` before and after #369, plus the harness controls (fake perfect, fake degraded). Trace: each question's assistant session in hermes-host `state.db` read with `plan/eval/brain_trace.py`, and the run's `brain_answers.jsonl`; results posted on #358. Must be seen: for every question scored below 0.7, whether the gold evidence never came back, came back unused, or the gold answer is wrong; controls pass and fail as expected.
2. *Slack positions findable by meaning (#369).* Run: the G003, G005 and G010 questions in their own words after the change. Trace: their sessions in `state.db`. Must be seen: the search call whose result contains Tyler's message, not only a correct final answer.
3. *Tyler's pilot pack (#357).* Run: each case, with its real item filled in, through the adapter. Trace: each session in `state.db`, recorded per case on #357. Must be seen: per case, the evidence returned and how the answer used it; isolation cases show the refusal and that the private fact was never retrieved.
4. *Usage (#360).* Run: the weekly count for one past week. Trace: the usage ledger rows it counts (event kinds per person), recorded on #360. Must be seen: delivered answers and feedback counted per person, and agents' `direct_retrieval` calls excluded.
5. *Feature register (#362).* Run: the scheduled register refresh. Trace: each feature's probe output and the session or log it read, linked from the register. Must be seen: per feature, the dated check, its trace link, and a failure opening a concern.

**Disproof:** the approach is wrong if after the #369 change the gold set's retrieval misses remain (the traces still show Tyler's Slack evidence never returned) or the re-measure moves less than the number of fixed misses explains; or if per-feature usage cannot be separated from agents' calls in the ledger. Run and trace for each: criterion 1's re-run sessions, and criterion 4's ledger rows.

<a id="non-goals"></a>
**Non-goals:** new assistant features; Tyler-ness scoring (Brian, 2026-10-08: "the sounds like tyler is not something we need right now"); changing who answers brain decisions (code-c1's lane, decided by Brian 2026-10-08); posting to company Slack.

## Architecture And Capability Invariants

<a id="shared-mechanism"></a>
- Measurements read existing records (hermes-host `state.db` sessions, the usage event ledger, brain run records); nothing records less than today.
- The harness keeps exit codes 0 pass / 1 below threshold / 2 incomplete.
- Every scored item carries its session ID so its trace can be read.

## Milestone Horizon

| Milestone | Planning state | Inspectable output / stable boundary | Required capability and evidence | Promotion or replan trigger |
|---|---|---|---|---|
| E1 Gold set honest (#358) | fully_specifiable_now | every gold answer cites a Tyler statement or is dropped with its reason; all misses traced | brain_trace.py; source search | promote when criterion 1's pre-change half holds |
| E2 Slack by meaning (#369) | exploration_required | G003/G005/G010 retrieve by meaning; gold re-measure | prior-art choice (below) | replan if disproof fires |
| E3 Tyler's pilot pack (#357) | conditional | per-case results with traces | E1 harness | after E1 |
| E4 Usage counts (#360) | conditional | weekly per-person delivered-answer and feedback counts | ledger; coordinate with code-c1's thumbs feedback | after code-c1 confirms its feedback events |
| E5 Feature register (#361/#362) | deliberately_deferred | register with dated works/used/good per feature | E1-E4 | after E4 |

## Active Slice

E1: re-source or drop G009 and G017 (gold not something Tyler said), trace G004 (source not found), then trace every question scored below 0.7 and post the classification on #358.

## Coordination

**Owners and claimed paths:** this plan's agent (claude-code session code-15): `plan/eval/` in Inside-Success/brians-2nd-brain-integration-work, the #369 retrieval change wherever it lands, `knowledge/storage/weekly_usage.py` in Team-Brains for E4, and issues #357, #358, #360-#362, #369. Session code-c1: Team-Brains `knowledge/mcp_server/brain_value.py` (#651), the no-repeat change (#652), tracing and thumbs feedback (RV-T1/T3), and brain-decision routing (`brain_proposals.yaml`, the self_file path).
**Dependencies:** E4 counts code-c1's thumbs feedback events once they exist; E2 may change the structured-source or shared-evidence services that code-c1's tracing reads.
**Conflict surfaces:** Team-Brains `main` (both sessions merge there); the `team-tools`, `shared-evidence` and `structured-source` containers (both deploy); the shared deploy lock on the server.
**Integration owner:** this plan's agent (`claude-code:second-brain-evaluation`) is accountable for integrating this plan's work end to end: its pull requests merge only after their tests match main, it announces each deploy to code-c1 before taking the shared lock, and it reconciles any Team-Brains change that touches both lanes. code-c1 integrates its own lanes. A Team-Brains change touching both lanes' files waits for the other session's agreement.
**Work-unit evidence:** per milestone, its issue (#357, #358, #360, #361, #362, #369) and the pull requests that close it; for code-c1, Team-Brains #651, #652 and its RV-T1/T3 pull requests.
**Reporting:** each lane posts its result on its issue; deploys are announced to the other session before taking the shared lock.

<!-- goal-authority-reversion:v1:start -->
```yaml
schema_version: "1.1"
owner: "claude-code:second-brain-evaluation"
receiver: "claude-code:recovery"
transfer:
  trigger: "explicit_handoff"
reporting:
  event: "result posted on the milestone's issue"
  deadline: "PT4H"
  one_probe_transition: "block"
non_gating_utility_review:
  broad_cycle_limit: 2
  on_limit: "compare_direct_route_and_merge_or_defer"
  later_review: "exact_counterexample_only_unless_scope_expands"
```
<!-- goal-authority-reversion:v1:end -->

## Evaluation Design

<a id="evaluation"></a>
**Decision it changes.** The before/after gold-set run around #369 decides whether the chosen Slack retrieval change stays deployed. If G003, G005 and G010 now retrieve Tyler's messages (seen in their traces) and position accuracy rises by about the number of fixed misses, it stays and E3 proceeds on it. If not, it is rolled back and the other approach (ingesting Slack positions into the governed passages) is tried instead.

**Irreducible uncertainty.** Whether a meaning-based search over this company's Slack actually returns Tyler's short, informal messages for questions phrased in other words. That depends on how the embedding model handles this corpus (slang, threads, very short posts); neither first principles nor prior art on other corpora settles it, and the existing evidence (three traced misses) only shows the current keyword search fails.

**Parity.** Minimum every compared run must meet before its score counts: the adapter returns an answer and a session ID for all 22 questions (0 errors); the harness controls pass (fake perfect PASS, fake degraded FAIL) in the same session; the retrieval services the assistant calls (`structured-source`, `shared-evidence`) are healthy at run time; and every miss below 0.7 has its trace read. Beyond that, both runs use the same 22 questions at the same fixed gold-set revision, the same adapter route (`ask_my_brain`, owner read-only), the same judge model and `reasoning_effort`, and the harness controls passing (fake perfect PASS, fake degraded FAIL) in the same session.

**Cost.** One run is about $0.05 of judge calls and about 12 minutes of assistant turns. The alternative, choosing one approach now and correcting it later, is cheap to reverse (a redeploy of the previous commit, about 2 minutes) but expensive to detect: without a measured before/after, a retrieval regression shows only as worse answers to every teammate, and finding it later means running this same comparison anyway, after the damage, plus tracing which answers it affected. So the run costs the same as the detection a later correction would need, and less than the harm in between.

## Model Calls

<a id="llm-calls"></a>
**Call graph.** (1) The adapter calls the team MCP tool `ask_my_brain` once per question; the assistant runs one agent turn with its knowledge tools and returns JSON (`answer`, `session_id`, `mirror`, `tools_used`). (2) The runner makes one structured judge call per question through `llm_client.call_llm` with a JSON schema (`score`, `explanation`). No other model calls.
**Tracing.** Assistant turns: every tool call, argument and result in hermes-host `state.db`, read by session ID with `plan/eval/brain_trace.py`. Judge calls: `llm_client` call logs under the run's `trace_id` (`eval-<id>-<qid>-acc`), one JSON line per call.
**Provider and spend authority.** Judges go through `llm_client`'s `judging` profile on OpenRouter (`OPENROUTER_API_KEY`), bounded to about $1 per run; assistant turns use the team's configured model on the team's budget. Spend authority: Brian (agent spend approved for this work, 2026-10-07/08).
**Authentic-run condition before promotion.** A score is reported only from a full live run whose harness controls pass in the same session and whose every miss below 0.7 has had its trace read and classified; this held for the 2026-10-08 run.

## Boundaries

<a id="boundaries"></a>
| Boundary | Owning authority | Rollback or containment | Disposition |
|---|---|---|---|
| Deploys to the shared Inside Success server (159.195.19.181) | Brian (deploys his own work; Dagim also deploys) | `deploy-integration-runtime.sh` / `deploy-team-tools.sh` restore the prior pair on any failed check; redeploy the previous commit to roll back | proceed, announced to code-c1, under the shared lock |
| Posting to company Slack (`ask_person_brain` mirrors every exchange) | Brian | containment: the adapter calls only `ask_my_brain` (owner read-only; each reply reports "not mirrored", checked per answer in `brain_answers.jsonl`), and has no code path to any posting tool; a run whose log shows `mirrored: true` stops and is reported to Brian, since a Slack post cannot be unsent | excluded unless Brian approves the exact posts |
| Teammates' usage data (E4) | each person's own data | counts only, per person, no query or answer text | proceed with counts only |

## Decisions And Assumptions

<a id="uncertainties"></a>
The three uncertainties below are material: each can change which milestone runs next or whether its result counts (the #369 approach decides E2's deploy; the pack's validity decides whether E3 measures what Tyler wants; separable usage decides whether E4 can exist at all).

| Item | Kind | Owner or resolving evidence |
|---|---|---|
| Which #369 approach (meaning-based Slack search vs ingesting Slack positions into governed passages) | open | E2 prior-art review, then a before/after on G003/G005/G010 traces |
| Whether Tyler's pack still reflects what he wants tested (he marked it superseded 2026-07-17) | assumption | Owner: this plan's agent. Resolving evidence: his replacement, `FOUNDATIONAL-ROLLOUT-MAP.md`, read for test cases before E3 (on 2026-10-08 it had readiness criteria and none), and Tyler's own reply if Brian chooses to ask him (not gating). |
| Whether the ledger can separate people's use from agents' | open | E4: the event kinds in Brian's own weekly report (direct_retrieval vs answer_delivered) |

## Evidence And Current State

- Gold-set run and traces: Inside-Success/2nd-brain-plan-repo#358, #369.
- Harness, adapter, trace reader: Inside-Success/brians-2nd-brain-integration-work#940.

## Human Decisions

None pending for E1-E2.

## Exact Next Action

E1 active slice (above).

## Prior Art And Parallel-Implementation Check

<a id="prior-art"></a>
Searched on 2026-10-08: existing owners (Team-Brains `evals/`, integration `plan/eval/`, grounded-research's Eval-R), internal lineage (the June lil-tyler gold set and its harness), and external evaluation frameworks (promptfoo, RAGAS, DeepEval, LangSmith evaluations). Disposition of each:

| Candidate | Category | Disposition |
|---|---|---|
| integration `plan/eval/eval_runner.py` + `gold_set.json` (June, lil-tyler) | internal lineage | **reuse** (fixed and controlled 2026-10-08, #940) |
| integration `plan/eval/foundation_wiki_task_evaluation_*` | existing owner | **bounded exception** (left with its owner): it grades wiki task cards, not answers about a person's positions; revisit if E5 measures the wiki |
| Team-Brains `evals/attribution` (who-said-what, 19/20 on 2026-07-13) | existing owner | **reuse** as the attribution measure in the feature register (E5) |
| Team-Brains `evals/BETA_QUESTION_SUITE.md`, `evals/hive-brain` | existing owner | **extend**: candidate question sources for E3/E5; Hive Brain's suite stays its owner's |
| grounded-research Eval-R | existing owner | **bounded exception** (left with its owner): it grades research reports, not the assistants; revisit if E5 adds research answers |
| promptfoo, RAGAS, DeepEval, LangSmith | external | **bounded exception** (not adopted): the reused harness already scores this contract with passing controls, and a framework switch adds setup without changing any decision for 22 questions; revisit when E5 needs more than three suites |

- **Evaluation harness:** reuse the existing June harness (`plan/eval/eval_runner.py`), fixed and controlled 2026-10-08, rather than adopt promptfoo or RAGAS: it already scores this contract and its controls pass; a framework switch buys nothing for 22 questions.
- **Traces:** reuse hermes-host `state.db` sessions (every tool call, argument and result is already recorded); no new tracing store. code-c1's tracing lane (RV-T1) is the place for any trace UI.
- **#369 retrieval:** meeting transcripts already have hybrid (meaning plus keyword) search; extending the same approach to Slack is the first option to evaluate before any new index.

<a id="parallel-check"></a>
**Parallel-implementation check:** code-c1's thumbs feedback (RV-T3) is the feedback source for E4; this plan counts it, it does not build a second feedback path.

## Activation Facts

<a id="activation-facts"></a>
shared_mechanism true (the harness and register are reused by other agents); empirical_comparison_proposed true (before/after #369); llm_central true (assistant answers, LLM judges); irreversible_or_spend_action true (judge spend, deploys).

<a id="route"></a>
## Route

coordinated (PLANNING_PATH.json): another session writes the same Team-Brains area and the server is shared.

<a id="irreversible-actions-and-spend"></a>
## Irreversible Actions And Spend

- **Spend:** judge calls about $0.05 per 22-question run (cap about $1 per run); assistant turns about 30 s each on the team's model budget. Boundary: only the runs this plan names. Authorized by Brian (agent spend for this work, 2026-10-07/08); any run beyond them, or above the cap, needs his approval first. Contained by the per-call `max_budget` in the harness.
- **Deploys:** reversible (transactional scripts with rollback), under the shared lock, announced to code-c1.
- **Company Slack:** boundary: any call to `ask_person_brain`, which mirrors each exchange into the company brain-to-brain channel as Brian. Authorized only by Brian, per exact post. Contained by using `ask_my_brain` (owner read-only, "not mirrored") for every run; the adapter calls no other brain tool.
