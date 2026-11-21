# lane-sweep Specification

## Purpose

Finished git worktrees (lanes) and their branches are removed automatically, minutes after their work reaches the remote default branch. A lane whose work was never merged is removed only after 72 hours idle, and only after its tip is kept in a local archive ref and a verified bundle, with its branch kept. A lane holding uncommitted changes, or 1 MiB or more of ignored files that are not regenerable caches, is never removed.

Ported into AES from code2-workspace commit eafa8e06894917f0d297e281202b60e86b12f819 (2026-11-16) under the AES consolidation plan, item 7 (Brian, 2026-11-16, Decision 25). The installed `lane-sweep` command and its timer still run the workspace copy until a side-by-side run switches them over. In the port, the gh wrapper per GitHub account and the canonical-lock tool became the person's settings (`graph-config.yaml`), not code.

## Requirements

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

### Requirement: Fast-forward primary checkouts that are clean and idle

After judging a repository's lanes, `scripts/lane_sweep.py` SHALL fast-forward the repository's primary
checkout (the main worktree, the parent of `--git-common-dir`) to the remote default branch with
`git merge --ff-only`, and only when all hold: the checkout is on the branch that the remote default
branch tracks; `git status --porcelain` is empty (ignored files do not count); the local branch is a
strict ancestor of the remote default branch after the sweep's fetch; no git command holds the checkout's
`index.lock`; and no running process outside the
sweep's own ancestors and session has its working directory inside the checkout, not counting
processes inside a linked worktree nested in it. It SHALL never reset or rebase the checkout. Each
fast-forward SHALL append the checkout, branch, old commit and new commit to the day's log. A checkout
that is behind but not moved SHALL be listed with the reason. Without `--apply` it SHALL only list the
checkout as fast-forwardable. Repositories with no lanes SHALL be fetched and judged too. A checkout
whose root folder is read-only (`canonical_lock.py` locked it while a lane claim is live) SHALL be
moved with `canonical_lock.py --sync` (unlock, `git pull --ff-only`, re-lock) instead of `git merge`.

Source: inferred by agent from BrianMills2718/company-planning#211, option (a), which the issue assigns to `scripts/lane_sweep.py`: callers run the adoption gate from `~/code2/company-planning`, which moved only when someone pulled, so the Plan 69 fix on origin/main did not reach them.

#### Scenario: A clean idle primary checkout is fast-forwarded

- **GIVEN** a primary checkout on main with no changes, behind origin/main, in a repository with no lanes
- **WHEN** the sweep runs with `--apply`
- **THEN** the checkout's main points at origin/main and the day's log names the old and new commit

#### Scenario: A primary checkout with uncommitted changes is not moved

- **GIVEN** a primary checkout behind origin/main with an uncommitted edit
- **WHEN** the sweep runs with `--apply`
- **THEN** the checkout stays at its commit and is listed as skipped for uncommitted changes

#### Scenario: A primary checkout on another branch is not moved

- **GIVEN** a primary checkout on a branch other than main while origin/main has moved
- **WHEN** the sweep runs with `--apply`
- **THEN** neither branch moves and the checkout is listed as skipped for being on another branch

#### Scenario: A primary checkout with its own commits is not moved

- **GIVEN** a primary checkout whose main has a commit that origin/main does not
- **WHEN** the sweep runs with `--apply`
- **THEN** the checkout stays at its commit and is listed as skipped for having diverged

#### Scenario: A primary checkout a process is working in is not moved

- **GIVEN** a clean primary checkout behind origin/main that a process in another session has as its working directory
- **WHEN** the sweep runs with `--apply`
- **THEN** the checkout stays at its commit and is listed as skipped for being in use

#### Scenario: A process in a lane nested in the checkout does not hold it

- **GIVEN** a clean primary checkout behind origin/main and a process working only inside a linked worktree folder nested in it
- **WHEN** the sweep runs with `--apply`
- **THEN** the checkout's main points at origin/main

#### Scenario: Without apply the checkout is only reported

- **GIVEN** a clean, idle primary checkout behind origin/main
- **WHEN** the sweep runs without `--apply`
- **THEN** the checkout stays at its commit and is listed as fast-forwardable

#### Scenario: A primary checkout with a git lock is not moved

- **GIVEN** a clean primary checkout behind origin/main whose `.git/index.lock` exists
- **WHEN** the sweep runs with `--apply`
- **THEN** it exits 0, the checkout stays at its commit, and it is listed as skipped with the lock's age

#### Scenario: A locked primary checkout moves through canonical lock sync

- **GIVEN** a clean, idle primary checkout behind origin/main whose root folder is read-only
- **WHEN** the sweep runs with `--apply`
- **THEN** it exits 0, the checkout's main points at origin/main, and the move went through `canonical_lock.py --sync`

Source of the locked-checkout rule: inferred by agent from lane-sweep's 2026-11-05 17:20 failure (process_tracing fast-forward, "unable to unlink old 'docs/CONCERNS.md': Permission denied"); Brian, 2026-11-05: "i still need your help on the 7" (the failing timers).

### Requirement: Keep lanes that a systemd user unit runs from

