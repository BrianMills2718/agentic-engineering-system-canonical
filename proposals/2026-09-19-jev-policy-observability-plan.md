# Proposal: Jev-backed AES policy intelligence and full-fidelity observability

Status: **DRAFT PROPOSAL — not an accepted implementation plan or runtime-provider selection.**

Prepared: 2026-09-19. Canonical baseline: `cd3705cfa23e3fe40f6a34f56f211747bab36497`. Principal predecessor inspected: `Inside-Success/agentic-engineering-system@17ed0c5b10f04d88dc919a5b52bd2244c78134ac`.

This records Brian's requested direction and a proposed implementation sequence. It does not install hooks, call paid inference APIs, change active policies, replace Enforced Planning, close Plan 001, or establish current runtime conformance. Research consisted of GitHub source inspection and public documentation; Brian's installed clients, transcript archive, credentials, and local processes were not inspected or executed.

## 1. The intended result

AES governs agentic software engineering through policies, context, observation, enforcement, and feedback. Claude Code, Codex, and their subagents do the engineering. Jev is a candidate for pervasive, inexpensive contextual judgment within that system, not a replacement coding agent or the owner of policy.

Brian should be able to run an ordinary coding task in an AES-governed repository and later inspect:

- what the agent was asked to do and what context was actually supplied;
- every exposed action, result, policy evaluation, warning, block, and recovery;
- where a policy helped, missed something, or obstructed legitimate work;
- what a revised policy or context strategy would have done differently;
- the evidence supporting promotion, revision, or retirement of that control.

The first useful deliverable is a replay report over real archived sessions showing what Jev would have noticed, warned about, or blocked, including its mistakes. The next is the same view for a live coding session, initially without Jev changing the agent's behavior.

This is work on the AES-governed coding loop. Adapting arbitrary non-AES repositories is not a prerequisite. Repository Context's existing implementation and evidence are preserved; its roadmap disposition is handled explicitly in section 12.

### Directional choices from this conversation

Record all accessible engineering telemetry by default. Preserve raw source material; derive smaller views without replacing the originals. Recover the previous failure taxonomy, policy index, exception handling, measured/blocking lifecycle, and hook lessons rather than inventing them again. Prefer contextual policy evaluation where brittle procedural checks caused failures. Make intervention intensity configurable. Let feedback eventually improve every part of AES, while introducing its effects in bounded stages.

### Working hypothesis

A combination of deterministic observations, Jev judgments, a small explicit policy runner, and richer-model escalation can outperform the old hooks on useful intervention, false blocks, latency, recovery, and total engineering effort.

That hypothesis is not yet measured on Brian's workloads. Strong Jev results in one policy family do not authorize its use as a blocker in another.

## 2. What the investigation actually established

### Existing AES work is a starting point

The predecessor's `src/agentic_engineering/models.py` already defines measured and blocking policy tiers, a promotion request, negative-control and client-wiring observations, and a concrete recovery action. `src/aes/rules.py` preserves problem identity and explains failures caused by stripping or changing exceptions. Those semantics are donors, not requirements to copy the old implementation wholesale. [R4, R5]

The retained Codex recurrence-control report identifies a post-tool output-format problem and explicitly distinguishes hook completion from client acceptance of the hook response. Its historical successful probe is not proof about the clients installed today. [R6]

The inspected hook receipt writer records hashes and start/completion metadata rather than complete input bodies. It is useful lineage and receipt-design material, but does not meet the new full-retention objective by itself. We must join actual archived payloads where available, not treat a hash as reconstructable content. [R7]

### Current Jev constraints that affect this design

As checked on 2026-09-19, TypeSafe lists `jev-1.13.0`, text-only input, a 64k aggregate request budget and a 32k state-plus-longest-question budget. Input price is $0.042 per million tokens; rate limits are explicitly subject to change. Pin a version and retain the returned model identity rather than relying on a moving alias. [J1]

