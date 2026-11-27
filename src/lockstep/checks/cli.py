"""`lockstep check <name> [options]`: run one commit check and apply its mode from `lockstep.yaml`.

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml,
    lockstep-checks/changed-count-line-and-exit-status

Requirement text (generated):
    lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml: `lockstep check
        <name>` (`trace`, `arch`, `test-first`, `sources`, `docmeta` and the others) SHALL read
        `checks:` in `lockstep.yaml` at the repository root, where each check is `block` (the
        default when absent or when there is no file), `warn` or `off`; `maintainability`,
        `helper-reuse` and `mutation` SHALL instead be `off` when absent, and a bare YAML `on` SHALL
        mean `block`. A failing `block` check SHALL exit 1; a failing `warn` check SHALL print a
        `warning:` line and exit 0; an `off` check SHALL not run, SHALL print `skipped (off)` and
        exit 0. A value other than those three, or an unknown check name, SHALL exit 2 naming it.
        The file's `sources.human_pattern` (default `brian`), `owner` (no default) and `likec4`
        (default `1.60.0`) settings SHALL be read from the same file. `lockstep check` with no name,
        or only `--repo`, `--base` and `--json`, SHALL keep running the whole-tree plan check.
    lockstep-checks/changed-count-line-and-exit-status: The changed check SHALL end with the line
        `RESULT changed requirements=<n> unplanned=<n> no_scenario=<n> wording_only=<n> small=<n>
        full=<n> no_plan_size=<n> no_planning_package=<n> exit=<0|1>`, exiting 1 when `unplanned`,
        `no_scenario`, `no_plan_size` or `no_planning_package` is above zero. `small` and `full`
        SHALL count the listed requirements of each size. When `<rev>` does not name a commit it
        SHALL check nothing, print `RESULT changed skipped="base <rev> not found" exit=0` and exit
        0. `changed` SHALL be a check name in `lockstep.yaml` with the same `block`, `warn` and
        `off` modes as the other checks.

Names: `trace`, `arch [gen|check]`, `test-first [--base REV]`, `sources [--json]`, `docmeta`, `project [--check]`,
`instructions [--chain FILE]`, `changed [--base REV] [--json]`, `maintainability [--base REV]`,
`helper-reuse [--base REV]`, `mutation [--timeout S] [--issue]` (these three off unless switched on); each takes
`--repo PATH` (default the current folder). The output is code2check's, ending in a `RESULT` line.
Exit: the check's own status when its mode is `block` (the default); 0 with a `warning:` line when
it fails and its mode is `warn`; 0 with `skipped (off)` and nothing run when `off`; 2 when
`lockstep.yaml` or the options cannot be read.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:cli.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml, lockstep-checks/changed-count-line-and-exit-status, lockstep-projection/project-status-and-show-are-lockstep-commands, lockstep-projection/status-lists-each-part-with-its-mode-and-last-gate-result

### Requirement: Each check can be set to block, warn or off in lockstep.yaml

`lockstep check <name>` (`trace`, `arch`, `test-first`, `sources`, `docmeta` and the others) SHALL read `checks:` in
`lockstep.yaml` at the repository root, where each check is `block` (the default when absent or when there
is no file), `warn` or `off`; `maintainability`, `helper-reuse` and `mutation` SHALL instead be `off` when absent,
and a bare YAML `on` SHALL mean `block`. A failing `block` check SHALL exit 1; a failing `warn` check SHALL print a
`warning:` line and exit 0; an `off` check SHALL not run, SHALL print `skipped (off)` and exit 0. A value
other than those three, or an unknown check name, SHALL exit 2 naming it. The file's `sources.human_pattern`
(default `brian`), `owner` (no default) and `likec4` (default `1.60.0`) settings SHALL be read from the
same file. `lockstep check` with no name, or only `--repo`, `--base` and `--json`, SHALL keep running the
whole-tree plan check.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (the three checks become Lockstep checks each repository switches on itself, off by default); earlier Brian, 2026-11-11, approving the one-tool design ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 4: the checks are Lockstep's, each switchable so another repository can adopt them one at a time).

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

#### Scenario: The three switched-on checks are off when absent

- **GIVEN** a `lockstep.yaml` that does not name `maintainability`, `helper-reuse` or `mutation`
- **WHEN** the settings are read
- **THEN** those three are `off` and `trace` is `block`; `mutation: on` reads as `block`, and `mutation.issue_repo` and
  `mutation.name` are read (an `issue_repo` that is not `OWNER/NAME` is an error)

### Requirement: Changed: Count line and exit status

The changed check SHALL end with the line `RESULT changed requirements=<n> unplanned=<n> no_scenario=<n> wording_only=<n> small=<n> full=<n> no_plan_size=<n> no_planning_package=<n> exit=<0|1>`, exiting 1 when `unplanned`, `no_scenario`, `no_plan_size` or `no_planning_package` is above zero. `small` and `full` SHALL count the listed requirements of each size. When `<rev>` does not name a commit it SHALL check nothing, print `RESULT changed skipped="base <rev> not found" exit=0` and exit 0. `changed` SHALL be a check name in `lockstep.yaml` with the same `block`, `warn` and `off` modes as the other checks.

Source: inferred by agent (the same count-line, missing-base and mode rules the other Lockstep checks follow; the four size fields count what the plan-size requirement reports)

#### Scenario: Changed: Nothing changed gives a zero count and exit 0

- **GIVEN** a repository whose plan is the same as at the base
- **WHEN** the check runs
- **THEN** its last line is `RESULT changed requirements=0 unplanned=0 no_scenario=0 wording_only=0 small=0 full=0 no_plan_size=0 no_planning_package=0 exit=0`

#### Scenario: Changed: A missing base is reported, not crashed

- **GIVEN** a base revision that does not exist
- **WHEN** the check runs
- **THEN** it prints the skipped line and exits 0

#### Scenario: Changed: Mode off skips the check

- **GIVEN** `lockstep.yaml` with `checks: {changed: off}`
- **WHEN** `lockstep check changed` runs
- **THEN** it prints `skipped (off)` and exits 0

### Requirement: Project, status and show are Lockstep commands

`lockstep check project`, `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool; `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other checks, and SHALL read source and test folders from `[tool.lockstep]` in `pyproject.toml`, else from `[tool.code2check]`.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: The commands are top-level and check modes apply

- **GIVEN** a repository with a stale docstring block
- **WHEN** `lockstep check project --check` runs with mode block, warn or off
- **THEN** it exits 1, exits 0 with a warning, or skips

### Requirement: Status lists each part with its mode and last gate result

`lockstep status --parts` SHALL print one row per AES part: each commit check named in `lockstep-checks`' check list
with its mode (`block`, `warn` or `off`, defaults as the commit checks apply them), `planning.gate` and
`planning.one_page_plans` (default `warn`), `planning.validator` and `planning.skills` only when `lockstep.yaml` sets
them, `guard.mode` (`warn (default)` when unset), and `rules` and `feedback` as `per-repository control unavailable`. Modes SHALL be read from
`lockstep.yaml` in the working tree with the same mode normalization as the hook and plugin settings, and the output SHALL say that ship reads the planning settings from the default
branch at origin. For `planning.gate` and `planning.one_page_plans` the last result SHALL be the outcome, time and short
head of the newest record (by its `time`) among `planning-verdicts/*.jsonl` in ship's log folder (`$SHIP_LOG_DIR`, else
`~/code2/.ship-logs` where `~/code2` exists, else the XDG state folder) whose `repo` is this repository's owner/name from
origin, gate `planning gate` or `one-page plans`; every other row, and a gate with no matching record, SHALL say
`no record`. A record line that is not JSON SHALL be skipped. `--json` SHALL print the rows as a JSON list. The command
SHALL exit 0, and 2 when `lockstep.yaml` cannot be read or holds a value the commit checks reject.

Source: Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece" (docs/planning/next.goal.md, parking item "`lockstep status` prints each part's mode and last result"). Inferred by agent: the parts table is a `--parts` flag on the existing `lockstep status` (already the requirement report), the row list, and showing a record's outcome rather than its mode text.

#### Scenario: Each part's mode comes from the working tree's settings

- **GIVEN** a repository whose `lockstep.yaml` sets `checks: {trace: warn}` and `planning: {gate: block}` and no guard
- **WHEN** `lockstep status --parts --json` runs
- **THEN** trace is `warn`, mutation is `off`, arch is `block`, `planning.gate` is `block`, `planning.one_page_plans` is `warn`, `guard.mode` is `warn (default)`, rules and feedback are `per-repository control unavailable`, and no validator row is listed

#### Scenario: The newest planning-gate record for this repository is shown

- **GIVEN** ship's log folder holding records for this repository's planning gate on two days and a newer record for another repository
- **WHEN** `lockstep status --parts` runs
- **THEN** the planning gate row shows the outcome and head of this repository's newer record, and `planning.one_page_plans` says `no record`

#### Scenario: Unreadable settings exit 2

- **GIVEN** a `lockstep.yaml` whose check mode is not block, warn or off
- **WHEN** `lockstep status --parts` runs
- **THEN** it exits 2 naming the problem

Tested by: tests/lockstep/checks/test_lockstep_check_changed.py, tests/lockstep/checks/test_lockstep_check_parts.py, tests/lockstep/checks/test_lockstep_check_plugin.py, tests/lockstep/checks/test_lockstep_checks_config.py
[[[end]]]
"""

