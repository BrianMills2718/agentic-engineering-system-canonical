---
plan_id: aes-brownfield-docs
status: shaping
method_conformance_receipt: proposals/aes-brownfield-docs/conformance.receipt.json
planning_path_decision: proposals/aes-brownfield-docs/PLANNING_PATH.json
goal:
  outcome: graph-retrieval's documentation follows AES canonical's declared layout, and a reader reaches every document meant for reading from wiki/index.md within two clicks; the retrofit is recorded in AES canonical as evidence for the documentation-rule decision
  canonical_example: an agent new to graph-retrieval, asked "why does this repository orchestrate agents the way it does?", clicks wiki/index.md -> Decisions -> docs/decisions/DECISIONS.md#001-agent-orchestration-architecture and cites that section; proposals/aes-brownfield-docs/reach.py on merged main reports every unreachable file as an instruction file, fixture, generated output or tool-read template, and none as an orphan
  forbidden_substitutes: a file-count target; one flat list of every file in place of routed navigation; rewriting or summarising document content; a reachability number without classifying each unreachable file; a cold-reader run that is handed file paths instead of starting at wiki/index.md
  boundaries: Inside-Success/graph-retrieval through one pull request at a time (gh-insidesuccess) and this plan folder only; no other repository; no change to AES's .agentic/repo.yaml contract or to the workspace documentation rule (that is Brian's M3 decision)
  done_when: the M1 pull request is merged and reach.py on graph-retrieval main reports 0 orphan reader documents; the cold-reader transcript answers the plan's five questions, each citing a document reached through wiki links within two hops; graph-retrieval's checks give the same results as on main before the change; the M2 retrofit note is committed in this folder
  do_not_gate_on: Brian reading this plan or a review page; the M3 rule decision; other repositories adopting the layout
  owner: claude-code:shaping-aes-brownfield-docs
---

# AES Brownfield Documentation Layout: Living Plan