The API accepts state and typed questions: Noul, Choice, and Score. Question-map keys are not inference instructions. Put the actual policy condition into instructions and criteria. Choice/Score confidence is derived from their output distributions; Noul has no separate confidence field. Do not invent an independent confidence measurement. [J2, J3]

TypeSafe documents literal-reading errors, difficulty with indirection and numerical precision, distraction by irrelevant context, and susceptibility to misleading input. Separate questions need not satisfy expected probability identities. These become evaluation cases, not footnotes. [J4]

Parallel questions share a state and do not consume one another's answers. They can reduce round trips; they are not independent witnesses that an action is correct. Conditional combinations belong in code. If a later question genuinely needs an earlier answer, make that dependency explicit. [J5]

The vendor's latency and calibration claims are not AES measurements. Schema-valid output is not proof of a correct judgment. Jev does not generate free-form explanations or new policies; use fixed explanation templates or a generative model for those tasks. Current customization is through state, questions, and criteria, not customer-specific fine-tuning. [J1, J4, J6]

The Reddit discussion supplied by Brian is an inspiration source. A fresh attempt to retrieve it during this planning session failed, so none of the acceptance criteria depend on its anecdotal results. [J7]

## 3. Separate three different things

**The sensor:** supplies observations and contextual judgments. Examples: actual Git state, a process exit status, Jev's assessment that a claim overstates its evidence.

**The policy:** specifies expected behavior, applicability, exceptions, required evidence, intervention mode, and what happens when a check cannot run.

**The enforcement connection:** makes the policy's decision affect the intended action at the correct runtime boundary.

Jev mainly changes the first part. It cannot fix a hook that never fires, a client that rejects the output envelope, a stale worktree snapshot, or a block with no legal recovery path.

A model must not estimate a fact we can directly observe. Git identity, hashes, exit codes, file existence, deadlines, and exact revision comparisons remain deterministic. Contextual interpretation is the model's job. A plausible-looking judgment does not manufacture user authorization, a verification receipt, or a successful run.

## 4. Proposed runtime shape

Use a small shared AES runtime with thin native-client adapters. Do not make each hook a separate policy application.

```text
Claude Code / Codex / subagent event
                 |
          native AES adapter
                 |
      durable raw-event recording
                 |
        exact context/state snapshot
                 |
        +--------+------------------------+
        |                                 |
selected synchronous checks       queued semantic observation
before a consequential action     after/alongside normal work
        |                                 |
Jev + deterministic facts          Jev classification, context
        |                          relevance, failure/recovery tags
versioned policy decision                  |
        |                                 |
client-specific response           append-only annotations
        |                                 |
client acceptance + actual effect ---------+
                 |
      inspectable session/replay report
                 |
   evaluation -> proposed improvement -> trial -> outcome
```

### The waiting path

Only checks that must affect the imminent action run synchronously. Broad logging and learning do not require every action to wait for a cloud model. A selected pre-action check gets one batched request over a bounded state, an explicit deadline, and policy-specific unavailable behavior.

Expired judgments cannot authorize a different tool call or a changed worktree. Bind them to action identity, context digest, policy version, and relevant state preconditions; revalidate local preconditions before the action proceeds. Caching is only over identical relevant inputs and versions, never merely the same command string.

### The observation path

Record first, then analyze through durable workers. Start without behavioral intervention. The agent must not receive shadow-mode findings as instructions; doing that would change the behavior we are trying to measure. Findings remain visible to the operator and are retained for later analysis.

Give worker jobs durable identities, bounded concurrency, retries, queue-age telemetry, and deduplication. Recover after crashes from retained events. Do not launch an untracked new background process for every event.

### Runtime differences are explicit

Current Claude Code documentation supports several hook mechanisms, while current Codex documentation says command and MCP-tool handlers are supported and prompt/agent handlers are parsed but skipped. Do not assume one hook configuration works identically in both. Start with a transport supported by the exact installed versions and a tiny validated response envelope per event. [C1, C2]

