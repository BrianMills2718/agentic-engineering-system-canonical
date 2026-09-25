# AES v0.2 provider evaluation — round 2: generic dependencies

Review role: **supporting dependency rationale**. Current candidate bindings are in `21-provider-bindings.candidate.yaml`.

Status: **candidate provider evaluation / non-normative**
Date: 2026-09-24

## Question

Which generic dependencies should the Greenfield MVP actually require a colleague
to install?

The answer should minimize dependency surface without reimplementing solved
mechanics.

## Candidate baseline

~~~text
Git
Python
ruamel.yaml
Pydantic v2
~~~

JSON Schema Draft 2020-12 remains the candidate interchange/published schema
format when/if AES publishes schemas. It is not by itself the semantic validator.

## Git

### Selected capability contribution

Candidate reuse for:

- repository identity;
- exact committed revision;
- tracked-file inventory;
- diff/change sets;
- content retrieval;
- normal version lineage;
- optional local enforcement invocation.

### Important boundary

Git does not own AES target, current, gap, plan, or evidence semantics.

Git hooks do not prove enforcement universally. A standard pre-commit hook can be
bypassed, so AES validation must remain an explicit runnable command/capability.
Hooks, CI, and agent-client adapters invoke the same validator.

### Candidate disposition

`reuse`.

## Python

### Candidate first supported runtime

Python is the first Greenfield-MVP ecosystem/runtime.

Reasons:

- one ecosystem is enough to prove the model;
- the standard library includes AST parsing;
- AES can characterize Python source without importing/executing target modules;
- Python packaging can distribute the AES CLI/tooling directly;
- using Python does not require a universal language abstraction.

### Candidate disposition

`reuse` as the first product runtime, not as an AES semantic dependency.

## Python stdlib ast

### Selected capability contribution

Candidate first source-characterization provider for:

- module/class/function/method identity;
- signatures/annotations;
- docstrings;
- static imports;
- source locations.

### Explicit insufficiency

AST alone does not prove:

- every runtime dependency;
- dynamic import targets;
- actual call graph;
- runtime data flow;
- behavioral conformance.

AES must mark such facts as unobserved/unknown rather than infer certainty.

### Candidate disposition

`reuse`.

## ruamel.yaml

### Why not PyYAML by default

The Greenfield target is human-authored and Git-reviewed. Duplicate mapping keys
must fail rather than silently replace semantic facts, and round-trip preservation
is useful when tooling modifies accepted YAML.

ruamel.yaml's current documented API rejects duplicate mapping keys by default
and supports YAML 1.2 plus round-trip loading/writing.

### AES-owned boundary

ruamel.yaml owns syntax parsing/serialization only.

It does not own:

- AES record semantics;
- ref resolution;
- ID uniqueness;
- semantic invariants;
- evidence sufficiency;
- target/current/gap.

### Candidate disposition

`reuse`.

## Pydantic v2

### Selected capability contribution

Candidate in-process implementation for:

- strict typed Python record models;
- field-level validation;
- serialization;
- model-level validators;
- generation of published structural schemas where useful.

### AES-owned boundary

Pydantic models are implementation of AES semantics, not independent authority.
The canonical project record remains YAML/native project artifacts.

Cross-object semantic validation remains AES code because structural validators
cannot determine all graph invariants merely from local field schemas.

### Candidate disposition

`reuse`.

## JSON Schema Draft 2020-12

### Selected contribution

Candidate external/interchange structural contract for AES YAML-loaded data.

Useful for:

- tooling-neutral schema publication;
- editor integration;
- fixtures;
- basic structural conformance;
- compatibility tests independent from Python implementation.

### Boundary

JSON Schema validates structural instance constraints. AES still needs semantic
validators for:

- typed reference resolution;
- unique semantic identity across relevant scopes;
- no duplicated relationship authority;
- provider/capability ownership rules;
- topology/generation-rule invariants;
- criterion/evidence composition;
- target/current/gap semantics.

### Candidate disposition

`reuse` as published structural schema format, but not required as a separate
runtime engine if Pydantic-generated/checked schemas prove sufficient.

## Dependency policy

For the Greenfield MVP:

1. prefer standard library when it meets the exact need;
2. keep third-party runtime dependencies few and explicit;
3. pin/test supported versions in the distribution;
4. do not depend on private Brian-authored repositories;
5. do not expose internal library types as the enduring AES semantic identity;
6. every generic dependency has a replacement boundary.

## Candidate distribution dependency set

Required candidate runtime:

~~~text
Python supported-version range
ruamel.yaml
Pydantic v2
Git executable
~~~

Optional/development:

~~~text
JSON Schema validator
pytest
type checker/linter
~~~

The exact package versions and Python range remain unselected until the package
skeleton and compatibility tests exist.

## Replacement boundaries

### YAML parser

Replaceable if another parser:

- supports required YAML subset/version;
- rejects duplicate keys;
- preserves human-authored semantics safely;
- passes round-trip/negative fixtures.

### typed validation library

Replaceable if another implementation:

- expresses the accepted AES record model;
- supports strict validation;
- supports required serialization/schema publication;
- preserves all AES semantic validation behavior.

### source analyzer

Python AST is provider-specific. A later language adds a new characterization
provider rather than changing AES target/current semantics.

### revision provider

Git is the Greenfield MVP revision provider. A non-Git repository would require a
future provider that supplies equivalent identity/inventory/change semantics; it
is not part of MVP scope.

## Nonclaims

This round does not yet accept package versions, CLI packaging technology,
installer command syntax, or schema-generation strategy.
