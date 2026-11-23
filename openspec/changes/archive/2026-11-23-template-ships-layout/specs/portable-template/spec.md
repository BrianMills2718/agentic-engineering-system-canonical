## ADDED Requirements

### Requirement: A fresh copy ships its planned file layout

A repository made with `copier copy` SHALL include `lockstep.yaml` with `governed:` and `fixed:` covering
`src/<package>/` and a `layout:` row for each starter source file (`__init__.py`, `core.py`, `cli.py`), each with a
purpose, the requirements it implements, its tests and its typed exports. Each starter file SHALL hold a cog block
in its docstring that the copy's `lockstep check project` fills with the row's plan text, so the edit hook refuses a
file under `src/<package>/` that has no row. Its `AGENTS.md` SHALL say that a plan adds a row for every new or
changed file with the OpenSpec change and that `uv run lockstep layout` then creates the files, and its `make check`
SHALL run the whole-tree check (`lockstep check --repo . --base <ref>`) against the merge base with `origin/main`,
else the first commit, saying it skipped when there is no commit yet.

Source: Brian, 2026-11-23: "i approve", item (c) of docs/planning/back-on-design-2026-11-23.md ("the planned file layout back in the template"); plan docs/planning/template-layout-2026-11-23.md

#### Scenario: A fresh copy refuses an unplanned source file

- **GIVEN** the template rendered with its defaults
- **WHEN** its `lockstep.yaml` is read and the edit hook is asked about writing `src/demo/extra.py`
- **THEN** the three starter files are rows whose exports pass the symbol gate, and the write is refused naming `lockstep.yaml`

#### Scenario: A default copy with no remote passes make check

- **GIVEN** a copy made with its defaults and tasks, with one commit and no remote
- **WHEN** `make check` runs
- **THEN** it exits 0 and its output shows the whole-tree check allowing the tree

### Requirement: Updating an older copy adds no layout plan

`copier update` of a copy made before the template shipped `lockstep.yaml` SHALL NOT add `lockstep.yaml`, while
adding or updating the template's other files.

Source: inferred by agent (cold review finding 1 of docs/planning/template-layout-2026-11-23.md: a plan added to an older copy's existing files would refuse them; `_skip_if_exists` protects only a file that already exists)

#### Scenario: An update of an older copy keeps it without a plan

- **GIVEN** a committed copy made from a template version without `lockstep.yaml`
- **WHEN** it is updated to the current template
- **THEN** it has no `lockstep.yaml` and its `AGENTS.md` names `uv run lockstep layout`
