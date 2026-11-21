## MODIFIED Requirements

### Requirement: Remove finished lanes and report the rest

`scripts/lane_sweep.py` SHALL, for every linked worktree of each repository it is given (default: every
repository under `~/code2`), remove the worktree and delete its local branch only when all hold: the tree
has no uncommitted changes (ignored files do not count); its content is on the remote default branch,
meaning the branch tip is an ancestor of it, or every file the branch changed has the same content there, or a merged pull request's head on GitHub is exactly the branch tip;
no running process outside the sweep's own ancestors and session (the command that launched it) uses the worktree, meaning its working directory, a command-line argument, an open or mapped file, a code search path in its environment (`PYTHONPATH`, `VIRTUAL_ENV` and similar) or an absolute path in a `.pth` file of the Python environment it runs from is inside the worktree;
and the worktree has been idle for at least 30 minutes, or 24 hours when the branch has no commits of
its own; and its ignored files that are not regenerable caches total under 1 MiB (1048576 bytes), where a cache
is anything under a folder named `.venv`, `venv`, `node_modules`, `__pycache__`, `.pytest_cache`, `.mypy_cache`,
`.ruff_cache`, `.tox`, `dist`, `build`, `.cache`, `.next`, `target`, `.lockstep`, `.code2check` or `.work`, or an
`.egg-info` folder, at any depth; a size that cannot be read SHALL count as reaching the limit. A lane failing
only this check SHALL be kept with the reason `holds ignored non-cache files: <up to 5 paths>`, because
`git worktree remove` deletes ignored files even without `--force`; a removed lane's smaller ignored non-cache
files SHALL be listed in the day's log. Every other lane SHALL be kept and listed with the reason, except an idle lane whose content is not on the
remote default branch, which the requirement "Archive then remove idle unmerged lanes" governs. Each removal SHALL append the branch
name, its tip and the command that restores the branch to one log file per day. Removal SHALL first
move the worktree aside with `git worktree move` to the hidden sibling `.<name>.lane-sweep-removing`, so
the lane's own path disappears in one step, and SHALL then run `git worktree remove` without `--force`.
When the move fails nothing is changed. When a process uses the moved tree, a folder in it cannot be
written, or the removal fails while the moved tree's tracked files are intact, it SHALL be moved back. When the removal fails after deleting
files, the remains SHALL stay at the hidden path, the branch SHALL be kept, and the log SHALL name the
command that recreates the lane; a later sweep SHALL keep and list such a hidden path. A git command that
times out SHALL count as a failed step and SHALL NOT stop the sweep. Without `--apply` it
SHALL only report. Worktree records whose folder is gone SHALL be pruned. `scripts/ship.py` SHALL run
the sweep for its repository right after the pull request reads back MERGED, passing its own lane as
`--merged-lane` so that lane skips only the idle wait; a failed sweep SHALL NOT fail the ship.

Source: Brian, 2026-10-25, "i guess if thats th ebest way to do it but i feel like there should be a way to do it more immeidately" (approving automatic removal of clean worktrees whose content is on main, after "i dont udnerstand why we always ahve these old branches that arent celanedup and handled automatically")

Source: inferred by agent from the coordinating session's brief of 2026-11-20 for this change: the 2026-11-19 manual removal of 86 lanes found ignored work that a removal would have deleted in real lanes (`.claude/hook_log.jsonl`, `*.db`, `*-wal`, `*-shm`, `var/`, `results/`, `data/`, `openspec/changes/archive/`, `site/`); the 1 MiB allowance and the cache list are from that brief.

Source: inferred by agent from the 2026-10-27 lane-sweep log: the sweep removed `~/code2/data-contracts-wt/claimant` (03:01:04) and `~/code2/claim-extraction-wt/efficiency` (03:58:49) while live greer runs imported from them through `PYTHONPATH`, and the second removal stopped partway, leaving a registered worktree with its tracked files deleted.

