"""Stop an edit to a planned file while its docstring copy of the plan is stale (behavior 3.4).

Called by the edit hook (`lockstep.hook`), which only warns unless the file is fixed or PCW_MODE=block
(behavior 5.1). Set PCW_BLOCK_STALE=0 to allow a stale edit even then.

[[[cog import lockstep.cogtext as c; c.docstring("ART-STALE-EDIT", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
BEH-3.4: An agent's edit to a planned file while the file's docstring copy
  of the plan is out of date tells the agent to run `make project`; by
  default the edit goes through with that warning and is logged as a would-
  block, and it is stopped for a file the side file marks fixed or with
  PCW_MODE=block; PCW_BLOCK_STALE=0 turns the stop into a plain allow.
SC-3.4: With PCW_MODE=block the hook denies an edit to a planned file whose
  docstring differs from the plan, and allows the same edit once the copy is
  regenerated; by default it allows the stale edit with the warning.
  Disproved if: Under PCW_MODE=block (PCW_BLOCK_STALE unset) an edit goes
  through while the copy is stale, or is stopped after regeneration; or by
  default a stale edit is stopped or goes through without the warning.
Proven by: VS-3.4-a (tests/test_stale_edit.py)
Declares (typed signatures, from the plan):
  projection_stale(root: Path, relpath: str) -> str | None
  stops_edits() -> bool
  stale_reason(rel: str, cog_said: str, packet: str) -> str
[[[end]]] (sum: 0b29C6pjDc)
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
