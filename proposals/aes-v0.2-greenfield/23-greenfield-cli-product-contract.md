# AES v0.2 Greenfield CLI/product contract

Status: **candidate product surface / non-normative**
Date: 2026-09-24

## Product principle

A colleague should not need to understand AES internals, provider repositories, or
historical governance systems to use the supported Greenfield lifecycle.

The CLI is a composition surface over AES capabilities. It does not own their
semantics.

Candidate executable:

~~~text
aes
~~~

## 1. Initialize adoption

~~~text
aes init --project-id <id>
~~~

Preconditions:

- current directory is a Git repository or the command is given an explicit
  project root;
- .aes/ does not already represent an incompatible adoption.

Effects:

- create .aes/project.yaml;
- do not create empty target/analysis/plan/observation/generated artifacts;
- report the next required semantic action: establish an outcome.

Must not:

- install private repositories;
- create CLAUDE.md/AGENTS.md/relationships.yaml/meta-process.yaml implicitly;
- install hooks without explicit opt-in;
- write credentials.

## 2. Establish/validate target

Candidate commands:

~~~text
aes target validate
aes target show
~~~

Target authoring may initially occur through direct YAML editing or an agent/human
planning interaction.

The CLI should not require a form wizard before the target schema is proven.

Validation includes:

- strict YAML parsing;
- structural typing;
- stable-ID uniqueness;
- typed-ref resolution;
- criterion/evidence requirements;
- topology/provider/verification invariants once present.

Exit non-zero on invalid canonical target.

## 3. Materialize current/gaps before implementation

~~~text
aes reconcile
~~~

For a fresh target with no realization yet, output explicitly represents
unrealized current and open gaps.

Effects:

- produce/rebuild .aes/generated/current.yaml;
- produce/rebuild .aes/generated/gaps.yaml;
- retain provenance/input identities.

## 4. Prepare planning problem

~~~text
aes plan prepare [--gap <gap-id> ...]
~~~

Output:

- structured planning request;
- readable summary;
- request identity/digest;
- exact target/current/gap/analysis input identities;
- planning contract and output requirements.

Default behavior should select the smallest gap/concern set necessary rather than
dump all project state when the selected concern is known.

## 5. Validate provider proposal

~~~text
aes plan validate <proposal>
~~~

Checks:

- proposal binds to the correct planning request;
- no unknown/unresolved refs are silently accepted;
- every proposed durable artifact has exact path or bounded generation rule;
- selected symbol commitments bind to planned artifacts;
- exercised criteria have concrete verification routes;
- load-bearing uncertainty is either resolved or represented by a probe/stopping
  rule;
- provider bindings expose semantic/replacement boundaries.

The command does not accept target changes automatically.

## 6. Accept planning result

Candidate command:

~~~text
aes plan accept <proposal>
~~~

This is a consequential mutation.

Minimum behavior:

1. verify proposal is still based on current planning inputs;
2. materialize the accepted target delta into .aes/target.yaml;
3. write the accepted transition plan under .aes/plans/;
4. validate resulting target;
5. recompute current/gaps;
6. report closing gaps and next execution boundary.

The exact human/authorization confirmation model remains open. The CLI must never
silently accept a stale proposal.

## 7. Check repository conformance

~~~text
aes check
aes check target
aes check topology
aes check evidence
~~~

aes check is the truthful aggregate local gate for AES-owned invariants.

It must be directly runnable.

Optional Git/CI/agent hooks invoke these commands; they do not replace them.

Topology findings distinguish at least:

- missing planned artifact;
- orphan governed artifact;
- generation-rule mismatch;
- selected symbol/signature/type mismatch;
- unresolved realized identity;
- intended/observed dependency mismatch when configured as consequential.

## 8. Characterize realized repository

~~~text
aes characterize
~~~

For the first Python/Git provider:

- bind exact Git revision;
- inventory governed/tracked artifacts;
- parse Python source statically;
- record symbols/signatures/types/docstrings/imports;
- preserve uncertainty/unsupported dynamic facts;
- compare selected planned identities where mechanically valid.

Output is generated observation/current substrate, not target authority.

## 9. Project working context

~~~text
aes context <subject>
aes context <subject> --format json
~~~

Subject forms remain to be frozen, likely stable semantic subject IDs with
path/symbol locators accepted as convenience resolution inputs.

Human-readable default includes:

- subject identity;
- full applicable normative text;
- full criterion/disproof text;
- provenance;
- current;
- gaps;
- active plan transition;
- verification obligations;
- relevant dependency consequences;
- explicit unresolved/omitted supporting context.

No required semantic atom is silently clipped to satisfy a context budget.

## 10. Record observations

Candidate boundary:

~~~text
aes observe ...
~~~

Do not force every external test runner through an AES wrapper.

AES needs a way to retain observations from:

- deterministic commands/tests;
- runtime probes;
- human reviews;
- LLM rubrics;
- external consumer use.

The exact command grammar is deferred until observation schemas are stable.

A test command's exit code alone is not criterion satisfaction.

## 11. Assess/reconcile evidence

Candidate commands:

~~~text
aes evidence assess
aes reconcile
~~~

evidence assess:

- finds criterion evidence requirements;
- evaluates available observations;
- computes freshness/adequacy/standing with assessor provenance.

reconcile:

- combines target, realized characterization and evidence assessments;
- rebuilds current/gap;
- never uses plan-complete status as closure evidence.

These may later be combined operationally if that improves UX without collapsing
their semantics.

## 12. Inspect state

~~~text
aes status
~~~

Compact output should answer:

- What outcome are we pursuing?
- What is current?
- What gaps remain?
- What plan is active?
- What evidence is stale/insufficient?
- What is the next governed action?

It is a projection, not another authority.

## 12a. Human review surface (candidate, added 2026-09-25)

~~~text
aes review [--decision <file>]
~~~

Writes `.aes/generated/review.html`: a self-contained page a person opens
with `file://` to judge the accepted target and its realization without
reading YAML. Pending decision first, then intent, rules, proof coverage with
existence marks, file map, orphans. Derived, never authority. See open
question 22. Temporary renderer: AES `scripts/probe/render_review.py`.

## 13. Optional adapters

Not required for core MVP:

~~~text
aes install-hook git
aes adapter install <agent/client>
~~~

Any adapter must call the same core commands/models rather than reimplement AES
rules.

## Greenfield happy path

~~~text
git init my-project
cd my-project

install AES distribution

aes init --project-id my-project
# establish first accepted target outcome
aes target validate
aes reconcile

aes plan prepare
# human/agent produces proposal
aes plan validate proposal.yaml
aes plan accept proposal.yaml

# implementation
aes check
aes characterize
# run/record required observations
aes evidence assess
aes reconcile

aes status
~~~

At any implementation step:

~~~text
aes context <subject>
~~~

provides the bounded working surface.

## Error design

Errors must be actionable.

A hard failure should identify:

- violated invariant;
- exact subject/file/ref;
- current evidence/input identity;
- recovery class:
  - fix implementation;
  - amend target;
  - replan;
  - rerun observation;
  - resolve uncertainty;
  - refresh stale planning/context input.

Do not emit "policy failed" without a runnable next route.

## CLI nonclaims

This candidate does not yet freeze:

- argument spelling;
- target-authoring UX;
- interactive TUI;
- automatic LLM API integration;
- Git hook installation behavior;
- CI provider;
- observation command grammar;
- deployment/operations workflows.
