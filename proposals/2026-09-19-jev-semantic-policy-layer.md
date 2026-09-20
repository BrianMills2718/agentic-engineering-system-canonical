# Proposal: Jev-backed contextual policy and observability for AES

Date: 2026-09-19
Status: **PROPOSED — design and phased delivery proposal, not an accepted execution plan**
Baseline: canonical `cd3705cfa23e3fe40f6a34f56f211747bab36497`
Predecessor inspected: `Inside-Success/agentic-engineering-system@17ed0c5b10f04d88dc919a5b52bd2244c78134ac`

No runtime, hook installation, policy mode, dependency selection, or current plan status is changed by this proposal. No Jev requests, transcript replay, or machine tests were executed during preparation. The proposal is based on GitHub source inspection, retained predecessor evidence, the owner's direction in this conversation, and current public documentation. Existing implementations are not claimed freshly verified.

## 1. Outcome and owner intent

AES governs **agentic coding through policies, context delivery, observability, enforcement, and feedback**. The coding agents perform the engineering work. AES is not an autonomous actor that enters repositories.

The intended outcome is: Brian can delegate a real coding task in an AES-governed repository, inspect what the agent and policy mechanisms actually did, understand an intervention without reconstructing a transcript, and improve the system from the retained observations.

The direction proposed here is substantial use of Jev for contextual judgments throughout that loop, with adoption qualified separately for each use. The target is not merely a dangerous-command filter.

Owner preferences informing this proposal:

- Record everything the supported runtimes expose. Preserve existing Claude Code and Codex archives. Summaries and selected context are additional views, never replacements for originals.
- Recover prior policy, failure-mode, context, and observability work instead of inventing another policy system from scratch.
- Use model judgment where rigid hooks failed to interpret context. Keep exact facts and protocol mechanics in ordinary code.
- Support silent observation, warn-only, and configurable enforcement.
- Let the eventual feedback loop improve policies, context, skills, subagent strategy, routing, planning, verification, and its own evaluators.
- Use a repository already participating in AES governance. General legacy-repository onboarding is not the critical path of this program.
- Do not presume that predecessor or related repositories must become runtime dependencies. Distinguish ideas, adapted code, installed bootstrap mechanisms, and selected providers.

**Program sequence:** recover lessons → capture and replay → compare judgments → observe live → give useful advice → enforce selected policies → expand feedback and context adaptation.

## 2. What is established, and what remains a hypothesis

### Repository facts

Canonical already defines adaptive policy, meaningful error/unknown states, recovery on block, negative controls, append-only evidence, source-local context, and learning that changes future decisions. These are existing target requirements, not new inventions in this proposal. [R1]

Canonical also currently selects Company Planning and Enforced Planning as providers; `.agentic/repo.yaml` pins the Enforced Planning revision and installation provenance. The owner's expectation that these might be donors rather than enduring dependencies therefore needs explicit reconciliation. It would be inaccurate to call the present installation donor-only. [R1, R2]

The inspected predecessor has `PolicyTier.MEASURED` and `PolicyTier.BLOCKING`, a promotion request, negative-control and client-wiring observations, and a recovery action in its admission evidence. Its behavioral-rule model preserves problems, source text and exceptions. These are strong salvage candidates, not evidence that every original implementation should be copied. [R3, R4]

A retained September 1 hook recurrence record describes a Codex output-envelope problem, fresh-process testing, a configuration that did not hot-reload in an existing session, and insufficient correlation between hook completion and client parsing. Another predecessor module stores content-free hook receipts with hashes. A receipt alone is therefore neither the full raw input nor proof of the client's actual enforcement effect. [R5, R6]

The exact historical policy index needs further location/history tracing: fetching `policy/registry.yaml` at the inspected predecessor revision returned 404. References to a past registry are not proof that it remains at that path. Warn-only controls are documented in predecessor audit search results; silent shadow evaluation and visible warnings must remain separate behaviors.

### Jev facts, as documented on the research date

TypeSafe documents state plus typed Choice, Score, and Noul questions, with multiple questions evaluated in parallel. Jev does not generate prose or scripts. Code or a generative model must render explanations, author new questions, write scripts, or discover new failure descriptions. [W1, W2]

The models page lists `jev-1.13.0`, text-only input, 64k tokens per request, a 32k limit for state plus the longest question, published limits of 1,200 requests/minute and 250,000 tokens/second, and $0.042 per million input tokens with free output. Account-specific availability and limits still require an authenticated probe. [W3]

