# Plan 002 eval protocol

Status: P0 source inventory in progress
Authority: Plan 002 defines scope and stop rules; this directory holds bounded evaluation definitions and source-reference manifests.
Execution handoff: [`P0_RUNBOOK.md`](P0_RUNBOOK.md) contains the exact machine/provider closure sequence.

## Current finding

GitHub inspection located four exact authentic completion/verification decision events with retained session/transcript or receipt identities. These four are now the frozen initial exploratory dataset for Plan 002.

The case-count gate is **cleared at 4/4**. Before a real OpenRouter-backed replay can run, the remaining required step is provider preflight:

1. run the AES execution-readiness preflight if machine access is needed;
2. authenticate to OpenRouter, confirm the key is usable, and select one explicit structured-output-capable model ID;
3. run one protocol-only structured-output chat-completions smoke request;
4. keep any raw-custody limitations for the four cases explicit rather than blocking exploratory learning on an arbitrary fifth-case target.

## Candidate source families

The frozen exploratory dataset is the four exact predecessor Plan 10 cases:

- P10-S3 native Stop allow — authentic Claude Code response, exact transcript digest and completed receipt retained.
- P10-S4 provider/dependency warning — authentic Stop decision with exact failed-session transcript digest and completed receipt identity.
- P10-S4 unsupported verification block — authentic Stop decision, exact completed receipt digest, and source transcript identity.
- P10-S4 post-recovery allow — authentic identical-claim retry after the focused test ran, with exact receipt digest and recovery-session transcript digest.

Later cold-start evidence from 2026-09-21 records additional real live assertion-gate outcomes, including an initial `allow/no_report`, a replayed `block/claim_support_rejected:3_of_3`, and another live blocked/revised turn. GitHub evidence does not retain enough event-level IDs for those observations to count as exact replay-ready cases yet.

A 2026-09-22 follow-up also records **4 of 4** benign live `echo` verification turns reaching the real judge and blocking with `claim_support_rejected:1_of_1` because of an evidence-scope mismatch. That is strong authentic failure evidence, but the retained Git page still omits session/transcript/receipt identities, so those turns remain leads rather than counted P0 cases.

Plan 16 also contains an installed positive/negative assertion-admission proof. It is useful protocol/regression evidence but uses test-generated transcripts and therefore is **not counted** toward the authentic-case P0 threshold.

## Leakage rule

Eventual outcome, later human adjudication, later fixes, and later verification may label/report a case but must never enter the Jev evaluator's event-time state. Every case used in V1/V2 must make that separation mechanically checkable.

## Privacy/custody rule

Git stores only source references, hashes, bounded sanitized excerpts where already retained by the source repository, evaluation definitions, and safe generated reports. Raw private transcripts remain with their existing archive owner.
