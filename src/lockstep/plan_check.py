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

Implements: lockstep-plan-check/lockstep-plan-check-runs-company-planning-s-validator

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

Tested by: tests/lockstep/test_lockstep_plan_check.py

Declares (typed signatures, from the plan):
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


def fetch_planning_validator(run: Run) -> tuple[str | None, str | None]:
    """Return (path of Company Planning's validate_planning_package.py, None), or (None, why it cannot be had).

    $SHIP_PLANNING_VALIDATOR is taken as given; otherwise the validator's folder is extracted from origin/main of
    $SHIP_COMPANY_PLANNING (default ~/code2/company-planning) into the log folder. `ship` and `lockstep plan check` both
    call this, so a plan is checked by one validator.
    """
    from lockstep.ship import GOAL_PROVENANCE, VALIDATOR

    validator = os.environ.get("SHIP_PLANNING_VALIDATOR")
    if not validator:
        source = Path(os.environ.get("SHIP_COMPANY_PLANNING", Path.home() / "code2" / "company-planning"))
        if run.step("fetch company-planning", ["git", "-C", str(source), "fetch", "-q", "origin"]).returncode:
            return None, f"could not fetch {source}, so the planning package cannot be validated"
        # the validator imports its sibling modules (coverage_check.py), so extract the whole scripts folder;
        # it finds goal_provenance.py three folders up, so every path keeps its place in company-planning
        scripts_dir = str(Path(VALIDATOR).parent)
        present = [p for p in GOAL_PROVENANCE
                   if subprocess.run(["git", "-C", str(source), "cat-file", "-e", f"origin/main:{p}"],
                                     capture_output=True).returncode == 0]
        archive = Path(run.log.parent) / "planning-validator.tar"
        target = Path(run.log.parent) / "planning-validator"
        target.mkdir(parents=True, exist_ok=True)
        made = run.step("archive the validator folder from company-planning origin/main",
                        ["git", "-C", str(source), "archive", "-o", str(archive), "origin/main", scripts_dir, *present])
        if made.returncode:
            return None, f"could not archive {scripts_dir} from {source} origin/main"
        unpacked = run.step("unpack the validator folder", ["tar", "-x", "-f", str(archive), "-C", str(target)])
        if unpacked.returncode:
            return None, f"could not unpack {scripts_dir} into {target}"
        validator = str(target / VALIDATOR)
    if not Path(validator).is_file():
        return None, f"the planning validator {validator} does not exist"
    return validator, None


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
            validator, refused = fetch_planning_validator(run)
            python = validator_python(run) if validator else None
        if validator is None:
            return 2, f"cannot check: {refused}"
        if python is None:
            return 2, ("cannot check: no interpreter has the validator's packages; set SHIP_VALIDATOR_PYTHON to one "
                       "that imports jsonschema and pydantic")

        def validate(*extra: str) -> subprocess.CompletedProcess:
            """Run the validator once."""
            return subprocess.run([*python, validator, "--repo", str(repo), str(package), *extra],
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
