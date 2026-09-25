# AES v0.2 Greenfield MVP — fresh review entrypoint

Status: **review snapshot / proposal / non-normative**
Date: 2026-09-24
Branch: `architecture/v0.2-greenfield`
Base lineage: `main@36c205d3363a7304c6043ca645acae5eea58e97c`

## Review question

Review the current candidate architecture as though prior AES mechanisms did not
have architectural privilege.

The decision is:

> **accept, revise, or reject the AES v0.2 Greenfield-MVP architecture strongly
> enough to authorize implementation planning/execution.**

This is not a request to approve code. No v0.2 product implementation is present
on this branch.

## Scope

AES v0.2 is an architecture/contract lineage.

The first supported delivery scope is **Greenfield MVP**:

- new projects governed by AES from inception;
- first supported repository/runtime ecosystem: candidate Python + Git;
- no arbitrary existing-project retrofit claim.

Retrofit remains a later capability.

## What not to assume

Do not assume AES v0.2 must inherit:

- `meta-process.yaml`;
- either historical `relationships.yaml`;
- Enforced Planning;
- Project Meta;
- Company Planning;
- ACA;
- Data Contracts;
- prior hook systems;
- generated source regions;
- an embedded LLM/provider API.

Prior systems are donors/provider candidates only.

## Recommended fresh-review reading order

Read these as the **current candidate**, not chronologically:

1. **`01-design-thesis.md`** — product thesis and non-negotiable invariants.
2. **`02-semantic-model.candidate.yaml`** — semantic kernel.
3. **`03-lifecycle.candidate.yaml`** and **`04-greenfield-mvp.candidate.yaml`** — lifecycle and product boundary.
4. **`15-planning-contract.candidate.yaml`** — how target design becomes accepted realization and then execution.
5. **`13-greenfield-materialization.candidate.md`**, **`14-initialization-contract.candidate.yaml`**, and **`16-record-shapes.candidate.yaml`** — candidate project storage/materialization.
6. **`20-realization-topology.candidate.yaml`** — exact proposed AES source/test topology and selected symbol commitments.
7. **`21-provider-bindings.candidate.yaml`** and **`22-portable-provider-boundaries.md`** — provider choices/rejections and portable planning/context boundaries.
8. **`10-greenfield-mvp-validation-profile.md`** and **`23-greenfield-cli-product-contract.md`** — falsifiable MVP proof and colleague-facing product flow.
9. **`06-open-questions.md`** — unresolved review decisions.

The numbered clean-sheet passes and detailed provider evaluations are supporting
rationale/evidence. They are not competing current architectures.

## Current candidate in one diagram

```text
accepted outcome + normative target
        ↓
qualified CURRENT + GAP
        ↓
AES planning request
        ↓
human/agent reasoning provider
        ↓
proposed realization + verification target delta
        ↓
AES validation + authorized acceptance
        ↓
accepted exact durable topology
        ↓
bounded subject working context
        ↓
native implementation
        ↓
Git + ecosystem characterization
        ↓
observations
        ↓
freshness + adequacy + standing
        ↓
qualified CURRENT
        ↓
GAP
        ↓
next plan / stop
```

## Semantic kernel under review

Current first-class semantics:

- outcome;
- normative item;
- success criterion;
- disproof and evidence requirements;
- failure mode as accepted engineering analysis;
- capability requirement;
- provider binding;
- realization unit;
- planned durable artifact;
- bounded artifact-generation rule;
- selected load-bearing symbol commitment;
- verification subject;
- time-bounded plan;
- realized-repository characterization;
- observation;
- evidence assessment;
- derived current;
- derived gap.

Not first-class authored authority by default:

- generic relationship graph;
- current;
- gap;
- wiki/review views;
- source-local context;
- reverse navigation;
- impact/relevance edges.

Those are derived projections unless a later requirement proves otherwise.

## Candidate project materialization

```text
.aes/
├── project.yaml                  operational AES adoption/config
├── target.yaml                   accepted target authority
├── analysis.yaml                 only when accepted non-target analysis exists
├── plans/PLAN-<id>.yaml          accepted time-bounded transitions
├── observations/<id>.yaml        retained observations
└── generated/                    rebuildable current/gap/graph/context/views
```

