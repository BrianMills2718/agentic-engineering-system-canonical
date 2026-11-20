## REMOVED Requirements

### Requirement: The edit guard logs to .lockstep

**Reason**: Logs inside the checkout were deleted with short-lived worktrees and committed by repositories without the `.gitignore` line (issue #974).

**Migration**: Replaced by "The edit guard logs outside the checkout"; `--would-block` still counts the old `.lockstep/` and `.pcw/` folders.

## ADDED Requirements

### Requirement: The edit guard logs outside the checkout

The edit guard SHALL append its decision log to `hook-<date>.jsonl` in the folder named by `LOCKSTEP_LOG_DIR` when that is set, and otherwise in `${XDG_STATE_HOME:-~/.local/state}/lockstep/<repository name>/`, where the repository name is the main checkout's folder name for every worktree of it; `lockstep-hook --would-block` SHALL count records there and in the project's older `.lockstep/` and `.pcw/` folders.

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md named `.lockstep/`); moved outside the checkout by issue #974, inferred by agent: logs inside a worktree were deleted with it after merge and a repository without the `.gitignore` line committed them (2026-11-19). Brian, 2026-11-20, "yes" to the local proofs, whose step 1 is this fix (docs/planning/next.goal.md).

#### Scenario: A decision is logged outside the checkout

- **GIVEN** a project with the edit guard installed and `LOCKSTEP_LOG_DIR` unset
- **WHEN** it decides on an edit
- **THEN** `${XDG_STATE_HOME}/lockstep/<repository name>/hook-<date>.jsonl` holds the record, the project gains no `.lockstep/` or `.pcw/` folder, and records already in the project's `.lockstep/` and `.pcw/` are still counted

#### Scenario: A worktree logs under its repository name

- **GIVEN** a worktree whose `.git` file points into `<main>/.git/worktrees/<name>`
- **WHEN** the guard picks its log folder
- **THEN** it is the same folder as the main checkout's, so the log survives the worktree's removal

#### Scenario: An override names the folder

- **GIVEN** `LOCKSTEP_LOG_DIR` names a folder
- **WHEN** the guard decides on an edit
- **THEN** the record is written in that folder and `--would-block` counts it
