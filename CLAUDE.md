# Agentic Engineering System — Canonical governance

Start with `wiki/index.md`.

This repository is a protocol-pilot consumer of the standalone architecture in `BrianMills2718/wiki_methodology` at revision `0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`.

## Authority rules

- Project-agnostic architecture stays in `wiki_methodology`; link to it, do not restate it as a second authority.
- AES-specific normative target lives in `docs/architecture/` with stable clause IDs.
- Accepted durable choices live in `docs/decisions/`.
- Plans live in `docs/plans/` and must link to explicit gaps they intend to close.
- Current implementation truth comes from revision-bound characterization/evidence, not timeless status prose.
- The wiki is derived progressive-disclosure navigation, not a native authority.
- Existing systems remain capability authorities until an accepted disposition selects reuse, extend, adapt, supersede, salvage, historical, not-applicable, or unresolved.

## Bootstrap constraints

- Do not create an implementation root merely to begin coding. First derive target implementation and verification topology through Company Planning.
- Do not hand-author a first execution plan before the target/current gap set has been materialized and dispositioned.
- Before new reusable behavior is implemented locally, resolve the relevant capability through ACA and record the reuse/extend/supersede/local-residual disposition.
- Use Enforced Planning as the execution-governance incumbent unless and until an AES-owned replacement is accepted from authentic evidence.
- A block must provide a runnable recovery path or an explicit human escalation boundary.
- Plan completion never closes a gap by itself; fresh observation and re-characterization determine closure.
- Proposed changes to the adopted methodology go through `proposals/` and then the owning methodology repository; this consumer does not silently redefine the standard.

## Repository shape

The roots declared in `.agentic/repo.yaml` are a pilot contract. If the contract proves wrong, record the friction/proposal; do not create ad hoc top-level homes.
