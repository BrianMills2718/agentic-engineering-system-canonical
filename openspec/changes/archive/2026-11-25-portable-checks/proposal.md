# Maintainability, helper-reuse and mutation become Lockstep checks

Plan size: full
Planning package: docs/planning/planning-package.json

Full, not small: the checks ship in the Lockstep package, `lockstep init` and the template, which other repositories use.

## Why

Three checks were built for AES alone: the maintainability ratchet and the helper-reuse check as AES scripts, and
mutation testing as a code2-workspace script hard-wired to AES. Brian approved making them portable Lockstep features
that each repository switches on in its own `lockstep.yaml` (Brian, 2026-11-25: "ia prpove yourr ecommednations").
They stay off unless switched on because each has a cost a repository should choose: maintainability needs `uvx ruff`,
helper-reuse a paid model call, mutation a long nightly run.

## What changes

- `lockstep check maintainability`, `lockstep check helper-reuse` and `lockstep check mutation`: the two AES scripts
  move into `src/lockstep/checks/` (helper-reuse's prompts become package data); the workspace script is ported with
  its issue code. The three default to `off`; `block` and `warn` switch them on. A bare YAML `on` reads as `block`.
- `mutation: {issue_repo, name}` in `lockstep.yaml`: where `--issue` keeps its issue (default origin) and the name in
  the title and summary. Its kept state moves from `~/projects/data/mutation/` to `<git-common-dir>/lockstep-mutation/`.
- `lockstep init` writes the three as `off` with a comment each and leaves them out of the lefthook command; the
  template's `make check` calls `lockstep check maintainability` (skipped until switched on).
- AES switches on maintainability and mutation (issue in code2-workspace, titled for AES as before).

## Impact

`src/lockstep/checks/{config,cli,maintainability,helper_reuse,mutation}.py`, `src/lockstep/checks/prompts/`,
`src/lockstep/init_repo.py`, `template/Makefile`, `Makefile`, `pyproject.toml`, `lockstep.yaml`,
`openspec/specs/lockstep-checks/spec.md`, `openspec/specs/lockstep-init/spec.md`. code2-workspace follows in its own
change: gates-nightly calls `lockstep check mutation --issue` and its `mutation_report.py` is removed.