Async hooks cannot retroactively block an action that already happened. Native async process lifetime also needs testing; a durable AES worker should not depend on a short-lived client process staying alive. [C1]

A runtime-coverage manifest records which event/action paths are observable and which are enforceable: shell tools, patch/edit tools, MCP calls, subagents, stop/completion, and relevant git boundaries. Uncovered paths are named as gaps. A voluntary guard call is not mandatory enforcement.

## 5. Policy and context design

### Preserve the old policy lineage

Inventory existing IDs and original wording first. Map them forward rather than creating a second policy registry. Keep failure/problem identities independent of their current mitigations. One failure may need better context, a skill, a deterministic check, a semantic check, or several together; not every failure needs a blocking hook.

The proposed policy contract extends whichever existing schema is selected after inspection:

| Concern | Required information |
| --- | --- |
| Identity | Policy ID/version, source wording, owner, problem/failure references |
| Meaning | Applicability, explicit exceptions, intended outcome |
| Inputs | Required facts and context; acceptable age and source |
| Judgment | Question version, provider/model, criteria, output schema |
| Intervention | Mode, thresholds/decision logic, authorized override scope |
| Failure handling | Deadline, missing-context behavior, model-outage behavior |
| Recovery | Concrete action or explicit escalation; retry/loop limits |
| Validation | Positive and negative cases, judged examples, promotion evidence |

Keep evaluation state separate from intervention. `missing_context`, `stale`, `timeout`, `provider_error`, `invalid_response`, and `not_evaluated` are not low-risk answers. A profile may continue after an unavailable advisory check, but the record must say it continued without that check rather than labeling it passed.

### Modes

| Mode | Effect |
| --- | --- |
| Off | Do not evaluate this policy; keep base event recording |
| Shadow / measured | Evaluate and record what would happen; no agent intervention |
| Warn | Give the agent relevant feedback; do not block |
| Enforce | Apply the specific accepted allow/block/escalate behavior |

Modes are configurable per policy, repository, runtime, and task/risk profile. Record the resolved effective configuration and its precedence. Keep warning separate from shadow because warnings can change agent behavior. Promotion is evidence-based; demotion, revision, and retirement remain available. A zero firing count alone is not evidence that a policy is obsolete—it might be preventing the behavior or its sensor might be broken.

### Context is not one big prompt

Keep native mandatory instructions intact: root and applicable subdirectory CLAUDE.md/AGENTS.md, accepted task boundaries, required policy clauses, and actual permissions. Jev may rank optional context; it may not silently drop required instructions or decide which authority outranks another.

Maintain source and version references for task/plan context, relevant wiki sections, skills, tool definitions, parent/subagent instructions, current working state, and retrieved evidence. Distinguish available, retrieved, injected, and consumed-by-tool events. Injection is observable; actual cognitive understanding is not proven by injection.

Build small named state packets from the large archive. Preserve the candidates considered, selected fragments, omitted fragments, selection method, and token counts. Include `none_of_the_above`/insufficient-information behavior when a choice set might omit the correct answer. Model-based policy routing must not filter out mandatory checks before they run.

## 6. Full-fidelity observability

**Recording breadth and inference context size are separate settings.** Keep the complete accessible record even when the active agent or Jev receives a small projection.

Capture all exposed transcript messages, tool arguments/results, commands, stdout/stderr, exit codes, patch/diff content, subagent messages, session transitions, compaction boundaries, instructions and skills supplied, policy evaluations, retries, warnings, blocks, overrides, recovery steps, verification runs, artifacts, timing, and reported usage. Preserve native source files and event payloads; normalized records are additional views.

Record exposed reasoning artifacts when the runtime supplies them. Do not claim to capture hidden model state or events that the client never exposes. Mark omissions, truncation, disabled logging, and unknown capture coverage explicitly.

