# Fit test — AES evidence semantics vs W3C PROV, in-toto, and SLSA

Status: discriminating probe
Date: 2026-09-17

## Purpose

Determine which evidence/provenance concepts AES should reuse from standards rather than hand-model, while preserving the genuinely AES-specific semantics around evidence adequacy, freshness, characterization, and gap reconciliation.

AES source reviewed:
- `research/synthesis/aes-evidence-characterization-and-context-suggestions.md`
- accepted `SYSTEM_BOUNDARY.md` evidence/gap clauses

External sources:
- W3C PROV: https://www.w3.org/TR/prov-primer/ and https://www.w3.org/TR/prov-constraints/
- in-toto: https://in-toto.io/docs/getting-started/ and https://in-toto.io/docs/specs/
- SLSA 1.2: https://slsa.dev/spec/v1.2/

## AES evidence semantics observed

AES research already distinguishes several semantics that matter operationally:

- raw observations / execution receipts;
- exact subject and revision binding;
- observer/provider version and environment;
- required proof kind vs observed check kind;
- evidence adequacy separately from check result;
- explicit epistemic states such as PASS / FAIL / UNOBSERVED / ERROR / STALE;
- freshness / invalidation when dependencies change;
- characterization as a materialized interpretation over evidence;
- evidence-bearing relationship assertions;
- negative controls / counterfactual sensitivity;
- fresh characterization before gap closure or narrowing;
- stakeholder/human observation as a separate evidence class.

These semantics combine provenance, assurance, epistemology, and lifecycle reconciliation.

## W3C PROV fit

PROV provides a generic interchange model around:

- **Entity** — a thing/data/artifact;
- **Activity** — something that occurs and acts upon/produces entities;
- **Agent** — a responsible actor/system;
- generation / usage;
- derivation;
- attribution / association / responsibility;
- collections and related provenance links;
- validity/inference constraints.

### Strong mapping

| AES need | PROV fit |
| --- | --- |
| artifact/evidence identity | strong (`Entity`) |
| execution/observation event | strong (`Activity`) |
| observer/provider/actor | strong (`Agent`) |
| produced-by relation | strong (`wasGeneratedBy`) |
| used-input relation | strong (`used`) |
| derived-from relation | strong (`wasDerivedFrom`) |
| responsibility/association | strong |
| provenance interchange | strong |

### Missing AES semantics

PROV intentionally does not decide:

- whether the observation proves a criterion;
- whether the check was strong enough for the claim;
- whether evidence is currently fresh for a changed subject;
- whether a relationship is sufficient for conformance;
- whether a gap closes or narrows;
- whether an observation was a positive or negative control;
- whether a stakeholder judged a surface useful.

### Disposition

Use PROV as the external **provenance projection/interchange layer**. Do not duplicate generic Entity/Activity/Agent/derivation semantics in a universal AES provenance model.

AES retains a small qualification/reconciliation layer above PROV.

## in-toto fit

in-toto provides signed software-process evidence:

- a signed **layout** defines expected supply-chain steps and authorized functionaries;
- executed steps emit signed **link metadata**;
- links record command/material/product information;
- the final chain can be verified against the approved layout;
- stable v1.0 specification and stable v1.0 Attestation Framework exist.

### Strong mapping

| AES need | in-toto fit |
| --- | --- |
| exact executed step receipt | strong |
| signed actor/functionary custody | strong |
| input/output artifact hashes | strong |
| expected step sequence | strong for software supply-chain style flows |
| tamper-evident verification | strong |
| command/material/product evidence | strong |

### Missing AES semantics

in-toto does not answer:

- whether an executed step is the right proof for an AES criterion;
- whether a human-review observation is useful/valid;
- whether a passing receipt closes a target/current gap;
- whether a semantic implementation relationship remains valid;
- whether an observation is stale because a non-file dependency changed;
- what next plan/slice should be derived.

### Disposition

Prefer in-toto attestations over bespoke signed execution receipts when the boundary is genuinely a software-process step with identifiable inputs/outputs/functionary.

Do not force all AES observations into in-toto.

## SLSA fit

SLSA 1.2 defines supply-chain security levels/tracks and standard provenance formats. Build provenance uses the in-toto attestation framework and records:

- builder identity;
- build type;
- external/internal parameters;
- resolved dependencies;
- produced artifact subjects;
- where/when/how artifacts were built.

### Strong mapping

SLSA is authoritative for:

- build provenance;
- source provenance;
- build platform identity/security claims;
- software artifact production provenance.

### Missing AES semantics

SLSA is intentionally not a general engineering evidence model. It should not be stretched to encode:

- planning decisions;
- requirement-to-implementation fit;
- test adequacy;
- stakeholder utility;
- gap closure;
- generic repository observations.

### Disposition

Use SLSA where AES needs build/source provenance. Do not recreate build provenance contracts locally.

## Proposed layered evidence architecture

```text
native checks / tools / humans
        ↓
raw observations
        ↓
external evidence/provenance substrate where applicable
    PROV         -> generic provenance graph
    in-toto      -> signed software-step attestations
    SLSA         -> source/build provenance
        ↓
AES evidence qualification residual
    criterion being supported
    required evidence kind
    observed check kind
    epistemic state
    adequacy
    freshness / invalidation
    negative-control / coverage semantics
        ↓
revision-bound characterization
        ↓
gap reconciliation
```

## Key conclusion

**AES should not own generic provenance or software-build attestation schemas.**

Its residual value is the interpretation/reconciliation layer:

> Given this provenance and these receipts, what is AES justified in believing about the current implementation at this exact revision, and what target/current gap remains?

That question is not answered by PROV, in-toto, or SLSA and is legitimately AES-specific.

## Suggested canonical subject boundaries

Safe to stub after naming review:

- `ProvenanceProjectionProvider` — maps native evidence into PROV-compatible relations when useful;
- `AttestationProvider` — accepts/emits in-toto-style attestations when applicable;
- `BuildProvenanceProvider` — consumes SLSA provenance rather than redefining it;
- `EvidenceQualification` / `EvidenceAssessment` residual — compares observed evidence to required proof semantics;
- `FreshnessAssessment` residual;
- `Characterization` residual;
- `GapReconciliation` residual.

Names are provisional; semantic boundaries are the important result.

Do not stub universal local equivalents of:

- provenance Entity/Activity/Agent;
- generic artifact derivation relations;
- signed software-step layout/link formats;
- build/source provenance schemas.

## Follow-on fit tests

1. Map a real Plan 001 verification receipt into PROV + an AES qualification envelope.
2. Test whether an in-toto Statement/attestation can carry the exact external-consumer execution receipt without losing relevant fields.
3. Test SLSA only at build/source boundaries; reject it early for non-build evidence rather than overgeneralizing it.
