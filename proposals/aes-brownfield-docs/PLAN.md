---
plan_id: aes-brownfield-docs
status: shaping
method_conformance_receipt: proposals/aes-brownfield-docs/conformance.receipt.json
planning_path_decision: proposals/aes-brownfield-docs/PLANNING_PATH.json
goal:
  outcome: Inside-Success/brians-2nd-brain-integration-work is organized in AES canonical's layout (decisions in docs/decisions/, governing design in docs/architecture/, plans in docs/plans/, generated output separated from reading), with wiki/index.md routing by question to every reader document within two links
  canonical_example: an agent new to the repository, asked "why was the Foundation IR wiki visibility handled the way it is?", clicks wiki/index.md -> Decisions -> docs/decisions/ and cites the decision record; a decision record found outside the declared decision root fails the layout check
  forbidden_substitutes: reachability through generated per-folder lists without moving documents to their homes; a file-count target; rewriting or summarising document content; merging records the repository's registry keeps separate on purpose; a cold-reader run handed file paths
  boundaries: this repository through one pull request at a time (gh-insidesuccess) plus this plan folder; no change to the AES .agentic/repo.yaml contract; generated output keeps its generators working (paths repointed, not reimplemented)
  done_when: the migration map in this plan is complete and executed in a merged pull request; the layout check (declared roots exist and hold the decision, design and plan documents; generated output is under a generated area) and reach.py report no findings on main; a fresh agent answers the plan's five questions from wiki links within two hops; the repository's checks match main before the change
  do_not_gate_on: Brian reading this plan; other repositories; the daily check's rollout to Brian's own repositories
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
**Outcome:** Documentation is *organized*, not only reachable (Brian, 2026-10-08: "it isnt as much about unreachable pages to me as well organized pages ... the organization in aes canonical is at least a first approximation"). For Inside-Success/brians-2nd-brain-integration-work that means decisions in `docs/decisions/`, governing design in `docs/architecture/`, plans in `docs/plans/`, generated output separated from reading material, and `wiki/index.md` routing by question. graph-retrieval (M1) already has this shape.

**Example.** An agent new to graph-retrieval is asked "why does this repository orchestrate agents the way it does?". Today it opens `wiki/index.md` and finds no route to the decision log or the root `README.md`; it falls back to searching the tree. After M1 it clicks `wiki/index.md` -> "Decisions" -> `docs/decisions/DECISIONS.md#001-agent-orchestration-architecture` (two clicks) and cites that section. The same path works for the root `README.md` ("What this repository does", one click) and for the active plan (`docs/plans/206_...`, two clicks).

**Actor and recurring job:** an agent or Brian starting work in the repository and needing to find the current state, a past decision, or the active plan.

**System model:** exempt: one repository's documentation layout; the layout contract (`.agentic/repo.yaml`) is the model.

<a id="canonical-probe"></a>
**Canonical probe:** Starting state: integration repo main `7f91be42`, 2,086 tracked .md; decision records in `roadmap/decisions/` and as `plan/ADR-*.md`; design in `roadmap/architecture/`; plans in `plan/`; 666 generated pages in `plan/okf_exports/`; wiki reaches 264 documents. Action: the active slice. Inspectable result: the layout check finds every decision, design and plan document under its declared root and generated output in a generated area; `reach.py` finds no orphan; a fresh agent answers five questions from wiki links. Negative case: a decision record left in `plan/` fails the layout check.

<a id="success-disproof"></a>
**Success evidence:** (1) the migration map below is complete (every moved folder, its consumers, and their repointing) and executed in a merged pull request; (2) the layout check and `reach.py` report no findings on main; (3) a fresh agent on Haiku answers the five questions within two links; (4) the repository's checks (meta tests, `validate-okf`, `repo-hygiene`, `roadmap-spine-check`, the wiki-reading tests) match main before the change.

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
| M5 Organize the integration repository in the AES layout | fully_specifiable_now (after the migration map, step 1 of the active slice) | merged PR; layout check and reach.py clean; fresh-agent run | migration map; layout check | promote when success evidence holds; replan if the map shows the move breaks generators beyond path repointing |
| M6 Measure organization daily | conditional | project-meta daily check reports layout conformance per repository beside count and reachability | M5's layout check proven on two repositories | M5 done |

## Active Slice

**Visible result:** the integration repository organized in the AES layout, with the wiki routing by question.

**Input / output and affected boundaries:** input main `7f91be42`. Step 1 (no file moves): the migration map, one row per current home: `roadmap/decisions/` and `plan/ADR-*.md` -> `docs/decisions/`; `roadmap/architecture/` -> `docs/architecture/`; current plans in `plan/` -> `docs/plans/`; `plan/okf_exports/` -> under `generated/`; each row lists its consumers (scripts, Makefile targets, tests, `scripts/relationships.yaml` records, OKF validators) and how each is repointed. Step 2: one pull request that executes the map with `git mv`, repoints every consumer, and rewrites `wiki/index.md` to route by question. Knowledge entries stay separate files behind one index (the registry keeps each separately citable on purpose); evaluation readouts that tests open stay where the tests read them, declared as evidence.

**Implementation constraints:** claimed worktree; the repository's hooks; generators keep working with repointed paths; no content rewriting; Haiku agents for mechanical per-folder consumer inventory, the parent for the map and review.

