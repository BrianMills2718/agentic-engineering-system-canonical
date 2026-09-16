# AES evidence, characterization, and context suggestions

Status: research synthesis; non-normative suggestions only.

Date: 2026-09-16

Purpose: capture design suggestions for the canonical Agentic Engineering System (AES) around evidence, characterization, freshness, proof adequacy, relationship semantics, and source-local agent context. These suggestions are intended to inform future Company Planning and capability disposition. They do **not** alter the accepted system boundary, select an implementation topology, or transfer authority.

## Relationship to Code Map V4

AES is **not based on Code Map V4** and should not be described as a continuation, derivative, or generalization of it.

The two systems have different goals, histories, and architectural centers:

- canonical AES is an integrated engineering lifecycle spanning target, current, gap, planning, capability composition, governed execution, evidence, characterization, reconciliation, and learning;
- Code Map V4 is a repository-characterization / evidence / comprehension system developed around source analysis, claim grounding, freshness, and generated context.

There is nevertheless useful **convergence**. Code Map V4 explored several evidence and characterization mechanisms that happen to be relevant to problems AES independently defines in clauses such as `AES-PLAN-003`, `AES-POL-002`, `AES-POL-004`, `AES-CTX-002`, and `AES-EVID-001`.

Accordingly, Code Map V4 is treated here only as one incumbent evidence source for transferable lessons. Nothing in this document assumes that AES should inherit Code Map's product architecture, ontology, wiki model, extractor matrix, or implementation.

For the narrower Code Map-specific inventory, see [`code-map-v4-salvage-for-aes.md`](code-map-v4-salvage-for-aes.md).

---

# Executive suggestion

The canonical AES architecture already has the right high-level lifecycle:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

The next important design question is not whether AES needs more artifacts. It is how AES will know, at any exact revision, **what it has sufficient evidence to believe**, **what that evidence actually establishes**, **when the belief is no longer current**, and **what bounded context an engineering agent should receive when acting on a subject**.

A useful design direction is therefore:

```text
native authorities
      |
      v
raw observations / execution receipts
      |
      v
proof-adequacy + provenance + freshness evaluation
      |
      v
materialized current characterization
      |
      +--> gap reconciliation
      +--> evidence-bearing relationships
      +--> source-local engineering context
      +--> progressive-disclosure wiki synthesis
```

The most important suggestions are:

1. **Distinguish the proof a criterion requires from the check that actually ran.** A passing proxy must not silently become sufficient evidence for a stronger claim.
2. **Keep generated interpretations in a candidate state until promotion criteria are met.** Model confidence must not substitute for evidence adequacy.
3. **Bind important observations to exact revisions, environments, subjects, and dependencies.** Current truth must be invalidatable.
4. **Treat load-bearing relationships as evidence-bearing assertions where necessary.** `requirement -> implementation -> verification` edges can themselves be wrong or stale.
5. **Generate source-local engineering packets, not raw graph dumps.** Context should synthesize target, current, gap, plan, verification, risk, and recovery information for the subject being changed.
6. **Preserve explicit epistemic states.** `UNOBSERVED`, `ERROR`, and `STALE` must never collapse into green.
7. **Use independent evaluation signals for important capability claims.** A mechanism should not construct the answer key used to certify itself.
8. **Resist substrate completion as a proxy for engineering value.** The first authentic vertical should determine which of these abstractions are actually necessary.

These are design constraints and hypotheses for the first vertical, not a request to build a universal evidence platform before Company Planning derives the topology.

---

# 1. Separate required proof from observed check

One of the highest-value ideas to preserve is an explicit distinction between:

```text
what kind of evidence would be sufficient for this criterion?
```

and:

```text
what check did the system actually perform?
```

Code Map V4 called these `proof_kind` and `check_type`. AES does not need to reuse those names or that taxonomy, but the semantic distinction is important.

## Why this matters

A check can pass while still being inadequate for the claim.

Examples:

```text
criterion:
  authentic external consumer behavior works

required evidence:
  external runtime behavior

observed check:
  unit test

check result:
  PASS

claim status:
  INSUFFICIENT_EVIDENCE
```

