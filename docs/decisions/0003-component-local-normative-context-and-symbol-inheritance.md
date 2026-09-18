---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills delegated high-confidence planning authority
date: 2026-09-17
reversible: true
resolves:
  - AQR-002
  - AQR-004
  - AQR-005
  - AQR-008
  - AQR-012
---

# Decision 0003 — Component-local normative context with inherited symbol scope

## Context

AES needs normative documentation and implementation structure to remain aligned without creating a manually maintained relationship edge from every requirement to every private function.

The first source-local dogfood used the real Repository Context component. It showed two things:

1. a generated, verbatim local projection can preserve exact normative wording and catch real drift; and
2. blindly injecting every repository-wide clause into every code location creates irrelevant context.

AC17 lineage evidence also shows that decomposition becomes harmful when it hides cross-component semantics or fragments context without a real semantic boundary.

## Decision

### 1. Component is the default governance boundary

A **component** is the smallest independently governed implementation boundary at which AES normally maintains:

- coherent responsibility;
- normative scope;
- implementation home;
- provider/semantic-owner disposition;
- consequential boundary information;
- verification obligation and disproof;
- current/gap linkage when realized.

The default physical shape is a component directory under the implementation root.

### 2. One implementation file is a preference, not a rule

Start with one implementation module when the responsibility is coherent and the file remains easy to reason about.

Do not split merely because conventional style favors many small modules/classes/functions, and do not force one-file components when distinct implementation concerns genuinely require multiple files.

The existing multi-file Repository Context implementation remains a valid component.

### 3. Normative wording is authored once

A normative clause has one owning source.

Component-local context may repeat the clause **verbatim only as a generated projection** with exact source identity. The local copy is never independently edited authority.

### 4. Local context uses explicit applicability, not blanket global injection

Source-local working context is layered:

- direct component norms;
- incident seam/context-delivery norms;
- outcome context where it helps explain the current vertical;
- condition-triggered norms only when their trigger applies;
- current plan acceptance obligations;
- current/gap state.

Repository-wide norms remain reachable but are not injected into every component merely because they exist.

### 5. Symbols inherit context, not conformance

Symbols inside a declared component inherit that component's applicable context for routing and comprehension.

This does **not** mean each symbol independently implements, verifies, or satisfies every component requirement.

Create explicit symbol-level links only when a symbol has:

- a narrower or additional normative obligation;
- a load-bearing acceptance criterion;
- an exception from component defaults;
- independent architectural significance;
- an independently meaningful verification boundary.

Realized symbol identities should use native language/source identity; SCIP remains an optional external candidate for cross-language indexing rather than a required AES symbol model.

### 6. Component decomposition follows semantics

Split a component when there is a meaningful independent difference in one or more of:

- semantic responsibility;
- authority/provider ownership;
- state ownership;
- public or consequential interface;
- replacement/reuse boundary;
- verification lifecycle;
- failure/recovery boundary.

Do not split on arbitrary line counts or function counts.

### 7. Capability/requirement mappings are many-to-many

Do not force one capability = one component or one requirement = one symbol.

Prefer one obvious component owner for a coherent normative concern when that is truthful, but allow:

- one capability to require multiple components;
- one component to support multiple capabilities/requirements;
- seam/system requirements to span components.

Every normative concern must still have an explicit owner, shared seam, or unresolved disposition.

## Physical bootstrap consequence

Reserved component directories may exist before behavior exists.

Until a boundary is resolved, a directory contains only a structural placeholder describing the planned home and blockers. It must not contain fake implementation APIs, passing placeholder tests, or skipped tests that resemble evidence.

## Evidence

- evidence/bootstrap-alignment/repository-context-source-local-observation-001.json
- evidence/bootstrap-alignment/reserved-component-tree-observation-001.json
- research/synthesis/2026-09-17-source-local-context-dogfood-result.md
- research/synthesis/2026-09-17-ac17-salvage-for-aligned-normative-component-planning.md

## Consequences

- AQR-002, AQR-004, AQR-005, AQR-008, and AQR-012 are resolved for the current bootstrap.
- The remaining architecture work does not need a per-symbol normative graph.
- The repository may expose its complete intended component structure before APIs are frozen.
- A future component schema should encode this decision without inventing a universal external Component ontology.
