# Agentic Engineering System — Canonical governance

Start with `wiki/index.md`.

**Project brain:** read `.project-brain/now.md` first (layout: agent-skills
`contracts/client-config/agents/project-brain.md`). When a change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request; `python3 scripts/hive/brain_fresh.py .` exits 1 when the brain is stale.

This repository is a protocol-pilot consumer of the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`.

### AES governs itself (v0.2, primary workflow)

AES canonical is governed by its own AES v0.2 target in `.aes/`, accepted by
`docs/decisions/0010-greenfield-v0.2-accepted.md` (accepted architecture:
`docs/architecture/greenfield-v0.2/`; user start:
`docs/greenfield/GETTING_STARTED.md`). The governed roots are
`src/agentic_engineering_system/` and `tests/greenfield/`. This is the primary
workflow for work under those roots; the v0.1 commands further down still work
and are retained under Decision 0010's v0.1 disposition.

- `.aes/target.yaml` is the plan. Every file under a governed root must be a
  planned artifact with that exact path, or the pre-commit hook (written by
  `aes hooks install`; do not edit or bypass it) refuses the commit. The v0.1
  files there are planned as retained history (`NI-AES-HIST`), not v0.2 work.
- Plan changes through AES, not by hand: `aes plan prepare`, write a proposal,
  `aes plan validate <file>` until clean, `aes plan accept <file>`, then commit
  the target and `.aes/plans/<id>.yaml` together before implementing.
- Record evidence with `aes evidence record <VS-ID>` (runs the test, writes
  `.aes/observations/`); hand-write only external observations, in the same
  shape. Evidence recorded on a branch names that branch's commit, so merge
  such PRs with a merge commit, never squash: a squashed-away commit makes
  its observations UNREACHABLE (re-record and set `superseded_by` if it
  happens). The same holds for plans: `aes plan accept` warns off the default
  branch, and `aes status` counts an unreachable accepted plan as a warning.
  `aes status` is the one-screen view; `make aes` runs validate,
  topology and status with this checkout's code, `make aes-check` adds the
  greenfield and repository_context tests.

## Commands

### v0.1 provider commands (retained; Decision 0010)

```bash
# Slice 1 implementation + focused verification
uv venv .venv
. .venv/bin/activate
uv pip install -e '.[dev]'
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

- Do not create an implementation root merely to begin coding. First derive target implementation and verification topology through Company Planning. (For the v0.2 governed roots this is superseded by Decision 0010: topology and plans come from `.aes/target.yaml` through `aes plan`.)
- Do not hand-author a first execution plan before the target/current gap set has been materialized and dispositioned. (Under v0.2 the gap set is `aes status`/`aes plan prepare`; Decision 0010.)
- Apply `docs/architecture/SYSTEM_BOUNDARY.md` AES-CAP-001 through AES-CAP-005 and Decision 0009 during normal product design: adopt a sufficient existing product/framework first, use its native modules and extension points, consult ACA's relevant published boundaries/evidence, and record the reuse/configure/adapt/local-residual disposition in the existing design packet. ACA is not a separate runtime or prerequisite experiment.
- Keep cohesive reusable behavior behind a consumer-independent boundary; keep consequential product policy in configuration/strategies and thin adapters. Use the selected ecosystem's normal packages, declared dependencies, examples, and compatibility tests; do not require framework neutrality, speculative extraction, or a new interface for every function.
- Do not restart standalone ACA benchmarks, demonstration products, or mechanism-building from historical plans. They require separate explicit authorization for a concrete product decision/blocker. Product acceptance and compatibility tests remain required; existing provider ownership and the current Plan 001 frontier are unchanged. (Decision 0010 changes provider ownership for the v0.2 governed roots only.)
- Use Enforced Planning as the execution-governance incumbent unless and until an AES-owned replacement is accepted from authentic evidence. (Decision 0010 accepts AES v0.2 as that replacement for its governed roots; Enforced Planning stays for the v0.1 material and `make check`.)
- A block must provide a runnable recovery path or an explicit human escalation boundary.
- Plan completion never closes a gap by itself; fresh observation and re-characterization determine closure.
- Verification is provider-independent under Decision 0008: local/external execution is first-class, hosted CI is optional infrastructure, evidence reuse is claim-specific over the transitive executed subject, and fresh exact-revision runs should use the incumbent Enforced Planning verification-batch mechanism. (For the v0.2 governed roots, fresh runs are `aes evidence record`; Decision 0010.)
- Select the execution transport before applying its readiness checks. Native Codex/Claude sessions and their subagents use the local filesystem/process tools already exposed under their task permissions; they do not require Remote MCP discovery or a device ping for local work. Work that requires Remote MCP follows the Execution readiness preflight below, including tool exposure, device readiness and ping. Missing Remote MCP tools block that remote route; they do not establish that the machine or WSL is offline or block an authorized native local route. Prefer ChatGPT Work for substantial Remote MCP execution when available because connector exposure can vary across conversations.
- Proposed changes to the adopted methodology go through `proposals/` and then the owning methodology repository; this consumer does not silently redefine the standard.

