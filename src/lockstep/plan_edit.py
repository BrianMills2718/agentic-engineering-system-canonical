"""Name the plan items an edit by hand to the plan file changes, and every file and symbol linked to them (behavior 3.8).

The plan (`.aes/target.yaml`) is Lockstep's one normative document (Q19): it changes only through
`aes plan accept`, which writes the plan and its change-log entry together. An Edit, MultiEdit or Write
call on the plan itself skips that, so the edit hook asks this module what the call would change and
warns with the answer: each changed item and the files whose docstrings carry it, found by behavior
3.5's own rule (`lockstep.change_list`), so the agent is handed the linked functions at once. `pcw check`
refuses the committed hand edit as well (behavior 5.2).

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:plan_edit.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Names no requirement; the layout row says why.
[[[end]]]
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
