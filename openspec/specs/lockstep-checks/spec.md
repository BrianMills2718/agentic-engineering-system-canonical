# lockstep-checks Specification

## Purpose

Lockstep's commit checks, ported from code2check: trace, arch, test-first, sources and docmeta refuse a plan, code, test, diagram or wiki that has drifted, each switchable to block, warn or off in `lockstep.yaml` (`proposals/one-planning-tool/DESIGN.md`, slice 4).

## Requirements

### Requirement: Trace: Every requirement has an implementer

The trace check SHALL fail when an OpenSpec requirement has no source module, class or function whose
docstring contains a line `Implements: <capability>/<requirement-slug>`.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way" Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Requirement without implementer fails

- **GIVEN** a spec with requirement "Do the thing" in capability "core"
- **WHEN** no source docstring says `Implements: core/do-the-thing`
- **THEN** the check reports `core/do-the-thing` as unimplemented and exits 1

#### Scenario: Trace: Implemented requirement passes

- **GIVEN** the same spec
- **WHEN** a source docstring says `Implements: core/do-the-thing`
- **THEN** the check reports no finding for that requirement

### Requirement: Trace: Every scenario has a test

The trace check SHALL fail when an OpenSpec scenario has no test decorated with
`@pytest.mark.req("<capability>/<scenario-slug>")`.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way" Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Scenario without test fails

- **GIVEN** a spec with scenario "It works" in capability "core"
- **WHEN** no test carries `req("core/it-works")`
- **THEN** the check reports `core/it-works` as untested and exits 1

### Requirement: Trace: Unknown IDs fail

The trace check SHALL fail when a docstring or test marker names an ID that no spec defines.

Source: inferred by agent (a marker naming no planned ID means the plan and code disagree) Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Stale marker fails

- **GIVEN** a test marked `req("core/renamed-away")`
- **WHEN** no spec defines that scenario
- **THEN** the check reports the unknown ID with its file and exits 1

### Requirement: Trace: IDs from changes in progress are known

The trace check SHALL treat requirement and scenario IDs defined in an active change's spec delta
(`openspec/changes/<name>/specs/<capability>/spec.md`, archive excluded) as known, and SHALL not
require them to be implemented or tested until the change is archived.

Source: inferred by agent (needed so failing tests can be committed before the spec is archived) Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Test written for an active change passes trace

- **GIVEN** an active change whose delta adds scenario "It also works" to capability "core"
- **WHEN** a test carries `req("core/it-also-works")` and no code implements the new requirement yet
- **THEN** the check reports no finding for either ID

### Requirement: Trace: Source folders are configurable

The trace check SHALL search for `Implements:` lines in the folders listed under `[tool.lockstep] (or`[tool.code2check]`, its old name)
source` in `pyproject.toml`, and in `src` when none are listed.

Source: inferred by agent (existing repositories keep code outside src) Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Implementer outside src is found

- **GIVEN** `source = ["scripts"]` and a docstring in `scripts/tool.py` saying `Implements: core/do-the-thing`
- **WHEN** the trace check runs
- **THEN** it reports no unimplemented finding for `core/do-the-thing`

### Requirement: Trace: Test folders are configurable

The marker reader SHALL discover `@pytest.mark.req` in `test_*.py` files under the folders listed
in `[tool.lockstep] (or`[tool.code2check]`, its old name) tests` in `pyproject.toml`, defaulting to `tests` when omitted. Trace, status,
generated plan coverage and test-first SHALL use those same roots. Overlapping roots SHALL not
duplicate a discovered test marker.

Source: inferred by agent (existing source roots are configurable, but actual consumer repositories also keep tests outside the root tests directory; the same canonical marker reader must serve every linked view) Ported from code2-template `openspec/specs/trace/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Trace: Configured test folders feed trace

- **GIVEN** configured source and test folders outside `src` and root `tests`
- **WHEN** the trace check inspects the repository
- **THEN** it finds the implementer and the test there and reports no finding (code2check's status, show and projection views are not part of this slice)

#### Scenario: Trace: Overlapping test folders do not duplicate markers

- **GIVEN** configured test folders that overlap
- **WHEN** the marker reader finds a test
- **THEN** it reports that test marker once

### Requirement: Arch: Diagram becomes import contracts

`lockstep check arch gen` SHALL write one import-linter forbidden contract per diagram element that has
`python` metadata, forbidding direct imports of every other mapped element it has no relation to. When
LikeC4 reports the diagram invalid, it SHALL stop with LikeC4's errors and write no contracts.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way" Ported from code2-template `openspec/specs/arch/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Arch: Missing arrow forbids the import

