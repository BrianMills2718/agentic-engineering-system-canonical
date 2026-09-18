# Normative/component alignment dogfood checkpoint

Status: **structured bootstrap checkpoint; non-authoritative except for cited accepted foundations**

Date: 2026-09-17

This checkpoint intentionally uses the model under discussion:

```text
accepted foundations
        +
current directions
        +
AQRs / unresolved questions
        +
research provenance
        ↓
next planning gate
```

The canonical machine-readable record is:

`docs/architecture/normative-component-alignment.bootstrap.yaml`

## Why this is dogfood

The record does **not** turn every discussion point into an ADR.

- Existing accepted AES decisions/clauses remain the accepted foundation.
- User-endorsed design ideas are recorded as `direction`, not silently promoted.
- Open architecture questions are explicit AQRs.
- Research records support directions/questions but do not become authority.
- The next filesystem/component freeze is blocked on the minimum questions that
  actually affect its correctness.

This directly exercises the intended future planning lifecycle: normative intent
and architecture questions are represented before implementation structure is
declared complete.

## Current strategic direction

The strongest current direction is that Company Planning (or an AES profile/fork
of it) should produce an **architecture-realization blueprint** in which normative
responsibility and implementation structure are co-designed.

The intended granularity is component-level by default:

```text
system/seam norms
       ↓
component normative scope
       ↓
typed boundary + implementation home + checks
       ↓
realized symbols (derived/inherited)
```

AC17 materially supports this direction but also warns against lossy component
context: every unit must retain complete applicable system/seam semantics.

## What is still deliberately not decided

The checkpoint leaves open:

- the minimal normative document taxonomy;
- the physical component/file layout;
- exact component vocabulary/profile mapping;
- symbol inheritance mechanics;
- system/seam inheritance representation;
- Company Planning upstream/profile/fork boundary;
- pre-implementation typing depth;
- component sizing rules;
- which prose views remain authored vs generated;
- migration of current canonical documents;
- the minimal architecture-blueprint schema;
- capability/requirement ↔ component cardinality semantics.

Those questions should be answered by the next bounded planning/research cycle,
not by empty filesystem stubs or convenience classes.