or:

```text
criterion:
  policy recovery path restores an allowed execution state

required evidence:
  observed BLOCK -> recovery -> ALLOW transition

observed check:
  configuration file contains recovery_command

check result:
  PASS

claim status:
  INSUFFICIENT_EVIDENCE
```

Without this distinction, AES can accidentally upgrade a structural proxy into behavioral confidence.

## Suggested principle

> **A passing check proves no more than the semantics of that check. Evidence adequacy is evaluated separately against the criterion being supported.**

This fits the existing canonical boundary particularly well:

- `AES-PLAN-003` already says plan completion does not establish conformance;
- `AES-POL-004` already requires counterfactual / negative-control evidence for important controls;
- `AES-DOGFOOD-001` and `AES-DOGFOOD-002` already require an authentic external lifecycle rather than self-description.

## Possible future shape

Illustrative only:

```yaml
evidence_claim:
  criterion_id: AES-DOGFOOD-001
  required_evidence_kind: authentic_external_behavior
  observed_check_kind: local_unit_test
  result: pass
  adequacy: insufficient
  reason: does not cross the external consumer boundary
```

The exact contract should be derived from the first vertical rather than standardized prematurely.

---

# 2. Use monotonic evidence promotion for generated interpretations

AES will likely contain model-produced outputs in planning, characterization, review, context generation, and perhaps capability reasoning. The safest useful pattern is an asymmetric promotion model:

```text
raw evidence
   |
   v
candidate interpretation
   |
   v
promotion checks
   |
   v
operational characterization / context
```

A reviewer or generator may propose a stronger interpretation, but it should not be able to create the missing evidence that makes the interpretation operational.

## Suggested asymmetry

A model or reviewer may:

- propose a characterization;
- identify a possible contradiction;
- identify missing evidence;
- downgrade confidence;
- mark a relationship disputed;
- request re-observation;
- surface uncertainty.

It should not, solely by assertion:

- convert `UNOBSERVED` to `PASS`;
- convert stale evidence to current;
- strengthen the required proof kind;
- manufacture provenance;
- promote a proxy check to authentic behavioral evidence;
- turn a disputed relationship into an evidenced-current relationship.

## Confidence should be derived where operational

Models may report their own uncertainty because that can be useful diagnostic information. But operational trust should derive from things such as:

- evidence kind;
- exact subject and revision binding;
- independent corroboration where required;
- freshness;
- negative-control or counterfactual behavior;
- scope/coverage;
- authority provenance;
- known residuals.

A high-confidence model statement with weak evidence remains weak operational evidence.

## Why this matters for AES

This gives AES a disciplined way to use capable agents without making the agent itself an authority database.

It also preserves `AES-SYS-002`: integration does not collapse native authority.

---

# 3. Revision-bound evidence should be first-class

`AES-EVID-001` already establishes the key rule: observations/evidence are retained, while current-state and gap views are materialized from the latest valid revision-bound evidence.

The implementation implication is that important observations eventually need enough provenance to answer:

```text
what was observed?
about which subject?
at which exact revision?
in which relevant environment?
by which observer/control/provider version?
using which supporting inputs?
what dependencies make this observation no longer applicable?
what was the outcome?
```

## Minimal conceptual envelope

Illustrative, not normative:

```yaml
observation_id: obs-...
subject_ref: ...
revision: ...
environment_ref: ...
observer:
  capability: ...
  version: ...
source_refs: [...]
dependency_refs: [...]
status: observed | unobserved | error | stale
payload: ...
```

AES should avoid requiring every native tool or capability to emit one universal giant schema. Native typed boundaries should remain native. A shared envelope is justified only where cross-capability lifecycle reasoning actually needs it.

## Important consequence

A statement like:

```text
"the current implementation satisfies criterion C"
```

should eventually be resolvable to evidence that is specific enough to determine whether that statement still applies after a change.

Otherwise `current` becomes historical prose rather than a materialized state.

---

