#!/usr/bin/env python3
"""Refuse an OpenSpec change that adds a requirement but has no decided prior-art record.

Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search so that we are only buidling what
we need to. that needs to be ienforced. the cost is weeks/months workign ont his and nto really making any
progress because nothing is anything mroe than text"

A change needs `prior-art.json` in its folder when it is `openspec/changes/<name>/` (under `archive/` only when
`--files` names it),
its `.openspec.yaml` `created` date is on or after `--since` (a missing or unreadable date falls back to the
date git first committed a file in the change folder; a change with neither counts as needing one), and a `specs/**/spec.md` in it has a line that is exactly `## ADDED Requirements`.
This script only decides which changes need a record; every rule about the record's content is in
`prior-art.schema.json` (beside this file) and is applied with the `jsonschema` package.

Usage: lockstep check prior-art, or prior_art.py [--repo DIR] [--since YYYY-MM-DD] [--files PATH ...]
Exit 0 when no change fails, 1 when any fails, 2 when it cannot run. Run it without the package installed:
uv run --no-project --with jsonschema python src/lockstep/prior_art.py

Ported from code2-workspace scripts/prior_art_check.py at ec500633 (2026-11-20) so the check is public and `ship`
can run it on any machine (docs/planning/minimal-core-2026-11-20.md, section 7). Standard library plus jsonschema
only, so it runs as a plain file.

Implements: prior-art-check/a-change-that-adds-a-requirement-carries-a-prior-art-record
Implements: prior-art-check/a-candidate-cannot-be-left-undecided-and-the-decision-must-follow-from-the-candidates
Implements: prior-art-check/only-a-change-that-adds-a-requirement-from-the-start-date-needs-a-record

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:prior_art.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: prior-art-check/a-change-that-adds-a-requirement-carries-a-prior-art-record, prior-art-check/a-candidate-cannot-be-left-undecided-and-the-decision-must-follow-from-the-candidates, prior-art-check/only-a-change-that-adds-a-requirement-from-the-start-date-needs-a-record

### Requirement: A change that adds a requirement carries a prior-art record

`src/lockstep/prior_art.py` (`lockstep check prior-art`) SHALL fail (exit 1) for each unarchived OpenSpec change that needs a record and
has no `prior-art.json`, naming the change and the path to create, and for a `prior-art.json` that is not
valid JSON or that breaks `src/lockstep/prior-art.schema.json`, printing each violation with its place in the file.
It SHALL exit 0 when every change that needs a record has a valid one.

Source: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search so that we are only
buidling what we need to. that needs to be ienforced". Ported from code2-workspace `ec500633` (2026-11-20, minimal core section 7) so the check is public.

#### Scenario: No record on a change that adds a requirement

- **GIVEN** an unarchived change dated 2026-11-18 with `## ADDED Requirements` and no `prior-art.json`
- **WHEN** the check runs
- **THEN** it exits 1 and names the path `prior-art.json` would have

#### Scenario: Complete record

- **GIVEN** the same change with a complete `prior-art.json`
- **WHEN** the check runs
- **THEN** it exits 0

#### Scenario: Invalid JSON

- **GIVEN** a `prior-art.json` that is not JSON
- **WHEN** the check runs
- **THEN** it exits 1

### Requirement: A candidate cannot be left undecided and the decision must follow from the candidates

`src/lockstep/prior-art.schema.json` SHALL state every rule about the record's content, and the check SHALL apply
it with the `jsonschema` package, not with rules written again in Python: each candidate's verdict is one of
adopt, combine, fork or reject; the search lists at least one place in our own work and one outside it; a
decision of adopt, combine or fork needs a candidate with that verdict; a decision of build needs a non-empty
gap and every candidate rejected.

Source: inferred by agent, from the incident above (a candidate list left "not yet evaluated" for 53 days);
the four verdict words and the field names are working defaults.

#### Scenario: Verdict not yet evaluated

- **GIVEN** a record with a candidate whose verdict is "not yet evaluated"
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Build without a gap

- **GIVEN** a record whose decision is `build` and which has no `gap`
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Build while a candidate is adopted

- **GIVEN** a record whose decision is `build` while a candidate's verdict is `adopt`
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Adopt without an adopted candidate

- **GIVEN** a record whose decision is `adopt` and no candidate has verdict `adopt`
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Search with nothing outside

- **GIVEN** a record whose searches are all in our own work
- **WHEN** the check runs
- **THEN** it exits 1

#### Scenario: Real record against the real schema

- **GIVEN** the real schema file and this change's own record
- **WHEN** the record is validated
- **THEN** it has no violations

### Requirement: Only a change that adds a requirement, from the start date, needs a record

The check SHALL require a record only for a change whose date is on or after `--since` (default 2026-11-18) and whose spec deltas hold a line exactly `## ADDED Requirements`. A change's date is its `.openspec.yaml` `created` date; when that is missing or unreadable, it is the date git first committed a file in the change folder; a change with neither counts as needing a record. Without `--files` it SHALL look only at unarchived changes. With `--files` it SHALL look only at the changes those paths belong to, archived (`openspec/changes/archive/<name>/`) or not. It SHALL print one summary line with counts and exit 2 when it cannot run.

Source: inferred by agent: the start date and the ADDED-header test are working defaults; the header marks what OpenSpec treats as new required behavior. Inferred by agent (code2-workspace issue 833, slice 1): archived changes named by `--files` are checked, because `ship` checks a merge after its change has been archived. Inferred by agent (issue 833 follow-up, 2026-11-18): five changes made before the rule had no `created` date and were refused, so git's first commit date stands in for it.

#### Scenario: Only modified requirements

- **GIVEN** a change whose only delta header is `## MODIFIED Requirements`
- **WHEN** the check runs
- **THEN** it exits 0 and counts no change as needing a record

#### Scenario: Change before the start date

- **GIVEN** a change created 2026-11-17 that adds a requirement and has no record
- **WHEN** the check runs
- **THEN** it exits 0 and counts no change as needing a record

#### Scenario: Undated change first committed before the start date

- **GIVEN** a change with no `created` date that adds a requirement, has no record, and was first committed on 2026-11-13
- **WHEN** the check runs
- **THEN** it exits 0 and counts no change as needing a record

#### Scenario: Undated change never committed

- **GIVEN** a change with no `created` date that adds a requirement, has no record, and has never been committed
- **WHEN** the check runs
- **THEN** it reports the missing record and exits 1

#### Scenario: Archived change

- **GIVEN** a change under `openspec/changes/archive/` that adds a requirement and has no record
- **WHEN** the check runs
- **THEN** it exits 0 and looks at no change

#### Scenario: Archived change named by files

- **GIVEN** a change under `openspec/changes/archive/` that adds a requirement and has no record
- **WHEN** the check runs with `--files` naming a file in that change
- **THEN** it reports the missing record and exits 1

#### Scenario: Files limit the check

- **GIVEN** two changes needing a record, only one with a record, and `--files` naming a file of the one with a record
- **WHEN** the check runs
- **THEN** it exits 0

Tested by: tests/lockstep/test_lockstep_prior_art.py
[[[end]]]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ENFORCED_FROM = "2026-11-18"
SCHEMA = Path(__file__).resolve().with_name("prior-art.schema.json")
RUN_HINT = "uv run --no-project --with jsonschema python " + str(Path(__file__).resolve())


def changes_in(repo: Path, files: list[str] | None) -> list[Path]:
    """Return the change folders to look at: every unarchived one, or those the given paths belong to, archived or not."""
    base = repo / "openspec" / "changes"
    if files is None:
        return sorted(d for d in base.iterdir() if d.is_dir() and d.name != "archive")
    found = set()
    for f in files:
        p = Path(f)
        try:
            parts = (p.resolve().relative_to(repo.resolve()) if p.is_absolute() else p).parts
        except ValueError:
            continue
        if len(parts) >= 4 and parts[:2] == ("openspec", "changes") and parts[2] != "archive":
            if (base / parts[2]).is_dir():
                found.add(base / parts[2])
        elif len(parts) >= 5 and parts[:3] == ("openspec", "changes", "archive"):
            # An archived change counts only when named: `ship` checks a merge after its change was archived.
            if (base / "archive" / parts[3]).is_dir():
                found.add(base / "archive" / parts[3])
    return sorted(found)


def first_commit_date(change: Path) -> str | None:
    """Return the date git first committed a file in the change folder, or None when it never did."""
    try:
        out = subprocess.run(["git", "-C", str(change), "log", "--diff-filter=A", "--format=%cs", "--", "."],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    dates = out.stdout.split() if out.returncode == 0 else []
    return min(dates) if dates else None


def created_date(change: Path) -> str | None:
    """Return the change's `created` date, else git's first commit date, or None when it has neither."""
    try:
        text = (change / ".openspec.yaml").read_text(encoding="utf-8")
    except OSError:
        text = ""
    m = re.search(r"^created:\s*['\"]?(\d{4}-\d{2}-\d{2})", text, re.M)
    return m.group(1) if m else first_commit_date(change)


def adds_requirement(change: Path) -> bool:
    """Return True when a spec delta in the change has a line exactly `## ADDED Requirements`."""
    for spec in (change / "specs").glob("**/spec.md"):
        try:
            if "## ADDED Requirements" in spec.read_text(encoding="utf-8").splitlines():
                return True
        except OSError:
            continue
    return False


def where(error) -> str:
    """Return the place of a schema violation in plain words."""
    return "the record" if not error.absolute_path else "the record, at " + " > ".join(str(p) for p in error.absolute_path)


def problems(change: Path, repo: Path, validator) -> list[str]:
    """Return what is wrong with the change's record, or an empty list when it passes."""
    record = change / "prior-art.json"
    shown = record.relative_to(repo) if record.is_relative_to(repo) else record
    if not record.is_file():
        return [f"{change.name}: no prior-art record; create {shown} (rules, with a description of each field: {SCHEMA})"]
    try:
        data = json.loads(record.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        return [f"{change.name}: {shown} is not valid JSON ({err})"]
    return [f"{change.name}: {shown}: {where(e)}: {e.message}" for e in sorted(validator.iter_errors(data), key=lambda e: list(map(str, e.absolute_path)))]


def main(argv: list[str] | None = None) -> int:
    """Check the changes that need a record and return the exit code."""
    ap = argparse.ArgumentParser(description="Refuse a change that adds a requirement but has no prior-art record.")
    ap.add_argument("--repo", default=".", help="repository root (default: the current folder)")
    ap.add_argument("--since", default=ENFORCED_FROM, help=f"first creation date that needs a record (default {ENFORCED_FROM})")
    ap.add_argument("--files", nargs="*", default=None, help="check only the changes these paths belong to")
    args = ap.parse_args(argv)
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print(f"prior-art: cannot run, the jsonschema package is missing. Run: {RUN_HINT}", file=sys.stderr)
        return 2
    try:
        validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
    except (OSError, ValueError) as err:
        print(f"prior-art: cannot read {SCHEMA} ({err}). Run: {RUN_HINT}", file=sys.stderr)
        return 2
    repo = Path(args.repo).resolve()
    if not (repo / "openspec" / "changes").is_dir():
        print("prior-art: 0 changes looked at, 0 need a record, 0 passes, 0 fails")
        return 0
    looked = needing = failing = 0
    for change in changes_in(repo, args.files):
        looked += 1
        created = created_date(change)
        if (created is not None and created < args.since) or not adds_requirement(change):
            continue
        needing += 1
        found = problems(change, repo, validator)
        failing += bool(found)
        for line in found:
            print(line)
    print(f"prior-art: {looked} changes looked at, {needing} need a record, {needing - failing} passes, {failing} fails")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
