## MODIFIED Requirements

### Requirement: The project check reports Company Planning plugin drift

`lockstep check project` SHALL compare `.claude/settings.json` in the working tree with `planning.skills` in `lockstep.yaml`, with no network, looking only at whether `extraKnownMarketplaces.inside-success.source` is `{source: github, repo: <marketplace>}` (repository compared without letter case) and `enabledPlugins."company-planning@inside-success"` is `true`. A missing key or file SHALL print a `refused:` line under `mode: block` (and make the check exit 1) and a `warning:` line under `warn`; under `off` or no `skills` key nothing SHALL be looked at. A conflict (another source or repository, or an `enabledPlugins` value that is not `true`, such as an opt-out `false`) SHALL only print a `warning:` line naming the key, whatever the mode. While `extraKnownMarketplaces.inside-success` names another source or repository, a missing `enabledPlugins` entry SHALL NOT get a line of its own, since `lockstep init` withholds it until that source is fixed; the conflict's `warning:` line names the entry to change or remove before running `lockstep init`. Each line SHALL name `lockstep init` as the fix. A bad `skills` value (unknown mode, marketplace not `owner/repo` or missing when on) SHALL be refused naming its line in `lockstep.yaml`, and SHALL also be named by the side-file check; `ship`'s `planning_modes` SHALL NOT validate `skills`, so it never stops a merge. The check adds no name to `checks:`.

Source: Brian, 2026-11-25, the settings model adopted in docs/planning/next.goal.md ("Company Planning skills | per-person plugin install | slice 3"); slice 3 planned in full 2026-11-26 in docs/planning/next.goal.md ("Drift check, inside `lockstep check project`", "Not a ship gate"). Inferred by agent (review of init-keeps-refusing, 2026-11-28): the missing `enabledPlugins` line is dropped under a source conflict because its advice, `lockstep init`, could not clear it. Inferred by agent: the check rides on `project` so the lefthook command init generates stays unchanged in existing repositories.

#### Scenario: A deleted enabledPlugins entry refuses under block and warns under warn

- **GIVEN** a repository init wrote the keys into, then `enabledPlugins` lost its `company-planning@inside-success` entry
- **WHEN** `lockstep check project` runs with `planning.skills.mode` block, then warn
- **THEN** under block it prints a `refused:` line naming the key and `lockstep init` and exits 1; under warn it prints a `warning:` line and exits 0

#### Scenario: A conflict only warns

- **GIVEN** `.claude/settings.json` naming another `inside-success` repository, or `enabledPlugins` set to `false`
- **WHEN** `lockstep check project` runs under `block`
- **THEN** it prints a `warning:` line naming the key and the drift adds no failure

#### Scenario: A conflicting source without enabledPlugins names the source to fix

- **GIVEN** `.claude/settings.json` whose `inside-success` names another repository and no `enabledPlugins` entry
- **WHEN** `lockstep check project` runs under `block`
- **THEN** it prints one `warning:` line naming `extraKnownMarketplaces.inside-success` and `lockstep init`, no `refused:` line, and exits 0

#### Scenario: Off is not looked at

- **GIVEN** `planning.skills.mode: off` and no plugin keys
- **WHEN** `lockstep check project` runs
- **THEN** it prints no skills line

#### Scenario: A bad skills value is named with its line and ship ignores it

- **GIVEN** `planning.skills` with an unknown mode, or a marketplace that is not `owner/repo`
- **WHEN** the side-file check and `lockstep check project` run, and `planning_modes` reads the file
- **THEN** both checks name `planning.skills` and the line, and `planning_modes` returns the gate modes without error
