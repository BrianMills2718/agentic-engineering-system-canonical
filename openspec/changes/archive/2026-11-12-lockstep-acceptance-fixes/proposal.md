# Three failures the Lockstep acceptance runs found (A2, A3)

## Why

Real acceptance runs (`docs/planning/runs/lockstep-acceptance/a2.json`, `a3.json`) failed three ways:
the edit guard's refusal names no file the plan allows (A2 expects it to); `lockstep check arch` compares the
`.importlinter` file with the diagram but never checks the code's imports, so a commit adding a forbidden import
is accepted (A3); and `lockstep check test-first` accepts silently when pytest cannot run in Lockstep's environment.

## What changes

- A refusal of a write to a file the plan does not name also lists the planned files (same folder first, at most 15, then "and N more").
- `lockstep check arch check` also runs `lint-imports` on the code and refuses with the broken contract and importing module; a missing import-linter is a non-zero failure.
- `lockstep check test-first` fails (exit 1, "pytest could not run") when no test report is produced.
- `import-linter` and `pytest` become runtime dependencies of Lockstep (`pyproject.toml`, `uv.lock`).
