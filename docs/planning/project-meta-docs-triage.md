---
title: Project Meta docs triage
description: Folder-by-folder proposal for the 2,734 files under Project Meta docs/, with a reviewed column that overrides the mechanical rule
---

# Project Meta docs triage (slice 0b)

Nothing here has been moved, archived or deleted. This is a proposal table for Brian (Decision 6, approved as the first step instead of a wiki index; inferred by agent: the reviewed column).

Source: Project Meta `f1e27c906`, cutoff 2026-10-14; produced by `scripts/project_meta_docs_triage.py`, raw output in `evidence/runs/project-meta-docs-triage-20261114.json`.

The mechanical rule is fixed: outside mentions > 0 or changed since cutoff > 0 means read, otherwise archive. It gives 1,604 files read and 1,130 archive across 17 folders. The reviewed column overrides it where the rule is wrong; the main errors are generated wiki folders (changes there are regeneration) and `ops` (mixed content).

| Folder | Files | MiB | Changed since cutoff | Outside mentions | Mechanical | Reviewed proposal | Reason |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| project_wiki_mediawiki | 888 | 3.2 | 268 | 0 | read | regenerate or archive | Written by `render_project_wiki_mediawiki.py` from `PROJECT_GRAPH.json`. The 268 recent changes are regeneration, not editing. Output follows the project graph owner (slice 4); do not read page by page. |
| wiki_artifacts_mediawiki | 663 | 6.1 | 0 | 0 | archive | archive | Same generator manifest; nothing changed since 2026-09-01 and nothing outside refers to it. |
| evidence | 451 | 8.9 | 0 | 0 | archive | archive | Old run records, last commit 2026-09-17, no outside mentions. Keep the folder whole, not file by file. |
| plans | 393 | 5.7 | 0 | 102 | read | read a sample, then archive whole | 393 files, 102 outside mentions: those links must still resolve, so the archive keeps the same relative paths. |
| ops | 207 | 4.0 | 4 | 107 | read | read, split by file type | 207 files mix hand-written markdown (read) with script-written tsv/json (archive with the script that writes them). 107 outside mentions. |
| meta-patterns | 40 | 0.2 | 0 | 6 | read | read | 40 small files; the likeliest place for ideas worth porting into AES. |
| planning | 17 | 0.2 | 17 | 0 | read | read | All 17 files changed since the cutoff; most recent live material. |
| designs | 16 | 0.3 | 0 | 17 | read | read | 16 files, 17 outside mentions. |
| portfolio_wiki_mediawiki | 13 | 0.1 | 1 | 0 | read | read, generator unconfirmed | Name suggests generated, but no render script mentions it. Find the writer before deciding. |
| reviews | 12 | 3.0 | 0 | 6 | read | read, then likely archive | 12 files but 3.0 MiB: large review dumps. |
| migrations | 10 | 0.1 | 0 | 0 | archive | archive | No mentions, untouched since 2026-09-12. |
| repo_versioning_notes | 7 | 0.0 | 0 | 16 | read | read | 7 tiny files, 16 outside mentions. |
| project_restart_protocol | 6 | 0.0 | 0 | 6 | read | read | 6 files, 6 outside mentions. |
| handoffs | 5 | 0.1 | 0 | 1 | read | read | 5 files, 1 outside mention. |
| model | 3 | 0.0 | 0 | 0 | archive | archive | 3 files, no mentions. |
| runs | 2 | 0.0 | 0 | 0 | archive | archive | 2 files, no mentions. |
| decisions | 1 | 0.0 | 0 | 0 | archive | read the one file, then archive | A single file; named by 2 scripts. |

## Limits

- Mentions are text matches of `docs/<folder>` in the other repositories and `scripts/`, not proof of runtime use.
- The generated-by hint is a path match in builder scripts; only `render_project_wiki_mediawiki.py` was read to confirm.
- The reviewed column rests on folder-level facts and one script read, not on reading the files. "Read" means a later reading pass, not done here.
- "Archive" means a move to `~/archive/project-meta/<timestamp>/` with a log, after the slice's ablation step; nothing is deleted.
