# Candidate structured engineering model

Status: **proposal / non-binding**

Date: 2026-09-24

Source synthesis:
`research/synthesis/2026-09-24-planning-derived-source-and-realized-characterization.md`

## Purpose

This proposal turns the approved research synthesis into concrete candidate YAML record
types that can be validated and dogfooded before any normative-authority cutover.

It deliberately separates four concerns:

1. `system-record.v0` — authored system-level normative target.
2. `component-record.v0` — authored component target plus exact planned repository/source
   topology and verification subjects.
3. `realized-source-projection.v0` — generated revision-bound characterization of native
   source.
4. `engineering-event.v0` — append-only semantic event/receipt referencing authoritative
   payloads.

The schemas are structural probes, not accepted AES contracts.

## Candidate authority model

```text
AUTHORED TARGET AUTHORITY
  system record
      ↓
  component record
      ↓
  exact planned files / public symbols / verification subjects
      ↓
  persistent generated source regions + native implementation
      ↓
GENERATED REALIZED SOURCE PROJECTION
      ↓
current characterization
      ↓
gap

APPEND-ONLY ENGINEERING EVENTS
  record accepted changes / observations / invalidations / dispositions
  without becoming a second mutable authority.
```

## Key choices encoded in the candidate schemas

### Success criteria are normative

`system-record.v0` and component-local requirements place success criteria and disproof
inside the normative requirement structure. A criterion declares its required proof kind
and exact proof statement.

### Exact durable paths are first-class

`component-record.v0` requires exact paths for implementation subjects and for file-backed
verification subjects. A subject also declares why it exists and which requirements it
realizes or criteria it verifies.

This is intended to support a future invariant that no durable governed artifact is
semantically orphaned.

### Public symbol skeletons are planning data

A planned implementation subject may declare public symbols with:

- native symbol name;
- symbol kind;
- native-language signature declaration;
- purpose;
- normative/criterion applicability;
- mandatory verbatim-context projection.

The candidate schema does not model executable bodies.

### Persistent generated regions are explicit

A planned implementation subject can declare generated regions with:

- `persistent_generated` or `initial_skeleton_only`;
- placement such as file header, symbol docstring, signature, or declaration block;
- content refs;
- whether verbatim source text is required.

The current candidate assumes `verbatim_required: true` for normative source-local
regions.

### Realized source remains native authority

`realized-source-projection.v0` is generated observation. It records actual:

- files and content digests;
- native symbol IDs;
- qualified names;
- signatures;
- docstrings;
- dependency edges;
- generated-region freshness/state.

It is not editable implementation authority.

### Failure modes are linked to capabilities and criteria

System records can state failure modes and classify responses as:

- `prevent`;
- `detect`;
- `contain`;
- `recover`.

Each response links to capabilities, requirements, or success criteria.

### Append-only semantic history is separate from current projections

`engineering-event.v0` records event identity, event kind, exact source revision,
subject refs, payload refs/digests, and a concise summary.

It does not copy the full mutable target/current payload. Current/gap/wiki/source-local
views should be regenerated from authorities plus observations/events.

## Structural validation versus semantic validation

JSON Schema can prove record shape. It cannot establish the most important cross-record
invariants.

A future semantic validator should additionally reject at least:

1. duplicate IDs across the governed target;
2. unresolved requirement/capability/failure-mode/component references;
3. a component subject that realizes no resolvable normative requirement;
4. a verification subject whose criterion ID does not resolve;
5. a success criterion with no verification disposition;
6. a durable planned file with no semantic purpose;
7. an observed durable file outside accepted topology or an explicit generation/tool rule;
8. a generated region whose rendered text differs from authoritative text when
   `verbatim_required: true`;
9. a planned public symbol missing from realized source;
10. a normative signature commitment whose realized native signature differs;
11. a current projection built from stale/error/unobserved evidence but rendered as current;
12. relationship/current/gap views whose source revisions do not match their declared
    authority/evidence inputs.

## Candidate files

```text
schemas/
  system-record.v0.schema.json
  component-record.v0.schema.json
  realized-source-projection.v0.schema.json
  engineering-event.v0.schema.json

examples/
  system.candidate.yaml
  component.candidate.yaml
  realized-source.candidate.yaml
  engineering-event.candidate.yaml
```

All four examples validate structurally against their candidate JSON Schema 2020-12
contracts in the proposal authoring check.

## Open questions intentionally not frozen

- exact split between system-owned and component-owned normative requirements;
- which public/private symbols deserve planned identity;
- which signatures remain permanently generated;
- safe generated-region mechanics for each language;
- realized-source provider choice: native AST/LSP, SCIP, or composition;
- dependency-context depth/relevance;
- semantic event schema beyond the minimum receipt fields;
- whether verification subjects need a separate top-level record family;
- how human-review and LLM-rubric verification subjects should bind to durable review
  artifacts;
- how generator/tool rules for durable output families should be represented;
- how the target repository topology should be compiled into hard pre-commit/Stop hooks.

## Dogfood gate

Do not adopt these schemas from structural validity alone.

The next useful test is one bounded `repository_context` change in which AES:

1. authors target system/component candidate records;
2. generates at least one persistent source-local region containing full verbatim
   requirement and criterion text;
3. makes one native implementation change;
4. characterizes the realized source back into the realized-source projection;
5. detects one intentional target/realized drift;
6. executes criterion-appropriate verification;
7. writes append-only semantic receipts;
8. rematerializes current/gap and source-local/wiki projections;
9. measures whether a fresh agent can act correctly without reconstructing the repo.

Only that outcome should decide which parts move from proposal into accepted architecture.
