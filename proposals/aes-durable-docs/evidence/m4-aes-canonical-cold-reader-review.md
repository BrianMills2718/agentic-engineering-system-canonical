---
description: Review of the fresh Haiku reader's trace answering the canonical question in AES canonical (aes-durable-docs M4)
---

# Cold-reader review: AES canonical (M4)

**Question** (verbatim in `m4-aes-canonical-cold-reader-question.txt`): what rule decides whether earlier
evidence still counts after the code changes, who owns it, which check proves it, and why?
**Reader:** `claude -p --model haiku`, Read tool only (Bash, Grep, Glob, Edit, Write, web and agents
disallowed), `--max-turns 40`, no prior context, question on stdin, run in a fresh detached checkout of
main at `3e1eff078` (after PRs #518 and #519). Trace: `m4-aes-canonical-cold-reader.jsonl`. 9 turns, 0.071 USD.

**Files opened, in order (from the trace's tool calls):** `wiki/index.md`, `docs/decisions/0008-...md`,
`docs/decisions/0010-greenfield-v0.2-accepted.md`, `docs/model/trace.yaml`, one Bash call (refused by the
harness: "No such tool available: Bash"), `src/agentic_engineering_system/evidence.py`,
`tests/greenfield/test_evidence.py`, `tests/greenfield/test_reconcile.py`.

**Part by part, against the trace file:**

- **Rule:** `RULE-DEPENDENCY-CHANGE-STALES`, cited from `docs/model/trace.yaml` lines 86-95 (opened). Correct;
  line 86 is the rule's id at this revision. The reader also summarised the full freshness rule (reachable
  commit, unchanged dependency paths, unchanged target entries) from `evidence.py`'s docstring and
  `freshness()` at line 376 (opened). Correct.
- **Owner:** `src/agentic_engineering_system/evidence.py` (opened). Correct.
- **Check:** `test_evidence.py::test_changed_dependency_stales_support` (line 97) and
  `test_reconcile.py::test_dependency_change_reopens_a_supported_criterions_gap` (line 149), both opened and
  both the trace's listed checks; it described what each asserts. Correct. It added a third, related test
  (`test_discovered_dependencies_union_declared_ones`) found in the opened file.
- **Why:** Decision 0008 section 3, with its counterexample (an unchanged `cli.py` importing a changed
  renderer gave a false pass), opened. Correct and matches the trace's decision link.

**Every file the answer cites was opened.** The reader reported what it did not open (`.aes/target.yaml`,
fixtures, observations) and that it did not run the tests.

**Reader-found limits worth keeping:** closure discovery covers Python imports only (non-Python subjects
rely on declared `--depends-on`); the tests exercise a fixture target, not AES's own `.aes/target.yaml`.
Its note that `reviewed_at: 2026-10-11` is "after today" is a timezone artefact: the machine's UTC date
was 2026-10-11 while its local date was 2026-10-10.

**Conclusion:** pass. From `wiki/index.md` the reader reached the rule, owner, check and decision in four
reads and confirmed owner and checks in three more.

Deferred: R6 generated glossary -- no reader question needs it yet
