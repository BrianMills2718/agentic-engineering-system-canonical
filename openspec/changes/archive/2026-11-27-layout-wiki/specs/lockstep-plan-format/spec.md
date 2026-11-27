## MODIFIED Requirements

### Requirement: Every refusal in a layout repository names a layout command

In a layout repository, the whole-tree commit check SHALL judge a planned file's docstring exactly as the edit hook does, and its stale reason SHALL name `uv run lockstep check project`. A refusal for an undeclared, removed or retyped public symbol SHALL name the file's layout row `exports:` in lockstep.yaml as where to declare it. Every edit-hook refusal SHALL end by pointing to the layout rows in `lockstep.yaml` and to `uv run lockstep show <file>`, and SHALL NOT point to `python -m lockstep.wiki`. A repository with `.aes/target.yaml` SHALL keep its current wording.

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), whose rerun was blocked at commit by a check naming `.aes/target.yaml`; the rule itself inferred by agent. The refusal pointer added 2026-11-23 after `python -m lockstep.wiki` was found to crash in a layout repository (inferred by agent, while carrying out Q54).

#### Scenario: The commit check judges an Implements block the same way

- **GIVEN** a committed file whose `Implements:` block is current, edited in the working tree
- **WHEN** `lockstep check` runs, then again after an active change rewords its requirement, then after `lockstep check project`
- **THEN** it allows, then blocks the file as stale naming `lockstep check project` and not `.aes/target.yaml`, then allows

#### Scenario: An undeclared public symbol names the layout exports

- **GIVEN** a planned layout file
- **WHEN** an agent's edit adds a public function its layout row does not export, under `PCW_MODE=block`
- **THEN** the edit is refused naming the row's `exports:` in lockstep.yaml and not `aes plan`

#### Scenario: A refusal points to lockstep show, not the wiki

- **GIVEN** a layout repository with no `.aes/` folder
- **WHEN** the edit hook refuses a write to an unplanned file
- **THEN** the refusal names `uv run lockstep show` and does not name `python -m lockstep.wiki`
