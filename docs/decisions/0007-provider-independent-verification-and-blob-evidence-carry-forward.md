---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills delegated high-confidence planning authority
date: 2026-09-18
reversible: true
---

# Decision 0007 — Verification is provider-independent; carry execution evidence only across identical relevant blobs

## Context

AES needs trustworthy verification without making one hosted CI provider a semantic
authority or a delivery gate.

During Plan 001, GitHub Actions repeatedly failed before executing workflow steps.
The user subsequently confirmed the cause is exhausted GitHub Actions funding.
That is an execution-provider availability constraint, not evidence about the code.

At the same time, Plan 001 has authentic prior local execution evidence:

- focused Repository Context tests passed;
- the exact pinned private `data-contracts` check passed;
- the real CLI resolved the pinned consumer;
- deterministic artifacts were retained.

The implementation was later integrated through architecture/documentation-only
changes. Blindly demanding a fresh hosted run would therefore couple evidence
validity to a paid execution provider rather than to the verified subject.

## Decision

### 1. Hosted CI is optional verification infrastructure

GitHub Actions, or any other hosted CI service, is a convenience execution
provider. Its availability, billing state, queueing state, or runner failure does
not determine AES conformance.

A hosted-CI outage or funding limit is represented as **provider unavailable**,
not PASS and not FAIL.

### 2. Local/external execution is a first-class verification path

A trusted local or otherwise authorized execution environment may produce the
same or stronger evidence as hosted CI when it:

- executes the accepted verification commands;
- binds external consumers to exact immutable revisions;
- records the exact AES revision and relevant dependency/runtime versions;
- retains enough result detail to distinguish executed checks from source review;
- preserves negative/error controls where required.

For Plan 001, the pinned private consumer remains an explicitly local/external
acceptance boundary through `AES_DATA_CONTRACTS_CHECKOUT`.

### 3. Execution evidence may carry forward only by exact relevant-blob identity

Prior authentic execution evidence may support a later revision without rerunning
unchanged behavior only when all **relevant** executable inputs are byte-identical.

Relevant inputs include, as applicable:

- implementation modules exercised by the claim;
- verification/test modules exercising the claim;
- package/dependency declaration affecting execution;
- immutable external-consumer revision;
- deterministic input artifacts required by the claim.

The carry-forward record must enumerate the compared paths and blob identities.
A commit-message claim, file-path sameness, or human assertion is insufficient.

### 4. Changed verification subjects split the evidence boundary

If a relevant executable or test blob changes, prior execution does not silently
transfer to that changed behavior.

The changed concern must instead have one of:

- fresh execution evidence;
- a narrower non-runtime evidence claim, such as static/source validation, where
  that evidence is actually adequate;
- an explicit unobserved state.

A change in unrelated documentation/governance files does not invalidate
execution evidence for byte-identical runtime/test subjects.

### 5. Utility evidence remains separate

Blob identity and technical execution evidence cannot establish stakeholder
utility.

A human-facing projection that changes after a `change` disposition still
requires direct follow-up observation before utility can be accepted, even if its
technical inputs are unchanged.

### 6. Do not keep automatic hosted workflows merely as failing ceremony

When a hosted provider is known unavailable for administrative reasons, automatic
workflow triggers should be disabled or made manual-only if they create noise
without executable evidence.

Re-enable hosted automation only when it provides decision-relevant evidence at a
reasonable operational cost.

## Plan 001 application

Current canonical Repository Context core implementation/test/package blobs are
identical to the authentic execution revision
`53be16fa1159f31648773062531d751c85d7a011`.

The corrected renderer, renderer regression test, and retained HTML are instead
identical to corrected projection revision
`821d00766b0caed658faf4c816521560a6ccada0`.

The pinned `context.json` is identical across the original executed revision,
the corrected projection revision, and current canonical main.

Therefore:

- prior authentic execution may carry forward for the unchanged resolver/model/
  adapters/CLI/pinned-consumer behavior;
- the corrected renderer may claim only its actually observed/static evidence
  boundary until direct utility review occurs;
- GitHub Actions funding is no longer a Plan 001 closure blocker.

## Consequences

- Verification is tied to evidence and immutable subjects, not a CI vendor.
- Repeated paid execution can be skipped when exact relevant blobs prove nothing
  executable changed.
- Evidence carry-forward becomes explicit and auditable rather than informal.
- The current remaining Plan 001 blocker is primarily follow-up utility/closure
  evidence, not GitHub Actions availability.
