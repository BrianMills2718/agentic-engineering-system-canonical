"""Copy the typed signatures the plan declares for a file into its docstring (behavior 3.2).

`aes context` hands each planned artifact with its `exports`: a name for a constant or class,
a full typed signature for a function. They are copied verbatim, one per line, after the plan
text and never wrapped, since a wrapped signature would no longer read as declared. The docstring
renderer (`lockstep.cogtext.render`, behavior 3.1) appends these lines, so `make project`, the
stale-copy check (`pcw check`, the hook) and the plan text the hook hands an agent all carry them.

[[[cog import lockstep.cogtext as c; c.docstring("ART-SIGNATURE-TEXT", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
BEH-3.2: The typed signatures the plan declares for a file are copied into
  its docstring.
SC-3.2: After `make project`, every export the plan declares for a file
  appears in its docstring as declared.
  Disproved if: A declared signature is missing from the docstring or
  differs from the plan's.
Proven by: VS-3.2-a (tests/test_signature_text.py)
Declares (typed signatures, from the plan):
  signature_lines(ctx: dict) -> list[str]
[[[end]]] (sum: IsRz0dYcl4)
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
