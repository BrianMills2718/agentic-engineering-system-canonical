"""Parts report: each AES part's mode from lockstep.yaml and, for ship's planning gates, the newest recorded result.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:parts.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-projection/status-lists-each-part-with-its-mode-and-last-gate-result

### Requirement: Status lists each part with its mode and last gate result

`lockstep status --parts` SHALL print one row per AES part: each commit check named in `lockstep-checks`' check list
with its mode (`block`, `warn` or `off`, defaults as the commit checks apply them), `planning.gate` and
`planning.one_page_plans` (default `warn`), `planning.validator` and `planning.skills` only when `lockstep.yaml` sets
them, `guard.mode` (`warn (default)` when unset), and `rules` and `feedback` as `not built`. Modes SHALL be read from
`lockstep.yaml` in the working tree, and the output SHALL say that ship reads the planning settings from the default
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
- **THEN** trace is `warn`, mutation is `off`, arch is `block`, `planning.gate` is `block`, `planning.one_page_plans` is `warn`, `guard.mode` is `warn (default)`, rules and feedback are `not built`, and no validator row is listed

#### Scenario: The newest planning-gate record for this repository is shown

- **GIVEN** ship's log folder holding records for this repository's planning gate on two days and a newer record for another repository
- **WHEN** `lockstep status --parts` runs
- **THEN** the planning gate row shows the outcome and head of this repository's newer record, and `planning.one_page_plans` says `no record`

#### Scenario: Unreadable settings exit 2

- **GIVEN** a `lockstep.yaml` whose check mode is not block, warn or off
- **WHEN** `lockstep status --parts` runs
- **THEN** it exits 2 naming the problem

Tested by: tests/lockstep/checks/test_lockstep_check_parts.py

Declares (typed signatures, from the plan):
  verdicts_dir() -> Path
  last_results(repo_name: str, folder: Path) -> dict[str, str]
  parts(repo: Path) -> list[Part]
  as_json(rows: list[Part]) -> str
  table(rows: list[Part]) -> str
[[[end]]]
"""

import json
import os
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

from lockstep.checks import config
from lockstep.checks.gate_records import ORIGIN_NAME

# Record `gate` names as ship writes them (ship.py, record_gate_verdict callers) -> the lockstep.yaml key.
GATES = {"planning gate": "planning.gate", "one-page plans": "planning.one_page_plans"}
NOT_BUILT = ("rules", "feedback")
NOTE = "planning.* modes are this working tree's; ship reads them from the default branch at origin."


@dataclass(frozen=True)
class Part:
    """One row: the part, its mode (or setting), and its last recorded result."""

    part: str
    mode: str
    last: str = "no record"


def verdicts_dir() -> Path:
    """ship's planning-verdicts folder: $SHIP_LOG_DIR, else ~/code2/.ship-logs where ~/code2 exists, else XDG state.

    The same rule as ship.default_log_dir, which lockstep.checks may not import (.importlinter).
    """
    if os.environ.get("SHIP_LOG_DIR"):
        return Path(os.environ["SHIP_LOG_DIR"]) / "planning-verdicts"
    workspace = Path.home() / "code2"
    if workspace.is_dir():
        return workspace / ".ship-logs" / "planning-verdicts"
    return Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state") / "ship" / "logs" / "planning-verdicts"


def _repo_name(repo: Path) -> str:
    """owner/name from origin, computed as record_gate_verdict computes it; the path when there is no origin."""
    done = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"], capture_output=True, text=True)
    found = ORIGIN_NAME.search(done.stdout.strip()) if done.returncode == 0 else None
    return "/".join(found.groups()) if found else str(repo)


