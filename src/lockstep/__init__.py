"""Lockstep (package `lockstep` in AES canonical since 2026-11-11; before that repository lockstep, package `pcw`): keep a plan, code docstrings and a wiki in step.

The plan copies in these docstrings were projected from the lockstep repository's own plan at 150d5a8; they move to
OpenSpec in this repository with slice 2 of `proposals/one-planning-tool/DESIGN.md`.

The plan (`.aes/target.yaml`) is where requirement text is written for a repository without OpenSpec specs;
with them, OpenSpec is (`lockstep.openspec_text`).
`cog` projects it into docstrings, MkDocs builds the wiki from the plan and
those docstrings, and an agent edit hook hands the same text to the agent and
blocks an edit while a docstring is out of date with the plan.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:__init__.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: (no requirement)
[[[end]]]
"""
