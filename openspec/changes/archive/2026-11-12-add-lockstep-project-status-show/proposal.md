# Lockstep gains `check project`, `status`, `show` and the pytest plugin (one-tool design, slice 6a)

## Why

The code2 template should install `lockstep` instead of `code2check` (BrianMills2718/code2-template#27). Slice 4 ported
trace, arch, test-first, sources and docmeta; the commands still missing are the projection of requirement text and
coverage, the status report, `show`, and the pytest plugin that registers the `req` marker
(`proposals/one-planning-tool/DESIGN.md`, slice 6; Brian, 2026-11-11: "i approve single tool desing re d4").

## What changes

- `lockstep check project [--check]` writes requirement text into docstrings, coverage into plans and `docs/status.md`;
  it prints `rewrote <path>` lines as code2check did, so the template's hook can pipe them into `git add`. It is a
  check with a mode (`checks: {project: block|warn|off}` in `lockstep.yaml`).
- `lockstep status [--json|--md]` and `lockstep show FILE` are top-level commands.
- `src/lockstep/checks/plugin.py` registers the `req` marker, declared as a `pytest11` entry point.
- Source and test folders come from `[tool.lockstep]` in `pyproject.toml`, else `[tool.code2check]` (already so since
  slice 4). A plan block written by code2check is replaced, not duplicated.

## Not in this change

The edit hook (`code2check.hook`, slice 5), the template's own edits, and retiring code2check.
