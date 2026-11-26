## Why

Brian, 2026-11-25, on whether ship's paperwork checks give more friction than value: "i agree witht he warn but we should be recoridn these so we can review them afterwards to see whether they were helpful or not and how to make the paperwork actually valuable". Nothing records how often a planning gate refuses or whether a refusal helped.

## What Changes

- An absent `planning.gate` or `planning.one_page_plans` now means `warn`, not `block`. `block` stays one line away.
- Every planning-gate run (pass, warn, refuse, unavailable, off) is appended as one JSON line to `planning-verdicts/<date>.jsonl` beside ship's day log, with repository, branch and head so a review can follow up what happened next.

## Impact

- A repository without a `planning:` section is no longer refused for a missing or failing plan; it merges with a warning. A validator that cannot be fetched or run still refuses.
- `src/lockstep/checks/config.py`, `src/lockstep/ship.py`, `tests/test_ship.py`.
