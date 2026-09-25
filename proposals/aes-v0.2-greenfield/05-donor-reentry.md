# AES v0.2 donor/provider re-entry rule

Review role: **supporting principle**. Current provider decisions are summarized in `21-provider-bindings.candidate.yaml`.

Status: **candidate evaluation rule / non-normative**

## Purpose

Prevent the clean-sheet architecture from silently becoming a repackaging of
existing private systems.

The v0.2 semantic model is derived first. Only then are prior mechanisms compared
against required capabilities.

## What prior work contributes before provider selection

Prior systems may contribute:

1. **observed failure modes** — evidence about what previously went wrong;
2. **candidate capabilities** — useful abilities demonstrated by earlier systems;
3. **mechanism evidence** — concrete evidence that an implementation did or did
   not work under stated conditions;
4. **constraints/lessons** — information that should shape success/disproof
   criteria.

They do not contribute automatic architecture ownership.

## Re-entry procedure

For each candidate mechanism:

```text
AES capability requirement
        ↓
semantic boundary
        ↓
success + disproof criteria
        ↓
distribution requirement
        ↓
candidate provider evaluation
        ↓
reuse | configure | adapt | compose | residual | reject
```

The evaluation must be possible without changing the AES requirement merely to
match the candidate's vocabulary.

## Candidate donors to inspect later

The following are explicitly **not selected** by this document:

- current AES v0.1/bootstrap mechanisms;
- Company Planning;
- Enforced Planning;
- Project Meta;
- prior hook systems;
- Agentic Capability Architecture;
- Data Contracts;
- Code Map;
- Representation Router;
- Fluid Governance;
- other Brian-authored repositories;
- external standards/OSS identified by earlier research.

External standards and mature OSS receive the same capability-fit treatment.
"External" is not equivalent to "correct provider."

## Required questions

For a candidate provider:

- Which exact AES capability does it satisfy?
- Which AES semantic facts remain owned by AES?
- What API/contract does AES rely on?
- What required behavior is unsupported?
- What assumptions or hidden dependencies does the provider introduce?
- Can an ordinary AES user obtain/configure it?
- What evidence proves the fit?
- What negative result would reject the provider?
- What is the replacement boundary?
- Does adoption create duplicate semantic authority?

## Distribution gate

A mechanism that only works because Brian has access to a private companion
repository is not an acceptable default Greenfield-MVP provider unless that
provider is deliberately packaged/distributed as a supported dependency.

Historical provenance may identify where a mechanism came from without exposing
that historical repository as a user prerequisite.

## Extraction rule

Do not create a separate repository merely because a capability has a name.

Keep an implementation inside AES canonical until there is a demonstrated
ownership/release/reuse boundary that justifies extraction. Capability,
component, package, repository and provider are separate concepts.

## Expected first provider evaluations after semantic acceptance

Likely capability families to evaluate include:

- AES planning derivation;
- repository/artifact admission;
- execution custody and protected actions;
- source characterization;
- revision/source identity;
- typed boundary validation;
- context projection;
- evidence/verification execution.

This list is not a selection or implementation plan.