# 4. Freshness should be executable, not decorative metadata

A revision-bound evidence model is only useful if invalidation has operational consequences.

The desired lifecycle is conceptually:

```text
observation at revision R
        |
        v
current characterization
        |
     dependency changes
        |
        v
support still applicable?
      /        \
    yes        no
     |          |
 current      stale
                |
                v
          fresh observation
```

## Fail safely toward stale

AES should prefer false-stale over false-current when the system cannot determine whether supporting evidence still applies.

That does not mean invalidating the entire repository after every edit. The first vertical should start with the cheapest defensible dependency unit, for example:

- exact artifact/content hash;
- file hash;
- test/config hash;
- environment fingerprint;
- provider version;
- accepted target/plan revision.

Only introduce AST/CST/source-span precision where measured false-stale churn justifies the complexity.

## Derived context rule

Generated wiki/context may surface stale evidence, but it should not silently present stale evidence as current.

A useful invariant is:

```text
STALE evidence visible as STALE      -> allowed
STALE evidence rendered as CURRENT   -> invalid projection
```

The same should apply to `ERROR` and `UNOBSERVED` states.

---

# 5. Preserve explicit epistemic states across interfaces

The canonical system boundary already requires meaningful states including pass, fail, none/unobserved, error, and stale.

The key implementation requirement is that these states survive composition.

For example:

```text
observer crashed
   -> ERROR
   -> current unresolved
   -> gap unresolved
```

must never become:

```text
observer crashed
   -> missing row
   -> no detected gap
   -> green
```

## Suggested minimum discipline

Where a control or characterization result feeds another lifecycle decision, distinguish at least:

```text
PASS
FAIL
UNOBSERVED / NONE
ERROR
STALE
```

Additional domain-specific states can exist beneath this layer, but no downstream materializer should need to guess whether absence means success, failure, not applicable, not run, or crashed.

## Failure is evidence about the observation process

An observation attempt that errors is itself useful evidence:

- the subject may not be characterizable by the chosen provider;
- the environment may be broken;
- a policy or capability may have hidden preconditions;
- the verification topology may be wrong.

That outcome should remain inspectable rather than disappearing from the current projection.

---

# 6. Treat important relationships as assertions with lifecycle semantics

The canonical repository already reserves `.agentic/relationships.yaml` for future topology such as:

```text
requirement -> implementation subject -> verification subject
```

The first version of these relationships may be simple structural links. However, load-bearing relationships should eventually be able to distinguish:

```text
asserted / planned relationship
```

from:

```text
evidenced-current relationship
```

because edges can be wrong or stale even when their endpoints still exist.

## Examples

Questions gap reconciliation will eventually need to answer include:

- Does implementation subject `S` still realize criterion `C`?
- Does verification subject `T` still exercise the behavior it claims to verify?
- Does a policy still govern this boundary?
- Does a capability-provider binding still satisfy the required semantic capability?
- Does the current plan still own this implementation change?

These are relationship claims.

## Possible future metadata

Illustrative only:

```yaml
relationship:
  kind: verified_by
  source: implementation-subject
  target: verification-subject
  origin: accepted-planning-output
  observed_at_revision: ...
  evidence_refs: [...]
  freshness: current | stale | unobserved | error
  invalidation_refs: [...]
```

Not every graph edge deserves this weight. Use it where the edge itself participates in conformance, routing, safety, or gap closure.

---

# 7. Generate source-local engineering packets

`AES-CTX-002` is potentially one of the most valuable practical outputs of the architecture.

Once implementation subjects exist, an agent operating on a subject should not need to load the entire AES ontology, all project history, or every evidence record.

Instead, AES should produce a bounded **subject packet** / **engineering packet** / source-local context projection.

The name is unimportant; the behavior matters.

## Suggested packet contents

For a concrete implementation subject:

