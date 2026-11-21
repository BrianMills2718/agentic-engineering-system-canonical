---
description: Decision (moved from code2-template decision 0001) to use off-the-shelf tools (OpenSpec, LikeC4, Zensical, import-linter) for documentation and planning.
---

# Decision 0015: Off-the-shelf documentation and planning stack

- Status: accepted
- Date: 2026-10-15
- Decider: Brian ("we should use off the shelf stuff to accomplish the goals i was trying to handbuild
  previously", 2026-10-15)

Governs: copier.yml, template/

Moved here from code2-template decision 0001 on 2026-11-21 with the template (Brian: "yes" to moving code2-template into this repository). code2check became `src/lockstep/checks/`.

## Context and problem

The hand-built system (AES durable documents, `durable_docs_check.py`, `trace.yaml`, docstring wiki,
governed wiki) kept documents linked to code and tests, but its docstring automation was never built
and its enforcement ran through plan gates that were turned off on 2026-10-13.

## Decision

| Goal | Tool |
| --- | --- |
| Docs generated from docstrings | Zensical 0.0.70 with mkdocstrings-python |
| Requirements and scenarios | OpenSpec |
| Architecture | arc42 headings; C4 diagrams in LikeC4 |
| Diagram enforced on code | import-linter, contracts generated from the LikeC4 model |
| Decision records | MADR markdown |
| Docstring drift | pydoclint, interrogate, strict docs build |
| Agent navigation | AGENTS.md index plus `llms.txt` from mkdocs-llmstxt |
| Same layout in every repository | copier template (`copier update` carries later changes) |

Built in code2check (now Lockstep), because the 2026-10-15 landscape review found no tool that reads OpenSpec: code2check
(requirement to code, scenario to test, diagram to contracts, test-first).

## Options not chosen

- StrictDoc, Doorstop, sphinx-needs: each is a second requirements store beside OpenSpec.
- Structurizr: enforces C4 rules but needs a JVM or Docker; runner-up to LikeC4.
- Mermaid C4: no model to check against; fine for one-off pictures.
- cookiecutter: cannot update repositories made from an older template.
- erdantic (entity diagrams from Pydantic models): deferred; it needs Graphviz system libraries and
  no repository needs it yet.

## Wrong if

A repository made from the template still has a requirement, scenario or diagram arrow that its code
or tests contradict while every check passes, or a check takes long enough that agents skip it.
