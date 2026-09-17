# Plans

Status: one active pilot plan; D1 closed; Slice 1 implementation partial; A1 pending.

## Active

- [`001_repository_context_resolution_vertical.md`](001_repository_context_resolution_vertical.md) — Plan 001 / first external-consumer vertical. The implementation exists on `slice-1/repository-context` / PR #5, but delivery is not yet claimed.
- [`001_D1_contract_surface_topology_freeze.md`](001_D1_contract_surface_topology_freeze.md) — **closed** subordinate D1 record. It is not a second plan.

## Current state

The repository is no longer `planned_unrealized`.

- implementation state: **PARTIAL**;
- verification state: **PARTIAL**;
- frozen external consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`;
- active actor surface: `aes-repo-context` -> revision-scoped `context.json` + static `index.html`;
- selected substrate: local Git + Pydantic 2.13.5 + PyYAML 6.0.3 + Python stdlib;
- Data Contracts, Representation Router, Code Map V4, and predecessor AES systems remain unselected as Slice 1 runtime dependencies;
- direct stakeholder utility at A1 remains separate from technical/evidence conformance.

## Immediate frontier

The next work is to **characterize the implemented slice through authentic execution**, not broaden the architecture.

```text
current Slice 1 implementation
        ↓
local governed-repo install / audit
        ↓
focused automated checks
        ↓
pinned data-contracts external execution
        ↓
generated context.json + index.html
        ↓
Attention Checkpoint A1: continue | change | stop
        ↓
revision-bound characterization
        ↓
fresh gap recomputation
```

Before A1, do not generalize into repository indexing, a characterization platform, Representation Router, a graph store, or a final AES dashboard unless a recorded stop/replan condition demonstrates that Slice 1 requires it.

## Closure discipline

Plan completion does not close gaps. Slice 1 may claim delivery only after:

1. the exact external canonical example and negative/error controls are observed through the real entrypoint;
2. required evidence is adequate and revision-bound;
3. the intended reviewer directly uses the working surface;
4. A1 records stakeholder utility separately from automated evidence; and
5. fresh characterization recomputes which originating gaps are closed, narrowed, or still open.
