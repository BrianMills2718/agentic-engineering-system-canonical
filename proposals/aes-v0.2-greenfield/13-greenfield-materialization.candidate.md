# AES v0.2 Greenfield MVP materialization candidate

Status: **candidate materialization / non-normative**
Date: 2026-09-24

## Goal

Choose the smallest opinionated project storage convention that can materialize
the clean semantic model for a fresh project without making storage layout part
of the ontology.

This is deliberately Greenfield-MVP scoped.

## Candidate root

Use one project-local AES control root:

~~~text
.aes/
~~~

Rationale:

- unambiguous ownership by the AES distribution;
- does not compete with native source/test/contract roots;
- makes generated versus native project artifacts distinguishable;
- avoids inheriting the v0.1 .agentic naming merely for compatibility;
- allows a colleague to identify the AES control surface immediately.

The root name remains candidate until the initialization contract is accepted.

## Candidate canonical files

~~~text
.aes/
├── project.yaml
├── target.yaml
├── analysis.yaml                 # created when accepted analysis exists
├── plans/
│   └── PLAN-<id>.yaml
├── observations/
│   └── <observation-id>.yaml
└── generated/
    ├── current.yaml
    ├── gaps.yaml
    ├── semantic-graph.yaml
    └── ... concern-specific projections
~~~

Native implementation remains in the ecosystem's normal locations, for example
src/, tests/, package manifests, framework directories, contracts, migrations,
and deployment configuration as appropriate.

AES does not relocate native authorities into .aes merely for uniformity.

## .aes/project.yaml — operational adoption/configuration

Purpose:

- identify the project and AES architecture/distribution version;
- identify enabled/supported ecosystem adapters;
- configure operational defaults that are not project normative target;
- locate generated output if defaults are overridden;
- declare supported provider configuration references where operationally needed.

Must not become a dumping ground for:

- requirements;
- success criteria;
- accepted repository topology;
- provider-binding architecture decisions;
- current/gap state;
- secrets.

Candidate distinction:

~~~text
project.yaml
  how this repository uses the AES product

target.yaml
  what this project has accepted should be true
~~~

Environment secrets remain outside canonical project target records.

## .aes/target.yaml — canonical accepted target

Candidate Greenfield-MVP authority for:

- outcomes;
- normative items;
- success/disproof/evidence requirements;
- accepted capability requirements;
- accepted provider bindings;
- accepted realization units;
- accepted planned artifacts;
- accepted artifact-generation rules;
- selected planned symbol commitments;
- accepted verification subjects.

This is one structured authority in the MVP to avoid premature partitioning and
duplicate joins.

The semantic items retain stable IDs so later architecture versions can partition
the physical storage without changing semantic identity.

### Why one target file first

Advantages:

- one atomic target snapshot;
- no cross-file synchronization protocol needed for the MVP;
- many-to-many semantic refs are local and mechanically resolvable;
- context/wiki projections mean humans/agents do not need to browse this whole
  file during ordinary implementation;
- target changes can be reviewed as one coherent semantic diff.

Risk:

- target.yaml can become large.

Disposition:

Accept that risk for the Greenfield MVP. Split only after measured scale/concurrent
editing pressure justifies a partitioning design.

## .aes/analysis.yaml — accepted engineering analysis

Candidate authority for accepted non-target analysis needed by planning, initially:

- failure modes;
- material feasibility findings;
- explicit planning uncertainties that remain active;
- provider-landscape references/dispositions before provider binding is accepted.

Analysis may cause target changes but does not itself become target/current
conformance state.

Do not store broad research prose here. Retain source research in its natural
external/project research surface and reference it.

## .aes/plans/PLAN-<id>.yaml — accepted transitions

One plan file owns one accepted time-bounded transition.

Candidate contents:

- plan identity/status;
- origin gap refs;
- intended transition;
- proposed target changes;
- verticals/probes;
- planning uncertainty/stopping rules;
- execution boundaries;
- completion evidence requirements;
- provider selections proposed by this transition;
- plan dispositions/history refs as needed.

