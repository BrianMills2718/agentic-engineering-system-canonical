"""Render plan text for a docstring. Called from cog blocks.

Usage inside a docstring: a cog block whose one line of code is
`import lockstep.cogtext as c; c.docstring("ART-FINDER")`, closed by cog's end
marker on the next line (`lockstep.scaffold.STUB` writes one). The markers are
spelled out only in `OPEN` and `END` below, so `cog` run over Lockstep's own
source finds only real blocks.

`cog -r -c` writes the block from the plan; `cog --check -c` fails when the
plan changed and the block was not regenerated, or when someone hand-edited it.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:cogtext.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/the-plan-is-openspec-plus-layout-rows

### Requirement: The plan is OpenSpec plus layout rows

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 2: "Lockstep reads requirements from OpenSpec ... and layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it").

In a repository whose `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL take the
planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it implements, its tests, optionally
its typed exports), the governed folders from `governed:`, and the requirement text from OpenSpec. A repository with
`.aes/target.yaml` SHALL be read as before.

#### Scenario: The layout is laid out with first docstrings

- **GIVEN** a layout row for `src/greeter/__init__.py` implementing `greeting/greet-by-name`, tested by `tests/test_greet.py`
- **WHEN** `lockstep layout` runs
- **THEN** the file is created with a docstring holding its `Implements:` line, the requirement and its scenarios word for word, the test names and its declared signature, and an existing file is left as it is

#### Scenario: An unplanned file is refused against the layout

- **GIVEN** `governed: [src/]` and no row for `src/greeter/extra.py`
- **WHEN** an agent writes that file under `PCW_MODE=block`
- **THEN** the edit hook refuses it and names `lockstep.yaml` as where the file must be planned

#### Scenario: A planned file's edit hands over its requirement

- **GIVEN** a laid-out planned file
- **WHEN** an agent edits it
- **THEN** the edit is allowed and the agent is handed the OpenSpec requirement text

#### Scenario: The whole-tree check reads the layout

- **GIVEN** a laid-out, committed layout repository
- **WHEN** `lockstep check` runs, and again after an unplanned file is added under `src/`
- **THEN** the first allows and the second blocks with that file as `unplanned`

#### Scenario: A layout row must name real requirements

- **GIVEN** a row whose `implements` names a requirement no spec defines, and a row with no purpose
- **WHEN** the layout is checked
- **THEN** both are reported, naming the row's path

#### Scenario: An AES plan is still read

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** Lockstep reads its plan
- **THEN** the planned files come from `.aes/target.yaml` exactly as before
[[[end]]]
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from lockstep.aes_bridge import context, find_root
from lockstep.parent_text import parent_lines
from lockstep.signature_text import signature_lines

WIDTH = 76
OPEN = "[[[" + "cog"     # cog's markers, split so cog run over this source does not read them as a block
CLOSE = "]]" + "]"
END = "[[[" + "end" + CLOSE


def _layout_render(ctx: dict) -> list[str]:
    """A layout row's copy: the requirements it implements word for word, then its tests and its signatures."""
    lines = [f"Plan (generated from {ctx['source']}; edit the spec or the layout row, not this text):", "",
             f"Implements: {', '.join(ctx['implements'])}" if ctx["implements"] else "Names no requirement; the layout row says why."]
    for _, text in ctx["requirements"]:
        if '"""' in text or "\\" in text:
            raise ValueError(f"{ctx['subject']['id']}: a requirement holds a triple quote or a backslash, "
                             "which cannot be copied into a docstring verbatim")
        lines += ["", *(line.rstrip() for line in text.splitlines())]
    if ctx["tests"]:
        lines += ["", f"Tested by: {', '.join(ctx['tests'])}"]
    sig = signature_lines(ctx)
    return lines + ([""] + sig if sig else [])


def render(ctx: dict) -> list[str]:
    if "requirements" in ctx:
        return _layout_render(ctx)
    lines = ["Plan (generated from .aes/target.yaml; edit the plan, not this text):", ""]
    lines += parent_lines(ctx, WIDTH)  # behavior 7.1: the parent requirement first, in full
    for ni in ctx.get("normative_items", []):
        lines += textwrap.wrap(f"{ni['id']}: {ni['statement']}", WIDTH, subsequent_indent="  ")
    for sc in ctx.get("success_criteria", []):
        lines += textwrap.wrap(f"{sc['id']}: {sc['statement']}", WIDTH, subsequent_indent="  ")
        lines += textwrap.wrap(f"Disproved if: {sc['disproof']}", WIDTH, initial_indent="  ", subsequent_indent="  ")
    for vs in ctx.get("verification_subjects", []):
        lines.append(f"Proven by: {vs['id']} ({vs['locator']})")
    lines += signature_lines(ctx)  # behavior 3.2: the declared exports, verbatim, last
    return lines


def docstring(subject: str, indent: int = 4) -> None:
    import cog  # provided by cogapp while it runs a block

    root = find_root(Path(cog.inFile).parent)
    if root is None:
        raise RuntimeError(f"{cog.inFile}: no .aes/project.yaml or lockstep.yaml layout above this file")
    pad = " " * indent
    for line in render(context(root, subject)):
        cog.outl((pad + line).rstrip())
