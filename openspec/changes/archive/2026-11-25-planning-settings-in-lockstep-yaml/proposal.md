# Planning settings in lockstep.yaml

## Why

Brian, 2026-11-25: "yes it should hold all 4 parts btu the whole systm should be configurable so you can congfigure
what is on or off or any other settings. for any piece". Today the planning part's two `ship` gates switch only from
`.copier-answers.yml`, which only repositories made from the template have, and they can only be on or off. Every AES
repository has `lockstep.yaml` (`lockstep init` writes it), so the planning part's settings belong there beside the
commit checks. Plan: `proposals/aes-whole-system/PLAN.md`, slice 1.

## What changes

- `lockstep.yaml` gains `planning: {gate, one_page_plans}`, each `block`, `warn` or `off` (bare YAML booleans
  normalized as in `checks:`).
- `ship` reads them from `lockstep.yaml` on the default branch at origin, never from the branch being shipped. The
  copier keys are still read; either one saying off turns the gate off.
- `warn` turns a plan verdict (validator rejection, missing package, incomplete one-page plan, plan-list refusal) into
  a printed warning; a validator that cannot be fetched or run still refuses, since that is not a verdict.
- `lockstep init` writes the `planning:` section with both set to `block` (today's behavior).
- `side_file.py` accepts the `planning`, `guard`, `rules`, `feedback` and `mutation` top-level keys.

## Impact

`src/lockstep/checks/config.py`, `src/lockstep/ship.py`, `src/lockstep/init_repo.py`, `src/lockstep/side_file.py`
and their tests. A repository with no `planning:` section behaves as before.
