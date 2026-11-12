# `lockstep plan check` (one-tool design, slice 5)

## Why

Brian approved one planning-and-checking tool (`proposals/one-planning-tool/DESIGN.md`; Brian, 2026-11-11:
"i approve single tool desing re d4"). Slice 5 moves the plan-format checks out of Company Planning's package
validator (company-planning at b8a53a0) so the acceptance and requirement format is defined in one place.

## What changes

- New module `src/lockstep/plan_check.py` and the command `lockstep plan check [--repo PATH] [--acceptance PATH] [--json]`.
- It validates `docs/planning/acceptance-criteria.json` (ported from `validate_planning_package._check_acceptance`) and,
  when the file records Brian's words and a stored coverage judgment, that every requirement is sourced in his words and
  covered or deferred by him (ported from `coverage_check.check`, `quote_in_words`, `staleness`, without the model call).

## Not in this change

The review page, diagrams, cold review, freshness, goal provenance and the model call that makes a coverage judgment stay in
Company Planning. Company Planning is not changed. Nothing in the ported checks reads Brian's machine, so `lockstep.yaml`
gets no new key.