`scripts/lane_sweep.py` SHALL keep a lane, and report it with the unit's name, when any systemd user unit
names a path inside it in a unit file or a drop-in (`<unit>.service.d/*.conf`), on any line (for example
`WorkingDirectory`, `ExecStart` or `Environment`), whether or not a process is running from it. It SHALL read
every folder systemd loads user units from: `~/.config/systemd/user`, the transient folder
`$XDG_RUNTIME_DIR/systemd/transient` (`/run/user/<uid>` when the variable is unset), the runtime
`$XDG_RUNTIME_DIR/systemd/user`, `~/.local/share/systemd/user` and `/etc/systemd/user`. A timer's job is no
process until the timer fires, and `systemd-run --user --on-calendar` writes its unit only to the transient
folder, so reading `~/.config/systemd/user` alone lets the sweep remove a lane that a scheduled run will start
from.

Source: inferred by agent from BrianMills2718/code2-workspace#76 (the issue Brian's session filed on 2026-10-30, with its stated rule: treat as in use "any lane path appearing in a loaded user unit or pending timer's WorkingDirectory, ExecStart or Environment"); the folder list is the user-unit search path of `systemd.unit(5)`.

#### Scenario: A lane a pending transient timer runs from is kept

- **GIVEN** a finished worktree named in the `WorkingDirectory`, `Environment` and `ExecStart` of a service that `systemd-run --user --on-calendar` wrote to the transient folder, and no running process using it
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree and its branch stay and the lane is reported with the unit's name (code2-workspace#76)

#### Scenario: A lane named only in a unit's drop-in is kept

- **GIVEN** a finished worktree named only in `<unit>.service.d/*.conf`, not in the unit's own file
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree and its branch stay and the lane is reported with the unit's name

#### Scenario: A unit that names another folder does not keep a lane

- **GIVEN** a finished worktree and a unit that names only a sibling folder whose name starts with the lane's name, and the lane's parent folder
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree folder and the local branch are gone

### Requirement: Keep lanes git will not remove without force

The sweep SHALL keep a lane whose worktree contains a `.gitmodules` file and report it with the reason that git
moves and removes such a worktree only with --force, instead of attempting the removal and counting a failure.

Source: inferred by agent from the 2026-11-11 lane-sweep journal (every run failed on
`worktrees/sbm-planning-package`: "working trees containing submodules cannot be moved or removed").

#### Scenario: A lane with submodules is kept, not failed

- **GIVEN** a clean, idle worktree whose commits are on origin/main and whose tree has a `.gitmodules` file
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree and its branch stay, it is reported as containing submodules, and the sweep exits 0

### Requirement: Keep locked worktrees

`scripts/lane_sweep.py` SHALL keep a worktree that git reports as locked (`git worktree lock`), whatever else
is true of it, and SHALL report it as locked, with the lock's reason when one was given. A lock is how a tool
marks a worktree that is not a lane, such as a pinned checkout another project's Python environment imports
from: with no process running, such a worktree passes every other check and looks like a finished lane.

Source: inferred by agent from the lane-sweep logs of 2026-11-05 to 2026-11-13: the sweep removed
process_tracing's pinned llm_client checkout (`~/.local/share/process_tracing/llm_client/<revision>`) six
times, last at `~/code2/.lane-sweep-logs/2026-11-13.log:337`, after which every process_tracing test run
failed at `import llm_client` for three days. The sweep already kept locked worktrees; nothing stated or
tested it.

#### Scenario: A locked worktree is kept

- **GIVEN** a clean, idle, detached worktree whose commit is on origin/main, locked with a reason
- **WHEN** the sweep runs with `--apply`
- **THEN** the worktree stays and is reported as locked with that reason

### Requirement: settings-come-from-config

The gh command that asks GitHub for a merged pull request SHALL be `$LANE_SWEEP_GH` when set, else the
wrapper `github_accounts:` in `graph-config.yaml` (beside `$PROJECT_GRAPH`, default
`~/code2/aes-config/PROJECT_GRAPH.json`) names for the repository's owner, else the one it names for the
top-level `owner:`, else `gh`. The canonical-lock tool SHALL be `$LANE_SWEEP_CANONICAL_LOCK`, else the
`canonical_lock:` key; when neither names one, a primary checkout moves with `git merge --ff-only`.
Settings SHALL be read when needed, never at import, so a machine without the file still sweeps.

Source: inferred by agent from the AES consolidation plan item 7 task: AES is public, so account names, wrapper names and private tool paths are the person's configuration, reusing the `github_accounts:` and `owner:` keys the project-graph machinery already reads.

#### Scenario: The gh wrapper comes from graph-config

- **GIVEN** `graph-config.yaml` with `owner:`, `github_accounts:` and `canonical_lock:`
- **WHEN** the sweep picks a gh command and the lock tool
- **THEN** a listed owner gets its wrapper, an unlisted owner gets the wrapper of `owner:`, `$LANE_SWEEP_GH` wins, and the lock tool is the named path

#### Scenario: No config uses plain gh and no canonical lock

- **GIVEN** no `graph-config.yaml`
- **WHEN** the sweep picks a gh command and the lock tool
- **THEN** it uses `gh`, and no lock tool

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
