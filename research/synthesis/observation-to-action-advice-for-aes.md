# Observation-to-Action metamodel advice for canonical AES

Status: research synthesis / tentative advice

Authority: analytical; non-normative

Disposition: candidate semantic donor; no runtime/provider adoption decision

Captured: 2026-09-16

## Review basis

This note compares the current canonical Agentic Engineering System (AES) architecture with the current Observation-to-Action (O→A) metamodel to identify concepts that may be useful to AES without transferring authority or importing O→A wholesale.

Reviewed revisions:

- canonical AES: `BrianMills2718/agentic-engineering-system-canonical@a6bd092fb16f5ebca21d621015fc40152dce3dc7`
- O→A: `BrianMills2718/observation-to-action-metamodel@a060d3ac5b1dc1691a30c784c72e948c52c25a94`

Primary AES references:

- `docs/architecture/SYSTEM_BOUNDARY.md`
- `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`
- `docs/architecture/INITIAL_GAP_LEDGER.md`
- `docs/plans/001_repository_context_resolution_vertical.md`
- `docs/plans/001_D1_contract_surface_topology_freeze.md`
- `research/synthesis/aes-evidence-characterization-and-context-suggestions.md`
- `research/synthesis/representation-review-and-epistemic-surface-suggestions-for-aes.md`
- `research/synthesis/fluid-governance-selective-salvage.md`

Primary O→A references:

- `04-SPEC.md`
- `03-VOCABULARY.jsonld`
- `constraints.json`
- `08-decisions/003-record-side-and-agent-side.md`
- `08-decisions/018-reflective-feedback-boundary.md`
- `08-decisions/019-repository-release-is-not-runtime-activation.md`

This synthesis does not amend the AES system boundary, select O→A as a runtime dependency, authorize new implementation, or change any incumbent ownership decision.

---

## Executive advice

O→A is relevant to AES, but primarily at one boundary:

> **AES owns the integrated engineering lifecycle, governed execution, policy/admission, and authoritative effects. O→A is a candidate semantic donor for representing what an observed result is entitled to support, how that standing reaches a belief/decision, and how later evidence changes that standing without rewriting history.**

The strongest candidate concepts are:

1. `LicenseRelation` — separate a successful result from the stronger claim it is permitted to support.
2. `LicenseConditionRelation` — make evidence adequacy, establishment, bounds, and pre-commitment explicit.
3. `ClaimRelation` + `BeliefStateRelation` — separate an asserted proposition from what is currently held, including competitors and supporting licences.
4. `DecisionRelation` — retain why a decision was entitled by the then-current belief state.
5. `FeedbackRelation` with immutable historical snapshots — let later evidence invalidate a warrant or condition without rewriting the state under which an earlier decision was made.
6. `ProjectionRelation` versus `TransformationRelation` — distinguish a different representation of the same information from a content-changing synthesis/inference.
7. staged self-amendment from O→A Decision 018 — a proposed successor governance/method version must not become part of the authority that validates its own creation.

The recommended first use is a **small Plan 001 evidence/standing trace**, not adoption of the whole O→A schema.

---

## Why the fit is real

Canonical AES already asks the question O→A is designed to answer.

`research/synthesis/aes-evidence-characterization-and-context-suggestions.md` identifies a central unresolved design problem:

```text
what has sufficient evidence to be believed?
what does that evidence actually establish?
when is the belief no longer current?
```

It also says that:

- a passing check may be inadequate evidence for the criterion it is being used to support;
- generated interpretations should remain candidates until promotion conditions are met;
- current truth must become stale when its support is invalidated;
- important relationships may themselves need evidence/freshness semantics;
- `PASS`, `FAIL`, `NONE/UNOBSERVED`, `ERROR`, and `STALE` must survive composition.

O→A provides a concrete semantic decomposition for the part between **observed result** and **decision entitlement**:

```text
Observation
    ↓
Analysis
    ↓
Result
    ↓
License + LicenseCondition
    ↓
Claim
    ↓
BeliefState
    ↓
Decision
```

with downstream:

```text
Action seam
    ↓
Effect
    ↓
Feedback
    ↓
changed standing in a later snapshot
```

This is not the same as the AES lifecycle. It is a narrower epistemic/decision trace that can sit inside or beside an AES lifecycle run.

---

## Candidate mapping

