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

Disposition: **no ACA-verified provider found**.

## Relationship to external sourcing

ACA discovery is only one part of provider selection. The canonical AES sourcing rule now checks stable platform, standard, mature OSS/service options before treating internal bespoke code as the default provider.

That separate landscape is recorded in `2026-09-16-repository-context-provider-landscape.md`. It found useful substrate but no complete provider for the AES authority-resolution boundary.

Current capability disposition: **compose native/off-the-shelf substrate + bounded residual AES semantics**.

This is not permission to immediately create a generalized shared package. Internal repositories remain evidence/design donors unless a positive runtime-provider decision selects them.

## Consumer-specific evidence

`data-contracts` already demonstrates why this capability matters:

- its canonical typed contract surfaces live primarily under `src/data_contracts/`;
- its root `contracts/` directory is not the universal contract authority;
- its README is currently the local repository entrypoint while global navigation lives in the Vision wiki;
- its current navigation still advertises legacy top-level roots including `ui/` and `misc/`.

A resolver that assumes `contracts/` owns contracts, assumes `wiki/index.md` already exists, or assumes every repo has the same implementation root would misroute an agent.

## Planning consequence

The first vertical must prove semantic routing from declared/adopted repository context rather than folder-name heuristics. Company Planning must derive the smallest outcome-bearing vertical separately from the gap list or any dependency graph. Concrete code topology remains unresolved until dependency subplan D1 freezes the contract and exact implementation/verification subjects.