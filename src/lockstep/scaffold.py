"""`python -m lockstep.scaffold`: create every file the plan declares that does not exist yet.

Each new source or test file gets a module docstring holding a cog block for
its planned artifact, so `make project` can write the plan's words into it.
Existing files are never touched. Prints what it created.

[[[cog import lockstep.cogtext as c; c.docstring("ART-SCAFFOLD", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
BEH-3.3: Every declared Python source or test file that does not exist yet
  is created with a docstring holding the cog block for its plan text; an
  existing file is never touched.
SC-3.3: `python -m lockstep.scaffold` creates each missing declared .py file with
  its cog block and leaves existing files unchanged.
  Disproved if: A missing declared file is not created, is created without
  its cog block, or an existing file changes.
Proven by: VS-3.3-a (tests/test_scaffold.py)
Declares (typed signatures, from the plan):
  STUB
  main() -> int
[[[end]]] (sum: ykKlQwg6+R)
"""

from __future__ import annotations

import sys
from pathlib import Path

from lockstep.aes_bridge import find_root, target
from lockstep.cogtext import CLOSE, END, OPEN

STUB = '''"""{purpose}

{open} import lockstep.cogtext as c; c.docstring("{art}", indent=0){close}
{end}
"""
'''


def main() -> int:
    root = find_root(Path.cwd())
    if root is None:
        print("scaffold: no .aes/project.yaml or lockstep.yaml layout here or above", file=sys.stderr)
        return 1
    made = []
    for art in target(root).get("planned_artifacts") or []:
        rel = (art.get("locator") or {}).get("exact_path")
        if not rel or not rel.endswith(".py"):
            continue
        path = root / rel
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB.format(purpose=art.get("purpose", "").capitalize() + ".", art=art["id"], open=OPEN, close=CLOSE, end=END))
        made.append(f"{rel}  ({art['id']})")
    print("scaffold: created\n  " + "\n  ".join(made) if made else "scaffold: every planned file already exists")
    return 0


def layout() -> int:
    """`lockstep layout`: create every planned file that does not exist yet, then fill its docstring from the plan.

    The files are created as `main` creates them, then cog writes each new file's plan text (its requirements, success
    criteria, tests and signatures) into the block; an existing file is never touched.
    """
    from cogapp import Cog

    root = find_root(Path.cwd())
    if root is None:
        return main()  # it says why there is nothing to lay out
    missing = sorted(p for p in _planned_py(root) if not (root / p).exists())
    code = main()
    if code or not missing:
        return code
    return Cog().main(["cog", "-r", "-c", *(str(root / p) for p in missing)])


def _planned_py(root: Path) -> list[str]:
    return [rel for art in target(root).get("planned_artifacts") or []
            if (rel := (art.get("locator") or {}).get("exact_path")) and rel.endswith(".py")]


if __name__ == "__main__":
    raise SystemExit(main())
