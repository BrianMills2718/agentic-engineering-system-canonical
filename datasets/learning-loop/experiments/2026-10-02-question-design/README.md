# Jev question-design test (2026-10-02)

How should Jev (typesafe/jev-1.13) be asked to sort a learning into the failure
families of `docs/failure-modes.md`? Lesson and discussion: issue #64.

**Ground truth.** These are my (Claude's) judgments of which families are
acceptable for each item, not Brian's:
- `gt.tsv` holds 30 items. Some v2 option wording was written after seeing
  misses on these, so they are partly tuned on.
- `holdout_gt.tsv` holds 20 fresh items (`holdout_ids.json`, seed 20261003),
  judged before any run.
- `synthetic.json` holds 4 invented failures that no family covers, to test
  `other`.

| Design | Files | Tuned 30 | Held-out 20 |
|---|---|---|---|
| One yes/no question per family | `ml.py`, `ml_out.jsonl` | top 12/29 | — |
| One choice, plain-text descriptions | `sc.py`, `sc_out.jsonl` | top 18/29; 25/30 with is_failure fact rule and near-top labels | — |
| **v2: one choice, TypeSafe-style options (`what` / `not_for`), state as named fields, `other` and `not_a_failure` options** | `v2.py`, `v2lib.py`, `v2_out.json`, `holdout.py`, `holdout_out.json` | top 24/30; near-top 0.15: 25/30 | **top 13/20; near-top 0.15: 16/20 (avg 1.6 labels)** |
| Two-level hierarchy (5 groups, then family; TypeSafe hierarchical cookbook) | `hier.py`, `hier_*.json` | family 21/30 | group 12/20, family 7/20 (worse; groups overlap) |

**Other findings:**
- `other` works with v2 wording: synthetic secret leak → `other` (0.57).
  The licence violation went to U instead. The other two synthetic items got
  acceptable specific families.
- Confidence ≥ 0.9 was right 8/8 across both sets, but covers only 16% of
  items.

**Adopted:** v2 with near-top 0.15 labels. The frozen question set is
`scripts/learning_loop/question_set_v2.json`. It meets Brian's 8/10 floor on
the held-out set; it does not reach 9/10.