**Focused check and authentic observation:** layout check (a script beside `reach.py`: roots exist; decision, design and plan documents inside their roots; generator outputs under the generated area); `reach.py`; the repository checks on branch and main; then a fresh Haiku agent answers: what the repository does; where decisions are and one decision; one plan in progress; one knowledge entry of type decision; where generated pages come from.

**Failure / containment / rollback:** if a generator or test cannot follow a moved path by repointing alone, that row stays and is recorded as a finding; revert the merge if checks newly fail. The earlier reachability-only branch (57 generated folder lists, unmerged) is not merged: it made pages reachable without organizing them.

## Migration Map (M5, integration repository)

Built 2026-10-08 from read-only Haiku inventories at main `7f91be42` (one batched consumer search per row) and a document-by-document classification of the plan folder (rules for 106 documents, a light model for the 139 that names could not settle; each call carries a quoted reason). Executed as three pull requests, in order, each compared with unchanged main before merge.

| PR | Row | Moves | Consumers to repoint | State |
|---|---|---|---|---|
| 1 | Decisions and design | 13 decision records (`roadmap/decisions/`, every `ADR-*`) to `docs/decisions/`; 17 design, requirement and governance documents (`roadmap/architecture/`, `roadmap/requirements/`, `roadmap/governance/`, four named methodology and contract documents) to `docs/architecture/` | about 11 tests and generators (`tests/meta/test_roadmap_spine.py` with sha256 fingerprints, `test_documentation_inventory.py`, `test_relationship_context_pilot.py`, `plan/documentation_review_index.py`), 445 registry lines, about 525 document-link lines; `docs/WIKI_BACKLINK_INDEX.json` rebuilt by its own tool | moved and repointed in the worktree; layout check clean except row 3's generated pages; test comparison showed regressions to fix before merge |
| 2 | Plans | 119 plans and goals to `docs/plans/` (keeping their sub-paths), 17 standards and design documents to `docs/architecture/`, 3 decision records to `docs/decisions/`; 106 stay (fixtures, release snapshots, dated notes and findings, redirect stubs, READMEs of code folders) | 21 tests and code readers (including a sha256 fingerprint ledger), 2,586 registry lines, about 1,343 link lines, 230 relative links into files that stay | classified; not started |
| 3 | Generated pages | `plan/okf_exports/` (822 files) to `generated/okf_exports/` | generator output-root guards (`plan/okf_projection/contracts.py`, `project_foundation_ir*.py`), Makefile targets, `scripts/artifact_directory_policy.yaml`, 3,602 registry lines, manifests that record each page's sha256 and embed its path | not started; if the guards and manifests cannot follow by path repointing and regeneration alone, the row stays and is recorded as a finding (see Failure / containment) |

Unchanged on purpose: `plan/graph/okf/` (the planning graph that `make validate-okf` checks), `plan/atlas_refinement/readouts/` (evidence tests open), `knowledge/corpus/entries/` (kept separate by the registry), and all code under `plan/`. The layout check (`layout_check.py` in this folder) and `reach.py` are the done-when instruments.

## Decisions And Assumptions

<a id="uncertainties"></a>
Settled choices:

| Choice | Disposition | Reason / evidence | Affected boundary |
|---|---|---|---|
| Pilot repository is graph-retrieval | human_set | Brian approved option (a), 2026-10-07 | M1 |
| Plans follow Company Planning | human_set | Brian, 2026-10-07 | this plan |
| Path durable_solo, depth Small | agent_decided_reversible | PLANNING_PATH.json validated (classified durable_solo) | planning |
| Five fixed cold-reader questions | agent_decided_reversible | cover purpose, a decision, an active plan, tooling, generated outputs | M1 acceptance |
| Target is organization in the AES layout; reachability is a check on it | human_set | Brian, 2026-10-08 (quoted in Outcome) | M5, M6 |
| Knowledge entries stay separate files behind one index | agent_decided_reversible | the repository's registry records each entry with `separate_file_reason` and its own review questions | M5 |
| Integration repository is the next repository | human_set | Brian chose Inside Success second-brain repositories first; reverse-ontology-engine skipped ("it is not my repo") | M5 |
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

Fix migration PR 1's test regressions (repoint the tests' paths and fingerprint records, re-run until the failure list matches main), merge it, then PR 2.

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

Declared in `activation-facts.json`: `shared_mechanism` true, because M3 extends the shared daily documentation check in project-meta (`scripts/md_file_cap.py`) and the workspace rule every agent follows. `empirical_comparison_proposed` false: no alternative designs are compared; the cold-reader run checks the built result against fixed questions. `llm_central` false: no model call is part of the change; the cold reader is an evaluation step, not a product component. `irreversible_or_spend_action` true: M5 spends model tokens on bounded read-only Haiku agent fan-outs (boundary, authorizer and containment in "Irreversible Actions And Spend"); nothing irreversible.

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
| Agent work for M5 (read-only inventories and classifications on Haiku; the parent's own implementation runs) | one fan-out of at most four Haiku agents per migration step, read-only, no writes outside the session scratch folder | Brian's standing approval of multi-agent workflows and Haiku for bulk work (2026-10-07) | stop the fan-out if a step's agents exceed about 500k tokens without a usable result, and record it |
| Rule change at M3 | workspace AGENTS.md and project-meta daily check | Brian (human decision listed above) | revert the two commits |

Model spend is limited to the agent work row above; no deployment, no data deletion, nothing sent outward.
