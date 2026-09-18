# AC17 salvage for AES aligned normative/component planning

Status: research synthesis; non-normative donor analysis.

Date: 2026-09-17

## Why AC17 is relevant

AC17's central mechanism is an executable blueprint: specification + typed interfaces + pytest verification drive implementation, while the blueprint itself remains a claim subject to provenance, independent reading, mutation, hidden adjudication, and trace review.

This is directly relevant to the emerging AES idea that planning should jointly produce normative structure and implementation structure rather than authoring disconnected prose and code.

AC17 is not selected as an AES dependency or architecture. It is an empirical donor.

## High-value lessons

### 1. Blueprint alignment is real and useful

AC17 demonstrates a concrete version of:

```text
normative specification
      +
typed interfaces
      +
verification
      ↓
implementation
```

This supports the AES direction where Company Planning emits an aligned normative/component blueprint before implementation.

### 2. Component boundaries can be machine-readable and small

AC17's exercised `components.json` is intentionally compact:

- component ID;
- owned implementation artifacts;
- owned unit-test paths;
- assembly-owned artifacts.

This is very close to the minimum AES component manifest we have been discussing. AES would add semantic ownership, normative scope, typed boundary refs, and provider disposition rather than inventing a huge graph.

### 3. Do not project away normative context

AC17's decomposition research records a major failure in AC14: per-component spec projection deleted facts available in the whole-spec arm, so components implemented the wrong reading. AC17 deliberately changed the rule so every unit sees the complete specification and interfaces; scoping is by which implementation/tests the unit owns, not by hiding the rest of the specification.

AES implication:

- component-local context should improve locality;
- it must not become a lossy rewrite of system-wide or seam-level normative truth;
- inherited system norms and relevant neighboring/seam semantics should be included verbatim or directly addressable;
- generated component context must be completeness-checkable.

### 4. Cross-component interactions are first-class normative objects

AC17 found that individually correct clauses/tests did not guarantee correct behavior when clauses co-fired or had precedence/suppression relationships. It built explicit interaction manifests, joint witnesses, clause-effect IR, and mutation checks.

AES implication:

The normative model needs more than:

```text
requirement -> component
```

It also needs an economical representation for important cross-component or cross-requirement seams/interactions, especially:

- co-fire / simultaneous obligations;
- precedence;
- suppression;
- exclusivity;
- shared-state/effect interaction;
- ordering dependencies.

These should live at system/seam scope, not be duplicated into every component.

### 5. Semantic authority must remain explicit

AC17 had three unresolved interaction semantics that could not be inferred from implementations or references. They were resolved only by an explicit project-owner decision, and the independent references were treated as corroboration rather than specification authority.

AES implication:

Research, code, tests, external standards, and existing implementations can inform a normative decision but cannot silently become its authority. AQR -> research -> decision remains valuable.

### 6. Verification should challenge the blueprint, not merely execute it

AC17 treats the blueprint as a claim and checks it using:

- provenance;
- independent reading;
- mutation;
- hidden adjudication;
- full trace review;
- negative/fault-injection behavior.

AES implication:

Company Planning's output should itself have conformance/quality checks before implementation starts:

- every requirement owned;
- no duplicate/contradictory ownership;
- typed seams resolve;
- provider decisions match planned abstractions;
- important interactions represented;
- checks cover required behavior;
- no normative clause disappears in component projection.

### 7. Decomposition should be driven by semantic ownership, not by making things small

AC17's predecessor evidence found decomposition could increase failures and cost when it fragmented context without a real semantic reason.

AES implication:

Prefer fewer, larger, coherent components. Split only where there is a meaningful independent semantic/ownership/interface/verification boundary. Source symbols can remain fine-grained under a component without becoming separate planning objects.

## Proposed AES/Company Planning translation

AC17's blueprint can be generalized into an AES planning output:

```yaml
component:
  id: evidence_qualification
  responsibility: ...
  normative:
    requirements: [...]
    inherited_system_norms: [...]
    seam_obligations: [...]
  semantic_owner:
    kind: aes_local_residual
  provider_disposition: ...
  implementation:
    homes:
      - src/.../qualification.py
  interfaces:
    inputs: [...]
    outputs: [...]
  checks:
    - tests/.../test_qualification.py
```

The key difference from AC17 is that AES should avoid forcing every normative clause directly into each component record. System-wide and seam-level norms should remain separately authoritative and be inherited/addressed without duplication.

## Candidate planning-cycle change

A future AES planning profile or Company Planning extension should add an architecture-realization phase:

1. goal / north-star / PRD;
2. unresolved AQRs + research;
3. semantic ownership / provider sourcing;
4. requirements + important interaction semantics;
5. component boundaries;
6. typed seams;
7. implementation homes;
8. verification obligations;
9. blueprint validation;
10. work/slice decomposition;
11. implementation.

The implementation topology and normative topology are produced together.

## What not to carry forward

Do not adopt AC17 wholesale.

Do not assume:
- waterfall sequencing is universally right;
- all requirements can be frozen before observation;
- componentization itself improves outcomes;
- hidden adjudication is always available;
- every semantic interaction deserves a heavyweight manifest;
- every component needs an independent model session.

The transferable mechanism is aligned executable planning plus adversarial validation of the plan, not AC17's full experimental runtime.

## Current disposition

**Salvage as a strong conceptual and empirical donor.**

Most relevant mechanisms:
- executable blueprint;
- typed interfaces;
- compact component ownership manifest;
- complete normative context during decomposition;
- explicit interaction semantics;
- semantic-authority decisions;
- blueprint-as-claim verification.

These should inform the AES component/normative planning model before filesystem stubbing is frozen.
