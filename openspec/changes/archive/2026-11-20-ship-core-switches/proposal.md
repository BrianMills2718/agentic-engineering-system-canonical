## Why

Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first minimal core milestone". The minimal core (`docs/planning/minimal-core-2026-11-20.md` section 6, step 6) merges with `ship` running `make check` and the core checks only; the planning gate and the one-page-plan gate are add-ons (section 5). Today `ship` runs every gate in every repository, with no switch: on 2026-11-20 it refused #990 until the new module was named in the system map. Section 6 step 2 also says the hidden acceptance tests "must pass before `ship`", and nothing enforces that yet (#990 left it to this slice).

## What Changes

- **Switches**: `ship` reads two keys from `.copier-answers.yml` on the default branch (so a branch cannot switch its own gates off) (the copier answers file, the one switch named in section 7): `ship_planning_gate` and `ship_one_page_plans`. `false` turns that gate off for the repository and ship prints `ship: <gate>: off (.copier-answers.yml <key>: false)`. A missing file, a missing key, or any other value leaves the gate on, so every repository behaves as before until its answers say otherwise.
- **Hidden acceptance gate (core)**: after the catch-up rebase, ship reads the run records `lockstep accept check` writes (`${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/<run id>/summary.json`, spec plan-run) for this branch (same branch name, or a recorded head on this branch). When there is one, the newest must show the hidden tests ran and passed (`accept.exit` 0), nothing uncommitted, and `head` equal to the HEAD being merged; otherwise ship refuses with nothing pushed and says to run `lockstep accept check <change>` again. With no record, ship prints `ship: no hidden-test run recorded for this branch` and goes on.

## Test seam

- `addon_on(repo: Path, key: str) -> bool`.
- `accept_refusal(run, repo, branch) -> str | None`.
- `ship.main([...])` against the existing throwaway repository, bare remote and fake gh in `tests/test_ship.py`; run records are written under `$XDG_STATE_HOME` by the test.

## Out of scope

Installing `ship` with `uvx`, the public hooks file, the prior-art script's private location, and the template's answers are the next slices.

## Impact

- `scripts/ship.py`, `tests/test_ship.py`, spec `openspec/specs/ship/spec.md`.

Plan size: small