TypeSafe's 70–500 ms figures are vendor-reported, not measured AES latency or an SLA. Its known-limitations page explicitly notes literal interpretation, numerical/date weaknesses, indirection, distracting context, and inconsistent relationships between separately framed questions. Type correctness does not establish semantic correctness. [W4, W5]

Choice/Score `confidence` is derived from their distributions; it is not interchangeable with the probability of a particular violation. Noul has no separate confidence field. Thresholds must be evaluated per question type, policy, and model version. Parallel questions are not thereby statistically independent. [W5, W6]

The linked Reddit post is an anecdotal integration report. Its statement that Jev writes a script does not describe Jev's documented interface. Treat that as an unspecified surrounding implementation, not an API capability or verified benchmark. [W7]

**Hypothesis to test:** on representative AES decisions, a Jev-backed evaluator improves contextual discrimination enough to replace selected brittle policy predicates at acceptable end-to-end latency and cost, without weakening capture, recovery, or known exact controls.

## 3. Decisions proposed before implementation

### Preserve existing work; change priorities explicitly

Recommend recording Plan 001 as **paused, implementation-partial, not delivered**, at its existing evidence boundary, while this program becomes the proposed next priority. This proposal itself does not perform that transition or erase its outstanding verification and utility work. Reusable revision/evidence utilities may be salvaged without making legacy context resolution a prerequisite.

Adoption requires an explicit decision and reconciliation of the active-plan/frontier metadata. Review the existing external-dogfood and provider clauses rather than silently contradicting them. Derive the first execution-ready increment through the adopted planning process after the relevant target/current gaps and provider dispositions are accepted. [R1, R2]

### Separate long-term ownership from bootstrap dependence

AES owns its accepted policy semantics and lifecycle. For each predecessor mechanism record one disposition: idea donor, adapted code, temporary installed provider, selected continuing provider, replace, reject, or unresolved. Preserve working incumbent controls until an alternative has demonstrated the needed behavior. No wholesale Enforced Planning port, wholesale removal, or organizational repository convergence is assumed.

### Make Jev pervasive by use, not compulsory by architecture

Use one small evaluator interface and one initial Jev adapter. Compare against existing deterministic checks and an available small generative model. Prefer the documented TypeSafe SDK/direct API for the initial experiment; use a gateway only for a demonstrated availability or operational reason. TypeSafe and Vercel both document integration routes. [W2, W8]

Pin the explicit model identifier and actual SDK version used. Record the returned model identity and any inability to establish immutable provider identity. Do not silently carry an accepted policy evaluation across a `latest` alias change.

## 4. Gap-to-work mapping

These are proposed program gaps, not modifications to the existing gap ledger and not claims of complete estate inspection.

| Proposed gap | Existing AES target | Work that addresses it |
| --- | --- | --- |
| Contextual policy judgment is not qualified for Jev | AES-POL-001, AES-POL-004 | Historical comparisons, shadow evaluation, per-policy promotion |
| Hook completion does not necessarily prove client acceptance or effect | AES-POL-002, AES-POL-003, AES-EVID-001 | Versioned adapters, coverage map, actual client negative controls |
| Full causal joins between archives, supplied context, evaluations, and outcomes are not established | AES-EVID-001 | Raw capture audit, event identities, replayable evidence references |
| Context selection is not qualified against omitted-information failures | AES-CTX-002, AES-CTX-003 | Candidate logging, mandatory-context preservation, relevance evaluation |
| Feedback into policy/context changes is not an evidenced Jev-backed cycle | AES-LEARN-001 | Reviewed changes, shadow re-evaluation, scoped rollout and rollback |
| Owner intent and selected-provider/current-frontier records need reconciliation | AES-SYS-002, AES-SYS-004, AES-CAP-002 | Explicit disposition and priority decision; no silent dependency removal |

## 5. The runtime design

```text
Claude Code / Codex event
             |
             +--> durable original event and payload capture
             |
             +--> exact facts + source-linked context packet
                         |
                         +--> selected synchronous evaluation, only when needed
                         |      deterministic facts + Jev judgments
                         |      -> AES decision -> client-specific effect
                         |
                         +--> durable background analysis queue
                                classification, policy shadow tests,
                                context recommendations, feedback candidates

All evaluations, client effects, failures, recoveries, and later outcomes
join back to the original event. Review views are derived from that history.
```

A hook is the entry/exit connection to the coding client, not the place to hide the entire policy system. Keep that adapter small. Replacing a regex with Jev does not fix a missing trigger, malformed stdout, stale installation, or an unsupported client response.

