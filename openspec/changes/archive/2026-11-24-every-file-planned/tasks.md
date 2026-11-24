## 1. Tests first

- [x] 1.1 Test: a record array keyed by `path` projects; a duplicate path exits 2 without writing
- [x] 1.2 Test: every tracked file has a layout row with a purpose, every top-level entry is governed, `generated/files.md` is current and linked from `wiki/index.md`

## 2. Build

- [x] 2.1 `key` option in `src/lockstep/doc_projection.py`
- [x] 2.2 Layout rows for every tracked file (catalog purposes, fresh purposes) and `governed:` widened
- [x] 2.3 Projection `projection-file-catalog` into `generated/files.md`; link from `wiki/index.md`

## 3. Retire the hand catalog

- [x] 3.1 Repoint references to `wiki/documents.md`; reachability and orphan checks pass without it
- [x] 3.2 Retirement record in `docs/retired/2026-11-24.md`; delete `wiki/documents.md`; lower the Markdown cap
- [x] 3.3 Reword the AGENTS.md principle's mechanism; close PR #861
