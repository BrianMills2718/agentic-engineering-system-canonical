# Agentic Engineering System — Canonical governance

Start with `wiki/index.md`.

This repository is a protocol-pilot consumer of the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`.

## Commands

```bash
# Slice 1 implementation + focused verification
python -m pip install -e . pytest
python -m pytest -q tests/repository_context
AES_DATA_CONTRACTS_CHECKOUT=/path/to/data-contracts \
  python -m pytest -q tests/repository_context/test_data_contracts_pinned.py
python -m agentic_engineering_system.repository_context.cli \
  --repo /path/to/data-contracts \
  --expect-revision 90c38998e8141bd07e49a77a49ec417aa29beee0

# Plan 001 terminal verification without hosted CI
export AES_DATA_CONTRACTS_CHECKOUT=/path/to/data-contracts
make verification-batch-freeze \
  DECISION="Plan 001 repaired end-to-end acceptance" \
  VERIFY_COMMAND='AES_DATA_CONTRACTS_CHECKOUT="$AES_DATA_CONTRACTS_CHECKOUT" python -m pytest -q tests/repository_context && python -m agentic_engineering_system.repository_context.cli --repo "$AES_DATA_CONTRACTS_CHECKOUT" --expect-revision 90c38998e8141bd07e49a77a49ec417aa29beee0'
AES_DATA_CONTRACTS_CHECKOUT="$AES_DATA_CONTRACTS_CHECKOUT" \
  python -m pytest -q tests/repository_context
python -m agentic_engineering_system.repository_context.cli \
  --repo "$AES_DATA_CONTRACTS_CHECKOUT" \
  --expect-revision 90c38998e8141bd07e49a77a49ec417aa29beee0
make verification-batch-check

# Governed-repo install/audit; run these from a checkout of BrianMills2718/enforced-planning
python scripts/install_governed_repo.py \
  --repo-root /path/to/agentic-engineering-system-canonical --write
python scripts/audit_governed_repo.py \
  --repo-root /path/to/agentic-engineering-system-canonical --strict-governed
```

## Principles

- Project-agnostic architecture stays in `wiki_methodology`; link to it, do not restate it as a second authority.
- AES-specific normative target lives in `docs/architecture/` with stable clause IDs.
- Accepted durable choices live in `docs/decisions/`.
- Plans live in `docs/plans/` and must link to explicit gaps they intend to close.
- Current implementation truth comes from revision-bound characterization/evidence, not timeless status prose.
- The wiki is derived progressive-disclosure navigation, not a native authority.
- Existing systems remain capability authorities until an accepted disposition selects reuse, extend, adapt, supersede, salvage, historical, not-applicable, or unresolved.

## Workflow

- Do not create an implementation root merely to begin coding. First derive target implementation and verification topology through Company Planning.
- Do not hand-author a first execution plan before the target/current gap set has been materialized and dispositioned.
- Before new reusable behavior is implemented locally, resolve the relevant capability through ACA and record the reuse/extend/supersede/local-residual disposition.
- Use Enforced Planning as the execution-governance incumbent unless and until an AES-owned replacement is accepted from authentic evidence.
- A block must provide a runnable recovery path or an explicit human escalation boundary.
- Plan completion never closes a gap by itself; fresh observation and re-characterization determine closure.
- Verification is provider-independent under Decision 0008: local/external execution is first-class, hosted CI is optional infrastructure, evidence reuse is claim-specific over the transitive executed subject, and fresh exact-revision runs should use the incumbent Enforced Planning verification-batch mechanism.
- Before any machine-dependent plan or promise, run the Execution readiness preflight below. Missing Remote MCP tools are a session/tool-exposure failure, not evidence that the machine or WSL is offline.
- Proposed changes to the adopted methodology go through `proposals/` and then the owning methodology repository; this consumer does not silently redefine the standard.

## Execution readiness preflight

Machine-dependent work must fail fast at the execution boundary instead of discovering tool unavailability after planning or repository changes.

Before promising or beginning work that requires Brian's machine:

1. Confirm the Remote MCP toolset itself is exposed in the current conversation. The minimum expected tools are `devices_list`, `devices_ping`, and `process_start`.
2. If `devices_list` is unavailable as a tool, classify the state as **SESSION_TOOL_NOT_EXPOSED**. Do not diagnose the machine, WSL, or repository; those layers have not been reached. Continue only with work that is genuinely GitHub-only, or hand off to a fresh session.
3. If the tool exists, call `devices_list`; confirm the intended device (normally `WINDOWS-STQ88HK`) is present and `execution_ready`.
4. Call `devices_ping` before any filesystem/process operation.
5. Only after the ping succeeds may the agent inspect local repository state or launch the guarded WSL path.

Use this failure taxonomy:

| Observation | Classification | Next action |
| --- | --- | --- |
| `devices_list` tool absent | `SESSION_TOOL_NOT_EXPOSED` | new session / connector-surface diagnosis; do not blame device |
| tool exists, intended device absent | `DEVICE_NOT_REGISTERED` | inspect Remote MCP/device registration |
| device present but not `execution_ready` | `DEVICE_NOT_READY` | restore machine agent/readiness |
| `devices_ping` fails | `DEVICE_UNREACHABLE` | inspect machine/network/tunnel |
| ping succeeds, `process_start` fails | `EXECUTION_RUNTIME_FAILURE` | inspect permissions/process runtime |
| guarded WSL probe fails | `WSL_UNHEALTHY` | stop WSL fan-out; repair WSL separately |

A session-level missing tool is not evidence that the device is offline. A device-level failure is not evidence that WSL is broken. Preserve these boundaries in handoffs and evidence.

For fresh sessions expected to use Brian's machine, the first machine-related action should be the preflight above before committing to a machine-dependent execution plan.

## Repository shape

The roots declared in `.agentic/repo.yaml` are a pilot contract. If the contract proves wrong, record the friction/proposal; do not create ad hoc top-level homes.

## References

- `wiki/index.md` — progressive-disclosure navigation only; follow links to native authority.
- `.agentic/repo.yaml` — repository protocol, active frontier, selected providers, and concern roots.
- `docs/plans/001_repository_context_resolution_vertical.md` — active Plan 001 / Slice 1 execution contract.
- `docs/architecture/SYSTEM_BOUNDARY.md` — AES-specific normative target.
- `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md` — actor-surface and attention-economics constraints.
- `docs/architecture/INITIAL_GAP_LEDGER.md` — recomputed current gap projection from the post-integration characterization.
- `docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md` — provider-independent verification, transitive executed-subject evidence boundaries, and Enforced Planning verification-batch ownership.
- `evidence/provider-provenance/enforced-planning-install-2026-09-18.json` — installed Enforced Planning provider revision/provenance boundary.
- `BrianMills2718/wiki_methodology@0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe` — adopted project-agnostic methodology authority.
