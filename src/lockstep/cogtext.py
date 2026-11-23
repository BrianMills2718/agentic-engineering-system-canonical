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

Implements: (no requirement)
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
             f"Implements: {', '.join(ctx['implements'])}" if ctx["implements"] else "Implements: (no requirement)"]
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