Native source, tests, contracts, manifests, migrations, and framework files stay
in ecosystem-native locations.

## Candidate implementation/provider boundary

Current candidate default:

```text
AES-local semantic core
+ Git
+ Python
+ Python stdlib ast
+ ruamel.yaml
+ Pydantic v2
```

JSON Schema 2020-12 is a candidate published structural contract format.

Not selected as required Greenfield runtime dependencies:

- Enforced Planning;
- Project Meta;
- Company Planning;
- ACA;
- Data Contracts.

Company Planning is a strong planning-method donor. Enforced Planning is a strong
mechanism donor. Neither controls v0.2 semantics.

## Exact realization proposal

The current topology proposal contains:

- 9 realization units;
- 18 exact source/test artifacts;
- 7 selected public/load-bearing symbol/signature commitments;
- criterion-linked verification subjects.

A proposal self-check across the Greenfield semantic instance and realization
topology found:

- 109 declared IDs;
- 125 typed references;
- 0 unresolved references;
- 0 duplicate IDs;
- 20 exact planned paths;
- 0 duplicate exact paths.

This is a consistency check only, not evidence that the architecture is correct.

## Product usability boundary

Core product use must work without private historical repositories.

Candidate command lifecycle:

```text
aes init
aes target validate
aes reconcile
aes plan prepare
aes plan validate <proposal>
aes plan accept <proposal>
aes check
aes characterize
aes context <subject>
aes observe ...
aes evidence assess
aes status
```

Planning intelligence is provider-neutral: AES emits a constrained request and
validates the returned proposal. A human or agent can be the reasoning provider.

`aes context <subject>` is sufficient as the first context-delivery boundary.
Automatic Claude/Codex/IDE injection is optional later automation.

## Load-bearing review questions

A fresh review should concentrate on these, not wording/style:

1. Is the semantic kernel minimal, or has AES still invented unnecessary concepts?
2. Is `realization unit` a justified boundary, and should the public term be
   `component`?
3. Is exact durable artifact topology too strong, too weak, or correctly scoped?
4. Is one `.aes/target.yaml` the right Greenfield MVP authority, or is it
   prematurely monolithic?
5. Does the planning transaction correctly separate proposed target change,
   accepted target, recomputed gap, and execution plan?
6. Is the evidence model—observation vs freshness/adequacy/standing—sufficient
   without becoming a policy language?
7. Is Python + Git an appropriate first supported ecosystem without leaking into
   AES-wide semantics?
8. Are the AES-local residuals actually AES-specific, or are we unnecessarily
   rebuilding mature generic providers?
9. Does the exact realization topology create meaningful engineering boundaries,
   or merely another file layout?
10. Is the Greenfield validation profile strong enough to falsify the product
    claim?
11. Are the provider rejections justified, especially Company Planning and
    Enforced Planning as non-default dependencies?
12. What must be decided before implementation versus deliberately learned by the
    first bounded implementation probe?

## Explicit nonclaims

This review snapshot does not:

- modify current v0.1 accepted architecture;
- supersede Decisions 0001–0009;
- change v0.1 Plan 002 state;
- authorize implementation;
- claim retrofit support;
- claim the provider versions are pinned/verified for distribution;
- claim a fresh consumer has passed the MVP;
- claim chronological supporting notes remain current if they disagree with the
  primary candidate files.

## Review outcome expected

The useful output of a fresh review is one of:

### Accept for implementation probing

The semantic/materialization/planning/provider/topology model is coherent enough
to authorize bounded implementation and falsification probes. Remaining issues are
implementation-resolvable rather than architecture blockers.

### Revise before implementation

Name the exact semantic/materialization/provider/topology defects that must be
changed before implementation.

### Reject/reframe

Identify which core assumption is wrong—for example exact topology, structured
target authority, projected context, or the target/current/gap lifecycle—and what
model should replace it.

Do not approve merely because the records are structurally consistent.
