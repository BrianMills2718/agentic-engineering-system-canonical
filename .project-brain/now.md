# Now (2026-10-02, Claude Code session)

**Stopped at (2026-10-04):** pilot BRI-27 measured the cold-reader state of the
`make` gates at main `56044f0` and fixed what docs/install/Makefile can fix:
`test`/`test-quick`/`check` now run `$(PYTHON) -m pytest|mypy` instead of a bare
`pytest`/`mypy` on `PATH` (that was the exit-127 `pytest: No such file or
directory`), pytest and mypy are declared as a `[dev]` extra in
`pyproject.toml`, and the README install step installs it. That makes
`make aes-check` runnable from a clean clone; it had failed with
`.venv/bin/python: No module named pytest`, which is the `ModuleNotFoundError`
the weekly plan reported.

**All three `make` gates now exit 0 from a clean clone** (2026-10-04). The
16-19 pre-existing `mypy src/` errors that kept `make check` red — in the
retained v0.1 `repository_context/render_html.py` and in the v0.2
`cli.py`/`characterize.py`/`reconcile.py`/`planning.py` — were cleared
annotation-only under BRI-29 in PR #112, which merged on Brian's yes together
with BRI-27's PR #110. Re-measured at `c00b3e2` in a fresh clone, with only the
README's install line and nothing else on `PATH`: `make check` exit 0 (183
passed, 1 skipped; mypy clean on 20 source files), `make aes` exit 0,
`make aes-check` exit 0 (177 passed, 1 skipped). The "not green" finding in
`evidence/modular-design-integration-2026-09-22.md` is therefore superseded as
a statement about current state; it stands as the 2026-09-22 observation.
Decision 0010 is unchanged: `make check` is Enforced Planning's gate and
`make aes`/`make aes-check` are the AES gate — green is not the same as
authoritative.

**Stopped at (2026-10-03):** agents sign in again; the Coordinator started the
pilot (BRI-13, waiting on BRI-16 for the weekly plan). Done before that:
M3 slice 2, the M4 first slice (this brain, `brain_fresh.py`), the restore
check, Codex's Jev hook confirmed, and `scripts/hive/controls.py`.

**Hosted dashboard (2026-10-03):** `scripts/hive/dashboard.py --vps` builds the
page on the VPS with one-tap answers on decision cards; the server, timer and
deploy/rollback steps are personal-vps `apps/hive-dashboard/` (prepared, not
deployed yet; the deploy needs Brian's yes, already given 2026-10-03).

**Next step:** follow "Exact next action" in `proposals/hive-brain-v1/ROADMAP.md`.
In short:
1. Follow the Coordinator's first `Pilot:` task (BRI-13 comments) through
   build, Brian's review in the terminal, and merge.
2. Seed `.project-brain/` in each pilot project the Coordinator picks (done:
   AES, theory-forge, cybernetic_influence_v3; portfolio waits for another
   session's claim to clear).
3. Run `python3 scripts/hive/controls.py` at each stop (exit 0 = no control silent).

**Rule for every agent:** read this file first. When your change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request. `python3 scripts/hive/brain_fresh.py .` exits 1 when this brain is
older than the work since.