import argparse
import json
from pathlib import Path
import sys

import yaml

from lockstep.checks import (arch, changed, docmeta, helper_reuse, instructions, maintainability, mutation, plugin_settings, project, show,
                             sources, status, suppressions, test_first, trace)
from lockstep.checks.config import CHECK_NAMES, Config, ConfigError, load


def _trace(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print trace findings and return the exit status."""
    findings = trace.check(root)
    for f in findings:
        print(f"{f.kind:13} {f.id}  ({f.where})")
    print(f"RESULT trace findings={len(findings)} exit={int(bool(findings))}")
    return int(bool(findings))


def _arch(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Write or compare the import contracts and return the exit status."""
    action = args.action
    try:
        text = arch.generate(root, cfg.likec4)
    except arch.DiagramToolUnavailable as err:
        print(err)
        print(f"RESULT arch-{action} tool_unavailable=1 exit=1")
        return 1
    except arch.DiagramInvalid as err:
        print(err)
        print(f"RESULT arch-{action} invalid_diagram=1 exit=1")
        return 1
    path = root / arch.CONTRACTS
    if action == "gen":
        path.write_text(text)
        print(f"RESULT arch-gen wrote={path.name} exit=0")
        return 0
    current = path.read_text() if path.exists() else ""
    stale = current != text
    if stale:
        print(f"{path.name} does not match the diagram; run: lockstep check arch gen")
        print(f"RESULT arch-check stale=1 exit=1")
        return 1
    try:
        broken, report = arch.lint_imports(root)
    except arch.ImportLinterMissing as err:
        print(err)
        print("RESULT arch-check stale=0 import_linter_missing=1 exit=1")
        return 1
    if broken:
        print(report)
    print(f"RESULT arch-check stale=0 broken_contracts={broken} exit={int(bool(broken))}")
    return int(bool(broken))


def _test_first(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print tests that passed on base and return the exit status."""
    try:
        result = test_first.check(root, args.base)
    except test_first.PytestUnavailable as err:
        print(err)
        print("RESULT test-first pytest_unavailable=1 exit=1")
        return 1
    if result.skipped:
        print(f"RESULT test-first skipped=\"{result.skipped}\" exit=0")
        return 0
    for node in result.passed_before:
        print(f"passed-before {node}  (it does not prove the new behavior)")
    for node in result.existing:
        print(f"existing      {node}  (marked existing=True; not run on the base)")
    for ident in result.no_failing_test:
        print(f"no-failing-test {ident}  (its text changed and no test marked for it fails on the base source; "
              "change a test, or add `Wording-only: <id>` to the plan)")
    print(f"RESULT test-first checked={len(result.checked)} existing={len(result.existing)} "
          f"passed_before={len(result.passed_before)} changed={len(result.changed)} "
          f"no_failing_test={len(result.no_failing_test)} exit={int(not result.ok)}")
    return int(not result.ok)


def _changed(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print each requirement changed since the base (or JSON), its findings and the count line; return the exit status.

    With `--json` the JSON goes to stdout, the finding lines to stderr and the RESULT line last on stdout,
    as `sources --json` does.
    """
    result = changed.check(root, args.base)
    if result.skipped:
        print(f"RESULT changed skipped=\"{result.skipped}\" exit=0")
        return 0
    if args.json:
        print(json.dumps(result.as_dict(), indent=1))
    else:
        for item in result.requirements:
            tests = ", ".join(f"{t['node']} ({t['label']})" for t in item.tests)
            print(f"{item.kind:13} {item.id}  ({item.where})")
            print(f"  {'differs':11} {'; '.join(item.differs)}")
            print(f"  {'code':11} {', '.join(item.implementers) or '-'}")
            print(f"  {'tests':11} {tests or '-'}")
            documents = ", ".join(f"{d['where']} ({d['label']})" for d in item.documents)
            print(f"  {'documents':11} {documents or '-'}")
            print(f"  {'plan':11} {', '.join(item.plans) or 'none'}")
            print(f"  {'size':11} {item.size or '-'}")
    out = sys.stderr if args.json else sys.stdout
    for item in result.requirements:
        if "unplanned" in item.findings:
            print(f"unplanned     {item.id}  (no change or plan page added or edited since {args.base} names it)", file=out)
        if "no-scenario-changed" in item.findings:
            print(f"no-scenario-changed  {item.id}  (the statement changed and no scenario under it is new or "
                  f"different; change a scenario and its test, or add `Wording-only: {item.id}` to the plan)", file=out)
        if "no-plan-size" in item.findings:
            print(f"no-plan-size  {item.id}  (no plan naming it states its size; add the line `Plan size: small` "
                  f"or `Plan size: full` to {', '.join(item.size_files)})", file=out)
        if "no-planning-package" in item.findings:
            named = ", ".join(item.missing_packages)
            why = f"the planning package it names is not a file: {named}" if named else "no plan naming it has a `Planning package: <path>` line"
            print(f"no-planning-package  {item.id}  (its plan size is full and {why}; add the line "
                  f"`Planning package: <path>` naming the package file, or state `Plan size: small`)", file=out)
    for item in result.requirements:
        if item.wording_only:
            print(f"wording-only  {item.id}  ({item.wording_only})", file=out)
    print("RESULT changed " + " ".join(f"{k}={v}" for k, v in result.counts().items()) + f" exit={int(not result.ok)}")
    return int(not result.ok)


def _suppressions(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print each added suppression with no reason and the count line; return the exit status."""
    result = suppressions.check(root, args.base)
    if result.skipped:
        print(f"RESULT suppressions skipped=\"{result.skipped}\" exit=0")
        return 0
    for finding in result.unreasoned:
        print(f"unreasoned {finding}  (add a further `#` comment of three or more words saying why; for an "
              "import-linter ignore in .importlinter or setup.cfg, a comment line directly above it)")
    print(f"RESULT suppressions added={result.added} reasoned={result.added - len(result.unreasoned)} "
          f"unreasoned={len(result.unreasoned)} exit={int(not result.ok)}")
    return int(not result.ok)


def _sources(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print items without a source (or all items as JSON) and return the exit status."""
    items = sources.check(root, cfg.human_pattern)
    missing = [i for i in items if i.source == "missing"]
    if args.json:
        print(json.dumps(sources.as_dicts(items), indent=1))
    for i in missing:
        print(f"no-source     {i.id}  ({i.where}); add a line: Source: Brian, <date>: \"<quote>\" or "
              "Source: inferred by agent (<basis>)", file=sys.stderr if args.json else sys.stdout)
    first = [i for i in items if i.source_first]
    for i in first:
        print(f"source-first  {i.id}  ({i.where}); put the statement first and the Source: line after it",
              file=sys.stderr if args.json else sys.stdout)
    failed = bool(missing or first)
    counts = {k: sum(i.source == k for i in items) for k in ("brian", "inferred", "other", "missing")}
    print("RESULT sources " + " ".join(f"{k}={v}" for k, v in counts.items()) + f" source_first={len(first)} exit={int(failed)}")
    return int(failed)


def _docmeta(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print the docmeta count line and one line per finding; return 1 on any finding."""
    result = docmeta.check(root)
    print(result.count_line())
    for f in result.findings:
        print(f"{f.kind:28} {f.where}  ({f.reason})")
    return int(bool(result.findings))


def _instructions(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Print the instructions count line and one line per finding; return 1 on any finding."""
    chain = None if args.chain is None else [Path(p).expanduser() for p in args.chain if p != "none"]
    result = instructions.check(root, chain)
    print(result.count_line())
    for f in result.findings:
        print(f"{f.kind:20} {f.where}  ({f.reason})")
    return int(bool(result.findings))


def _project(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Rewrite generated blocks (or with --check, list stale ones) and return the exit status.

    Implements: lockstep-projection/project-status-and-show-are-lockstep-commands

    Requirement text (generated):
        lockstep-projection/project-status-and-show-are-lockstep-commands: `lockstep check project`,
            `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool;
            `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other
            checks, and SHALL read source and test folders from `[tool.lockstep]` in
            `pyproject.toml`, else from `[tool.code2check]`.
    """
    changed = project.project(root, check=args.check)
    for path in changed:
        print(f"stale         {path}" if args.check else f"rewrote {path}")
    missing = project.missing_copies(root)
    for path in missing:
        print(f"no-copy       {path}")
    if missing:
        print("a planned file under a fixed: glob has no plan copy; add one (lockstep layout writes the form)"
              " then run: lockstep check project")
    refusals, warnings = plugin_settings.drift(root)  # planning.skills; not a ship gate
    for line in warnings:
        print(f"warning: {line}")
    for line in refusals:
        print(f"refused: {line}")
    if args.check:
        if changed:
            print("generated blocks are out of date; run: lockstep check project")
        failed = bool(changed or missing or refusals)
        print(f"RESULT project stale={len(changed)} no_copy={len(missing)} exit={int(failed)}")
        return int(failed)
    failed = bool(missing or refusals)
    print(f"RESULT project rewrote={len(changed)} no_copy={len(missing)} exit={int(failed)}")
    return int(failed)


def run_status(argv: list[str]) -> int:
    """`lockstep status [--json|--md] [--repo PATH]`: print the status table, JSON or Markdown page; exit 0.

    Implements: lockstep-projection/project-status-and-show-are-lockstep-commands

    Requirement text (generated):
        lockstep-projection/project-status-and-show-are-lockstep-commands: `lockstep check project`,
            `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool;
            `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other
            checks, and SHALL read source and test folders from `[tool.lockstep]` in
            `pyproject.toml`, else from `[tool.code2check]`.

    Args:
        argv: The options after `status`.

    Returns:
        0, or 2 when the options cannot be read.
    """
    ap = argparse.ArgumentParser(prog="lockstep status", description="each requirement's code, tests and result")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    ap.add_argument("--md", action="store_true", help="print the report as the Markdown status page")
    ap.add_argument("--parts", action="store_true", help="each part's mode and last planning-gate result instead")
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    if args.parts:
        return _run_parts(args.repo, as_json=args.json, md=args.md)
    result = status.report(args.repo)
    if args.md:
        print(status.markdown(result))
        return 0
    if args.json:
        print(json.dumps(result.as_dict(), indent=1))
    else:
        print(f"results: {result.results_note}")
        for ident, req in result.requirements.items():
            print(f"{req.state:24} {ident}  {', '.join(req.links) or '-'}")
            for sid, sc in result.scenarios.items():
                if sc.requirement == ident:
                    print(f"  {sc.state:22} {sid}  {', '.join(sc.links) or '-'}")
        for plan in result.plans:
            shown = ", ".join(f"{i} ({s})" for i, s in plan.open.items()) or "none"
            print(f"plan {plan.path}: {len(plan.closes)} closes, open: {shown}")
    print("RESULT status " + " ".join(f"{k}={v}" for k, v in result.counts().items()) + " exit=0")
    return 0


def _run_parts(repo: Path, *, as_json: bool, md: bool) -> int:
    """`lockstep status --parts [--json]`: print each part's mode and last result; 2 for --md or unreadable settings.

    Implements: lockstep-projection/status-lists-each-part-with-its-mode-and-last-gate-result

    Requirement text (generated):
        lockstep-projection/status-lists-each-part-with-its-mode-and-last-gate-result: `lockstep
            status --parts` SHALL print one row per AES part: each commit check named in
            `lockstep-checks`' check list with its mode (`block`, `warn` or `off`, defaults as the
            commit checks apply them), `planning.gate` and `planning.one_page_plans` (default
            `warn`), `planning.validator` and `planning.skills` only when `lockstep.yaml` sets them,
            `guard.mode` (`warn (default)` when unset), and `rules` and `feedback` as
            `per-repository control unavailable`. Modes SHALL be read from `lockstep.yaml` in the
            working tree with the same mode normalization as the hook and plugin settings, and the
            output SHALL say that ship reads the planning settings from the default branch at
            origin. For `planning.gate` and `planning.one_page_plans` the last result SHALL be the
            outcome, time and short head of the newest record (by its `time`) among
            `planning-verdicts/*.jsonl` in ship's log folder (`$SHIP_LOG_DIR`, else
            `~/code2/.ship-logs` where `~/code2` exists, else the XDG state folder) whose `repo` is
            this repository's owner/name from origin, gate `planning gate` or `one-page plans`;
            every other row, and a gate with no matching record, SHALL say `no record`. A record
            line that is not JSON SHALL be skipped. `--json` SHALL print the rows as a JSON list.
            The command SHALL exit 0, and 2 when `lockstep.yaml` cannot be read or holds a value the
            commit checks reject.
    """
    from lockstep.checks import parts
    if md:
        print("lockstep status: --parts has no Markdown page; use --json or the table", file=sys.stderr)
        return 2
    try:
        rows = parts.parts(repo)
    except ConfigError as exc:
        print(f"lockstep status: {exc}", file=sys.stderr)
        return 2
    print(parts.as_json(rows) if as_json else parts.table(rows))
    return 0


def run_show(argv: list[str]) -> int:
    """`lockstep show FILE [--repo PATH]`: print the requirements a file implements; exit 0.

    Implements: lockstep-projection/project-status-and-show-are-lockstep-commands

    Requirement text (generated):
        lockstep-projection/project-status-and-show-are-lockstep-commands: `lockstep check project`,
            `lockstep status` and `lockstep show` SHALL be commands of the one `lockstep` tool;
            `project` SHALL take its mode (block, warn or off) from `lockstep.yaml` like the other
            checks, and SHALL read source and test folders from `[tool.lockstep]` in
            `pyproject.toml`, else from `[tool.code2check]`.

    Args:
        argv: The file, then options.

    Returns:
        0, or 2 when the options cannot be read.
    """
    ap = argparse.ArgumentParser(prog="lockstep show", description="the requirements a file implements")
    ap.add_argument("file")
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    text = show.show(args.repo, args.file)
    print(text or f"{args.file} implements no requirement", end="" if text else "\n")
    print(f"RESULT show requirements={sum(1 for line in text.splitlines()[1:] if not line.startswith(' '))} exit=0")
    return 0


def _maintainability(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """New maintainability findings since the base; see `lockstep.checks.maintainability`."""
    return maintainability.run(root, args.base, tuple(args.folders.split(",")), args.max_lines)


def _helper_reuse(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """New functions that rewrite an existing helper; see `lockstep.checks.helper_reuse`."""
    return helper_reuse.run(root, args.base, tuple(args.folders.split(",")), args.head)


def _mutation(root: Path, args: argparse.Namespace, cfg: Config) -> int:
    """Surviving mutants; see `lockstep.checks.mutation`."""
    return mutation.run(root, args.timeout, args.issue, cfg.mutation_issue_repo, cfg.mutation_name)


_BASE = (("--base",), {"default": "origin/main"})
_FOLDERS = (("--folders",), {"default": "src,scripts", "help": "comma-separated folders to read"})
# check name -> the options it takes beyond `--repo`, as (flags, add_argument keywords)
_OPTIONS: dict[str, list[tuple[tuple[str, ...], dict]]] = {
    "arch": [(("action",), {"nargs": "?", "choices": ["gen", "check"], "default": "check"})],
    "test-first": [_BASE],
    "changed": [_BASE, (("--json",), {"action": "store_true", "help": "print every listed requirement as JSON"})],
    "suppressions": [_BASE],
    "instructions": [(("--chain",), {"action": "append", "help": "file loaded before the repository's own (repeatable; "
                      "`none` for no chain); default: INSTRUCTION_CHAIN, else the workspace core.md and AGENTS.md"})],
    "project": [(("--check",), {"action": "store_true", "help": "fail when a generated block is stale, writing nothing"})],
    "sources": [(("--json",), {"action": "store_true", "help": "print every item with its source"})],
    "maintainability": [_BASE, _FOLDERS, (("--max-lines",), {"type": int, "default": 800,
                                                             "help": "a file over this that grew is a finding"})],
    "helper-reuse": [_BASE, _FOLDERS, (("--head",), {"default": None,
                                                     "help": "read the branch at this revision, not the working tree"})],
    "mutation": [(("--timeout",), {"type": int, "default": mutation.TIMEOUT, "help": "seconds before mutmut is stopped"}),
                 (("--issue",), {"action": "store_true", "help": "keep one owner:agent issue listing the survivors"})],
}


def run(argv: list[str]) -> int:
    """Run the named check, `argv[0]`, with its options and apply its mode.

    Args:
        argv: The check name, then its options.

    Returns:
        The exit status described in the module docstring.
    """
    ap = argparse.ArgumentParser(prog="lockstep check", description="run one commit check")
    sub = ap.add_subparsers(dest="name", required=True)
    for name in CHECK_NAMES:
        p = sub.add_parser(name)
        p.add_argument("--repo", type=Path, default=Path.cwd())
        for flags, kwargs in _OPTIONS.get(name, []):
            p.add_argument(*flags, **kwargs)
    try:
        args = ap.parse_args(argv)
    except SystemExit as exit_:
        return int(exit_.code or 0) if isinstance(exit_.code, int) else 2
    root = args.repo
    try:
        cfg = load(root)
    except ConfigError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    mode = cfg.mode(args.name)
    if mode == "off":
        print(f"{args.name}: skipped (off)")
        return 0
    runner = {"trace": _trace, "arch": _arch, "test-first": _test_first, "sources": _sources, "docmeta": _docmeta,
              "instructions": _instructions, "project": _project, "changed": _changed,
              "suppressions": _suppressions, "maintainability": _maintainability, "helper-reuse": _helper_reuse,
              "mutation": _mutation}
    try:
        status = runner[args.name](root, args, cfg)
    except (ValueError, TypeError, OSError, SyntaxError, yaml.YAMLError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    if status and mode == "warn":
        print(f"warning: {args.name} failed (mode warn in lockstep.yaml); not blocking")
        return 0
    return status