def last_results(repo_name: str, folder: Path) -> dict[str, str]:
    """`<outcome> <time> <head[:8]>` of the newest record per planning key for this repository; bad lines skipped."""
    newest: dict[str, dict] = {}
    for path in sorted(folder.glob("*.jsonl")) if folder.is_dir() else []:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = GATES.get(str(rec.get("gate"))) if isinstance(rec, dict) else None
            if key and rec.get("repo") == repo_name and str(rec.get("time", "")) >= str(newest.get(key, {}).get("time", "")):
                newest[key] = rec
    return {k: f"{r.get('outcome')} {r.get('time')} {str(r.get('head') or '')[:8]}" for k, r in newest.items()}


def parts(repo: Path) -> list[Part]:
    """The rows for `lockstep status --parts`.

    Implements: lockstep-projection/status-lists-each-part-with-its-mode-and-last-gate-result

    Requirement text (generated):
        lockstep-projection/status-lists-each-part-with-its-mode-and-last-gate-result: `lockstep
            status --parts` SHALL print one row per AES part: each commit check named in
            `lockstep-checks`' check list with its mode (`block`, `warn` or `off`, defaults as the
            commit checks apply them), `planning.gate` and `planning.one_page_plans` (default
            `warn`), `planning.validator` and `planning.skills` only when `lockstep.yaml` sets them,
            `guard.mode` (`warn (default)` when unset), and `rules` and `feedback` as `not built`.
            Modes SHALL be read from `lockstep.yaml` in the working tree, and the output SHALL say
            that ship reads the planning settings from the default branch at origin. For
            `planning.gate` and `planning.one_page_plans` the last result SHALL be the outcome, time
            and short head of the newest record (by its `time`) among `planning-verdicts/*.jsonl` in
            ship's log folder (`$SHIP_LOG_DIR`, else `~/code2/.ship-logs` where `~/code2` exists,
            else the XDG state folder) whose `repo` is this repository's owner/name from origin,
            gate `planning gate` or `one-page plans`; every other row, and a gate with no matching
            record, SHALL say `no record`. A record line that is not JSON SHALL be skipped. `--json`
            SHALL print the rows as a JSON list. The command SHALL exit 0, and 2 when
            `lockstep.yaml` cannot be read or holds a value the commit checks reject.

    Raises:
        config.ConfigError: lockstep.yaml is not YAML or holds a value the commit checks reject.
    """
    try:
        cfg = config.load(repo)
        path = repo / config.SIDE_FILE
        data = (yaml.safe_load(path.read_text()) or {}) if path.is_file() else {}
    except yaml.YAMLError as exc:
        raise config.ConfigError(f"{config.SIDE_FILE} is not YAML ({exc})") from exc
    planning = data.get("planning") or {}
    guard = data.get("guard") or {}
    last = last_results(_repo_name(repo), verdicts_dir())
    rows = [Part(name, cfg.mode(name)) for name in config.CHECK_NAMES]
    rows += [Part(f"planning.{key}", cfg.planning[key], last.get(f"planning.{key}", "no record"))
             for key in config.PLANNING_KEYS]
    if "validator" in planning:
        rows.append(Part("planning.validator", str(planning["validator"])))
    if "skills" in planning:
        skills = planning["skills"]
        rows.append(Part("planning.skills", str(skills.get("mode", "off") if isinstance(skills, dict) else skills)))
    rows.append(Part("guard.mode", str(guard["mode"]) if isinstance(guard, dict) and "mode" in guard else "warn (default)"))
    rows += [Part(name, "not built") for name in NOT_BUILT]
    return rows


def as_json(rows: list[Part]) -> str:
    """The rows as a JSON list of {part, mode, last}."""
    return json.dumps([asdict(r) for r in rows], indent=1)


def table(rows: list[Part]) -> str:
    """The rows as a plain-text table with the default-branch note last."""
    width = max(len(r.part) for r in rows)
    mode_w = max(len(r.mode) for r in rows)
    lines = [f"{'part':{width}}  {'mode':{mode_w}}  last result"]
    lines += [f"{r.part:{width}}  {r.mode:{mode_w}}  {r.last}" for r in rows]
    return "\n".join([*lines, "", NOTE])
