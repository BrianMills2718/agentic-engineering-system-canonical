"""Put each parent requirement, word for word, before a behavior's own text in its docstring.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:parent_text.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Names no requirement; the layout row says why.
[[[end]]]
"""

from __future__ import annotations

import textwrap


def parent_lines(ctx: dict, width: int) -> list[str]:
    """The "Part of REQ-n: ..." lines for every requirement (AES outcome) in an `aes context`.

    They come first and in full because agents read what is in the file and do not follow
    references (wiki/behavior-layout.md).
    """
    lines: list[str] = []
    for out in ctx.get("outcomes", []):
        lines += textwrap.wrap(f"Part of {out['id']}: {out['statement']}", width, subsequent_indent="  ")
    return lines
