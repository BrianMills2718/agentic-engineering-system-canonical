# AES v0.2 Greenfield MVP validation profile

Status: **candidate acceptance profile / non-normative**
Date: 2026-09-24

## Purpose

Prevent the Greenfield MVP from being "validated" by a project so trivial that it
does not exercise the architecture's load-bearing semantics.

The first authentic consumer project is not selected here. This file defines the
minimum phenomena that project must contain.

## Fresh-project requirement

The acceptance consumer must begin as a genuinely new repository/project created
under AES governance from inception.

It must not require:

- recovering undocumented pre-existing intent;
- classifying unexplained legacy files;
- migrating a pre-existing architecture;
- importing private historical AES machinery.

AES canonical itself may be used to develop the tooling, but its existing
repository cannot by itself establish the Greenfield-MVP product claim.

## Minimum semantic coverage

The consumer must contain enough real scope to exercise:

### Outcomes and obligations

- at least one concrete actor/consumer outcome;
- multiple normative items;
- at least one cross-cutting constraint or invariant;
- multiple success criteria;
- explicit disproof for each exercised criterion.

### Evidence diversity

At least:

- one deterministic executable proof;
- one non-identical proof mode such as human review, runtime observation, LLM
  rubric, contract validation, or external-consumer observation;
- one criterion requiring more than "some test passed" to establish sufficiency.

This tests the separation between observed result and evidence adequacy.

### Failure-mode planning

At least one material failure mode with explicit:

- threatened target;
- prevention or detection response;
- recovery or containment response where meaningful;
- criterion/evidence capable of showing the control is sensitive.

At least one negative or recovery control must prove that an important mechanism
can turn red or recover, not only pass on the happy path.

### Capability/provider separation

At least one required capability must be satisfied by a provider or external
dependency whose identity is distinct from the capability itself.

The accepted binding must state:

- what the provider supplies;
- what semantics remain owned locally;
- why the provider was selected;
- the replacement boundary.

This provider must be obtainable by an ordinary user of the supported
distribution.

### Realization topology

The project must contain:

- more than one durable implementation/verification artifact;
- at least one coherent realization-unit boundary;
- exact planned paths for knowable durable artifacts;
- at least one artifact that tests the generation-rule path if a natural
  tool-managed/generated durable artifact exists.

Do not manufacture a generated artifact solely to satisfy this bullet. If the
selected authentic project has no justified generation-rule family, validate the
rule separately without weakening the main consumer claim.

### Selected symbol commitment

At least one public/load-bearing native symbol must have an intentionally planned
identity and signature/type commitment.

Private helper symbols remain free implementation detail.

The realized characterizer must detect a deliberate mismatch in that commitment.

### Realized-repository characterization

At one exact revision AES must characterize enough of the realized repository to
answer mechanically:

- which planned durable artifacts exist;
- which planned durable artifacts are missing;
- whether an undeclared governed durable artifact exists;
- whether the selected planned symbol exists;
- whether its planned signature/type matches;
- which relevant dependency relationships were observed with their provenance or
  uncertainty.

### Current and gap

At least three distinct states must be exercised during the lifecycle:

1. target accepted, realization absent -> explicit unrealized current + open gap;
2. realization present, evidence incomplete -> current distinguishes implemented
   from adequately verified;
3. adequate evidence obtained -> gap can close only after fresh reconciliation.

At least one stale or invalidated-evidence transition must be exercised after a
material change.

### Projected context

The same real change is attempted under two conditions:

A. **projected-context condition**
- agent receives the bounded AES working context for the governed subject.

B. **control condition**
- agent receives the repository and ordinary entry documentation but not the
  AES subject projection.

The evaluation should compare, at minimum:

- unrelated files/documents read before correct action;
- context/tokens consumed before correct action where measurable;
- missed normative obligations;
- missed verification obligations;
- stale or false assumptions;
- topology violations;
- human corrections/rework.

The experiment does not need a universal benchmark claim. It must be strong
enough to tell whether projected context materially helps on the selected real
change.

## Deliberate falsifiers

The validation must intentionally introduce and detect at least:

1. an undeclared durable artifact;
2. a missing declared artifact or verification subject;
3. a selected symbol/signature/type drift;
4. stale evidence after a material subject/dependency change;
5. a criterion with a pass-like observation but insufficient required evidence.

If any of these can silently render green, the relevant MVP criterion fails.

## Distribution test

At least one run must be performed from the perspective of a user who has:

- the supported AES distribution;
- documented external dependencies;
- the fresh consumer repository;
- no dependency on Brian's private historical repositories;
- no hidden conversational context required to understand the project.

## What this profile does not prove

Passing this profile does not prove:

- retrofit of existing repositories;
- universal language/framework support;
- organization-scale portfolio governance;
- all possible evidence kinds;
- all possible providers;
- that every project should use the same repository topology.

It proves only the bounded Greenfield-MVP capability exercised by the authentic
consumer.