| Canonical AES concern | O→A candidate concept | Advice |
| --- | --- | --- |
| A passing check does not necessarily establish the criterion | `LicenseRelation` | Strong candidate. Treat a result as separate from the claim reach it is licensed to support. |
| Evidence requirements/conditions must be inspectable | `LicenseConditionRelation` | Strong candidate. Particularly relevant to required evidence kind, condition status, establishment, bounded uncertainty, and pre-commitment. |
| Generated interpretations must not self-promote | `ClaimRelation` + derived licence standing | Strong candidate. A claim may exist while remaining operationally unsupported. |
| Current characterization may involve competing interpretations | `BeliefStateRelation` | Strong candidate when AES needs to record what is held plus live competitors rather than collapsing to one current claim. |
| A continuation/routing choice should be explainable from evidence | `DecisionRelation` | Strong candidate for decision lineage, provided AES/native owners retain decision authority. |
| Later evidence changes whether earlier support is still applicable | `FeedbackRelation` -> `LicenseConditionRelation` | Strong candidate for a narrow, case-earned invalidation path. Do not generalize all feedback propagation prematurely. |
| Historical evidence should remain inspectable | immutable O→A snapshots / Decision 018 | Strong fit with `AES-EVID-001`. Later standing should not rewrite the earlier record. |
| Generated wiki/context/working surface must remain a projection | `ProjectionRelation` | Useful donor concept: representation choice can change what is computable/visible without becoming authority. |
| Agent summary/inference may create or omit semantic content | `TransformationRelation` | Useful donor concept: distinguish representation changes from content-changing synthesis. |
| Policy/methodology may eventually amend itself | Decision 018 staged self-amendment | High-value governance invariant when AES begins changing its own policy/planning machinery. |
| Runtime policy, recovery, execution, admission, activation | `ActionRelation` seam; no `ActivationRelation` | Boundary confirmation, not adoption. AES/Enforced Planning should continue to own authoritative execution/admission effects. |
| Stakeholder purpose, preferences, risk posture, choice rule | O→A agent-side relations | Research input only for now. These O→A relations are still declared rather than case-earned and must not become a parallel decision-theory model. |

---

## Highest-value candidate: result standing rather than one overloaded status

AES already distinguishes operational observation states such as:

```text
PASS
FAIL
NONE / UNOBSERVED
ERROR
STALE
```

These should remain AES/native observation and control states. O→A should not replace them.

They answer:

> What happened when the check/observation was attempted, and is that observation current?

O→A's licence semantics answer a different question:

> Given that result, what stronger proposition is the result entitled to support, for this purpose and consequence class, under these conditions?

For example, Plan 001 deliberately requires an authentic external consumer outcome. A local test could pass while the external-behavior criterion remains unsupported:

```text
observed check:
  local unit test -> PASS

analysis result:
  succeeded

claim:
  "repository context resolution works for the authentic external consumer"

licence condition:
  authentic external behavior observed? -> unassessed

licence standing:
  unestablished

criterion:
  still open / insufficient evidence
```

This provides a principled semantic explanation for a rule canonical AES already wants: **green check output does not imply adequate evidence for a stronger claim**.

---

## License conditions may directly help Plan 001

O→A `LicenseConditionRelation` has several distinctions that map well to the first AES vertical:

- condition state: `satisfied | bounded | unsatisfied | unassessed`;
- establishment: `derived | tested | asserted | unestablished`;
- basis and bound;
- named criterion/question;
- whether the criterion was fixed before the result existed (`condPreCommitted`).

The pre-commitment field is especially relevant because Plan 001 freezes AC-001 through AC-011 before implementation. AES should preserve the difference between:

```text
criterion fixed before observing the implementation result
```

and:

```text
criterion selected or weakened after seeing the result
```

O→A already has a case-earned semantic hook for that distinction. This is worth testing before inventing a separate AES evidence-adequacy vocabulary.

---

## Candidate thin slice for Plan 001

Do **not** convert `RepositoryContextArtifact` into an O→A graph. The native typed artifact should retain its selected contract owner and AES should continue to honor `AES-CONTRACT-001`.

Instead, after Slice 1 has a real artifact and executed evidence, construct an optional epistemic trace over one load-bearing routing claim.

A suitable canonical example is:

