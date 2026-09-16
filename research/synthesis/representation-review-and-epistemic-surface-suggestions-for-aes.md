# Representation, review, and epistemic-surface suggestions for canonical AES

Status: research synthesis; non-normative suggestions only.

Sources considered:

- canonical AES system boundary on `main`, especially `AES-SYS-002`, `AES-PLAN-003`, `AES-POL-002`, `AES-POL-004`, `AES-CTX-001`, `AES-CTX-002`, and `AES-EVID-001`;
- `research/synthesis/code-map-v4-salvage-for-aes.md`;
- `BrianMills2718/code_map_v4` at the revision reviewed by that synthesis;
- Representation Router as an additional proving source for source-bound planning/review surfaces and representation-policy boundaries.

Purpose: suggest a small set of AES design directions that combine the strongest Code Map evidence/freshness lessons with concern-centric planning/review representation, without making Code Map, a wiki, or a representation layer into a new authority.

This document does **not** adopt a new AES contract, implementation root, representation framework, or workflow. Any implementation still requires an explicit target/current gap, Company Planning derivation, ACA/incumbent capability resolution, and accepted implementation/verification topology.

---

## Executive recommendation

The canonical AES architecture would benefit from treating **current-state characterization** and **human/agent comprehension** as two different layers with an explicit boundary between them.

A useful conceptual stack is:

```text
native authorities
  target clauses / source / code / tests / runtime / planning state
                    |
                    v
revision-bound observations and evidence
                    |
                    v
current characterization
  explicit epistemic state + provenance + freshness
                    |
                    v
target / current / gap / plan projections
                    |
                    v
concern-specific working representations
  navigation / review / explanation / decision support
                    |
                    v
human or agent judgment / action
                    |
                    v
owning system performs any authoritative effect
```

The key recommendation is **not** to create one giant AES knowledge graph or one universal schema. The recommendation is to preserve several durable distinctions:

1. **authority versus observation**;
2. **observation versus current characterization**;
3. **current characterization versus gap/plan projection**;
4. **structured projection versus human-facing synthesis**;
5. **human-facing action versus authoritative effect**.

Code Map provides strong implementation lessons for the first three distinctions. Representation Router provides useful design lessons for the last two.

If only five suggestions from this document survive, retain these:

1. **Evidence has a lifecycle.** A visible assertion should be able to say what evidence supports it, which revision/environment it applies to, and whether that evidence is still current.
2. **Load-bearing relationships deserve evidence.** `requirement -> implementation -> verification` edges can be stale or unsupported independently of the nodes they connect.
3. **Ignorance should be visible at the presentation layer.** `unobserved`, `error`, `stale`, `partial`, and `unsupported` must not collapse into a visually reassuring “current” state.
4. **Facts are substrate, not comprehension.** Context surfaces should synthesize the answer to the current concern rather than dump all facts and links.
5. **Review surfaces are projections, not authorities.** A surface may coordinate target/current/gap/plan/evidence and request a decision without owning the underlying state transition.

---

# 1. Keep characterization and representation separate

The Code Map salvage synthesis already identifies a candidate characterization kernel. That is directionally strong.

One additional boundary should remain explicit:

> **Characterization determines what AES currently knows about a subject. Representation determines how a person or agent should understand or act on that knowledge for a particular concern.**

These are not the same capability.

For example, characterization might establish:

```text
subject: checkout-service/payment-adapter
revision: abc123
implementation state: observed
integration-test receipt: passed
runtime probe: stale
requirement R-17 linkage: observed-current
requirement R-23 linkage: unobserved
```

A planning surface, code-review surface, operations surface, and source-local coding context may all consume that same characterization while presenting it differently.

The representation layer should not change the characterization merely because a convenient diagram would prefer different semantics. Conversely, the characterization layer should not dictate a single UI or document format.

### Suggested AES implication

Treat a future characterization capability as a provider of **revision-bound semantic material**, not as the wiki/page/graph product.

A consuming context or review surface should ask:

```text
what concern are we answering?
which characterized subjects matter?
which target/gap/plan relationships matter?
which evidence states must remain visible?
what decision or next action should become cheap?
```

This complements `AES-CTX-001`: the wiki remains derived progressive disclosure rather than becoming the characterization authority.

---

# 2. Add an epistemic presentation discipline

