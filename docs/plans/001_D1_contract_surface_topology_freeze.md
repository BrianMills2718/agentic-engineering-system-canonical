# Plan 001 / D1 — Contract, surface, and topology freeze

Status: ready dependency-resolution brief; implementation not authorized by this artifact.
Parent authority: [`001_repository_context_resolution_vertical.md`](001_repository_context_resolution_vertical.md).

This is a subordinate execution brief for **Dependency subplan D1** in Plan 001. It does not create a second plan, add success criteria, or change the accepted outcome. If this brief conflicts with Plan 001, Plan 001 wins and this brief must be corrected or retired.

## Purpose

Close only the remaining design decisions that prevent Slice 1 from starting without hidden architectural choices:

1. determine the natural owner/shape of the repository-context result contract;
2. choose the smallest authentic human/agent entrypoint for Slice 1;
3. freeze concrete implementation and verification subjects;
4. record the exact provider/dependency disposition needed to execute Slice 1.

D1 is `dependency_resolution`, not an implementation slice. Its mandatory return path is **immediately to Plan 001 / Slice 1**.

## Accepted Slice 1 outcome

Do not redesign this outcome during D1:

> A person or agent entering the exact reviewed `data-contracts` revision can use one source-bound surface to identify the relevant navigation and authority surfaces, see uncertainty/absence/error honestly, reach the exact supporting source/evidence, and know the legitimate place to deepen next without reconstructing the repository from raw code or agent dialogue.

The surface is an actor boundary, not necessarily a graphical application. A CLI, generated local HTML view, existing representation provider, or another small authentic interaction may qualify if it satisfies the parent plan.

## D1 inputs

Use only enough source material to decide the four items above:

- Plan 001 and its AC-001 through AC-011;
- `docs/architecture/SYSTEM_BOUNDARY.md`;
- `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`;
- `research/investigations/2026-09-16-repository-context-provider-landscape.md`;
- current Data Contracts native contract/capability ownership surfaces;
- current ACA discovery/provider knowledge;
- current repository conventions needed to place the smallest residual implementation;
- Representation Router only if Slice 1 actually requires representation-selection/composition capability rather than a simple bounded projection.

Freeze the exact `data-contracts` revision used for the Slice 1 canonical example as part of D1 output.

## Decision 1 — Result-contract disposition

Answer:

```text
Does an existing native/provider-neutral typed contract honestly express
RepositoryContextArtifact semantics?
```

Choose exactly one disposition:

- `reuse` — existing owner/contract matches;
- `extend` — natural owner exists and a narrow compatible extension is justified;
- `aes_local_residual` — no existing neutral contract fits, so the smallest project-local typed boundary is justified.

Do not create a generic repository-context contract merely because Data Contracts exists. Do not move Data Contracts' native contract authority into AES.

Record:

- contract owner;
- exact contract/schema/model reference if reused/extended;
- semantic fields Slice 1 actually requires;
- compatibility/version implications;
- why rejected nearby contracts/providers do not fit.

## Decision 2 — Slice 1 actor surface

Choose the **smallest authentic surface** that makes AC-010 and Attention Checkpoint A1 possible.

Consider only decision-relevant alternatives, for example:

- structured CLI / terminal interaction;
- generated local HTML or equivalent inspectable artifact;
- reuse/adaptation of an existing representation capability such as Representation Router;
- another established local surface that is cheaper and equally authentic.

Evaluate qualitatively against:

- direct usability for repository orientation;
- progressive disclosure with exact source/revision reachable;
- honest `NONE` / `ERROR` / unresolved presentation;
- implementation and maintenance cost;
- AI/tool/runtime cost where material;
- stakeholder reconstruction/attention cost;
- reversibility and replaceability;
- whether the option forces a premature frontend/framework commitment;
- whether it creates a new semantic/workflow authority.

