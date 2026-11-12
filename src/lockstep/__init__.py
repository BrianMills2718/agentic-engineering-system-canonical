"""Lockstep (package `lockstep` in AES canonical since 2026-11-11; before that repository lockstep, package `pcw`): keep a plan, code docstrings and a wiki in step.

The plan copies in these docstrings were projected from the lockstep repository's own plan at 150d5a8; they move to
OpenSpec in this repository with slice 2 of `proposals/one-planning-tool/DESIGN.md`.

The plan (`.aes/target.yaml`) is where requirement text is written for a repository without OpenSpec specs;
with them, OpenSpec is (`lockstep.openspec_text`).
`cog` projects it into docstrings, MkDocs builds the wiki from the plan and
those docstrings, and an agent edit hook hands the same text to the agent and
blocks an edit while a docstring is out of date with the plan.

[[[cog import lockstep.cogtext as c; c.docstring("ART-INIT", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-1: The plan declares the normative side and the whole file
  structure: the plan, written as structured YAML in the AES plan format,
  declares the normative side (requirements, success criteria and decisions)
  and declares every file and every strongly typed function and class; no
  code file, test or document exists without a declared reason.
Part of REQ-2: Each success criterion names how it is checked: every success
  criterion in the plan names how it is checked: a test file by name,
  Brian's sign-off, or an AI-graded rubric.
Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
Part of REQ-4: A hook copies status from the code up into the normative
  documents: a hook copies status from the code up into the normative
  documents automatically: what exists, test results, and drift. It also
  keeps an automatic append-only change log of every normative change,
  including those made in a docstring, so the history is there.
Part of REQ-5: Links are checked both ways on every change: links between
  requirement, criterion, test, file and symbol are checked in both
  directions on every change, at edit time (the hook) and before commit
  (`pcw check`); an unplanned or stale item is refused.
Part of REQ-6: The wiki gets an agent to the right document or code within
  two links: from the wiki's front page, an agent reaches the normative
  document or the code that answers its question within two links, and each
  link comes with a summary of what it leads to.
Part of REQ-7: The bet: full linkage and projection are achievable, so code
  may be laid out by behavior: full linkage and projection (REQ-1 to REQ-6)
  work on a real repository, and in support of that the plan supports code
  laid out by behavior rather than by human-readability convention.
[[[end]]] (sum: F8euHwOB3Y)
"""
