# First vertical capability discovery

Date: 2026-09-16
Status: current investigation

## Question

For the first external AES dogfood vertical, does ACA already expose a verified semantic action that resolves a governed repository's local context, authority surfaces, and navigation entrypoint?

## Consumer

`BrianMills2718/data-contracts`

## Required behavior

Given a governed repository, resolve enough machine-readable and human-readable context to answer:

- where is the repository navigation entrypoint?
- which roots own normative, decision, plan, implementation, verification, and contract authority?
- which concern roots are available?
- which native contract surfaces must not be relocated or duplicated?
- what current concern/gap should the agent deepen into next?

Candidate semantic identity: `repository.context.resolve`.

This name is provisional until ACA accepts or rejects it.

## ACA discovery

Search of the current ACA canonical repository found no verified semantic export matching repository/context resolution.

The current charter emphasizes narrow semantic action identities and currently audited actions such as `approval.resolve`, `availability.query`, `state.transition.plan`, and `notification.email.send`.

Disposition: **no incumbent verified provider found**.

## Residual classification

`repository.context.resolve` is therefore a residual capability requirement for the first vertical, not permission to immediately implement a new shared package.

Company Planning must decide the smallest implementation boundary needed for the vertical. The first implementation may be AES-local if that is the smallest honest seam. Promotion into ACA as a reusable capability requires an explicit semantic action contract, provider binding, evidence, and later reuse/disposition.

## Consumer-specific evidence

`data-contracts` already demonstrates why this capability matters:

- its canonical typed contract surfaces live primarily under `src/data_contracts/`;
- its root `contracts/` directory is not the universal contract authority;
- its README is currently the local repository entrypoint while global navigation lives in the Vision wiki;
- its current navigation still advertises legacy top-level roots including `ui/` and `misc/`.

A resolver that assumes `contracts/` owns contracts, assumes `wiki/index.md` already exists, or assumes every repo has the same implementation root would misroute an agent.

## Planning consequence

The first vertical must prove semantic routing from declared/adopted repository context rather than folder-name heuristics. Any code topology remains unresolved until the plan derives the narrowest mechanism and verification subjects.