Maintain separate fields for:

- **Judgment:** satisfied, violated, uncertain, not applicable, evaluation error, or unavailable.
- **Configured mode:** disabled, shadow, warn, or enforce.
- **Intended action:** continue, warn, hold/block, request an authorized decision, or initiate a bounded recovery.
- **Observed effect:** what the client actually accepted and what the tool actually did, including unknown or unsupported effects.

An uncertain judgment is not a clean bill of health. A model prediction cannot manufacture execution evidence or explicit user authorization. An existing exact prohibition cannot be overridden just because Jev returns a favorable score.

### Two execution paths

**Immediate path:** collect the necessary facts, evaluate only the policies that must act before this operation, then return a valid client response within a declared deadline. Batch independent questions that share state. Questions that depend on earlier answers require another stage or code composition; their answers cannot be referenced within the same independent batch. [W1]

**Background path:** persist an event first, then analyze it without waiting in the coding-agent path. Use an acknowledged queue or equivalent replayable cursor; crashes, retry exhaustion, and backlog are observable. Capture evaluator-origin events too, but do not recursively send every evaluator event back into the same trigger. Bound recursion, retries, and recovery loops.

Background judgments cannot retroactively prevent an action. Claude's own hook documentation explicitly distinguishes asynchronous observation from synchronous control. [W9]

### Modes and outages

| Mode | Normal effect | Evaluator unavailable |
| --- | --- | --- |
| Disabled | No semantic evaluation; raw capture continues | Capture continues |
| Shadow | Record a hypothetical judgment; no new warning or block | Record unavailable; leave incumbent behavior unchanged |
| Warn | Deliver concise advice without adding a block | Continue under existing controls and record the missed evaluation |
| Enforce | Apply the policy's accepted action and recovery contract | Follow its explicit bounded fallback: retain an existing exact gate, use a qualified fallback, or hold the particular protected action for recovery/escalation |

Do not make all coding stop because Jev is down. Equally, do not turn an unavailable required check into an implicit pass. A mode change must be visible and reversible.

## 6. Capture everything available; derive smaller working views

Inventory the existing transcript archives before building another collector. Preserve original bytes, source identities, timestamps, ordering information, and collector versions. Capture before truncation where the integration exposes that point. Record capture gaps explicitly where it does not.

Retain available prompts and messages, tool arguments/results, stdout/stderr, streaming chunks, file changes, Git state, context injection, skill and subagent activity, policy evaluations, warnings, blocks, overrides, recoveries, model requests/responses, token use, latency, and errors. Do not invent inaccessible model reasoning or claim that an archived transcript contains every hidden or internally assembled prompt.

Distinguish **available**, **selected**, **submitted to the runtime**, and **confirmed delivered** context. A file existing or being read does not establish that the model used it.

Use the existing archive as the first raw-data authority if it passes the capture/durability checks. Add normalized metadata and rebuildable indexes rather than duplicating every payload. Lossless compression and content-addressed deduplication preserve information; silent sampling or summary-only retention do not. Keep raw volumes in durable archive storage, with policies, code, provenance manifests, and selected evaluation evidence in GitHub. Do not leave the only meaningful copy on one laptop.

Minimum event/evaluation joins:

```text
event_id, parent_event_id, session_id, turn_id, tool_call_id
client/version, adapter/version, event time, ingest time, origin
repo/revision, worktree identity, dirty-state/diff or content digests
raw payload references and capture-completeness state
policy ID/version, mode, relevant exceptions and source references
context packet version/hash, candidate/selected/omitted source IDs
provider/model/SDK, exact questions and response, returned distributions
facts, judgment, decision-code version, intended effect, observed effect
attempts, latency breakdown, reported token usage, cost estimate
recovery, override, outcome and evaluation-label references
```

Coding naturally changes a dirty worktree. A commit SHA alone does not identify the action's actual input state: retain relevant diffs/content identities and recheck changed state before acting on a cached or delayed decision.

## 7. Recover the old work before rebuilding

Recover the previous policy index across current and historical revisions, behavioral rules, problems/failure taxonomy, exceptions, instruction renderer, hook receipts, hook-error records, promotion evidence, and observability readers. Start with the inspected files [R3–R6], then follow their references, including the archived `BrianMills2718/aes` when relevant.

For each candidate record what exists, the exact source, prior evidence, observed failure, and proposed disposition. Do not import a mechanism solely because it exists, or reject it solely because it is programmatic.

