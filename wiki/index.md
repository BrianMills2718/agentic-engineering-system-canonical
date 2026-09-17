# Agentic Engineering System — canonical development wiki

This is the progressive-disclosure front door for the canonical AES convergence project. It is a derived navigation/synthesis surface, not a native authority.

## Current orientation

**Target:** one coherent engineering system in which accepted intent produces explicit gaps; Company Planning converts those gaps plus actor outcome, maturity, uncertainty, provider sourcing, feasibility and dependency constraints into coherent human-observable implementation slices; ACA resolves reusable capabilities; Enforced Planning governs execution; policy keeps work aligned with recovery/change paths; evidence and direct stakeholder observation re-characterize the result; gaps are recomputed; and useful observations strengthen future capability, policy and planning knowledge.

**Current:** bootstrap architecture and repository protocol are realized. Plan 001 is implementation-ready. D1 is closed and has frozen the exact external consumer revision, AES-local contract ownership, Git/Pydantic/PyYAML dependency set, static HTML + CLI actor surface, concrete implementation paths, concrete verification paths, and legacy/manifest precedence semantics. No implementation subject exists yet; the repository remains `planned_unrealized`.

**Gap:** the integrated lifecycle remains unrealized. The planning and sourcing decisions are concrete, but no Slice 1 code, authentic working surface, policy block/recovery receipt, external execution evidence, stakeholder utility observation, or fresh post-implementation characterization exists yet.

**Plan:** implement Plan 001 / Slice 1 against `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`. Enforced Planning should govern the frozen execution contract. The actor uses `aes-repo-context` to produce a revision-scoped `context.json` plus static `index.html`; automated evidence and Attention Checkpoint A1 remain separate dimensions before fresh gap recomputation.

## Read in this order

1. [`../docs/architecture/SYSTEM_BOUNDARY.md`](../docs/architecture/SYSTEM_BOUNDARY.md) — AES-specific normative system boundary.
2. [`../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`](../docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md) — human-observable slices, experience-backward design, feasibility probes, utility/conformance separation and attention economics.
3. [`../docs/architecture/INITIAL_GAP_LEDGER.md`](../docs/architecture/INITIAL_GAP_LEDGER.md) — current target/current variance after D1 closure.
4. [`../docs/plans/001_repository_context_resolution_vertical.md`](../docs/plans/001_repository_context_resolution_vertical.md) — implementation-ready Slice 1 execution contract and A1.
5. [`../docs/plans/001_D1_contract_surface_topology_freeze.md`](../docs/plans/001_D1_contract_surface_topology_freeze.md) — closed D1 decision record and exact frozen topology.
6. [`../research/investigations/2026-09-16-repository-context-provider-landscape.md`](../research/investigations/2026-09-16-repository-context-provider-landscape.md) — external provider search and residual-semantics conclusion.
7. [`../research/investigations/2026-09-16-first-vertical-capability-discovery.md`](../research/investigations/2026-09-16-first-vertical-capability-discovery.md) — ACA discovery result.
8. [`../research/synthesis/incumbent-capability-inventory.md`](../research/synthesis/incumbent-capability-inventory.md) — donor versus runtime-provider inventory.
9. [`../docs/decisions/0001-canonical-convergence-boundary.md`](../docs/decisions/0001-canonical-convergence-boundary.md) — canonical convergence boundary.
10. Standalone methodology: `BrianMills2718/wiki_methodology@0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`, `docs/architecture/README.md`.

## Concern snapshot

### Planning and delivery
Target: gap-backed planning where Company Planning derives risk-ordered human-observable vertical slices and Enforced Planning governs their execution.
Current: D1 is closed. Slice 1 has a frozen actor outcome, static HTML/CLI surface, contract semantics, exact code/test paths, provider bindings and stop/replan conditions.
Gap: the slice has not executed, so the planning method is not yet evidenced by a working human-observable vertical.
Next depth: `docs/plans/001_repository_context_resolution_vertical.md`.