## Execution readiness preflight

Machine-dependent work must fail fast at the execution boundary instead of discovering tool unavailability after planning or repository changes.

Native local execution: use the current session's exposed filesystem/process tools within repository authority and the task's permissions. This applies to parent sessions and subagents. If the required local tool is absent, report that local capability limitation; do not substitute a Remote MCP prerequisite for it.

Remote MCP execution: before promising or beginning work that requires that transport:

0. Prefer a ChatGPT Work task/session for substantial machine execution when available. This is an operational preference based on observed connector persistence behavior, not an assertion that normal Chat can never execute Remote MCP.
1. Confirm the Remote MCP toolset itself is exposed in the current conversation. The minimum expected tools are `devices_list`, `devices_ping`, and `process_start`.
2. If `devices_list` is unavailable as a tool, classify the state as **SESSION_TOOL_NOT_EXPOSED**. Do not diagnose the machine, WSL, or repository; those layers have not been reached. Continue only with work that is genuinely GitHub-only. For required machine work, prefer a fresh Work task/session; if Work is unavailable, use a fresh normal chat as the fallback rather than repeatedly reconnecting an otherwise healthy connector.
3. If the tool exists, call `devices_list`; confirm the intended device (normally `WINDOWS-STQ88HK`) is present and `execution_ready`.
4. Call `devices_ping` before any filesystem/process operation through Remote MCP.
5. Only after the ping succeeds may the agent inspect repository state or launch the guarded WSL path through Remote MCP.

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

For fresh sessions expected to use Remote MCP, the first remote machine action should be the preflight above before committing to a remote execution plan.

## Repository shape

The roots declared in `.agentic/repo.yaml` are a pilot contract. If the contract proves wrong, record the friction/proposal; do not create ad hoc top-level homes.

## References

- `wiki/index.md` — progressive-disclosure navigation only; follow links to native authority.
- `docs/decisions/0010-greenfield-v0.2-accepted.md` — AES v0.2 greenfield MVP accepted as realized: evidence, standing decisions with wrong-when conditions, non-claims, v0.1 disposition.
- `docs/architecture/greenfield-v0.2/` — accepted v0.2 architecture; `.aes/target.yaml` is the live authority for this repository.
- `.agentic/repo.yaml` — repository protocol, active frontier, selected providers, and concern roots.
- `docs/plans/001_repository_context_resolution_vertical.md` — completed Plan 001 / Repository Context Slice 1 record and closure evidence.
- `docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md` - AES-local modular-design integration, existing owner boundaries, and the stop rule for standalone ACA work.
- `docs/architecture/SYSTEM_BOUNDARY.md` — AES-specific normative target (v0.1 bootstrap; v0.2 in `docs/architecture/greenfield-v0.2/`).
- `docs/architecture/HUMAN_OBSERVABLE_DELIVERY.md` — actor-surface and attention-economics constraints.
- `docs/architecture/INITIAL_GAP_LEDGER.md` — recomputed current gap projection from the post-integration characterization.
- `docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md` — provider-independent verification, transitive executed-subject evidence boundaries, and Enforced Planning verification-batch ownership.
- `evidence/provider-provenance/enforced-planning-install-2026-09-18.json` — installed Enforced Planning provider revision/provenance boundary.
- `BrianMills2718/wiki_methodology@0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe` — adopted project-agnostic methodology authority.
