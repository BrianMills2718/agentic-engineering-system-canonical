## ADDED Requirements

### Requirement: AES plans every tracked file

This repository's `lockstep.yaml` SHALL have one `layout:` row with a nonempty purpose for every Git-tracked file, SHALL govern the whole repository (`.` under `governed:`), so a new file anywhere, including a new top-level file or folder, is reported, and SHALL project the rows' paths and purposes into `generated/files.md`, which `wiki/index.md` links.

Source: Brian, 2026-11-13, AES #849: "Every Git-tracked file must be reachable and summarized from `wiki/index.md`"; where the rows live: Brian, 2026-11-11, approving `proposals/one-planning-tool/DESIGN.md` (line 41: which files exist and why lives in `lockstep.yaml` `layout:` rows). The checkable form is inferred by agent.

#### Scenario: Every tracked file has a planned row and the catalog page is current

- **GIVEN** this repository at HEAD
- **WHEN** its tracked files, `lockstep.yaml` and `generated/files.md` are read
- **THEN** every tracked file has a layout row with a purpose, a new file in a new top-level folder, at the top level or under `docs/` is governed, the projection of the layout into `generated/files.md` is current, and `wiki/index.md` links `generated/files.md`

## MODIFIED Requirements

### Requirement: The plan is OpenSpec plus layout rows

In a repository whose `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL take the
planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it implements, its tests, optionally
its typed exports), the governed folders from `governed:`, and the requirement text from OpenSpec. A `governed:` entry
ending in `/` covers every path under it, `.` covers the whole repository, and any other entry covers that one file or
a folder of that name. A repository with
`.aes/target.yaml` SHALL be read as before.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 2: "Lockstep reads requirements from OpenSpec ... and layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it"). How a `governed:` entry matches (`/`, `.`, a file or folder name) inferred by agent, 2026-11-24, after a review found a bare `Makefile` entry covered `Makefile.bak` and a list of top-level names missed a new top-level file.

#### Scenario: The layout is laid out with first docstrings

- **GIVEN** a layout row for `src/greeter/__init__.py` implementing `greeting/greet-by-name`, tested by `tests/test_greet.py`
- **WHEN** `lockstep layout` runs
- **THEN** the file is created with a docstring holding its `Implements:` line, the requirement and its scenarios word for word, the test names and its declared signature, and an existing file is left as it is

#### Scenario: An unplanned file is refused against the layout

- **GIVEN** `governed: [src/]` and no row for `src/greeter/extra.py`
- **WHEN** an agent writes that file under `PCW_MODE=block`
- **THEN** the edit hook refuses it and names `lockstep.yaml` as where the file must be planned

#### Scenario: A planned file's edit hands over its requirement

- **GIVEN** a laid-out planned file
- **WHEN** an agent edits it
- **THEN** the edit is allowed and the agent is handed the OpenSpec requirement text

#### Scenario: The whole-tree check reads the layout

- **GIVEN** a laid-out, committed layout repository
- **WHEN** `lockstep check` runs, and again after an unplanned file is added under `src/`
- **THEN** the first allows and the second blocks with that file as `unplanned`

#### Scenario: A layout row must name real requirements

- **GIVEN** a row whose `implements` names a requirement no spec defines, and a row with no purpose
- **WHEN** the layout is checked
- **THEN** both are reported, naming the row's path

#### Scenario: A governed entry covers what it names

- **GIVEN** `governed:` entries `src/`, `.`, `Makefile` and `src/lockstep`
- **WHEN** paths are matched against each
- **THEN** `src/` covers `src/a/b.py` but not `srcx/b.py`, `.` covers every path, `Makefile` covers `Makefile` but not `Makefile.bak`, and `src/lockstep` covers `src/lockstep/x.py` but not `src/lockstep_old.py`

#### Scenario: An AES plan is still read

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** Lockstep reads its plan
- **THEN** the planned files come from `.aes/target.yaml` exactly as before
