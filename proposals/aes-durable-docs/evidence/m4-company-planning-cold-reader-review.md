---
description: Review of the fresh Haiku reader's trace answering the canonical question in company-planning (Plan #63)
---

# Cold-reader review (Plan #63, R11)

**Question:** what rule governs plan adoption, who owns it, which check proves it, and why?
**Reader:** `claude -p --model haiku`, Read tool only (Bash, Grep, Glob, Edit, Write, web and agents disallowed), `--max-turns 40`, no prior context, started at `wiki/index.md`, told to follow only links or paths in files it had read.

| Run | Trace | Files opened (from the trace's Read calls) | Result |
|---|---|---|---|
| attempt 1 | `cold-reader-attempt1-noprompt.jsonl` | none | invalid run: `--disallowedTools` consumed the prompt argument ("Input must be provided"); fixed by passing the question on stdin |
| run 1 | `cold-reader-run1.jsonl` | `wiki/index.md`, `docs/model/trace.yaml`, `docs/decisions/0001-plan-adoption-requires-a-receipt.md` | all four parts answered in 3 reads (4 turns, 0.013 USD); owner and check cited from the trace file without opening them, which the reader said plainly; fails this plan's stricter criterion (owner or test file opened) |
| run 2 | `cold-reader.jsonl` | `wiki/index.md`, `docs/model/trace.yaml`, `docs/decisions/0001-...`, `plugins/company-planning/scripts/method_conformance/gate.py`, `tests/test_method_conformance.py` (three ranges) | pass (8 turns, 0.023 USD) |

**Run 2, part by part, against the trace:**

- **Rule:** `RULE-ADOPT-RECEIPT` with its statement, quoted from `docs/model/trace.yaml` (opened, read 2). Correct.
- **Owner:** `gate.py`, with `evaluate()` setting the result to fail on a failing blocking item and `adopt()` setting `decision = "adopted" if receipt["result"] == "pass" else "refused"` (opened, read 4). Correct; the cited lines match the file at this revision.
- **Check:** `test_mixed_structural_and_semantic_failures_still_write_a_valid_refusal` and what it asserts (refused decision, fail result, schema-valid receipt, both failing item IDs), plus the two other listed checks (opened, reads 5-7). Correct.
- **Why:** decision 0001's reasons (self-attestation without inspectable evidence; a universal checklist becomes ceremony and hides work behind "not applicable") (opened, read 3). Correct, with one misreading: the reader says the record's "Wrong when" section reports the source design does not record "this reasoning"; the record actually says the wrong-when condition is not recorded. The reason itself is stated correctly.

**Every file the answer cites was opened** in the trace, except the design document, which the reader explicitly says it did not open and does not rely on.

**Conclusion:** the durable documents route a fresh reader from `wiki/index.md` to the rule, owner, check and reason in three reads, and to verified owner and check in five.