Do not choose a richer surface merely because it is visually impressive. Do not choose raw JSON merely because it is cheap if the reviewer must reconstruct the experience mentally.

The output may be a **temporary validated projection**. D1 must not design the final AES UI.

## Decision 3 — Concrete implementation topology

Freeze only subjects required by Slice 1.

At minimum resolve concrete homes for the conceptual roles already named by Plan 001:

- `RepositoryContextResolver`;
- `RepositoryContextArtifact` or selected native equivalent;
- `AuthoritySurfaceObservation`;
- bounded legacy-repository adaptation;
- pilot-manifest reading where needed for tests/negative controls;
- `RepositoryContextWorkingSurface` or the selected authentic entrypoint.

For each subject record:

- exact repository path/module;
- owner/authority role;
- consumed contracts/providers;
- whether it is selected provider code, AES residual semantics, adapter, projection, or verification;
- intended consumer.

Do not introduce a generalized crawler, symbol index, graph store, characterization platform, representation framework, or fleet abstraction to make the topology look complete.

## Decision 4 — Verification topology

Map every Plan 001 criterion to a concrete planned check/observation while preserving the distinction between **check success** and **required evidence adequacy**.

D1 must identify concrete subjects for:

- exact-revision external consumer case;
- wrong-`contracts/` negative assertion;
- missing-wiki behavior;
- capability-decomposition routing;
- source/evidence provenance;
- malformed-manifest negative control;
- absent-declaration negative control;
- block/recovery or escalation path;
- post-implementation characterization/gap recomputation;
- direct actor-surface usability observation (AC-010);
- separate stakeholder `continue | change | stop` observation receipt (AC-011).

Automated checks may support AC-010/011 but cannot substitute for direct stakeholder observation.

## Permitted D1 probes

D1 may use a disposable, clearly non-authoritative mock/prototype only when a decision cannot be made responsibly from existing evidence—for example, comparing whether a CLI versus local HTML surface makes the same repository-context artifact materially easier to judge.

A D1 probe must have:

- one explicit question;
- the smallest representative input;
- a decision-changing readout;
- a stop condition;
- no production-authority claim;
- cleanup/quarantine or explicit promotion path.

A probe that starts accumulating reusable product infrastructure is D1 failure and triggers replan.

## Required D1 outputs

D1 closes only when Plan 001 can be updated with all of the following:

```text
exact data-contracts consumer revision
contract disposition + exact owner/reference
selected Slice 1 actor surface + rationale
selected provider/dependency bindings
exact implementation subjects/paths
exact verification subjects/paths
explicit residual AES semantics
explicit rejected/generalized non-goals
```

Then update the existing authorities/projections as needed:

- Plan 001 concrete topology;
- `.agentic/relationships.yaml`;
- `.agentic/repo.yaml` implementation/verification roots if they have become concrete;
- `wiki/index.md` current/next-depth projection.

Do not mark implementation as realized merely because paths are planned.

## D1 exit test

A fresh implementation agent should be able to answer, without making a new product/architecture decision:

- What exact user-visible outcome am I building?
- Through what authentic entrypoint will it be used?
- Which exact contract/model owns the result shape?
- Which code subjects may I create/change?
- Which existing providers/dependencies must I use?
- What residual semantics are AES-local and why?
- Which exact checks/observations establish each criterion?
- What failure/recovery behavior must be observed?
- What must I explicitly not generalize?

If any answer still requires choosing product semantics, authority ownership, a provider strategy, or a frontend architecture, D1 is not closed.

## Handoff after D1

When the exit test passes:

```text
D1 CLOSED
   ↓
Plan 001 topology frozen
   ↓
Enforced Planning execution contract
   ↓
Slice 1 TDD / governed implementation
   ↓
authentic actor surface
   ↓
Attention Checkpoint A1
```

D1 itself never closes the originating AES gaps. Only implementation, fresh evidence, direct utility observation where required, re-characterization, and gap recomputation can do that.
