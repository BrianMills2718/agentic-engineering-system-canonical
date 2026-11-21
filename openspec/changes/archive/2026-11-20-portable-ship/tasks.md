## 1. Prior-art check in Lockstep

- [x] 1.1 Port code2-workspace `tests/test_prior_art_check.py` to `tests/lockstep/test_lockstep_prior_art.py` with req markers; run red
- [x] 1.2 Copy `scripts/prior_art_check.py` and `hooks/prior-art.schema.json` into `src/lockstep/`; schema path beside the module; `lockstep check prior-art` branch in `check.py`

## 2. Ship runs the bundled check

- [x] 2.1 Point the prior-art tests in `tests/test_ship.py` at the bundled check (missing file refuses; no `$SHIP_WORKSPACE`)
- [x] 2.2 `prior_art_refusal()` runs `prior_art.py` beside ship

## 3. Ship installs with uvx

- [x] 3.1 Test: `scripts/ship.py --help` and `python -m lockstep.ship --help` exit 0; `import ship` from `scripts/` is `lockstep.ship`
- [x] 3.2 `git mv` ship and lane_sweep into `src/lockstep/`; shims at the old paths; `ship` command and `jsonschema` in `pyproject.toml`
- [x] 3.3 `uvx --from <worktree> ship --help` exits 0
