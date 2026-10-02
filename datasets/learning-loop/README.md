# Learning loop datasets

Design: `proposals/aes-learning-loop/DESIGN.md`.

## legacy-learnings-labelled-v2.jsonl

The 2,575 entries of the legacy learnings register
(`BrianMills2718/project-meta` `learnings/entries/*.json`, read 2026-10-02),
labelled once by Jev with question set **v2**
(`scripts/learning_loop/question_set_v2.json`, `scripts/learning_loop/label_items.py`).
It is kept as a file, not as GitHub issues; see the design's "Decisions".

One record per entry: `entry_id`, `recorded_at`, `project`, `text` (first 600
characters), `questions`, `outcome` (`fact` | `other` | `filed`), `choice`,
`families` (every family within 0.15 of the top probability), `p`,
`confidence`, `confident` (confidence >= 0.9), `second`, `cost`, or `error`
when the call failed.

- Model: `typesafe/jev-1.13` through OpenRouter `/api/v1/systemone`.
- Run 2026-10-02:
  - outcomes: 2,429 filed (531 with several families, 402 confident), 135 fact,
    11 other;
  - 0 errors; cost $0.2496.
- Quality:
  - 16/20 on items judged before the run (`experiments/2026-10-02-question-design/`).
  - Claude's own check of the report's seeded 10-item sample: 9 acceptable.
    The miss was lrn-20260904T150750724303Z-217b34b030 (usage table inflated by
    sweeps), labelled A where L fits better.
  - Brian has not spot-checked it yet.
- The earlier v1 file (`legacy-learnings-labelled.jsonl`) is removed and
  remains in git history at commit 26b4c13.
- Taxonomy: `docs/failure-modes.md`, copied from `agent-skills/skills/review/references/failure-modes.md`
  (sha256 `4a2032d3d91be0147e4c5e00fb4038de1d44be41e8fc025741ef053345433143` at copy time).
- Report: `python3 scripts/learning_loop/label_items.py report --in datasets/learning-loop/legacy-learnings-labelled-v2.jsonl`.