A normalized event envelope should include session/turn/action/parent identifiers; source runtime and version; wall time and monotonic duration where available; repository commit plus relevant dirty-worktree snapshot/diff identity; task and policy versions; raw payload references and digests; origin (`authentic_runtime`, `historical_replay`, `test`, `synthetic`, `manual_review`); and observation completeness.

For every semantic evaluation, additionally retain the full application request and response, context selection, question/criteria versions, provider request ID where supplied, model identity, all returned values/distributions, retries, latency components, token usage, and cost calculation. A policy decision then references those records and separately records what the client actually accepted and what happened next.

The capture chain is explicit:

```text
event observed -> hook invoked -> input accepted -> evaluation completed
-> policy decided -> response accepted by client -> action/effect observed
```

A missing link remains missing. Hook exit status alone is not proof that the client enforced its answer.

### Storage and recovery

First inspect and reuse Brian's existing transcript archive/export pipeline. Do not launch a new archive platform merely to start this work. Add immutable event/payload references and a rebuildable query index. Lossless compression and deduplication may reduce physical storage while preserving original bytes and multiplicity of observations.

A small local durable spool plus the existing archive and a SQLite index is the initial candidate, subject to the first throughput/recovery probe. Large raw archives do not belong in ordinary Git history. GitHub retains code, policy/config versions, dataset manifests, bounded examples, evaluation definitions, readouts, and durable change history.

Recording should survive worker/network failure. Backpressure, queue growth, disk exhaustion, and archival failure must surface as operating states; never silently discard events. Define the response to local storage exhaustion in the operating profile, including an explicit degraded/capture-unavailable state or pause. No design can promise lossless capture with unavailable storage.

Filter the observer's own operations by origin so analysis does not repeatedly trigger itself. Preserve those operations in telemetry without recursively spawning unlimited new evaluations.

## 7. Implementation sequence and usable checkpoints

Stages are ordered by evidence, not calendar estimates. Later stages are conditional. Work can proceed in parallel only where contracts are stable and it does not delay the first useful observation.

### Stage 0 — Recover the evidence and reconcile the direction

Inspect the old policy index, exception model, hook failure records, adapters, receipt readers, transcript/export tooling, and actual installed-client boundaries. Start with the already located sources [R4–R7], then trace their references and archived implementation history. Mark each mechanism reuse/adapt/donor-only/reject/unresolved; an old file is not automatically a runtime dependency.

Build a compact failure table with original event/evidence references, expected behavior, observed behavior, root-cause hypothesis, and whether contextual judgment could have helped. Separate semantic mistakes from wiring, protocol, state, race, deployment, and recovery failures.

Freeze a small first candidate set from actual examples. Proposed families are: legitimate action incorrectly blocked; unsupported verification/completion claim; scope/plan drift; repeated failed recovery; and missing relevant instructions/skill. These are selection candidates, not newly invented canonical policy IDs.

Materialize the proposed target/current variances below against the current gap ledger, then use the adopted planning provider to derive/freeze the implementation and verification topology before code. Resolve the Plan 001 and provider-boundary questions in section 12 instead of silently changing the roadmap.

**Usable checkpoint:** Brian can inspect real failure cases and see which ones this experiment addresses. No claim that Jev would have fixed them yet.

### Stage 1 — Replay archived sessions and compare evaluators

Implement one offline path: native archive record -> prefix-only context packet -> candidate questions -> selected evaluator -> policy decision -> inspectable report.

Run the old deterministic control where reconstructable, Jev, and one small generative comparator on the same cases. Select exact comparator model/version at execution; Haiku or Luna are candidates, not assumptions about API availability. Use mocks only for protocol tests, never as evidence of Jev accuracy.

Keep the future hidden from each replayed decision. Later outcomes can label it, but must not enter the event-time context. Split development, threshold-tuning, and held-out cases by session/project or time so neighboring events do not leak across the split. Keep synthetic edge cases separately labeled from authentic runtime evidence.

