---
schema_version: "1.0"
artifact_type: design_plan
id: aes-feedback-prevention
status: proposed
conflict_surfaces:
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: "proposals/aes-feedback-prevention"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: "proposals/README.md"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: "proposals/aes-learning-loop/feedback-system.svg"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: "CLAUDE.md"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: "AGENTS.md"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: "scripts/meta/render_agents_md.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: "tests/test_execution_readiness.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: ".project-brain/now.md"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: ".company-planning/active-execution.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agentic-engineering-system-canonical"
    target: ".company-planning/history"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "scripts/taxonomy_feedback_pass.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "tests/test_taxonomy_feedback_pass.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "taxonomy_feedback_state.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "README.md"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "tests/test_archive_artifacts.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "tests/test_check_destructive.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "tests/test_install.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "tests/test_skill_portfolio_contracts.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "tests/test_sync_skills.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "tests/test_work_market_skills.py"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "skills/brian-positions/evals/trigger_cases.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "skills/diagram-design/evals/trigger_cases.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "skills/impeccable/evals/trigger_cases.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "skills/representation-router/evals/trigger_cases.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "skills/resume-writing/evals/trigger_cases.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "skills/review-skill-feedback/evals/trigger_cases.json"
    access: write
  - kind: repository_path
    repository: "BrianMills2718/agent-skills"
    target: "skills/visual-explainer/evals/trigger_cases.json"
    access: write
method_conformance_receipt: proposals/aes-feedback-prevention/PLAN.receipt.json
goal:
  outcome: "New feedback reaches existing failure-pattern review and one real native-agent failure reaches checked prevention"
  canonical_example: "A native subagent preflight failure is dispositioned against the taxonomy, its shared instruction is repaired, and native versus Remote MCP cases are checked"
  forbidden_substitutes: "More reports, a generated candidate list, source text alone, a child self-rating, or treating one episode as two independent sightings"
  boundaries: "Claimed AES and agent-skills worktrees plus the exact Agent Skills main-branch linear-history setting; no new feedback store, router, global hook, agent/tool permissions, model override, benchmark, destructive action or private publication"
  done_when: "Inspect source report through default taxonomy command and committed disposition; inspect native positive and remote-required negative child traces and parent receipts; pass local gates and integrate recoverably"
  do_not_gate_on: "No new human approval for reversible work or merge; no benchmark, elapsed-time gate, unrelated backlog or automatic agent-routing promotion"
---

# Feedback reaches review and prevents one repeated failure

Each section below answers the checklist items quoted in it; the gate judges only that
section's text. Replace every `TODO(answer ...)` line before running `cli.py check`. Quote
values in the front matter: an unquoted ` #` starts a YAML comment and cuts the value.

## Actor and result

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

