# lockstep-init Specification

## Purpose

`lockstep init` installs Lockstep in a repository with one command: `lockstep.yaml`, the Claude Code and Codex edit-guard hooks and a lefthook pre-commit command, written only when absent and with no absolute path; the edit guard logs outside the checkout, under `${XDG_STATE_HOME:-~/.local/state}/lockstep/<repository name>/` (`proposals/one-planning-tool/DESIGN.md`, slice 6; issue #974).

## Requirements

### Requirement: Init installs Lockstep in a repository without overwriting

`lockstep init` SHALL write, for each of these that is absent, `lockstep.yaml` (a `checks:` map setting every commit check to `block` except `maintainability`, `helper-reuse` and `mutation`, which it writes as `off` with a comment saying what each does, `owner`, `sources.human_pattern`, a `planning:` section setting `gate` and `one_page_plans` to `block` with a comment saying what each does, a `guard:` section setting `mode` to `block` with a comment saying what it does, empty `governed` and `layout`), a Claude Code PreToolUse hook in `.claude/settings.json`, a Codex PreToolUse hook in `.codex/hooks.json`, neither setting `PCW_MODE`, and a `lockstep` pre-commit command in `lefthook.yml` (which leaves those three out). It SHALL print one line per file it wrote or skipped, SHALL leave an existing `lockstep.yaml` unchanged, SHALL add its hook to an existing settings or hooks file without removing other keys, and a second run SHALL change nothing.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (the three written off); Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off" (the planning section, docs/planning/next.goal.md slice 1, and the guard section, parking item `guard.mode`); Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, "A concrete example of the finished tool" step 1. Writing `block` so a fresh install refuses as the hardcoded `PCW_MODE=block` did is inferred by agent.

#### Scenario: Fresh repository gets all four

- **GIVEN** an empty git repository
- **WHEN** `lockstep init` runs
- **THEN** `lockstep.yaml`, `.claude/settings.json`, `.codex/hooks.json` and `lefthook.yml` exist and each names Lockstep,
  and `lockstep.yaml` sets every check to `block` except `maintainability`, `helper-reuse` and `mutation`, set to `off`, `planning:` sets `gate` and `one_page_plans` to `block`, `guard:` sets `mode` to `block`, and no hook command holds `PCW_MODE`

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

### Requirement: Init upgrades its own old hook command only where lockstep.yaml sets the guard

When a settings or hooks file holds the edit-guard command an earlier `lockstep init` wrote (exactly `PCW_MODE=block uvx --from <source> lockstep-hook`, with its client prefix or suffix), `lockstep init` SHALL rewrite that command to the current one when the repository's `lockstep.yaml` has a `guard:` section, and SHALL otherwise leave it unchanged and print a line saying to add `guard: {mode: block}` to `lockstep.yaml` and run `lockstep init` again. Any other Lockstep hook command SHALL be left unchanged.

Source: inferred by agent: dropping the hardcode without this would leave installed repositories with `PCW_MODE=block`, which wins over `guard.mode`, while rewriting it in a repository whose `lockstep.yaml` has no `guard:` would silently turn its refusals into warnings; the same exact-match rule `lockstep init` already uses for its lefthook command.

#### Scenario: An old hook command is upgraded where guard is set

- **GIVEN** `.claude/settings.json` holding the old `PCW_MODE=block` command and `lockstep.yaml` with `guard: {mode: block}`
- **WHEN** `lockstep init` runs
- **THEN** the command no longer holds `PCW_MODE`, the file is reported as written, and a second run reports it skipped

#### Scenario: An old hook command stays where guard is not set

- **GIVEN** `.claude/settings.json` holding the old `PCW_MODE=block` command and `lockstep.yaml` with no `guard:` section
- **WHEN** `lockstep init` runs
- **THEN** the command is unchanged and the output says to add `guard: {mode: block}`

#### Scenario: A custom hook command is left alone

- **GIVEN** `.claude/settings.json` holding a `lockstep-hook` command init did not write and `lockstep.yaml` with `guard:`
- **WHEN** `lockstep init` runs
- **THEN** the command is unchanged
