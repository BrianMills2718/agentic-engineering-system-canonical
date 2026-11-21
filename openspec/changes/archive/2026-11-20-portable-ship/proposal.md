## Why

Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first minimal core milestone". The minimal core's milestone (`docs/planning/minimal-core-2026-11-20.md` section 8) is a repository made from the template running one plan through `ship` as a second user or on a clean machine. Today that cannot happen: `ship` exists only as the link `~/.local/bin/ship` to a clone on this machine (section 7), and its prior-art gate, which stays core (Decision 1a, code2-workspace #897), reads `scripts/prior_art_check.py` from `~/code2/workspace`, a private repository.

## What Changes

- **Prior-art check moves into Lockstep** (public): `src/lockstep/prior_art.py` and `src/lockstep/prior-art.schema.json`, copied from code2-workspace `ec500633` with its rules unchanged; `lockstep check prior-art [--repo] [--since] [--files]` runs it. The module stays standard library plus `jsonschema`, so it runs as a plain file.
- **`ship` runs that copy**: it runs `src/lockstep/prior_art.py` beside itself (with `uv run --no-project --with jsonschema python`, or `$SHIP_PRIOR_ART_PYTHON`). `$SHIP_WORKSPACE` is no longer read. When the file is missing, ship refuses (fails closed, as before).
- **`ship` installs with `uvx`**: `scripts/ship.py` and `scripts/lane_sweep.py` move to `src/lockstep/ship.py` and `src/lockstep/lane_sweep.py`; `pyproject.toml` adds the command `ship = "lockstep.ship:main"`, and declares `*.json` as package data so the schema is always in the wheel. The old `scripts/` paths stay as short files that load the moved module, so the link `~/.local/bin/ship`, the daily refresh, `scripts/plan_content.py` (the push hook imports `ship` beside it) and the tests keep working. Run as a file, the shim puts `src/` on the import path and calls `main()`; imported, it makes `ship` the same module object as `lockstep.ship`, so tests that patch it still work. `lockstep.ship` imports only the standard library, so `/usr/bin/python3` still runs it.
- **Refusal text** names the schema in Lockstep, not the private workspace rule file.
- A repository made from code2-template already turns the planning gate and the one-page-plan gate off (`.copier-answers.yml`, code2-template #34), so those gates, which read `~/code2/company-planning` and `~/code2/aes-config`, do not run there.

## Test seam

- `lockstep.prior_art.main(argv) -> int`, ported tests from code2-workspace `tests/test_prior_art_check.py`.
- `ship.main([...])` with the existing throwaway repository, bare remote and fake gh in `tests/test_ship.py`; the prior-art tests there now point at the bundled check.
- One test that `/usr/bin/python3 -I scripts/ship.py --help` and `python -m lockstep.ship --help` both exit 0.

Independent read: 2026-11-20, revise then pass (cold reviewer subagent: wrong entry name, plan_content.py sibling lookup, shim run as a file, package data, remaining machine-bound gates; all fixed above).

## Out of scope

Removing code2-workspace's copy (follow-up on code2-workspace#896); moving ship's log folder default off `~/code2/.ship-logs` (a folder is created, nothing breaks); publishing code2-template.

## Impact

- New: `src/lockstep/prior_art.py`, `src/lockstep/prior-art.schema.json`, `tests/lockstep/test_lockstep_prior_art.py`.
- Moved: `scripts/ship.py`, `scripts/lane_sweep.py` into `src/lockstep/`; shims left at the old paths.
- Changed: `src/lockstep/check.py` (one CLI branch), `pyproject.toml` (command and `jsonschema` dependency), `tests/test_ship.py`, specs `ship` and `prior-art-check`, `docs/planning/system-map.md`, `wiki/lockstep.md`.

Plan size: small
