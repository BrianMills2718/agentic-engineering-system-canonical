"""Name the plan items an edit by hand to the plan file changes, and every file and symbol linked to them (behavior 3.8).

The plan (`.aes/target.yaml`) is Lockstep's one normative document (Q19): it changes only through
`aes plan accept`, which writes the plan and its change-log entry together. An Edit, MultiEdit or Write
call on the plan itself skips that, so the edit hook asks this module what the call would change and
warns with the answer: each changed item and the files whose docstrings carry it, found by behavior
3.5's own rule (`lockstep.change_list`), so the agent is handed the linked functions at once. `pcw check`
refuses the committed hand edit as well (behavior 5.2).

[[[cog import lockstep.cogtext as c; c.docstring("ART-PLAN-EDIT", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
BEH-3.8: An edit that changes the plan file itself (.aes/target.yaml) other
  than through `aes plan accept` is warned about at edit time (refused with
  PCW_MODE=block), naming each changed plan item and every file and symbol
  whose docstring carries it, so the agent is told to make the change
  through a plan and is handed the list of linked functions.
SC-3.8: An Edit, MultiEdit or Write call that changes a plan item's text in
  .aes/target.yaml is answered by the edit hook with a warning (a refusal
  under PCW_MODE=block) that names each changed item and lists every file
  whose docstring carries it, with that file's declared symbols; a call that
  leaves the plan's items unchanged gets no such warning.
  Disproved if: A hand edit that changes a plan item gets no warning from
  the edit hook, or its warning misses a changed item or a file that carries
  it; or an edit that changes no plan item is warned about.
Proven by: VS-3.8-a (tests/test_plan_edit.py)
Declares (typed signatures, from the plan):
  plan_edit_reason(root: Path, rel: str, after: str) -> str | None
[[[end]]] (sum: bioOn1M0+K)
"""

from __future__ import annotations

from pathlib import Path

import yaml

from lockstep.change_list import TARGET, changed_items, linked_files


def plan_edit_reason(root: Path, rel: str, after: str) -> str | None:
    """Why an edit leaving the plan file `rel` as `after` is a hand edit, with the linked list; None if it changes no item."""
    if rel != TARGET:
        return None
    try:
        old = yaml.safe_load((root / rel).read_text(encoding="utf-8")) or {}
        new = yaml.safe_load(after) or {}
    except (OSError, yaml.YAMLError) as exc:
        return (f"This edits the plan ({TARGET}) by hand, and the result cannot be read as the plan: "
                f"{str(exc).splitlines()[0]}. Change the plan through `aes plan prepare/validate/accept`.")
    if not isinstance(old, dict) or not isinstance(new, dict):
        return None
    changed = changed_items(old, new)
    if not changed:
        return None
    files = linked_files(old, new, changed)
    lines = [f"This edits the plan ({TARGET}) by hand, which changes {', '.join(changed)}. The plan changes only through "
             "`aes plan prepare/validate/accept`, which also writes its change-log entry; `pcw check` refuses a hand "
             "edit before commit. Draft the change as a plan under plans/ instead.",
             f"These {len(files)} file(s) carry that text and will need `make project` and a check of their code "
             "once the change is accepted:"]
    for f in files:
        symbols = f"; symbols: {', '.join(f['symbols'])}" if f["symbols"] else ""
        lines.append(f"- {f['path']} ({f['artifact']}): {', '.join(f['items'])}{symbols}")
    return "\n".join(lines)
