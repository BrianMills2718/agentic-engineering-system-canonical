## MODIFIED Requirements

### Requirement: Init installs Lockstep in a repository without overwriting

`lockstep init` SHALL write, for each of these that is absent, `lockstep.yaml` (a `checks:` map setting every commit check to `block` except `maintainability`, `helper-reuse` and `mutation`, which it writes as `off` with a comment saying what each does, `owner`, `sources.human_pattern`, empty `governed` and `layout`), a Claude Code PreToolUse hook in `.claude/settings.json`, a Codex PreToolUse hook in `.codex/hooks.json`, and a `lockstep` pre-commit command in `lefthook.yml` (which leaves those three out). It SHALL print one line per file it wrote or skipped, SHALL leave an existing `lockstep.yaml` unchanged, SHALL add its hook to an existing settings or hooks file without removing other keys, and a second run SHALL change nothing.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (the three written off); Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, "A concrete example of the finished tool" step 1

#### Scenario: Fresh repository gets all four

- **GIVEN** an empty git repository
- **WHEN** `lockstep init` runs
- **THEN** `lockstep.yaml`, `.claude/settings.json`, `.codex/hooks.json` and `lefthook.yml` exist and each names Lockstep,
  and `lockstep.yaml` sets every check to `block` except `maintainability`, `helper-reuse` and `mutation`, set to `off`

#### Scenario: A second run changes nothing

- **GIVEN** a repository `lockstep init` already ran in
- **WHEN** it runs again
- **THEN** every file is byte-identical and each is reported as skipped

#### Scenario: Existing settings keep their other keys

- **GIVEN** a `.claude/settings.json` with other keys and another PreToolUse hook
- **WHEN** `lockstep init` runs
- **THEN** those remain and the Lockstep hook is added once