```text
subject identity
  |
  +-- applicable target clauses / success criteria
  +-- current characterization
  +-- current gaps / unresolved uncertainty
  +-- accepted plan/work ownership
  +-- capability/provider decisions
  +-- relevant neighboring subjects / seams
  +-- verification subjects and required proof kinds
  +-- latest evidence + freshness warnings
  +-- commands / controls likely needed
  +-- known risks / non-obvious interactions
  +-- sanctioned recovery / plan-change path
```

The packet should be revision-aware and rebuildable.

## What it should not become

It should not be:

- a second authority;
- a dump of every graph node;
- a restatement of every requirement;
- a static `AGENTS.md` that goes stale silently;
- an opaque model summary with no provenance.

## Success criterion

A useful evaluation question is:

> Does this packet materially improve an agent's ability to make the correct engineering decision at this subject while preserving uncertainty and native authority provenance?

That is stronger than measuring whether the packet contains many links or facts.

---

# 8. Facts are substrate; comprehension requires synthesis

A major recurring failure mode in repository-context systems is assuming that a sufficiently complete structured fact inventory automatically becomes useful engineering comprehension.

It does not.

AES should preserve three conceptual layers:

```text
1. native authority + raw evidence
                |
                v
2. structured materialized projections
   target / current / gap / plan / relationships
                |
                v
3. derived comprehension
   wiki / subject packet / agent briefing
```

Layer 3 must synthesize, not merely enumerate.

For a subject, useful synthesis answers things like:

- What is this subject responsible for?
- Which target criteria constrain it?
- What is currently known to be true?
- Which gaps remain?
- Which interactions or failure modes are easy to miss?
- What plan owns the change?
- What verification would actually establish success?
- What evidence is stale, missing, disputed, or weak?
- What recovery/change path is available if a control blocks the work?

## Warning against empty scaffolding

An elaborate generated template with headings such as `Invariants`, `Warnings`, `Tests`, and `Architecture` is not useful if those sections merely rearrange the same fact inventory.

The test is not whether the context has the right headings. The test is whether it provides **decision-relevant synthesis that was not already available as a flat fact dump**, while keeping its evidentiary basis visible.

---

# 9. Use negative controls and counterfactuals where claims are load-bearing

`AES-POL-004` already states the right principle: important controls must prove they can fail.

This idea should be generalized carefully beyond policy controls wherever false green would be costly.

A meaningful proveout often includes:

```text
known-good condition       -> expected PASS / ALLOW
known-bad condition        -> expected FAIL / BLOCK
observer/control error     -> expected ERROR, never PASS
stale evidence             -> expected STALE / RECHECK
scope boundary             -> evidence control applies where claimed
recovery route             -> blocked state can reach valid allowed state
```

## Proof meaning must remain explicit

A counterfactual check does not prove more than it tests.

For example:

```text
mutation/counterfactual survived correctly
```

can support:

```text
this check is sensitive to this class of defect
```

but not automatically:

```text
this natural-language statement is semantically exact under all conditions
```

AES should prefer precise proof language over broad labels such as `verified` when the underlying guarantee is narrower.

---

# 10. Evaluation must not be circular

An important methodological rule is:

> **A mechanism should not construct the answer key used to certify itself unless the evaluation explicitly acknowledges that dependency.**

Examples for AES:

- do not evaluate a planner solely by whether its generated plan says all requirements are handled;
- do not evaluate a policy registry solely against the registry's own claimed scope;
- do not evaluate a characterization provider solely against another projection generated from the same extractor path;
- do not evaluate a capability provider solely from provider-authored fit metadata;
- do not treat plan completion as gap closure;
- do not evaluate generated context only by asking the same generator whether the context is helpful.

The existing authentic external-consumer requirement is a strong defense against this failure mode.

Where feasible, important capability evaluations should use a source of truth or outcome that is independent along the relevant axis.

Independence should be named precisely when it matters, for example:

- source independence;
- model independence;
- session/process independence;
- implementation independence;
- adjudicator independence;
- organizational/human independence.

Avoid using the bare word `independent` as though all of these were equivalent.

---

# 11. Suggested operating maxim

A useful maxim from adjacent evidence-system work is:

> **Capture broadly, normalize selectively, operationalize strictly.**

