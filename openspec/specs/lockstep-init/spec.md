# lockstep-init Specification

## Purpose

`lockstep init` installs Lockstep in a repository with one command: `lockstep.yaml`, the Claude Code and Codex edit-guard hooks and a lefthook pre-commit command, written only when absent and with no absolute path; the edit guard logs outside the checkout, under `${XDG_STATE_HOME:-~/.local/state}/lockstep/<repository name>/` (`proposals/one-planning-tool/DESIGN.md`, slice 6; issue #974).

## Requirements

### Requirement: Init installs Lockstep in a repository without overwriting

`lockstep init` SHALL write, for each of these that is absent, `lockstep.yaml` (a `checks:` map setting every commit check to `block`, `owner`, `sources.human_pattern`, empty `governed` and `layout`), a Claude Code PreToolUse hook in `.claude/settings.json`, a Codex PreToolUse hook in `.codex/hooks.json`, and a `lockstep` pre-commit command in `lefthook.yml`. It SHALL print one line per file it wrote or skipped, SHALL leave an existing `lockstep.yaml` unchanged, SHALL add its hook to an existing settings or hooks file without removing other keys, and a second run SHALL change nothing.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, "A concrete example of the finished tool" step 1

#### Scenario: Fresh repository gets all four

- **GIVEN** an empty git repository
- **WHEN** `lockstep init` runs
- **THEN** `lockstep.yaml`, `.claude/settings.json`, `.codex/hooks.json` and `lefthook.yml` exist and each names Lockstep

#### Scenario: A second run changes nothing

- **GIVEN** a repository `lockstep init` already ran in
- **WHEN** it runs again
- **THEN** every file is byte-identical and each is reported as skipped

#### Scenario: Existing settings keep their other keys

- **GIVEN** a `.claude/settings.json` with other keys and another PreToolUse hook
- **WHEN** `lockstep init` runs
- **THEN** those remain and the Lockstep hook is added once

### Requirement: Installed files name no machine and read their settings from lockstep.yaml

Files `lockstep init` writes SHALL contain no absolute path and no `/home/`; the hook commands SHALL install Lockstep from a git address with `uvx`. `--owner` SHALL set `owner:` in `lockstep.yaml`, else the owner of the git `origin` remote, else a placeholder. `--human-pattern` SHALL set `sources.human_pattern`, else the checks' own default. The checks SHALL read their modes, `owner` and `sources.human_pattern` from `lockstep.yaml`, so a file copied from one repository works in another.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, "Nothing names Brian's machine" and acceptance A5

#### Scenario: No written file holds an absolute path

- **GIVEN** a fresh repository
- **WHEN** `lockstep init` runs
- **THEN** no file it wrote contains `/home/`, `~/` or a path starting with `/`

#### Scenario: Owner lands in lockstep.yaml

- **GIVEN** a fresh repository
- **WHEN** `lockstep init --owner Acme` runs
- **THEN** `lockstep.yaml` says `owner: Acme`

#### Scenario: A lockstep.yaml copied to another repository is read there

- **GIVEN** a `lockstep.yaml` from `init` with one check set to `warn`
- **WHEN** it is copied into another repository
- **THEN** that repository's checks read the same modes and owner

### Requirement: The edit guard logs outside the checkout

The edit guard SHALL append its decision log to `hook-<date>.jsonl` in the folder named by `LOCKSTEP_LOG_DIR` when that is set, and otherwise in `${XDG_STATE_HOME:-~/.local/state}/lockstep/<repository name>/`, where the repository name is the main checkout's folder name for every worktree of it; `lockstep-hook --would-block` SHALL count records there and in the project's older `.lockstep/` and `.pcw/` folders.

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md named `.lockstep/`); moved outside the checkout by issue #974, inferred by agent: logs inside a worktree were deleted with it after merge and a repository without the `.gitignore` line committed them (2026-11-19). Brian, 2026-11-20, "yes" to the local proofs, whose step 1 is this fix (docs/planning/next.goal.md). Brian, 2026-11-23, "i approve" to keeping the log outside the checkout, a departure from DESIGN.md:48 listed in back-on-design slice 3.

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
