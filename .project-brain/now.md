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
in the README and the progress log.

**Next step:** follow "Exact next action" in the roadmap. In short: the
Coordinator keeps taking jobs from the refreshed weekly plan; the terminal
session merges AES pull requests (this repo's own hook refuses runner merges)
and keeps the roadmap current; the remaining v1 conditions are evidence that
accrues on its own (a rule blocking real work, seven quiet days, a pick-up
retest after each rewrite of the roadmap).

**Rule for every agent:** read this file first. When your change moves where
the project stands, update `now.md` (and `state.md` if needed) in the same pull
request. `python3 scripts/hive/brain_fresh.py .` exits 1 when this brain is
older than the work since.
