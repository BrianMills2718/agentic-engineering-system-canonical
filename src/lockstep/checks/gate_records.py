"""One JSON line per run of ship's planning gates, beside ship's day log, for a later review of whether each helped.

Brian, 2026-11-25: "i agree witht he warn but we should be recoridn these so we can review them afterwards to see
whether they were helpful or not and how to make the paperwork actually valuable".

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:gate_records.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: ship/every-planning-gate-run-is-recorded

### Requirement: Every planning-gate run is recorded

Each time ship runs one of its two planning gates it SHALL append one JSON line to `planning-verdicts/<YYYY-MM-DD>.jsonl` beside the day's ship log, holding `time`, `repo` (owner/name from origin), `branch`, `head`, `gate`, `mode`, `outcome` (`pass`, `warn`, `refuse`, `unavailable` or `off`), `reason` (the refusal text, or null) and `log` (the day's ship log). A record that cannot be written SHALL NOT stop the merge; the day's log SHALL say so.

Source: Brian, 2026-11-25: "i agree witht he warn but we should be recoridn these so we can review them afterwards to see whether they were helpful or not and how to make the paperwork actually valuable". Recording passes and refusals as well as warnings, and the fields, were inferred by agent: a review needs the rate and the commit to follow up.

#### Scenario: A warned gate is recorded

- **GIVEN** a new repository with no planning package and no planning setting
- **WHEN** ship merges it with a warning
- **THEN** a `planning gate` record has outcome `warn`, the reason, the branch, the 40-character head and the log path

#### Scenario: Refused, passed and off gates are recorded

- **GIVEN** a new repository with no planning package and the gate set to block
- **WHEN** ship refuses it, and then merges it after the default branch sets the gate off
- **THEN** the records hold a `refuse` and an `off` for the planning gate and a `pass` for the one-page plans

Tested by: tests/test_ship.py

Declares (typed signatures, from the plan):
  record_gate_verdict(log: Path, repo: Path, gate: str, mode: str, outcome: str, reason: str | None, *, on_error: Callable[[str], None]) -> None
[[[end]]]
"""

import datetime
import json
import re
import subprocess
from collections.abc import Callable
from pathlib import Path

ORIGIN_NAME = re.compile(r"([^/:]+)[/:]([^/:]+?)(?:\.git)?/?$")


def record_gate_verdict(log: Path, repo: Path, gate: str, mode: str, outcome: str, reason: str | None, *,
                        on_error: Callable[[str], None]) -> None:
    """Append this gate run to <log's folder>/planning-verdicts/<date>.jsonl; a write that fails goes to on_error.

    Implements: ship/every-planning-gate-run-is-recorded

    Requirement text (generated):
        ship/every-planning-gate-run-is-recorded: Each time ship runs one of its two planning gates
            it SHALL append one JSON line to `planning-verdicts/<YYYY-MM-DD>.jsonl` beside the day's
            ship log, holding `time`, `repo` (owner/name from origin), `branch`, `head`, `gate`,
            `mode`, `outcome` (`pass`, `warn`, `refuse`, `unavailable` or `off`), `reason` (the
            refusal text, or null) and `log` (the day's ship log). A record that cannot be written
            SHALL NOT stop the merge; the day's log SHALL say so.
    """
    def git(*args: str) -> str:
        done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, errors="replace")
        return done.stdout.strip() if done.returncode == 0 else ""
    found = ORIGIN_NAME.search(git("remote", "get-url", "origin"))
    record = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
              "repo": "/".join(found.groups()) if found else str(repo), "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
              "head": git("rev-parse", "HEAD"), "gate": gate, "mode": mode, "outcome": outcome, "reason": reason,
              "log": str(log)}
    folder = log.parent / "planning-verdicts"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / f"{datetime.date.today().isoformat()}.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except OSError as exc:  # a record that cannot be written never stops a merge; ship's day log says so
        on_error(f"ship: warning: could not record the {gate} verdict ({exc})")
