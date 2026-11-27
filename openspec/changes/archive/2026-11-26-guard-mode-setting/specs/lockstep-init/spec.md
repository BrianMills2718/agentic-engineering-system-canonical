## MODIFIED Requirements

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

## ADDED Requirements

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