When a target change is accepted, target.yaml is updated atomically with the plan
acceptance/change. The plan remains transition history, not timeless target
authority.

## .aes/observations/<observation-id>.yaml — revision-bound observations

Candidate append-only project evidence surface for AES-native observation
receipts.

Each observation records what actually ran/was attempted and its exact
subject/revision/provider/method/result/error.

This directory does not imply that large native tool artifacts must be copied
into YAML. An observation may reference an external/native retained artifact with
identity/digest.

Evidence assessments may be generated from observations or retained alongside
them depending on the later evidence design.

Observation IDs must be stable and unique; timestamp-only identity is not assumed.

## .aes/generated/ — rebuildable projections

Never independent authority.

Candidate outputs:

- current.yaml;
- gaps.yaml;
- semantic-graph.yaml;
- subject/working context;
- human navigation/review views;
- conventional requirements/architecture views.

A generated projection must identify enough provenance/freshness information to
determine whether it is current.

Deleting and regenerating this directory must not destroy normative target,
accepted analysis, accepted plan history, native realization, or retained
observation evidence.

## YAML as the Greenfield-MVP canonical structured representation

Candidate choice: YAML for AES-authored structured project records.

Reasons:

- readable multiline normative prose;
- easy diff/review in Git;
- convenient typed validation;
- direct representation of IDs/refs/lists/mappings;
- usable by humans without requiring a database.

YAML is a representation choice, not the semantic model.

The implementation must reject dangerous ambiguity such as duplicate mapping
keys. Schemas/validators remain to be designed after the record shape stabilizes.

## Native artifacts remain native

Examples:

- Python/TypeScript/Rust/etc. source remains native code;
- OpenAPI remains OpenAPI when it is the actual API contract;
- package manifests/lockfiles remain ecosystem-native;
- database migrations remain framework-native;
- tests remain the framework's normal test format.

AES target.yaml references and governs these where appropriate; it does not copy
their full semantics into an AES replacement format.

## Initialization contract

A fresh-project initializer should create only the minimum durable AES control
surface required before project-specific planning.

Candidate initial materialization:

~~~text
.aes/project.yaml
.aes/target.yaml
~~~

analysis.yaml, plan files, observations and generated projections appear only
when their semantic class exists.

The initializer may also create native project bootstrap artifacts only when the
chosen initialization workflow has already accepted their purpose/topology.

Do not create empty directories merely to advertise future capabilities.

## Atomicity requirement

Changes that accept a new target topology must not leave target authority and
native realization in a misleading half-state.

Candidate transaction boundary for Git-based projects:

- target/plan changes;
- created/renamed/removed governed artifacts;
- affected verification topology;
- regenerated required projections/receipts as defined later;

are reviewed as one coherent change set.

Whether a single Git commit is always required remains open, but the resulting
accepted revision must be internally reconcilable.

## Source-local context is a projection, not another authority

The working context may eventually be delivered via:

- generated source region;
- sidecar;
- agent/IDE injection;
- hybrid.

Whichever mechanism is selected, it is generated from target/current/gap/plan
facts and contains full applicable semantic text with provenance.

Do not create another manually maintained source-local normative authority.

## Relationship graph remains generated

No relationships.yaml is part of this candidate layout.

semantic-graph.yaml is generated from:

- typed target refs;
- plan refs;
- realized characterization;
- observation/evidence refs;
- derived impact/relevance relationships.

If later work proves a relationship has no natural owning fact, add the smallest
specific authored semantic type required rather than defaulting to a universal
edge registry.

## Explicit nonclaims

This candidate does not decide:

- the final .aes root name;
- exact YAML schemas;
- provider APIs;
- source characterization implementation;
- context delivery mechanism;
- observation/evidence file granularity at scale;
- signing/attestation format;
- retrofit layout;
- organization-level configuration.