- **GIVEN** elements cli, detect and apply mapped to Python modules, and only cli -> detect and cli -> apply
- **WHEN** contracts are generated
- **THEN** detect is forbidden to import cli and apply, apply is forbidden to import cli and detect, and cli is forbidden nothing

#### Scenario: Arch: Invalid diagram stops generation

- **GIVEN** a diagram that names a component `views`, which LikeC4 cannot parse
- **WHEN** the model is exported for contract generation
- **THEN** export raises an error carrying LikeC4's "Invalid" report, and no partial model is returned

### Requirement: Arch: Committed contracts match the diagram

`lockstep check arch check` SHALL exit 1 when the committed contracts file differs from what the current
diagram generates.

Source: inferred by agent (a stale contracts file would let the diagram drift) Ported from code2-template `openspec/specs/arch/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Arch: Diagram changed without regenerating

- **GIVEN** a committed contracts file generated from an older diagram
- **WHEN** the diagram gains a relation and the check runs
- **THEN** the check reports the file as out of date and exits 1

### Requirement: Test-first: New scenario tests fail before the change

`lockstep check test-first --base <rev>` SHALL run, against the base revision's source, every test marked
for a scenario that the current revision's specs or active changes define and the base revision's specs
and active changes do not, and exit 1 if any of them passes there.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way" Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Test-first: Test that already passed is reported

- **GIVEN** a scenario added since the base and a test for it that passes on the base source
- **WHEN** the check runs
- **THEN** it reports the test as not proving the new behavior and exits 1

#### Scenario: Test-first: Test that failed before passes the check

- **GIVEN** a scenario added since the base and a test for it that fails on the base source
- **WHEN** the check runs
- **THEN** it exits 0

#### Scenario: Test-first: A scenario in an active change is checked

- **GIVEN** a scenario written in an active change since the base and a test for it that passes on the base source
- **WHEN** the check runs
- **THEN** it reports the test as not proving the new behavior and exits 1

#### Scenario: Test-first: Archiving a change makes no scenario new

- **GIVEN** a change, present at the base, archived since so that its scenarios moved into the specs
- **WHEN** the check runs
- **THEN** it checks none of those scenarios' tests and exits 0

#### Scenario: Test-first: Configured test folders run against the base source

- **GIVEN** `[tool.lockstep] tests` names a folder outside `tests`, and a scenario added since the base with a test there that passes on the base source
- **WHEN** the check runs
- **THEN** it runs that test against the base source, reports it as passed before and exits 1

### Requirement: Test-first: A missing base revision is reported, not crashed

`lockstep check test-first --base <rev>` SHALL, when `<rev>` does not name a commit, check nothing,
report that the base was missing, and exit 0.

Source: inferred by agent (a new repository has no origin/main yet) Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Test-first: New repository without a base passes with a skip notice

- **GIVEN** a repository whose base revision `origin/main` does not exist yet
- **WHEN** the check runs
- **THEN** it reports the check as skipped because the base is missing and exits 0

### Requirement: Test-first: Tests for existing behavior are exempt and counted

The test-first check SHALL not run a test marked `req(..., existing=True)` for a scenario that is new since the base, and SHALL report how many such tests it skipped. For a scenario whose text changed since the base, `existing=True` SHALL NOT exempt a test: it is run on the base source like any other test marked for that scenario.

Source: inferred by agent (working default awaiting Brian: tests marked existing=True for behavior that already worked are not run on the base revision, so existing repositories can adopt the format) Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4). The changed-scenario sentence is inferred by agent, 2026-11-17 (once the text changes, the behavior it describes is not the existing one).

#### Scenario: Test-first: Existing-behavior test is skipped and counted

- **GIVEN** a scenario added since the base and its test, marked `existing=True`, that passes on the base
- **WHEN** the check runs
- **THEN** it exits 0 and lists the test as existing

#### Scenario: Test-first: An existing-behavior mark does not exempt a changed scenario

- **GIVEN** a scenario whose text differs from the base and whose only test, marked `existing=True`, passes on the base source
- **WHEN** the check runs
- **THEN** it reports `no-failing-test` for the scenario and exits 1

### Requirement: Sources: Every normative item names its source

The sources check SHALL fail when an OpenSpec requirement (in `openspec/specs` or an active change delta)
or a decision record in `docs/decisions/` has no `Source:` line, so nobody mistakes an agent's guess for
Brian's rule. A decision record may give a `Decider:` line instead.

Source: Brian, 2026-10-15: "this applies much more to normative docuemntation. i dont ingeneral care as much abotu the implemetnation"; "i approve" Ported from code2-template `openspec/specs/sources/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Sources: Requirement without source fails

- **GIVEN** a spec whose requirement "Do the thing" has no `Source:` line
- **WHEN** the sources check runs
- **THEN** it reports `core/do-the-thing` as missing a source and exits 1

