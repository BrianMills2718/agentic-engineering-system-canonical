"""Copy the typed signatures the plan declares for a file into its docstring (behavior 3.2).

`aes context` hands each planned artifact with its `exports`: a name for a constant or class,
a full typed signature for a function. They are copied verbatim, one per line, after the plan
text and never wrapped, since a wrapped signature would no longer read as declared. The docstring
renderer (`lockstep.cogtext.render`, behavior 3.1) appends these lines, so `make project`, the
stale-copy check (`pcw check`, the hook) and the plan text the hook hands an agent all carry them.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:signature_text.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: (no requirement)
[[[end]]]
"""

from __future__ import annotations


def signature_lines(ctx: dict) -> list[str]:
    """The "Declares:" lines for the exports of the artifact an `aes context` is about; empty when it has none."""
    subject = ctx.get("subject") or {}
    exports = [str(e).strip() for e in subject.get("exports") or [] if str(e).strip()]
    if not exports:
        return []
    if any('"""' in e or "\\" in e for e in exports):
        raise ValueError(f"{subject.get('id')}: an export holds a triple quote or a backslash, "
                         "which cannot be copied into a docstring verbatim")
    return ["Declares (typed signatures, from the plan):", *(f"  {e}" for e in exports)]
