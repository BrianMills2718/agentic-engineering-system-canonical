# AES v0.2 design thesis

Status: **candidate design thesis / non-normative**

## 1. Product thesis

AES is a revision-bound engineering system that turns accepted intent into an
explicit planned realization, supplies the smallest authoritative working context
needed for engineering action, observes the realized system and its evidence, and
reconciles target versus current state into actionable gaps.

The repository should be a materialization of the accepted engineering model,
not an accidental accumulation of files produced during implementation.

## 2. Greenfield-first boundary

The first supported product scope is **new projects governed by AES from
inception**.

Retrofit of arbitrary existing repositories is a later capability. Greenfield
success is not evidence that AES can infer the intent, ownership, or rationale of
legacy repositories reliably.

## 3. Version lineage and capability maturity are different axes

- `AES v0.2` identifies the architecture/contract lineage.
- `Greenfield MVP` identifies the first supported implementation scope.
- `aes.adoption.retrofit` is a later capability, not another meaning of version.

A later capability becoming implemented does not by itself require a new
architecture version.

## 4. Normative intent is structured

Normative authority must be machine-addressable while remaining capable of
carrying full prose.

At minimum it can express:

- outcomes;
- requirements;
- constraints/invariants;
- success criteria;
- disproof criteria;
- failure modes;
- capability requirements;
- coherent realization-boundary responsibilities;
- consequential boundaries.

A success criterion is normative. A test, human review, LLM rubric, runtime
observation, or contract check is a verification subject capable of producing
evidence for that criterion. Passing one verification subject does not
automatically prove a criterion if the required evidence is broader.

## 5. Planning is an AES capability

AES owns the semantics of AES planning.

The planning capability derives, as appropriate:

- required capabilities;
- provider dispositions;
- failure-mode mitigations;
- components;
- dependencies;
- exact durable repository artifacts;
- selected public/load-bearing symbols;
- planned signatures/contracts where they are true commitments;
- verification subjects and their criterion mappings;
- execution-ready vertical slices.

Planning may use external providers, but AES's definition of a complete AES plan
must not depend on private historical knowledge.

## 6. Durable artifacts require semantic justification

Every durable governed artifact must either:

1. be declared by accepted planned topology, or
2. match an explicitly accepted generation/tooling rule.

A durable file boundary should represent a meaningful engineering boundary, not
merely a readability preference.

Ephemeral build/runtime artifacts are outside this invariant.

Renames are topology changes. Stable semantic subject identities may survive a
path rename, but the accepted target path changes explicitly.

## 7. Planned and realized source are distinct

Planned source facts are target commitments.

Realized source facts are observations of native implementation.

Do not manually copy realized facts into target records unless those facts are
intended commitments.

Examples:

- planned public signature: normative realization commitment;
- actual parsed signature: realized observation;
- private helper introduced during implementation: normally realized detail,
  unless planning explicitly governs it.

## 8. Native realization remains native authority

AES does not turn structured planning records into a general programming language.

Accepted target semantics may justify generation of repository artifacts or
working-context material, but the concrete generation mechanism is not part of
the clean-sheet semantic model.

Executable bodies remain native code. Native contracts, configuration, tests and
other realized repository artifacts remain authoritative for their own realized
bytes/behavior while never redefining normative target merely by existing.

## 9. Working context contains meaning, not only identifiers

Generated source-local context for a governed subject must contain the actual
applicable normative and success/disproof text, not merely IDs that require an
agent to perform another retrieval step.

IDs remain necessary for provenance, joins, impact analysis, and history.

Context should be the smallest complete concern-specific projection, not a raw
dump of the entire repository model.

## 10. Realized repository state becomes structured observation

AES should characterize the realized repository into revision-bound structured
observations containing enough information to compare target and realization.

For source code this may include symbols, signatures/types, docstrings and
dependencies. For other governed artifacts it may include contracts,
configuration, tests, generated artifacts, digests and other provider-specific
facts.

This characterization is observation/current substrate, never native executable
or normative authority.

## 11. Current and gap are derived

`CURRENT` is a qualified interpretation over revision-bound observations and
evidence.

`GAP` is the variance between accepted target and qualified current state.

Plans intend transitions. Plan completion does not establish gap closure.

Unknown, stale, missing, error, and insufficient-evidence states must not become
green.

## 12. Relationships should be derived where possible

Do not begin v0.2 with a universal authored `relationships.yaml`.

Relationships directly implied by canonical typed records or realized source
should be compiled into a semantic graph/projection.

Only relationships that cannot truthfully live in an owning record or be derived
should justify an additional authored relationship authority.

## 13. History must not become a second current-state authority

Git is the baseline source lineage. Durable decisions/plans preserve accepted
reasoning, and revision-bound observations/evidence preserve what was observed.

A separate append-only semantic event stream is a candidate only if Greenfield
MVP work demonstrates material lifecycle information that these existing
authorities cannot represent cleanly. If introduced, events remain historical
receipts and never become mutable current-state authority.

## 14. Failure modes are first-class planning input

AES should be able to represent:

```text
failure mode
    ↓
prevent | detect | contain | recover
    ↓
capability / requirement / control
    ↓
success or disproof criterion
    ↓
verification / evidence
```

This prevents defensive behavior from becoming undocumented incidental code.

## 15. Prior systems must earn re-entry

Existing mechanisms are donors/provider candidates only.

For every candidate:

```text
AES-required capability
        ↓
provider success criteria
        ↓
evaluate candidate
        ↓
reuse | adapt | compose | residual | reject
```

No mechanism is grandfathered into v0.2 because it existed in v0.1.

## 16. Distribution is architectural

A supported AES distribution must not require undocumented access to private
historical repositories.

The Greenfield MVP must have a coherent default configuration and documented,
obtainable dependencies.

## Candidate high-level invariants

1. One semantic fact has one mutable authority.
2. Generated projections are reproducible and identify provenance/freshness.
3. Every durable governed artifact has a declared semantic reason or generation rule.
4. Every success criterion states what evidence can establish it, and planning maps those requirements to concrete verification subjects before governed execution.
5. Selected planned public/load-bearing commitments can be compared mechanically to realized source.
6. Current state is revision-bound and invalidatable.
7. A stale/error/unobserved requirement cannot be represented as satisfied.
8. Plans do not close gaps; evidence-backed reconciliation does.
9. Agents receive full applicable normative meaning at the working surface.
10. Prior mechanisms have no implicit architectural authority.
11. Greenfield MVP makes no retrofit claim.
12. A user without access to private historical repositories can use the supported AES lifecycle.
