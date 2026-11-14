---
description: How AES separates document authority and lifecycle from the views used to read it
status: current
---

# Documentation: authorities and reading views

AES keeps each fact with its owning source and presents related facts together for a reader. A research finding, an accepted requirement, a plan and an execution receipt can concern the same feature without becoming interchangeable kinds of truth. The authority map reconciles existing architecture and decisions. The upkeep section records the subsequently authorized catalog maintenance and freshness gate.

Source: the methodology adopted in [.agentic/repo.yaml](../../.agentic/repo.yaml), specifically [documentation architecture](https://github.com/BrianMills2718/wiki_methodology/blob/0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe/docs/architecture/AGENTIC_CODING_DOCUMENTATION_ARCHITECTURE.md) and [concern-root vocabulary](https://github.com/BrianMills2718/wiki_methodology/blob/0cddc6b1d75a9dbc39019cfa2ce6183aac790cbe/docs/architecture/REPOSITORY_CONCERN_ROOTS.md); AES [Decision 0004](../decisions/0004-compact-structured-normative-records-and-generated-views.md) and Brian's accepted [Decision 0013](../decisions/0013-truth-lives-where-it-is-edited.md).

## Which source owns what?

| Kind | Authority and lifecycle | Editing rule in AES |
| --- | --- | --- |
| Normative architecture and required behavior | What should be true; changed through an explicit design or requirement change | Architecture belongs in `docs/architecture/`; current required behavior belongs in `openspec/specs/`. Change those sources rather than inferring requirements from code. |
| Research | Sources, bounded investigations and reusable synthesis inform choices; findings do not become requirements by being cited | Preserve source provenance and uncertainty. Promote accepted conclusions through the owning requirement or decision. Historical research may be linked at its retained revision. |
| Decisions | Accepted choices, rationale and supersession | Keep the original choice attributable; record a replacement or amendment explicitly in `docs/decisions/`. |
| Proposals and plans | A proposal is non-binding until adopted; a plan owns bounded change, not timeless product truth | Current behavior changes use OpenSpec proposals and tasks. Planning-package documents describe their own scope. Do not revive retired `docs/plans/` or `.aes/target.yaml` as AES's workflow. |
| Evidence | What was observed at a particular revision, time and environment | Retain the observation and its provenance; revise the interpretation separately. Passing a test does not redefine intended behavior. Keep private evidence in its governed private store. |
| Generated material | Rebuildable output from named inputs; never an independent authority | Edit the inputs and regenerate. Identify the source and generator. A generated file need not physically live under `generated/`—`AGENTS.md` is an example. |
| Wiki | Derived navigation and synthesis across sources | Organize a reading path around the reader's concern; link native authorities and preserve uncertainty. Do not add a competing editable copy of a source-owned fact. |
| PRD and other conventional views | Decision 0004's design treats a PRD as a view of goals, actors, outcomes, journeys and requirements | That is the historical structured-record target, not a claim that a complete PRD generator or universal record schema operates today. Use the actual declared sources; do not invent a second PRD authority. |

The upstream concern-root vocabulary is explicitly a **candidate**, not a frozen mandate to create every folder. Its categories distinguish ownership, authority and lifecycle. Native code, typed contracts and tool configuration retain their native homes. AES's repository declaration records routing, but some older provider and implementation fields still describe retired work; use the [retirement record](../retired/2026-11-12.md) when interpreting them.

## What belongs in a wiki summary?

A reader investigating one concern should be able to move from its intended behavior to current evidence, remaining gap and next action without mentally joining unrelated document silos. The adopted architecture calls this a concern view: target, success criteria, current state, gap, plan, implementation and verification. Those are reading dimensions, not permission to merge their authorities.

Brian's [Decision 0013](../decisions/0013-truth-lives-where-it-is-edited.md) sharpens the editing boundary: a document's description belongs in that document; a code description belongs in its docstring. Catalogs and wiki views displaying those facts take them from that source. Rules applying to many artifacts remain authored once, with source-local projections where implemented. A hand-written description kept only in a remote wiki page cannot reliably follow edits to its subject.

Cross-source synthesis still helps readers understand relationships and conflicts. It should explain those relationships with links, rather than silently owning facts that belong elsewhere. This wiki is a navigation layer; its existence does not prove all summaries are generated or fresh. Current projection work is described on [Lockstep's page](../../wiki/lockstep.md); the old docstring-wiki generator was [retired](../retired/2026-11-12.md).

## Current workflow versus historical design

Decision 0004 proposed compact system/component records with generated conventional documents and an explicit single-authority migration. It expressly left accepted Markdown authoritative until a separate cutover. Decision 0010 carried those principles into the historical v0.2 line; AES subsequently retired its own `.aes/` governance. Current [repository instructions](../../CLAUDE.md) use OpenSpec for required behavior, and [.agentic/repo.yaml](../../.agentic/repo.yaml) names that requirements source. Do not interpret the old record design as a replacement for today's OpenSpec files.

Unresolved documentation and realization gaps belong in the [open-questions ledger](../../wiki/open-questions.md), rather than being hidden by a polished navigation page.

## Coverage and consolidation assessment

Source: Brian, 2026-11-13, clarified that every file must be reachable and
summarized from the navigational wiki and that the review should assess
consolidation and optimization (AES #849). This broadens the earlier
reader-Markdown check. The boundary here is every Git-tracked file in AES
canonical, plus explicit navigation to owning external sources. Ignored caches,
installed environments, credentials and private runtime stores are not silently
published or treated as repository documentation.

### What the earlier check missed

At base revision `2034c64`, AES had 407 tracked files and 126 Markdown files.
The earlier reachability result covered 69 reader Markdown files. Generated
instructions, archived changes, fixture documents and all non-Markdown files
fell outside that check. The catalog also left entries without summaries when
source description metadata was absent. These were material scope gaps.

A structural inspection found 227 files with a standard Markdown description,
Python module docstring or native top-level description field, and 180 without
one. This counts those fields, not summary accuracy. Some formats legitimately
have no place for prose: a lockfile, empty package marker or generated client
sentinel needs a derived description bound to its actual contents and owner.

The initial compiled review covered 408 files: all 407 base files plus the inventory
itself. Initial review dispositions are 332 keep, 35 update, 38 generated and
three consolidation candidates. The record retains 22 findings and 12 grouped
consolidation recommendations. These counts describe assessment, not completed
repairs or retirement approvals.

### The replacement coverage contract

- [The complete file catalog](../../wiki/documents.md) lists each tracked file
  with a concrete purpose, role and review disposition. It includes generated
  views, fixtures and history without promoting them to current authority.
- [The source inventory](../planning/file-inventory.json) records per-file
  summaries, source locators, content identities and assessment reasons. It is a
  derived review record, not a replacement for source authorities.
- Existing source descriptions are preferred where they accurately summarize
  the file. Other summaries are explicit content reviews, bound to source hashes.
  A changed input needs review; a matching hash does not prove semantic quality.
- Inventory and catalog entries describe themselves as generated review views.
  Their own output digests are omitted to avoid a self-referential checksum;
  they remain included in coverage. They do not claim continuous automatic refresh.
- A coverage check must compare the actual tracked path set with the inventory
  and the catalog, verify nonempty summaries and resolve each link. The Markdown
  reachability tool remains useful but is insufficient for this wider claim.

### Consolidation decisions and recommendations

| Concern | Assessment and disposition | Information that must survive |
| --- | --- | --- |
| File catalogs | Consolidate the reader-only enumeration into one complete catalog, backed by one inventory. Keep the question-based front page as a different reading view. | Every file's purpose, source and role; direct concern routes and decision history. Applied in this repair. |
| Planning versus Lockstep | Show planning as an explicit function supplied by Company Planning. Lockstep consumes and checks its output. The old three-part shorthand was incomplete as a functional map. | Planning method ownership, behavioral decomposition, interfaces, tests and evidence boundaries. Applied to the current overview. |
| Policy inventories | Link the original Project Meta register, AES's small register, provisional migration manifest and shared instruction sources from one policy reading path. Do not merge their contents or infer retirement. | All 263 original identifiers and texts, current authority, proposed dispositions, source provenance and actual enforcement. Navigation repaired; per-policy reconciliation remains open. |
| Current contracts versus legacy implementation | Keep OpenSpec/layout contracts separate from retained AES-target records and the legacy behavior checker. | The stronger legacy one-behavior/one-file rule, modern layout's different representation, normative-change history and proving fixtures. Documentation now exposes the distinction. |
| Generated planning pages and graphs | Regenerate from their owning ledger/build inputs or label them as dated records. Do not hand-edit a generated PASS or erase old evidence to match the latest count. | Run revision, observation boundary, earlier open questions, generator and source identities. Recommendations remain open. |
| Machine-readable repository maps | Reconcile current provider/path claims separately from retained historical relationships before any runtime/configuration change. | Former component identity and acceptance history, current actual callers and routing semantics. Kept with update findings. |
| Agent/client instructions | Shared workflow text may be consolidated at its generator, preserving client-specific adapters. Avoid deleting mirrors on matching names. | Trigger metadata, native syntax, client enablement and recovery instructions. Generator-level proposal only. |
| Brain and wiki summaries | Keep identity, current action, dated observations and historical receipts distinct; source-link repeated facts and collapse long historical reading paths where safe. | Unique delivery receipts, open obligations, restore paths and chronology. No history retired by this review. |
| Taxonomy maintenance prose | Preserve the taxonomy and provenance; correct the obsolete claim that family labeling/problem analysis is unbuilt. | Family definitions, derivation caveats and the distinction between implemented code and enabled/completed jobs. Applied in place. |

This is not a file-count reduction target. A small live document may deserve to
remain distinct because it owns different facts or a different lifecycle. A
consolidation candidate requires an actual content comparison, named survivor,
retained unique claims and updated inbound references before retirement.
Generated and historical files remain discoverable even when they should not be
read as the current answer.

### Initial review and verification limits (historical)

This review compiles a dated repository snapshot. Current native fact refresh
covers declared projections; it is not a universal summarizer for every file.
The complete catalog must be refreshed and its semantic descriptions reviewed
when its inputs change. The initial documentation repair introduced no new service, classifier or runtime
gate; the subsequently authorized upkeep below adds the catalog freshness check. Verification records state which files and sources
were checked; unresolved recommendations remain in the discussion ledger.

## Ongoing complete-file catalog upkeep

Source: Brian, 2026-11-13, “i approve proceed” after the recommendation to repair
the wiki's actual upkeep path (AES #857). This deliberately extends the existing
complete-file inventory and native Lockstep refresh; Repo Docs retains its code
documentation role. It does not restart the retired universal AES regime.

The optional `catalog` declaration in `lockstep.yaml` names the existing
inventory and catalog. Git's index supplies membership, including staged new
files and staged deletions. Ignored and untracked private runtime files are not
published. Add a new intended repository file to Git before expecting the catalog
to include it. A missing indexed file is an error until its deletion is staged.

1. A native source edit invokes the existing post-edit refresh. It regenerates
   deterministic navigation and reports pending semantic reviews to the agent.
   The hook uses Claude's documented [PostToolUse additional context](https://code.claude.com/docs/en/hooks#posttooluse-decision-control).
2. The agent runs `lockstep catalog pending`, reads each complete changed source
   and checks the affected wiki explanations. It revises the summary or explicitly
   retains it with a reason. This is agent judgment, not a test outcome.
3. In ignored `.lockstep/reviews.json`, the agent writes a JSON list of rows:
   `path`, the observed `sha256`, `summary`, and `review_reason`. New entries also
   need `role`, `disposition`, `reason` and `source_locator`. It submits the list
   with `lockstep catalog review --input .lockstep/reviews.json`.
4. Review rejects a changed source hash before updating the inventory. After a
   successful review, `lockstep catalog refresh` renders the stored summaries,
   roles, dispositions and links; `lockstep catalog check` independently checks
   membership, reviewed hashes and rendered output. `make check-catalog` calls
   that check locally and from the added pre-commit command.

For example, changing a search-once module to a looping search makes its old
review pending. Refresh cannot declare “search once” current by replacing its
hash. The agent must read the implementation and decide whether the summary
should change. Recording the observed hash prevents acknowledging a different
version that appeared after reading. It cannot prove the agent understood it.

Inventory and catalog remain included in coverage, with their own content
hashes omitted to avoid recursion. The catalog visibly marks pending source
reviews. Daily catalog and projection receipts under ignored `.lockstep/` record
review inputs, generated output identities and failures. Read-only checks do not
write receipts. The bounded retained demonstration will identify the native
client route actually exercised; configuration alone does not prove ordinary
session loading or Codex host execution.

This maintains the complete file catalog and declared fact blocks. Changes to
question-based wiki explanations still require the agent's semantic review;
automatic rendering does not establish their completeness or semantic truth.
