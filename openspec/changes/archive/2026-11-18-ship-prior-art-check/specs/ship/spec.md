## ADDED Requirements

### Requirement: Refuse a merge whose OpenSpec change lacks a prior-art record

Before the planning gate and the check, `scripts/ship.py` SHALL run code2-workspace's `scripts/prior_art_check.py` (from `$SHIP_WORKSPACE`, default `~/code2/workspace`) with `--repo` set to the repository and `--files` set to every file under `openspec/changes/` that the merge (from the merge base with the default branch to HEAD) adds or changes; when no merge base is found it SHALL run it without `--files`. When the merge adds or changes no file under `openspec/changes/` it SHALL run nothing and print and log one line saying so. It SHALL refuse the merge, with nothing pushed, when the script exits 1, showing what the script printed. When the script is missing it SHALL refuse the merge and say to run `git -C <workspace> pull --ff-only`; when the script exits with any status other than 0 or 1 it SHALL refuse the merge, show the exit status and say this is not a verdict on the record. When the script exits 0 it SHALL print and log its summary line.

Source: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search so that we are only buidling what we need to. that needs to be ienforced" (code2-workspace Policy `prior-art-per-feature`; issue 833, slice 1, names `ship` as the merge point). Inferred by agent: running nothing when no change is touched, reading the script from the workspace checkout, and refusing when it is missing or cannot run (the merge rules fail closed).

#### Scenario: A change with no record is refused

- **GIVEN** a branch that adds an OpenSpec change whose prior-art check exits 1
- **WHEN** `ship` runs
- **THEN** it exits 1, the check does not run, nothing is pushed, and the output holds what the prior-art check printed

#### Scenario: A change with a record merges

- **GIVEN** a branch that adds an OpenSpec change whose prior-art check exits 0
- **WHEN** `ship` runs
- **THEN** it merges, the prior-art check was given `--files` naming the change's files, and its summary line is printed and logged

#### Scenario: A merge that touches no change runs nothing

- **GIVEN** a branch that changes no file under `openspec/changes/`
- **WHEN** `ship` runs
- **THEN** the prior-art check is not run, a line says no OpenSpec change is in the merge, and the merge proceeds

#### Scenario: A missing prior-art check refuses

- **GIVEN** a branch that adds an OpenSpec change, and no `scripts/prior_art_check.py` in the workspace folder
- **WHEN** `ship` runs
- **THEN** it exits 1 with nothing pushed and says to run `git -C <workspace> pull --ff-only`

#### Scenario: A prior-art check that cannot run refuses

- **GIVEN** a branch that adds an OpenSpec change whose prior-art check exits 2
- **WHEN** `ship` runs
- **THEN** it exits 1 with nothing pushed, and says the exit status and that this is not a verdict on the record