Classify hook failures into three useful categories:

1. **Judgment failure:** the rule misinterpreted a legitimate or problematic action. Jev may help.
2. **Integration failure:** the hook did not run, used the wrong payload/response, failed to reload, timed out, or was bypassed by an unobserved path. Adapter and execution tests address this.
3. **Policy-design failure:** the rule or exception was wrong, contradictory, or left no recoverable next action. The policy needs revision, irrespective of evaluator.

Preserve the distinction between an enduring failure/problem and a particular rule attempting to address it. A rare observed failure is not automatically obsolete: the control may be preventing it. Revisit policies through evidence, not rule-count targets.

## 8. Phased delivery

### Phase 0 — Reconcile scope and recover the first failure cases

Produce one bounded inventory and decision record, not an exhaustive rewrite of the estate. Select a small initial policy set from genuine failures. Suggested families, subject to recovered evidence: unsupported completion/verification claims; losing or overwriting work; a legitimate exception incorrectly blocked; plan/task drift; repeated unproductive recovery.

Check Jev access, model identity, SDK behavior, account limits, and a declared initial spending allowance before any paid runs. Identify the real archive locations and client versions during machine preflight. Freeze the policy meanings and comparison rubric before tuning prompts.

**Exit:** explicit active-frontier/provider disposition, selected evidence-backed policies, accessible corpus references, and an approved bounded first implementation contract. Unknowns stay visible rather than being filled with assumptions.

### Phase 1 — Archive replay and a usable case viewer

Import existing sessions without mutating originals. Construct decision-time packets containing only information available before the action. Preserve later results separately for labeling. Build a simple local case viewer/report that shows the original event, contemporaneous context, existing hook decision, eventual outcome, and evidence links.

A practical initial target is approximately 300 decision points from 20 or more sessions, if available, covering real failures and ordinary successful work. This is a debugging/evaluation starting point, not a statistically sufficient release certificate. Do not fabricate cases to meet a quota; report missing strata. Keep a representative natural sample separate from a deliberately failure-enriched sample.

Replay here means re-evaluating captured inputs. It must not re-execute historical shell commands or edits.

**Exit:** Brian can open a real case and understand what happened without reading the entire transcript; raw bytes remain recoverable; missing context is explicit; duplicate imports, crashes, and restart/resume are tested.

### Phase 2 — Compare Jev with what it would replace

Add the thin evaluator interface and Jev adapter. Run the existing predicate where available, Jev, and an available small generative model against equivalent packets. A strong reviewer may assist with labels, but agreement among models is not ground truth. Separate policy correctness, evaluator correctness, and client/infrastructure effects.

Retain every request, response, error, latency, and hypothetical intervention. Split development and held-out cases by session/task and time, not random neighboring transcript events. Preserve failed/uncertain cases and investigate confident mistakes. Do not let future outcomes enter the decision packet.

**Exit:** a per-policy comparison identifies which evaluator is useful, which cases need abstention/escalation, and which policies are not ready. Jev is allowed to lose a comparison; another use can still be qualified.

### Phase 3 — Live shadow operation

Run on real coding work in the canonical governed repo or another already-governed repo with a demonstrated reason to use it. Start with one client integration; qualify Claude Code and Codex separately before claiming both work.

Keep new semantic judgments silent and non-blocking. Durable raw capture precedes queued evaluation. Expose collector health, missing events, backlog, evaluator failures, estimated costs, and hypothetical actions in one review view.

Test the actual installed clients: ordinary command, shell-based edit, structured edit, subagent, interruption, resume, stale configuration, malformed evaluator response, unavailable provider, and recovery. Record client acceptance and effects, not only hook exit codes. Map uncovered tool paths and mark them as uncovered. Current Codex documentation explicitly notes tool coverage exceptions and unsupported response forms; do not assume client parity. [W10]

**Exit:** the adapters remain stable during genuine work, capture completeness is characterized, shadow adds no new blocking behavior, and observed false positives/negatives are reviewable.

### Phase 4 — Advisory policies and contextual assistance

Enable helpful warnings for individually qualified policies. Make warnings specific and actionable; suppress repeated UI noise without dropping the repeated raw events. Add one narrowly measured context use: recommend a relevant skill/instruction or select a compact view of a long tool result.

Preserve mandatory root/directory instructions and accepted policy precedence. Jev ranks optional context, not permission to discard authoritative requirements. Log candidate sets as well as selections so retrieval failures can be detected. Keep full output reachable; important errors and protocol structure must survive any reduced agent-facing view.

