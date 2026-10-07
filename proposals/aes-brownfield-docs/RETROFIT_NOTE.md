# Retrofit note: AES documentation layout on an existing repository (graph-retrieval)

Milestone M2 of [`PLAN.md`](PLAN.md). Records what bringing an existing repository's documentation into AES canonical's declared layout actually took, so the documentation-rule decision (M3) and any rollout (M4) start from evidence.

## Result

Inside-Success/graph-retrieval, `main` at `8cc8c598` (PRs [#246](https://github.com/Inside-Success/graph-retrieval/pull/246) and [#248](https://github.com/Inside-Success/graph-retrieval/pull/248), repository Plan #207):

| Measure | Before (`4e1403fb`) | After (`8cc8c598`) |
|---|---|---|
| Tracked Markdown files | 97 | 98 (the repo's own Plan #207 file is the one added) |
| Reachable from `wiki/index.md` | 56 | 76, all within two clicks (55 in one) |
| Unreachable reader documents (orphans) | 14 | 0 |
| Unreachable, allowed kinds | 27 | 22: 20 instruction files, 1 fixture, 1 template (generator outputs are now linked) |
| Repository checks | baseline | identical to baseline (list below) |

Measured with [`reach.py`](reach.py). Negative control: a throwaway commit of the same `main` with the wiki's link to `README.md` removed reports `README.md` as the single orphan and exits 1.

## What the layout required of an existing repository

1. **Moves, not rewrites.** Decisions moved from `docs/adr/` to `docs/decisions/`; the three governing design documents (`GRAPH_DESIGN.md`, `REFERENCE.md`, `REPO_SURFACE.md`, identified as design by the repository's own `docs/ACTIVE_DOCS.md`) moved to `docs/architecture/`; plans were already in `docs/plans/`. Seven `git mv` operations; no document content changed.
2. **Repointing is the real work.** 28 files carried repo-root paths to moved documents and 7 carried relative links whose base or target moved. A two-pass transform (path strings, then link resolution from each file's original location) is committed in the repository as `scripts/doc_consolidation/aes_layout_move_2026-10-07.py`.
3. **History must be left alone.** Archive manifests, the 2026-10-07 consolidation mapping and restore commands describe past state; closed work graphs are bound to coordination claims by content hash, so editing them would break the binding. The transform excludes them explicitly.
4. **Short relative route text escapes path matching.** A nested instruction file (`docs/CLAUDE.md`) routed readers with paths relative to `docs/` (`adr/DECISIONS.md`), which a repo-root pattern does not match; it was fixed by hand after a search for short forms.
5. **The declaration is small.** `.agentic/repo.yaml` copies AES canonical's `navigation` and `authorities` keys unchanged; no planning keys, because the repository's plan tooling is its own.
6. **Navigation needed links, not structure.** All 14 orphans were reader documents that already existed (the root `README.md`, `FUNCTIONALITY.md`, `KNOWLEDGE.md`, folder READMEs, plan design companions). Each got one line in the wiki section a reader would look in; the wiki copies no content.
7. **Tooling changed: none.** No checker, hook or generator needed code changes for the layout (the disproof threshold was about 10 non-documentation files). The only script added is the move transform itself.

## Cold-reader test

A fresh agent with no prior context, told only to start at `wiki/index.md`, open nothing that was not linked, and use only the Read tool, answered the plan's five questions. Its tool calls were checked against its claims: every file it opened was reached through a link. Compact transcripts: [`cold-reader-transcripts.json`](cold-reader-transcripts.json).

- **Run 1** (`a1d401b9`, after #246): questions 1-4 answered within two clicks; question 5 only partly, because the generator scripts that write the plan readouts were named in code text but not linked. This is a navigation defect the reachability count could not see (the readouts themselves were allowed as generator outputs).
- **Repair** (#248): the wiki's documentation map links each generated readout to its generator.
- **Run 2** (`8cc8c598`): all five answered within two clicks, six files opened, including the action conformance matrix whose header names `scripts/generate_operator_conformance_matrix.py`.

Limitation reported by the cold reader itself: the harness loads nested `CLAUDE.md`/`AGENTS.md` files into an agent's context automatically, so the reader was not perfectly cold; it states none of its answers relied on them.

## Repository checks, before and after (identical)

`make doc-links`, `scripts/check_markdown_links.py`, `sync_plan_status.py --check`, `validate_document_authority.py`, `check_agents_sync.py --check`, the five `generate_*.py --check` runs, `tests/unit/test_consolidated_docs_tooling.py` with `test_meta_complete_plan.py` (7 passed), and `make ci-check` exit 0 on both. `check_doc_coupling.py --validate-config` exits 1 on both because `docs/configuration.md` is missing, which predates this work.

## Findings for the AES layout contract

- **The contract held.** Three roots plus a wiki entry fit an existing repository with seven moves and no tooling change.
- **Reachability needs a classification rule.** A count of unreachable files means nothing until each is classified; `reach.py` classifies by path and by code assignment (`*OUTPUT*` constants), never by reading prose.
- **Reachability is necessary, not sufficient.** Run 1 shows a reader can reach every document and still not reach the thing a question needs (a generator script). The cold-reader run is the check that catches this; keep both.
- **Repository plans versus AES plans.** The repository's commit rule wants `[Plan #N]`, and the AES commit rule (observe mode) logged that repository Plan #207 has no Company Planning receipt; the adopted Company Planning plan lives here in AES canonical. A repository plan that tracks an AES-adopted plan has no way to cite that receipt today.

## What this means for the open decision (M3)

The pilot supports measuring documentation by reachability from the wiki plus a cold-reader run, with a file count kept only as a tripwire. Whether the workspace rule changes is Brian's call (see `PLAN.md`, "Human Decisions").