For AES this can mean:

## Capture broadly

Retain raw observations, receipts, failures, rejected fits, and useful execution evidence when they are cheap enough and may matter later.

## Normalize selectively

Create shared representations only where cross-capability lifecycle reasoning actually requires them.

Do not force every planner, policy engine, verification provider, code analyzer, capability provider, and runtime probe into one universal domain ontology.

## Operationalize strictly

Allow an observation or interpretation to drive:

- gap closure;
- current-state green status;
- policy decisions;
- agent context;
- capability-selection confidence;
- conformance claims;

only when provenance, freshness, proof adequacy, and authority semantics support that use.

This helps AES avoid both extremes:

```text
one giant universal schema for everything
```

and:

```text
unrelated opaque subsystem outputs that cannot participate in one lifecycle
```

---

# 12. Do not build a universal characterization platform before the first vertical

These suggestions should **not** trigger a structure-first implementation pass.

The canonical repository currently has no accepted implementation root, and that is appropriate.

The first authentic vertical should determine the minimum evidence and characterization semantics actually required.

A reasonable progression is:

```text
1. Company Planning selects a real vertical and target topology.
2. Derive the evidence questions the vertical must answer.
3. Identify which incumbent capabilities can answer them.
4. Define the minimum shared envelope/relationship/freshness semantics needed.
5. Run the lifecycle.
6. Observe false-green, false-stale, context, cost, and authority failures.
7. Generalize only from demonstrated recurring need.
```

Do not begin by implementing:

- a universal claim grammar;
- a universal subject ontology;
- a graph database;
- a large extractor matrix;
- a generalized wiki compiler;
- a universal proof taxonomy;
- per-sentence LLM verification;
- source-span invalidation everywhere.

Any of these may later become justified. None should be assumed to be part of AES merely because a related system found them useful.

---

# 13. Thin-slice experiment for the first vertical

When the first external-consumer vertical is accepted, a deliberately small evidence/characterization slice could test the suggestions in this document.

One concern should include:

1. one accepted target clause or success criterion;
2. one implementation subject;
3. one verification subject;
4. an explicit statement of required evidence kind;
5. one observation receipt bound to an exact revision;
6. one materialized current characterization;
7. one derived gap;
8. one accepted implementation plan/work unit;
9. governed implementation that changes the subject;
10. explicit invalidation of prior evidence;
11. fresh observation;
12. recomputed gap state;
13. regenerated source-local engineering context;
14. one deliberate `ERROR`, `STALE`, or policy `BLOCK -> recovery -> ALLOW` path.

## Add one proof-adequacy mismatch on purpose

The slice should include a case where a check passes but the required proof is deliberately stronger.

Example:

```text
required:
  authentic external runtime outcome

available:
  unit test passes

expected AES state:
  check PASS
  criterion NOT YET CONFORMANT / INSUFFICIENT EVIDENCE
```

This would directly prove that AES does not confuse check success with criterion satisfaction.

## Add one freshness transition on purpose

Example:

```text
revision R1:
  verification current

revision R2:
  implementation dependency changes
  prior verification becomes STALE

fresh verification:
  observation at R2
  current rematerialized
```

This would prove that `AES-EVID-001` is operational rather than documentary.

---

# 14. Questions for Company Planning

When evidence/characterization becomes relevant to a real vertical, Company Planning should answer at least the following.

## Proof and conformance

1. What exact success criteria exist?
2. What kind of evidence would actually be sufficient for each criterion?
3. Which planned checks are exact evidence versus structural or behavioral proxies?
4. What does `PASS` mean for each check, and what does it **not** mean?
5. Which residual uncertainty is acceptable?

## Revision and freshness

6. Which exact revision/environment dimensions must be captured?
7. What dependencies make each observation stale?
8. What is the cheapest safe invalidation granularity for this vertical?
9. What happens when freshness cannot be determined?

## Relationships

10. Which requirement -> implementation -> verification relationships are merely planned topology?
11. Which relationships must become evidenced-current before gap closure?
12. Which relationship changes should invalidate current characterization?

