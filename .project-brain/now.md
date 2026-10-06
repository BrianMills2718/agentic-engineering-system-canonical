# Now (2026-10-04, hive-brain session)

**Stopped at (2026-10-04 16:20 UTC):** hive brain v1 has seven merged jobs;
conditions 1 (pilot) and 3 (learning loop) are met. Rule K1 blocked real work
and its wrong block came back as friction issue #137. Still open: governance
firing inside a pilot job (condition 2), seven clean days (condition 4, earliest
2026-10-10), and a fresh-reader test of the plan (condition 5). Since 08:47 UTC
the Coordinator has been stopped by the Claude weekly usage limit; it should
resume after the 17:00 UTC reset. The hosted dashboard
(https://hive.brianmills.dev) now opens a panel for every map box, explains
every label, reloads itself and has a laptop layout (#136). The plan:
`proposals/hive-brain-v1/ROADMAP.md`; the chronicle with evidence:
`proposals/hive-brain-v1/PROGRESS_LOG.md`.

**Install path.** In this
repository, all three `make` gates pass from a clean clone with the README's
install line since PRs #110, #112 and #118 (2026-10-04); the measurements are
in the README and the progress log. That install line is now `uv venv .venv &&
uv pip install -e ".[dev]"` (2026-10-04), not `python3 -m venv` plus `pip`:
Brian's standing preference is uv with its shared cache in every repository.
The Makefile needed no change, because `$(PYTHON)` only ever consumed
`.venv/bin/python` and never created it. `docs/greenfield/GETTING_STARTED.md`
now installs with uv too (BRI-36, 2026-10-04), so no venv-plus-pip install path
is left in this repository: the page was run end to end from an empty directory
at `d89fe2e` and recorded as `OBS-AES-CLEAN-USER-d89fe2e`, which supersedes the
three earlier clean-user observations, and the clean-install test in
`tests/greenfield/test_distribution.py` builds its throwaway venv with uv
instead of stdlib `venv` plus `pip` (so it needs no `ensurepip`; it skips only
where uv is missing). That observation assesses `ER-SC-GF-001-01` INCONCLUSIVE
rather than SUPPORTS on purpose: the runner was the session that wrote the
change, not an independent fresh reader, so it proves the page's commands work
and not that the page reads well cold. Restoring SUPPORTS needs one fresh
session given only the page and a pin — the open follow-up on the install path.

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


## Standing policy update — 2026-10-06

AES capability sourcing now treats **apparent novelty as unresolved search debt**, not as a positive design signal. When a needed capability or abstraction appears to have no established owner, the expected response is increased sourcing pressure: try alternate terminology and standards, adjacent disciplines/ecosystems, structural analogues, mature compositions/adapters, internal/historical attempts, failed approaches, and requirement/frame challenge before authorizing bespoke implementation. The more consequential and apparently novel the machinery, the stronger the burden to falsify the novelty claim and shrink the residual gap. Custom construction is a last-resort bounded residual, not an achievement in itself.

This policy is encoded in `docs/architecture/SYSTEM_BOUNDARY.md` under AES-CAP-002 and surfaced in `docs/plans/TEMPLATE.md` as an apparent-novelty check plus residual-invention declaration.