Brian and parent coding agents need feedback to reach a generalized failure mode and an enforceable prevention check. Brian approved this exact next increment with “proceed” after the compliance discussion on 2026-10-08. Canonical case feedback-prevention-v1: the original native child stopped at an inapplicable Remote MCP prerequisite (AES #468); its actual feedback report reaches the existing taxonomy reviewer (AES #458), receives a source-grounded disposition, the canonical instruction is scoped to the execution transport, and a repeated native read-only task completes while a task requiring Remote MCP stays inconclusive when its network readiness calls are excluded. PlanningPathDecisionV1 is planning-path-decision.json: repair, with concurrency retained as a coordination control. This is a source/code repair with behavioral acceptance, not a human-judged prose revision loop.

## Requirements

> **CORE-REQUIREMENTS-TRACED** (blocking): The plan lists its requirements: what was asked for, and what the delivered work's own claims imply. A claim here is what the work is presented as being or doing to its users, for example work presented as following a standard, schema or contract (which implies conformance to it) or an output labelled as showing something (which implies it shows it correctly); the plan's own format and front matter are not such claims, and the details a check examines (what a trace must show) belong to that check rather than being separate requirements. Each requirement names the check that verifies it (a test, script, gate step, or named review of a run) and its status: passing, failing, planned and not yet run, or deferred with a stated reason; deferred requirements are carried onto every release or completion record the plan names. A plan fails this item if it has no requirements list, if any requirement has neither a check nor an explicit deferral with its reason, or if the plan presents the work as following a named standard, schema or contract, or as having another property its users rely on, that its requirements list omits.

R1 — New collector feedback-report.v1 observations must be readable by the existing default taxonomy command, alongside retained legacy entries, with exact record IDs, text, evidence links, report/session identity and occurrence time preserved; check: agent-skills tests/test_taxonomy_feedback_pass.py plus authentic default-CLI intake trace; status passing: 23 focused reader regressions, actual intake and installed reader exact-record checks (private repair-verification.jsonl:58,77). R2 — The original native failure must receive an actual semantic disposition against all existing families, without a new family licensed by duplicate records from one episode; check: one traced bounded semantic review, committed taxonomy_feedback_state.json, and the existing disposition verifier on exact source IDs; status passing: traced all-22-family review, one original episode classified family N, committed disposition and deployed verifier exit 0 (private repair-verification.jsonl:58,77). R3 — Native local inspection must not require Remote MCP tools, and genuinely remote work must retain list/readiness/ping prerequisites; check: feedback-prevention-v1 native positive and remote-required negative role cases, full trace review and executable parent result/schema/source checks; status passing: native supported result and remote-required no-network inconclusive result, five parent-check self-tests per case, old native inconclusive result rejected (private repair-verification.jsonl:57). R4 — Claude and Codex must receive the same scoped authority, through canonical CLAUDE.md and generated AGENTS.md; check: make check generated-instruction sync and source-linked review of both case traces; status passing: canonical/generated instruction sync in the AES gate; native Codex behavior traced, Claude delivery parity checked but no fresh live Claude child run (private repair-verification.jsonl:57,61). R5 — The change must remain recoverable and the existing consumers must adopt it; check: focused regressions, final local make check in AES, agent-skills make test/check, merge-commit readback and canonical/runtime default reader smoke; status passing: AES make check 340 passed/1 skipped and mypy clean; Agent Skills make test 466 passed/0 failed and make check passed; PRs 479 and 460 merged with tested source ancestry preserved; installed default reader exact-record smoke passed 7 checks (private repair-verification.jsonl:61,74-77). No requirement is deferred. External DevelopmentInvestigationResultV1 schema validation is included in R3; the taxonomy's Entry projection is not emitted or labelled as a feedback-report.v1 object.

## Success and disproof

> **CORE-SUCCESS-DISPROOF** (blocking): The plan defines the evidence that would show success and a concrete condition that would disprove the approach. Each success measure is the property the plan claims, or a check that directly tests that property, not a stand-in for it: a count, a picture, a readability judgment, or the pipeline agreeing with itself (hashes, labels, byte equality) does not show correctness or conformance it does not test. A plan fails this item if it has no disproof condition, or if a success measure is such a stand-in for the claimed property and the plan names no direct check of that property.

> **CORE-TRACE-REVIEW** (blocking): Every success or acceptance criterion in the plan is judged from the full trace of a run, not only its final outcome: it names the run whose full trace is examined (for example the session, its tool and LLM calls, commits, check output, or messages), where that trace lives, and what must be seen in that trace beyond the final outcome. A criterion that names only an outcome, such as tests passing, a PR merged, a test fixture reproducing the journey, or a status reading succeeded, fails this item. A criterion for which no run exists, such as a pure document edit, passes only when the plan states that exemption and its reason explicitly.

Success is direct consumer behavior: the default taxonomy command reads the real failure record's actual sentence and links; a reviewed disposition covers that exact source and names the general failure; a native leaf reads the permitted parser source and returns a supported diagnosis; the remote-required leaf stops before parser inspection when readiness and ping cannot be performed within the task permissions. Parent checks reject the old inconclusive result when submitted as the expected native-positive case. Disproof includes: new records absent from the reviewed batch; a report count accepted without sentence membership; duplicate/mutated record IDs silently accepted; failure inferred solely from a final status; native work still blocked by remote prerequisites; remote work bypassing the preflight; an output labelled DevelopmentInvestigationResultV1 violating its JSON Schema. The repair proves this case and its prevention check, not universal recurrence elimination or a better role/model.

Named run feedback-prevention-v1 in native parent session 01a11cac-2557-7dc0-8edd-8487ed5968d1. Read the complete original child trace 01a11dcc-f50a-72f3-9a03-94cdb11ffe8f and the full trace of each repeated child assignment: authority inputs, actual source reads, tool arguments/results, missing-tool discovery, returned citations, model usage where observed and mutations. Native transcripts live under ~/.codex/sessions; private trace refs, returned result bytes and checks go in the existing repair-verification.jsonl. Inspect the source report's actual record, the default taxonomy command's exact input/output, the semantic call prompt/result, committed disposition, parent checker argv/stdin hashes/stdout/stderr/exit, filing readback where a new report is filed, and each local gate's full log including failing/surprising cases. Negative evidence is the old native inconclusive result rejected by the positive checker and the remote-required case retaining its stop. Documentation edits have no separate behavioral execution: verify their source links and generated authority sync. Never treat a receipt hash or a candidate family list alone as semantic correctness.

## System model

> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: exempt -- <reason>`, which fits only a project with no stored state and no user-facing view. Unless exempt, the plan names each system-model element (entity, process, record or event, or view) that the work adds, changes, or relies on, and its trace review names, for each such element, what the examined run must show of it (for example an event of that record type with its id, or the view displaying that entity). A plan with neither a model link nor the exemption line fails this item, as does one that lists model elements without saying what the examined run must show of each, or one that names no element without stating that the work touches none and why. For a maintained repository, the plan also cites the documentation entry point from which the model is reachable; a shared model explicitly identifies this repository's scope. It names applicable source-linked views, explains material omissions without imposing a fixed diagram quota, names concrete model freshness or drift checks, and states how the model, view coverage and verification evidence will be reconciled in the same change (or gives a concrete reason each needs no update). A bare model path without these discovery, view, freshness and reconciliation obligations fails this item. Representation Router may render selected views but does not supply planning authority or prove executed behavior.

System-model integration element: the Agent Skills main-branch merge-history rule; inspect the actual GraphQL input/result, REST before/after protection and source-commit ancestry at the PR merge. It adds no feedback entity or product UI.

System model: SYSTEM_MODEL.md in this proposal, a bounded extension of proposals/aes-subagent-feedback/SYSTEM_MODEL.md and proposals/aes-learning-loop/PLAN.md. Discovery: wiki/index.md → CLAUDE.md → direct plan/model/goal links; the proposal index also lists the repair. Its scope explicitly includes AES instruction/report ownership and the agent-skills taxonomy consumer. Elements and required observations: daily report/record — exact ID, sentence, links and occurrence time in native evidence; taxonomy Entry projection — the same IDs and provenance at default CLI intake; disposition — exact ID, selected family/rejection and reviewed rationale in committed state; shared instruction — the canonical transport distinction and its generated Codex projection; native assignments/results — actual authority/source reads and remote stop in full traces; prevention receipt — executable parent check rejects the old result and accepts only the expected case behavior. Applicable views: the source-linked flow in SYSTEM_MODEL.md and the case evidence shown in the final conversation; no new product UI is added. Freshness checks: compare consumed record content/provenance to source, run the disposition verifier and generated AGENTS sync, and bind execution evidence to exact revisions. Reconcile the model, the existing feedback diagram status caption, proposal links, parent receipts, reviewed state and .project-brain/now.md in this same change. Existing licensing/recurrence logic is unchanged and is not shown as freshly proven.

## Capability reuse

> **CORE-CAPABILITY-REUSE** (blocking): The plan answers capability reuse against the capability catalogue in agentic-capability-architecture-canonical, which has two files: `reuse_candidates.yml`, whose entries under `candidates:` are cross-project capabilities with their selected off-the-shelf implementations, each named by its `id` (for example `documents_to_text`) and marked candidate or promoted; and `capability_registry.yml`, whose entries under `capabilities:` are the packages that repository holds, each named by its key (for example `approvals`) with the capability ids it `provides` (for example `approval.resolve`). An entry from either file counts. The plan names each catalogue capability the work reuses, by its id, key or provided id; names each new capability the work adds together with its first consumer (the project, command or workflow in this plan that uses it); and, where no entry covers what the work needs, states `No catalogue entry fits, because <reason>`, the reason saying what the work needs that no entry provides. A plan may give more than one of these answers. A plan fails this item if it gives none of them, if it claims reuse without naming the catalogue entry or id reused (reusing code or a contract that is not a catalogue entry does not count), if it adds a capability without naming its first consumer, or if it says no entry fits without a reason.

Inspected agentic-capability-architecture-canonical/reuse_candidates.yml (3 candidates) and capability_registry.yml (4 packages). No catalogue entry fits, because this work needs an existing agent-feedback JSONL projection into an existing failure-taxonomy consumer and instruction-scope repair; approval_action_workflow, documents_to_text, Twitter search, core/approvals/scheduling/notifications do not provide that seam. No catalogue entry is claimed as reused. The listed AES records.py/feedback_log/subagents, native role result schema, taxonomy_feedback_pass.py/state and instruction renderer are existing owner-local code seams, not catalogue entries; extending them adds no catalogue package. The only added consumer capability is current-feedback intake in the existing taxonomy reviewer; its first consumer is the existing taxonomy-feedback service/default CLI. No generic workflow engine, new database, new LLM client or new policy router is introduced.

## Authority and non-goals

> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).

Brian's “proceed” authorizes the scoped plan and reversible implementation; the root session owns both claimed lanes and integration. AES owns its canonical CLAUDE.md and generated AGENTS.md; agent-skills owns the taxonomy reader and durable dispositions. Non-goals: changing automatic agent routing/model selection, child permissions, global hooks, role contracts, taxonomy growth from one episode, shared claim implementation, licensing thresholds, unrelated historical backlog, benchmarks or public disclosure of raw/private feedback. The existing keyed concerns provide the checkable feedback path for a wrong instruction change.

## Irreversible actions and spend

> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.

No destructive operation, migration, external announcement or publication of private data. Routine recoverable commits/pushes/merge and refresh of the existing private local reader are covered by workspace authority. Brian's standing configured-model authority and this scoped approval cover routine Company Planning checks, one bounded taxonomy semantic decision, and two bounded native role cases, plus one corrected negative rerun after the first parent expectation proved wrong; each native assignment is read-only with at most 12 turns and no model override. Use the approved shared llm_client OpenRouter route for semantic checks, max_budget 0.05 USD per light call and at most 2 USD for this bounded plan/check/disposition work; stop on quota/billing errors, do not cap tokens or retry them away. Native usage remains its configured route. No paid comparison or broad evaluation is authorized or required.

## Uncertainties

> **CORE-UNCERTAINTIES** (blocking): The plan lists its material uncertainties, and each one has an owner or the evidence that would resolve it.

Root owns projection compatibility: resolve from an authentic existing report plus malformed/duplicate/provenance regression cases before broader cleanup. Root owns semantic family coverage: inspect all existing detecting questions with one traced review; use covered or novel_candidate truthfully, never manufacture a second independent instance. Root owns transport behavior: native positive and remote-required negative traces settle whether the scoped instruction acts. Remote MCP connectivity itself is outside this proof: tools are now advertised, but the negative task prohibits network calls and must stop before local substitution; do not claim a live remote device connection. Root owns federation/landing: retain one canonical plan in AES, use configured federated plan lookup or an explicit native plan-root binding for the agent-skills commit; never copy a second authoritative plan. All choices are agent_decided_reversible; no material human decision remains.

## Activation facts

> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend. claims_external_standard is triggered when the plan claims, or presents its work as, following, implementing or conforming to a standard, schema or contract owned outside the repository being changed (for example a model presented as DM2, or output said to match a published schema); conforming to the repository's own contracts does not trigger it; aes_governed_target when the target repository is governed by an AES target (`.aes/target.yaml`). These two facts are optional: an undeclared one is shown as false and is judged like a declared false.

crosses_system_boundary=true: AES feedback records are consumed by the separately owned agent-skills reviewer, without mutating their producer contract. deploys=true: refresh the existing private taxonomy-feedback runtime from the merged committed reader, with unchanged service configuration. shared_mechanism=true: extend the reusable taxonomy intake seam. llm_central=true: actual semantic disposition and native role behavior are necessary evidence. empirical_comparison_proposed=false: canonical acceptance and negative regression cases, no comparison of designs/models. irreversible_or_spend_action=true: routine approved semantic/native checks incur configured usage, but no irreversible operation. claims_external_standard=true: native result must satisfy the agent-skills DevelopmentInvestigationResultV1 schema. aes_governed_target=true: AES has .aes/target.yaml; this work changes no target-governed src or tests/greenfield artifact.

## Prior art and ownership

The complete bounded candidate list is: AES collector/daily reports — reuse; AES records.py and feedback_log — reuse; AES subagents native adapter/checker — reuse; agent-skills taxonomy Entry reader — extend; legacy Project Meta register reader — reuse; taxonomy disposition state and verifier — reuse; canonical CLAUDE/AGENTS renderer — reuse; W3C PROV attribution already used by the accepted subagent design — compose; catalogue approval_action_workflow, documents_to_text, twitterapi_io_search_candidates_wrapper, core, approvals, scheduling and notifications — bounded exception: excluded from this one repair, with the common reason that none provides feedback JSONL intake or transport-scoped repository authority. No other candidate was found in the bounded source/catalogue search, and none is superseded.



> **OV-PRIOR-ART-DISPOSITION** (blocking): Existing ownership, internal lineage, and relevant external prior art were searched, and each candidate found is dispositioned as reuse, extend, compose, supersede, or bounded exception.

> **OV-PRIOR-ART-PARALLEL-CHECK** (advisory): The plan names one concrete structural check or consumer-path observation that would detect a silent parallel implementation of the same concern.

Inspected current collector/projection and consumer implementation, native original trace, official claims, Project Meta capability-owner index and the vision ideas register's per-skill feedback/typed-outcome/authority-scope entries. Extend the existing agent-skills Entry/disposition seam to consume the current JSONL contract; retain legacy register reading for historical entries. Reuse FEEDBACK_OUT and the collector's daily append-only reports rather than re-enable retired legacy writes or mirror the private log into another store. Reuse canonical instruction projection and parent verification; scope the existing Remote MCP rules rather than create a remote-access framework. External prior art: the existing accepted W3C PROV entity/activity/agent attribution used by the subagent-feedback plan (https://www.w3.org/TR/prov-primer/); compose its already adopted provenance approach, no claim of PROV conformance or new ontology. Catalogue candidates are dispositioned above. No new runtime framework or algorithm is needed.

Inspect the scoped git diff for absence of a new feedback store/legacy writer; assert the authentic record's original ID/sentence/links survive into the existing default consumer and durable disposition. This directly detects a parallel queue or a generated report that never read the new source.

## LLM call boundary

> **OV-LLM-CALL-BOUNDARY** (blocking): The plan describes the model call graph, the structured result boundary each call returns, and how calls are traced.

> **OV-LLM-AUTHORITY-PROMOTION** (blocking): The plan names the provider and spend authority for model calls and one authentic-run condition that must hold before the behavior is promoted.

Graph: parent → existing Company Planning typed semantic checks; parent → one shared llm_client structured taxonomy judgment using all current families and the actual linked source record; parent → two native development-investigator assignments → existing DevelopmentInvestigationResultV1 JSON Schema validation and executable source/result checks. Taxonomy call returns a Pydantic judgment with status, family or null, source_record_ids and a rationale; only code validates and writes its exact IDs/rationale into existing state. Models never author evidence URLs. Native role inherits configured model/effort; parent reports unknown metadata as unknown. Keep full semantic task/trace IDs, arguments/results and usage, and full native parent/child traces; output status alone is not evidence.

Brian authorizes the configured native route and approved OpenRouter/shared-client routine calls through his scoped “proceed” and workspace policy; no provider/model override. Promotion condition: actual default consumer reads the authentic source sentence, semantic disposition is source-grounded and validator-accepted, native source inspection now proceeds, and the remote-required negative case remains blocked. This promotes only the input repair and scoped instruction fix; it does not promote role trust, new taxonomy families or automatic selection. Full traces must support these conditions before integration.

## Coordination

> **OV-COORD-OWNERSHIP** (blocking): The plan names exact ownership, dependencies, conflict surfaces, the integration owner, and the work-unit evidence for each concurrent writer.

Work-unit evidence and conflict surfaces: FP-AES is root's sequential instruction/case unit, branch feedback-prevention, evidenced by retained repair commit d5163ee53ac30e2ba43ce61d38bf071626b4f249, full local gate commit 236ba7aa167b0277a2006591fbf1b8667bdac67b, and private repair-verification.jsonl:57. Its exact write surfaces are the AES repository_path rows in front matter. FP-INTAKE is the same root's sequential reader/gate unit, branch feedback-taxonomy-intake, evidenced by pushed a6b41b461c0ff4e4888f765bb076af8e01bb0aa8 and repair-verification.jsonl:58-59; its exact write surfaces are the Agent Skills repository_path rows in front matter. These are bounded work units described here, not WorkUnitGraphV1 records or delegated tasks. The admission receipts are the official coordination claims for scopes feedback-prevention and feedback-taxonomy-intake, checked through project-meta/scripts/meta/check_coordination_claims.py, not mailbox messages.

The only concurrent writer this repair consumes is codex:01a1198b-539e-7d32-8dc4-7fe62cc903d9. Its independently adopted harness-mailbox-repair support unit exclusively owns tests/test_manage_client_config.py in worktrees/harness-mailbox-repair under scope harness-mailbox-support. Work-unit evidence: exact ready blob c0e67a2:tests/test_manage_client_config.py, owner-reported 21/21 tests, PR agent-skills #461, and the official live support claim. Its parent exclusively owns contracts/client-config/hook-manifest.v1.json and proposals/harness-mailbox-repair under scope harness-mailbox-repair. Root writes none of those paths while they are claimed; this gate repair does not adopt or revise that independent work. The dependency is integration/readback of the test-only fix after sanctioned release or merge, and the manifest's integrated behavior is checked separately. AES capability-catalogue owns wiki/index.md; root used already-owned CLAUDE.md links instead. Other AES rules-sort/worktree-lifecycle claims are unrelated writers with no assigned work under this plan, not additional implementation dependencies. Native feedback_canary only reads the packet's allowed paths and owns no writes. Root is the integration owner of FP-AES and FP-INTAKE; the harness agent remains integration owner of its mailbox unit.

One root writer, session codex:01a11cac-2557-7dc0-8edd-8487ed5968d1, owns AES worktrees/feedback-prevention (this proposal, CLAUDE.md/AGENTS.md, needed instruction projection/verification files and .project-brain/now.md) and agent-skills worktrees/feedback-taxonomy-intake (scripts/taxonomy_feedback_pass.py, tests/test_taxonomy_feedback_pass.py, taxonomy_feedback_state.json and README.md). Official sanctioned bootstrap receipts and claims list are ownership evidence. Existing capability-catalogue, rules-sort/agent-router, worktree-lifecycle and harness-mailbox-repair claims do not overlap these paths and are preserved. Native role cases are read-only with no write claim; reuse the existing canary agent if available. No delegated implementation; root sequentially owns the exact gate-repair test/fixture paths listed in front matter after a claim refresh. The independently owned tests/test_manage_client_config.py correction is a narrow dependency: preserve its claim until the owner confirms sanctioned release or merges it, then integrate its exact test-only bytes. No work graph is needed for root's sequential linked lanes. Root integrates reader first, then its source-linked AES case evidence/instruction repair, with merge commits preserving the recorded subjects.

## Standard conformance

> **OV-STANDARD-CONFORMANCE-RULES** (blocking): The plan names each external standard, schema or contract the work claims to follow (for example DM2, a JSON Schema, or an API specification), where its machine-readable rules live (file path or URL, for example a DM2 pack's role-expected-type constraints), and which of those rules the work's artifacts must satisfy. Where the standard publishes no machine-readable rules, the plan says so and names the written rules its check will encode instead.

> **OV-STANDARD-CONFORMANCE-GATE** (blocking): A named check tests the work's artifacts against those rules and runs in the merge or release gate (the plan names the command and the gate step that runs it), not only once by hand. The plan's disproof includes: an artifact labelled as conforming to the standard violates one of its rules. Anything the work adds beyond the standard (extra roles, types or fields) is labelled as an extension in the artifact and in the plan, never presented as part of the standard.

The AES Record contract publishes machine-readable Pydantic validation in scripts/learning_loop/records.py; it publishes no whole-report JSON Schema. The reader encodes its consumed written rules: report/record IDs and nonempty text must be strings; records and evidence links have their declared structural types; provenance is retained; repeated IDs with differing substantive payloads fail; identical replay IDs deduplicate. It is explicitly a taxonomy-specific projection, not full report conformance. External contract: agent-skills/contracts/specialists/development-investigation-result.v1.schema.json, Draft 2020-12 machine-readable DevelopmentInvestigationResultV1 rules. Both native role returns must validate their required fields, status, evidence objects and mutation declaration; parent also binds task identity, source citations and expected case behavior. The current feedback-report.v1 producer contract is AES scripts/learning_loop/records.py; the reader consumes a labelled taxonomy Entry projection of its ID/kind/text/links/provenance, not an object advertised as a complete external report. Added Entry provenance and taxonomy-specific fields are consumer extensions, never part of the native role or producer schema.

Disproof for this gate: an artifact labelled as conforming to the external standard violates any of that standard’s rules. Exact conformance command: python proposals/aes-feedback-prevention/verify_case.py --packet <packet> --result <result> --expect supported|inconclusive. It runs as the VS-FP-TRANSPORT step of this plan’s merge gate before PR merge, alongside the final make check, and records schema validation plus behavioral rejection/acceptance for the actual cases. It also has a --self-test mode that rejects invalid native result shapes and the wrong expected status. The new provenance fields in the consumer evidence are labelled projection_extensions; the plan labels them taxonomy-specific extensions. Merge gate includes executable parent JSON Schema validation using jsonschema.Draft202012Validator against the actual installed role schema, plus task/result/source checks for feedback-prevention-v1. Retain these check inputs, argv/output/exit and exact schema digest with the final gate receipt. Focused reader regressions and the agent-skills make test gate verify required source fields, malformed inputs, duplicate content conflicts and exact provenance preservation. AES make check verifies regenerated authority parity. Invalid role JSON or the original inconclusive result presented as native-positive must fail; no fixture-only conformance claim is accepted.

## AES target

The governing target is `.aes/target.yaml`. Explicit verification-subject mapping: R1 → VS-FP-INTAKE (default taxonomy command and tests/test_taxonomy_feedback_pass.py); R2 → VS-FP-DISPOSITION (same command --verify-dispositions and traced semantic review); R3/R4 → VS-FP-TRANSPORT (python proposals/aes-feedback-prevention/verify_case.py --packet <packet> --result <result> --expect supported|inconclusive and full child traces) and VS-FP-PARITY (python3 scripts/meta/check_agents_sync.py --check); R5 → VS-FP-LOCAL-GATES (AES make check and agent-skills make test/check). All five operational subjects serve SC-TR-001/TR-REQ-001 and the original target VS-TRACE-REVIEW; R5 additionally serves SC-AP-001/SC-AP-002 through VS-AP-COMMIT-RULE and VS-AP-PLAN-RECEIPT. These are additional plan-local operational subjects, not a target delta.



> **OV-AES-TARGET-TRACE** (blocking): The target repository is governed by an AES target (`.aes/target.yaml`). The plan maps each of its requirements to the target's normative items and success criteria, each with a verification subject. Where the work adds to or changes the target, the plan declares that target delta, including running things (files, services, containers, agent rules), and gives the passing result of `aes plan validate` for its proposal; where it changes none of the target, it says so and names the existing target items or success criteria its requirements serve.

No .aes target delta: no files under target-governed src/agentic_engineering_system or tests/greenfield and no target component/service/container is added or changed. The instruction-scope correction is repository operational authority, not a new target implementation root. R1/R2 serve RU-AES-PLANNING, TR-REQ-001/SC-TR-001 through source-linked default intake and disposition verification; R3/R4 serve the same trace-review requirement through real role instruction/result traces and generated-authority sync; R5 serves RU-AES-COMMIT-RULE, SC-AP-001/SC-AP-002 with adopted-plan commit and completion binding. Existing verification subjects VS-TRACE-REVIEW and VS-AP-PLAN-RECEIPT remain in the required AES make check; focused reader and native case checks are this plan's additional operational subjects. No target proposal or aes plan validate is needed because the target is unchanged.

## Execution observations within the adopted scope

Brian selected “Repair the shared test gate (Recommended)” on 2026-10-09 after the focused feedback checks passed and the full Agent Skills suite failed. This bounded prerequisite is AS #459, independently reproduced by the harness-mailbox agent. Extend R5 with VS-FP-GATE-REPAIR: change only test fixtures and their expectations, then run every changed test module and the full Agent Skills make test/check gates. The original 465-test baseline had six failures and 73 errors (private repair-verification.jsonl:59); the repaired combined head 80e08cb7b8131321fab7cee9ef0e3371859c28a7 passed all 466 tests with zero failures/errors (private repair-verification.jsonl:75). AES make check passed 340 tests, one skip and mypy at revision 236ba7aa; no AES executable code changes are planned for this prerequisite.

Repair the root fixture mismatch: synthetic Git histories must use truthful allowed commit tags while retaining the installed commit hooks; neither disable hooks nor weaken commit enforcement. Installer/client-config tests must distinguish recorded disabled hooks from active declarations, preserving Brian's disabling decision. Feedback logger tests must isolate the client-home input actually consumed by main, rather than patch a derived LOG_DIR that main replaces. Hosted-CI tests must verify the manual-only workflow and local pre-commit contract rather than restore automatic runs. Restore named target and adjacent trigger fixtures for the seven automatic skills missing them, without changing their instructions or claiming a model routing score. Historical Work Market tests must run the archived planning scripts with their own archived authority, rather than launch the current external package through a forwarding wrapper. These are deterministic repository checks; there is no new evaluation, benchmark, model choice or shared planning-policy change.

Ownership remains the existing root's claimed Agent Skills lane for the exact added test/fixture paths in front matter. tests/test_manage_client_config.py remains under the independent harness-mailbox-support claim; do not write or claim it until its owner confirms sanctioned release. The owner's ready test-only blob c0e67a2 is supporting evidence, not permission to import the manifest or whole commit. Integrate that independent fix only after release or its ordinary merge; then rerun its tests against the integrated manifest. Root remains integration owner of this repair. Shared hooks, client-config code/manifests, Company Planning source and live settings are outside this increment.

Gate-repair success is that destructive-command history tests exercise actual commits and still reject data loss, disabled hooks remain absent from installed configuration, feedback written through the selected client is read from that isolated client home, workflow triggers remain manual-only, all automatic skills have explicit target/adjacent cases, and archived planning checks validate only their archived inputs. Disproof is a green suite obtained by skipping failing tests, suppressing hooks, restoring disabled controls, or grading a different planning version. The full gate run's argv, revision, stdout, per-step duration and exit status are retained in repair-verification.jsonl; read all failing assertions and a sample of passes. Model/view freshness: SYSTEM_MODEL.md needs only the gate evidence added after verification; its feedback entities and transport flow are unchanged by these fixture repairs. Update the plan's completion evidence and PR bodies with actual counts, never presumed success.

The authentic intake exposed four retained taxonomy_changed dispositions bound to the same historical taxonomy digest. That digest is verified at agent-skills revision f1afe816bd43cda14e1a082449c9a5c7e47b3cf4; history validation now accepts retained decisions only when their bytes remain in Git, while a new observed change still requires the current digest. No historical disposition is rewritten. Default input emitted the exact original record, including occurrence time and trace links; one traced semantic review covered all 22 current families and selected N. The first remote expectation assumed missing tools; actual metadata showed them advertised. Its verifier failed, and a fresh no-network remote case was declared before execution and stopped at the required readiness/ping boundary. These corrections change neither the target scope nor licensing and recurrence thresholds.

## Contracts and dependencies

> **OV-CONTRACTS-SCHEMAS** (blocking): For each system boundary the plan crosses, it names every schema or contract the crossing uses or changes, with its owner and its file or URL, and says whether this plan changes it.

GitHub owns BranchProtectionRule, UpdateBranchProtectionRuleInput and the main branch-protection REST representation (https://docs.github.com/en/graphql/reference/branches and https://docs.github.com/en/rest/branches/branch-protection). These API contracts are consumed unchanged: one existing policy value changes, not any schema. R5 checks exact before/after field membership and the tested source commit ancestry. AES owns feedback-report.v1 and its Record, Link and Provenance Pydantic definitions in scripts/learning_loop/records.py, emitted inside daily report JSONL by feedback_log.py; consumed unchanged. Agent-skills owns the internal Entry dataclass and taxonomy-entry-projection/v1 extension in scripts/taxonomy_feedback_pass.py; this plan extends that owner-local projection with original evidence links and provenance variants, not the producer's Record schema. Agent-skills owns taxonomy-feedback-evidence/v1 and current-batch.json in that same reader: additive per-entry content hashes bind its existing verifier to the observed batch. Existing disposition keys/statuses in taxonomy_feedback_state.json remain unchanged. Agent-skills owns contracts/specialists/development-investigation-result.v1.schema.json; native children produce this unchanged schema and the AES parent checker consumes it. Company Planning owns contracts/method-conformance/planning-method-conformance-receipt.v1.schema.json, contracts/planning-path/planning-path-decision.v1.schema.json and contracts/execution-loop/plan-execution-cursor.v1.schema.json in the pinned 9411224 runtime snapshot; these adoption receipt, PlanningPathDecisionV1 and execution cursor schemas are consumed unchanged. No role, producer, external schema, licensing or recurrence contract is changed.

Landing order:

> **OV-CONTRACTS-DEPENDENCIES** (blocking): The plan names the dependencies on each side of every boundary it crosses (what produces and what consumes each schema or contract) and the order in which the changes land so no consumer breaks in between.

AES feedback_log/records produces daily feedback-report.v1 records; agent-skills load_feedback_entries projects them into Entry, emit_observation produces taxonomy-feedback-evidence/v1/current-batch hashes, the existing semantic reviewer produces dispositions, and verify_current_batch consumes those dispositions plus observed source hashes. The legacy Project Meta register remains a parallel reader input. Native development-investigator produces DevelopmentInvestigationResultV1; AES verify_case.py consumes it with frozen allowed source hashes and case-specific required citations. Canonical CLAUDE.md produces generated AGENTS.md through the existing renderer. Company Planning method_conformance/cli.py adopt produces the adoption receipt consumed by the AES commit rule and native execution supervisor. Company Planning planning-path declaration produces PlanningPathDecisionV1, consumed by method-conformance compile/adopt. Native execution-state start/replace produces the PlanExecutionCursorV1 consumed by plan_execution_supervisor.py and check_execution_cursor_boundary.py; these planning-control seams remain unchanged. Land the adopted AES plan and transport repair first; retain its source/receipt as the single cross-repository authority. Then land the backward-compatible agent-skills reader and exact disposition; refresh its existing private runtime last. Neither side requires a producer migration: old sources/API calls and existing batches without new hashes remain readable. Older consumers ignore the additive projection fields; no consumer expects an altered Record or specialist result schema.

## Deployment

Integration prerequisite discovered after full local verification: Agent Skills permits merge commits at repository level, but its main branch requires linear history. GitHub rejected PR #460 with “Merge commits are not allowed”; rewriting these commits would discard the identities cited by native evidence. Existing workspace history preservation governs this reversible technical decision. Change only BranchProtectionRule BPR_kwDOTEL1cs4E5Tup (pattern main), requiresLinearHistory true → false, using GitHub GraphQL updateBranchProtectionRule; keep every other branch-protection field unchanged. The published API explicitly supports this one-field update (https://docs.github.com/en/graphql/reference/branches#updatebranchprotectionrule). GitHub rule state is an additional model element relied on at R5 integration, not a new code or role contract.

Record the complete branch-protection snapshot before and after in private repair-verification.jsonl; normalize API metadata only and assert the only policy delta is required_linear_history.enabled. Exact deployment operation: gh api graphql with updateBranchProtectionRule(input: {branchProtectionRuleId: "BPR_kwDOTEL1cs4E5Tup", requiresLinearHistory: false}). Live checks: REST readback of main protection, unchanged force-push/deletion/admin/review restrictions, ordinary PR merge, and Git ancestry membership of the tested 80e08cb7b8131321fab7cee9ef0e3371859c28a7. Failure/disproof: any unrelated protection changes, or the merged history cannot reach that tested source revision. Rollback is the same one-field mutation with requiresLinearHistory true; never rewrite or delete history. A keyed feedback concern records this control mismatch and its readback. This is within existing implementation/merge authority and adds no actor access. No new general merge policy, bypass flag or forced push is used.

> **OV-DEPLOY-PLAN** (blocking): For each deployment the plan makes, it names the target, the command or script that deploys, the live check that proves the new version is serving, and the rollback.

Target: the existing private checkout ~/.local/share/ecosystem-runtime/taxonomy-feedback/agent-skills used by taxonomy-feedback.service. The service was checked inactive and its checkout clean at c5c8a988e024b7a378af46c0715bc41766964adc. After merge, recheck both conditions, git fetch origin, then git checkout --detach <verified merged commit>; do not force or discard any dirty work. The service already fetches/checks out origin/main before each scheduled run; service configuration is unchanged. Live check: run that deployed checkout's default emit-observation command with the exact originally failing record ID selected explicitly for bounded replay, inspect its original text/links/provenance in emitted evidence, read back its code/HEAD and verify the committed original case disposition. Use a separate bounded private smoke state so the production review batch is untouched. Rollback: revert the reader change through a normal recoverable source commit/merge and refresh this checkout to that verified revert; a temporary detached checkout of the retained pre-deploy revision can also establish the previous behavior, but is not a persistent rollback because the service follows origin/main.


## Verified integration outcome — 2026-10-09

AES PR #479 merged as ba8e49744e428974b1a1b5f9b8a1b83fa9b6b19d, retaining instruction source d5163ee53ac30e2ba43ce61d38bf071626b4f249 and AES gate source 236ba7aa167b0277a2006591fbf1b8667bdac67b. Agent Skills PR #460 merged as d709bcf527dd861734dafa888460795ed0b66217 with tested head 80e08cb7b8131321fab7cee9ef0e3371859c28a7 as its second parent. The exact GitHub protection readback showed only required_linear_history.enabled true → false, with every other protection field equal (private repair-verification.jsonl:76). The clean inactive service checkout was refreshed to d709bcf; its default reader emitted the original record with all content/qualifiers/provenance preserved and its committed disposition verifier passed (private repair-verification.jsonl:77). No service configuration, producer schema, permissions or model route changed. See completion-evidence.json for revision-bound outcomes and remaining shared-tool follow-ups.
