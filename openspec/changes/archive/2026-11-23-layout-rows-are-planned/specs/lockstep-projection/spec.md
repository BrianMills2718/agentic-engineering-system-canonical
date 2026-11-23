## ADDED Requirements

### Requirement: Links show planned files and exports

In a repository whose `lockstep.yaml` has `layout:` rows, `docs/links.json` SHALL hold a `file` node for each row's path and a `symbol` node for each declared export, each with `state` `planned` when the file (or, for an export, the top-level function or class of that name in the file) does not exist yet and `exists` when it does. A row's `file` node SHALL link to the requirements the row implements and to its test files; an export's `symbol` node, with ID the file's module path and the export name, SHALL link to the file. An implementer found in a comment line (no Python symbol) SHALL link its requirement to the `file` node directly.

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md`; `docs/architecture/LOCKSTEP.md:23-26` (requirement, file and symbol are one chain); plan `docs/planning/template-layout-2026-11-23.md`, step 4.

#### Scenario: A planned file that does not exist yet is shown as planned

- **GIVEN** a layout row for `src/pkg/new.py` implementing `core/do-the-thing`, with tests `tests/test_new.py` and export `make() -> int`, and no such file
- **WHEN** the links are built
- **THEN** node `src/pkg/new.py` has type `file`, state `planned` and links to `core/do-the-thing` and `tests/test_new.py`, and node `pkg.new.make` has type `symbol`, state `planned` and links to `src/pkg/new.py`

#### Scenario: A laid-out file with its export is shown as existing

- **GIVEN** the same row and `src/pkg/new.py` defining `def make() -> int`
- **WHEN** the links are built
- **THEN** both nodes have state `exists`
