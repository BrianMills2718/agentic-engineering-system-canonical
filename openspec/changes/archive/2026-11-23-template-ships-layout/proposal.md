# The template ships the planned file layout

Plan size: full
Planning package: docs/planning/planning-package.json

## Why

A copy made from the template had no `lockstep.yaml`, so nothing named its planned files: the edit hook refused
nothing and `lockstep layout` had nothing to lay out. Slice 2 of back-on-design puts the layout plan back in the
template (plan `docs/planning/template-layout-2026-11-23.md`, steps 1, 2 and 5).

## What changes

- `template/lockstep.yaml.jinja`: `governed:` and `fixed:` cover `src/<package>/`; one row each for the three
  starter files, with typed exports.
- `copier.yml` excludes `lockstep.yaml` on `copier update`, so an older copy gets no plan that refuses its files.
- The starter source files ship cog blocks that the copy's `lockstep check project` fills from the rows; the
  hand-written `Implements:` line in `core.py` goes.
- Template `AGENTS.md` says how a plan adds rows and when to run `uv run lockstep layout`; template `make check`
  runs the whole-tree check against the merge base with `origin/main`, else the first commit.
