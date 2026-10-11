---
description: Truth lives where it is edited, so documents are generated or checked from their owning source
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills (2026-10-10, in conversation, quoted below)
date: 2026-10-10
reversible: true
amends:
  - docs/architecture/SYSTEM_BOUNDARY.md (adds AES-CTX-004)
---

# Decision 0013 - Truth lives where it is edited

Governs: generated/docstring_wiki.md, docs/architecture/SYSTEM_BOUNDARY.md#aes-ctx-004--truth-lives-where-it-is-edited

## Context

On 2026-10-10 a documentation cleanup of DIGIMON (542 Markdown files, 12 with
a description of themselves) proposed keeping per-file summaries in a separate
list. Brian stated the principle it was missing:

> "the source of truth should be at the place where the edits are made. for
> example if you put the summary of a file in the wiki, then when the agent
> goes and edits the file it doesnt know to update the wiki. but if you put
> the summary in the file then when the agent edits the file it sees that
> summary and updates it so the projection in the wiki stays up to date.
> this should be clear in the thesis documentation of aes canonical"

Decision 0003 item 3 already covers rules that govern many places (authored
once, generated into each). For code, `make docstring-wiki` generates a wiki
from docstrings and `make docstring-wiki-check` fails when it is stale.
Documents had no equivalent, and no clause said where a one-artifact fact lives.

## Decision

1. A fact about one artifact is authored in that artifact: a `description`
   front-matter line for a document, the docstring for code.
2. Wiki pages, indexes and catalogs that show such facts are generated from
   the in-artifact copy. The wiki routes and links; it holds no second
   hand-written copy.
3. A rule that governs many artifacts stays authored once and is generated
   into each implementing site (Decision 0003 item 3, AES-CTX-002).

## Wrong when

- In a sample of 20 recent commits that substantively changed a file with an
  in-file `description`, 3 or more leave that description wrong; or
- a fresh reader working only from a current generated catalog picks the wrong
  document for a question in 2 of 5 tries.

Either means co-location alone does not keep summaries true, and an edit-time
check (a large body change with an unchanged description) is needed.
