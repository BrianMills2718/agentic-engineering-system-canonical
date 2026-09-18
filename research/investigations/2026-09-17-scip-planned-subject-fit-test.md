# Fit test — SCIP symbol identity vs AES planned implementation subjects

Status: discriminating probe
Date: 2026-09-17

## Purpose

Determine whether AES should define its own universal code-symbol vocabulary for functions/classes/modules, or reuse SCIP for realized code identity while retaining only the planning semantics SCIP cannot represent.

External sources:
- https://github.com/scip-code/scip
- https://github.com/scip-code/scip/blob/main/docs/scip.md

## SCIP semantics observed

SCIP is a language-agnostic code intelligence protocol built around a Protobuf schema. It models:

- documents and source-relative paths;
- occurrences at exact source ranges;
- standardized symbol identities;
- package identity (`manager`, `name`, `version`);
- descriptors for namespace, type, term, method, type parameter, parameter, macro and local/meta symbols;
- symbol kind metadata;
- signatures/documentation;
- relationships such as implementation/reference relationships;
- diagnostics;
- definitions/references/implementations for navigation.

SCIP symbols have a standardized fully-qualified string representation and are intended to uniquely identify realized language symbols within a package.

## AES planned implementation subject semantics

An AES planned implementation subject exists before code necessarily exists. It identifies a concrete realization target derived from accepted architecture/planning, for example:

- future module/file;
- future class/model;
- future resolver/service;
- future adapter/provider boundary;
- future function/method;
- future CLI/API boundary;
- occasionally a broader implementation boundary that will realize as several code symbols.

A planned subject therefore needs lifecycle states such as planned/stubbed/implemented/observed/verified and links to target clauses, plans, gaps and verification subjects.

## Mapping

| Concern | SCIP | AES planned subject |
| --- | --- | --- |
| existing class/function/method identity | strong | should reference SCIP when available |
| source range / occurrence | strong | not a planning concern |
| definitions/references/implementations | strong | consume rather than recreate |
| symbol kind/signature | strong | consume rather than recreate |
| package/version identity | strong | useful realization metadata |
| entity before source exists | absent | core AES need |
| planned module/file that has no symbol yet | absent | core AES need |
| one planned unit realizing as several symbols | not native planning concept | core AES mapping need |
| target/gap/plan ownership | absent | AES |
| verification-subject linkage | absent | AES |
| realization lifecycle | absent | AES |

## Result

**SCIP should own realized code-symbol identity/navigation. AES should own planned realization identity and the mapping to realized symbols.**

The right relationship is:

```text
AES planned implementation subject
        ↓ realization
filesystem artifact(s)
        ↓ index
SCIP symbol(s) / occurrences
        ↓
verification + characterization
```

AES should not build a universal parser/indexer/symbol grammar merely to identify classes/functions/methods.

## Canonical model consequence

A planned subject should use a stable AES identity independent of a source symbol. After realization it may bind to zero/one/many external realization refs such as:

```text
realization_ref:
  kind: scip_symbol
  index_revision: ...
  symbol: ...
```

For file/module boundaries that are not naturally represented as a SCIP symbol, AES may also carry a revision-bound repository path reference.

The mapping itself can become evidence-bearing and stale if the implementation changes.

## Stubbing disposition

Safe to stub:
- `PlannedImplementationSubject` or equivalent AES residual;
- realization-reference abstraction supporting external identifiers;
- mapping/characterization boundary from planned subject to realized symbols/files.

Do not stub:
- `CodeSymbol`;
- universal `Function`, `Class`, `Method`, `Reference`, `Occurrence` models;
- a language-neutral symbol grammar;
- a new source index format.

Use SCIP/indexer output when realized-code identity is required.

## Practical implication for the canonical skeleton

When we stub the whole AES repository, the planned-subject registry can name future code homes without pretending those subjects are already SCIP symbols. Once code is created and indexed, characterization binds the planned identity to actual SCIP/file identities.

This preserves stable planning identity across refactors while delegating language semantics to mature code-intelligence tooling.
