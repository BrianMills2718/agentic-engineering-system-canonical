# Plan 001 / R1 — Substantive repository-context replan

Status: **REPLAN REQUIRED — no replacement implementation authorized yet**
Parent plan: `001_repository_context_resolution_vertical.md`
Trigger evidence: `evidence/plan-001/a1/821d00766b0caed658faf4c816521560a6ccada0.md`
Canonical consumer remains: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`

## Why this record exists

Plan 001 / Slice 1 successfully demonstrated exact-revision routing, evidence binding, honest unknown-state handling, and a bounded static projection. It did **not** demonstrate a useful repository-context experience.

Two direct stakeholder observations found the surface too sparse. The second review made the failure mode explicit: the surface named authoritative paths but did not actually convey substantive repository information.

The parent plan's stop/replan condition is therefore active. This record does not reopen the technical evidence already learned; it redefines the unresolved actor outcome before more implementation is attempted.

## Observed gap

The current `RepositoryContextArtifact` can say:

- which file is the local entrypoint;
- which path carries implementation/contract/ownership authority;
- what must not be inferred;
- which exact source/revision supports those routing claims.

It cannot carry enough substantive context to answer basic newcomer questions such as:

- what the repository is for;
- what capabilities it owns;
- what it explicitly does not own;
- what public/package surfaces matter;
- how a new actor should read or work in the repo;
- what checks/commands matter;
- what ecosystem relationships or consumers are stated;
- what important uncertainties remain.

This is a contract-level information gap, not a CSS/layout problem.

## Evidence that bounded native sources are sufficient to investigate

The pinned `data-contracts` consumer already exposes rich bounded native context in sources that the parent plan allowed the legacy adapter to inspect:

### `README.md`

It explicitly states, among other things:

- repository role: shared typed boundary/validation substrate for cross-project boundaries;
- core owned surfaces: strict/permissive boundary models, `@boundary`, compatibility checks, registry/CLI, composition contracts/validators, governed lifecycle contracts;
- explicit non-ownership: project semantics, provider discovery/dispatch, planner policy, persistence, workflow runtime and canonical semantic builds;
- suggested reading order;
- package surface and quick-start behavior;
- known consumers;
- local verification commands and repository navigation.

### `docs/ops/CAPABILITY_DECOMPOSITION.md`

It explicitly states:

- what `data_contracts` owns;
- what it does not own;
- capability ownership/posture decisions;
- boundary rules;
- maintained consumers;
- open uncertainties.

The immediate problem is therefore not a need for broad repository crawling. It is that the current artifact contract reduces allowed source content to routing metadata and throws away the information a human actually needs.

## Replanned actor outcome

A person or agent entering an unfamiliar governed repository should receive a directly useful, source-bound context surface that can answer **before opening raw source**:

1. **Repository role** — what is this repository for?
2. **Owned responsibilities** — what capabilities/semantics does it own?
3. **Explicit exclusions** — what does it not own, and where do those responsibilities stay?
4. **Primary surfaces** — what are the main package/API/CLI/document surfaces that matter?
5. **Navigation/read order** — where should a newcomer deepen next and in what order?
6. **Safe-work commands** — what repository-native checks/commands are stated for validation or operation?
7. **Ecosystem relationships** — which consumers/dependencies/upstream owners are explicitly stated and relevant to orientation?
8. **Open uncertainties/cautions** — what remains unsettled or must not be inferred?
9. **Provenance** — which exact revision-bound native sources support each substantive claim?

The surface may still link to native sources for depth, but it must not require the actor to reconstruct these answers from those sources.

## Minimum information shape to evaluate

Do not freeze a replacement schema yet. The replan should evaluate a minimal provider-neutral information family along these lines:

- `RepositoryRoleObservation`
  - summary / evidence refs
- `ResponsibilityObservation`
  - owned vs explicitly-not-owned / subject / summary / evidence refs
- `CapabilityObservation`
  - named capability/surface / posture or role when explicitly stated / evidence refs
- `NavigationStepObservation`
  - ordered step / purpose / location / evidence refs
- `CommandObservation`
  - command / purpose / evidence refs
- `RelationshipObservation`
  - related repo/system / relationship type as explicitly stated / evidence refs
- `UncertaintyObservation`
  - issue/caution / state / evidence refs

This is a planning hypothesis, not an authorized shared schema. Prefer the smallest local residual contract that proves the human outcome.

## Bounded-source posture

Preserve the strongest lesson from Slice 1: do not infer semantics from plausible folder names.

For a legacy repository without an authoritative context manifest, the next experiment should remain bounded to explicit sources such as:

1. exact Git identity/revision;
2. root context/navigation docs;
3. directly referenced ownership/capability docs;
4. package metadata where it supplies explicit package identity/surface facts;
5. explicit commands/read-order/consumer/boundary statements in those sources.

Do **not** respond to this A1 failure by immediately adding a generalized crawler, symbol index, graph store, code map, or repository-wide semantic scan.

## Semantic extraction problem

The replan must distinguish **finding sources** from **understanding source content**.

Slice 1 solved bounded source finding/routing. The new missing capability is extraction/composition of substantive repository context from explicit native prose and structured metadata.

Before implementing that residual capability, run proportionate ACA/provider discovery. Evaluate at least these classes without preselecting one:

- deterministic Markdown/metadata extraction where native structure is explicit enough;
- an existing reusable semantic-document extraction/summarization provider;
- an LLM-backed bounded summarization provider with exact source/provenance constraints;
- Representation Router only if the demonstrated requirement is genuinely representation selection/composition rather than semantic content extraction itself.

Representation Router is **not selected** by this replan merely because related human-presentation work exists elsewhere.

## Important design distinction

The missing information is not mainly a rendering problem.

A better card layout cannot compensate for an artifact that contains only paths. The next slice must ensure substantive, evidence-backed information exists **before** presentation concerns are optimized.

Presentation/routing can then decide how that information is progressively disclosed to a human.

## Proposed next discriminating probe

Before freezing a replacement implementation contract:

1. use only the pinned consumer's `README.md`, `docs/ops/CAPABILITY_DECOMPOSITION.md`, and package metadata;
2. produce a source-bound candidate context containing the nine actor-answer categories above;
3. retain exact evidence refs for every substantive claim;
4. show that candidate directly to the stakeholder;
5. determine whether the information content is finally useful before selecting generalized infrastructure.

This probe may be produced manually or with a temporary research harness for planning evidence. It is **not** yet the production Slice 1 replacement.

## Stop conditions for the replan

Stop and escalate rather than forcing a local parser if:

- useful context cannot be extracted from bounded explicit sources without repository-name-specific prose rules;
- deterministic Markdown structure is too inconsistent to support the actor outcome;
- a semantic provider is required but no acceptable provenance-bound provider can be selected;
- the actor outcome expands into full repository characterization/code understanding rather than bounded orientation;
- stakeholder feedback shows even the substantive candidate context is not valuable.

## Current decision boundary

Until this replan is resolved:

- PR #5 remains open and unmerged;
- Plan 001 / Slice 1 is not delivered;
- no gap closure is claimed;
- no next vertical is derived;
- no Representation Router/Data Contracts/Code Map dependency is selected;
- further cosmetic iteration on the old routing-only HTML is out of scope.
