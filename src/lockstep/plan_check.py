"""`lockstep plan check [--repo PATH] [--json]`: run Company Planning's validator on the repository's plan.

There is one plan checker: Company Planning's `validate_planning_package.py`. `ship` runs it on every merge, and this
command runs the same validator, fetched and started by the same functions (`fetch_planning_validator` below, which
`ship` calls, and `lockstep.ship.validator_python`), so a plan passes or fails the same way in both places. Until 2026-11-25 this file held a
port of two of the validator's checks (the acceptance file and requirement coverage) and a copy of its citation-anchor
code; they were removed so the rules live in one place (`openspec/specs/lockstep-plan-check/spec.md`).

The work-unit DAG (`docs/planning/work-units.json`, `lockstep plan units`) is Lockstep's own check and is added here.

Exit: the validator's status (0 passes, 1 problems; a package failing only freshness passes with a warning, as in
`ship`), 1 also when the work units have problems, 2 when there is no planning package or the validator cannot be
fetched or run, or exits with another status.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:plan_check.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-check/lockstep-plan-check-runs-company-planning-s-validator, lockstep-plan-check/the-validator-s-source-is-set-in-lockstep-yaml, lockstep-plan-check/the-validator-can-use-an-installed-graph-schema

### Requirement: `lockstep plan check` runs Company Planning's validator

`lockstep plan check` SHALL accept `--repo PATH` (default the current directory) and `--json`. It SHALL run Company
Planning's `validate_planning_package.py` on `docs/planning/planning-package.json` under the repository, fetched from
origin/main of Company Planning and run by the same function and interpreter choice `ship` uses (so
`SHIP_PLANNING_VALIDATOR`, `SHIP_COMPANY_PLANNING` and `SHIP_VALIDATOR_PYTHON` work the same), print the validator's
output, and exit with the validator's exit status, except that, as in `ship`, a package that fails only the freshness
check (it passes with `--no-freshness`) exits 0 with a warning. When `docs/planning/work-units.json` exists it SHALL also report the
work-unit problems and exit 1 when there are any. It SHALL exit 2, saying why, when the repository has no planning
package or the validator cannot be fetched or run, or exits with a status other than 0 or 1. With `--json` it SHALL print one object with `ok`, the validator's
exit status and output, and the work-unit problems. Lockstep SHALL hold no copy of the validator's checks.

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5: "`lockstep plan check` validates it"); one plan checker approved by Brian, 2026-11-25: "ia prpove yourr ecommednations though" (Company Planning's validator kept as that checker: inferred by agent, the archived one-plan-checker proposal, restored by `docs/retired/2026-11-25.md`).

#### Scenario: The validator's verdict is the command's verdict

- **GIVEN** a repository with a planning package and a validator that exits 1
- **WHEN** `lockstep plan check` runs
- **THEN** it prints the validator's output and exits 1; with a validator that exits 0 it exits 0

#### Scenario: A package out of date only by freshness passes with a warning

- **GIVEN** a validator that exits 1, and 0 with `--no-freshness`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and prints a warning that the package is out of date

#### Scenario: A repository with no planning package cannot be checked

- **GIVEN** a repository without `docs/planning/planning-package.json`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and names the missing package

#### Scenario: Work-unit problems are added

- **GIVEN** a planning package the validator passes and a work-units file with a unit depending on a missing unit
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names the work-unit problem

### Requirement: The validator's source is set in lockstep.yaml

`ship` and `lockstep plan check` SHALL take Company Planning's validator from the first of: `SHIP_PLANNING_VALIDATOR`
(a file, used as given); `SHIP_COMPANY_PLANNING` (a local Company Planning checkout, read at `origin/<ref>`);
`planning.validator.repo` in `lockstep.yaml` on the repository's default branch at `origin` (an address git can clone,
kept as a bare clone under `$XDG_CACHE_HOME/lockstep/`, default `~/.cache/lockstep/`, in a folder named by a hash of
the address, cloned or fetched under a file lock with `GIT_TERMINAL_PROMPT=0`, ssh `BatchMode=yes` and a 300-second
timeout, and read at `<ref>`); else `~/code2/company-planning` read at `origin/<ref>`. `planning.validator.ref` SHALL
name a branch, `main` when absent. Each run SHALL print and log the line `ship: planning validator: <source>` naming
the source that won and why, and SHALL print and log a warning when an environment variable overrides a configured
repository. A `planning.validator` that is not a mapping of a text `repo` and an optional text `ref` SHALL refuse with
a configuration error naming the setting. A clone or fetch that fails or times out SHALL be reported as the validator
not fetchable, naming the address. Credentials SHALL come only from the user's own git setup, never from
`lockstep.yaml`.

Source: Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece." Inferred by agent: the order of sources, the cache, the default branch `main` and the log line (`docs/planning/next.goal.md`, slice 2).

#### Scenario: A configured repository is the source

- **GIVEN** `lockstep.yaml` on the default branch naming `planning.validator.repo`, and neither environment variable set
- **WHEN** `lockstep plan check` runs
- **THEN** the validator from that repository runs, and the output names that repository as the source

#### Scenario: An environment variable overrides a configured repository with a warning

- **GIVEN** a configured repository and `SHIP_COMPANY_PLANNING` set
- **WHEN** `lockstep plan check` runs
- **THEN** the validator from `SHIP_COMPANY_PLANNING` runs and a warning names the configured repository it overrode

#### Scenario: The ref picks the branch

- **GIVEN** a configured repository whose `release` branch holds a different validator, and `ref: release`
- **WHEN** `lockstep plan check` runs
- **THEN** the validator from the `release` branch runs

#### Scenario: An unreachable configured repository cannot be fetched

- **GIVEN** a configured repository address that does not exist
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and names the address it could not fetch

#### Scenario: A bad validator setting is a configuration error

- **GIVEN** `planning.validator` set to a text instead of a mapping
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and names `planning.validator`

### Requirement: The validator can use an installed graph schema

When the operator sets a nonempty `SHIP_TYPED_GRAPH_SCHEMA`, both `ship` and `lockstep plan check` SHALL pass that local path as the value of the Company Planning validator's `--typed-graph-schema` option for the initial check and any freshness retry. An unset or empty variable SHALL leave the option absent so that the selected validator uses its own default. The validator SHALL continue to judge the graph.

Source: Brian, 2026-11-27, AES clean Linux validator goal. Inferred by agent: reuse the upstream CLI option and the existing trusted shell settings for validator dependencies.

#### Scenario: Both validator entry points use the installed graph schema

- **GIVEN** an operator-provisioned schema whose path contains a space and a real package due for a fresh review
- **WHEN** either command runs the validator and retries without the freshness check
- **THEN** both invocations receive the same schema path as one argument

Tested by: tests/lockstep/test_lockstep_plan_check.py, tests/test_ship.py

Declares (typed signatures, from the plan):
  validator_command(python: list[str], validator: str, repo: Path) -> list[str]
  fetch_planning_validator(run: Run) -> tuple[str | None, str | None]
  run_validator(repo: Path) -> tuple[int, str]
  unit_problems(repo: Path) -> list[str]
[[[end]]]
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lockstep.ship import Run

PACKAGE = "docs/planning/planning-package.json"
UNITS = "docs/planning/work-units.json"


class Unreadable(Exception):
    """The file cannot be checked at all (exit 2)."""


def _load(path: Path) -> Any:
    """Read a JSON file, raising Unreadable when it is missing or is not JSON."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise Unreadable(f"{path}: not found") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise Unreadable(f"{path}: cannot read ({exc})") from exc
    except json.JSONDecodeError as exc:
        raise Unreadable(f"{path}: not JSON ({exc})") from exc