### Human/agent working surfaces
Target: planning, coding and review are made tractable through the smallest concern-specific source-bound representation that lets a human or agent act without reconstructing the system from dialogue, code and prose.
Current: Slice 1 selects a low-lock-in static HTML projection generated from one typed artifact. Representation Router remains unselected because this slice does not require representation routing/composition.
Gap: the working surface has not yet been implemented or used.
Next depth: Plan 001 AC-010 / AC-011 and `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`.

### Capability composition and sourcing
Target: external/native substrate first, ACA capability knowledge, internal donors only by positive selection, local code only for demonstrated residual semantics.
Current: `repository.context.resolve` is frozen as Git + Pydantic 2.13.5 + PyYAML 6.0.3 + Python stdlib + bounded AES authority-resolution semantics. Data Contracts and Representation Router were reviewed but not selected as runtime dependencies.
Gap: the selected bindings have not yet been exercised through implementation.
Next depth: D1 record and provider-landscape investigation.

### Contract and implementation topology
Target: one natural owner per mutable fact, no parallel schema authority, and concrete target topology before coding.
Current: `RepositoryContextArtifact` is AES-local under `src/agentic_engineering_system/repository_context/models.py`; planned implementation root is `src/agentic_engineering_system/`; planned verification root is `tests/repository_context/`.
Gap: target paths exist only as planning declarations; source implementation is absent.
Next depth: Plan 001 frozen topology.

### Economics and autonomy
Target: AI autonomy multiplies scarce human judgment rather than postponing it.
Current: D1 consumed no standing stakeholder checkpoint and returned directly to the implementation frontier; A1 is positioned after the first usable outcome.
Gap: no execution evidence yet shows whether this sequencing reduces reconstruction cost or utility-discovery latency.
Next depth: `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md`.

### Policy
Target: adaptive controls with honest epistemic state, recovery/escalation, negative controls, and evidence-bearing transitions.
Current: malformed authoritative manifests are planned to block rather than fall back; AC-006/007/008 freeze negative/error/recovery semantics.
Gap: no live block/recovery transition has occurred.
Next depth: Plan 001 AC-006 through AC-008.

### Documentation and context
Target: concern-centric progressive disclosure over native authorities, with source-local target/current/gap/plan context once implementation subjects exist.
Current: wiki, machine contract, architecture, gap ledger and plans agree on the Slice 1 frontier.
Gap: no realized implementation subject exists, so source-local generated context remains not yet applicable.
Next depth: Plan 001 Slice 1.

## First external consumer

`BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0` is the frozen first consumer. Its README explicitly remains the local repository entrypoint, its `pyproject.toml` declares packages under `src`, and `docs/ops/CAPABILITY_DECOMPOSITION.md` is the repo-local ownership record. Root `contracts/` is not treated as repository-wide authority by folder name.

Plan 001 is read-only with respect to `data-contracts`; migration remains out of scope.

## Donor and incumbent sources

- Company Planning — current planning/design provider.
- Enforced Planning — current execution-governance provider.
- Agentic Capability Architecture — capability-plane authority/incumbent.
- Data Contracts — typed-boundary/composition authority where shared semantics match; reviewed and intentionally unselected as a Slice 1 runtime dependency.
- Representation Router — working-surface donor/future provider candidate; unselected for Slice 1.
- Project Meta — policy/control evidence and ecosystem-policy authority where applicable.
- `Inside-Success/agentic-engineering-system` — predecessor evidence/design donor; no dependency by default.
- `BrianMills2718/aes` — archived predecessor donor.
- `BrianMills2718/code_map_v4` — characterization/evidence donor; provider unselected.
- AC16/AC17 — method/evidence donors; not runtime architecture.
- Fluid Governance — typed recovery/receipt donor; not execution authority.

Nothing becomes a runtime dependency merely by appearing in this list.
