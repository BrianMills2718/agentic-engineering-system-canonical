# AES v0.2 provider evaluation — round 1

Review role: **supporting provider rationale**. Current candidate bindings are in `21-provider-bindings.candidate.yaml`.

Status: **candidate provider evaluation / non-normative**
Date: 2026-09-24
Contract: `17-provider-evaluation-contract.candidate.yaml`

## Scope

Evaluate providers for the Greenfield-MVP capability set from the AES capability
requirements outward.

This is not a general review of prior repositories.

Candidate evidence inspected:

- `BrianMills2718/company-planning@54dc2a2f64eb081b9a69bd02f827214b7fa13cda`
- `BrianMills2718/enforced-planning@f96930777388b03b3d56cd526f9dd0935b73460f`
- `BrianMills2718/project-meta@380b4de184942b5ebec74885fb5cb5b60a7e78df`
- `BrianMills2718/data-contracts@a1fe25d8d5ef750d3fad186ff9804aa4cddb52d9`
- `BrianMills2718/agentic-capability-architecture-canonical@a7dae1a779523fa42cc1013535f334f02621dfb9`
- current public documentation for Git, Python AST, and ruamel.yaml.

No provider binding below is accepted merely by appearing in this document.

---

## Proposed first supported ecosystem

**Candidate:** Python project in a Git repository.

Reasons:

- Git provides exact commit/repository lineage and deterministic tracked-file
  inventory without AES inventing version control.
- Python's standard `ast` API parses source into an AST without importing or
  executing target modules and exposes syntax, symbol and annotation structure.
- The AES Greenfield MVP needs one authentic supported ecosystem, not universal
  language abstraction.
- Python keeps the first source-characterization residual small enough to test
  the AES semantics rather than a language-server platform.

Nonclaim:

This is not evidence that Python is the best long-term or only ecosystem.

---

# CAP-GF-INIT — initialize a fresh AES-governed project

## Requirement boundary

The provider must create only initialization-contract artifacts, require no
private historical repository, keep secrets out of canonical records, and expose
actionable failures.

## Candidate evaluation

### Existing private systems

**Company Planning:** reject as initialization provider.

Its product is a planning-method/plugin distribution, not a minimal AES project
initializer. Requiring it would also make Greenfield initialization depend on
access to a separate private planning repository in its current form.

**Enforced Planning:** reject as initialization provider.

Its governed-repository installers bring their own governance/context model and
expect existing surfaces such as CLAUDE.md, relationships declarations and
file-context runtime in some installation modes. That is exactly the hidden
architecture inheritance v0.2 is avoiding.

**Project Meta:** reject as initialization provider.

It is explicitly an ecosystem governance hub with project graph/policy ownership,
not a portable project bootstrap substrate.

## Proposed disposition

`residual` — implement the thin AES initializer inside AES canonical.

Generic providers:

- Git for repository identity when Git is the selected revision provider;
- strict YAML loader/validator dependencies used by the target capability.

The initializer should remain boring: create only what the accepted
initialization contract authorizes.

---

# CAP-GF-TARGET — represent and validate accepted target

## Requirement boundary

AES needs multiline structured normative text, stable semantic IDs, typed refs,
strict validation, duplicate-key rejection, and cross-record semantic checks.

## Candidates

### data-contracts

**Disposition:** reject as the target-semantic owner; possible narrow reuse later
for native typed-boundary validation.

Data Contracts owns producer/consumer boundary contracts and provider-neutral
composition validation. Its own capability decomposition explicitly excludes
project-specific planning/semantic-build ownership. Reusing it as AES target
authority would broaden its semantic ownership incorrectly.

### Pydantic

**Disposition:** candidate `reuse` for in-process typed model validation.

Useful generic mechanics:

- typed Python models;
- strict field validation;
- schema generation support.

AES still owns every target semantic type and cross-reference invariant.

### ruamel.yaml

**Disposition:** candidate `reuse` for YAML loading/writing.

Material fit:

- YAML 1.2 support;
- round-trip preservation useful for human-authored Git diffs;
- duplicate mapping keys are rejected by default in the documented API.

AES must still validate semantic refs and invariants after parsing.

## Proposed composition

```text
ruamel.yaml
    ↓ parse strict YAML
AES-owned typed models / semantic validators
    ↓
Pydantic as generic validation implementation candidate
```

Do not create an AES YAML language beyond the accepted record shapes.

---

# CAP-GF-PLANNING — derive realization and verification target

