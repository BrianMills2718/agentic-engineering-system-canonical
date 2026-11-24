"""Stop an edit to a planned file while its docstring copy of the plan is stale (behavior 3.4).

Called by the edit hook (`lockstep.hook`), which only warns unless the file is fixed or PCW_MODE=block
(behavior 5.1). Set PCW_BLOCK_STALE=0 to allow a stale edit even then.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:stale_edit.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/a-planned-file-without-a-cog-plan-copy-is-judged-by-its-implements-block

### Requirement: A planned file without a cog plan copy is judged by its Implements block

In a layout repository, the edit hook SHALL treat a planned file that holds no cog plan copy as current when `lockstep check project` would not change it, and as stale when that command would rewrite its generated `Implements:` requirement text. A stale file's refusal SHALL name `uv run lockstep check project`, and running that command SHALL clear it. A file with a cog plan copy, and a repository with `.aes/target.yaml`, SHALL be judged as before.

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), where every edit to a planned file that predated its layout row was refused; the rule itself inferred by agent from `proposals/one-planning-tool/DESIGN.md` ("one projector ... fed from OpenSpec").

#### Scenario: An existing file with a current Implements block can be edited

- **GIVEN** a file written before its layout row, whose `Implements:` block `lockstep check project` has written
- **WHEN** an agent edits it under `PCW_MODE=block`
- **THEN** the edit is allowed and the agent is handed the requirement text

#### Scenario: A stale Implements block names the command that fixes it

- **GIVEN** that file and an active change that rewords its requirement
- **WHEN** an agent edits it under `PCW_MODE=block`, runs `lockstep check project`, and edits it again
- **THEN** the first edit is refused naming `lockstep check project` and not `make project`, and the second is allowed with the new text
[[[end]]]
"""

from __future__ import annotations

import os
from pathlib import Path

from lockstep.check import docstring_mismatch


def projection_stale(root: Path, relpath: str) -> str | None:
    """Why a file's projection is missing or differs from its plan; executes no checked-tree code."""
    if not (root / relpath).is_file():
        return None
    return docstring_mismatch(root, relpath)


def stops_edits() -> bool:
    """True unless PCW_BLOCK_STALE=0 turns the stop into a warning."""
    return os.environ.get("PCW_BLOCK_STALE", "1") != "0"


def stale_reason(rel: str, cog_said: str, packet: str) -> str:
    """The message the agent receives when its edit is stopped: what to run, then the plan text."""
    return (f"The docstring in {rel} is out of date with the plan. Run `make project` "
            f"(cog -r -c) to regenerate it, then retry. If the plan text there was edited on purpose, "
            f"`make project` first turns the edit into a draft plan change under plans/ "
            f"(`python -m lockstep.docstring_up`), so the edit is not lost: accept it yourself with `aes plan accept` "
            f"when you are confident in it or it is not significant, and otherwise leave it as a draft and ask "
            f"a person.\n\ncog said: {cog_said}\n\n{packet}")