**Exit:** observed advice or context recommendations help real work, and omitted-information regressions are checked. No claim that context was used follows solely from it being delivered.

### Phase 5 — Selective enforcement with recovery

Promote one qualified semantic policy at a time, by policy version and client version. Keep exact predicates that already work. For each enforced policy require legitimate exceptions, deliberate violation cases, uncertain/missing-context cases, timeout behavior, actual client block evidence, a valid recovery path, and a tested switch back to the previous mode.

For work-loss prevention, recoverability and explicit scope/ownership facts remain necessary; a high Jev score cannot certify that unknown local changes are disposable. Bind a decision to the action and state it evaluated. Delayed or changed-state results require reevaluation, not stale permission reuse.

**Exit:** a genuine governed coding task includes a correct intervention and successful recovery without needless disruption, supported by source-bound evidence. This is not a blanket claim that all possible agent actions are controlled.

### Phase 6 — Broader context and feedback

Expand Jev qualification to policy applicability, output relevance, skill/subagent recommendations, plan-deviation detection, completion triage, failure classification, and recovery selection. Each use gets its own evaluation boundary; success at command-risk classification does not qualify completion judgment.

Use Jev to classify and prioritize retained events. Use code or a generative model to draft new policies, prompts, context strategies, and explanations. Preserve unknown/novel failure categories rather than forcing everything into an old taxonomy.

Initially, feedback creates a source-linked proposal/PR. Evaluate it on held-out cases, try it in shadow, apply it to a limited scope, compare outcomes, and retain an immediate rollback. Later automation may adjust explicitly authorized parameters within bounded ranges. It may not quietly rewrite its own authority or independently certify its own improvement.

**Exit:** at least one traceable observation changes a policy or context mechanism, the changed version is evaluated and exercised, and its effect is characterized. Feedback scope can later expand without pretending all dimensions are implemented now.

## 9. Evaluation and promotion standards

Use policy-specific measures, not one overall accuracy score. Measure missed violations, erroneous interventions on legitimate actions, exception handling, abstention and its frequency, context omission errors, client effect coverage, successful recoveries, human corrections, rework, latency, and spend.

Report the population and denominator. A failure-enriched test set estimates different things from naturally occurring activity. Sample some would-allow cases for review, not only flagged cases, or missed failures remain invisible. Correlated judgments across many policies can create cumulative warning/block burden; measure session-level interruption rate as well as per-policy rates.

A silent replay can establish what an evaluator would have said. It cannot prove that its proposed intervention would have prevented the later failure. Use live observation, controlled fixtures, and limited matched comparisons to investigate effects. Do not experiment by removing established protections from destructive operations.

Before promotion define a tolerable error envelope for the policy's consequences and collect enough representative labeled opportunities to support the claim. Small samples and zero observed errors are not proof of universal reliability. Keep ambiguity explicit. Do not transfer numeric thresholds between Noul and Choice or between model/question versions. [W5, W6]

Separate deployment tests from model-quality tests. Required deployment failures include unavailable provider, rate limit, timeout, malformed payload, stdout contamination, configuration not loaded, parser rejection, duplicate delivery, missing completion, race/stale state, disk/queue pressure, and recursive evaluator triggering.

## 10. Latency, cost, and operation

Record end-to-end overhead: client hook startup, context assembly, queue delay, network, inference, retries, decision computation, and client response. Model latency alone is not agent latency.

Starting budget proposals, to accept or revise before live enforcement: at most one synchronous model round trip for the initial qualified operation; a one-second total deadline for that semantic path; no inline retry storm; and a measured session-level overhead ceiling agreed from the baseline. Advisory/background work should not wait on inference in the tool path. Queue/budget exhaustion defers analysis with an explicit state; it does not silently discard raw history.

Illustrative provider-only arithmetic at the currently published price: 10,000 evaluations × 4,000 billed input tokens = 40 million tokens, or $1.68. At 100,000 such evaluations, $16.80. These are assumptions, not measured bills, and exclude retries, extra passes, gateways, fallback models, storage, and engineering cost. Use the API's actual token accounting and periodically compare estimated versus billed usage. [W2, W3]

For perspective, 1,000 serial checks adding 250 ms each would add 250 seconds. Heavy use should primarily mean broad capture, batched contextual judgments, and background evaluation—not a serial model call at every possible step.

