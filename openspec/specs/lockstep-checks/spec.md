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

The test-first check SHALL not run a test marked `req(..., existing=True)`, and SHALL report how many
such tests it skipped.

Source: inferred by agent (working default awaiting Brian: tests marked existing=True for behavior that already worked are not run on the base revision, so existing repositories can adopt the format) Ported from code2-template `openspec/specs/test-first/spec.md` at 6ce00a9; approved for Lockstep by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

#### Scenario: Test-first: Existing-behavior test is skipped and counted

- **GIVEN** a scenario added since the base and its test, marked `existing=True`, that passes on the base
- **WHEN** the check runs
- **THEN** it exits 0 and lists the test as existing

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