**Authority:** Brian, 2026-10-07: "ok lets make our plans movigin forward company plans complaint", following his approval of the graph-retrieval pilot and "we want the wiki to act as a naviagational alyer". Repository authority: AES canonical `.agentic/repo.yaml` (layout pilot contract), project-meta `docs/ops/WIKI_AND_DOCS_POLICY.md` (docs/generated/wiki split).
**Selected controls:** continuity across sessions (this plan); uncertainty (layout never applied to an existing repo); one writer; reversible (git); no external effect beyond pull requests.
**Artifact consumer / decision value:** Brian and the agents that continue this work; it decides whether AES's documentation layout replaces the 100-file count as the documentation rule.
**Stage / investment boundary:** pilot on one repository.
**Last outcome-bearing update:** 2026-10-07, graph-retrieval main 8cc8c598 (PRs #246 and #248): 0 orphans, 76 documents reachable within two clicks, cold reader answered all five questions; see [RETROFIT_NOTE.md](RETROFIT_NOTE.md).

## Outcome And Boundaries

<a id="outcome"></a>
**Outcome:** A reader of graph-retrieval (Brian, or an agent with no prior context) opens `wiki/index.md` and reaches any document meant for reading within two clicks, finding decisions under `docs/decisions/`, governing design under `docs/architecture/`, and plans under `docs/plans/`, as declared in the repository's `.agentic/repo.yaml`. Today 23 reader documents (including the root `README.md`, `KNOWLEDGE.md`, `FUNCTIONALITY.md`) cannot be reached from the wiki at all.

**Example.** An agent new to graph-retrieval is asked "why does this repository orchestrate agents the way it does?". Today it opens `wiki/index.md` and finds no route to the decision log or the root `README.md`; it falls back to searching the tree. After M1 it clicks `wiki/index.md` -> "Decisions" -> `docs/decisions/DECISIONS.md#001-agent-orchestration-architecture` (two clicks) and cites that section. The same path works for the root `README.md` ("What this repository does", one click) and for the active plan (`docs/plans/206_...`, two clicks).

**Actor and recurring job:** an agent or Brian starting work in the repository and needing to find the current state, a past decision, or the active plan.

**System model:** exempt: one repository's documentation layout; the layout contract (`.agentic/repo.yaml`) is the model.

<a id="canonical-probe"></a>
**Canonical probe:** Starting state: graph-retrieval main 4e1403fb, `proposals/aes-brownfield-docs/reach.py` reports 97 tracked .md, 56 reachable from `wiki/index.md`, 41 unreachable (18 instruction files, 23 others). Action: apply the active slice. Inspectable result: `reach.py` reports every unreachable file as one of the allowed kinds (instruction file read by path, test fixture, generated output with its generator named, template read by a tool), and a cold agent answers five fixed questions using only links from `wiki/index.md`. Negative case: a reader document deliberately left unlinked must be reported as an orphan by the check.

<a id="success-disproof"></a>
**Success evidence:** (1) `reach.py` classification shows zero orphan reader documents; (2) the cold-reader run answers the five questions with the source document cited for each, every citation reached via wiki links; (3) the repository's own checks give the same results as on unchanged main (doc-links, sync_plan_status --check, check_doc_coupling --strict, validate_document_authority, make ci-check, targeted pytest).
**Disproof:** any orphan reader document remains; the cold agent needs a file it could not reach from the wiki; or any repository check newly fails. Also disproved if the AES layout forces tooling changes larger than the documentation moves themselves (more than about 10 files of non-documentation code), which would mean the layout does not fit existing repositories.

<a id="non-goals"></a>
**Non-goals:** AES code governance of existing repositories, which `proposals/aes-adopt-existing` owns (`aes adopt` legacy baseline for `src/` and `tests/`, merged 2026-10-07); a file-count target; rewriting document content; other repositories before the pilot result; changing AES's layout contract itself.

**Authority limits:** pull requests to Inside-Success/graph-retrieval merged by the agent after its checks pass (Brian's standing merge rule); no spend beyond normal agent use; nothing published or sent outward.

## Architecture And Capability Invariants

- `.agentic/repo.yaml` in the target repo declares the roots; the wiki entry is `wiki/index.md`; decisions live under `docs/decisions/`, governing design under `docs/architecture/`, plans under `docs/plans/`.
- The wiki links and routes; it does not copy content (project-meta wiki-system: "authority lives once, wiki explains and links").
- Every moved document stays reachable by its old path through git history and a redirect line in the restore index; every reference in code, tests, configs and docs is repointed in the same change.
- Plan files that the repo's plan tooling creates and edits per file stay as files.

```text
reader finds doc <- wiki/index.md links <- declared roots (.agentic/repo.yaml) <- docs moved and repointed <- current graph-retrieval main
```

<a id="shared-mechanism"></a>
| Capability | Canonical owner/seam | Typed dependencies | Evidence | State |
|---|---|---|---|---|
| Layout declaration | AES canonical `.agentic/repo.yaml` (schema 0.1-pilot) | none | AES canonical's own copy | reuse, unchanged |
| Reachability measure | `proposals/aes-brownfield-docs/reach.py` (committed with this plan); to move into project-meta `scripts/md_file_cap.py` daily check | git refs | 4-repo run 2026-10-07 | extend existing daily check at milestone 3; no new service |
| Doc tooling in graph-retrieval | `scripts/check_markdown_links.py`, `scripts/meta/sync_plan_status.py`, `scripts/relationships.yaml` | paths of moved docs | PR #245 changed the same seams successfully | adapt (repoint paths only) |

## Milestone Horizon

| Milestone | Planning state | Inspectable output / stable boundary | Required capability and evidence | Promotion or replan trigger |
|---|---|---|---|---|
| M1 Pilot on graph-retrieval | done 2026-10-07 (graph-retrieval #246, #248) | merged PR; reach classification with zero orphans; cold-reader transcript | active slice below | promote to M2 when success evidence holds; replan if disproof fires |
| M2 Record the retrofit in AES canonical | done 2026-10-07 ([RETROFIT_NOTE.md](RETROFIT_NOTE.md)) | a retrofit note in this proposal folder: what the layout required of an existing repo, what tooling changed | M1 evidence | M1 merged |
| M3 Replace the count rule | done 2026-10-07: Brian chose both rules ("probably both"); workspace AGENTS.md (projects-dotclaude #102) and the daily check (project-meta #2444) | project-meta daily check reports orphans and layout per repo; AGENTS.md rule reworded from "100 files" to reachability with 100 as a tripwire | M1 + M2 | Brian's go-ahead on the rule wording (human decision) |
| M4 Roll out to further repos | deliberately_deferred | one PR per repo | M3 | after M3 |

## Active Slice

**Visible result:** graph-retrieval main where every reader document is reachable from `wiki/index.md` within two clicks, laid out under the AES roots and declared in `.agentic/repo.yaml`.

**Input / output and affected boundaries:** input graph-retrieval main 4e1403fb. Output one PR that: adds `.agentic/repo.yaml` (roots as AES canonical's, no planning keys); moves `docs/adr/*` to `docs/decisions/`; moves the governing design documents (identified by `validate_document_authority.py` and `docs/ACTIVE_DOCS.md` as authority) to `docs/architecture/`; links the 23 unreachable non-instruction documents from `wiki/index.md` or classifies them (generated output, template, fixture); repoints every reference across all file types.

**Implementation constraints:** claimed worktree in graph-retrieval; Inside Success git transport (`gh-insidesuccess`); the repo's own hooks, never bypassed; no content rewriting.

**Focused check and authentic observation:** `reach.py` with classification on the branch; the repo checks listed under success evidence, on branch and main; then a fresh agent, given only the repository and the instruction "start at wiki/index.md", answers: (1) what does the repo do, (2) where is the decision about agent orchestration architecture, (3) what plan is in progress, (4) how are plan statuses checked, (5) where do generated readouts come from. Each answer must cite a document reached through wiki links.

**Failure / containment / rollback:** if any repo check newly fails or the cold reader cannot reach a cited document, fix within the slice or revert the PR; old paths remain in git history.

## Decisions And Assumptions

<a id="uncertainties"></a>
Settled choices:

| Choice | Disposition | Reason / evidence | Affected boundary |
|---|---|---|---|
| Pilot repository is graph-retrieval | human_set | Brian approved option (a), 2026-10-07 | M1 |
| Plans follow Company Planning | human_set | Brian, 2026-10-07 | this plan |
| Path durable_solo, depth Small | agent_decided_reversible | PLANNING_PATH.json validated (classified durable_solo) | planning |
| Five fixed cold-reader questions | agent_decided_reversible | cover purpose, a decision, an active plan, tooling, generated outputs | M1 acceptance |
| AES's pinned wiki_methodology entrypoint is valid | agent_decided_reversible | `git cat-file -e 0cddc6b1:docs/architecture/README.md` succeeds; the file was removed on later main only | layout contract |

Material uncertainties. These three are the complete set; each could make the pilot fail its purpose, and there are no others.

| Material uncertainty | Disposition | Owner | Evidence that resolves it |
|---|---|---|---|
| "Two clicks" is the right reachability bound | assumption | this plan's owner (claude-code:shaping-aes-brownfield-docs) | The M1 cold-reader run records link hops to each cited document; any answer needing more than two hops, or Brian setting a different bound when he reads the M1 result, changes the bound and the wiki page before M3. |
| The AES layout fits an existing repository without large tooling changes | assumption | this plan's owner | The M1 pull request's diff: more than about 10 changed non-documentation files triggers the disproof in "Success evidence" and a retrofit note at M2 saying what the layout should change. |
| Whether the workspace rule changes from a 100-file cap to wiki reachability | human_set: both rules ("probably both", 2026-10-07) | Brian | His answer to the M3 decision, given after he has seen the merged M1 pull request, the reachability result and the cold-reader transcript. Until then the 100-file rule stays in force. |

## Evidence And Current State

| Claim or result | Exact evidence | Limitation | Status |
|---|---|---|---|
| 41 of 97 docs unreachable from wiki | reach.py on graph-retrieval 4e1403fb | link-following only; does not judge usefulness | measured (before) |
| 0 orphans; 76 of 98 reachable within two clicks; 22 unlinked are instruction files, a fixture and a template | reach.py on graph-retrieval 8cc8c598; negative control (README link removed) reports 1 orphan, exit 1 | link-following only | measured (after) |
| Cold reader answers all five questions within two clicks | [cold-reader-transcripts.json](cold-reader-transcripts.json) run 2 at 8cc8c598; tool calls checked against claims | harness auto-loads nested instruction files | passed (run 1 at a1d401b9 failed question 5; repaired in #248) |
| Repository checks unchanged | same command set on branch and on unchanged main, both runs | `check_doc_coupling --validate-config` fails on both (pre-existing) | identical |
| 18 of the 41 are instruction files | basename CLAUDE.md/AGENTS.md among unreachable | other loader-read files not yet classified | measured |
| Consolidation kept checks green | graph-retrieval PR #245 check list | same failures on main and branch | merged |
| AES treats retrofit as later capability | AES Decision 0010; v0.2 design thesis section 2 | no retrofit procedure exists | read |

## Human Decisions

- None open. M3 was decided by Brian on 2026-10-07: keep the 100-file cap and add wiki reachability.

## Exact Next Action

M4 rollout, deliberately deferred until scoped: the first daily run of the extended check (project-meta `scripts/md_file_cap.py`) lists every owned repository breaking either rule (2026-10-07 dry run: 36 over the cap, 152 with unreachable reader documents, 28 with no `wiki/index.md`). Each repository is brought into the AES layout with this pilot's method, one pull request per repository, starting with those whose orphans are a few reader documents rather than source collections.

<a id="prior-art"></a>
## Prior Art And Parallel-Implementation Check

Searched: internal lineage in AES canonical (`git grep -i 'retrofit|brownfield|existing repositor'` over docs, proposals and research, which found Decision 0010, the v0.2 architecture and `proposals/aes-adopt-existing`), every `~/code` repository for an existing `.agentic/repo.yaml` (AES canonical, collective-competence, collective-competence-aeon-p0), project-meta's wiki policies, and external documentation-structure practice. Existing ownership searched in graph-retrieval itself: its documentation tooling (`scripts/check_markdown_links.py`, `scripts/meta/sync_plan_status.py`, `scripts/meta/validate_plan.py`, `scripts/validate_document_authority.py`, `scripts/relationships.yaml`, `docs/ACTIVE_DOCS.md`).


| Existing capability | Owner / seam | Disposition | Why |
|---|---|---|---|
| Repository layout declaration | AES canonical `.agentic/repo.yaml` (pilot contract) | reuse | It already names the wiki entry and the decision, design and plan roots; this pilot adopts it unchanged in a second repository. |
| Wiki as navigation layer | project-meta `wiki/wiki-system.md` and `docs/ops/WIKI_AND_DOCS_POLICY.md`; adopted methodology `wiki_methodology@0cddc6b1` | reuse | "authority lives once, wiki explains and links" is the rule this pilot measures. |
| Daily documentation check | project-meta `scripts/md_file_cap.py`, run by `workspace_map_alert.py` | extend (M3) | The reachability measure joins the existing check and its keyed concern; no second checker, timer or alert. |
| Restore index for moved documents | `docs/ARCHIVED_DOCS_INDEX.md` added in graph-retrieval PR #244 | reuse | Moved paths get a line there instead of a new redirect mechanism. |
| `proposals/aes-adopt-existing` (`aes adopt`, legacy baseline) | AES canonical, merged 2026-10-07 | compose | It brings an existing repository's code under AES; this plan brings its documentation under the AES layout. Together they are the brownfield path; neither reimplements the other. |
| AES Decision 0010 and the v0.2 architecture (`docs/architecture/greenfield-v0.2/`) | AES canonical | bounded exception | They define AES v0.2 for new projects and declare retrofit of existing repositories a non-goal of the code-governance MVP. This plan uses none of the v0.2 code governance; it adopts only the `.agentic/repo.yaml` documentation layout, which Decision 0010 does not govern. |
| graph-retrieval documentation tooling (link checker, plan-status sync, plan validator, authority validator, relationships.yaml, ACTIVE_DOCS.md) | Inside-Success/graph-retrieval | extend | Paths are repointed to the AES roots and the tools keep their jobs; the consolidation PR #245 already extended the same tools for anchors. No new checker is added in the repository. |
| collective-competence-aeon-p0's `.agentic/repo.yaml` | BrianMills2718/collective-competence-aeon-p0 | reuse | A variant checkout of collective-competence with the same layout declaration; read as a third example, not a separate pattern. |
| collective-competence's `.agentic/repo.yaml` | BrianMills2718/collective-competence | reuse | An existing repository already declaring the AES layout; its file is the second example to copy from, alongside AES canonical's own. |
| Diátaxis-style document typing, adr-tools one-file-per-ADR | external prior art | bounded exception | Not adopted for this pilot: the AES roots already decide document homes and graph-retrieval already keeps one consolidated decision log; a second typing scheme would be a second authority. Revisit if the M1 cold reader cannot find documents by type. |

<a id="parallel-check"></a>
**Parallel-implementation check:** at M3, `git grep -l "wiki/index.md" -- 'scripts/*.py'` in project-meta must return only `scripts/md_file_cap.py` (no second reachability checker), and the authentic consumer proof is the daily `md-file-cap` concern listing orphan documents by repository from the scheduled `workspace-map-check` run. In graph-retrieval, `git grep -n "docs/adr/"` across all files on the merged branch must return no live references, so no reader or tool keeps using the old decisions home in parallel.

## Activation Facts

Declared in `activation-facts.json`: `shared_mechanism` true, because M3 extends the shared daily documentation check in project-meta (`scripts/md_file_cap.py`) and the workspace rule every agent follows. `empirical_comparison_proposed` false: no alternative designs are compared; the cold-reader run checks the built result against fixed questions. `llm_central` false: no model call is part of the change; the cold reader is an evaluation step, not a product component. `irreversible_or_spend_action` false: see "Irreversible Actions And Spend".

<a id="route"></a>
## Route

Company Planning path `durable_solo` (PLANNING_PATH.json), bounded-design depth Small: one repository, reversible, no shared contract changed, no data migration, no registry, no external publication. No work graph or packet: one writer, no machine consumer.

<a id="irreversible-spend"></a>
## Irreversible Actions And Spend

This plan proposes zero irreversible actions and zero spend.

| Action | Boundary | Authorizer | Containment |
|---|---|---|---|
| Moving and linking documents in graph-retrieval | one pull request to Inside-Success/graph-retrieval, merged after its checks pass | Brian's standing merge rule (workspace AGENTS.md, 2026-10-04) | `git revert` of the merge commit; every moved file keeps its full history and its old path is listed in `docs/ARCHIVED_DOCS_INDEX.md` |
| Proposal files in AES canonical | this folder on branch `shaping/aes-brownfield-docs` | Brian (approved the pilot, 2026-10-07) | delete the branch or revert the merge |
| Rule change at M3 | workspace AGENTS.md and project-meta daily check | Brian (human decision listed above) | revert the two commits |

No model spend beyond ordinary agent use, no deployment, no data deletion, nothing sent outward.
