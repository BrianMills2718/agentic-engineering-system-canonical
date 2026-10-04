# State (2026-10-04)

Detail and evidence: `proposals/hive-brain-v1/ROADMAP.md` ("Where we are",
"Capabilities") and `proposals/hive-brain-v1/PROGRESS_LOG.md`. This page is the
short version.

- **Hive brain v1** (`working`): condition 1 of 5 met (five jobs merged from
  AES canonical and personal-wiki); conditions 2–5 partway.
  - Paperclip on personal-vps runs three agents (Coordinator, Research and
    Code Review, Brian Contact) on Brian's one-year token; one new job per
    6 hours, 2 open at once, taken from `weekly-plans/personal/THIS_WEEK.md`
    (refreshed 2026-10-04 with Priority 7, the hive brain's own lines).
  - Brian is reached on his phone through the relay (board thread BRI-2) and
    on https://hive.brianmills.dev. Agents merge their own work after the
    repository's checks; he is asked only for a surface he said is out with
    other people for review, or for an irreversible action (2026-10-04).
  - Terminal relay `scripts/hive/decisions.py`; silence check
    `scripts/hive/controls.py` (12 controls, daily); weekly
    `scripts/hive/readout.py` with cost per job.
  - Learning loop slices 1–2 done; rule K1 enforced since 2026-10-03; Jev
    gate in observe mode; guard mode after the 2026-10-09 log review.
  - Project brains in AES, theory-forge, cybernetic_influence_v3 and
    personal-wiki; `scripts/hive/brain_fresh.py` reports a stale one.
- **This repository's gates** (`approved` as measured 2026-10-04): `make
  check`, `make aes` and `make aes-check` exit 0 from a clean clone with the
  README's install line (PRs #110, #112, #118). The repo's own Claude Code
  hook refuses `gh pr merge` for the workers; merges happen from the terminal.
- **AES v0.2 product** (`approved` as realized, Decision 0010): governed by
  `.aes/target.yaml`; `aes status` is the one-screen view. Not the current
  focus.