## Requirement boundary

Planning must consume accepted target/current/gaps/analysis, produce a proposed
target-realization delta, preserve load-bearing uncertainty, derive exact artifact
and verification topology where knowable, and separate design from execution
transition.

## Company Planning

**Disposition:** `adapt` as the strongest current method donor; not selected as
the Greenfield runtime/distribution dependency.

Strong fit already demonstrated by its bounded-design method:

- target outcome -> requirements -> boundaries -> domain rules -> contracts ->
  schema -> fixtures -> thin slices;
- success/disproof before implementation;
- capability/provider landscape and reuse/supersession reasoning;
- failure/containment/recovery concerns;
- authentic human-reviewable outcomes;
- design before downstream decomposition.

Material gaps against AES v0.2:

- it does not currently make exact durable repository topology a universal
  planning output;
- its broad plugin/workflow semantics exceed the AES planning boundary;
- current distribution requires access to a separate private repository;
- its existing semantic kernels/graphs must not become AES target authority.

## Proposed disposition

Implement **AES Planning** as an AES-local capability whose method can adapt the
useful bounded-design reasoning from Company Planning.

Do not make Company Planning a hidden prerequisite for colleagues.

A later distribution decision may package/reuse the provider if it satisfies the
standalone gate without transferring AES semantic authority.

---

# CAP-GF-TOPOLOGY — materialize and assess durable topology

## Requirement boundary

Exact path or bounded generation rule; orphan detection; durable/ephemeral
distinction; accepted topology-amendment recovery path.

## Enforced Planning artifact creation

**Disposition:** reject as direct provider; retain as mechanism donor.

Useful evidence:

- existing artifact-intent checks require creation justification and
  separate-file reason;
- observe/enforce staging exists;
- negative-control tests exist.

Mismatch:

- current implementation is coupled to its own meta-process configuration and
  relationship registry;
- its artifact model is not the v0.2 target.yaml topology model;
- importing the whole provider would reintroduce duplicate/inherited authority.

## Git

**Disposition:** `reuse` as repository inventory/revision provider.

Use Git-native tracked-file inventory and revision identity.

Important limitation:

Git hooks are only invocation channels. Standard pre-commit hooks can be bypassed
with `--no-verify`; AES correctness cannot depend on the hook having run.

## Proposed composition

```text
AES-local topology validator
    reads accepted target topology
    + Git repository inventory
    + accepted generation rules
        ↓
findings / hard exit status

optional invocation adapters
    pre-commit
    CI
    agent pre-write hooks
    explicit CLI
```

The validator is the capability. Hooks are adapters.

---

# CAP-GF-CONTEXT — project bounded complete working context

## Requirement boundary

Full applicable normative/success/disproof text, provenance/freshness, bounded
subject relevance, explicit omission/unresolved state, no required ID
dereference.

## Enforced Planning context system

**Disposition:** reject as direct v0.2 provider; strong algorithm/negative-evidence
donor.

Useful evidence:

- deterministic static inventory;
- Python AST symbol/signature/docstring extraction;
- bounded context packets;
- provenance;
- explicit unresolved/omitted context;
- content receipts and required-atom handling;
- source-derived summaries rather than duplicated registry prose.

Material mismatches:

- relationship-context design relies on a reviewed authored
  `relationships.yaml`;
- some consumer modes require CLAUDE.md, relationships.yaml, Makefile and
  existing file-context runtime;
- current packet semantics rank/compile neighbors from a different authority
  model;
- v0.2 requires full target semantics to derive directly from target/current/gap
  refs rather than a parallel relationship registry.

## Proposed disposition

Implement the first AES context compiler locally from:

```text
typed target refs
+ planned topology
+ realized characterization
+ current/gaps
+ plan
        ↓
subject-specific projection
```

Reuse ideas and possibly small source-characterization routines only after they
fit the new inputs.

Do not adopt relationships.yaml as a prerequisite.

---

# CAP-GF-CHARACTERIZE — characterize realized repository

## Requirement boundary

Exact revision, durable artifacts, selected symbols/signatures/types,
dependencies with uncertainty/provenance, no invented target mappings.

## Python stdlib AST

**Disposition:** candidate `reuse` for the first Python source provider.

Sufficient candidate first slice:

- parse Python without importing target code;
- enumerate module/class/function definitions;
- reconstruct selected signatures/annotations;
- extract docstrings;
- enumerate static imports with source locations.

