# Fresh-agent handoff — AES canonical

Date: 2026-09-17

Status: operational handoff / synthesis, not normative authority.

## Start here

A fresh agent should read this file first, then inspect the **live** state of PR #6
and PR #5 before acting.

Do not infer merge approval from this handoff. Brian delegated high-confidence,
reversible architecture cleanup, but merge remains an explicit protected action.

## Repository state at handoff

Repository: `BrianMills2718/agentic-engineering-system-canonical`

`main` observed at:

`91a04441b0df8ee73b6d749b1edd44949566e9f2`

### PR #6 — architecture/bootstrap line

Title: **Bootstrap component-aligned AES architecture and external sourcing**

Branch: `bootstrap/external-sourcing-audit`

Observed head before this handoff file was added:

`b1c87e9a075a3fbd4aee2e11af0fdcda7eaf6e66`

State at observation: **open, mergeable, unmerged**.

Purpose:

- external/OSS sourcing research;
- dogfood of normative/code alignment;
- accepted-on-merge architecture decisions 0002–0006;
- compact system/component normative model;
- AES Company Planning profile;
- minimal architecture-realization JSON Schema;
- physically reserved component/test homes without fake APIs/tests.

The live PR head will be newer than the SHA above because this handoff is itself a
PR #6 commit. Always re-read the live PR before integration.

### PR #5 — Plan 001 / Slice 1 implementation line

Title: **Implement Slice 1 repository context resolution**

Branch: `slice-1/repository-context`

Observed head:

`9f82f3500e4a472b26756c31ea9205f908d7c394`

State at observation: **open, mergeable, unmerged**.

This is the sole active Repository Context implementation line.

It contains the technical implementation and prior technical execution evidence.
Plan 001 is **not delivered** because A1 human-facing review/presentation remains
pending in the separate Representation Router workstream.

Do not restart presentation work here.

### PR #4

Already closed and explicitly superseded by PR #5.

## Integration hygiene

At handoff, PR #5 changed **165 files** and PR #6 changed **59 files**, with
**zero changed-file overlap**.

That is a useful current observation, not a guarantee about future edits.

If Brian later explicitly approves adoption/merge, the low-risk conceptual order is:

1. merge/adopt PR #6 first so the architecture/bootstrap decisions become canonical;
2. refresh/review PR #5 against the new `main`;
3. re-run the applicable PR #5 verification at its exact refreshed head;
4. merge PR #5 only with separate explicit merge approval.

Do not assume step 1 authorizes step 4.

## Bootstrap architecture state

The bootstrap design phase is closed enough to stop meta-design.

All twelve AQRs in
`docs/architecture/normative-component-alignment.bootstrap.yaml`
are resolved to explicit decisions.

Important decisions:

- `0002-company-planning-aes-profile-before-fork.md`
  - use an AES-local profile over Company Planning;
  - do not fork Company Planning now;
  - do not add AES-specific fields to generic `DesignPacketResult`.

- `0003-component-local-normative-context-and-symbol-inheritance.md`
  - Component is the default governed implementation boundary;
  - symbols inherit component context, not component conformance;
  - split on semantic/ownership/interface/verification boundaries, not arbitrary size.

- `0004-compact-structured-normative-records-and-generated-views.md`
  - target model is compact **system + component** structured normative records;
  - PRD, requirements, journeys, architecture/component maps, AQR views, wiki,
    and source-local context are generated views by default;
  - existing accepted Markdown remains authority until an explicit atomic migration.

- `0005-aes-component-scope-and-consequential-seam-typing.md`
  - AES Component is a planning/governance concept, not a microservice or universal
    Backstage/TOSCA/SysML identity;
  - freeze consequential seams before independent implementation;
  - do not predeclare private helper signatures or provider-specific APIs before provider selection.

- `0006-minimal-architecture-realization-json-schema.md`
  - YAML-compatible architecture-realization data is validated by JSON Schema 2020-12;
  - AES adds only small residual cross-reference checks;
  - do not duplicate generic capability/workflow/policy/provenance/API/symbol models.

Decision 0001 remains the canonical convergence boundary.

## Current machine-readable entrypoints

Read these, in this order:

1. `docs/architecture/normative-component-alignment.bootstrap.yaml`
   - resolved bootstrap design record and next dogfood gate.

2. `docs/architecture/normative-record-model.bootstrap.yaml`
   - accepted bootstrap system/component normative model.

3. `docs/architecture/aes-company-planning-profile.bootstrap.yaml`
   - AES-local profile over Company Planning.

4. `docs/architecture/schemas/architecture-realization.bootstrap.schema.json`
   - minimal architecture-realization schema.