Cache only against the complete relevant state, policy/questions, evaluator version, and evidence freshness. Do not reuse an action authorization after Git state, user instruction, scope, or evidence changes. Keep an inference kill switch and per-policy mode controls; capture remains independently operable.

## 11. Implementation shape and recoverable checkpoints

Proposed responsibilities, not precreated packages: client adapters; capture/archive integration; event normalization; context assembly; policy loading; evaluator adapters; deterministic decision handling; replay/evaluation; review projection; feedback proposals.

Use existing archive and provider mechanisms where fit is demonstrated. Prefer ordinary files, an existing durable queue, and a rebuildable index over a new distributed event platform for the initial single-operator deployment. Decide the concrete topology and contracts in the first accepted implementation plan, not by copying this heading list into empty directories.

Useful PR-sized checkpoints follow the phase boundaries: recovered cases and selected policy semantics; capture/replay with a case viewer; Jev comparison; live shadow adapters; advisory/context assistance; one enforcement policy; one feedback improvement. Tests and evidence accompany each. Do not accumulate all implementation as one uncommitted local change.

Machine-dependent implementation starts only after Remote MCP tool discovery, `devices_list`, execution-ready confirmation, and `devices_ping`; then inspect Git status and preserve existing changes. Use a branch/worktree, the guarded PowerShell-to-WSL path, and a real-repository coding agent when useful. Push coherent checkpoints before risky or long-running execution. This is execution procedure, not an AES dependency on Remote MCP.

## 12. Current unresolved prerequisites

- Authenticated Jev access, returned model identity, exact SDK version, account-specific limits, and first-run budget have not been checked.
- Archive location, capture completeness, backup durability, and runtime versions have not been inspected on Brian's machine.
- The full historical policy index and hook failure taxonomy have not been recovered; this proposal inspected targeted predecessor files and evidence.
- The exact small-model baseline, including what the owner's reference to Luna maps to in the available runtime, remains a selection task; no model ID is assumed.
- No Jev policy has earned enforcement, context-pruning, or automatic-policy-change authority yet.
- Main still has Plan 001 and the current provider bindings. This proposal recommends a deliberate next-priority decision, not a silent replacement.

## 13. Immediate next increment

After the proposal's scope/provider/frontier decisions are accepted, derive and execute the bounded **failure-case recovery + archive replay + first Jev comparison** increment. Preserve raw evidence from the outset and expose a usable case review early. Do not begin by rewriting every hook, building a general agent platform, or reorganizing non-AES repositories.

The first meaningful demonstration is: open a real past hook failure, show what was knowable at the time, compare the old predicate and Jev, explain any disagreement from the original evidence, and retain the result. The next is the same pipeline watching real coding work without obstructing it.

## Sources and evidence boundaries

Repository links are pinned to inspected revisions. Web documentation was accessed on 2026-09-19 and remains vendor documentation, not an AES execution receipt.

- [R1: Canonical system boundary](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/cd3705cfa23e3fe40f6a34f56f211747bab36497/docs/architecture/SYSTEM_BOUNDARY.md)
- [R2: Canonical repository/provider metadata](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/cd3705cfa23e3fe40f6a34f56f211747bab36497/.agentic/repo.yaml)
- [R3: Predecessor policy tiers and admission contracts](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/src/agentic_engineering/models.py)
- [R4: Predecessor behavioral rules and problem/exception lineage](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/src/aes/rules.py)
- [R5: Hook recurrence evidence and limitations](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/docs/evidence/codex-hook-recurrence-controls-20260901.json)
- [R6: Content-free predecessor hook receipts](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/src/aes/hook_receipts.py)
- [W1: TypeSafe introduction and parallel atomic questions](https://docs.typesafe.ai/introduction)
- [W2: TypeSafe API reference](https://docs.typesafe.ai/api)
- [W3: TypeSafe model IDs, pricing, and limits](https://docs.typesafe.ai/models)
- [W4: Jev launch, vendor-reported performance and evaluation caveats](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [W5: Jev 1.13 documented limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
- [W6: Confidence versus probability](https://docs.typesafe.ai/confidence)
- [W7: User-supplied Reddit experiment](https://www.reddit.com/r/AI_Agents/comments/1wkzjtx/i_tested_jev_as_a_subconscious_helper_for_my_ai/)
- [W8: Vercel Jev integration](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway)
- [W9: Claude Code hook reference](https://code.claude.com/docs/en/hooks)
- [W10: Codex hook reference](https://developers.openai.com/codex/hooks/)
