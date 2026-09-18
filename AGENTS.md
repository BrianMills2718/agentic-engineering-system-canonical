# Agentic Engineering System — Canonical governance

<!-- GENERATED FILE: DO NOT EDIT DIRECTLY -->
<!-- generated_by: scripts/meta/render_agents_md.py -->
<!-- canonical_claude: CLAUDE.md -->
<!-- canonical_relationships: scripts/relationships.yaml -->
<!-- canonical_relationships_sha256: a7a6badb84a5 -->
<!-- sync_check: python scripts/meta/check_agents_sync.py --check -->

This file is a generated Codex-oriented projection of repo governance.
Edit the canonical sources instead of editing this file directly.

Canonical governance sources:
- `CLAUDE.md` — human-readable project rules, workflow, and references
- `scripts/relationships.yaml` — machine-readable ADR, coupling, and required-reading graph

## Purpose

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

# Governed-repo install/audit; run these from a checkout of BrianMills2718/enforced-planning
python scripts/install_governed_repo.py \
  --repo-root /path/to/agentic-engineering-system-canonical --write
python scripts/audit_governed_repo.py \
  --repo-root /path/to/agentic-engineering-system-canonical --strict-governed
```

## Operating Rules

This projection keeps the highest-signal rules in always-on Codex context.
For full project structure, detailed terminology, and any rule omitted here,
read `CLAUDE.md` directly.

### Principles

- Project-agnostic architecture stays in `wiki_methodology`; link to it, do not restate it as a second authority.
- AES-specific normative target lives in `docs/architecture/` with stable clause IDs.
- Accepted durable choices live in `docs/decisions/`.
- Plans live in `docs/plans/` and must link to explicit gaps they intend to close.
- Current implementation truth comes from revision-bound characterization/evidence, not timeless status prose.
- The wiki is derived progressive-disclosure navigation, not a native authority.
- Existing systems remain capability authorities until an accepted disposition selects reuse, extend, adapt, supersede, salvage, historical, not-applicable, or unresolved.

### Workflow

- Do not create an implementation root merely to begin coding. First derive target implementation and verification topology through Company Planning.
- Do not hand-author a first execution plan before the target/current gap set has been materialized and dispositioned.
- Before new reusable behavior is implemented locally, resolve the relevant capability through ACA and record the reuse/extend/supersede/local-residual disposition.
- Use Enforced Planning as the execution-governance incumbent unless and until an AES-owned replacement is accepted from authentic evidence.
- A block must provide a runnable recovery path or an explicit human escalation boundary.
- Plan completion never closes a gap by itself; fresh observation and re-characterization determine closure.
- Verification is provider-independent under Decision 0008: local/external execution is first-class, hosted CI is optional infrastructure, evidence reuse is claim-specific over the transitive executed subject, and fresh exact-revision runs should use the incumbent Enforced Planning verification-batch mechanism.
- Proposed changes to the adopted methodology go through `proposals/` and then the owning methodology repository; this consumer does not silently redefine the standard.

## Machine-Readable Governance

`scripts/relationships.yaml` is the source of truth for machine-readable governance in this repo: ADR coupling, required-reading edges, and doc-code linkage. This generated file does not inline that graph; it records the canonical path and sync marker, then points operators and validators back to the source graph. Prefer deterministic validators over prompt-only memory when those scripts are available.

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
