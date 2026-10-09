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
  fix --> remote[Remote-required case: readiness and ping remain required]
  native --> check[Executable parent schema, source and outcome checks]
  remote --> check
  check --> report
```

The feedback-prevention-v1 traces show the exact source record at default intake, semantic review against all 22 existing families, its family N disposition, native source inspection and a remote-only stop. The remote route was unavailable within the no-network task: tools were advertised, but readiness/ping could not be called. The first remote expectation incorrectly required a missing-tool citation; its parent check failed, and a fresh corrected case passed. This is not a live remote-connectivity check. Private transcript/result bytes stay in the existing private verification log. The original inconclusive child fails the native-positive check. Matching hashes prove identity only. Existing licensing and recurrence processes are unchanged; this case does not establish universal prevention.

The integration boundary also relies on Agent Skills main-branch history policy. GitHub permits merge commits but its observed linear-history requirement blocked the source-preserving merge. The adopted correction changes only that boolean; the final API trace shows every other protection field unchanged, and merge d709bcf retains tested reader revision 80e08cb as its second parent (private repair-verification.jsonl:76-77). The installed default reader at that merge directly preserved the original record and passed disposition verification. The feedback flow above remains unchanged.