```text
ObservationRelation
  subject: exact reviewed data-contracts revision
  observation: native authority/navigation evidence
        ↓
AnalysisRelation
  method/action: repository.context.resolve
        ↓
Result
  RepositoryContextArtifact produced
        ↓
ClaimRelation
  "src/data_contracts/ is a native implementation / typed-contract authority surface"
        ↓
LicenseRelation
  purpose: repository orientation
  consequence class: operational
        │
        ├─ LicenseCondition: exact revision bound
        ├─ LicenseCondition: positive source reference present
        ├─ LicenseCondition: no folder-name-only inference
        └─ LicenseCondition: authority evidence adequate for the routing claim
        ↓
BeliefStateRelation
  held routing interpretation
  + any unresolved competitor/ambiguity
        ↓
DecisionRelation
  route actor to the legitimate native authority surface
        ↓
ActionRelation seam
  working surface opens/shows/navigates through AES-owned execution path
        ↓
EffectRelation
  stakeholder/agent use observed at A1
        ↓
FeedbackRelation
  refine or invalidate a supporting condition if the observed utility/evidence contradicts it
```

### What this experiment should answer

The experiment is useful only if it changes an engineering decision or makes a false-green state materially easier to prevent or understand.

Measure qualitatively:

1. Does the trace make AC-005 evidence provenance easier to inspect?
2. Can it represent `PASS but insufficient evidence` without inventing another overloaded status field?
3. Does it make AC-009 re-characterization clearer when a dependency/revision changes?
4. Can a later observation invalidate only the affected warrant rather than marking unrelated history false?
5. Does the trace reduce reviewer reconstruction cost at AC-010/A1?
6. Can it coexist with native result contracts, Enforced Planning, and policy controls without becoming another authority?

If the trace adds ceremony but does not improve one of those outcomes, do not adopt it.

---

## Feedback, invalidation, and freshness

There is a promising but bounded fit between AES freshness and O→A feedback.

Canonical AES wants:

```text
observation @ revision R1
        ↓
current characterization
        ↓
dependency/revision changes
        ↓
prior support becomes STALE
        ↓
fresh observation @ R2
```

O→A has a case-earned path in which a later `EffectRelation` produces `FeedbackRelation` of kind `invalidates-condition`, targeted at an actual `LicenseConditionRelation`. That challenge changes dependent licence standing in the next snapshot while preserving the old snapshot.

Possible composition:

```text
AES freshness mechanism
    determines that supporting evidence is stale / changed
        ↓
O→A-style feedback trace
    identifies which licence condition/warrant is challenged
        ↓
next materialized standing
    dependent claim no longer decision-grade until re-established
```

Important boundary: O→A should **not** become AES's general repository invalidation engine. AES still needs revision/dependency mechanics that determine *whether* support changed. O→A may be useful for representing *which epistemic warrant that change affects*.

O→A deliberately implements only the narrow invalidates-condition propagation earned by an authentic case. AES should preserve that restraint.

---

## Projection versus transformation may improve AES context/review semantics

Canonical AES repeatedly requires generated wiki/context/working surfaces to remain projections rather than authority. O→A offers a useful distinction:

### Projection

A `ProjectionRelation` changes computational or representational form and may expose/lose distinctions without necessarily changing semantic content.

Examples in AES could include:

- rendering a typed repository-context artifact as HTML;
- selecting a concern-specific subset for an engineering packet;
- showing one source-bound graph/table/lens over the same underlying facts.

### Transformation

A `TransformationRelation` changes content and explicitly records what was preserved, omitted, approximated, aggregated, created, or destroyed.

Examples in AES could include:

- an agent synthesizing several observations into a new characterization claim;
- summarizing a long evidence record into an inference-bearing conclusion;
- extracting an authority relationship that was not directly asserted in the source.

This distinction could help AES surfaces avoid treating:

```text
"the same facts displayed differently"
```

as equivalent to:

```text
"new semantic content was inferred or synthesized"
```

The latter should normally face stronger evidence/licensing scrutiny.

---

## Belief state may be useful where AES currently says "current"

AES should not replace all current-state materialization with `BeliefStateRelation`. Most current facts can remain ordinary revision-bound observations and native projections.

`BeliefStateRelation` becomes useful when a lifecycle decision depends on an **interpretive proposition with live alternatives**.

For example:

```text
held:
  "root contracts/ is not the repository-wide contract authority"

competing / unresolved:
  "root contracts/ may own a narrower concern-specific contract role"

as-of:
  exact reviewed data-contracts revision

licenses:
  evidence/licences establishing the held routing interpretation
```