Build an operator report that shows source event, original rule/exception, old behavior, Jev judgment, comparator judgment, proposed intervention, uncertainty, eventual outcome, and human adjudication. Support disagreement/false-block/missed-failure/latency filters and direct source drill-down.

**Usable checkpoint:** a real archived session can be replayed and Brian can see both useful judgments and model errors. The readout supports selecting a first policy or rejecting a policy/model fit.

### Stage 2 — Live observation without behavioral interference

Connect the first native client through a thin adapter and durable capture path. Add the second client to the same contract rather than duplicating the policy engine. Run candidate policies in shadow, preserving existing controls unchanged.

Test actual native tool/patch/subagent events, session restart, compaction, cancellation, parallel sessions, and missing-hook detection. Compare native transcripts with captured event counts. A replay-harness pass does not replace these tests.

Add a live session view showing capture completeness, policy evaluations, queue lag, provider availability, and hypothetical interventions. Prove that turning off Jev leaves ordinary recording and the existing coding workflow operational.

**Usable checkpoint:** Brian runs a real coding task in an AES-governed repo and sees what the policy layer observed without it obstructing the task.

### Stage 3 — Warnings that improve the same task

Promote only selected policies to warn after reviewing Stage 1/2 evidence. Feedback must name the issue, show relevant evidence or its absence, state the applicable exception, and offer a usable next action. Rate-limit repeated warnings and join them to recovery episodes.

Use prewritten response templates populated from observations. If an explanation requires new reasoning, use the richer model and label its interpretation. Do not pretend Jev generated a rationale it did not return.

Observe whether agents take useful corrective action, ignore warnings, repeat blocked-style loops, or need human rescue. Warnings are a treatment, not an untreated baseline.

**Usable checkpoint:** one real task benefits from contextual feedback, with a trace showing whether the improvement happened and what effort it cost.

### Stage 4 — Selective enforcement with recovery

Promote one policy at a time and only on explicitly verified client/action paths. Require a held-out quality result, a true violating case that is stopped, a valid exception that passes, a runnable recovery, and fault-injected unavailable behavior. Existing deterministic invariants remain in force.

Start with a reversible workflow boundary, not a broad rule allowing Jev to authorize irreversible operations. A candidate example is a completion/verification claim that needs correction or an evidence attachment. The legal recovery includes accurately stating that verification was not run where the task permits that, not forcing every task through an unnecessary test suite.

Bound intervention loops. Never repeatedly deny the same action without new evidence, a concrete recovery route, or an explicit pause/escalation. Test disabling/demoting the policy without corrupting work or receipts.

**Usable checkpoint:** an actual violation is prevented, a legitimate exception succeeds, and the agent completes recovery without Brian untangling the hook.

### Stage 5 — Expand semantic assistance across context and coordination

Introduce optional-context ranking, skill suggestions, subagent selection/handoff review, plan-deviation classification, verification relevance, completion review, and session-health signals. Each new action-bearing application starts in shadow or advice mode and gets its own evaluation set.

For context ranking, measure omitted important information as well as token savings. For skill selection, allow no skill. For subagents, retain parent-child context/effect lineage. For completion, a semantic verdict never substitutes for execution evidence.

Do not hold up useful policy controls until this broader layer is complete. Conversely, useful nonblocking observability applications may expand before model-based blocking is justified.

**Usable checkpoint:** agents receive more relevant context or delegation support, and the report shows whether task outcomes improved rather than merely shrinking prompts.

### Stage 6 — Close the improvement loop

Cluster recurring failures, compare interventions/outcomes, and propose changes to policies, exceptions, context composition, skills, routing, verification, planning, provider choice, and the taxonomy itself.

Begin with evidence-backed proposals and ordinary reviewed Git changes. Replay each proposed change against retained regression cases and a held-out set; then deploy a bounded trial and compare real outcomes. Record acceptance, rejection, rollback, and unresolved uncertainty.

Later, allow automated promotion only within a separately accepted scope. The evaluator must not redefine its own success criteria, suppress its own failures, or weaken required controls without an authorized change path. Jev may help classify feedback; it is not the sole judge of whether its own policy changes succeeded.

