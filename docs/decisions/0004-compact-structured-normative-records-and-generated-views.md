---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills delegated high-confidence planning authority
date: 2026-09-17
reversible: true
resolves:
  - AQR-001
  - AQR-009
  - AQR-010
---

# Decision 0004 — Compact structured normative records with generated conventional views

## Context

AES needs goals, product intent, requirements, user journeys, architecture,
questions, decisions, plans, and code to remain aligned without creating a
separately authored document for every conventional artifact type.

A dogfood projection of existing authoritative AES Markdown represented a north
star, product outcome, user journey, system requirements, component reference,
and open AQRs in one structured system record. From that one projection AES
generated PRD-style, user-journey, requirements, architecture/component, and
AQR views without separately authoring normative wording.

The pilot also rejected duplicated IDs, paraphrased normative text, current
state promoted into normative target, native contracts copied into YAML, false
authority claims, and a resolved AQR without a decision reference.

## Decision

### 1. Canonical authored taxonomy stays small

AES uses two primary structured normative record families:

1. **System record** — system/product-level intent and cross-component norms.
2. **Component record** — component-scoped normative realization and code/check
   alignment.

Do not create a mandatory file family for every conventional document label.

### 2. System record content

The system record may contain, as applicable:

- north star;
- goals;
- actors/stakeholders;
- product outcomes;
- journeys/scenarios;
- system requirements, constraints and invariants;
- cross-component seam obligations;
- open AQRs;
- decision references;
- component references.

Sections are optional except for stable identity and at least one normative
requirement/obligation appropriate to the governed system.

A PRD is therefore normally a **view** over north-star/goals/actors/outcomes/
journeys/requirements rather than an independent editable authority.

### 3. Component record content

One component record owns or references:

- component identity and responsibility;
- direct normative requirements;
- inherited applicable system requirements;
- seam obligations;
- component scenarios/examples where useful;
- open AQRs and decision references;
- semantic-owner/provider disposition;
- native contract/boundary references;
- implementation home;
- verification home, obligations and disproof;
- current plan references when applicable.

Native typed contracts remain native authorities and are referenced rather than
redefined in the normative record.

### 4. Conventional documents are generated views by default

PRD, requirements, user-journey, architecture, component-map, AQR, decision-log,
wiki, and source-local-context surfaces are generated/materialized views when
useful to a human or agent.

Their absence is not missing normative information if the canonical structured
records contain the necessary semantics and remain addressable.

A separate independently authored prose authority requires an explicit reason
and authority boundary.

### 5. Distinct lifecycle records remain distinct

Research, durable decisions, change plans, and evidence retain their current
separate native lifecycles because they are not the same kind of truth:

- research informs normative change but is not normative;
- ADR/decision records capture accepted choice, rationale and supersession;
- plans are time-bounded change authority, not timeless target;
- evidence is observed history/current support, not desired behavior.

AQRs are lightweight scoped records inside the system/component record by
default. Split an AQR into a separate record only when its research/discussion
lifecycle materially warrants it.

### 6. Migration is single-authority cutover, not synchronization

Existing accepted Markdown remains authoritative until a separately accepted
migration.

During migration, generated structured projections may be used for dogfood, but
they do not become a second editable truth.

A future cutover must:

- preserve stable IDs;
- preserve wording verbatim unless an accepted normative revision changes it;
- verify required generated views/navigation;
- switch the owning authority atomically;
- retire the previous location as editable authority.

Do not maintain the same normative wording manually in both Markdown and YAML.

### 7. Human prose remains possible

Structured authority does not forbid prose. Long rationale, examples or
explanation may be fields/blocks in the owning record or a referenced decision/
research source.

The rule is one semantic authority, not "everything must be terse YAML."

## Evidence

- evidence/bootstrap-alignment/normative-record-view-dogfood-001.json
- generated/bootstrap-normative/system.pilot.yaml
- generated/bootstrap-normative/view-bundle.md
- docs/architecture/normative-record-model.bootstrap.yaml
- research/synthesis/2026-09-17-external-document-semantics-for-normative-model.md

## Consequences

- AQR-001, AQR-009 and AQR-010 are resolved for the current bootstrap.
- Documentation growth is driven by semantic/lifecycle need, not conventional
  document names.
- Company Planning can target system/component records while rendering familiar
  views for review.
- AQR-011 remains open: the exact machine schema for the architecture-realization
  blueprint still needs to be minimized and frozen from the now-accepted record
  decisions.
