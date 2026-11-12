# lockstep-init Specification

## Purpose

`lockstep init` installs Lockstep in a repository with one command: `lockstep.yaml`, the Claude Code and Codex edit-guard hooks and a lefthook pre-commit command, written only when absent and with no absolute path; the edit guard logs to `.lockstep/` (`proposals/one-planning-tool/DESIGN.md`, slice 6).

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

Files `lockstep init` writes SHALL contain no absolute path and no `/home/`; the hook commands SHALL install Lockstep from a git address with `uvx`. `--owner` SHALL set `owner:` in `lockstep.yaml`, else the owner of the git `origin` remote, else a placeholder. The checks SHALL read their modes, `owner` and `sources.human_pattern` from `lockstep.yaml`, so a file copied from one repository works in another.

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

### Requirement: The edit guard logs to .lockstep

The edit guard SHALL append its decision log to `.lockstep/hook-<date>.jsonl` in the project, and `lockstep-hook --would-block` SHALL count records in both `.lockstep/` and the older `.pcw/`.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md names `.lockstep/`

#### Scenario: A decision is logged under .lockstep

- **GIVEN** a project with the edit guard installed
- **WHEN** it decides on an edit
- **THEN** `.lockstep/hook-<date>.jsonl` holds the record and `.pcw/` is not created