5. `generated/bootstrap-normative/architecture-realization.minimal.pilot.yaml`
   - nine-component/four-seam generated pilot projection;
   - **not normative authority**.

The older
`docs/architecture/architecture-realization.bootstrap.yaml`
is explicitly superseded research history, not the forward contract.

## Reserved component topology

PR #6 physically reserves these component homes:

- `normative_context`
- `capability_sourcing`
- `planning`
- `execution`
- `policy_control`
- `evidence_assessment`
- `gap_reconciliation`
- `learning`

Each unresolved source component contains only
`component.placeholder.yaml`.

Each corresponding test home contains only
`verification.placeholder.yaml`.

Do **not** interpret placeholders as implementation, APIs, tests, or verification.
Do not add passing placeholder tests or invented class/function signatures just to
fill the tree.

Repository Context is different: its real code exists on PR #5.

## Dogfood evidence worth knowing

### Source-local context

`evidence/bootstrap-alignment/repository-context-source-local-observation-001.json`

The first generated local context accidentally paraphrased AC-003. Exact-source
checking caught it and the text was corrected.

This is important evidence that local normative context should be **verbatim
generated projection**, not hand-maintained summaries.

The same pilot showed that injecting every global clause into every source
location is too noisy. Current direction is explicit applicability:

- direct component norms;
- incident seam/context-delivery norms;
- outcome context;
- condition-triggered repository norms;
- active plan criteria;
- current/gap state.

### Documentation without explosion

`evidence/bootstrap-alignment/normative-record-view-dogfood-001.json`

One structured projection generated PRD-style, journey, requirements,
architecture/component and AQR views without separately authored normative text.

### Company Planning fit

`evidence/bootstrap-alignment/company-planning-profile-conformance-001.json`

Current evidence supports an AES profile, not a Company Planning fork.

### Architecture-realization schema

`evidence/bootstrap-alignment/architecture-realization-schema-observation-001.json`

The exact committed Draft 2020-12 schema and exact nine-component/four-seam pilot
were validated. Negative controls also covered unresolved-without-blocker,
unknown fields, mutable revisions, missing disproof, unsafe paths, duplicate
component IDs and broken seam references.

Structural validity is not semantic/provider/runtime conformance.

## External-first sourcing result

Research looked at:

- JSON Schema / OpenAPI / AsyncAPI;
- Backstage;
- TOSCA 2.0;
- SysML v2 / KerML;
- Open Workflow Specification;
- OPA/Rego;
- W3C PROV;
- in-toto / SLSA;
- SCIP.

Internal systems such as Data Contracts, Company Planning, Enforced Planning, ACA,
Representation Router and predecessor AES repos are donors/candidates, not defaults.

Do not create generic AES-local copies of Capability, Workflow/Task, PolicyEngine,
ProvenanceGraph, API/schema language, or Symbol identity without new evidence.

The OPA/TOSCA/PROV mappings on PR #6 are conceptual fit probes, not executed
provider-conformance results.

## Plan 001 boundary

`data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`
is a pinned, read-only external consumer.

It is not the AES product and is not being migrated into AES format.

PR #5 technical implementation exists, but:

- do not mark Slice 1 delivered;
- do not close originating gaps from plan completion;
- do not treat A1 presentation feedback as a data-contracts substantive replan;
- do not add Representation Router/Data Contracts/Code Map as runtime dependencies
  merely because related work exists.

## What the next fresh agent should do

### Before any code or architecture work

1. Fetch live PR #6 and PR #5 state.
2. Verify their current heads and changed-file overlap.
3. Read PR #6's current body and decisions 0002–0006.
4. Read PR #5's body and exact current Plan 001 status.
5. Preserve the no-merge-without-explicit-approval boundary.

### If PR #6 has not been explicitly approved for merge

Do not manufacture more meta-architecture simply to stay busy.

The meaningful protected frontier is adoption of the bootstrap architecture.
Further work should be limited to corrections discovered by review or genuinely
new evidence.

### After PR #6 is explicitly adopted

Use the accepted AES Company Planning profile and the versioned
architecture-realization schema on the **next real component-specific design from
an actual gap**.

Do not reopen the bootstrap schema questions unless real dogfood falsifies a
decision.

### PR #5 remains separate

After architecture adoption, refresh PR #5 against the new base and re-observe
the relevant technical checks before asking for its own merge approval.

A1 remains separately handled through the Representation Router workstream.

## User working preference / authority note

Brian has authorized high-confidence reversible work to proceed without routine
approval. Ask when a real semantic/authority choice is required.

This does **not** include implicit permission to merge PRs.
