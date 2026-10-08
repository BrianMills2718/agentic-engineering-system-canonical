---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills (2026-10-08, "i approve")
date: 2026-10-08
reversible: true
---

# Decision 0012 - Capability reuse is enforced at plan adoption against one catalogue

## Context

Brian, 2026-10-08: "how should we move forward with an ecosystem where capabilities are
modular and reused across time in different workflows/projects rather than basically every
project starting from scratch", and, on utilities, "we should definitely be using off the
shelf for all these utils unless we absolutely can't."

[AES-CAP-001 to AES-CAP-004](../architecture/SYSTEM_BOUNDARY.md#aes-cap-001--capability-first-residual-implementation)
and [AES-CONTRACT-001](../architecture/SYSTEM_BOUNDARY.md#aes-contract-001--native-typed-boundaries)
already require capability resolution before hand-authored behavior, external-first sourcing,
reusable code staying with its natural owner, and typed boundaries through Data Contracts.
They are not enforced against a shared list of what exists, so each plan resolves candidates
from its own search. Evidence that this lets work start from scratch:

- the vision program thesis (2026-10-05) records six attempts at reusable infrastructure built
  first and none reused, and 1,321 logged lessons with none turned into a binding check;
- DIGIMON's capability ledger (2026-10-08, `docs/reports/216_capability_ledger.md` in
  BrianMills2718/digimon_application_20260215) found 19 earlier KGAS capabilities neither
  present nor recorded, and document ingestion implemented separately in four projects
  (crest_kg, graph_application_toolkit, trajectory, DIGIMON's legacy `corpus_prepare`) with
  no owner;
- two registries describe themselves as the capability catalogue: ecosystem-ops'
  `capability_registry.py` (behind dashboard.brianmills.dev/capabilities) and
  agentic-capability-architecture-canonical's `capability_registry.yml`.

## Decision

1. **One catalogue.** The authoritative capability catalogue is agentic-capability-architecture-canonical,
   applied through AES (Decision 0009). It has two files: `reuse_candidates.yml` for capabilities
   observed across projects and their selected off-the-shelf implementations (candidate, then
   promoted), and `capability_registry.yml` for the packages that repository itself holds. Each entry names a capability (the job), its implementations (off-the-shelf
   engines first, per AES-CAP-002), its tool (the callable agents use), its boundary (the typed
   input and output), and its consumers. The catalogue holds pointers and evidence, never the
   product code (AES-CAP-004). The ecosystem-ops registry becomes a read-only view of it or is
   retired; it is not a second authority.
2. **Filled from evidence.** An entry is added when something works and is used, with the
   evidence that shows it (a ledger row, a test, a consumer). Aspirational entries are not
   catalogue entries.
3. **Reuse is checked at plan adoption.** Company Planning's adoption checklist gains a core
   item: the plan names, from the catalogue, the capabilities it reuses, and any new capability
   it adds together with its first consumer, or states that no catalogue entry fits and why.
   A plan that does not answer cannot be adopted.
4. **Extract on the second use.** A capability is pulled out into shared form when a second
   project needs it, not before. A first implementation stays local to its project.
5. **Pieces compose through shared contracts.** Hand-offs between capabilities use Data
   Contracts types (AES-CONTRACT-001), including the receipt, `measured_on` and claim-scope
   contract once it moves from DIGIMON.

First case: "documents to text" (IBM Docling as primary implementation, because it keeps page and
position provenance per passage; MarkItDown as fallback), consumed by DIGIMON and crest_kg.

## Wrong if

After the first three plans adopted under the new checklist item, none names a reused
catalogue capability. That would mean the catalogue is not useful for planning, and this
decision is revisited.

## Feedback path

A checklist refusal that a plan author judges wrong is filed as a `kind:friction` issue in this
repository (the feedback record, `learned` skill), quoting the refusal.
