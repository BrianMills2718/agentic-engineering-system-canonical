# Family Z re-test (2026-11-05)

Adding family Z ("the fix landed where the symptom showed, not where the cause
starts") changes the frozen question set, so `label_items.py` asks for the
judged test sets to be re-run first. Concern: agent-skills issue #538.

`retest.py <question_set.json> <out.json>` runs the 2026-10-02 held-out set (20
judged learnings and 4 synthetic `other` items, from
`../2026-10-02-question-design/`) plus six private feedback issues through Jev
(`typesafe/jev-1.13`), using `label_items.py`'s own `ask()` and `decide()`. The
feedback issues are fetched at run time with `gh`; their text is not stored
here. Each configuration ran twice on the same day. Cost about $0.003 per run.

| Question set | File | Held-out top | Held-out near-top | Synthetic top |
|---|---|---|---|---|
| Before (22 families) | `question_set_before.json` | 13/20, 13/20 | 14/20, 14/20 | 2/4, 3/4 |
| Z, first wording | `question_set_after.json` | 10/20, 10/20 | 12/20, 12/20 | 2/4, 2/4 |
| **Z, narrow wording (shipped)** | `question_set_after_narrow.json` | 12/20, 11/20 | 13/20, 12/20 | 2/4, 2/4 |

**First wording rejected.** It pulled three held-out items to Z, one of them
plainly wrong (a profile label that made the profile mandatory), and also took
a feedback item where a test caught a fix's mistake. It read Z as "any fix that
was too narrow".

**Narrow wording.** Z now requires a named upstream stage left unchanged while a
downstream consumer compensates, and its `not_for` sends too-narrow fixes to
`untested_reasoning` or `partial_list_treated_as_complete`. This wording was
tuned once on this held-out set after seeing the first wording's misses, so
the set is no longer fully held out for Z.

The one item Z still takes is `lrn-20260824T164328079988Z-db549010ab`
(ground truth R, C): a per-case flag was added in the acceptance tier while
`_contract_from_draft` kept raising on non-object inputs, and "the same failure
returns at the next gate". Re-judged after the run, Z is an acceptable answer
for it; counting that, the narrow wording scores 13/20 and 12/20 against the
baseline's 13/20 and 13/20. The second run's other miss
(`lrn-20260905T173141084473Z-c`, U to B) gave Z no probability and is run-to-run
variation. Ground truth in `../2026-10-02-question-design/` is unchanged.

Feedback items under the narrow wording: agent-feedback-log #475, #1068, #1686
and #1266 go to Z (p 1.0, 0.75, 0.99, 0.6); #1419 and #904 stay `other`.
Before Z, #475 and #1068 were `other`, #1686 was N and #1266 was E.

Source: inferred by agent from agent-feedback-log#475 and #1068 (independent
sessions, 2026-10-10 and 2026-10-25), 2026-11-05.