**Usable checkpoint:** one observed failure leads to an accepted change, a later comparable session tests it, and the resulting evidence determines retain/revise/revert.

## 8. Candidate acceptance gates

These are proposed initial operating targets, not observed performance or universal release standards. Freeze the policy-specific criteria before evaluating the held-out cases.

### Measurement and semantics

Measure false warnings/blocks, missed relevant failures, abstentions/unavailable checks, applicability coverage, and recovery outcomes by policy and runtime. Include the denominator of relevant actions, not only firings. Distinguish outcome probability, model confidence, and evidence completeness.

For a first reversible blocking pilot, propose false-block rate below 1% on relevant legitimate cases, alongside an explicit miss tolerance chosen for that failure's consequence. As a scale illustration, zero errors in 300 independent legitimate cases gives a one-sided 95% upper bound of about 1% (`1 - 0.05^(1/300)`); repeated near-identical events are not 300 independent cases. Small or unrepresentative samples justify warning/shadow status, not a claim of safety.

Use human-adjudicated examples and verifiable subsequent outcomes. Another model may assist labeling but is not ground truth. Include random samples of apparent passes to find misses, plus reviewed disagreements and rare consequential cases. Re-evaluate on changes to policy wording, exceptions, questions, context composition, model, or native client.

Shadow replay measures proposed decisions; it cannot establish what would actually have happened had the intervention changed the trajectory. Effectiveness claims need later live controlled comparisons, never unsafe removal of mandatory safeguards for an experiment.

### Latency and availability

Initial measurement targets: durable capture/dispatch overhead p95 at or below 20 ms; selected synchronous policy overhead p95 at or below 500 ms and p99 at or below 1.5 seconds; a proposed two-second total decision deadline. Validate or deliberately revise these targets on the real environment. Report timeout rates and tails rather than hiding them from averages.

Budget context retrieval, queueing, network time, inference, response handling, and local precondition revalidation separately. Keep a warm worker/connection pool if measurement shows startup overhead matters. Batch related questions, not unrelated contexts whose union makes judgments worse.

Disable long SDK retry chains on the synchronous path; deadline includes any attempt. An over-deadline generative escalation becomes an explicit bounded pause/review path, not an invisible sequence of additional calls. Background jobs may retry with bounded backoff. TypeSafe documents SDK retry behavior and transient overload responses, so defaults require deliberate review. [J2, J8]

On Jev outage, base recording and existing controls continue. Shadow jobs queue for later replay; advisory policies report unavailable. A policy promoted to blocking has a documented fallback/pause rule and must not silently convert a timeout into approval. Do not stop every ordinary read just because a noncritical semantic annotation failed.

### Enforcement and recovery fault matrix

| Failure family | Required test |
| --- | --- |
| Wrong contextual judgment | Real false positives, true failures, valid exceptions, insufficient evidence |
| Missed action path | Actual shell, edit/patch, MCP, subagent, and stop events for each installed client |
| Protocol failure | Malformed/missing fields, extra stdout, unsupported event response, client parse rejection |
| State error | Dirty worktree, branch switch, stale snapshot, changed policy, late cached decision |
| Runtime failure | Deadline, provider outage/overload, worker crash, cancelled session, restart |
| Concurrency | Parallel sessions, duplicate/out-of-order delivery, policy rollout during execution |
| Recovery loop | Repeated deny, failed recovery, stale claim, unavailable escalation channel |
| Logging failure | Interrupted writes, archive outage, full disk, missing source events, truncated payload |
| Evaluation drift | Misleading transcript content, missing choice option, altered exceptions, contradictory criteria |

Negative controls run in disposable fixtures/worktrees, never by risking unrelated work. Model robustness cases are engineering reliability tests: a transcript's assertion that its own action is fine must not become authoritative evidence.

## 9. Economics of heavy use

