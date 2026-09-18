# Normative/component alignment dogfood checkpoint

Status: **provisional blueprint recorded; structural probe observed; architecture adoption and runtime behavior unverified**

## Current entrypoints

- Directions and open AQRs: `docs/architecture/normative-component-alignment.bootstrap.yaml`.
- Concrete design candidate: `docs/architecture/architecture-realization.bootstrap.yaml` (`AES-BLUEPRINT-001`, revision 1).
- Reproducible research-only structural probe: `research/investigations/validate_architecture_blueprint.py`.
- Exact-content observation: `evidence/bootstrap-alignment/blueprint-structural-observation-001.json`.

These have different jobs. This page is navigation and interpretation, not another source of normative wording. The direction/AQR record remains open; its original blueprint-derivation objective now has a concrete candidate, not an accepted architecture.

## What was actually done

The blueprint was authored from inspected source records using Company Planning bounded-design guidance. It was not produced by an implemented Company Planning generator. It references the adopted documentation methodology at `wiki_methodology@0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe`, the research baseline at AES `2220ad62639c1e4596e57263b99e13fcc81b20ef`, and PR #5 implementation at `9f82f3500e4a472b26756c31ea9205f908d7c394` separately.

It proposes nine responsibility-shaped components and four interaction boundaries. Each component names applicable clauses, origin gaps, provider disposition, a code home, a colocated record home, an observed or unresolved boundary, verification/disproof obligations, and open questions. All 27 clauses in the pinned `SYSTEM_BOUNDARY.md` have declared mappings. That count demonstrates declared coverage, not that the mappings are semantically correct or sufficient.

The real worked binding is `RepositoryContextResolver.resolve` in the existing `repository_context/resolver.py`, its `RepositoryContextArtifact` result in `models.py`, and the existing malformed-manifest negative test. Their source identities are pinned. Existing Slice 1 files are not moved or replaced.

## Evidence qualification correction

Earlier PR comments and conversational summaries called the external mappings completed fit tests. The OPA, TOSCA, and PROV/in-toto probe documents contain conceptual or illustrative mappings, not retained executions establishing provider compatibility. They remain research inputs. No OPA evaluator, TOSCA parser/runtime, SCIP indexer, OWS engine, or attestation provider is selected by this blueprint.

Likewise, AC17 is a donor synthesis, not evidence that its complete approach works reliably or that AES has replicated its results.

Provider-first research does not imply one adapter module per named standard. The earlier technology-shaped skeleton remains an unaccepted historical proposal. This new responsibility-shaped draft is the current comparison candidate, not an accepted supersession of normative architecture.

## What the structural probe establishes

The probe ran in the ChatGPT Python sandbox against exact draft bytes. GitHub blob readback confirmed that the committed blueprint and checker match those executed bytes. It accepted the positive draft and rejected eight controlled invalid variants: duplicate YAML keys, duplicate components, overlapping homes, unknown clauses, missing disproof, mutable source revisions, false verified-boundary claims, and unknown seam participants.

The receipt binds the blueprint, checker, normative source, command, environment, result, limitations, and an interpreter-startup warning. This is neither GitHub CI evidence nor a test run on Brian's machine. The checker is deliberately a bounded research instrument, not a production schema or comprehensive semantic validator.

Reproduce from a checkout containing the draft:

```bash
python research/investigations/validate_architecture_blueprint.py \
  docs/architecture/architecture-realization.bootstrap.yaml \
  --system-boundary docs/architecture/SYSTEM_BOUNDARY.md \
  --self-test
```

## Decisions and uncertainties

The blueprint groups the twelve existing open AQRs into three proposed decisions (`BP-D1` through `BP-D3`): compact record/locality layout; component/symbol scope and typed boundaries; and Company Planning profile versus upstream change/fork. They remain proposed. No new accepted ADR, methodology revision, provider adoption, or Company Planning fork is claimed.

The proposed layout preserves system-level goals/product outcomes/journeys, component-local requirements, and shared seam norms without requiring a new file for every conventional document type. Existing accepted Markdown stays authoritative until an explicit migration. Native typed contracts are referenced instead of being rewritten in YAML.

Applicable context is inherited; behavioral conformance is not. Every symbol should be able to recover its declared applicable normative text, but no symbol is deemed to satisfy all component requirements merely because it is inside the component. Missing applicability relationships remain a semantic review problem beyond the structural probe.

## Next bounded dogfood

Use the real `repository_context` code location to exercise exact normative-text binding and declared-context preservation. Start with the complete small normative baseline; do not silently filter away system or seam obligations. A removed, changed, conflicting, or unresolved reference must remain visible.

Use that result to disposition the compact layout and then materialize the reserved tree with explicit planned/unresolved labels. This does not require every future provider or helper signature to be settled first. A reserved path is not an implemented capability.

PR #5 remains the only Slice 1 implementation line, open and unmerged. This research branch does not inherit its implementation by implication. Human presentation remains in the separate workstream; no HTML or other review UX was created. No Plan 001 delivery, fresh originating-gap closure, or integration completion is claimed here.