#### Scenario: Sources: Decision without source fails

- **GIVEN** a decision record `docs/decisions/0001-x.md` with neither `Source:` nor `Decider:`
- **WHEN** the sources check runs
- **THEN** it reports `decision/0001-x` as missing a source and exits 1

#### Scenario: Sources: Labeled items pass and are classified

- **GIVEN** one requirement with `Source: Brian, 2026-10-15: "..."` and one with `Source: inferred by agent (...)`
- **WHEN** the sources check runs with `--json`
- **THEN** it exits 0 and lists the first as `brian` and the second as `inferred`

### Requirement: Docmeta: Every wiki page declares its type

The docmeta check SHALL report every Markdown page under `wiki/` whose OKF front matter is missing,
unparseable or has no non-empty `type`. `wiki/index.md` and `wiki/log.md` are exempt, because the OKF
conventions give the catalog and the chronicle no front matter.

Source: Brian, 2026-11-05: "ok i approve all this" (doc-consolidation plan D9; earlier the same day: "maybe all docuemtnation should have like a lintable cleanup sstructured metadata?") Ported from code2-template `openspec/specs/docmeta/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Docmeta: Page without type fails

- **GIVEN** a wiki page whose front matter has a title but no `type`
- **WHEN** the docmeta check runs
- **THEN** it reports the page as `missing_type` and exits 1

#### Scenario: Docmeta: Index and log need no front matter

- **GIVEN** a wiki whose `index.md` and `log.md` have no front matter and whose other pages are clean
- **WHEN** the docmeta check runs
- **THEN** it exits 0

### Requirement: Docmeta: Current pages are checked within 60 days

The docmeta check SHALL report a page whose `status` is `current` (or absent, which means current)
when its `last_checked` date (YYYY-MM-DD) is more than 60 days old or missing.

Source: Brian, 2026-11-05: "ok i approve all this" (doc-consolidation plan D9) Ported from code2-template `openspec/specs/docmeta/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Docmeta: Stale current page fails

- **GIVEN** a current page whose `last_checked` is 61 days before today
- **WHEN** the docmeta check runs
- **THEN** it reports the page as `stale` and exits 1

### Requirement: Docmeta: Superseded pages name a successor

The docmeta check SHALL report a page whose `status` is `superseded` and which has no `successor`.

Source: Brian, 2026-11-05: "ok i approve all this" (doc-consolidation plan D9) Ported from code2-template `openspec/specs/docmeta/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Docmeta: Superseded page without successor fails

- **GIVEN** a page with `status: superseded` and no `successor`
- **WHEN** the docmeta check runs
- **THEN** it reports the page as `superseded_without_successor` and exits 1

### Requirement: Docmeta: One page owns each topic

The docmeta check SHALL report every topic listed in the `source_of_truth_for` of two or more pages,
naming the topic and each page.

Source: Brian, 2026-11-05: "ok i approve all this" (doc-consolidation plan D9) Ported from code2-template `openspec/specs/docmeta/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Docmeta: Two owners of one topic fail

- **GIVEN** two pages that both list `system-model` in `source_of_truth_for`
- **WHEN** the docmeta check runs
- **THEN** it reports the topic `system-model` with both pages and exits 1

### Requirement: Docmeta: Every current page is within two links of the index

The docmeta check SHALL report every current page under `wiki/` that cannot be reached from
`wiki/index.md` by following at most two relative Markdown links.

Source: Brian, 2026-11-05: "ok i approve all this" (doc-consolidation plan D10) Ported from code2-template `openspec/specs/docmeta/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Docmeta: Page three links away fails

- **GIVEN** a chain index → a → b → c of current pages
- **WHEN** the docmeta check runs
- **THEN** it reports `c` as `beyond_two_links` and not `a` or `b`, and exits 1

### Requirement: Docmeta: Field values have their allowed form

The docmeta check SHALL report a `status` other than `current`, `history` or `superseded`, a
`last_checked` that is not a YYYY-MM-DD date, and a `source_of_truth_for` that is not a list. Other
keys are allowed, as OKF permits.

Source: Brian, 2026-11-05: "ok i approve all this" (doc-consolidation plan D9 field list) Ported from code2-template `openspec/specs/docmeta/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Docmeta: Unknown status fails

- **GIVEN** a page with `status: draft`
- **WHEN** the docmeta check runs
- **THEN** it reports the page as `invalid_field` and exits 1

### Requirement: Docmeta: Count line and exit status

The docmeta check SHALL print one count line
`docmeta: pages=N missing_type=N stale=N superseded_without_successor=N topics_with_two_owners=N beyond_two_links=N invalid_field=N`
then one line per finding (path and reason), and exit 0 when there is no finding and 1 otherwise. A
repository with no `wiki/` folder prints the count line with `pages=0` and exits 0.