AES already establishes the normative rule in `AES-POL-002`: ignorance cannot render green.

That rule should apply not only to controls internally but also to **human-facing and agent-facing representations**.

A surface should not make these states look equivalent:

```text
PASS
FAIL
UNOBSERVED
ERROR
STALE
PARTIAL
NOT APPLICABLE
```

The exact state vocabulary may differ by provider and contract. The durable requirement is that absence/failure/staleness remain legible and cannot inherit a positive visual treatment by default.

### Why this matters

Many engineering review failures are presentation failures rather than data failures:

- an old passing test is shown next to a new implementation without a stale warning;
- a missing runtime observation looks like “no incidents”;
- an extractor error results in an empty panel that looks clean;
- a planned verification relationship is presented as though it were executed evidence;
- an accepted plan item visually reads as accepted implementation conformance.

A useful representation-level invariant is:

> **Every load-bearing visible claim has an epistemic state that is either explicit or safely derivable from its supporting characterization/evidence.**

### What not to do

Do not solve this by assigning a generic model-generated confidence number to everything.

Prefer explicit states and proof meaning:

```text
current because <specific evidence>
stale because <dependency changed>
unobserved because <observer not run>
error because <observer failed>
partial because <some required semantics/evidence missing>
```

A synthetic `confidence: 0.82` is less actionable than knowing why the assertion is incomplete or invalid.

---

# 3. Make load-bearing relationships evidence-aware

Code Map's first-class relationship artifacts are especially relevant to AES.

The important lifecycle questions in AES are often relationship questions:

```text
Does requirement R realize through implementation subject S?
Does verification subject V actually test S at this revision?
Does policy P apply to boundary B?
Does capability provider C still satisfy requirement K?
Does completed work W actually close gap G?
```

Those edges can be wrong or stale even when both endpoints still exist.

### Suggested conceptual model

For load-bearing relationships, AES should eventually be able to distinguish at least:

```text
relationship kind
source subject
target subject
origin / authority of the assertion
supporting evidence or observation
subject/revision scope
freshness / epistemic state
invalidation dependencies
```

Example:

```text
R-17
  -- realized_by --> payment-adapter

origin: accepted planning topology
observed implementation revision: abc123
evidence: characterization-812
state: current
invalidates_if: payment-adapter subject changes
```

and separately:

```text
payment-adapter
  -- verified_by --> payment-integration-test

origin: planned verification topology
execution evidence: none
state: unobserved
```

The second edge should not render as green merely because the test file exists.

### Storage caution

This does **not** imply `.agentic/relationships.yaml` must own all this metadata.

Per `AES-CONTRACT-001`, native authorities should continue to own their natural typed boundaries. Relationship evidence may live in observation/evidence artifacts, a planning topology, a verification provider, or another native owner.

The requirement is semantic: AES should be able to materialize the current relationship state without pretending an asserted edge and an evidenced-current edge are identical.

---

# 4. Borrow dependency-aware freshness, but keep it provider-specific

Code Map's span-precise invalidation is a powerful example, not a universal implementation requirement.

The general rule worth adopting is:

> **Invalidate the smallest current characterization unit whose supporting evidence is no longer valid, and fail safely toward stale rather than false-current.**

Different subject types need different anchors:

- source symbol: AST/CST identity or span fingerprint;
- configuration: content hash or typed field version;
- data contract: schema/version identity;
- runtime observation: deployment/environment/revision tuple;
- planning assertion: plan revision and subject identity;
- policy applicability: policy version plus covered boundary;
- external service: observed endpoint/version/environment.

### Do not confuse two different revision questions

There are at least two separate problems:

1. **Does the old evidence still apply?**
2. **Can the user's previous focus/selection safely carry into the new revision?**

Characterization/invalidation machinery should answer the first.

A context/representation layer should answer the second and should generally use stable semantic identity plus explicit remapping rules rather than silently matching labels.

This distinction helps prevent a freshness optimization from becoming an unsafe identity-transfer rule.

---

# 5. Treat facts as substrate and synthesis as a separate quality target

Code Map's strongest product lesson is that a rigorous fact graph can still produce poor comprehension.

AES should protect itself from the same failure mode.

A generated context surface can contain all of these and still be weak:

```text
clause IDs
subject IDs
plan IDs
gap IDs
source paths
verification receipts
policy states
capability-provider links
revision hashes
```