That is richer than storing a single `current=true` claim and makes the subsequent routing decision auditable without pretending all ambiguity disappeared.

Use this only where competitors matter to the decision.

---

## Decision lineage fits, but authority must remain native

O→A's `DecisionRelation` records the belief state, objective, considered options, and chosen option. This could be useful for AES decisions such as:

- provider disposition (`reuse | extend | adapt | residual`);
- a `continue | change | pause | stop | scale` stakeholder disposition;
- a routing decision based on resolved repository authority;
- a policy recovery decision, if represented as a non-authoritative epistemic trace.

But the O→A record must not become the authority that makes the decision.

Canonical AES already has explicit owners:

- Company Planning for planning/design derivation;
- Enforced Planning for execution governance;
- native repositories/contracts for their owned facts;
- policy authorities for policy decisions;
- human/portfolio authorities where judgment belongs to them.

O→A can record **why** a decision was entitled without becoming the component that is entitled to make it.

---

## Staged self-amendment is worth adopting as an AES invariant

O→A Decision 018 contains a governance rule that is relevant to AES once AES begins changing its own policy, planning, evidence, or execution-governance mechanisms.

The safe shape is:

```text
active version N
    ↓ evaluates
proposed version N+1
    ↓ accepted by the authority active under N
N+1 becomes eligible for the next cycle
```

The unsafe shape is:

```text
proposed N+1
    ↓
uses N+1's own rules to validate its creation
    ↓
immediately joins the authority that approved it
```

AES already values explicit policy decisions, negative controls, authority boundaries, and no self-certification. The staged-activation invariant should be considered when the first authentic self-amendment case appears.

Do not create a universal `ActivationRelation` now. O→A itself explicitly leaves runtime admission/activation outside its vocabulary until a real consumer requires that state to be queryable.

---

## Agent-side O→A concepts: relevant but premature

O→A separates record-side semantics from agent-side semantics:

```text
record-side:
  observation, analysis, result, licence, claim, effect

agent-side:
  epistemic agent, purpose, preferences, authority, decision algorithm
```

This conceptually aligns with canonical AES concerns such as:

- stakeholder goals and utility;
- human-attention economics;
- consequence/stakes of being wrong;
- authority to make `continue | change | stop` decisions;
- choice of decision rule.

However, O→A's `EpistemicAgentRelation`, `AnalyticPurposeRelation`, `PreferenceRelation`, and `DecisionAlgorithmRelation` are still `declared`, not case-earned. O→A also explicitly warns not to re-model decision theory.

Tentative advice:

- use these concepts as vocabulary/research input;
- do not create AES contracts from them yet;
- let an authentic AES case determine whether the coupling needs first-class representation;
- do not move utility computation, portfolio choice, or authority semantics into O→A.

---

## Concepts not recommended for adoption now

### Do not import the whole O→A metamodel

AES does not need all 25 O→A relations merely because several concepts fit. Doing so would violate the canonical preference for minimal, case-earned shared semantics.

### Do not make O→A the AES event schema

`.agentic/events/` and future AES execution/evidence contracts should be derived from actual AES lifecycle requirements and incumbent owners. O→A can be a semantic interpretation layer over selected evidence, not a universal transport format.

### Do not replace native typed contracts

`RepositoryContextArtifact`, policy/control results, provider contracts, and other native data shapes should remain with their natural authorities under `AES-CONTRACT-001`.

### Do not replace `.agentic/relationships.yaml`

O→A may eventually help express the standing of a load-bearing relationship, but the repository topology file has its own AES purpose and authority.

### Do not make O→A an execution or policy engine

`ActionRelation` is intentionally a seam. Runtime execution, admission, recovery, and activation remain AES/Enforced Planning/native-authority concerns.

### Do not introduce a universal graph database because O→A is graph-shaped

The semantic model can be tested as ordinary typed records/fixtures first. Storage technology is a separate decision that should be earned by real query or scale requirements.

---

## Suggested disposition by concept