## Generated interpretation

13. Which model outputs are only candidates?
14. What promotes a candidate to operational context/current characterization?
15. Which reviewers may downgrade or dispute, and which authority can actually establish stronger evidence?

## Context

16. What minimum subject packet lets an agent act correctly?
17. What information would be distracting or dangerously stale?
18. What synthesis must be generated that is not already present in the structured facts?
19. How will the system expose weak, stale, disputed, or missing evidence?

## Evaluation

20. What outcome source is independent enough to evaluate the mechanism being tested?
21. What false-green control will prove the system can reject an inadequate success signal?
22. What external outcome determines whether the added evidence/context machinery improved engineering performance?
23. What runtime, cognitive, maintenance, and invalidation cost would make the mechanism not worth adopting?

---

# 15. Suggested non-goals

Unless future evidence-backed gaps justify them, the following should remain non-goals for canonical AES:

- becoming a Code Map product or repository-symbol wiki;
- making Code Map V4 an architectural dependency;
- treating code characterization as the center of the AES lifecycle;
- creating a second mutable authority for facts already owned by native systems;
- forcing all evidence into one universal domain model;
- considering a model's confidence score evidence of conformance;
- considering a passing proxy check equivalent to the required proof;
- treating an artifact count, graph density, evidence count, or generated-page count as a proxy for engineering value;
- generating source-local context before there is a real subject, target, current state, gap, and plan to contextualize.

---

# 16. Primary risk: tractable substrate can crowd out the hard product outcome

There is a broader lesson worth carrying into AES from multiple predecessor and adjacent systems.

Evidence schemas, typed relations, policy registries, plan contracts, generated indexes, and validation rules are attractive work because they provide clean artifacts and green checks.

The hard outcome is whether the complete system helps real engineering work reach correct, evidenced, policy-compliant outcomes with acceptable cost.

AES is particularly vulnerable to building an elegant meta-system whose internal structures are excellent while the authentic engineering loop remains unproven.

The existing `AES-DOGFOOD-001` and `AES-DOGFOOD-002` requirements are therefore load-bearing safeguards.

A useful filter for any proposed infrastructure mechanism is:

> **Which wrong, unsafe, stale, or unnecessarily expensive engineering decision in the authentic vertical does this mechanism make easier to avoid?**

If the answer is not yet concrete, retain the mechanism as research rather than implementation.

---

# 17. Condensed recommendation

If these suggestions are reduced to five design rules, retain the following.

## A. Evidence adequacy is separate from check success

A check may pass while the criterion remains unsupported. Record both required proof and observed check semantics.

## B. Current truth must be invalidatable

Important current-state claims need enough revision, environment, provenance, and dependency information to become stale when their support no longer applies.

## C. Generated interpretations do not promote themselves

Model outputs remain candidates until the lifecycle's evidence and authority rules allow promotion. Review may challenge or downgrade without manufacturing stronger proof.

## D. Context must synthesize the engineering decision surface

Source-local agent context should combine target, current, gap, plan, verification, risk, freshness, and recovery information. A fact graph alone is not comprehension.

## E. The authentic vertical decides which abstractions survive

Do not implement a generalized characterization/evidence platform in advance. Use one real lifecycle to discover the minimum shared semantics that prove necessary.

---

## Suggested disposition

Treat this document as a **candidate design input to Company Planning**, not an accepted target amendment.

The strongest ideas are compatible with the existing system boundary and mostly make already-accepted clauses more operational:

- `AES-PLAN-003` — proof adequacy / fresh evidence rather than plan-completion green;
- `AES-POL-002` — explicit epistemic state preservation;
- `AES-POL-004` — negative-control / counterfactual discipline;
- `AES-CTX-002` — source-local engineering packets;
- `AES-EVID-001` — revision-bound observations, freshness, and rematerialized current state;
- `AES-DOGFOOD-001/002` — independent authentic outcome and end-to-end closure.

Future planning should decide whether these ideas require a small shared characterization/evidence capability, composition of existing providers, or no new local implementation at all.
