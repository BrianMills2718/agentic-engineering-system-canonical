"""Report the public functions and classes, and the declared signatures, that a change to a planned file adds against the plan (behavior 5.5).

The edit hook (`lockstep.hook`) and the before-commit check (`lockstep.check`) both ask this module one
question about one planned Python source file: given its text before and after the change, which
problems does the change add? A problem is a public top-level function or class (its name does not
start with `_`) that the file's `exports` in the plan do not name, or a declared function whose
signature in the code differs from the declared one. The text is parsed the way AES reads it
(`characterize_python.analyze`), never imported or run, so a hostile file cannot act here.

Only added problems count: one already in the text before the change is behavior 1.2's and 5.3's
report (`make check`), so an agent is never refused for drift it did not cause.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:symbol_gate.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/every-refusal-in-a-layout-repository-names-a-layout-command

### Requirement: Every refusal in a layout repository names a layout command

In a layout repository, the whole-tree commit check SHALL judge a planned file's docstring exactly as the edit hook does, and its stale reason SHALL name `uv run lockstep check project`. A refusal for an undeclared, removed or retyped public symbol SHALL name the file's layout row `exports:` in lockstep.yaml as where to declare it. Every edit-hook refusal SHALL end by pointing to the layout rows in `lockstep.yaml` and to `uv run lockstep show <file>`, and SHALL NOT point to `python -m lockstep.wiki`. A repository with `.aes/target.yaml` SHALL keep its current wording.

Source: Brian, 2026-11-20, "yes" to proving Lockstep on a from-scratch repository (`docs/planning/next.goal.md`, step 3), whose rerun was blocked at commit by a check naming `.aes/target.yaml`; the rule itself inferred by agent. The refusal pointer added 2026-11-23 after `python -m lockstep.wiki` was found to crash in a layout repository (inferred by agent, while carrying out Q54).

#### Scenario: The commit check judges an Implements block the same way

- **GIVEN** a committed file whose `Implements:` block is current, edited in the working tree
- **WHEN** `lockstep check` runs, then again after an active change rewords its requirement, then after `lockstep check project`
- **THEN** it allows, then blocks the file as stale naming `lockstep check project` and not `.aes/target.yaml`, then allows

#### Scenario: An undeclared public symbol names the layout exports

- **GIVEN** a planned layout file
- **WHEN** an agent's edit adds a public function its layout row does not export, under `PCW_MODE=block`
- **THEN** the edit is refused naming the row's `exports:` in lockstep.yaml and not `aes plan`

#### Scenario: A refusal points to lockstep show, not the wiki

- **GIVEN** a layout repository with no `.aes/` folder
- **WHEN** the edit hook refuses a write to an unplanned file
- **THEN** the refusal names `uv run lockstep show` and does not name `python -m lockstep.wiki`
[[[end]]]
"""

from __future__ import annotations

from pathlib import Path

from agentic_engineering_system.characterize_python import analyze, parse_export

from lockstep.aes_bridge import target
from lockstep.layout_plan import has_layout


def _problems(path: str, art: str, exports: list[str], text: str,
              route: str = "`aes plan prepare/validate/accept`") -> dict[str, str]:
    """Problem key -> plain-words problem, for one file's text against its declared exports."""
    declared: dict[str, str | None] = {}
    for entry in exports:
        try:
            name, signature = parse_export(entry)
        except ValueError:
            continue  # a malformed export is behavior 1.2's report, not a change's
        declared[name] = signature
    try:
        symbols = analyze(path, text, {}).symbols
    except SyntaxError:
        return {}  # a file that does not parse is not judged here
    out: dict[str, str] = {}
    present = {sym.name for sym in symbols}
    for name in declared:
        if name not in present:
            # Q38: the plan names it and the text lacks it; counted only when the text before had it.
            out[f"missing:{name}"] = (
                f"{path} would no longer define {name}, which the plan declares in {art}'s exports. "
                f"Keep it, or remove it from the plan through {route} first.")
    for sym in symbols:
        if sym.kind not in ("function", "class"):
            continue
        shown = f"{sym.name}{sym.signature}" if sym.signature else sym.name
        if sym.name not in declared:
            out[f"undeclared:{sym.name}"] = (
                f"{path} would define the {sym.kind} {shown}, which the plan does not declare in {art}'s exports. "
                f"Add it with its types through {route} first, or make it private "
                "(a name starting with _).")
        elif sym.kind == "function" and declared[sym.name] is not None and sym.signature != declared[sym.name]:
            out[f"signature:{sym.name}:{sym.signature}"] = (
                f"{path} would give {sym.name} the signature {sym.signature}, but the plan ({art}) declares "
                f"{sym.name}{declared[sym.name]}. Change the declared types through {route} "
                "first, or keep the declared signature.")
    return out


def added_symbol_problems(root: Path, rel: str, after: str, before: str | None) -> list[str]:
    """The problems `after` has that `before` (None: a new file) does not, for a planned Python source file; [] otherwise."""
    if not rel.endswith(".py"):
        return []
    for art in target(root).get("planned_artifacts") or []:
        if art.get("kind") == "source" and (art.get("locator") or {}).get("exact_path") == rel:
            exports = [str(e) for e in art.get("exports") or []]
            route = ("its layout row's `exports:` in lockstep.yaml" if has_layout(root)
                     else "`aes plan prepare/validate/accept`")
            now = _problems(rel, art.get("id") or rel, exports, after, route)
            was = _problems(rel, art.get("id") or rel, exports, before, route) if before is not None else {}
            # A new file is judged whole for what it adds; an export it does not define yet is unwritten, not removed.
            return [text for key, text in now.items() if key not in was and (before is not None or not key.startswith("missing:"))]
    return []


def text_after(call: dict, path: Path) -> str | None:
    """The file's text once an Edit, MultiEdit or Write call (or OpenHands' create or str_replace) is applied; None when unknown."""
    tin = call.get("tool_input") or {}
    name = call.get("tool_name")
    if name == "Write" and isinstance(tin.get("content"), str):
        return tin["content"]
    if name in ("file_editor", "str_replace_editor"):  # OpenHands' editor (the Project Brain runner's agent)
        if tin.get("command") == "create" and isinstance(tin.get("file_text"), str):
            return tin["file_text"]
        if tin.get("command") == "str_replace":
            name, tin = "Edit", {"old_string": tin.get("old_str"), "new_string": tin.get("new_str") or ""}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    edits = tin.get("edits") if name == "MultiEdit" else [tin] if name == "Edit" else None
    if not isinstance(edits, list):
        return None
    for e in edits:
        old, new = e.get("old_string"), e.get("new_string")
        if not isinstance(old, str) or not isinstance(new, str) or old not in text:
            return None
        text = text.replace(old, new) if e.get("replace_all") else text.replace(old, new, 1)
    return text