def _say(run: Run, line: str) -> None:
    print(line)
    run.write(line)


def _cached_clone(run: Run, address: str) -> tuple[Path | None, str | None]:
    """A bare clone of `address` under $XDG_CACHE_HOME/lockstep/, cloned or fetched now under a lock: (folder, None),
    or (None, why not). No password prompt (GIT_TERMINAL_PROMPT=0, ssh BatchMode) and a 300-second limit."""
    import fcntl
    import hashlib
    cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "lockstep"
    cache.mkdir(parents=True, exist_ok=True)
    folder = cache / f"{hashlib.sha256(address.encode()).hexdigest()[:16]}.git"
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0",
           "GIT_SSH_COMMAND": f"{os.environ.get('GIT_SSH_COMMAND', 'ssh')} -o BatchMode=yes"}
    with open(cache / f"{folder.stem}.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        cmd = (["git", "-C", str(folder), "fetch", "-q", "--prune", address, "+refs/heads/*:refs/heads/*"]
               if folder.is_dir() else ["git", "clone", "-q", "--bare", address, str(folder)])
        try:
            done = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
        except subprocess.TimeoutExpired:
            return None, f"could not fetch {address} within 300 seconds, so the planning package cannot be validated"
    _say(run, f"ship: fetch {address} into {folder}: exit status {done.returncode}")
    run.write(done.stdout + done.stderr)
    if done.returncode:
        said = (done.stderr.strip().splitlines() or [""])[-1]
        return None, f"could not fetch {address} ({said}), so the planning package cannot be validated"
    return folder, None


def fetch_planning_validator(run: Run) -> tuple[str | None, str | None]:
    """Return (path of Company Planning's validate_planning_package.py, None), or (None, why it cannot be had).

    The source is the first of $SHIP_PLANNING_VALIDATOR (taken as given), $SHIP_COMPANY_PLANNING (a checkout read at
    origin/<ref>), `planning.validator` in lockstep.yaml on the default branch (a cached bare clone read at <ref>), and
    ~/code2/company-planning at origin/<ref>; the validator's folder is extracted into the log folder. `ship` and
    `lockstep plan check` both call this, so a plan is checked by one validator.

    Implements: lockstep-plan-check/the-validator-s-source-is-set-in-lockstep-yaml

    Requirement text (generated):
        lockstep-plan-check/the-validator-s-source-is-set-in-lockstep-yaml: `ship` and `lockstep
            plan check` SHALL take Company Planning's validator from the first of:
            `SHIP_PLANNING_VALIDATOR` (a file, used as given); `SHIP_COMPANY_PLANNING` (a local
            Company Planning checkout, read at `origin/<ref>`); `planning.validator.repo` in
            `lockstep.yaml` on the repository's default branch at `origin` (an address git can
            clone, kept as a bare clone under `$XDG_CACHE_HOME/lockstep/`, default
            `~/.cache/lockstep/`, in a folder named by a hash of the address, cloned or fetched
            under a file lock with `GIT_TERMINAL_PROMPT=0`, ssh `BatchMode=yes` and a 300-second
            timeout, and read at `<ref>`); else `~/code2/company-planning` read at `origin/<ref>`.
            `planning.validator.ref` SHALL name a branch, `main` when absent. Each run SHALL print
            and log the line `ship: planning validator: <source>` naming the source that won and
            why, and SHALL print and log a warning when an environment variable overrides a
            configured repository. A `planning.validator` that is not a mapping of a text `repo` and
            an optional text `ref` SHALL refuse with a configuration error naming the setting. A
            clone or fetch that fails or times out SHALL be reported as the validator not fetchable,
            naming the address. Credentials SHALL come only from the user's own git setup, never
            from `lockstep.yaml`.

    Raises:
        ConfigError: `planning.validator` in lockstep.yaml is malformed.
    """
    from lockstep.checks.config import validator_source
    from lockstep.ship import GOAL_PROVENANCE, VALIDATOR

    configured = validator_source(run.repo)
    validator = os.environ.get("SHIP_PLANNING_VALIDATOR")
    checkout = os.environ.get("SHIP_COMPANY_PLANNING")
    overriding = "SHIP_PLANNING_VALIDATOR" if validator else "SHIP_COMPANY_PLANNING" if checkout else None
    if configured and overriding:
        _say(run, f"ship: warning: {overriding} overrides planning.validator.repo {configured[0]} in lockstep.yaml")
    if validator:
        _say(run, f"ship: planning validator: {validator} (SHIP_PLANNING_VALIDATOR)")
    else:
        ref = configured[1] if configured else "main"
        if configured and not checkout:
            folder, refused = _cached_clone(run, configured[0])
            if folder is None:
                return None, refused
            source, tree, said = folder, ref, f"{configured[0]} at {ref} (lockstep.yaml planning.validator)"
        else:
            source = Path(checkout or Path.home() / "code2" / "company-planning")
            if run.step("fetch company-planning", ["git", "-C", str(source), "fetch", "-q", "origin"]).returncode:
                return None, f"could not fetch {source}, so the planning package cannot be validated"
            tree = f"origin/{ref}"
            said = f"{source} at {tree} ({'SHIP_COMPANY_PLANNING' if checkout else 'the default checkout'})"
        _say(run, f"ship: planning validator: {said}")
        # the validator imports its sibling modules (coverage_check.py), so extract the whole scripts folder;
        # it finds goal_provenance.py three folders up, so every path keeps its place in company-planning
        scripts_dir = str(Path(VALIDATOR).parent)
        present = [p for p in GOAL_PROVENANCE
                   if subprocess.run(["git", "-C", str(source), "cat-file", "-e", f"{tree}:{p}"],
                                     capture_output=True).returncode == 0]
        archive = Path(run.log.parent) / "planning-validator.tar"
        target = Path(run.log.parent) / "planning-validator"
        target.mkdir(parents=True, exist_ok=True)
        made = run.step(f"archive the validator folder from company-planning {tree}",
                        ["git", "-C", str(source), "archive", "-o", str(archive), tree, scripts_dir, *present])
        if made.returncode:
            return None, f"could not archive {scripts_dir} from {source} {tree}"
        unpacked = run.step("unpack the validator folder", ["tar", "-x", "-f", str(archive), "-C", str(target)])
        if unpacked.returncode:
            return None, f"could not unpack {scripts_dir} into {target}"
        validator = str(target / VALIDATOR)
    if not Path(validator).is_file():
        return None, f"the planning validator {validator} does not exist"
    return validator, None


def validator_command(python: list[str], validator: str, repo: Path) -> list[str]:
    """Build the shared validator command, keeping the schema selected by the operator.

    Implements: lockstep-plan-check/the-validator-can-use-an-installed-graph-schema

    Requirement text (generated):
        lockstep-plan-check/the-validator-can-use-an-installed-graph-schema: When the operator sets
            a nonempty `SHIP_TYPED_GRAPH_SCHEMA`, both `ship` and `lockstep plan check` SHALL pass
            that local path as the value of the Company Planning validator's `--typed-graph-schema`
            option for the initial check and any freshness retry. An unset or empty variable SHALL
            leave the option absent so that the selected validator uses its own default. The
            validator SHALL continue to judge the graph.
    """
    command = [*python, validator, "--repo", str(repo), str(repo / PACKAGE)]
    schema = os.environ.get("SHIP_TYPED_GRAPH_SCHEMA")
    if schema:
        command.extend(["--typed-graph-schema", str(Path(schema).expanduser().absolute())])
    return command


def run_validator(repo: Path) -> tuple[int, str]:
    """Run Company Planning's validator on the repository's package the way `ship` does: (exit status, output).

    As in `ship`, a package that fails only the freshness check (plan content changed since its cold review) passes
    with a warning. Exit status 2 with the reason when there is no package or the validator cannot be fetched, started
    or finished, or exits with a status other than 0 or 1. The validator is unpacked into a fresh folder per run, so a
    `ship` running at the same time is not disturbed, and nothing is written to ship's day log; ship's progress lines
    go to stderr so `--json` output stays one object.
    """
    from lockstep.ship import Run, import_failure, validator_python

    package = repo / PACKAGE
    if not package.is_file():
        return 2, f"cannot check: no planning package at {package}"
    with tempfile.TemporaryDirectory(prefix="lockstep-plan-check-") as work:
        with contextlib.redirect_stdout(sys.stderr):
            run = Run(repo, log_dir=Path(work))  # its log and the unpacked validator live in this run's own folder
            from lockstep.checks.config import ConfigError
            try:
                validator, refused = fetch_planning_validator(run)
            except ConfigError as exc:
                validator, refused = None, str(exc)
            python = validator_python(run) if validator else None
        if validator is None:
            return 2, f"cannot check: {refused}"
        if python is None:
            return 2, ("cannot check: no interpreter has the validator's packages; set SHIP_VALIDATOR_PYTHON to one "
                       "that imports jsonschema and pydantic")

        command = validator_command(python, validator, repo)

        def validate(*extra: str) -> subprocess.CompletedProcess:
            """Run the validator once."""
            return subprocess.run([*command, *extra],
                                  capture_output=True, text=True, timeout=900)

        try:
            result = validate()
            output = (result.stdout + result.stderr).rstrip()
            broken = import_failure(result)
            if broken:
                return 2, f"cannot check: the validator could not run ({broken})\n{output}"
            if result.returncode == 1 and validate("--no-freshness").returncode == 0:
                return 0, (output + "\nwarning: the planning package is out of date (its plan content changed since "
                           "its cold review); it passes without that check, as in ship. Run the cold review again")
        except (OSError, subprocess.TimeoutExpired) as exc:
            return 2, f"cannot check: the validator did not finish ({exc})"
    if result.returncode not in (0, 1):
        return 2, f"{output}\ncannot check: the validator exited {result.returncode}"
    return result.returncode, output


def unit_problems(repo: Path) -> list[str]:
    """The work-unit DAG problems when the repository has a work-units file, else none."""
    units_file = repo / UNITS
    if not units_file.is_file():
        return []
    from lockstep.work_units import analyse
    try:
        return [f"work units: {p}" for p in analyse(_load(units_file))["problems"]]
    except Unreadable as exc:
        return [f"work units: {exc}"]


def plan_cli(argv: list[str]) -> int:
    """`lockstep plan <command>`: `check` (the validator plus work units) or `units` (the work-unit DAG)."""
    if argv and argv[0] == "units":
        from lockstep.work_units import units_cli
        return units_cli(argv[1:])
    if not argv or argv[0] != "check":
        print("usage: lockstep plan check [--repo PATH] [--json] | lockstep plan units [--repo PATH] [--json]",
              file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="lockstep plan check", description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", type=Path, default=Path("."), help="the repository (default: the current directory)")
    parser.add_argument("--json", action="store_true", help="print the result as one JSON object")
    args = parser.parse_args(argv[1:])
    repo: Path = args.repo.resolve()
    status, output = run_validator(repo)
    units = unit_problems(repo)
    final = status if status else (1 if units else 0)
    if args.json:
        print(json.dumps({"ok": final == 0, "validator": {"exit": status, "output": output}, "work_units": units},
                         indent=2))
    else:
        print(output)
        for p in units:
            print(f"  {p}")
        print(f"OUTCOME {'ok' if final == 0 else 'fail'}: validator exit {status}, {len(units)} work-unit problems")
    return final