Do not claim static AST knows every dynamic call/dependency.

## Git

**Disposition:** `reuse` for:

- exact revision;
- tracked-file inventory;
- changed-file comparison;
- content retrieval/digests as needed.

## Enforced Planning source inventory

**Disposition:** donor / possible code salvage after ownership review.

Its AST/static-inventory experience provides useful evidence, including failures
where early projections omitted private documented callables. But importing its
whole relationship compiler would bring unrelated semantics.

## Proposed composition

First provider:

```text
Git
+ Python stdlib ast
+ AES-local characterization model
```

This is intentionally Python-specific for the MVP.

---

# CAP-GF-EVIDENCE — assess freshness, adequacy and standing

## Requirement boundary

Keep observed result distinct from freshness/adequacy/standing; bind assessor
identity/version; preserve insufficient/unassessed states.

## Existing private providers

No inspected prior system cleanly owns this exact semantic model.

Company Planning and Enforced Planning contain evidence contracts and verification
mechanics, but adopting either as the authority would import broader lifecycle
semantics.

Data Contracts can validate typed receipt shapes but does not own criterion
sufficiency.

## Proposed disposition

`residual` — AES-local evidence-assessment semantics.

Generic mechanics may use Pydantic/JSON Schema for representation validation.

Assessment implementations should be deterministic where possible. Human or
model assessment remains explicitly identified as such.

---

# CAP-GF-RECONCILE — derive current and gap

## Requirement boundary

Current = qualified target-relative state.
Gap = target/current variance.
Plan completion has no closure authority.

## Existing systems

No existing provider should own this because these are core AES semantics.

Project Meta, Enforced Planning, and Company Planning all contain notions of
status, planning, evidence, or policy, but adopting one would make AES's defining
state model dependent on another product.

## Proposed disposition

`residual` — AES-local core.

This should be a small deterministic semantic engine over:

- accepted target;
- realized characterization;
- evidence assessments.

---

# Capability/provider summary

| AES capability | Round-1 disposition |
|---|---|
| CAP-GF-INIT | AES-local residual; Git + validation dependencies |
| CAP-GF-TARGET | AES-owned semantics; candidate ruamel.yaml + Pydantic mechanics |
| CAP-GF-PLANNING | AES-local capability adapting Company Planning method ideas |
| CAP-GF-TOPOLOGY | AES-local validator + Git; old artifact gate is donor only |
| CAP-GF-CONTEXT | AES-local projector; Enforced Planning context work donor only |
| CAP-GF-CHARACTERIZE | Git + Python stdlib AST + AES-local model |
| CAP-GF-EVIDENCE | AES-local semantic engine; generic validation libraries only |
| CAP-GF-RECONCILE | AES-local core semantic engine |
| capability/provider discovery | ACA may be queried as one provider knowledge source, never AES authority |
| native typed boundaries | Data Contracts may be reused when a real project boundary needs its semantics |

## Project Meta disposition

Project Meta is **not selected for any Greenfield-MVP runtime capability**.

Its historical work is useful evidence for:

- authority classification;
- visibility-before-enforcement;
- context/relationship failure modes;
- project lifecycle/policy lessons.

But it is explicitly an ecosystem governance hub. Making it a Greenfield AES
dependency would violate the standalone-product boundary and reintroduce the old
ecosystem architecture through the back door.

## ACA disposition

ACA is not a runtime dependency for the AES semantic core.

During provider selection it may contribute:

- provider-independent capability identity;
- verified semantic exports;
- selected/rejected provider evidence.

AES planning still owns the project's requirement, provider binding, and local
residual decision.

## Data Contracts disposition

Data Contracts remains a narrow candidate provider for typed native boundary and
composition semantics when an authentic project needs them.

It is not the AES target schema, relationship graph, planner, repository
characterizer, evidence model, or current/gap engine.

## Round-1 architectural consequence

The likely Greenfield MVP is smaller than v0.1's provider topology:

```text
AES package
  owns:
    semantic models
    initialization
    target validation
    planning contract + AES planning behavior
    topology validator
    context projection
    Python characterization adapter
    evidence assessment
    current/gap reconciliation

  generic dependencies:
    Git
    strict YAML parser
    typed validation library
    Python stdlib AST

  optional project/provider integrations:
    external/native product dependencies
    ACA knowledge when useful
    Data Contracts when its actual boundary semantics fit
```

This is not a final package topology yet. It is the first provider disposition
that survives the clean-sheet contract.
