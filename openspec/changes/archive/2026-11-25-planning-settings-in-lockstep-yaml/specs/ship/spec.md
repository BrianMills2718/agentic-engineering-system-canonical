## ADDED Requirements

### Requirement: Planning gates are set in lockstep.yaml

`ship` SHALL read `planning.gate` (the planning-package gate) and `planning.one_page_plans` (the one-page-plan check) from `lockstep.yaml` on the default branch at `origin`, never from the branch being shipped. Each SHALL be `block`, `warn` or `off`, a bare YAML `true` meaning `block` and `false` meaning `off`; an absent file, section or key SHALL mean `block`. A gate SHALL be off when either this setting or the `.copier-answers.yml` key says off, and the printed and logged line SHALL name the file that said so (`ship: planning gate: off (lockstep.yaml planning.gate: off)`). Under `warn`, a plan verdict (a validator rejection, a missing planning package, an incomplete one-page plan or a plan-list refusal) SHALL print and log `ship: warning: <gate>: <reason>; not refused (lockstep.yaml planning.<key>: warn)` and the merge SHALL go on, while a validator that cannot be fetched or cannot run SHALL still refuse. Any other value SHALL refuse the merge naming the value, with nothing pushed. The prior-art check has no switch.

Source: Brian, 2026-11-25: "yes it should hold all 4 parts btu the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece" (proposals/aes-whole-system/PLAN.md, slice 1); the prior-art exception: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search ... that needs to be ienforced".

#### Scenario: Off in lockstep.yaml on the default branch skips the gate

- **GIVEN** a new repository with no planning package whose default branch's `lockstep.yaml` says `planning: {gate: off}`
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: planning gate: off (lockstep.yaml planning.gate: off)`

#### Scenario: A branch cannot switch its own planning gate off in lockstep.yaml

- **GIVEN** a new repository with no planning package and a branch whose own `lockstep.yaml` says `planning: {gate: off}`
- **WHEN** ship runs
- **THEN** it is refused as before

#### Scenario: Warn passes a plan verdict

- **GIVEN** a new repository with no planning package whose default branch's `lockstep.yaml` says `planning: {gate: warn}`
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints a `ship: warning: planning gate:` line

#### Scenario: Warn still refuses a validator that cannot be fetched

- **GIVEN** a repository with a planning package, `planning: {gate: warn}` on the default branch and a company-planning source that cannot be fetched
- **WHEN** ship runs
- **THEN** it is refused and nothing is pushed

#### Scenario: A bad planning mode refuses

- **GIVEN** `planning: {gate: sometimes}` on the default branch
- **WHEN** ship runs
- **THEN** it exits 1 naming `sometimes`, with nothing pushed