| O→A concept | Tentative AES disposition | Why |
| --- | --- | --- |
| `LicenseRelation` | **experiment now** | Directly addresses proof adequacy versus successful check output. |
| `LicenseConditionRelation` | **experiment now** | Maps well to required evidence, condition assessment, bounds, and pre-committed criteria. |
| `ClaimRelation` | **experiment now** | Prevents generated interpretation from being conflated with established fact. |
| `BeliefStateRelation` | **experiment selectively** | Useful where a decision depends on live competing interpretations. |
| `DecisionRelation` | **experiment as trace only** | Good audit semantics; must not replace decision authority. |
| `FeedbackRelation` invalidates-condition path | **experiment narrowly** | Strong fit with freshness/invalidation while preserving history. |
| immutable historical snapshots | **adopt as design invariant where applicable** | Strongly aligned with append-only evidence/current projections. |
| `ProjectionRelation` | **adopt as design distinction** | Helps preserve projection ≠ authority. |
| `TransformationRelation` | **adopt as design distinction** | Helps identify content-changing synthesis requiring stronger scrutiny. |
| staged self-amendment | **retain as governance invariant candidate** | Prevents same-cycle self-certification. |
| `EpistemicAgentRelation` | **research only** | Relevant but not yet case-earned in O→A. |
| `AnalyticPurposeRelation` | **research only** | Useful concept, but AES already has actor/outcome/planning authorities. |
| `PreferenceRelation` | **research only** | Avoid duplicating utility/decision theory. |
| `DecisionAlgorithmRelation` | **research only** | Avoid creating another choice-rule authority. |
| `WorldModelRelation` | **defer** | No Plan 001 need has yet demonstrated the full world-model seam. |
| `AffordanceRelation` | **defer** | AES execution/action availability has not shown a gap requiring this semantic relation. |
| `ActivationRelation` | **do not add** | Neither AES nor O→A has earned a shared activation semantic contract yet. |

---

## Possible Plan 001 acceptance probes

If Company Planning decides the experiment is worthwhile, add no more than a small parallel trace around one or two existing acceptance criteria.

Candidate probes:

### Probe A — passing proxy, inadequate licence

```text
AC requires: authentic external consumer outcome
observed: local structural/unit check passes
expected:
  observation/check = PASS
  result exists
  stronger claim licence = unestablished
  criterion remains open
```

This proves that check success cannot silently promote itself into stronger evidence.

### Probe B — pre-committed criterion

Record that the relevant AC was fixed before the implementation result. Confirm that a post-result invented/changed criterion is visibly different rather than indistinguishable from the original acceptance condition.

### Probe C — invalidation without history rewrite

```text
R1:
  claim licensed under exact evidence/dependency set

R2:
  dependency/revision changes
  prior condition is no longer applicable

expected:
  R1 remains historical truth about what was believed/decided then
  current licence standing changes
  fresh observation is required for current promotion
```

### Probe D — projection versus transformation

Render the same `RepositoryContextArtifact` through the Slice 1 working surface and separately generate one model-produced synthesis. Verify the system can distinguish the source-preserving projection from the content-creating transformation and therefore apply different evidentiary treatment.

---

## Adoption test

O→A semantics should become an AES dependency or shared contract only if an authentic vertical demonstrates recurring value that cannot be supplied more simply by existing AES/native structures.

A positive adoption case should show at least one of:

- prevented false-green criterion closure;
- materially improved explanation of why a decision was entitled;
- narrower and more correct invalidation than coarse stale marking;
- materially lower reviewer reconstruction cost;
- reusable semantics across more than one AES concern/provider without authority collapse;
- clear reduction in duplicate bespoke evidence/standing logic.

Reject or keep as research if the experiment produces mainly:

- more graph/schema artifacts;
- duplicate statuses already available in native systems;
- ceremony around obvious claims;
- a second execution/planning/policy authority;
- a requirement to translate every AES artifact into O→A form;
- storage/ontology work that does not improve the authentic engineering outcome.

---

## Architectural boundary to preserve

The most useful long-term composition currently appears to be:

```text
                 O→A-shaped semantics
           evidence / standing / decision lineage

Observation -> Analysis -> Result -> Licence -> Claim -> Belief -> Decision
                                                               |
---------------------------------------------------------------|---
                    authority / execution boundary             |
                                                               v
                   AES / Enforced Planning / native owners

                governed action -> execution -> receipt/effect
                                      |
---------------------------------------------------------------|---
                                      v
                              O→A-shaped feedback

                         Effect -> Feedback
                               -> changed standing
                               -> next snapshot
```

This preserves the existing O→A boundary from Decision 018:

