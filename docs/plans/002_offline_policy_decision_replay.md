# Plan 002 — Offline policy-decision replay vertical

**Status:** Planned — no runtime or live-policy behavior changed
**Recorded:** 2026-09-22
**Type:** implementation
**Priority:** High
**Landscape disposition:** linked
**Planning baseline:** canonical AES `b06e28dba3d52eb7c036f140ac84cf8fadee368e`
**Planning provider basis:** `BrianMills2718/company-planning` canonical method + the AES-local profile. This record follows that contract; it does **not** claim a Company Planning plugin execution occurred in this chat.
**Blocked By:** authenticated TypeSafe/Jev access that exposes an exact model through `GET /v1/models`. The initial replay dataset is frozen at the four exact authentic cases already retained in `evals/plan-002/case_manifest.json`.
**Blocks:** any decision to use Jev in live AES shadow/warn/enforce paths for the selected policy family.

Execution tracker: [Issue #20 — Plan 002 offline completion/verification policy replay](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/20). The issue is a coordination/checklist surface only; this plan remains execution authority.

---

## Gap

**Current:** Plan 001 proved one bounded AES lifecycle, including exact verification, direct human utility, and gap reconciliation. The fresh gap state still marks broader policy/evidence maturation as incomplete. AES already has deterministic completion/verification controls through Enforced Planning, but there is no accepted evidence that a contextual model improves judgment on real AES policy decisions, and no current live Jev integration is authorized.

**Target:** For one existing policy family—completion / verification evidence—replay authentic historical decision points offline using the exact event-time evidence available then. Show the existing deterministic decision beside a Jev typed judgment in one source-linked report. The operator can inspect disagreements and decide whether Jev is worth advancing to **shadow-only** use for this policy family.

**Why:** This is the smallest useful test of contextual policy intelligence that preserves working deterministic controls and directly answers a product decision. It does not require a new policy engine, live hooks, or broad observability platform.

Relevant fresh gaps:
- `GAP-AES-007 / AES-PLAN-002`: prospective planning → execution custody remains broader than one delivered slice.
- `GAP-AES-011 / AES-POL-001`: adaptive policy behavior beyond Repository Context remains incompletely evidenced.
- `GAP-AES-012 / AES-POL-002`: broader pass/fail/stale/error control-state evidence remains incomplete.
- `GAP-AES-014 / AES-POL-004`: important controls need broader negative/counterfactual evidence.
- `GAP-AES-017 / AES-EVID-001`: evidence/current-state projections are not yet fully mechanical.
- `GAP-AES-025 / AES-PLAN-007`: broader feasibility/enabler decisions need case-earned evidence.

None of those gaps alone authorizes this plan. The authorized human/product outcome below does.

---

## User Outcome

**Brian can open one source-linked replay report for a real past completion/verification decision, see what the existing deterministic control decided, what Jev judged from the event-time context, where they disagree or abstain, what the evaluation cost/latency was, and decide `adopt-for-shadow | revise | reject` without changing live agent behavior.**

---

## Canonical Behavioral Example

**Starting input/state:** an authentic retained coding-agent event where the agent attempts a completion/stop/verification claim and the existing Enforced Planning completion contract has enough retained evidence to determine whether the claim was accepted, denied, stale, or unobserved.

**Action:** run the offline replay command against that exact event/case. The replay reconstructs only information available at decision time, evaluates the existing deterministic control, sends the same bounded policy state to Jev through a typed question, and generates a static JSON/HTML report.

**Expected observable result:** the report shows:

1. exact source event/session/repository/revision references;
2. event-time context completeness and any missing/stale state;
3. existing deterministic decision + reason code;
4. Jev model identity, question/version, typed answer/distribution or explicit unavailable/error state;
5. agreement/disagreement classification;
6. latency, usage and incremental cost where the provider reports them;
7. eventual outcome/adjudication in a **separate** section that was not supplied to the evaluator;
8. an operator disposition surface: `adopt-for-shadow | revise | reject`.

**Behavioral evidence:** currently unobserved.

**Substrate/process evidence:** current deterministic completion code exists in `enforced_planning/outcome_completion.py`; Plan 001 retained revision-bound evidence patterns; proposal PR #14 contains donor research on Jev, capture, and policy failure modes.

**Failure signal:** the replay cannot bind an authentic event-time source, silently uses future information, approximates the deterministic baseline instead of executing/reconstructing it faithfully, hides evaluator unavailability as pass, or requires live agent interception merely to produce a first report.

---

## Capability Adoption

**Disposition:** reuse

- Reuse **Enforced Planning** as the current deterministic completion/verification authority and control baseline.
- Reuse existing AES/native transcript or archive material as the event source if it is adequate; do not create a new archive platform to begin.
- Evaluate **TypeSafe Jev** as an external typed-judgment provider behind one replaceable provider adapter.
- Keep the replay/report orchestration as an AES-local residual in the already-reserved `policy_control` component.
- Do not copy the broad proposal runtime from PR #14 and do not create an ACA/Jev registry, policy DSL, or new universal evidence store.
- A small generative-model comparator is diagnostic-only and may be added later if it materially changes the decision; it is not required for the first vertical.

---

## References Reviewed

Repository-local:
- `docs/architecture/SYSTEM_BOUNDARY.md` — AES-POL-001..004, AES-EVID-001, AES-LEARN-001, AES-PLAN-005..007.
- `docs/architecture/INITIAL_GAP_LEDGER.md` — fresh post–Plan 001 gap state.
- `docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md` — use established modules/providers and avoid speculative parallel infrastructure.
- `enforced_planning/outcome_completion.py` — existing exact completion decision/custody surface.
- `evidence/plan-001/` — revision-bound evidence and human-observation precedent.
- PR #14 `proposal/jev-semantic-policy-layer-2026-09-19` — donor research only; not current authority.
- PR #12 `Plan Jev-backed policy intelligence...` — earlier overlapping donor proposal; not current authority.

Planning provider:
- `BrianMills2718/company-planning` — canonical planning-method repository.
- `docs/architecture/aes-company-planning-profile.bootstrap.yaml` — AES-local provider profile.

Current external provider sources checked 2026-09-22:
- https://api.typesafe.ai/docs — current OpenAPI surface exposes `POST /v1/systemone`, `GET /v1/models`, and typed Noul/Choice/Score schemas.
- https://typesafe.ai/blog/introducing-system-one-models-and-jev — Jev is early access; published cost/speed are provider claims, not AES measurements.
- https://evals.typesafe.ai/agent_trace_observability — provider example close to the intended trace-judgment use; useful prior art, not evidence of AES fit.

---

## Research Basis For This Slice

- Current post–Plan 001 gap ledger and accepted AES policy/evidence clauses define the need; this plan does not create a new requirement surface.
- PR #14 is the strongest local Jev/capture/policy donor synthesis but predates Plan 001 closure and is intentionally narrowed here.
- TypeSafe's current API/OpenAPI documentation, launch documentation, and Agent Trace Observability workflow were rechecked on 2026-09-22. Provider benchmark/speed/cost statements remain provider claims until measured in AES.
- Company Planning's canonical repository and the AES-local planning profile were reviewed for slice/verification shape. No plugin execution is claimed in this chat.

---

## Landscape And Prior Art

**Alternatives**

1. **Deterministic controls only — retain as authority/control.**
   - Lowest dependency/latency risk.
   - Cannot answer whether contextual judgment catches cases rigid predicates miss.
2. **Jev typed evaluator — candidate for the exploratory comparison.**
   - API shape is well matched to bounded yes/no/choice/score decisions.
   - Early-access provider, account/model availability and actual AES latency/accuracy remain unverified.
3. **Small generative LLM evaluator — deferred comparator.**
   - More flexible explanations but higher latency/cost and a broader output surface.
   - Add only if Jev-vs-deterministic results are ambiguous enough that the comparison can change the decision.
4. **Build a local semantic policy model/platform — rejected for this slice.**
   - No evidence currently justifies the maintenance/runtime burden.

**Project implications:** The first implementation must be provider-replaceable, offline, read-only, and attached to the existing `policy_control` component. Existing deterministic controls remain authoritative. Jev cannot authorize an action or weaken an exact gate in Plan 002.

**Refresh trigger:** TypeSafe model/API contract changes; Jev access is unavailable; authentic case reconstruction proves impossible; or first report shows the policy family is adequately served by deterministic controls.

**Decision method:** one bounded external provider behind a replaceable adapter, evaluated on authentic cases against the incumbent exact control. Stop if the experiment cannot change the policy-provider decision.

---

## Modality Assessment

| Part | Mode | Why | Planning Treatment |
|---|---|---|---|
| Replay/event custody | Deductive / plan-first | Exact source identity, timing and future-information exclusion are knowable invariants. | Freeze contracts, source refs and negative controls before evaluator work. |
| Deterministic baseline | Deductive / plan-first | Existing Enforced Planning semantics are current authority. | Execute/reconstruct exactly; never approximate silently. |
| Jev judgment quality | Exploratory / ladder | Accuracy, disagreement value, latency and provider availability are empirical. | Start with authentic cases, inspect concrete disagreements, stop or promote. |
| Operator report | Hybrid | Required information is knowable; usefulness needs direct observation. | Static source-linked report first, then one attention checkpoint. |

**Exploratory readout:** reviewed disagreements, false-block/miss/uncertain cases, provider errors, p50/p95 latency on the small case set, incremental cost, and Brian's final `adopt-for-shadow | revise | reject`.

**Step-down path:** aggregate disagreement/error counts always link to individual source cases, exact provider request/response metadata, baseline reason codes, and event-time evidence.

---

## Files Affected

Planned implementation scope:

- `src/agentic_engineering_system/policy_control/__init__.py` — modify when real code replaces the placeholder surface.
- `src/agentic_engineering_system/policy_control/models.py` — create strict replay/report models.
- `src/agentic_engineering_system/policy_control/replay.py` — create provider-neutral offline replay orchestration.
- `src/agentic_engineering_system/policy_control/providers/__init__.py` — create.
- `src/agentic_engineering_system/policy_control/providers/jev.py` — create thin TypeSafe adapter.
- `tests/policy_control/` — replace placeholder with focused replay/provider/future-information tests when implementation begins.
- `evals/README.md` and `evals/plan-002/` — active eval front door plus bounded case/evaluation protocol and source-reference manifest.
- `generated/policy-replay/` — generated non-authoritative reports.
- `evidence/plan-002/` — revision-bound provider-fit, verification and operator evidence.
- `docs/plans/002_offline_policy_decision_replay.md` — keep execution status/evidence current.
- `.agentic/repo.yaml`, `README.md`, `docs/plans/README.md`, `wiki/index.md` — active-plan/frontier projections only.

No raw archive/transcript store is added to Git.

---

## Target Implementation Topology

Use existing reserved component homes; do not add a parallel subsystem.

Planned runtime subjects:

```text
src/agentic_engineering_system/policy_control/
  __init__.py
  replay.py                  # provider-neutral offline replay orchestration
  models.py                  # strict AES-local replay/report models
  providers/
    __init__.py
    jev.py                   # thin TypeSafe adapter only

tests/policy_control/
  test_replay.py
  test_jev_adapter.py
  test_future_information_guard.py

evals/plan-002/
  README.md                  # case/evaluation protocol; no raw secrets
  case_manifest.json         # source refs + labels, not invented transcripts

generated/policy-replay/<run-id>/
  replay.json
  index.html

evidence/plan-002/<aes-revision>/
  verification-summary.json
  provider-fit.md
  operator-observation.md
```

Raw transcript/archive bytes stay with their existing owner. Git retains source references, bounded case manifests, code/config versions, provider metadata, generated review artifacts when safe, and decision evidence.

---

## Plan

**Critical-path classification:** `vertical`

The plan's product status advances only through V1/V2. P0 is a reproduced/declared `direct_blocker` gate that protects those verticals; satisfying P0 alone is not product progress.

### P0 — execution/provider preflight — `direct_blocker`

Goal: prove the vertical can use authentic data and the external provider before building replay machinery.

**Current P0 evidence — simplified starting set, 2026-09-22:** `evals/plan-002/case_manifest.json` retains **4 exact authentic** completion/verification decision events. That is now the frozen exploratory dataset for V1/V2; a fifth case is no longer a prerequisite. The remaining P0 blocker is authenticated TypeSafe/Jev provider access and one protocol smoke. Raw-custody verification for the four cases remains useful provenance work but no longer blocks starting the first offline comparison because the repository already retains exact source identities, transcript digests, receipt digests where available, and sanitized ordered evidence for the selected cases.

Exit gates:

- current session exposes required machine execution tools, or execution is handed to a machine-capable Work/session;
- retain the **4 exact authentic completion/verification decision events** already frozen in `evals/plan-002/case_manifest.json` as the initial exploratory dataset;
- confirm raw archive ownership/location and that the first cases can be used without copying secrets/client data into Git;
- authenticated TypeSafe call to `GET /v1/models` succeeds and records an exact available model identifier suitable for the run;
- one tiny non-policy smoke question proves the client/adapter protocol only; it is not accuracy evidence.

**Stop:** if TypeSafe access is unavailable, record the blocker and do not build a substitute policy platform. If one of the four retained cases proves unusable during replay, mark that case unusable and continue only if the remaining cases still support the exploratory question; do not manufacture replacement evidence merely to preserve a case-count target.

### V1 — one authentic offline replay + report — `vertical`

Goal: produce one inspectable source-bound report without affecting a live coding session.

- freeze one authentic case and its event-time context;
- execute/reconstruct the existing deterministic decision;
- evaluate the bounded question(s) through the Jev adapter;
- render JSON + static HTML;
- prove future outcome/adjudication was withheld from evaluator input;
- direct operator review of the exact report.

**Attention checkpoint:** Brian records `continue | change | stop` for the replay/report interaction, separately from the final Jev provider disposition.

### V2 — small frozen case set + provider disposition — `vertical`

Goal: make the actual provider decision.

- freeze a small authentic development set and separate review/holdout cases before threshold tuning;
- run deterministic baseline and Jev on the same event-time inputs;
- retain every disagreement/error/unavailable result;
- classify concrete failures rather than optimizing one aggregate score;
- report latency/cost and capture completeness;
- Brian records **`adopt-for-shadow | revise | reject`** for this policy family.

No live hooks, warnings, enforcement, context ranking, skill routing, or automated policy modification are authorized by V2.

---

## Epistemic Planning Frontier

| Area | State | Current contract | Trigger / stopping rule | Downstream update |
|---|---|---|---|---|
| Authentic archive cases | enabling_work_blocked | Existing archives are claimed by prior research but not freshly inventoried at this baseline. | P0 locates ≥5 usable exact cases or stops. | case manifest + evidence record |
| Jev account/model availability | enabling_work_blocked | Public API/model discovery exists; account access is unknown. | authenticated `GET /v1/models` | pinned execution manifest |
| Deterministic completion semantics | fully_specifiable_now | Enforced Planning is authority. | source/contract changes | plan + regression set |
| Jev question wording | exploration_required | Typed question family is known; best wording is empirical. | concrete disagreement review; freeze before holdout | evaluation manifest |
| Live intervention | deliberately_deferred | No behavioral change in Plan 002. | V2 `adopt-for-shadow` only | future plan required |
| Broad capture platform | deliberately_deferred | Existing archive should be reused first. | proven missing-data blocker | plan revision required |
| Generative comparator | conditional | Diagnostic option, not first-vertical dependency. | Jev-vs-control result is inconclusive and comparator can change decision | scoped plan amendment |

---

## Reassessment Contract

- **Triggers:** no authentic cases; provider access/model drift; event-time context cannot be separated from future information; deterministic baseline cannot be reproduced; first direct report is not useful; Jev disagreements are dominated by exact-control semantics it should never replace.
- **Autonomous action:** adjust local report layout, bounded adapter error handling, or question packaging while preserving frozen case/evaluator boundaries.
- **Plan revision required:** new archive system, live hooks, warnings/enforcement, policy registry changes, a second policy family, provider substitution, or a new external spend/dependency not already authorized.
- **Human decision required:** provider spend beyond a tiny bounded evaluation, use of sensitive client archives outside existing custody, any live behavioral intervention, final `adopt-for-shadow | revise | reject`.
- **Stopping rule:** stop once the first policy-family provider decision is evidence-backed. Do not continue into a broad policy platform merely because the replay infrastructure exists.

---

## Required Tests

### New tests

| Test | Verifies |
|---|---|
| replay rejects missing/stale source refs | ignorance never becomes green |
| replay preserves source repository/revision/session IDs | evidence custody |
| future/outcome fields cannot enter evaluator state | no label leakage |
| deterministic baseline result/reason is retained exactly | incumbent-control fidelity |
| Jev adapter preserves exact model/question IDs and typed answer | provider traceability |
| timeout/provider error becomes explicit `unavailable/error` | no silent pass |
| report links every summary row to concrete source case | step-down from aggregates |
| generated report contains no raw secret fields from fixture negatives | bounded review artifact |
| Jev adapter can be replaced by a fake provider in unit tests | provider boundary stays thin |

### Existing checks

- current AES tests remain green;
- Company Planning profile/schema checks remain green;
- Enforced Planning governance/sync checks remain green;
- generated `AGENTS.md` sync remains green;
- no Plan 001 evidence/current-state regression.

---

## Verification Strategy

Current stage: **Pilot**
Execution profile: **pilot**
Next decision: whether Jev merits **shadow-only** use for the completion/verification policy family.
Gate-time budget: keep first V1 report to one authentic case; V2 case count stays small enough for direct disagreement review rather than benchmark theater.
Stopping rule: if no decision-useful disagreement or improvement appears, reject/defer Jev for this family rather than expanding scope.

Boundary gate:
- exact case/source refs;
- event-time/future-information separation;
- provider/model identity;
- no live effect path.

Increment gate:
- focused policy-control tests;
- provider adapter protocol/error tests;
- report fixture review.

Terminal gate:
- frozen case manifest;
- exact provider/model/question versions;
- full relevant AES suite;
- source-linked V2 readout;
- direct operator provider disposition.

Hosted CI may assist but is not the authority; exact local/external execution and retained evidence remain first-class under Decision 0008.

---

## Acceptance Criteria

Feature:
- [ ] At least one authentic completion/verification event replays from exact source references.
- [ ] Existing deterministic decision is reproduced or explicitly marked non-reconstructable; never approximated silently.
- [ ] Jev result is typed, model/version-bound, source-linked, and records latency/usage/cost or explicit provider omission.
- [ ] Eventual outcome/adjudication is excluded from evaluator state and shown separately.
- [ ] Static report makes agreement/disagreement/error/uncertainty understandable without transcript reconstruction.
- [ ] Brian directly reviews the report.
- [ ] Small frozen case-set readout supports one explicit `adopt-for-shadow | revise | reject` decision.

Process:
- [ ] P0 blockers are cleared before replay implementation expands.
- [ ] No live policy behavior changes.
- [ ] No raw client/secret archive is copied into Git.
- [ ] Incumbent Enforced Planning controls remain authoritative.
- [ ] Exact verification evidence is revision-bound.
- [ ] Fresh characterization/gap update follows completion; plan completion alone closes nothing.

---

## Explicit Non-Goals

- live Claude Code/Codex hook integration;
- warn or enforce modes;
- replacing Enforced Planning;
- universal policy registry or DSL;
- building a transcript/archive platform;
- context/skill/subagent routing;
- automated policy generation or self-modification;
- general observability dashboard;
- proving Jev superior across AES;
- reopening ACA standalone experiments.

---

## Relationship To Prior Proposals

PRs #12 and #14 are research/proposal donors. Their broad multi-stage programs are **not** adopted wholesale by this plan. Plan 002 takes only the smallest decision-useful first vertical: authentic offline replay for one existing policy family. If this plan is accepted on `main`, those proposal PRs should be closed as superseded by this bounded execution plan while preserving their branches/history as research evidence.
