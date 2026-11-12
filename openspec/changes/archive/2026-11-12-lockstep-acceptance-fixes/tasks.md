## 1. Tests first

- [x] 1.1 Refusal lists allowed files (edit and shell, capped, same folder first)
- [x] 1.2 Arch check refuses a forbidden import, accepts a clean tree, fails loudly without import-linter
- [x] 1.3 Test-first fails loudly when pytest cannot run

## 2. Fix

- [x] 2.1 `unplanned_files.allowed_listing` and `hook._with_allowed`
- [x] 2.2 `checks.arch.lint_imports` and its use in `lockstep check arch check`
- [x] 2.3 `checks.test_first.PytestUnavailable`
- [x] 2.4 Dependencies in `pyproject.toml` and `uv.lock`

## 3. Close

- [x] 3.1 `openspec validate`, archive
