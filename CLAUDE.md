# Agentic Engineering System — Canonical governance

Start with `wiki/index.md`, then `docs/architecture/GOAL.md`. The goal is
**autonomous, effective coding agents**; code/documentation alignment supports it.
Lockstep plans behavioral structure, typed interfaces and tests before implementation,
projects full normative context into code, projects observed status back into the
documents, and links the sources through a navigational wiki. Read the component
contract `docs/architecture/LOCKSTEP.md` and document roles
`docs/architecture/DOCUMENTATION.md` before assessing a narrow mechanism.
These pages reconcile existing intent, not a new runtime policy.

**Project brain:** read `.project-brain/now.md` first (layout: agent-skills
`contracts/client-config/agents/project-brain.md`). When a change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request; `python3 scripts/hive/brain_fresh.py .` exits 1 when the brain is stale.

This repository is a protocol-pilot consumer of the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`.

### Current state (2026-11-13)

AES is the name for the whole system: planning supplied by Company Planning,
Lockstep, the feedback loop and the policy layer (Brian, 2026-11-11: "to me aes is the whole sysem lockstep is one
part"). Its current state is in `.project-brain/now.md`; the map is code2-workspace
`docs/architecture/model.c4`; what retires and what stays is code2-workspace
decision 0009 (Brian, 2026-11-10: feedback loop kept, the `aes` command line and `.aes/target.yaml` retire one repository at a time).

- Lockstep ships from this repository as package `src/lockstep/`: the one planning-and-checking tool, with code2check's commit checks and Company Planning's plan check (design approved by Brian, 2026-11-11, "i approve single tool desing re d4"; built in #831 to #841; [proposals/one-planning-tool/DESIGN.md](proposals/one-planning-tool/DESIGN.md); status in `wiki/lockstep.md`).
- The feedback machinery lives in `scripts/learning_loop`. Collection and labeling are scheduled; analysis, fix-owner and effects jobs are disabled as observed 2026-11-13. Scheduling is not evidence of end-to-end improvement; see `docs/architecture/FEEDBACK_AND_POLICY.md`.
- The policy layer combines the register in `docs/rules` and `scripts/rules` with shared agent rules in code2-workspace `agents/`; the register is not complete coverage of those instructions. Questions and recommendations belong in `docs/planning/open-questions.json`, navigated by `wiki/open-questions.md`.
- The `aes` command line (`src/agentic_engineering_system/`) is still used by dodaf, lifelike, lockstep, plan-code-wiki and whygame5, and retires with the last of them.
- AES no longer governs itself: its pre-commit refusal was removed on 2026-10-14 (#789), and its own `.aes/` target, the claims and worktree machinery, the old plans and 24 old proposals were retired on 2026-11-12 (record, reasons and restore command: `docs/retired/2026-11-12.md`). Merges go through `ship`; work happens in `claude -w` worktrees (`~/code2/AGENTS.md`).
- On 2026-10-13 Brian moved `~/code2` to off-the-shelf tools (OpenSpec for required behavior, lefthook, GitHub Issues). Behavior changes here go through OpenSpec (`openspec/specs/`).

## Commands

```bash
uv venv .venv && uv pip install -e '.[dev]'
make check        # AGENTS.md sync check, pytest without slow tests, mypy
make check-full   # check plus the slow end-to-end tests
```

## Principles

- Project-agnostic architecture stays in `wiki_methodology`; link to it, do not restate it as a second authority.
- AES-specific normative target lives in `docs/architecture/` with stable clause IDs.
- Accepted durable choices live in `docs/decisions/`.
- Current implementation truth comes from revision-bound characterization/evidence, not timeless status prose.
- The wiki is derived progressive-disclosure navigation, not a native authority.
- Every Git-tracked file must be reachable and summarized from `wiki/index.md`,
  including instructions, source, tests, fixtures, generated files and historical
  changes. Keep source identity, purpose, role and review disposition in the file
  inventory. Assess overlap and unique information before consolidating; preserve
  unresolved material. Source: Brian, 2026-11-13, clarified after the 69-reader-file
  check omitted the broader repository; AES #849. Reachability alone is not summary
  adequacy, and a dated reviewed inventory is not continuous automatic freshness.
- Existing systems remain capability authorities until an accepted disposition selects reuse, extend, adapt, supersede, salvage, historical, not-applicable, or unresolved.

## Workflow

- Apply `docs/architecture/SYSTEM_BOUNDARY.md` AES-CAP-001 through AES-CAP-005 and Decision 0009 during normal product design: adopt a sufficient existing product/framework first, use its native modules and extension points, and record the reuse/configure/adapt/local-residual disposition in the design.
- Keep cohesive reusable behavior behind a consumer-independent boundary; keep consequential product policy in configuration/strategies and thin adapters. Do not require framework neutrality, speculative extraction, or a new interface for every function.
- A block must provide a runnable recovery path or an explicit human escalation boundary.
- Plan completion never closes a gap by itself; fresh observation and re-characterization determine closure.
- Verification is provider-independent under Decision 0008: local/external execution is first-class, hosted CI is optional infrastructure, and evidence reuse is claim-specific over the transitive executed subject.
- Select the execution transport before applying its readiness checks. Native Codex/Claude sessions and their subagents use the local filesystem/process tools already exposed under their task permissions; they do not require Remote MCP discovery or a device ping for local work. Work that requires Remote MCP follows the Execution readiness preflight below. Missing Remote MCP tools block that remote route; they do not establish that the machine or WSL is offline or block an authorized native local route.
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
- `docs/retired/2026-11-12.md` — what was retired, why, and how to restore it.
- `docs/decisions/0010-greenfield-v0.2-accepted.md` — AES v0.2 greenfield MVP accepted as realized (history for this repository, which no longer governs itself with it).
- `docs/architecture/greenfield-v0.2/` — the v0.2 architecture that the retained `aes` library implements.
- `.agentic/repo.yaml` — repository protocol and concern roots.
- `docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md` - AES-local modular-design integration and the stop rule for standalone ACA work.
- `docs/architecture/SYSTEM_BOUNDARY.md` — AES-specific normative target.
- `docs/decisions/0008-provider-independent-verification-with-transitive-subjects.md` — provider-independent verification and transitive executed-subject evidence boundaries.
- `BrianMills2718/wiki_methodology@0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe` — adopted project-agnostic methodology authority.
