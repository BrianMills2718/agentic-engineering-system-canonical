## Why

Six `portable-template` requirements are built in `copier.yml` and `template/` but the trace check reads only
`Implements:` lines in Python docstrings, so they show as unimplemented and sit on
`docs/planning/trace-accepted.txt`. The next slice (the template ships the planned file layout) adds another
requirement built only in the template, which would add a finding and break the shrink-only trace gate. Source:
Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md`; open question Q50
(`docs/planning/open-questions.json`); plan `docs/planning/template-layout-2026-11-23.md`, step 0.

## What Changes

- `[tool.lockstep] comment_sources` in `pyproject.toml` lists files or folders whose comment lines count as
  implementers: an `Implements:` line after `#`, `{#`, `//` or `<!--`. A bare docstring line in a `.py.jinja`
  starter file is not read, so the template's own example requirements stay out of AES's trace.
- AES lists `copier.yml` and `template`; the six requirements get `Implements:` lines where they are built
  (Jinja comments in `.jinja` files, which copier strips, so copies carry none).

## Impact

`src/lockstep/checks/markers.py`, `tests/lockstep/checks/test_lockstep_check_trace.py`, `pyproject.toml`,
`copier.yml`, `template/`, `docs/planning/trace-accepted.txt` (six lines fewer). Repositories that set no
`comment_sources` are read as before.