#### Scenario: A clean lane whose commits are on main is removed

- **GIVEN** a clean worktree whose branch tip is an ancestor of origin/main and idle past the limit
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder and the local branch are gone

#### Scenario: A squash-merged lane is removed

- **GIVEN** a clean worktree whose commits are not ancestors of origin/main but every file it changed has the same content on origin/main
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder and the local branch are gone

#### Scenario: A lane with uncommitted changes is kept

- **GIVEN** a worktree with an uncommitted edit
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported as having uncommitted changes

#### Scenario: A lane with work not on main is kept

- **GIVEN** a clean worktree with a commit whose change is not on origin/main, idle for less than the archive limit
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree and branch stay and the lane is reported as not on main

#### Scenario: A lane a process is working in is kept

- **GIVEN** a finished worktree that a running process has as its working directory
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported as in use

#### Scenario: A lane a systemd unit runs from is kept

- **GIVEN** a finished worktree that a systemd user unit's file names, and no running process using it
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported with the unit's name

#### Scenario: A lane a process runs code from is kept

- **GIVEN** a finished worktree and a process started outside it whose arguments, open files or mapped files are inside it (for example `<lane>/.venv/bin/python <lane>/script.py`)
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported as in use (code2-workspace#65)

#### Scenario: The command that launched the sweep does not hold the lane

- **GIVEN** a finished worktree whose only process is in the sweep's own session, such as the other end of `ship | tail`
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder and the local branch are gone

#### Scenario: A new lane with no commits is kept

- **GIVEN** a clean worktree created minutes ago whose branch has no commits of its own
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported as recently active

#### Scenario: A removal can be undone

- **WHEN** the sweep removes a lane
- **THEN** the day's log names the branch, its tip and a `git branch <name> <tip>` command that restores it

#### Scenario: Without apply nothing changes

- **GIVEN** a finished worktree
- **WHEN** the sweep runs without `--apply`
- **THEN** the worktree stays and is reported as removable

#### Scenario: A shipped lane is removed right after merge

- **GIVEN** a clean worktree whose pull request `scripts/ship.py` has just merged
- **WHEN** the merge reads back MERGED
- **THEN** ship runs the sweep and the worktree folder and its local branch are gone

#### Scenario: A lane at a merged pull request head is removed

- **GIVEN** a clean, idle worktree whose files main has changed since its pull request merged
- **AND** GitHub reports a merged pull request for its branch whose head is the lane's tip
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder and the local branch are gone

#### Scenario: A lane a process imports from is kept

- **GIVEN** a finished worktree and a process started outside it, holding no file in it open, whose `PYTHONPATH` names a folder inside it
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported as in use

#### Scenario: A lane an editable install points into is kept

- **GIVEN** a finished worktree and a Python process started outside it from a virtual environment whose `.pth` file names a folder inside the worktree
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported as in use

#### Scenario: A removal that fails partway leaves no half tree at the lane's path

- **GIVEN** a finished worktree whose deletion stops partway for a reason the sweep cannot check first
- **WHEN** the sweep runs with `--apply`
- **THEN** it exits 1, the lane's path no longer exists, the remains sit at `.<name>.lane-sweep-removing`, the branch is kept, and the logged command recreates the lane

#### Scenario: A lane with a folder that cannot be written is kept whole

- **GIVEN** a finished worktree containing a folder this user cannot write, so deletion would stop partway
- **WHEN** the sweep runs with `--apply`
- **THEN** it exits 1, logs that the folder cannot be written, and the worktree is back at its path with its files and branch

#### Scenario: A removal that times out leaves the lane whole

- **GIVEN** a finished worktree whose `git worktree remove` times out before deleting anything
- **WHEN** the sweep runs with `--apply`
- **THEN** it exits 1 after logging its summary line, and the worktree is back at its path with its files and branch

#### Scenario: A lane holding ignored non-cache files is kept

- **GIVEN** a finished, idle worktree holding ignored `data/x.db` (2 MiB) and `var/state.db-wal`
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree and branch stay and it is reported as `holds ignored non-cache files:` naming `data/` and `var/`

#### Scenario: Ignored non-cache files under 1 MiB do not keep a lane

- **GIVEN** a finished, idle worktree whose only ignored non-cache file is a small `.claude/hook_log.jsonl`
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree is removed and the day's log lists `.claude/` among the ignored files the removal deletes

#### Scenario: Regenerable caches do not keep a lane

- **GIVEN** a finished, idle worktree holding 2 MiB each under `.venv/`, `pkg/__pycache__/` and `build/`
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree is removed

## ADDED Requirements

### Requirement: Archive then remove idle unmerged lanes

`scripts/lane_sweep.py` SHALL remove the worktree of a lane whose content is not on the remote default branch
when it passes every other check of "Remove finished lanes and report the rest" (clean, ignored non-cache files under 1 MiB, not in use by a process
or a systemd user unit, not locked, not passed as `--keep-lane`, no submodules) and has been idle for at least
the archive limit: 72 hours, or the number of hours in `lane_sweep_archive_after_hours:` in `graph-config.yaml`
(`$LANE_SWEEP_ARCHIVE_AFTER_HOURS`, `--archive-after-hours`); 0 or less SHALL turn this off. `--merged-lane`
SHALL NOT shorten this wait. Before any move it SHALL preserve the tip: when no remote-tracking branch holds the
tip, it SHALL create the local ref `refs/archive/<YYYYMMDD>/<lane folder name>` at the tip with `git update-ref`
refusing to overwrite (a name already taken by another commit gets `-<tip>` appended), write a `git bundle` of
that ref and the lane's branch holding only the commits not on the remote default branch into the log folder,
and run `git bundle verify` on it. A detached lane SHALL get the local ref even when a remote-tracking branch
holds its tip. When creating the ref, the bundle or its verification fails, the lane SHALL be kept whole and
the sweep SHALL exit 1. The ref SHALL be pushed to origin only when origin's GitHub owner is the `owner:` setting
and GitHub, asked through that owner's gh wrapper, reports the repository private; a failed push SHALL be logged
and SHALL NOT stop the removal. The removal SHALL then run as in "Remove finished lanes and report the rest",
except that the local branch SHALL be kept. The day's log SHALL name the branch, the tip, the bundle and the
command `git -C <repo> worktree add <path> <branch, or the archive ref when detached>` that restores the lane, and
SHALL list the ignored files the removal deletes, other than rebuildable caches such as `.venv`. Without
`--apply` the lane SHALL only be listed as archivable, with no ref and no bundle written.

Source: inferred by agent (the coordinating session's brief of 2026-11-19 for this change, with what it measured on Brian's machine that day: `~/code2`
had 136 worktrees using about 23 GB (mostly a `.venv` per lane), the 21:00 sweep kept 188 lanes and removed 0
because each was "work not on origin/main", and 47 lanes had their last commit on 2026-11-13 (one fan-out day,
29 of them in one repository) and were never merged; 86 were removed by hand with this procedure, which this
requirement automates). Also inferred by agent: that a ref is pushed only to a private repository (a tip no remote
branch holds was never published; the 2026-11-09 world-substrate archive, `~/code2/.lane-sweep-logs/
world-substrate-old-lanes-2026-11-09.remove.sh`, pushed its refs only because every tip was already public), that
the owner is the `owner:` setting rather than a name in code (requirement "settings-come-from-config"), that the
bundle holds only the commits not on the default branch (a full-history bundle per lane would spend the disk this
change frees), and that a detached lane always gets its local ref (the sweep fetches without `--prune`, so a
remote-tracking ref may name a branch GitHub no longer has).

#### Scenario: An unmerged lane holding ignored non-cache files is kept and not archived

- **GIVEN** a clean worktree with a commit not on origin/main, idle past the archive limit, holding ignored `site/index.html` (2 MiB)
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays, reported as `work not on origin/main; holds ignored non-cache files: site/`, and no archive ref or bundle is written

#### Scenario: A clean idle unmerged lane is archived and removed with its branch kept

- **GIVEN** a clean worktree with a commit not on origin/main, on no remote branch, idle past the archive limit
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder is gone, the branch stays at its tip, `refs/archive/<YYYYMMDD>/<name>` points at the tip, a verified bundle is in the log folder, and the logged `git worktree add` command brings the lane back

#### Scenario: A detached unmerged lane gets an archive ref

- **GIVEN** a clean, idle, detached worktree with a commit not on origin/main
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder is gone, `refs/archive/<YYYYMMDD>/<name>` points at its tip, and the logged command restores it from that ref

#### Scenario: An unmerged lane whose tip is on a remote branch needs no bundle

- **GIVEN** a clean, idle worktree whose branch tip is pushed to origin but not on origin/main
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder is gone, the branch stays, no archive ref or bundle is written, and the log names the remote branch

#### Scenario: A dirty unmerged lane is kept

- **GIVEN** an idle worktree with a commit not on origin/main and an uncommitted edit
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree and its edit stay, it is listed as having uncommitted changes, and no archive ref is written

#### Scenario: A locked unmerged lane is kept

- **GIVEN** an idle worktree with a commit not on origin/main, locked with `git worktree lock`
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays, it is listed as locked, and no archive ref is written

#### Scenario: An unmerged lane idle less than the limit is kept

- **GIVEN** a clean worktree with a commit not on origin/main, idle 71 hours, passed as `--merged-lane`
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is listed as not on main, to be archived after 72 hours idle

#### Scenario: Without apply an unmerged lane is only reported

- **GIVEN** a clean worktree with a commit not on origin/main, idle past the archive limit
- **WHEN** the sweep runs without `--apply`
- **THEN** the worktree stays, it is listed as archivable and counted in the summary, and no ref or bundle is written

#### Scenario: A bundle that fails to verify keeps the lane

- **GIVEN** a clean, idle unmerged worktree whose bundle `git bundle verify` rejects
- **WHEN** the sweep runs with `--apply`
- **THEN** it exits 1, the worktree, its files and its branch stay, and the log says the verify failed

#### Scenario: An archive ref is pushed only to a private repository of the configured owner

- **GIVEN** a clean, idle unmerged lane, `owner:` set, and origin a GitHub repository
- **WHEN** the sweep runs with `--apply`
- **THEN** the archive ref reaches origin when origin's owner is `owner:` and the repository is private, and not when the owner differs or the repository is not private; the lane is removed in every case

#### Scenario: The archive limit comes from graph-config

- **GIVEN** `graph-config.yaml` with `lane_sweep_archive_after_hours: 0`
- **WHEN** the sweep runs with `--apply` over a clean unmerged lane idle 73 hours
- **THEN** the lane stays and is listed as not on main; with no setting the limit is 72 hours

### Requirement: Count kept lanes per repository

After the kept lanes, `scripts/lane_sweep.py` SHALL print, and append to the day's log and `last-report.txt`, one
line `lanes kept per repository:` naming each repository that keeps at least one lane with its count, largest
first, and marking each count over 8 `(more than 8)`, so a repository where lanes pile up is visible in every run.

Source: inferred by agent (the coordinating session's brief of 2026-11-19: 29 of the 47 lanes left unmerged
since 2026-11-13 were in one repository, and nothing in the sweep's output showed it).

#### Scenario: The sweep counts kept lanes per repository

- **GIVEN** a repository with nine kept lanes
- **WHEN** the sweep runs
- **THEN** its output and the day's log have the line `lanes kept per repository: <repository> 9 (more than 8)`
