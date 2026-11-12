"""Put each parent requirement, word for word, before a behavior's own text in its docstring.

[[[cog import lockstep.cogtext as c; c.docstring("ART-PARENT-TEXT", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-7: The bet: full linkage and projection are achievable, so code
  may be laid out by behavior: full linkage and projection (REQ-1 to REQ-6)
  work on a real repository, and in support of that the plan supports code
  laid out by behavior rather than by human-readability convention.
BEH-7.1: A behavior's docstring carries its parent requirement in full,
  before the behavior's own text.
SC-7.1: The docstring of a planned file starts its plan text with each
  parent requirement word for word, before the behavior.
  Disproved if: A docstring omits its parent requirement, shortens it, or
  puts it after the behavior.
Proven by: VS-7.1-a (tests/test_parent_text.py)
Declares (typed signatures, from the plan):
  parent_lines(ctx: dict, width: int) -> list[str]
[[[end]]] (sum: 8ULSuBkjpj)
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
