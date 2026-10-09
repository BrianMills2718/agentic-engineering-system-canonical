# Feedback prevention case model

Scope: AES owns report production, native parent checks and canonical instructions; agent-skills owns the taxonomy reader and dispositions. This extends the existing [subagent model](../aes-subagent-feedback/SYSTEM_MODEL.md), not its producer contract.

```mermaid
flowchart LR
  report[Daily feedback report: original ID, text and links] --> entry[Existing taxonomy reader: provenance-preserving projection]
  entry --> review[Semantic review against every existing family]
  review --> state[Existing committed disposition state]
  state --> fix[Shared CLAUDE instruction: scope by transport]
  fix --> projection[Generated Codex authority]
  projection --> native[Native case: source inspection proceeds]
  fix --> remote[Remote-required case: preflight still blocks without tools]
  native --> check[Executable parent schema, source and outcome checks]
  remote --> check
  check --> report
```

All edges are claims until the named feedback-prevention-v1 trace shows the exact source record, actual semantic review, committed disposition, authority reads, source inspection or remote stop, and parent receipts. Private transcript/result bytes stay in the existing private verification log; this model contains no copied private report. The original inconclusive child must fail the native-positive check. Matching hashes prove identity only. Existing licensing and recurrence processes are unchanged; this case does not establish universal prevention.
