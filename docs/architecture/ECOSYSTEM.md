---
description: Adopted ecosystem consolidation direction, first legacy-source review, evidence limits and next reading sequence
status: current
doc_role: supporting_context
last_checked: 2026-11-14
---

# Ecosystem capabilities and predecessor review

Tracking: [AES #856](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/856).

## Outcome and authority

A person or agent should find an existing capability, its provider, exact input
and output contracts, consumers and evidence from one discovery route. Each
project can consume existing capabilities and contribute new reusable work.
Source: Brian's 2026-11-13 explanation and approval recorded in
[Decision 0014](../decisions/0014-ecosystem-consolidation-and-legacy-review.md).

AES owns this consolidation and review. Implementations, provider metadata,
schemas, dataset custody and observations retain their native owners. This page
owns the first-pass review and design discussion; accepted choices belong in
Decision 0014, and unresolved work in the existing [question ledger](../planning/open-questions.json)
(Q36–Q42). Proposed donor dispositions below are judgments, not completed
migration or authorization to restart old machinery.

## A concrete discovery journey

A project needs documents turned into claims. From one entry point, it should
find the semantic job, compare provider options, inspect a versioned output
schema, see which consumers accept it, and open evidence for a particular
provider/consumer connection. A dataset catalogue may locate its input files;
a runtime tool registry may make the chosen callable available to an agent.
These are connected capabilities with distinct responsibilities.

The same journey must work for other jobs: model access, file conversion,
planning, approval, scheduling or retrieval. Claim extraction is an example,
not the definition of the catalogue's domain.

## Current mismatch

The accepted AES [Decision 0012](../decisions/0012-capability-reuse-enforced-at-plan-adoption.md)
selects ACA's two-file catalogue. The later workspace [Decision 0004][workspace-list]
selects a workspace jobs/tools list. Project Meta's [registry architecture][pm-architecture]
locates its semantic catalogue in Project Meta. These concern partially distinct
levels, but repeat discovery and ownership decisions without a common update path.

Company Planning's [bounded-design instructions][planning-reuse] still require
ACA catalogue reuse and say reused code outside it does not count. ACA's inspected
files contain four package groups and three reuse candidates; Project Meta has
60 semantic catalogue entries and 24 ownership entries. Its 60 capability records
all link to one of ten ownership families, so differing IDs here are intentional
levels, not evidence of 60 broken joins.

The ecosystem-ops implementation already describes itself as a derived view;
Decision 0012's statement about competing self-described authorities is historical
context, not an accurate description of that current module's stated role.
It still reads the old sources. Its [loaders][merged-view] return empty results
for absent/unreadable/invalid inputs, and its output omits catalogue-only entries.
It can therefore obscure both known capabilities and source failure. These are
source-inspected failure paths, not observed production incidents.

The earlier local comparison found 31 of 64 distinct Project Meta boundary
bindings in the 36-contract runtime snapshot updated November 5. This is dated
snapshot coverage, not proof that 33 providers are absent or broken. Private
runtime data is not copied into this public review; reproduce against an explicit
local snapshot if this comparison is needed for migration.

## Target division of facts

| Fact | Authoritative home | What the discovery view shows |
| --- | --- | --- |
| Semantic job and cross-project selection/disposition | AES-owned integration decision, linked catalogue identity; final storage/provider is Q36 | Stable ID, aliases, purpose, alternatives and decisions |
| Callable/API/package identity and description | Provider source or native manifest | Owner, exact revision/version, invocation route, inputs/outputs |
| Payload schema and semantic checks | Natural contract owner, including data-contracts where appropriate | Versioned schema references and explicit compatibility/adaptation claims |
| Dataset and snapshot custody | Dataset manifest and data_library's native sources | Input asset references and resolution/verification states |
| Consumer relationship | Consumer dependency/configuration plus separate runtime evidence | Declared, source-inspected and observed use as distinct states |
| Strategic owner versus operating custody | Owning decision versus native operational records | Who maintains it versus who can operate/recover it |
| Availability, compatibility and effectiveness | Revision-bound observations | What was checked, when, where, limitations and stale/unknown/error |

One discovery route does not require one universal runtime or one file. Names
alone cannot establish schema compatibility, provider suitability or invocation
readiness. Import-dependent tool registration is one source of metadata; it must
not hide packages that were not imported, external services or non-callable jobs.

## First reading: what is worth carrying forward?

This is a bounded review of the cited documents and implementation seams at the
pinned source revisions. It is not a complete review of any donor repository.
Current use establishes dependencies; proposed dispositions assess value and fit.

| Source | Best idea or information to preserve | Concern and proposed disposition |
| --- | --- | --- |
| [Project Meta registry architecture][pm-architecture] | Separate capability, implementation/tool, action, schema, ownership, custody and views; use stable identities to connect them. | **Adapt** distinctions into AES. Reconcile its old global-authority claim; do not clone every layer as a new service. |
| [Project Meta semantic catalogue][pm-catalog] | Capability/family IDs, explicit provider bindings, evidence and source pointers. | **Adapt** unique entries with aliases and provenance. Recheck readiness instead of copying status. |
| [Ownership registry][pm-ownership] | Current host versus intended owner; provisional decisions, migration gates and blocking uncertainties. | **Adapt** strategic decisions separately from observed consumer use. A known-consumer label is not fresh execution proof. |
| [ecosystem-ops merged view][merged-view] | Joins tool and contract facts and exposes expectation gaps. | **Reuse/adapt candidate** as a view, not selected yet. Fix error-to-empty collapse, omitted catalogue-only records and bare-name joins before relying on it. |
| [ACA package registry][aca-registry] and [manifest catalogue tool][aca-tool] | Versioned package metadata, invariant notes and real source-target resolution. | **Keep native metadata; adapt exporter** as one source. AST target resolution does not establish installation, typed compatibility or successful invocation. |
| [ACA reuse candidates][aca-candidates] | Candidate versus observed evidence; limitations, rejected promotion and uncertainty preserved explicitly. | **Preserve** these distinctions. An implementation selected for future confirmation is a candidate, not ready software. |
| [data-contracts architecture][contracts-model] | Shared schemas and pure validation stay separate from discovery and execution. Minimal graph records required contracts and producer outputs. | **Keep contract ownership; consider minimal graph** for a plan view. Rich action/composition machinery remains optional until a consumer needs it. |
| [Source-claim locators][claim-locators] | Exact source hash and span, optional transcript placement, explicit withheld/set-aside records. | **Keep domain seam; adapt evidence pattern** where useful. A locator establishes source identity, not truth or readiness. |
| [data_library resolver][dataset-resolver] and [prompt discovery][dataset-readme] | Portable snapshot identity, remote versus materialized state, exact source revision and discovery without copying source authority. | **Keep dataset owner; adapt source-owned revision-bound discovery pattern.** A schema-reference string does not prove compatible consumption. |
| [llm_client tool metadata][tool-metadata] | Registration beside implementation, input/output type information and duplicate-name checks. | **Keep runtime owner; adapt metadata export.** Session activation and keyword search are not a complete ecosystem catalogue or suitability test. |
| [Project Meta policy system][policy-system] | One discoverable system map, native owners, coverage boundaries and explicit gaps. | **Salvage information needs.** Its old global entrypoint must eventually route to AES; do not import outdated claim/mailbox authority. |
| [Enforced Planning operating model][ep-model] | Outcome-first slices, uncertainty-sensitive planning, candidate/canonical evidence and consumer-boundary acceptance. | **Compare with Company Planning before adding.** Many principles already exist in AES; preserve rationale without a duplicate planning hierarchy. |
| [Project Meta policy registry][policy-registry] | Intent, scope, source, honest enforcement status, feedback route and maintenance triggers. | **Adapt selectively.** Do not activate legacy rows by importing them or treat a disposition hash as semantic/enforcement proof. |
| [Concern lifecycle decision][concern-lifecycle] | Stable concern identity, verifier-owned closure on a landed revision, recurrence reopening and feedback machinery checking itself. | **Adapt principles; integration unresolved.** A real attempted repair was rejected because the recurrence proof also passed on the broken revision. |
| [Earlier AES predecessor harvest][old-harvest] | Non-success states, recovery, legitimate counter-cases and parent verification. | **Preserve already adopted clauses; review residuals.** Do not resume the old supervisor, adapters or Plan 16 from historical next steps. |

## Concerns and recommendations

1. **Identity:** qualify provider/tool/action names and versions. The current merged
   view indexes some metadata by bare name; collisions can overwrite unrelated facts.
   Preserve legacy IDs through aliases and an explicit migration mapping.
2. **Coverage:** distinguish a known job, candidate provider, source-resolved target,
   runnable provider, adopted consumer and fit for this requirement. Preserve missing,
   unknown, unavailable, stale and error states rather than returning an empty success.
3. **Update path:** generate provider descriptions/contracts from owning sources.
   Author cross-project fit decisions once. A central hand-maintained copy would
   reproduce the fragmentation even if it were stored in AES.
4. **Reuse:** judge a donor against the ecosystem outcome and its guarantees, not
   popularity, historical investment or mere current use. Keep context and rejected
   fits so a later project can reuse knowledge as well as implementation.
5. **Governance:** Enforced Planning's old claim-first instructions conflict with
   current native worktrees and ship. Keep useful planning semantics; flag and route
   stale entrypoints before another agent treats them as current authority.
6. **Controls:** keep policy intent separate from configured, delivered, executed and
   effective machinery. Exceptions, legitimate passes, recovery and retry must survive
   consolidation. Existing AES feedback/policy concerns remain open.

## Second reading: concern identity, repair and recurrence

This source review covers Project Meta's accepted 2026-09-14 concern-lifecycle
decision, `feedback/concern-repair.yaml`, and the observer/verifier at the pinned
Project Meta revision [f1e27c9][concern-code]. It also reads AES's
`scripts/learning_loop/fix_owner.py`, `effects.py` and the relevant effects stage
in `problems.py` at AES revision [268d58e][aes-review-revision]. This is code and
design inspection, not a new live run.

| Concern | What the sources establish | Limit or recommendation |
| --- | --- | --- |
| Identity and evidence | Project Meta's decision chooses GitHub Issues as the shared concern register, with a stable key in the issue body; native stores keep evidence. AES separately derives problem IDs from its feedback members and looks up closed issues by a `concern-key` body marker. | Preserve the stable-key plus native-evidence split. Do not assume these IDs are already the same namespace or that two issue systems are one register. Define key ownership and cross-links before composing them. |
| Closure | Project Meta's concern-repair verifier says it checks the report, changed prevention paths, a recurrence proof that fails on the observed revision and passes on the fix, a green source signal, and an independent root-cause review. After landing it checks for a passing record tied to the exact tree and rechecks the source signal. | This is a stronger closure contract than issue state or receipt presence. The decision itself records a real attempted repair rejected because its recurrence proof also passed on the broken revision. That is direct counterevidence that a verifier-shaped workflow can still have a weak proof. |
| Live evidence | The same decision records one live repair attempt rejected at that recurrence gate; it also says that a repair passing every gate, landed closure, and a Codex run had not yet been observed at that decision's date. | Treat those as dated observations, not present-day deployment status. The reviewed source revision describes intended gates; this review did not query current timers, run a repair, or establish a successful end-to-end cycle. |
| AES receipt check | AES accepts an issue receipt when its comment contains parseable JSON with a timezone-aware `enforced_at`, a nonempty revision and verification reference, and the comment was created at or after that time. Fix-owner also checks the disposition and issue close reason. | These are structural checks on the comment and issue fields; this code does not open the referenced revision or execute the referenced verification. A valid receipt marker is therefore not equivalent to independent verifier evidence. |
| Recurrence | AES effects separates records around the receipt timestamp, ignores later restatements linked to an earlier incident, counts later sightings, revokes a licence and can reopen a concern in file mode. | This is a valuable feedback pattern. It depends on the effects job running and on the input reports being sufficiently complete; the current AES state says effects/fix-owner jobs are disabled. No absence-of-recurrence claim follows from a zero count. |
| Composition | Project Meta's concern lifecycle decision names GitHub Issues for concern state and Plan 273 for execution; AES has native Feedback records, issue markers and its own effects database. | Do not create a third concern register. Q42 remains open until the key namespace, register owner, evidence links and closure authority are mapped across actual consumers and a current successful landed path is observed. |

**Recommendation:** carry the design principles into AES: one durable concern identity,
native evidence ownership, explicit disposition, verifier-owned closure on the landed
revision, and recurrence reopening. Adapt the exact integration only after tracing
current producers/readers and proving a successful, revision-bound closure path. Keep
the negative-control failure as a required design lesson: a proof must fail on the
known-broken revision as well as pass on the fix. Do not count issue closure, a receipt
string, or a configured registration as proof of repair or ongoing operation.

## Bounded consolidation sequence

| Step | Visible result and evidence | Status |
| --- | --- | --- |
| 1. Read and reconcile direction | This review, accepted Decision 0014, linked Q36–Q42 and pinned source map | Initial bounded pass recorded; no exhaustive review claim |
| 2. Compare records and choose publication provider | Unique facts/aliases/readers/writers accounted for; one proposed source-to-view mapping; compare existing exporter/view with sufficient catalogue products | In progress; sources and known reader/writer seams are documented, but record-by-record reconciliation and provider selection remain open (Q36–Q38) |
| 3. Deliver one discovery journey | Real provider → versioned schema → real consumer → observed receipt, plus a second different capability; a reader finds and compares both | Not implemented |
| 4. Exercise freshness and failure | Change a provider description or schema; view refreshes or reports stale; unavailable input cannot look empty/complete | Not implemented |
| 5. Reconcile upstream routes | Workspace, ACA, Project Meta and Company Planning point at the demonstrated route; preserve old IDs and recovery references before retirement | Not implemented |

Each implemented discovery/refresh run must retain inputs, source revisions,
processing steps, tool arguments/results and output for inspection. Any model
step must use the existing harness/llm_client path with complete available trace
and a measured or worked cost basis; this documentation review introduces no
new runtime model call or estimated price.

## Continue reading the older system

Continue in this order, updating this page and the existing question ledger rather
than creating parallel trackers. A source counts as reviewed only for named
sections and a pinned revision, with proposed disposition and unresolved material.

1. **Catalogue writers and readers:** compare every old entry, aliases and update
   path; inspect actual consumers of the indexes. Reconcile catalogue authority
   through Q36, not by merging names mechanically.
2. **Concern/repair lifecycle:** source review completed for the pinned decision,
   registration, observer/verifier code and AES receipt/effects path above. Next,
   reconcile current concern producers/readers and obtain revision-bound live evidence
   before selecting a shared register or claiming the loop operates end to end (Q42).
3. **Policy families and exceptions:** review selected families tied to current AES
   gaps, including legitimate counter-cases and recovery. No full 263-policy audit
   has happened in this pass.
4. **Instruction delivery:** compare native configuration, synchronization and scope
   boundaries with agent-skills and current workspace instructions. Source a rule
   once, then inspect what the native host actually delivers.
5. **Earlier AES designs and evidence:** follow existing retirement/harvest links;
   read code and complete retained traces for a selected claim. Record what remains
   useful without reinstating retired executable instructions.

This begins the continuing review Brian requested. The completed portion is the
first source pass and consolidation direction; the queue remains explicit.

[workspace-list]: https://github.com/BrianMills2718/code2-workspace/blob/e430021149b5f24dac1fd082f48dd93071899f8a/docs/decisions/0004-one-capabilities-list.md
[pm-architecture]: https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/docs/ops/CAPABILITY_REGISTRY_ARCHITECTURE_V0.md
[pm-catalog]: https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/scripts/capability_catalog.yaml
[pm-ownership]: https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/scripts/capability_ownership_registry.yaml
[merged-view]: https://github.com/BrianMills2718/ecosystem-ops/blob/484f1c1fc51cabe26e507f3f1b46378cc90c4f01/capability_registry.py
[aca-registry]: https://github.com/BrianMills2718/agentic-capability-architecture-canonical/blob/8b1d8460b968166e7020fdc55b8068561ea48199/capability_registry.yml
[aca-candidates]: https://github.com/BrianMills2718/agentic-capability-architecture-canonical/blob/8b1d8460b968166e7020fdc55b8068561ea48199/reuse_candidates.yml
[aca-tool]: https://github.com/BrianMills2718/agentic-capability-architecture-canonical/blob/8b1d8460b968166e7020fdc55b8068561ea48199/tools/capability_catalog.py
[planning-reuse]: https://github.com/BrianMills2718/company-planning/blob/497405299c68de0da8c3ac92e4c265d4d6c3403e/plugins/company-planning/skills/bounded-design/SKILL.md#capability-reuse-default
[contracts-model]: https://github.com/BrianMills2718/data-contracts/blob/ff6f13bc32252ab3b687a16f68191c6a7ebc5329/wiki/system-model.md
[claim-locators]: https://github.com/BrianMills2718/data-contracts/blob/ff6f13bc32252ab3b687a16f68191c6a7ebc5329/src/data_contracts/source_claims.py#L189
[dataset-resolver]: https://github.com/BrianMills2718/data_library/blob/035a3e32fff14dfe880a9909d4e04e855c7398f2/src/data_library/resolver.py
[dataset-readme]: https://github.com/BrianMills2718/data_library/blob/035a3e32fff14dfe880a9909d4e04e855c7398f2/README.md#prompt-discovery
[tool-metadata]: https://github.com/BrianMills2718/llm_client/blob/4ee0cf800587598672dfacfed99ea2954c2e01e6/llm_client/tools/decorator.py
[policy-system]: https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/docs/ops/POLICY_SYSTEM.md
[policy-registry]: https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/policy/registry.yaml
[ep-model]: https://github.com/BrianMills2718/enforced-planning/blob/faf7d9e/PLANNING_OPERATING_MODEL.md
[concern-lifecycle]: https://github.com/BrianMills2718/project-meta/blob/f1e27c906f6c78a6d544bf62a878367640f7d186/docs/ops/ADR-2026-09-14-one-feedback-concern-lifecycle.md
[concern-code]: https://github.com/BrianMills2718/project-meta/tree/f1e27c906f6c78a6d544bf62a878367640f7d186/scripts/concern_repair_feedback.py
[aes-review-revision]: https://github.com/BrianMills2718/agentic-engineering-system-canonical/tree/268d58e6c1a6e8ecf697396752635ee7d5b1c639
[old-harvest]: https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/37dc876cc3dd7f88ece46873f17a0015228af123/research/synthesis/2026-09-26-inside-success-aes-harvest.md