Log real usage and latency rather than restricting observation preemptively. Also distinguish recording everything from synchronously evaluating everything.

At the documented input price, an illustrative 10,000 requests averaging 8,000 billed input tokens each cost `10,000 * 8,000 / 1,000,000 * $0.042 = $3.36`. This is arithmetic, not a workload forecast; include all question text, retries, context selection, storage, and richer-model escalation in the actual report. [J1]

Similarly, an illustrative 300 ms wait repeated 10,000 times adds 50 minutes of serial waiting even if inference is inexpensive. That is why broad semantic observation is queued and only selected consequential checks interrupt the coding agent.

Compare total work cost: model spend plus waiting, false-block recovery, rework, and Brian's intervention. Cheaper classifications that create expensive recovery are not a win. Freeze an experiment spending cap/profile before paid evaluation; this proposal makes no purchases or API calls.

## 10. Minimal implementation boundary

Reuse the existing archive, Git, installed clients, and suitable standard libraries. Candidate responsibilities are: capture/normalization, state construction, semantic-evaluator adapter, policy evaluation, native-client response adapters, replay/evaluation, and a small inspectable report. They are not seven new services.

Keep the Jev binding behind a small typed interface so the same cases can run against a deterministic baseline, Jev, or a selected generative comparator. Retain provider-native responses alongside normalized results. Missing native fields remain absent; adapters do not invent equivalence between confidence measures.

Use established native hooks/SDKs where supported. The public `jev-guard` project is an adapter/design candidate, not a chosen runtime dependency or evidence that our clients are covered. Review its exact code, license, failure behavior, logging, and state boundaries before any reuse. [J9]

Proposed code stays within `src/agentic_engineering_system/`, with verification under the selected existing/derived test homes. Use the adopted architecture-realization process to settle exact component paths after the Stage 0 inventory. Do not create a new implementation root, universal contract framework, dashboard platform, event broker, or rewritten coding agent simply to run the first replay.

## 11. Proposed target/current variances

These are planning inputs, not new accepted canonical gap-ledger entries or conformance claims.

| Variance | Evidence/current limitation | Relevant existing target |
| --- | --- | --- |
| Contextual control quality is unmeasured | Reported hook friction and retained recurrence records do not establish Jev improvement | AES-POL-001, AES-POL-004 |
| Full decision reconstruction is not established | Inspected receipt writer is content-free; archive joins and capture coverage are unverified | AES-EVID-001 |
| Client effect differs from hook success | Historical report explicitly limits adapter-parse attribution | AES-POL-002, AES-POL-003 |
| Context selection needs evidence | Broad mechanism inventory exists; Jev relevance/omission behavior unmeasured | AES-CTX-002, AES-CTX-003 |
| Closed-loop improvement is not demonstrated by this proposal | No new live policy trial or comparable outcome has run | AES-LEARN-001, AES-SYS-001 |

## 12. Roadmap and provider disposition

Current canonical governance explicitly selects Company Planning for planning/design and Enforced Planning for execution governance, with a pinned installed provider. That is stronger than 'donor only.' This proposal does not conceal or silently undo that current state. [R1–R3]

Proposed near-term disposition: preserve the installed governance as the baseline while evaluating the new semantic layer; treat predecessor ideas/code as donors unless individually selected. Do not add a new runtime dependency on the old AES repositories merely to recover their lessons. If Brian wants AES-native execution governance rather than the current provider arrangement, document the replacement boundary and migrate only after equivalent coverage and recovery are demonstrated.

Plan 001 remains partial in current main. Proposed roadmap change: allow this policy/observability workstream to become the next implementation priority, with Plan 001 explicitly paused/deferred if accepted. Preserve its code, evidence, and unresolved acceptance state. Do not mark it delivered to clear the path. Accepted clauses that currently require first-vertical external-consumer closure or a particular provider must be explicitly dispositioned, not worked around. [R2, R3]