Those are necessary substrate. They are not automatically useful context.

### A good AES context surface should answer the concern

For an implementation subject, source-local context might synthesize:

```text
What is this subject for?
Which accepted target clauses constrain it?
What is currently true at this revision?
Which gaps remain?
Which plan/work item owns the remaining change?
Which verification will decide closure?
What evidence is stale, missing, or errored?
What are the important non-claims or limitations?
What should the agent inspect or do next?
```

For a planning/review checkpoint:

```text
What was intended?
What changed?
What evidence was actually executed?
What evidence is stale or missing?
Where does implementation diverge from target or plan?
Which gap is still open?
What requires human judgment or authority?
```

### Suggested quality criterion

Do not measure a context surface primarily by artifact counts or link completeness.

A stronger criterion is:

> **Does the surface materially improve the user's or agent's ability to make the correct engineering decision at this subject while preserving uncertainty, provenance, and authority boundaries?**

That can later be operationalized through task completion, decision accuracy, time-to-answer, missed evidence, false inference rate, or other independent outcomes.

---

# 6. Use concern-specific working surfaces for planning and review

AES has an integrated lifecycle, but a person should not need to inspect the entire lifecycle graph every time they make a decision.

A useful representation principle is:

> **Project the smallest coordinated set of views that makes the current engineering question cheap to answer.**

For an AES planning/review checkpoint, a generic concern set might be:

### Target

- accepted normative clauses;
- success criteria;
- required boundaries/capabilities;
- target implementation and verification topology.

### Current

- revision-bound implementation characterization;
- current relationship state;
- observed runtime/verification/policy state;
- explicit stale/error/unobserved regions.

### Gap

- material target/current differences;
- blocked or unresolved relationships;
- evidence deficiencies;
- policy/capability discrepancies.

### Plan / execution

- dispositioned gaps;
- work units and dependencies;
- selected capability providers;
- execution/checkpoint state;
- recovery/change path.

### Evidence / review

- what actually ran or was observed;
- what those observations establish;
- what they do **not** establish;
- which exact subject/revision is under judgment;
- which decision remains human-owned.

These do not need to be five tabs or one universal interface. They are concern categories that can be represented as graph, table, matrix, timeline, sequence, diff, cards, or a coordinated surface depending on the task.

### Why this fits AES

This is consistent with `AES-SYS-002`: representations consume authoritative material without becoming authority.

It is also consistent with `AES-PLAN-003`: a “plan complete” representation cannot silently become a “gap closed” representation without fresh characterization/evidence.

---

# 7. Keep review disposition separate from workflow mutation

One lesson from Representation Router that fits AES especially well is the separation between:

```text
rendered review state
human disposition
authoritative workflow mutation
```

A surface may show:

```text
Approve
Request changes
Accept exception
Escalate
Replan
Retry observation
```

but rendering the control does not grant authority.

For a consequential action, the integration should be able to identify conceptually:

```text
action subject
exact subject revision
destination / owning system
target revision or concurrency boundary
actor / authority basis
stale-submission behavior
evidence retained with the decision
```

The exact contract belongs to the appropriate authority/provider, not to a universal AES UI schema.

### Why this matters

AES integrates systems with distinct authorities. A review surface that blurs local UI state and authoritative workflow state would undermine one of the architecture's strongest rules.

The representation layer should therefore be able to say:

```text
This is a proposed/local disposition.
No authoritative state changed.
```

or:

```text
This action was accepted by owner X against exact revision Y.
Receipt Z records the effect.
```

without treating those as the same event.

---

# 8. Apply negative controls to lifecycle claims, not just code behavior

`AES-POL-004` already requires important controls to prove they can fail.

The same discipline can strengthen AES context/review mechanisms.

Examples:

### Evidence presentation

```text
current matching evidence
  -> displayed as current

same evidence against changed subject revision
  -> displayed stale / requires refresh
```

### Verification relationship

```text
executed receipt for exact subject
  -> observed verification edge

test definition exists but no receipt
  -> planned/configured, not executed
```

### Characterization observer

```text
observer succeeds
  -> observation recorded

observer crashes
  -> ERROR / unresolved, never PASS
```

### Plan linkage control

