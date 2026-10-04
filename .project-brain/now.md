# Now (2026-10-04, hive-brain session)

**Stopped at (2026-10-04 05:50 UTC):** hive brain v1 has five merged jobs
(condition 1 of 5 met), a hosted dashboard (https://hive.brianmills.dev), a
phone channel both ways (the relay on personal-vps), and Brian's merge rule of
2026-10-04 (no merge needs his yes unless a surface is out with other people
for review; irreversible actions still ask). The plan was rewritten the same
morning: `proposals/hive-brain-v1/ROADMAP.md` holds the current state and
`proposals/hive-brain-v1/PROGRESS_LOG.md` the chronicle with evidence. In this
repository, all three `make` gates pass from a clean clone with the README's
install line since PRs #110, #112 and #118 (2026-10-04); the measurements are
in the README and the progress log. That install line is now `uv venv .venv &&
uv pip install -e ".[dev]"` (2026-10-04), not `python3 -m venv` plus `pip`:
Brian's standing preference is uv with its shared cache in every repository.
The Makefile needed no change, because `$(PYTHON)` only ever consumed
`.venv/bin/python` and never created it. `docs/greenfield/GETTING_STARTED.md`
still says venv plus pip on purpose — it is a planned artifact named in three
external clean-user observations, so changing it goes through AES, not a docs
edit.

**Next step:** follow "Exact next action" in the roadmap. In short: the
Coordinator keeps taking jobs from the refreshed weekly plan; agents merge
their own AES pull requests with `gh pr merge <n> --merge`, which this repo's
hook has accepted since PR #126 (it still refuses `--squash` and `--rebase`),
and keep the roadmap current; the remaining v1 conditions are evidence that
accrues on its own (a rule blocking real work, seven quiet days, a pick-up
retest after each rewrite of the roadmap).

**Rule for every agent:** read this file first. When your change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request. `python3 scripts/hive/brain_fresh.py .` exits 1 when this brain is
older than the work since.
