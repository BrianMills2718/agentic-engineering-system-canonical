---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills delegated high-confidence planning authority
date: 2026-09-17
reversible: true
resolves:
  - AQR-003
  - AQR-007
---

# Decision 0005 — AES Component is a governance scope; type only consequential seams early

## Context

AES needs a stable planning unit that aligns normative responsibility with code,
but external systems already use overlapping terms:

- Backstage uses Component for a cataloged unit of software and APIs/resources around it;
- TOSCA models nodes, capabilities, requirements, relationships and interfaces;
- SysML uses richer structural/behavioral/requirement concepts.

None is exactly the AES planning need: the smallest implementation boundary at
which normative scope, provider ownership, code home and verification should be
reasoned about together.

AES also needs design-before-code strong typing without pre-designing every
private helper or freezing provider-specific APIs before provider selection.

## Decision

### 1. Component is an AES planning/governance concept

Within AES architecture-realization records, Component means the governed
implementation boundary defined in Decision 0003.

It is not a universal runtime class and does not assert semantic equivalence to
Backstage Component, TOSCA Node/Capability, SysML Part, a deployable service, a
Python package, or a process boundary.

Use an explicit adapter/projection when an AES component needs to appear in one
of those external models.

### 2. Do not create an AES universal component ontology

The AES component record owns only AES-specific planning/governance information:

- responsibility and normative scope;
- semantic-owner/provider disposition;
- implementation home;
- consequential boundary references;
- verification obligation;
- questions/decisions/plans that govern realization.

Runtime topology, catalog metadata, capability semantics, APIs and source-symbol
identity stay with their natural authorities.

### 3. Freeze typing before implementation only where it prevents an unstated decision

Before independent implementation begins, freeze a typed seam when one or more
of these is true:

- it crosses component/provider/repository/process boundaries;
- independently implemented parties must agree on it;
- it carries persistent or externally visible state;
- failure/error/epistemic semantics can change correctness;
- compatibility or migration depends on it;
- it is a consequential public/actor boundary;
- verification requires a stable producer/consumer contract.

The frozen seam should make recoverable, as applicable:

- semantic input/output meaning;
- identity/version;
- required versus optional fields or states;
- failure/error/unknown semantics;
- authority/ownership;
- compatibility expectations;
- acceptance/disproof at the boundary.

### 4. Do not pre-freeze internal implementation detail

Planning does not need to freeze:

- private helper functions;
- every internal class;
- incidental module splits;
- local data structures with no cross-boundary meaning;
- provider-specific API shapes before the provider is selected;
- speculative interfaces for later slices.

Those become normal implementation symbols inside the governed component.

### 5. Unknown seams stay explicitly unresolved

If a consequential seam is known to matter but its correct shape is not yet
knowable, planning records:

- the boundary;
- the unresolved question/AQR;
- the discriminating probe or decision needed;
- the implementation work blocked by the uncertainty.

It does not invent a type merely to make the blueprint structurally complete.

## External mapping rule

External models may be used where they fit:

- Backstage for operational software catalog projection;
- TOSCA for generic capability/requirement/topology projection;
- SysML v2/KerML for richer systems-engineering traceability when justified;
- native API/schema standards for actual interfaces.

An external mapping is evidence about another concern. It does not redefine the
AES Component record.

## Evidence

- Decision 0003 component-local normative-context dogfood
- docs/architecture/aes-company-planning-profile.bootstrap.yaml
- evidence/bootstrap-alignment/company-planning-profile-conformance-001.json
- research/synthesis/2026-09-17-aes-semantic-ownership-crosswalk.md
- research/investigations/2026-09-17-backstage-tosca-sysml-topology-fit.md

## Consequences

- AQR-003 and AQR-007 are resolved for the current bootstrap.
- Component directories can be laid out without implying microservices or
  deployment boundaries.
- Strong typing remains an architectural tool at meaningful seams rather than a
  requirement to predeclare every symbol.
- At the time of this decision, the remaining open bootstrap AQR was the
  minimal machine-readable architecture-realization schema. Decision 0006
  subsequently resolved that question; unresolved component/provider/boundary
  questions must now come from real component design rather than reopening the
  bootstrap schema question.
