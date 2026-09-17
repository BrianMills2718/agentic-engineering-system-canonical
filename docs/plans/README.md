# Plans

Status: one active pilot plan; D1 closed; Slice 1 implementation partial; **A1 stop/replan triggered**.

## Active

- [`001_repository_context_resolution_vertical.md`](001_repository_context_resolution_vertical.md) — Plan 001 / first external-consumer vertical. Its routing/evidence implementation exists on `slice-1/repository-context` / PR #5, but delivery is not claimed.
- [`001_R1_substantive_repository_context_replan.md`](001_R1_substantive_repository_context_replan.md) — **active replan record** after two A1 observations showed the routing-only surface was materially too sparse.
- [`001_D1_contract_surface_topology_freeze.md`](001_D1_contract_surface_topology_freeze.md) — **closed** subordinate D1 record. It is not a second plan.

## Current state

The repository remains implementation/verification **PARTIAL**.

- frozen external consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`;
- implemented actor surface: `aes-repo-context` -> revision-scoped `context.json` + static `index.html`;
- demonstrated strengths: exact-revision binding, positive routing evidence, honest `NONE`/`ERROR`/`UNRESOLVED`, bounded legacy source discovery, deterministic static projection;
- demonstrated utility failure: the artifact/projection identifies authoritative paths but does not carry enough substantive repository information for a newcomer to understand what the repository is, owns, excludes, exposes, or how to work in it;
- second direct A1 disposition: **change / stop-replan**;
- selected substrate remains local Git + Pydantic 2.13.5 + PyYAML 6.0.3 + Python stdlib;
- Data Contracts, Representation Router, Code Map V4, and predecessor AES systems remain unselected as runtime dependencies.

## Immediate frontier

Do **not** continue cosmetic iteration on the old routing-only projection.

The next work is the replan discriminating probe:

```text
bounded explicit native sources
        ↓
substantive repository context
(role / owns / does-not-own / capabilities / read order / commands / relationships / uncertainties)
        ↓
exact evidence binding
        ↓
one directly informative working surface
        ↓
stakeholder utility observation
        ↓
provider/schema decision only if the information direction is useful
```

Use the pinned consumer's explicit README, ownership/capability document, and package metadata first. Do not jump to generalized crawling, a graph store, Code Map, or Representation Router unless the replan demonstrates an actual missing capability that requires one.

## Closure discipline

Plan 001 is **not delivered**. PR #5 must remain unmerged until a replacement actor outcome is planned and authentically observed.

No originating gap closes merely because the routing implementation works technically. Fresh characterization/gap recomputation remains downstream of an adequate substantive-context experience and its technical evidence.
