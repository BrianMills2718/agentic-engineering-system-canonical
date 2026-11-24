# Every tracked file is planned

## Why

AES's rule says every tracked file is reachable and summarized from `wiki/index.md` (Brian, 2026-11-13, AES #849).
Today a hand catalog, `wiki/documents.md` (1183 lines), carries that, and nothing checks it is complete or current.
The settled design puts "which files exist and why" in `lockstep.yaml` `layout:` rows
(`proposals/one-planning-tool/DESIGN.md`, line 41). Only the 57 files under `src/lockstep/` have rows.

## What changes

- Every tracked file gets a `layout:` row with a one-line purpose. 336 purposes come from the hand catalog and 222 were
  written from each file's content. `governed:` lists every top-level folder and file, so a new unplanned file is
  reported by `lockstep check` and the edit hook.
- Record-array projections gain an optional `key` (default `id`) and `link` (render a path field as a link), so the
  `layout` rows (keyed by `path`) render into `generated/files.md` with every path a link, and every tracked file is
  reachable from `wiki/index.md` through it.
- `wiki/documents.md` retires, with a record in `docs/retired/2026-11-24.md`. Parked PR #861 closes.

## Impact

`lockstep.yaml`, `src/lockstep/doc_projection.py`, `generated/files.md`, `wiki/index.md`, references to
`wiki/documents.md`, `.md-file-cap.yaml`.
