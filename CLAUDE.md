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
- Proposed changes to the adopted methodology go through `proposals/` and then the owning methodology repository; this consumer does not silently redefine the standard.

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
