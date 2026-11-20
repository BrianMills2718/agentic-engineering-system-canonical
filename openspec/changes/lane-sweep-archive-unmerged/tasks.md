## Tasks

- [x] Tests first: clean idle unmerged lane archived and removed with the branch kept; detached lane gets an archive ref; tip on a remote branch needs no bundle; dirty and locked unmerged lanes kept; unmerged lane under the limit kept (also with `--merged-lane`); report-only run writes nothing; failed bundle verify keeps the lane; push only to a private repository of the configured owner; limit from graph-config; kept count per repository
- [x] `judge` returns whether a lane needs archiving; `archive_and_remove`, `push_archive_ref`, `remove(keep_branch=True)` and the per-repository count in `scripts/lane_sweep.py`
- [ ] Run `make check` (blocked on 2026-11-19: the storage guard refuses every `git worktree add`, the tests' too, while C: is under its reserve)
- [ ] Archive the change, `lockstep check project`, `ship`
- [ ] Add `lane_sweep_archive_after_hours: 72` to aes-config `graph-config.yaml` (the code defaults to 72 without it)