```text
implementation linked to accepted plan
  -> ALLOW

same implementation without required plan linkage
  -> BLOCK

recovery: establish sanctioned plan linkage
  -> ALLOW
```

### Review concurrency

```text
review subject unchanged
  -> disposition may proceed

subject revision changed after review loaded
  -> reject or require refresh
```

This gives AES evidence that its representation/context layer preserves the same epistemic discipline as its internal control layer.

---

# 9. Separate recommendation/evaluation from self-confirmation

Code Map's circular retrieval evaluation is a useful warning for AES.

AES should avoid evaluation structures such as:

```text
planner produces topology
planner's own topology validator confirms topology
therefore planning quality proven
```

or:

```text
characterizer creates relationship graph
same graph defines eval ground truth
relationship retrieval scores highly
therefore characterization useful
```

or:

```text
context generator displays all expected IDs
snapshot tests pass
therefore user comprehension improved
```

These may establish implementation conformance, but not usefulness or correctness of the higher-level decision.

### Prefer independent signals

Depending on the capability, better evidence may include:

- authentic external-consumer outcome;
- human review accuracy;
- time-to-correct-decision;
- false acceptance / missed-gap rate;
- independent runtime behavior;
- independently specified success criteria;
- policy block/recovery outcome;
- independent subject characterization;
- transfer to a new case not used to produce the recommendation.

This aligns strongly with `AES-DOGFOOD-001` and `AES-DOGFOOD-002`.

---

# 10. Suggested thin slice for the first authentic AES vertical

When Company Planning selects the first authentic external-consumer vertical, it can test these ideas without first designing a general framework.

Choose one concern that includes:

1. one accepted target clause/success criterion;
2. one implementation subject at exact revision R1;
3. one load-bearing relationship from target/plan to that subject;
4. one verification subject;
5. one observation/verification receipt;
6. one materialized current characterization;
7. one visible epistemic state other than PASS/current;
8. one derived gap;
9. one governed implementation change producing revision R2;
10. invalidation of only the characterization/evidence affected by that change;
11. fresh observation at R2;
12. recomputed gap state;
13. one concern-specific review/context surface synthesizing the result;
14. one human/agent decision with explicit authority boundary;
15. one independent outcome indicating whether the surface helped.

A good test case deliberately includes a failure path.

Example:

```text
TARGET:
  request tracing must survive retry path

CURRENT @ R1:
  implementation exists
  integration test definition exists
  execution receipt missing

SURFACE:
  target = accepted
  implementation = observed
  verification = UNOBSERVED
  gap = open

EXECUTION:
  verification command errors

SURFACE:
  verification = ERROR
  gap remains open
  recovery = repair test environment and rerun

RECOVERY:
  test runs at R1 and fails

PLAN / IMPLEMENT:
  governed change produces R2

INVALIDATION:
  R1 behavior characterization -> stale
  unrelated characterization remains current

FRESH OBSERVATION @ R2:
  integration test passes

RECOMPUTE:
  gap closed if all other target conditions satisfied

REVIEW:
  human sees what changed, exact evidence, residual non-claims, and closure basis
```

This one thin slice exercises characterization, freshness, gap reconciliation, policy recovery, planning/execution, evidence, and concern-centric representation without requiring a universal implementation in advance.

---

# 11. Candidate contract questions for Company Planning

If the first vertical demonstrates a real need, Company Planning should resolve these before creating new reusable contracts:

1. What is the smallest stable subject identity needed for the concern?
2. Which source owns each mutable fact?
3. Which records are immutable observations versus derived current projections?
4. Which exact revision/environment dimensions determine evidence applicability?
5. Which relationships are merely planned, and which need observed-current status?
6. What dependencies invalidate each observation or relationship?
7. Which epistemic states must consumers preserve?
8. Which states are provider-specific and should not be standardized?
9. Which claims are synthesized for comprehension rather than stored as authority?
10. Which visible actions are local proposals versus authoritative effects?
11. What stale-submission/concurrency behavior is required for decisions?
12. Which controls need negative/counterfactual evidence?
13. What independent outcome evaluates the context/review surface?
14. What runtime/cognitive/maintenance cost is acceptable for freshness precision?
15. Does the same abstraction recur in at least two independent consumers before it becomes a reusable AES/Data Contracts capability?

---

# 12. Things not to adopt yet

## 12.1 No universal AES evidence mega-schema

