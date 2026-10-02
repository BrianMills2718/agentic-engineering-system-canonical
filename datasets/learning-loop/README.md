# Learning loop datasets

Design: `proposals/aes-learning-loop/DESIGN.md`.

## legacy-learnings-labelled.jsonl

The 2,572 entries of the legacy learnings register
(`BrianMills2718/project-meta` `learnings/entries/*.json`, read 2026-10-02),
labelled once by Jev with question set **v1** (`scripts/learning_loop/label_items.py`).
It is kept as a file, not as 2,572 GitHub issues; see the design's "Decisions".

One record per entry: `entry_id`, `recorded_at`, `project`, `text` (first 600
characters), `outcome` (`fact` | `filed` | `unsorted`), `family`, `p`, `confidence`,
`is_failure`, `fits_well`, `second`, `cost`, or `error` when the call failed.

- Model: `typesafe/jev-1.13` through OpenRouter `/api/v1/systemone`.
- Thresholds (v1): `is_failure < 0.7` → fact; family `p ≥ 0.6` → filed; otherwise unsorted.
- Taxonomy: `docs/failure-modes.md`, copied from `agent-skills/skills/review/references/failure-modes.md`
  (sha256 `4a2032d3d91be0147e4c5e00fb4038de1d44be41e8fc025741ef053345433143` at copy time).
- Report: `python3 scripts/learning_loop/label_items.py report --in datasets/learning-loop/legacy-learnings-labelled.jsonl`.
