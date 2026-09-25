# AES v0.2 — clean-sheet Greenfield MVP proposal

Status: **proposal / non-normative**
Date: 2026-09-24
Branch: `architecture/v0.2-greenfield`
Lineage base: `main@36c205d3363a7304c6043ca645acae5eea58e97c`

## Purpose

Define the next AES architecture generation from first principles while preserving
the existing repository as empirical history.

`v0.2` is an **architecture/contract lineage identifier**. It does not mean
"second product milestone" and it does not imply retrofit support.

The first intended implementation scope is the **Greenfield MVP**: AES governs a
new project from inception. Retrofitting arbitrary existing repositories is a
later capability and is explicitly outside the first MVP.

## Clean-sheet rule

This proposal inherits **lessons and observations**, not implementation machinery.

Existing AES bootstrap mechanisms, Company Planning, Enforced Planning, Project
Meta, hook systems, Code Map, Representation Router, ACA, Data Contracts, and
other prior systems may later be evaluated as donors or provider candidates.
None is part of the v0.2 architecture merely because it already exists.

The design order is:

```text
observed engineering needs / failure modes
        ↓
required AES semantics
        ↓
required AES capabilities
        ↓
success + disproof criteria
        ↓
provider search / implementation choice
```

Do not reverse this into "existing mechanism -> AES requirement."

## Standalone product requirement

A colleague must be able to obtain AES, configure a new project, and use the
supported AES lifecycle without access to Brian's private historical repositories
or undocumented knowledge of how AES evolved.

"Standalone" does not mean "dependency-free." It means all required dependencies
are explicit, obtainable, documented, and replaceable where appropriate.

## Core architectural hypothesis

```text
accepted outcome + normative target
    ↓
qualified current + gap
    ↓
AES planning
    ↓
accepted realization + verification topology
    ↓
bounded working context
    ↓
native implementation
    ↓
realized-repository characterization
    ↓
observations + evidence assessment
    ↓
qualified current
    ↓
gap
    ↓
next planning
```

Git is the baseline source lineage. A separate append-only semantic event layer
is deferred until Greenfield-MVP work demonstrates lifecycle information that
Git plus accepted authorities plus revision-bound observations/evidence cannot
represent cleanly.

## Fresh review

Start with **`REVIEW.md`**. It defines the review question, current candidate
reading order, artifact status, and decisions still open. Do not reconstruct the
architecture chronologically from the numbered files.

## Proposal artifacts

- `01-design-thesis.md` — candidate product thesis and invariants.
- `02-semantic-model.candidate.yaml` — current clean-sheet semantic kernel.
- `03-lifecycle.candidate.yaml` — current Greenfield lifecycle/state classes.
- `04-greenfield-mvp.candidate.yaml` — product boundary and minimum acceptance.
- `05-donor-reentry.md` — prior mechanisms must earn provider re-entry.
- `06-open-questions.md` — unresolved questions after semantic review.
- `07-semantic-clean-sheet-review-pass-1.md` — removes storage-layout, evidence-state and event-log conflation.
- `08-semantic-clean-sheet-review-pass-2.md` — defines natural semantic refs and derived relationship graph.
- `09-semantic-clean-sheet-review-pass-3-topology.md` — exact durable paths, bounded generation rules and no-orphan topology.
- `10-greenfield-mvp-validation-profile.md` — authentic consumer/falsifier profile.
- `11-semantic-clean-sheet-review-pass-4-target-analysis.md` — separates target, engineering analysis, transition and observation.
- `12-greenfield-mvp-semantic-instance.candidate.yaml` — models the real Greenfield MVP with the kernel; current reference check: zero missing refs/duplicate IDs.
- `13-greenfield-materialization.candidate.md` — candidate .aes structured project materialization.
- `14-initialization-contract.candidate.yaml` — minimal bootstrap contract for a fresh project.
- `15-planning-contract.candidate.yaml` — design-delta → accepted target → recomputed gap → execution-plan contract.
- `16-record-shapes.candidate.yaml` — candidate project/target/analysis/plan/observation/generated record shapes.
- `17-provider-evaluation-contract.candidate.yaml` — capability-first gate every old or external provider must pass.
- `18-internal-provider-evaluation.candidate.yaml` — detailed internal-donor evidence; supporting, not controlling.
- `18-provider-evaluation-round-1.md` — synthesized internal-provider rationale; supporting.
- `19-public-native-provider-evaluation.candidate.yaml` — detailed public/native provider evidence; supporting.
- `19-provider-evaluation-round-2-generic-dependencies.md` — synthesized generic-dependency rationale; supporting.
- `20-realization-topology.candidate.yaml` — exact candidate source/test topology and selected symbol commitments.
- `21-provider-bindings.candidate.yaml` — explicit candidate bindings and rejected default providers.
- `22-portable-provider-boundaries.md` — provider-neutral planning exchange and explicit context CLI boundary.
- `23-greenfield-cli-product-contract.md` — colleague-facing Greenfield lifecycle/command surface.

## Nonclaims

This proposal does **not**:

- change current AES accepted architecture;
- supersede Decisions 0001–0009 yet;
- authorize implementation;
- select Company Planning, Enforced Planning, Project Meta, or any other prior system;
- select a relationship-registry format;
- select a hook/enforcement implementation;
- claim retrofit support;
- claim the candidate YAML shapes are final schemas.

The next gate is a **fresh pre-implementation architecture review** of the
current candidate snapshot. Provider evaluation has already been performed at
proposal level; no implementation/provider binding is accepted yet.