Source: Brian, 2026-11-05: "ok i approve all this" (doc-consolidation plan D9: runs in seconds in each repository's merge check) Ported from code2-template `openspec/specs/docmeta/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Docmeta: Clean wiki passes

- **GIVEN** a wiki whose pages all have valid fields and sit within two links of the index
- **WHEN** the docmeta check runs on its path
- **THEN** it prints the count line with every finding count 0 and exits 0

#### Scenario: Docmeta: Repository without wiki passes

- **GIVEN** a folder with no `wiki/`
- **WHEN** the docmeta check runs
- **THEN** it prints `pages=0` and exits 0

#### Scenario: Sources: A configured human pattern replaces the default

- **GIVEN** `lockstep.yaml` with `sources: {human_pattern: dana}` and a requirement whose `Source:` line starts with "Dana"
- **WHEN** the sources check runs with `--json`
- **THEN** it lists that requirement as `brian` (the human class), where without the setting it is `other`

### Requirement: Each check can be set to block, warn or off in lockstep.yaml

`lockstep check <name>` (`trace`, `arch`, `test-first`, `sources`, `docmeta`) SHALL read `checks:` in
`lockstep.yaml` at the repository root, where each check is `block` (the default when absent or when there
is no file), `warn` or `off`. A failing `block` check SHALL exit 1; a failing `warn` check SHALL print a
`warning:` line and exit 0; an `off` check SHALL not run, SHALL print `skipped (off)` and exit 0. A value
other than those three, or an unknown check name, SHALL exit 2 naming it. The file's `sources.human_pattern`
(default `brian`), `owner` (no default) and `likec4` (default `1.60.0`) settings SHALL be read from the
same file. `lockstep check` with no name, or only `--repo`, `--base` and `--json`, SHALL keep running the
whole-tree plan check.

Source: Brian, 2026-11-11, approving the one-tool design ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 4: the checks are Lockstep's, each switchable so another repository can adopt them one at a time).

#### Scenario: A missing lockstep.yaml means every check blocks

- **GIVEN** a repository with no `lockstep.yaml` and a spec requirement with no implementer
- **WHEN** `lockstep check trace` runs
- **THEN** it exits 1 and prints `RESULT trace findings=2 exit=1`

#### Scenario: Warn prints a warning and exits zero

- **GIVEN** `checks: {trace: warn}` and a failing trace check
- **WHEN** `lockstep check trace` runs
- **THEN** it prints `warning: trace failed` and exits 0

#### Scenario: Off skips the check and exits zero

- **GIVEN** `checks: {trace: off}`
- **WHEN** `lockstep check trace` runs
- **THEN** it prints `skipped (off)`, runs nothing and exits 0

#### Scenario: Block set explicitly exits one and other checks keep their own mode

- **GIVEN** `checks: {trace: block, docmeta: off}`
- **WHEN** `lockstep check trace` and `lockstep check docmeta` run
- **THEN** trace exits 1 and docmeta is skipped with exit 0

#### Scenario: A bad mode or unknown check is an error

- **GIVEN** `checks: {trace: sometimes}`, or `checks: {nonsense: warn}`
- **WHEN** the settings are read
- **THEN** reading fails naming the value, and `lockstep check trace` exits 2

#### Scenario: Defaults when keys are absent

- **GIVEN** a `lockstep.yaml` with none of `checks`, `sources`, `owner`, `likec4`
- **WHEN** the settings are read
- **THEN** the human pattern is `brian`, the owner is unset and LikeC4 is `likec4@1.60.0`

#### Scenario: LikeC4 pin and owner are read

- **GIVEN** `likec4: 1.70.0` and `owner: Acme`
- **WHEN** the settings are read
- **THEN** LikeC4 is `likec4@1.70.0` and the owner is `Acme`

#### Scenario: Lockstep check without a name still runs the tree check

- **GIVEN** `lockstep check --repo PATH`
- **WHEN** the command runs
- **THEN** the whole-tree plan check runs, as before

#### Scenario: The lockstep command runs a named check

- **GIVEN** an installed Lockstep and a repository failing the trace check
- **WHEN** `lockstep check trace --repo PATH` runs as a process
- **THEN** it prints the trace RESULT line and exits 1

### Requirement: Arch: Code imports match the diagram

`lockstep check arch check`, when the committed contracts file matches the diagram, SHALL run the contracts against the code with import-linter and exit 1 when any contract is broken, printing the broken contract and the importing module. When import-linter is not installed it SHALL print that and exit 1; it SHALL NOT pass.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: Arch: An import the diagram forbids is refused

- **GIVEN** a current contracts file forbidding `app.detect` to import `app.cli`
- **WHEN** `app.detect` imports `app.cli` and the check runs
- **THEN** the check exits 1 and its output names the broken contract and `app.detect`

#### Scenario: Arch: Missing import-linter fails loudly

- **GIVEN** a current contracts file and no `lint-imports` command
- **WHEN** the check runs
- **THEN** it prints that import-linter is not installed and exits 1

### Requirement: Arch: A diagram check that cannot run fails as a tool failure

`lockstep check arch` SHALL report that LikeC4 could not be run, and SHALL NOT report the diagram
invalid, when `npx` is absent or cannot be started, when `npx likec4 validate` exits non-zero without
LikeC4 having run, or when the JSON export of an already-validated diagram fails. Whether LikeC4 ran
SHALL be decided by running it against no diagram, not by matching words in its output. Each of these
SHALL print `RESULT arch-<action> tool_unavailable=1 exit=1` and exit 1: a check that did not run must
fail, not pass. A diagram LikeC4 read and rejected SHALL still be reported `invalid_diagram=1`.

Source: inferred by agent from the 2026-11-18 nightly failure in `BrianMills2718/enforced-planning`: a valid diagram was reported `invalid_diagram=1` because npm could not write a shared cache containing root-owned directories, which made the run look like a repository defect. Same distinction the module already makes with `ImportLinterMissing`.

#### Scenario: Arch: A missing npx is a tool failure

- **GIVEN** no `npx` on PATH
- **WHEN** `lockstep check arch check` runs
- **THEN** it says npx is not installed, prints `tool_unavailable=1`, does not print `invalid_diagram`, exits 1, and runs no npx

#### Scenario: Arch: A LikeC4 that cannot start is a tool failure

- **GIVEN** an npx whose `validate` and `--version` both exit non-zero, reporting an unwritable npm cache
- **WHEN** `lockstep check arch check` runs
- **THEN** it carries npm's own report, prints `tool_unavailable=1`, does not print `invalid_diagram`, and exits 1

#### Scenario: Arch: A failing diagram export is a tool failure

- **GIVEN** a diagram LikeC4 validates and a JSON export that exits non-zero
- **WHEN** `lockstep check arch check` runs
- **THEN** it prints `tool_unavailable=1`, does not print `invalid_diagram`, and exits 1

### Requirement: Test-first: A test run that cannot start fails the check

`lockstep check test-first` SHALL exit 1 with a message saying pytest could not run when running the new tests on the base source produces no test report (pytest missing from Lockstep's environment, or a usage error); it SHALL NOT report the tests as not passing before.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: Test-first: Pytest that cannot run fails loudly

- **GIVEN** a new scenario with a marked test and a Python that cannot run pytest
- **WHEN** the check runs
- **THEN** it prints "pytest could not run" and exits 1

### Requirement: Instructions: The agent chain fits its budget

The instructions check SHALL report `payload_over_cap` when the byte sizes of the chain files that exist (default
`~/code2/AGENTS.md`, the project-root file Codex reads above the repository's own; `--chain FILE`, repeatable, or
`INSTRUCTION_CHAIN` separated by the path separator, replace it) plus the repository's root `AGENTS.md` add up to more
than 32,768 bytes, and `root_oversized` when the root `AGENTS.md` alone is more than 12,000 bytes. The global
`~/.codex/AGENTS.md` SHALL NOT be counted, because Codex's budget (`project_doc_max_bytes`) applies to project files
only.

Source: Brian, 2026-11-17: "leets figure this out re core.md this has to be testable and resarch able and might alreayd
be docuemtned"; Codex source `codex-rs/core/src/agents_md_manager.rs` (openai/codex 8011b92b): "The limit applies only
to project files." The 12 KB root guidance is in the `instruction-surfaces` skill.

#### Scenario: Instructions: An oversized root fails

- **GIVEN** a repository whose root `AGENTS.md` is 13,000 bytes
- **WHEN** `lockstep check instructions` runs
- **THEN** it reports `root_oversized` and exits 1

#### Scenario: Instructions: A chain over the cap fails

- **GIVEN** a 30,000-byte chain file and a 5,000-byte root `AGENTS.md`
- **WHEN** the check runs with that chain
- **THEN** it reports `payload_over_cap` and exits 1

### Requirement: Instructions: No CLAUDE.md with its own content

The instructions check SHALL report `claude_md_content` for every `CLAUDE.md` in the repository (outside `.git`,
`node_modules`, virtual environments, `worktrees` and `*_worktrees` folders) whose content is anything other than the
single line `@AGENTS.md`. A pure pointer is counted, not reported.

Source: Brian, 2026-11-17: "shouldnt it be no claude.md since claud code supports agents.md now but codex doesnt
supprot claude.md?"; Claude Code reads `AGENTS.md` only when no `CLAUDE.md` is in or above the working directory
(https://code.claude.com/docs/en/memory.md), and Codex never reads `CLAUDE.md`.

#### Scenario: Instructions: A CLAUDE.md with content fails

- **GIVEN** a repository with a `CLAUDE.md` holding rules
- **WHEN** the check runs
- **THEN** it reports `claude_md_content` for that file and exits 1

#### Scenario: Instructions: A pointer CLAUDE.md passes

- **GIVEN** a `CLAUDE.md` holding only `@AGENTS.md`
- **WHEN** the check runs
- **THEN** it reports no finding for it

### Requirement: Instructions: A nested file repeats nothing from its parents

The instructions check SHALL report `duplicated` for a nested `AGENTS.md` that has three or more lines of 40 or more
characters, after trimming, identical to lines of an `AGENTS.md` above it in the same repository.

Source: Brian, 2026-11-17: "basically you work your way up from the most nested dir and each parent dir only gets what
is relevant" and the policy's delta-only rule, "children do not restate parent policy"
(`project-meta/docs/ops/SUBTREE_INSTRUCTION_HIERARCHY.md`).

#### Scenario: Instructions: A repeated parent block fails

- **GIVEN** a nested `AGENTS.md` that copies three long lines from the root `AGENTS.md`
- **WHEN** the check runs
- **THEN** it reports `duplicated` for the nested file and exits 1

### Requirement: Instructions: Count line and exit status

The instructions check SHALL print one count line `instructions: files=N payload_bytes=N payload_over_cap=N
root_oversized=N claude_md_content=N duplicated=N`, then one line per finding (kind, path, reason), and exit 0 when
there is no finding and 1 otherwise. A repository with no `AGENTS.md` prints the count line with `files=0` and exits 0.

Source: inferred by agent, from the docmeta check's output form.

#### Scenario: Instructions: A clean repository passes

- **GIVEN** a repository with a 2,000-byte root `AGENTS.md`
- **WHEN** the check runs
- **THEN** every count but `files` and `payload_bytes` is 0 and it exits 0

### Requirement: Changed: Requirements that differ from the base are listed with their code and tests

`lockstep check changed --base <rev>` SHALL compare the text of every requirement and scenario in the plan at the current revision (`openspec/specs/` with the spec deltas of active changes applied over it) with the plan at the base revision, treating runs of whitespace as one space. It SHALL print, for each requirement that is new, removed, or whose statement or any scenario is new, removed or different: the requirement ID and its kind (`new`, `changed` or `removed`), which parts differ, the symbols whose docstrings implement it, the tests marked for its scenarios, each labelled `changed`, `unchanged` or `new` against the base revision's copy of that test function, and the plan that names it. `--json` SHALL print the same as JSON. It SHALL read the base revision from git without changing the working tree.

Source: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then that normative docuemtnation gets updated and then the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842; approved for build 2026-11-17, "i approve"). The output columns are inferred by agent.

#### Scenario: Changed: A reworded requirement is listed with its implementer and tests

- **GIVEN** a requirement whose statement differs from the base, with an implementing docstring and a marked test that is the same as at the base
- **WHEN** `lockstep check changed --base <rev>` runs
- **THEN** it lists the requirement as `changed`, names the implementing symbol, and labels the test `unchanged`

#### Scenario: Changed: Re-wrapped text is not a change

- **GIVEN** a requirement whose statement differs from the base only in line breaks and spacing
- **WHEN** the check runs
- **THEN** it lists nothing and exits 0

#### Scenario: Changed: A changed scenario marks its requirement changed

- **GIVEN** a requirement whose statement is the same as at the base and one of whose scenarios has different text
- **WHEN** the check runs
- **THEN** it lists the requirement as `changed` and names that scenario as the part that differs

#### Scenario: Changed: Text in an active change counts before it is archived

- **GIVEN** an active change whose spec delta gives an existing requirement a different statement
- **WHEN** the check runs
- **THEN** it lists the requirement as `changed` and names the change as its plan

#### Scenario: Changed: A test edited since the base is labelled changed

- **GIVEN** a changed requirement whose marked test function differs from the base revision's copy
- **WHEN** the check runs
- **THEN** the test is labelled `changed`

### Requirement: Changed: Every listed requirement is named by a plan in the same change set

The changed check SHALL report a listed requirement as `unplanned` and exit 1 when no plan that is new or different from the base revision names it. A plan names a requirement when it is an OpenSpec change (active, or archived since the base) whose spec delta has a heading for that requirement, or a page in `docs/plans/` or an OpenSpec change's `proposal.md` whose `Closes:` or `Wording-only:` line lists the requirement ID.

Source: Brian, 2026-11-17: "the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842; approved for build 2026-11-17, "i approve"). Which files count as a plan is inferred by agent (the two places `lockstep status` already reads a `Closes:` line from).

#### Scenario: Changed: A spec edited with no plan is unplanned

- **GIVEN** a requirement whose statement was edited in `openspec/specs/` since the base, and no change or plan page added or edited since the base
- **WHEN** the check runs
- **THEN** it reports the requirement as `unplanned` and exits 1

#### Scenario: Changed: An archived change in the same change set is its plan

- **GIVEN** a requirement whose statement differs from the base, and a change archived since the base whose spec delta has a heading for it
- **WHEN** the check runs
- **THEN** it names the archived change as the plan and reports no `unplanned` finding

#### Scenario: Changed: A plan page that was not touched does not count

- **GIVEN** a requirement whose statement differs from the base, and a page in `docs/plans/` with a `Closes:` line for it that is identical at the base
- **WHEN** the check runs
- **THEN** it reports the requirement as `unplanned`

### Requirement: Changed: A changed statement needs a changed scenario or a wording-only declaration

The changed check SHALL report `no-scenario-changed` and exit 1 when a requirement's statement differs from the base while none of its scenarios is new or different, unless a plan that is new or different from the base lists the requirement ID on a `Wording-only:` line. It SHALL print each wording-only declaration it accepted with the plan's path, and count them in its count line. A `Wording-only:` line MAY list scenario IDs as well as requirement IDs; a requirement ID covers its statement and all its scenarios.

Source: inferred by agent (a statement that changes while every scenario stays the same leaves nothing to test the change; the declaration is the one typed statement in the design and is printed so it can be read. Follows code2-workspace decision 0006, "a gap closes only through new evidence").

#### Scenario: Changed: A statement changed with no scenario changed fails

- **GIVEN** a requirement, named by a plan in the same change set, whose statement differs from the base and whose scenarios are all the same
- **WHEN** the check runs
- **THEN** it reports `no-scenario-changed` for the requirement and exits 1

#### Scenario: Changed: A wording-only declaration is accepted and printed

- **GIVEN** the same requirement, and a plan in the same change set with the line `Wording-only: <requirement id>`
- **WHEN** the check runs
- **THEN** it exits 0, prints the declaration with the plan's path, and its count line has `wording_only=1`

### Requirement: Changed: Count line and exit status

The changed check SHALL end with the line `RESULT changed requirements=<n> unplanned=<n> no_scenario=<n> wording_only=<n> exit=<0|1>`, exiting 1 when `unplanned` or `no_scenario` is above zero. When `<rev>` does not name a commit it SHALL check nothing, print `RESULT changed skipped="base <rev> not found" exit=0` and exit 0. `changed` SHALL be a check name in `lockstep.yaml` with the same `block`, `warn` and `off` modes as the other checks.

Source: inferred by agent (the same count-line, missing-base and mode rules the other Lockstep checks follow)

#### Scenario: Changed: Nothing changed gives a zero count and exit 0

- **GIVEN** a repository whose plan is the same as at the base
- **WHEN** the check runs
- **THEN** its last line is `RESULT changed requirements=0 unplanned=0 no_scenario=0 wording_only=0 exit=0`

#### Scenario: Changed: A missing base is reported, not crashed

- **GIVEN** a base revision that does not exist
- **WHEN** the check runs
- **THEN** it prints the skipped line and exits 0

#### Scenario: Changed: Mode off skips the check

- **GIVEN** `lockstep.yaml` with `checks: {changed: off}`
- **WHEN** `lockstep check changed` runs
- **THEN** it prints `skipped (off)` and exits 0

### Requirement: Test-first: A changed scenario needs a test that fails before the change

`lockstep check test-first --base <rev>` SHALL, for each scenario that both revisions define and whose text differs (runs of whitespace counting as one space; text from an active change's spec delta replacing the spec's), run every test marked for it against the base revision's source, and SHALL report `no-failing-test <scenario id>` and exit 1 when none of them fails there. It SHALL NOT check a scenario that a plan new or different from the base declares on a `Wording-only:` line, by its own ID or its requirement's. Its count line SHALL add `changed=<n>`, the number of changed scenarios checked, and `no_failing_test=<n>`.

Source: Brian, 2026-10-15: "we plan out with models and diagrams and then those are linked to tests presumablhy in a tdd way"; Brian, 2026-11-17: "the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842). That one failing test is enough for a changed scenario, where every test must fail for a new one, is inferred by agent (a changed scenario keeps tests for the parts that did not change).

#### Scenario: Test-first: A changed scenario whose tests all pass on the base fails the check

- **GIVEN** a scenario whose text differs from the base and whose only test passes on the base source
- **WHEN** the check runs
- **THEN** it reports `no-failing-test` for the scenario and exits 1

#### Scenario: Test-first: One test that fails on the base is enough for a changed scenario

- **GIVEN** a scenario whose text differs from the base, with one test that passes on the base source and one that fails there
- **WHEN** the check runs
- **THEN** it exits 0

#### Scenario: Test-first: A wording-only scenario is not checked

- **GIVEN** a scenario whose text differs from the base, whose only test passes on the base source, and a plan in the same change set with `Wording-only:` listing its requirement
- **WHEN** the check runs
- **THEN** it exits 0

### Requirement: Changed and test-first: The base is where the branch started

`lockstep check changed --base <rev>` and `lockstep check test-first --base <rev>` SHALL compare the current revision with the merge base of `<rev>` and the current commit, so that what was merged into `<rev>` after the branch started is not counted as this branch's change. When `<rev>` and the current commit share no history, or the repository has no commit yet, they SHALL compare with `<rev>` itself.

Source: inferred by agent, from the first run of the changed check on a branch behind `origin/main` (2026-11-17): four requirements merged there after the branch started were listed as removed and unplanned.

#### Scenario: Changed: A requirement added on the base branch after the branch started is not listed

- **GIVEN** a branch that changed no requirement, and a requirement added on `main` after the branch started
- **WHEN** `lockstep check changed --base main` runs on the branch
- **THEN** it lists no requirement and exits 0

#### Scenario: Test-first: A scenario reworded on the base branch after the branch started is not checked

- **GIVEN** a branch that changed no scenario, and a scenario reworded on `main` after the branch started
- **WHEN** `lockstep check test-first --base main` runs on the branch
- **THEN** it checks no changed scenario and exits 0

### Requirement: Trace: A marked quote matches its requirement

The trace check SHALL read, in every Markdown file tracked by git outside `openspec/`, each passage between `<!-- lockstep quote: <requirement id> -->` and `<!-- /lockstep quote -->`. It SHALL report `stale-quote` and fail when the passage, with runs of whitespace counting as one space, does not appear in the text of that requirement or of one of its scenarios, in `openspec/specs/` or in an active change's spec delta. It SHALL report `unknown` when no spec or active change defines the ID, and `unclosed-quote` when a start marker has no end marker after it in the same file. Each finding SHALL name the file and line of the start marker. In a folder that is not a git repository it SHALL read every Markdown file outside `openspec/` and folders whose name starts with a dot.

Source: Brian, 2026-10-22: "this doc string linkage system where the normative and docs tring stuff and gaps and planns would stay algined over time" (code2-workspace decision 0006); Brian, 2026-11-17: "if there is a change in the nromative docuemtnation ..." (code2-workspace issue 842, where seven hand-typed copies of one requirement's number stayed unchanged after the requirement changed). The marker form is inferred by agent.

#### Scenario: Trace: A quote that matches passes

- **GIVEN** a Markdown file with a marked passage that appears word for word in its requirement's statement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A quote left behind by a changed requirement fails

- **GIVEN** the same file after the requirement's statement changed so that the passage no longer appears in it
- **WHEN** the trace check runs
- **THEN** it reports `stale-quote` with the file and line, and exits 1

#### Scenario: Trace: A quote of a scenario's text passes

- **GIVEN** a marked passage that appears in the text of one of the requirement's scenarios
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A quote of an unknown requirement fails

- **GIVEN** a marked passage naming an ID no spec defines
- **WHEN** the trace check runs
- **THEN** it reports `unknown` for the passage and exits 1

#### Scenario: Trace: A quote matching an active change's text passes

- **GIVEN** a marked passage that appears only in an active change's spec delta for that requirement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A start marker with no end marker fails

- **GIVEN** a Markdown file with a start marker and no end marker after it
- **WHEN** the trace check runs
- **THEN** it reports `unclosed-quote` with the file and line, and exits 1

### Requirement: Changed: Documents that quote a listed requirement are listed with it

The changed check SHALL print, for each requirement it lists, every marked quote of it (`<!-- lockstep quote: <id> -->` in a tracked Markdown file outside `openspec/`) as `<path>:<line>` with the label `current` when the passage appears in the requirement's or its scenarios' current text and `stale` when it does not, and SHALL include them in its JSON output.

Source: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then that normative docuemtnation gets updated and then the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842). Inferred by agent: that the list shows documents beside code and tests.

#### Scenario: Changed: A document quoting a changed requirement is listed as stale

- **GIVEN** a requirement whose statement differs from the base and a Markdown file with a marked quote of the old statement's words
- **WHEN** `lockstep check changed --base <rev>` runs
- **THEN** the requirement's block names the file and line with the label `stale`
