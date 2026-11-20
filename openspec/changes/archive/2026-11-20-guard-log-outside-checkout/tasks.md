## 1. Guard log outside the checkout

- [x] 1.1 Tests first: decision logged under `$XDG_STATE_HOME/lockstep/<name>/`, worktree shares the main name, `LOCKSTEP_LOG_DIR` override, old folders still counted
- [x] 1.2 `log_dir()` and `_repo_name()` in `src/lockstep/hook.py`; `_write_log` and `would_block_counts` use them
- [x] 1.3 Test fixture keeps each test's log in its own temporary folder; the end-to-end run sets `LOCKSTEP_LOG_DIR` to show the log in its project
- [x] 1.4 Note the runner coupling in the pull request that closes #974
