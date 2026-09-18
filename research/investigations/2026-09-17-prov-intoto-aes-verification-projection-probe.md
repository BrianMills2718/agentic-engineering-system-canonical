# W3C PROV / in-toto projection probe against AES verification evidence

Status: research probe; non-normative.

## Question

Can generic provenance and attestation standards carry the factual part of an AES verification event while AES retains only evidence-adequacy, freshness, characterization, and gap-reconciliation semantics?

## Concrete AES event

PR #5 recorded an authentic technical execution at AES revision
`53be16fa1159f31648773062531d751c85d7a011`:

- Enforced Planning strict governed-repo audit: PASS/governed;
- focused repository-context suite: 13 passed, 1 skipped;
- exact pinned external test against `data-contracts@90c38998e8141bd07e49a77a49ec417aa29beee0`: 1 passed;
- real CLI result: RESOLVED;
- deterministic generated artifacts retained;
- regeneration produced no diff;
- GitHub Actions failure was explicitly *not* treated as code-test evidence because no workflow step executed.

This is an especially useful probe because it contains positive observations and a deliberately unresolved observation channel.

## PROV-style projection

Conceptually:

```text
Entity: aes-source@53be16...
Entity: data-contracts@90c389...
Entity: repository-context-context.json
Entity: repository-context-index.html

Activity: governed-repo-audit
  used -> aes-source@53be16
  generated -> audit-receipt(PASS)

Activity: focused-pytest
  used -> aes-source@53be16
  generated -> test-receipt(13 passed, 1 skipped)

Activity: pinned-consumer-test
  used -> aes-source@53be16
  used -> data-contracts@90c389
  generated -> external-test-receipt(1 passed)

Activity: repository-context-cli
  used -> aes-source@53be16
  used -> data-contracts@90c389
  generated -> context.json
  generated -> index.html

Activity: github-actions-attempt
  used -> aes-source@53be16
  generated -> ci-attempt-receipt(execution unavailable)

Agent: Enforced Planning provider
Agent: local test harness
Agent: GitHub Actions
```

PROV can model entities, activities, agents, use/generation, derivation, association, and attribution without AES inventing those generic relationships.

## in-toto-style projection

The governed audit, tests, and CLI execution can also be represented as signed/attested steps with:

- materials: exact AES revision and exact consumer revision;
- command;
- products: receipts and generated artifacts;
- byproducts: stdout/status metadata;
- functionary identity when available.

This is a better generic substrate than a bespoke AES execution-receipt envelope if cryptographic/software-process attestation is required.

SLSA is narrower: it is particularly useful when the evidence concerns source/build provenance and verified artifact production, not arbitrary AES semantic verification.

## What the standards do not answer

Neither PROV nor in-toto decides:

- what evidence kind a criterion requires;
- whether a passing unit test is adequate for an external-runtime claim;
- whether the observation is still current after a source/dependency change;
- whether an ERROR or unavailable observer blocks current characterization;
- whether the evidence closes, narrows, or leaves a gap unchanged;
- whether stakeholder utility evidence is required separately;
- whether a negative control is required;
- whether a relationship such as requirement -> implementation -> verification is itself adequately evidenced.

Those are AES lifecycle semantics.

## Disposition

- **W3C PROV:** strong candidate for generic provenance vocabulary/projection.
- **in-toto:** strong candidate for executable-process/software attestation where signatures/custody matter.
- **SLSA:** use where build/source supply-chain provenance applies; do not stretch it into general AES evidence.

AES should retain a small qualification layer: criterion/evidence-kind adequacy, revision/dependency freshness, epistemic state, characterization effect, gap effect, and stakeholder-vs-automation evidence class.

## Canonical-stub consequence

Safe to reserve:

- `evidence/prov_adapter.py`;
- `evidence/intoto_adapter.py`;
- `evidence/qualification.py` as a likely AES-local residual.

Do not stub a universal AES provenance graph or generic attestation language.
