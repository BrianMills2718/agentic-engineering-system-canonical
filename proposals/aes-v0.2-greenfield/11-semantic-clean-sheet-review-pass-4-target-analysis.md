# AES v0.2 semantic clean-sheet review — pass 4: target, analysis, transition, observation

Status: **proposal review / non-normative**
Date: 2026-09-24

## Problem

Several useful engineering facts participate in AES without all being the same
kind of truth.

If AES treats everything as "target," current/gap becomes incoherent. If it treats
everything as "documentation," authority becomes ambiguous.

## Four semantic roles

### 1. Accepted target

Accepted target answers:

> What should be true of the product/system and its accepted realization?

Candidate target facts include:

- outcomes;
- normative items;
- success/disproof criteria and evidence requirements;
- required capabilities once accepted;
- accepted provider bindings where materially architectural;
- accepted realization units;
- planned durable artifacts and generation rules;
- selected symbol/type/signature commitments;
- accepted verification topology.

These facts can participate directly in target-versus-current comparison.

### 2. Accepted engineering analysis

Accepted analysis answers:

> What do we currently believe matters when deciding how to realize or verify the
> target?

Examples:

- failure modes;
- provider landscape;
- feasibility findings;
- risk analysis;
- unresolved planning questions;
- dependency assumptions before they become accepted target commitments.

These may drive target changes or planning but are not automatically themselves
"should be true" claims.

Failure-mode example:

~~~text
analysis:
  credential leakage is a material failure mode

target response derived from analysis:
  secrets must never be committed

criterion:
  committed repository contains no secret material under the defined scan scope
~~~

Current/gap compares against the target response/criterion, not against the
existence of the failure-mode analysis.

### 3. Accepted transition

A plan answers:

> Given accepted target and qualified current/gap, what transition are we
> currently attempting?

A plan is temporally scoped.

It may:

- propose new target realization commitments;
- schedule verticals/probes;
- resolve planning uncertainty;
- select providers;
- define completion evidence for the transition.

Accepted durable target facts are promoted out of the plan into target authority.
Historical plans remain transition history.

### 4. Observation and derived state

Observation answers:

> What actually happened or exists at a bound subject/revision?

Evidence assessment answers:

> What are those observations entitled to support now?

Current answers:

> What is qualified as true now relative to the accepted target?

Gap answers:

> What variance remains?

## Consequence for failure modes

Failure mode remains first-class because planning should not lose defensive intent,
but its semantic class is **accepted analysis**.

Its response links can produce or justify:

- normative items;
- capability requirements;
- criteria/evidence requirements.

This avoids making risk analysis itself a conformance target.

## Consequence for provider research

A provider landscape or donor comparison is analysis.

A provider binding becomes accepted target only when the project accepts that
provider/composition as part of the intended realization.

This allows provider evidence to evolve without rewriting target until a decision
is accepted.

## Consequence for open questions

Open questions are important, but the Greenfield MVP does not yet need a universal
question registry.

Planning must be able to represent unresolved areas with:

- question/uncertainty;
- current known facts;
- what observation/decision resolves it;
- stopping rule;
- downstream target/plan update if resolved.

Whether those become a reusable top-level semantic type is deferred until the
planning model is exercised.

## Target-growth rule

Greenfield target grows in controlled stages:

~~~text
accepted outcome + obligations + criteria
        ↓
initial CURRENT = unrealized
        ↓
initial GAP
        ↓
planning/analysis
        ↓
accepted capability/provider/realization/verification commitments
        ↓
expanded accepted target
        ↓
rematerialized CURRENT + GAP
~~~

This is not a contradiction. The first target says what value/behavior must
exist; planning subsequently adds accepted realization commitments needed to
produce it.

## Anti-collapse rules

Do not collapse:

- failure mode into requirement;
- provider landscape into provider binding;
- plan into target;
- test result into evidence sufficiency;
- realized file into intended artifact;
- current into target;
- gap into plan;
- historical event into current.

Each transformation must be explicit enough to preserve why the fact changed
semantic class.

## Model correction

The semantic candidate should remove failure modes from the accepted-target set
while retaining them as first-class accepted analysis.

The lifecycle should show planning consuming accepted analysis without implying
that analysis itself is a target-current conformance subject.
