## ADDED Requirements

### Requirement: Init writes the Company Planning plugin keys when planning.skills is on

When `planning.skills` in `lockstep.yaml` is `{mode: block|warn, marketplace: OWNER/REPO}`, `lockstep init` SHALL merge into `.claude/settings.json` the marketplace `inside-success` (`extraKnownMarketplaces.inside-success.source` = `{source: github, repo: OWNER/REPO}`) and `enabledPlugins."company-planning@inside-success": true`, keeping every other key, and SHALL print `wrote`, `skipped` (everything already matches) or `conflict` for `planning.skills`. It SHALL never overwrite an `inside-success` entry with another source or repository, nor an `enabledPlugins` value that is not `true` (a `false` is a person opting out); each is named in a `conflict` line and left as it is. Extra fields such as `autoUpdate` SHALL be kept and SHALL NOT count as a difference. A `.claude/settings.json` that is not valid JSON SHALL make init exit 2. With `mode: off` or no `skills` key it SHALL write and remove nothing for this setting. When on, it SHALL print the two Codex commands with the configured address (`codex plugin marketplace add OWNER/REPO`, `codex plugin add company-planning@inside-success`), reading and writing nothing in `~/.codex/`, and the Claude Code project commands: list marketplaces, register the configured `OWNER/REPO` with `--scope project` only when `inside-success` is absent, then run `claude plugin install company-planning@inside-success --scope project`; it SHALL add that line once to an existing, non-symlinked `AGENTS.md` under a `## Company Planning plugin` heading, and otherwise only print it. A `skills` value with an unknown mode or a marketplace that is not `owner/repo` (or missing when on) SHALL make init exit 2 naming the line. A fresh `lockstep.yaml` SHALL hold the key commented out.

Source: Brian, 2026-11-25, the settings model adopted in docs/planning/next.goal.md ("Company Planning skills | per-person plugin install | slice 3": "the whole systm should be configurable so you can congfigure what is on or off"); slice 3 planned in full 2026-11-26 in docs/planning/next.goal.md, with one independent read. Inferred by agent: `off` is the default (this switch writes files), no default address (as slice 2), the AGENTS.md note goes only into an existing non-symlinked file (a symlinked AGENTS.md is another repository's source).

#### Scenario: Block writes the keys and a second run skips them

- **GIVEN** a repository whose `lockstep.yaml` says `planning: {skills: {mode: block, marketplace: Inside-Success/company-planning}}`
- **WHEN** `lockstep init` runs twice
- **THEN** the first run prints `wrote   planning.skills`, `.claude/settings.json` holds both keys beside the Lockstep hooks, `lockstep check project` reports no skills problem, and the second run prints `skipped planning.skills` and changes no file

#### Scenario: Warn also writes the keys

- **GIVEN** `planning.skills.mode: warn` with a marketplace
- **WHEN** `lockstep init` runs
- **THEN** both keys are written

#### Scenario: The keys merge into existing settings

- **GIVEN** a `.claude/settings.json` with other keys and hooks
- **WHEN** `lockstep init` runs with skills on
- **THEN** those keys and hooks remain and both plugin keys are added

#### Scenario: A malformed settings file exits 2

- **GIVEN** a `.claude/settings.json` that is not valid JSON and skills on
- **WHEN** `lockstep init` runs
- **THEN** it exits 2 and the file is unchanged

#### Scenario: Off writes nothing and keeps what exists

- **GIVEN** `planning.skills.mode: off`, or no `skills` key, and a settings file already holding the plugin keys
- **WHEN** `lockstep init` runs
- **THEN** the plugin keys are left exactly as they were, none are added to a file without them, and no Codex or install line is printed

#### Scenario: Another source or an opt-out is a conflict left as it is

- **GIVEN** a settings file whose `inside-success` names another repository, or whose `enabledPlugins` entry is `false`
- **WHEN** `lockstep init` runs with skills on
- **THEN** it prints `conflict planning.skills` with a line naming the key, and that value is unchanged

#### Scenario: autoUpdate is tolerated

- **GIVEN** the wanted `inside-success` entry with `autoUpdate: true` added
- **WHEN** `lockstep init` runs
- **THEN** it prints `skipped planning.skills` and the field stays

#### Scenario: Init prints the Codex commands and the install line

- **GIVEN** skills on with marketplace `Inside-Success/company-planning` and an existing `AGENTS.md`
- **WHEN** `lockstep init` runs twice
- **THEN** it prints `codex plugin marketplace add Inside-Success/company-planning`, `codex plugin add company-planning@inside-success` and the ordered Claude marketplace list, conditional project registration and project install commands, and `AGENTS.md` points to registration before its single install line

#### Scenario: A bad skills value stops init

- **GIVEN** `planning.skills` with mode `sometimes`, or a marketplace `not a repo`
- **WHEN** `lockstep init` runs
- **THEN** it exits 2 naming `planning.skills` and the line of `lockstep.yaml`
