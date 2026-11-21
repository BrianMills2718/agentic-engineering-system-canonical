## MODIFIED Requirements

### Requirement: Refuse a merge whose OpenSpec change lacks a prior-art record

Before the planning gate and the check, `ship` SHALL run Lockstep's prior-art check (`src/lockstep/prior_art.py`, the file beside ship's own module) with `--repo` set to the repository and `--files` set to every file under `openspec/changes/` that the merge (from the merge base with the default branch to HEAD) adds or changes; when no merge base is found it SHALL run it without `--files`. When the merge adds or changes no file under `openspec/changes/` it SHALL run nothing and print and log one line saying so. It SHALL refuse the merge, with nothing pushed, when the check exits 1, showing what the check printed. When the check file is missing it SHALL refuse the merge and say to reinstall `ship`; when the check exits with any status other than 0 or 1 it SHALL refuse the merge, show the exit status and say this is not a verdict on the record. When the check exits 0 it SHALL print and log its summary line.

Source: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search so that we are only buidling what we need to. that needs to be ienforced" (code2-workspace Policy `prior-art-per-feature`; issue 833, slice 1, names `ship` as the merge point). Inferred by agent: running nothing when no change is touched, and refusing when the check is missing or cannot run (the merge rules fail closed). Inferred by agent, 2026-11-20 (minimal core, section 7): the check ships inside the public package instead of being read from the private workspace checkout, so `ship` works on another machine.

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

- **GIVEN** a branch that adds an OpenSpec change, and no prior-art check beside ship's module
- **WHEN** `ship` runs
- **THEN** it exits 1 with nothing pushed and says to reinstall `ship`

#### Scenario: A prior-art check that cannot run refuses

- **GIVEN** a branch that adds an OpenSpec change whose prior-art check exits 2
- **WHEN** `ship` runs
- **THEN** it exits 1 with nothing pushed, and says the exit status and that this is not a verdict on the record

## ADDED Requirements

### Requirement: Install ship as a command from the public repository

The package SHALL install a `ship` command (`lockstep.ship:main`), so `uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical ship` runs it on any machine with `uv`, `git` and `gh`. The files `scripts/ship.py` and `scripts/lane_sweep.py` SHALL keep working as before, run as files or imported from `scripts/`, by loading the modules in `src/lockstep/`.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable". Inferred by agent (minimal core, section 7: "install from the public repo with `uvx`, like `lockstep` already is"): keeping the old paths, because `~/.local/bin/ship` and the daily refresh point at them.

#### Scenario: The command and the old file both run

- **GIVEN** the package installed, and the file `scripts/ship.py`
- **WHEN** `python -m lockstep.ship --help` and `python scripts/ship.py --help` run
- **THEN** both exit 0 and print ship's usage

#### Scenario: The old import path is the moved module

- **GIVEN** `scripts/` on the import path
- **WHEN** `import ship` runs
- **THEN** the module is `lockstep.ship`