Planning order is: accepted directional change -> fresh characterization/gap disposition -> provider fit -> Company Planning derivation/topology freeze -> implementation stages. The user has requested this planning work; runtime adoption and live enforcement remain future decisions supported by evidence.

## 13. Execution and handoff discipline

Each meaningful implementation increment has an isolated branch/worktree, inspected Git status, preserved pre-existing modifications, and an early pushed checkpoint. Native-client integration changes get rollback instructions before installation. Pin evaluation subjects and record transitive dependency/context changes; repository HEAD alone does not describe dirty working-state decisions.

Machine-dependent work uses Brian's actual environment only after Remote MCP device discovery, execution-ready confirmation, and ping. Use the guarded PowerShell-to-WSL launcher and resume agent sessions by session ID. A session without those tools can still perform GitHub-only research/planning; it must not diagnose the machine as offline or claim a local test ran. [R1]

The first implementation work order, after acceptance and topology derivation, is: select a small source-linked set of previous hook failures and legitimate exceptions; ingest the corresponding archive prefixes; run a minimal evaluator comparison; produce the first reviewable replay report. Do not begin by rewriting every hook or implementing every North Star component.

## Sources and evidence limits

Repository references use the exact inspected revisions. Public docs were accessed on 2026-09-19 and can change. Source inspection is not execution evidence.

- R1: [Canonical governance](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/cd3705cfa23e3fe40f6a34f56f211747bab36497/CLAUDE.md).
- R2: [Canonical manifest](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/cd3705cfa23e3fe40f6a34f56f211747bab36497/.agentic/repo.yaml) and [wiki orientation](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/cd3705cfa23e3fe40f6a34f56f211747bab36497/wiki/index.md).
- R3: [Accepted AES system boundary](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/cd3705cfa23e3fe40f6a34f56f211747bab36497/docs/architecture/SYSTEM_BOUNDARY.md).
- R4: [Predecessor policy promotion contracts](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/src/agentic_engineering/models.py).
- R5: [Predecessor problem/rule/exception model](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/src/aes/rules.py).
- R6: [Codex hook recurrence-control evidence](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/docs/evidence/codex-hook-recurrence-controls-20260901.json).
- R7: [Content-free hook receipt implementation](https://github.com/Inside-Success/agentic-engineering-system/blob/17ed0c5b10f04d88dc919a5b52bd2244c78134ac/src/aes/hook_receipts.py).
- J1: [Jev models, limits, versioning, pricing, customization](https://docs.typesafe.ai/models).
- J2: [TypeSafe API reference](https://docs.typesafe.ai/api).
- J3: [Confidence semantics](https://docs.typesafe.ai/confidence).
- J4: [Jev 1.13 documented failure modes](https://docs.typesafe.ai/model-jaggedness/jev-1.13).
- J5: [State](https://docs.typesafe.ai/concepts/state) and [parallel questions](https://docs.typesafe.ai/patterns/fan-out).
- J6: [TypeSafe launch article and benchmark limitations](https://typesafe.ai/blog/introducing-system-one-models-and-jev).
- J7: [User-supplied Reddit experiment](https://www.reddit.com/r/AI_Agents/comments/1wkzjtx/i_tested_jev_as_a_subconscious_helper_for_my_ai/) — retrieval unsuccessful in this planning session; not an acceptance source.
- J8: [Python SDK retry configuration](https://docs.typesafe.ai/sdk/python/api/retries).
- J9: [jev-guard public repository](https://github.com/leepokai/jev-guard) — candidate only; no installation or compatibility claim.
- C1: [Claude Code hook reference](https://code.claude.com/docs/en/hooks).
- C2: [Codex configuration reference](https://developers.openai.com/codex/config-reference).

## Completion status of this planning activity

Produced a source-grounded draft direction, staged work plan, observability requirements, evaluation gates, provider/roadmap reconciliation, and execution boundaries. No Jev accuracy/latency benchmark, local archive audit, client-coverage test, policy migration, runtime installation, or live feedback trial was performed.
