# Plans

Status: one active pilot plan; D1 closed; Slice 1 implementation partial; technical execution observed; first A1 = `change`; follow-up utility review and fresh characterization pending.

## Active

- [`001_repository_context_resolution_vertical.md`](001_repository_context_resolution_vertical.md) — Plan 001 / first external-consumer vertical. The implementation exists on `slice-1/repository-context` / PR #5, but delivery is not yet claimed.
- [`001_D1_contract_surface_topology_freeze.md`](001_D1_contract_surface_topology_freeze.md) — **closed** subordinate D1 record. It is historical design authority for the frozen Slice 1 choices, not a second active plan.

## Current state

The repository is no longer `planned_unrealized`.

- bootstrap architecture: **ADOPTED** on `main@45fa215dd977e2ab44338465d36ac37756f14e53`;
- implementation state: **PARTIAL**;
- verification state: **PARTIAL**;
- prior authentic technical execution: **OBSERVED** on exact pre-refresh revisions;
- first stakeholder A1: **`change`** at AES revision `53be16fa1159f31648773062531d751c85d7a011`;
- PR #5 refresh onto adopted architecture: `6bd121a2eb824043836516b93d3268169a714582`;
- frozen external consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`;
- active actor entrypoint: `aes-repo-context`;
- selected substrate: local Git + Pydantic 2.13.5 + PyYAML 6.0.3 + Python stdlib;
- Data Contracts, Representation Router, Code Map V4, and predecessor AES systems remain unselected as Slice 1 runtime dependencies;
- follow-up presentation work through Representation Router remains separate from Repository Context runtime semantics.

The refreshed branch preserves all Repository Context source/test blobs from the pre-refresh head. That makes prior execution evidence relevant to those exact blobs, but it does **not** convert prior execution into a fresh refreshed-head run.

## Immediate frontier

```text
refreshed Slice 1 branch on adopted architecture
        ↓
re-observe applicable technical/regression checks at the exact refreshed head
        ↓
re-run pinned private data-contracts acceptance with AES_DATA_CONTRACTS_CHECKOUT
        ↓
follow-up direct utility review when the corrected presentation is reviewable
        ↓
revision-bound characterization
        ↓
fresh originating-gap recomputation
```

Hosted GitHub regression CI is currently unavailable as execution evidence because jobs are failing before any workflow step runs. Even when hosted regression CI is healthy, it does not prove the private pinned-consumer acceptance boundary unless that checkout is explicitly provisioned.

Do not broaden into generalized indexing, a characterization platform, representation infrastructure, or a final AES dashboard unless a Plan 001 stop/replan condition fires.

## Closure discipline

Plan completion does not close gaps. Slice 1 may claim delivery only after:

1. the exact external canonical example and negative/error controls are adequately observed through the real entrypoint;
2. required evidence is adequate and revision-bound;
3. the intended reviewer directly uses the corrected working surface;
4. stakeholder utility remains separate from automated evidence; and
5. fresh characterization recomputes which originating gaps are closed, narrowed, or still open.