- O→A can own inspectable epistemic/decision lineage;
- AES/native systems own execution, admission, policy effects, and activation;
- neither system infers authority merely from an artifact or graph edge;
- historical evidence remains inspectable after current standing changes.

That is a promising architecture to test, not an adopted integration design.

---

## Questions for Company Planning / D1

Before using O→A semantics in Plan 001, answer:

1. Which AC actually needs a distinction between successful check output and licensed claim standing?
2. Can the existing selected contract/evidence provider represent that distinction adequately without O→A?
3. What is the smallest trace that would change a decision or prevent false green?
4. Does the trace remain optional/derived, or would a consumer require it as a stable contract?
5. Which exact component owns condition truth, freshness, and invalidation detection?
6. Is O→A only recording that standing, or accidentally becoming the evaluator/authority?
7. Which relation/condition identities must remain stable across revisions?
8. How will direct stakeholder utility evidence at A1 relate to technical/evidence standing without conflating the two?
9. If a stakeholder changes the direction despite technical conformance, is that represented as new planning/decision evidence rather than a retroactive falsification of earlier conformance?
10. What evidence would justify promoting any currently `declared` O→A agent-side relation into an AES-used semantic contract?

---

## Condensed recommendation

Treat O→A as a **candidate semantic donor for AES's evidence-to-decision boundary**, not as an AES subsystem by default.

For the first authentic vertical, test only enough O→A semantics to answer one concrete problem already identified by canonical AES:

> **Can AES represent that a check/result occurred successfully while the stronger claim needed for a decision is still unestablished, and can later evidence change that standing without rewriting history?**

If the answer becomes materially clearer and more operational through `LicenseRelation`, `LicenseConditionRelation`, `ClaimRelation`, selective `BeliefStateRelation`, and narrow feedback invalidation, those concepts have earned deeper provider/contract evaluation. If not, retain O→A as research and keep AES simpler.

---

## Revision-pinned reference pointers

The conclusions above are revision-bound. Re-check both repositories before any adoption/provider decision if either source has materially changed.

### Canonical AES reviewed source

- Repository: `https://github.com/BrianMills2718/agentic-engineering-system-canonical/tree/a6bd092fb16f5ebca21d621015fc40152dce3dc7`
- System boundary: `docs/architecture/SYSTEM_BOUNDARY.md`
- Human-observable delivery: `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`
- Initial gap ledger: `docs/architecture/INITIAL_GAP_LEDGER.md`
- Plan 001: `docs/plans/001_repository_context_resolution_vertical.md`
- D1 brief: `docs/plans/001_D1_contract_surface_topology_freeze.md`
- Evidence/characterization synthesis: `research/synthesis/aes-evidence-characterization-and-context-suggestions.md`
- Representation/epistemic-surface synthesis: `research/synthesis/representation-review-and-epistemic-surface-suggestions-for-aes.md`
- Fluid Governance salvage: `research/synthesis/fluid-governance-selective-salvage.md`

### O→A reviewed source

- Repository: `https://github.com/BrianMills2718/observation-to-action-metamodel/tree/a060d3ac5b1dc1691a30c784c72e948c52c25a94`
- Specification: `https://github.com/BrianMills2718/observation-to-action-metamodel/blob/a060d3ac5b1dc1691a30c784c72e948c52c25a94/04-SPEC.md`
- Vocabulary: `https://github.com/BrianMills2718/observation-to-action-metamodel/blob/a060d3ac5b1dc1691a30c784c72e948c52c25a94/03-VOCABULARY.jsonld`
- Executable constraints: `https://github.com/BrianMills2718/observation-to-action-metamodel/blob/a060d3ac5b1dc1691a30c784c72e948c52c25a94/constraints.json`
- Record-side / agent-side decision: `https://github.com/BrianMills2718/observation-to-action-metamodel/blob/a060d3ac5b1dc1691a30c784c72e948c52c25a94/08-decisions/003-record-side-and-agent-side.md`
- Reflective feedback / staged self-amendment decision: `https://github.com/BrianMills2718/observation-to-action-metamodel/blob/a060d3ac5b1dc1691a30c784c72e948c52c25a94/08-decisions/018-reflective-feedback-boundary.md`
- Release-versus-activation decision: `https://github.com/BrianMills2718/observation-to-action-metamodel/blob/a060d3ac5b1dc1691a30c784c72e948c52c25a94/08-decisions/019-repository-release-is-not-runtime-activation.md`
