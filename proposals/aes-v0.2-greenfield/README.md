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
accepted intent
    ↓
normative model
    ↓
AES planning
    ↓
planned repository + verification topology
    ↓
generated working/source context
    ↓
native implementation
    ↓
realized-source characterization
    ↓
evidence
    ↓
current
    ↓
gap
    ↓
next planning
```

Append-only engineering events record meaningful transitions and observations
without becoming mutable current-state authority.

## Proposal artifacts

- `01-design-thesis.md` — non-negotiable design principles and boundaries.
- `02-semantic-model.candidate.yaml` — candidate semantic information model.
- `03-lifecycle.candidate.yaml` — authored/generated/observed transformations.
- `04-greenfield-mvp.candidate.yaml` — first supported product scope and acceptance.
- `05-donor-reentry.md` — rule for evaluating prior mechanisms after the clean model exists.

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

The next gate is semantic review. Implementation/provider selection follows only
after the information model and lifecycle are accepted enough to test.
