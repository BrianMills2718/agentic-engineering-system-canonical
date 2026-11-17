## ADDED Requirements

### Requirement: A worktree is removed only on proof its branch landed

`scripts/prune_merged_worktrees.py` SHALL remove a linked worktree and its branch only when the forge shows a merged
pull request for that exact branch whose merge commit is on the local default branch, or when merging the branch into
the default branch would change no file. Every other worktree SHALL be kept and printed with the reason. A path given
with `--exclude` SHALL be kept even when proven merged; `--dry-run` SHALL remove nothing; `--help` and any unknown flag
SHALL remove nothing.

Source: inferred by agent, carried over unchanged from Project Meta `b743c308a` (the incidents of 2026-09-07, 2026-09-08
and 2026-09-15 are in the script and its tests).

#### Scenario: proven-merge-only

- **WHEN** a worktree's branch adds nothing to the default branch and the worktree is passed with `--exclude`
- **THEN** the worktree and its branch are kept and the output says `excluded: caller protection`; without
  `--exclude` the same worktree is removed, and with `--help` or `--dryrun` it is kept
