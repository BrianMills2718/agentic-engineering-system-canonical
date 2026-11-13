# Agentic Engineering System — Canonical governance

<!-- GENERATED FILE: DO NOT EDIT DIRECTLY -->
<!-- generated_by: scripts/meta/render_agents_md.py -->
<!-- canonical_claude: CLAUDE.md -->
<!-- canonical_relationships: scripts/relationships.yaml -->
<!-- canonical_relationships_sha256: 9c661ec9a50e -->
<!-- sync_check: python scripts/meta/check_agents_sync.py --check -->

This file is a generated Codex-oriented projection of repo governance.
Edit the canonical sources instead of editing this file directly.

Canonical governance sources:
- `CLAUDE.md` — human-readable project rules, workflow, and references
- `scripts/relationships.yaml` — machine-readable ADR, coupling, and required-reading graph

## Purpose

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

## Operating Rules

This projection keeps the highest-signal rules in always-on Codex context.
For full project structure, detailed terminology, and any rule omitted here,
read `CLAUDE.md` directly.

### Principles

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

### Workflow

- Apply `docs/architecture/SYSTEM_BOUNDARY.md` AES-CAP-001 through AES-CAP-005 and Decision 0009 during normal product design: adopt a sufficient existing product/framework first, use its native modules and extension points, and record the reuse/configure/adapt/local-residual disposition in the design.
- Keep cohesive reusable behavior behind a consumer-independent boundary; keep consequential product policy in configuration/strategies and thin adapters. Do not require framework neutrality, speculative extraction, or a new interface for every function.
- A block must provide a runnable recovery path or an explicit human escalation boundary.
- Plan completion never closes a gap by itself; fresh observation and re-characterization determine closure.
- Verification is provider-independent under Decision 0008: local/external execution is first-class, hosted CI is optional infrastructure, and evidence reuse is claim-specific over the transitive executed subject.
- Select the execution transport before applying its readiness checks. Native Codex/Claude sessions and their subagents use the local filesystem/process tools already exposed under their task permissions; they do not require Remote MCP discovery or a device ping for local work. Work that requires Remote MCP follows the Execution readiness preflight below. Missing Remote MCP tools block that remote route; they do not establish that the machine or WSL is offline or block an authorized native local route.
- Proposed changes to the adopted methodology go through `proposals/` and then the owning methodology repository; this consumer does not silently redefine the standard.

## Machine-Readable Governance

`scripts/relationships.yaml` is the source of truth for machine-readable governance in this repo: ADR coupling, required-reading edges, and doc-code linkage. This generated file does not inline that graph; it records the canonical path and sync marker, then points operators and validators back to the source graph. Prefer deterministic validators over prompt-only memory when those scripts are available.

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
