# Agentic Engineering System — canonical development wiki

This is the progressive-disclosure front door for the canonical AES convergence project. It is a derived navigation surface, not a native authority. Follow links to the owning architecture, decision, plan, evidence, or code before making consequential claims.

## Current orientation

**Target**

One coherent human+agent engineering lifecycle:

```text
orient -> target -> current -> gap -> plan -> capability composition
       -> governed execution -> evidence -> characterization -> gap reconciliation
       -> learning / policy or capability improvement
```

The lifecycle must preserve native authority, honest unknown/error states, direct stakeholder utility evidence, and fresh post-implementation characterization rather than equating plan completion with conformance.

**Current**

The component-aligned bootstrap architecture is established:

- Decisions 0001–0006 define the convergence boundary, Company Planning profile strategy, component/context rules, compact normative-record direction, consequential-seam typing, and the minimal architecture-realization contract.
- All twelve bootstrap architecture questions in `normative-component-alignment.bootstrap.yaml` are resolved to explicit decisions.
- The AES Company Planning profile targets the versioned minimal architecture-realization schema without changing generic `DesignPacketResult`.
- Reserved component and verification homes express intended topology only; placeholders are not implementation, tests, or evidence.
- Existing accepted Markdown remains normative authority until an explicit single-authority migration.
- Generated bootstrap projections remain non-authoritative dogfood/probe artifacts.

Plan 001 / Repository Context implementation exists on the separate `slice-1/repository-context` line (PR #5). That line has recorded technical execution and an initial A1 utility disposition of `change`, but it is not part of canonical `main` until separately refreshed, reviewed, and merged. Delivery and originating-gap closure remain unclaimed.

**Gap**

The integrated AES lifecycle is not yet demonstrated end to end on canonical `main`. In particular:

- the PR #5 implementation has not yet been refreshed onto the adopted bootstrap architecture;
- its corrected human-facing presentation still requires follow-up direct utility review through the separate Representation Router workstream;
- fresh revision-bound characterization and explicit gap recomputation remain pending;
- later components must be derived from real gaps rather than from the presence of reserved directories.

**Next**

```text
adopt bootstrap architecture on main
        ↓
refresh PR #5 against the adopted base
        ↓
re-run applicable technical/regression checks at the exact refreshed head
        ↓
keep pinned private data-contracts acceptance separate from hosted regression CI
        ↓
obtain follow-up direct utility observation when the corrected presentation is reviewable
        ↓
characterize the exact implementation revision
        ↓
recompute originating gaps
        ↓
derive the next real component-specific design from the resulting gap state
```

PR #5 still requires its own explicit merge decision.

## Read in this order

1. [`../docs/architecture/SYSTEM_BOUNDARY.md`](../docs/architecture/SYSTEM_BOUNDARY.md) — canonical AES target clauses and subsystem boundaries.
2. [`../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md) — delivery, direct-use, uncertainty, feasibility, and attention-economics rules.
3. [`../docs/architecture/README.md`](../docs/architecture/README.md) — architecture navigation, authority boundaries, and machine-readable bootstrap entrypoints.
4. [`../docs/architecture/normative-component-alignment.bootstrap.yaml`](../docs/architecture/normative-component-alignment.bootstrap.yaml) — resolved bootstrap design record and next dogfood gate.
5. [`../docs/architecture/aes-company-planning-profile.bootstrap.yaml`](../docs/architecture/aes-company-planning-profile.bootstrap.yaml) — AES-local planning profile and reproducible bootstrap checks.
6. [`../docs/architecture/schemas/architecture-realization.bootstrap.schema.json`](../docs/architecture/schemas/architecture-realization.bootstrap.schema.json) — minimal architecture-realization contract.
7. [`../docs/plans/001_repository_context_resolution_vertical.md`](../docs/plans/001_repository_context_resolution_vertical.md) — Plan 001 execution contract. On canonical `main`, treat implementation-state claims in the separate PR #5 branch as branch-local until integrated.
8. [`../docs/decisions/0001-canonical-convergence-boundary.md`](../docs/decisions/0001-canonical-convergence-boundary.md) through [`../docs/decisions/0006-minimal-architecture-realization-json-schema.md`](../docs/decisions/0006-minimal-architecture-realization-json-schema.md) — accepted architecture decisions and rationale.

## Authority rules that matter most

- One mutable fact has one owning authority or is explicitly a derived projection.
- Planning proposes and structures change; it does not manufacture current state or close gaps.
- Existing providers remain authoritative until an evidence-backed disposition changes that.
- External standards/OSS/providers are considered before bespoke local implementations when they plausibly fit.
- Native typed contracts remain with their natural authorities.
- Component-local context may repeat normative wording only as a generated, source-identified projection.
- Structural validity is not provider conformance, runtime verification, stakeholder utility, or gap closure.
- A completed plan is not evidence that the target is satisfied.

## Bootstrap architecture in one picture

```text
accepted AES intent + real gaps
        ↓
Company Planning + AES profile
        ↓
project-local architecture-realization record
        ↓
versioned JSON Schema + bounded AES cross-reference checks
        ↓
component responsibilities + provider disposition
+ implementation homes + consequential seams
+ verification obligations/disproof
        ↓
separately governed implementation
        ↓
observed evidence + direct use
        ↓
fresh characterization + gap reconciliation
```

The generated nine-component/four-seam bootstrap record demonstrates the contract shape only. It is not a backlog, current architecture authority, or proof that every reserved component should be implemented.

## First external consumer / Plan 001 boundary

`BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` remains the pinned, read-only first external consumer for Repository Context.

Do not:

- migrate `data-contracts` into AES format merely to satisfy the pilot;
- infer semantic authority from folder names;
- treat the private pinned-consumer check as satisfied by hosted regression CI that lacks `AES_DATA_CONTRACTS_CHECKOUT`;
- turn Representation Router into an AES runtime dependency merely because it is handling the follow-up presentation work;
- derive the next implementation vertical before fresh characterization/gap recomputation authorizes it.

## Provider and donor posture

- Company Planning — planning/design provider through the AES-local profile.
- Enforced Planning — execution-governance incumbent/provider.
- Agentic Capability Architecture — capability/provider-resolution incumbent.
- Data Contracts — shared typed-boundary authority where provider-neutral semantics fit; not automatically an AES runtime dependency.
- Representation Router — concern-specific working-surface provider candidate/workstream; no authority transfer implied.
- Backstage, TOSCA, SysML v2/KerML, Open Workflow Specification, OPA/Rego, W3C PROV, in-toto/SLSA, SCIP, Code Map, predecessor AES repositories, and other donors remain concern-specific references/candidates unless positively selected by a real design.

Nothing becomes a runtime dependency merely because it appears in research or can model part of AES.
