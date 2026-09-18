---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills delegated high-confidence planning authority
date: 2026-09-17
reversible: true
resolves:
  - AQR-011
---

# Decision 0006 — Freeze the minimal AES architecture-realization contract on JSON Schema 2020-12

## Context

After resolving the normative-record taxonomy, component scope, symbol inheritance,
typing depth, and Company Planning profile boundary, AES needs one machine-readable
contract for the architecture-realization blueprint itself.

The contract must be strong enough to align normative responsibility with code
and verification, but must not become a second generic language for capabilities,
workflows, policy, provenance, APIs, contracts, or source symbols.

## Decision

### 1. Use YAML-compatible data validated by JSON Schema 2020-12

The canonical architecture-realization record is authored/serialized as
YAML-compatible structured data and validated against JSON Schema Draft 2020-12.

JSON Schema owns ordinary structural validation. AES adds only bounded residual
checks that are awkward to express in the schema itself, such as:

- unique component IDs;
- unique seam IDs;
- seam participants exist;
- component seam references exist.

### 2. The architecture-realization record owns only AES alignment semantics

The minimum contract contains:

- exact source references;
- explicit nonclaims;
- components;
- cross-component seams.

Each component contains:

- stable component identity;
- responsibility;
- normative references grouped as direct/inherited/seam;
- semantic-owner/provider realization mode;
- implementation home and realization state;
- consequential boundary state plus native contract references or blockers;
- verification home;
- verification obligation plus disproof;
- question references;
- decision references.

Each seam contains:

- stable seam identity;
- participants;
- normative references;
- resolved/unresolved state;
- obligation;
- blockers when unresolved.

### 3. Do not duplicate external semantic systems

This schema does not define:

- generic Capability or Requirement semantics;
- workflow/task semantics;
- generic policy language/evaluator;
- provenance/attestation semantics;
- API or payload schemas;
- code-symbol identity;
- operational software catalog semantics.

Those remain native or external authorities and are referenced/projected when useful.

### 4. Unresolved state is first-class

A component may reserve its filesystem/verification home before its semantic
boundary is frozen.

An unresolved semantic owner or boundary must name blockers/questions. Structural
completeness must never force an invented class, API, or provider binding.

### 5. Verification is part of target topology

Every component record names at least one verification obligation with a disproof
condition. The existence of the record or test home is not evidence that the
obligation passed.

### 6. Exact source identity and nonclaims are mandatory

Source revisions used as design inputs must be immutable identities.

Every architecture-realization record carries explicit nonclaims so a proposed
blueprint cannot be mistaken for accepted architecture, provider conformance,
runtime verification, gap closure, or stakeholder utility.

## Canonical bootstrap schema

- docs/architecture/schemas/architecture-realization.bootstrap.schema.json
- schema version: aes.architecture_realization.v0

The schema remains bootstrap-versioned. Breaking semantic changes require a new
schema version and an explicit decision rather than silent field drift.

## Evidence

- evidence/bootstrap-alignment/architecture-realization-schema-observation-001.json
- generated/bootstrap-normative/architecture-realization.minimal.pilot.yaml
- research/investigations/validate_architecture_realization_schema.py

The historical execution receipt records a passing Draft 2020-12 schema
validation using jsonschema 4.26.0 for the exact schema and pilot blobs named in
that receipt. Those exact blobs produced zero JSON-Schema errors and zero bounded
AES cross-reference errors; negative controls rejected unresolved records without
blockers, unknown fields, mutable source revisions, missing disproof, unsafe
paths, empty nonclaims, duplicate component IDs, and broken seam references.

The generated bootstrap probe was later revised only to remove resolved AQR-011
as a false component blocker. That revision does not retroactively change the
scope of the historical receipt. The current AES Company Planning profile records
the commands that must be rerun against the current probe before making a fresh
execution-conformance claim. Source-level coherence of that correction is
recorded in `evidence/bootstrap-alignment/current-profile-path-coherence-001.json`.

## Consequences

- AQR-011 is resolved for the current bootstrap.
- All architecture-alignment AQRs opened in AES-BOOTSTRAP-ALIGNMENT-001 now have
  explicit decisions.
- The large exploratory architecture-realization record can remain research
  history; future planning should target the minimal versioned contract.
- Company Planning's AES profile can produce/reference this record without
  changing the generic DesignPacketResult transport.
