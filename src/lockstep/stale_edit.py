"""Stop an edit to a planned file while its docstring copy of the plan is stale (behavior 3.4).

Called by the edit hook (`lockstep.hook`), which only warns unless the file is fixed or PCW_MODE=block
(behavior 5.1). Set PCW_BLOCK_STALE=0 to allow a stale edit even then.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:stale_edit.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: (no requirement)
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
