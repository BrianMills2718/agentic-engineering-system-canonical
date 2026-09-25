# AES v0.2 semantic clean-sheet review — pass 3: repository topology

Review role: **historical/supporting rationale**. Current topology semantics are incorporated into `02-semantic-model.candidate.yaml`, `13-greenfield-materialization.candidate.md`, and `20-realization-topology.candidate.yaml`.

Status: **proposal review / non-normative**
Date: 2026-09-24

## Question

What must AES know before a durable repository artifact is allowed to exist?

The Greenfield MVP is intentionally opinionated: repository structure is an
accepted engineering output, not an incidental byproduct of coding.

## Core rule

Every durable governed artifact must be accounted for by exactly one of:

1. an accepted planned artifact with an exact repository path; or
2. an accepted artifact-generation rule that admits the artifact.

Exact path is the default when the path is knowable during planning.

A generation rule is not a wildcard escape hatch.

## Why exact paths are normally target facts

A path affects:

- repository navigation;
- ownership and realization boundaries;
- import/module identity;
- test discovery;
- deployment/build behavior;
- source-local context routing;
- evidence invalidation;
- human and agent expectations.

Therefore a rename of a governed durable artifact is normally a target-topology
change even when its stable semantic subject ID remains unchanged.

## Artifact-generation rule

A generation rule is justified when artifacts are legitimately created as a
family or by an external/native tool and exact members are not usefully enumerable
before generation.

Examples may include:

- package-manager lockfiles;
- generated schema/client families;
- migrations with generated names;
- compiler/build metadata intentionally committed;
- framework-required generated files.

A candidate generation rule must identify at least:

- stable rule ID;
- admitted path namespace/pattern;
- artifact kind;
- producer/tool identity or producer class;
- why this family exists;
- semantic justification refs;
- creation trigger/condition;
- lifecycle/retirement rule;
- whether generated members are editable;
- whether generation must be deterministic/reproducible;
- how realized members are characterized.

The rule must be narrow enough that an unrelated file cannot become legitimate
merely by matching a broad directory wildcard.

## Durable versus ephemeral

The invariant applies to durable repository state.

Ephemeral/tool-cache examples normally excluded:

- __pycache__;
- .pytest_cache;
- temporary build directories;
- editor scratch files;
- local runtime caches.

Whether a generated artifact is ignored by Git is not the semantic test. The
question is whether it is part of governed durable project realization.

## Repository topology is more than source code

Planned topology may include:

- normative authority artifacts;
- source;
- tests/evals;
- configuration;
- native contracts;
- migrations;
- generated durable projections;
- build/package metadata;
- other durable project artifacts.

The Greenfield MVP must not claim repository governance while only accounting for
Python source and tests.

## Bootstrap problem

AES itself must create some initial durable project artifacts before a
project-specific plan can name them.

That does not justify unplanned bootstrap files.

The distribution needs an accepted **initialization contract** that defines the
minimal artifacts/rules created by the project initializer. Those become the
starting accepted topology from which project-specific target/planning proceeds.

The exact initialization materialization remains undecided, but the semantics are
not:

- every initialized durable artifact has a declared reason;
- initialization does not silently import historical/private repository
  machinery;
- initialized authority versus generated scaffolding is explicit;
- a user can inspect why each initialized artifact exists.

## Realization unit versus file

File and realization-unit boundaries are different.

A realization unit groups artifacts because a shared responsibility/context/
ownership/lifecycle makes the grouping meaningful.

A file exists because its own durable artifact purpose is justified.

Therefore:

~~~text
realization unit
    owns grouping of
        planned artifact A
        planned artifact B
        planned artifact C
~~~

does not imply "one component = one file."

Likewise, a large file is not invalid because of line count alone. Split when a
meaningful engineering boundary is created, not merely to improve human reading.

## Agent-oriented cohesion test

A candidate realization unit is coherent when the same bounded working context
can govern most changes to its artifacts without repeatedly importing unrelated
norms, providers, state ownership, verification, or failure/recovery semantics.

This reframes cohesion for an agent-oriented system:

> A good realization boundary minimizes semantic/context switching and
> invalidation ambiguity, not merely file size.

## Selected symbol commitments

Exact artifact topology does not require planning every symbol.

A symbol becomes a target commitment only when its identity/type/signature or
narrow obligation matters independently, for example:

- public/consumer boundary;
- consequential cross-unit seam;
- native contract implementation point;
- externally referenced entrypoint;
- independently verified boundary;
- deliberately frozen strong type/signature;
- source-local context needs narrower-than-artifact applicability.

Private helpers remain realized implementation detail by default.

## Orphan conditions

Candidate hard findings include:

- durable file exists with no planned artifact or matching accepted generation
  rule;
- planned artifact is missing;
- artifact matches multiple conflicting generation rules;
- generation rule is broader than its declared semantic family;
- path changes without accepted topology change;
- planned verification artifact exists but maps to no criterion;
- test exists with no verification purpose;
- generated durable artifact cannot identify its generator/rule;
- realized artifact is assigned to a realization unit only through heuristic
  guessing.

## Consequence

The semantic model needs first-class artifact-generation rules and an
initialization contract concept.

Neither requires choosing a hook system, build tool, framework, or repository
layout yet.
