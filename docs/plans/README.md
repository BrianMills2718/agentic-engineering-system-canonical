# Plans

Status: one active pilot plan; D1 closed; Slice 1 implementation partial; historical core execution evidence retained; current end-to-end local verification pending after renderer/test repair; first A1 = `change`; post-integration characterization/gap recomputation complete; follow-up utility review pending.

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
- PR #5 integration onto canonical main: `320991b96a3e3aaa15aa8ba05817a7eee1c52603`;
- post-integration characterization: `evidence/plan-001/320991b96a3e3aaa15aa8ba05817a7eee1c52603/characterization.md`;
- initial gap ledger: recomputed from that characterization;
- frozen external consumer: `BrianMills2718/data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`;
- active actor entrypoint: `aes-repo-context`;
- selected substrate: local Git + Pydantic 2.13.5 + PyYAML 6.0.3 + Python stdlib;
- Data Contracts, Representation Router, Code Map V4, and predecessor AES systems remain unselected as Slice 1 runtime dependencies;
- follow-up presentation work through Representation Router remains separate from Repository Context runtime semantics.

Decision 0008 supersedes the earlier blob-only carry-forward rule. Narrow resolver/model/adapter claims may retain historical evidence where their transitive executed subject is unchanged, but the CLI and pinned-consumer path execute the changed renderer. The pinned test also contained stale wording assertions and has been repaired. Therefore current end-to-end acceptance requires one fresh local/external execution.

## Immediate frontier

```text
canonical Slice 1 implementation on adopted architecture
        ↓
run repaired focused suite + pinned private consumer + real CLI locally
        ↓
bind fresh verification to exact clean revision with Enforced Planning verification batch
        ↓
keep hosted GitHub Actions optional/manual
        ↓
follow-up direct utility review when the corrected presentation is reviewable
        ↓
refresh characterization/gap state only if new observations materially change it
        ↓
final Plan 001 closure/reconciliation
```

GitHub Actions is administratively unavailable because its funding is exhausted. Automatic triggers remain disabled. Hosted CI is not a Plan 001 acceptance gate; fresh local/external execution under Decision 0008 is the current technical closure path.

Do not broaden into generalized indexing, a characterization platform, representation infrastructure, or a final AES dashboard unless a Plan 001 stop/replan condition fires.

## Closure discipline

Plan completion does not close gaps. Slice 1 may claim delivery only after:

1. the exact external canonical example and negative/error controls are adequately observed through the real entrypoint;
2. required evidence is adequate and revision-bound;
3. the intended reviewer directly uses the corrected working surface;
4. stakeholder utility remains separate from automated evidence; and
5. fresh characterization recomputes which originating gaps are closed, narrowed, or still open.