The Code Map artifact envelope is a valuable example, not a reason to copy every field into one AES contract. Start from the actual vertical and keep provider-native authority intact.

## 12.2 No universal subject identity ontology

Code symbols, deployment subjects, data-contract versions, planning records, policies, and external-service observations may need different identity mechanisms.

## 12.3 No confidence score as a substitute for proof meaning

Prefer explicit evidence type, state, revision and limitation over a scalar score that hides why a claim is trusted.

## 12.4 No whole-lifecycle “single pane of glass” as a goal

AES should support coordinated concern-specific views, not force every lifecycle fact into one giant dashboard or graph.

## 12.5 No representation system as workflow authority

A graph, wiki, dashboard, review workbench, or source-local panel remains a projection over native authorities.

## 12.6 No large new representation framework before an authentic gap

Representation Router may be a useful incumbent/reference source for representation-policy ideas, but canonical AES should disposition it through the same capability-first process as any other incumbent rather than implicitly importing it.

## 12.7 No per-sentence generated test requirement

Code Map's negative-controlled synthesis is an interesting evidence technique. AES should prefer native verification subjects and plan-derived criteria first, using generated probes only where they solve an explicit verification gap.

---

# 13. Candidate AES dispositions suggested by this synthesis

These are research suggestions, not accepted decisions.

| Idea | Suggested disposition |
| --- | --- |
| revision-bound observation/evidence semantics | **strong candidate; already aligned with accepted AES boundary** |
| dependency-aware freshness / selective invalidation | **strong candidate; test in authentic vertical** |
| evidence-bearing load-bearing relationships | **strong candidate; test across target→implementation→verification** |
| explicit epistemic presentation states | **strong candidate; make UI/context preserve `AES-POL-002`** |
| concern-specific planning/review working surfaces | **salvage as presentation principle; do not make a new authority** |
| stable semantic focus across representations | **candidate presentation behavior; revision remap must remain explicit** |
| facts-versus-synthesis separation | **adopt strongly as context-quality principle** |
| action/authority separation in review surfaces | **adopt strongly as integration principle** |
| negative-control testing for presentation/decision claims | **strong methodological candidate** |
| independent evaluation signals | **adopt strongly as evidence principle** |
| generic confidence scores | **avoid as primary epistemic mechanism** |
| universal AES knowledge graph/wiki product | **do not adopt** |
| universal representation/workbench product | **do not adopt** |
| Code Map extractor matrix or Python identity rules | **provider-specific only** |
| generated tests for every synthesized sentence | **specialized evidence technique only** |

---

# 14. Relationship to existing Code Map salvage synthesis

This document is intended to complement, not replace, `code-map-v4-salvage-for-aes.md`.

That document answers:

> Which Code Map mechanisms are worth salvaging into AES characterization/evidence capabilities?

This document adds a second question:

> Once AES has trustworthy target/current/gap/plan/evidence material, how should that material be projected into useful planning, review, coding, and decision contexts without collapsing authority or epistemic state?

The combined answer is roughly:

```text
Code Map lesson:
  make current-state knowledge revision-bound, evidence-bearing and invalidatable

AES architecture:
  preserve native authority and recompute gaps from fresh characterization

Representation/review lesson:
  synthesize only the concern-relevant material into a working surface,
  keep uncertainty visible,
  and keep human-facing controls separate from authoritative effects
```

This creates a coherent direction without requiring any of the source systems to become the canonical AES product architecture.

---

## Condensed recommendation

For the first authentic AES vertical, do **not** begin by designing the final wiki, graph, workbench, evidence schema, or universal subject model.

Begin with one real concern and prove this chain:

```text
native target + exact implementation revision
        ↓
revision-bound observation
        ↓
current characterization with explicit epistemic state
        ↓
derived gap
        ↓
Company Planning + capability resolution + governed execution
        ↓
new exact implementation revision
        ↓
precise invalidation + fresh observation
        ↓
recomputed gap
        ↓
concern-specific synthesized review/context surface
        ↓
human/agent decision
        ↓
owner-controlled effect or explicit no-effect
```

If that chain works and the same characterization/presentation semantics recur across independent consumers, promote the smallest repeated abstraction into a reusable capability or provider-neutral contract.

Until then, keep these ideas as evidence-backed suggestions rather than another architecture layer.