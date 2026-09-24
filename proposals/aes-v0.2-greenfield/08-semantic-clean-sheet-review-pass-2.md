# AES v0.2 semantic clean-sheet review — pass 2: references and authority

Status: **proposal review / non-normative**
Date: 2026-09-24

## Goal

Define the minimum semantic joins required by the Greenfield MVP without
introducing a universal relationship registry.

The test is:

> Can every load-bearing relationship be owned by one semantic fact or derived
> mechanically from authoritative/observed facts?

If yes, a separate authored relationship object is unnecessary.

## Proposed reference model

### Outcome

An outcome is the first-class expression of intended value.

Candidate fields:

- id
- statement
- actor_or_consumer
- optional non_goals

It is part of accepted target.

### Normative item

A normative item links to one or more outcomes when applicable.

~~~text
normative_item
  -> outcome_refs
~~~

This answers **why this obligation exists** without making outcome prose a
requirement subtype.

### Success criterion

A criterion references one or more target obligations/outcomes that it can help
establish.

~~~text
success_criterion
  -> target_refs
  -> evidence_requirements
~~~

The criterion owns what would count as adequate proof, not the concrete test or
review implementation.

### Failure mode

A failure mode owns:

~~~text
failure_mode
  -> threatens_refs
  -> response requirements
~~~

A response requirement identifies the role:

~~~text
prevent | detect | contain | recover
~~~

and links to required capabilities, obligations or criteria. Concrete
implementation/control subjects are planned later.

### Capability requirement

A capability requirement owns:

~~~text
capability_requirement
  -> target_refs
~~~

A selected provider binding, when one exists, is a distinct accepted realization
fact:

~~~text
provider_binding
  -> capability_ref
  -> provider_identity
  -> disposition
  -> semantic_boundary / nonclaims
~~~

This prevents capability identity from collapsing into provider identity.

### Realization unit

A realization unit owns the grouping decision:

~~~text
realization_unit
  -> target_refs
  -> capability_refs
  -> planned_artifact_refs
~~~

The unit exists because those subjects require a coherent responsibility,
ownership, state, interface, replacement, verification, or failure/recovery
boundary.

The storage label component remains undecided.

### Planned artifact

A planned artifact owns:

~~~text
planned_artifact
  -> exact_path OR generation_rule_ref
  -> semantic_justification_refs
  -> realization_unit_ref when applicable
~~~

The existence of the artifact is itself an accepted realization commitment.

### Planned symbol commitment

A symbol commitment is subordinate to one planned artifact:

~~~text
planned_symbol_commitment
  -> artifact_ref
  -> target_refs
  -> optional criterion_refs
  -> optional normative signature/type
~~~

No global symbol registry is implied.

### Verification subject

A verification subject owns the planned proof mapping:

~~~text
verification_subject
  -> criterion_refs
  -> evidence_requirement_refs/match
  -> execution_or_review_locator
~~~

This is where exact test files/symbols, human review artifacts, LLM rubric
definitions, runtime probes, or external-consumer observations are planned.

### Plan

A plan owns only a transition:

~~~text
plan
  -> origin_gap_refs
  -> intended_transition
  -> proposed target changes
  -> execution slices/probes
  -> completion evidence requirements
~~~

When a target change is accepted, its durable semantics move into the owning
target facts. The historical plan remains evidence of why/when the transition was
attempted, not the permanent owner of the target.

### Provider binding

Provider binding is required when an AES capability is satisfied by a distinct
provider or composition whose identity materially affects the accepted
realization.

Candidate fields:

- capability_ref
- provider_identity
- disposition: reuse | configure | adapt | compose | residual
- semantic_boundary
- owned_elsewhere
- AES_residual_if_any
- replacement_boundary

This is semantic planning/architecture information, not package-manager metadata.

### Realized repository characterization

Characterization owns observations such as:

~~~text
realized artifact path + digest
native symbol identity
signature/type
docstring
observed dependencies
test target edges
other provider-specific realized facts
~~~

These facts link back to planned subjects when identity can be established.

A missing mapping is itself useful information; the characterizer must not invent
a target relation solely because a file or symbol looks similar.

### Observation

An observation owns:

~~~text
what observer ran
which exact subject/revision it observed
what result/error occurred
~~~

It does not own adequacy for a criterion.

### Evidence assessment

Evidence assessment owns the semantic judgment:

~~~text
criterion/claim
  <- observation refs (zero or more)
  + freshness
  + adequacy
  + standing
~~~

Zero observation refs is valid when the correct result is that required evidence
has not been observed.

### Current

Current is derived per target/realization scope from:

~~~text
accepted target
+ realized characterization
+ evidence assessments
~~~

Current may say, for example:

- unrealized;
- realized but unverified;
- realized and supported;
- contradicted;
- stale;
- observation error;
- evidence insufficient.

Those labels are candidate projections, not yet a frozen enum.

### Gap

Gap is derived:

~~~text
gap = variance(accepted target, qualified current)
~~~

The gap may additionally project active closing-plan refs, but a plan does not
own or close the gap.

## Why a generic authored relationship registry is unnecessary so far

Every required edge above has a natural owner.

Examples:

SC-17 -> REQ-4 is owned by SC-17.target_refs.

realization-unit-A -> capability-X is owned by the realization unit's
capability_refs.

test-file -> SC-17 is owned by the verification subject.

source-file imports package-Y is an observed realized relationship from the
characterization provider.

changing source-file may invalidate SC-17 evidence is a derived impact
relationship from source/dependency observations plus verification/evidence
bindings.

Authoring all of these again in a generic graph would create duplicate mutable
authority.

## Important distinction: intended, observed, derived

Dependency-like relationships must carry their semantic class.

~~~text
INTENDED
  accepted target/planning relation

OBSERVED
  analyzer/runtime/test observation

DERIVED
  impact, relevance, invalidation or navigation inference
~~~

These must never be collapsed merely because they use the same node identities.

Example:

~~~text
target:
  A must consume B

observed:
  A currently imports C

derived:
  target/realized dependency mismatch
  potential gap
~~~

## New correction: outcome should be first-class

The first candidate represented outcome inside an accepted_intent container.

The clean model does not need that container as a primitive.

It needs:

- one or more accepted outcomes;
- normative items;
- criteria;
- realization commitments.

accepted target is the semantic set of those accepted facts.

This avoids another storage/document wrapper becoming ontology.

## New correction: provider binding is semantically necessary

The prior candidate said provider selection was a planning output but did not
give the accepted provider choice a durable semantic home.

For a shareable AES distribution, that is insufficient. A user must be able to
tell which implementation/provider satisfies an AES capability and what AES still
owns locally.

Provider binding therefore survives the clean-sheet test, while provider-specific
interfaces and tooling remain deferred.

## Still not justified

The following still fail the necessity test:

- universal authored relationships file;
- universal code-symbol registry;
- mandatory semantic event stream;
- mandatory persistent generated source regions;
- system/component YAML files as ontology;
- one runtime/provider abstraction for every capability.

## Next model revision

The semantic candidate should:

1. replace accepted_intent with first-class outcome;
2. add provider binding;
3. keep accepted_target as a logical accepted-fact set, not a record type;
4. explicitly classify intended/observed/derived relationships;
5. keep record layout and provider API shapes deferred.
