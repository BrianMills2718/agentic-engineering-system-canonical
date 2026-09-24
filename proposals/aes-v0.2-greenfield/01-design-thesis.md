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
- component responsibilities;
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

## 8. Native code remains executable authority

AES does not turn YAML into a general programming language.

Structured target records may generate:

- initial source skeletons;
- persistent governed source regions;
- selected public/load-bearing signatures when intentionally frozen;
- source-local normative/context blocks.

Executable bodies remain native code.

## 9. Working context contains meaning, not only identifiers

Generated source-local context for a governed subject must contain the actual
applicable normative and success/disproof text, not merely IDs that require an
agent to perform another retrieval step.

IDs remain necessary for provenance, joins, impact analysis, and history.

Context should be the smallest complete concern-specific projection, not a raw
dump of the entire repository model.

## 10. Realized source becomes structured current evidence

AES should characterize native source into a generated structured projection
containing enough information to compare target and realization, such as:

- exact repository revision;
- file identities and content digests;
- symbols;
- signatures/types;
- docstrings;
- dependencies with provenance/confidence where necessary;
- generated-region status;
- verification associations.

This projection is observation/current substrate, never executable authority.

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

## 13. Append-only history is not current authority

Meaningful engineering events may record:

- accepted normative changes;
- accepted topology changes;
- decisions and supersession;
- implementation observations;
- verification observations;
- evidence invalidation;
- human/model dispositions;
- generated projections.

Events are append-only semantic receipts. Current state is materialized from
authorities and valid observations; events are not edited to represent current.

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
4. Every success criterion has an explicit verification disposition.
5. Selected planned public/load-bearing commitments can be compared mechanically to realized source.
6. Current state is revision-bound and invalidatable.
7. A stale/error/unobserved requirement cannot be represented as satisfied.
8. Plans do not close gaps; evidence-backed reconciliation does.
9. Agents receive full applicable normative meaning at the working surface.
10. Prior mechanisms have no implicit architectural authority.
11. Greenfield MVP makes no retrofit claim.
12. A user without access to private historical repositories can use the supported AES lifecycle.
