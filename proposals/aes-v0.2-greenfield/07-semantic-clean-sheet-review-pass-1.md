# AES v0.2 semantic clean-sheet review — pass 1

Review role: **historical/supporting rationale**. Its accepted corrections are incorporated into `02-semantic-model.candidate.yaml` and `03-lifecycle.candidate.yaml`.

Status: **proposal review / non-normative**
Date: 2026-09-24

## Review rule

For every proposed primitive, ask:

> If AES v0.1 and every prior implementation mechanism had never existed, would
> the Greenfield MVP still need this concept to state its target, plan a
> realization, execute it, establish current state, derive gaps, and project
> useful working context?

A useful idea from prior work is not sufficient. The concept must have an
independent semantic job.

## Findings

### 1. Record layout is not ontology

The first candidate model treated `system` and `component` records as
fundamental normative families.

That is premature.

AES needs semantic facts such as outcomes, obligations, criteria, capabilities,
planned realization boundaries, artifacts, and verification. Whether those facts
are stored in one YAML file, a system file plus component files, a database, or
another representation is a **materialization decision**.

v0.2 therefore separates:

```text
semantic model
        ≠
record/file layout
```

A later Greenfield-MVP planning pass may deliberately choose a system/component
file layout, but the ontology must not presuppose it.

### 2. Success criteria should not be owned by exactly one requirement

The first candidate nested success criteria conceptually under requirements.

That is unnecessarily restrictive. One criterion may establish several
cross-cutting obligations, while one obligation may require several criteria.

The cleaner shape is many-to-many:

```text
normative item(s)
      ↕
success criterion
      ↕
verification subject(s)
```

A criterion therefore names the target items it can establish rather than being
structurally owned by one requirement.

### 3. PASS/FAIL are not epistemic states

The first candidate mixed:

```text
PASS / FAIL
```

with:

```text
UNOBSERVED / ERROR / STALE / INSUFFICIENT
```

These answer different questions.

A clean model distinguishes at least:

- **observation/execution state** — did an observation run successfully?
- **observed result** — what happened? pass/fail/value/judgment/etc.
- **freshness** — is the observation still applicable to the claimed subject?
- **adequacy** — is the available evidence sufficient for the criterion?
- **standing** — does the qualified evidence support, contradict, or leave the
  criterion unresolved?

This prevents "test PASS" from being confused with "criterion satisfied."

### 4. Realized source is one realized-repository observation, not the whole current model

The first candidate used `realized_source_projection` as a major primitive.
That is too source-centric.

The Greenfield MVP governs durable repository realization, which may include:

- native source;
- tests;
- configuration;
- contracts;
- generated artifacts;
- migrations;
- other planned durable artifacts.

The more general semantic concept is a **realized-repository characterization**.
Language/source analyzers are providers that contribute observations to it.

### 5. Component is useful, but its clean-sheet semantic name is not settled

AES needs some coherent planned realization boundary because responsibility,
ownership, verification, replacement, and context projection cannot attach only
to individual files.

However, `component` is a label inherited from common software architecture and
earlier AES work. The semantic need is:

> a coherent realization unit/boundary that groups responsibility and governed
> subjects.

The proposal will temporarily call this a **realization unit** and leave
`component` as the likely conventional label.

This also prevents "component.yaml" from being assumed before planning decides
repository materialization.

### 6. Planned symbols are subordinate commitments, not a universal top-level inventory

AES needs to plan selected public/load-bearing symbols when their existence,
signature, type, narrower obligation, or verification boundary is genuinely part
of the accepted target.

AES does not need a universal planned-symbol registry.

Planned symbol commitments therefore belong to planned realization/artifact
topology and remain intentionally sparse.

### 7. A universal relationship authority is not justified

The clean model already produces relationships through typed references:

```text
criterion -> normative items
capability -> target items
realization unit -> capabilities
artifact -> realization unit / target items
verification subject -> criteria
observation -> subjects
evidence assessment -> observations + criteria
plan -> gaps + proposed target changes
```

Realized characterization adds observed dependency relationships.

A semantic graph can be compiled from these facts.

No separately authored universal relationship registry is justified yet.

### 8. Engineering events are not yet a Greenfield-MVP primitive

Git already preserves source history. Durable decisions/plans preserve important
accepted reasoning. Revision-bound observations/evidence preserve what happened.

An additional append-only semantic event stream may eventually add value, but
the clean-sheet model should not require it until we identify information that:

1. matters to AES semantics;
2. is not adequately represented by Git + authorities + observations/evidence;
3. benefits from append-only event semantics.

The event layer is therefore demoted to a candidate later capability.

### 9. Persistent generated source regions are a mechanism choice, not a semantic primitive

The semantic requirement is:

> the working context at a governed subject contains the complete applicable
> normative/success/disproof meaning with provenance, and drift from accepted
> commitments is detectable.

Persistent generated docstrings, headers, signatures, sidecars, IDE injection,
or another mechanism can satisfy this.

v0.2 should retain the requirement while deferring the mechanism.

### 10. Exact durable topology remains justified

Unlike the rejected implementation-derived concepts above, exact durable
repository topology survives the clean-sheet test.

Without it AES cannot strongly enforce:

- why a file exists;
- which target it realizes;
- which verification exists for which criterion;
- whether a durable artifact is orphaned;
- whether a path change is an architectural change;
- whether realized repository structure conforms to accepted planning.

Generation/tooling rules remain an allowed alternative when an exact path cannot
or should not be enumerated individually.

## Revised essential semantic set

The first-pass minimum is now:

```text
accepted intent / outcome

normative item
    requirement | constraint | invariant | quality/policy obligation as needed

success criterion
    + disproof
    + links to normative items

failure mode
    + threatened targets
    + prevent/detect/contain/recover responses

capability requirement

realization unit
    likely surfaced as "component", label not yet frozen

planned durable artifact
    exact path OR accepted generation rule

selected planned symbol commitment
    subordinate, sparse, only when load-bearing

verification subject
    criterion-linked planned proof mechanism

plan
    time-bounded intended transition

realized repository characterization
    revision-bound generated observation

observation
    what was actually observed

evidence assessment
    freshness + adequacy + standing for criterion/claim

current
    derived qualified state

gap
    derived target/current variance
```

## Derived, not separately authored by default

```text
semantic relationship graph
source-local / task-local context
wiki / OKF
requirements view
architecture view
component/realization map
verification view
current view
gap view
review surface
```

## Deferred mechanisms / candidates

- concrete YAML record/file partition;
- JSON Schema shape;
- universal relationship registry;
- append-only engineering event stream;
- persistent generated source regions;
- hook implementation;
- provider interfaces;
- source analyzer choice;
- execution-governance implementation;
- retrofit adoption.

## Consequence for the next pass

The semantic model should now be rewritten around the revised essential set
before any provider comparison.

The next hard questions are no longer "should we reuse the old component schema?"
or "which relationships file wins?" They are:

1. what exact references connect the essential semantic types;
2. what is authored versus planned versus observed versus derived;
3. what is the minimum evidence-adequacy model;
4. what makes a realization unit coherent;
5. which exact topology commitments are required for Greenfield MVP;
6. what minimum project configuration is necessary to materialize the model.
