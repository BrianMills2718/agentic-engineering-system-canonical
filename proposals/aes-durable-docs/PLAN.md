---
schema_version: "1.0"
artifact_type: design_plan
id: aes-durable-docs
status: proposed
method_conformance_receipt: proposals/aes-durable-docs/PLAN.receipt.json
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "Every governed repository keeps one fixed set of durable documents (goal and thesis, requirements with success criteria, the system model with traceable rules, decision records) that a fresh reader reaches from wiki/index.md, and no plan completes without updating the durable documents it declared."
  canonical_example: "In company-planning, an agent finishing a plan that changes the adoption gate: adoption refuses the plan until its Durable documents section names system-model rule RULE-ADOPT-GATE and a decision record; completion refuses until those two documents changed in the plan's commits; a fresh agent asked 'what rule governs plan adoption, who owns it, which check proves it and why' answers from wiki/index.md citing the rule ID, its owner file, its test and the decision record."
  forbidden_substitutes: "A count of documents per repository; a plan section that lists documents without the completion check verifying them; documents created empty or with placeholder text; a checker that passes on the pilots but was never shown to refuse a bad case; a cold-reader answer that cites files it did not open."
  boundaries: "Shaping in this folder of AES canonical; implementation by pull request to company-planning (plan template, adoption gate, completion check, references) and to the two pilot repositories; no change to scripts/complete_plan.py in enforced-planning while the Codex trace-review lane holds it; nothing published or sent outward."
  done_when: "Both pilots (company-planning, AES canonical) report zero findings from durable_docs_check.py on main; the two negative controls (a plan without the section is refused at adoption; a plan whose declared document did not change is refused at completion) are recorded with full output; the cold-reader run answers the canonical question with its navigation trace; each judged from the saved run outputs named under Success and disproof."
  do_not_gate_on: "Brian reading this plan; rollout to repositories beyond the two pilots (milestone M5); other teams adopting Company Planning."
---

# Durable documents every governed repository keeps

**Authority:** Brian, 2026-10-10, approving option (a), "I write the proposal in AES canonical and wire it into company planning's plan-finish step": "i approve a. i want plannign to be as rigorous as possible (within reason)". Earlier the same day: "i thin kthis '- Company planning: it centres on roadmaps and leaves the other document types optional.' shouldnt be the case."

**Last outcome-bearing update:** 2026-10-11 (UTC), M5 rollout merged in all 22 inventoried repositories (`evidence/m5-inventory.json`, per-repository PRs, merge methods and deviations in `evidence/m5-rollout.md`) (project-meta's own, PR #2526, merged `15cfecacd` after its full-suite failures were matched against unmodified main). The daily check gained durable-set findings (project-meta PR #2529, merge `d0bf845`) and reports `durable=ok(0)` on every rolled-out main. Next: on or after 2026-10-25 read the disproof sample (`evidence/m5-disproof-sample.md`).

**Previous update:** 2026-10-10, M3 merged: company-planning PR #109 (merge `7c79e5c`, Plan #61) ships the check and schema in the plugin (`plugins/company-planning/scripts/durable_docs_check.py`, `plugins/company-planning/contracts/durable-documents/durable_documents.v0_1.schema.json`), the adoption-gate overlay `OV-DURABLE-DOCS-DECLARED` (bounded-design@12), quick-adopt `--durable-doc`, the completion step and PMI-018; full suite 927 passed. The checker, schema and tests that were in this folder moved there (this folder keeps only the design and its M2 evidence). Next: M4, the two pilots declare the block and fill their durable documents.

**Why now.** A survey of 36 repositories active in the last two weeks (2026-10-10, `git ls-files` by path) found about 3,300 plan files and about 600 decision records, but requirements documents in 2 repositories, a system model (`docs/model/ODD.md`) in 8 and `.aes/target.yaml` in 4. Plans record each change and are never folded back into anything a reader can trust as current. Company Planning makes a PRD optional (`landscape-review/SKILL.md:74`), never asks for decision records, and has no completion step for quick-adopted plans.

## Actor and result

**Actor:** an agent (or Brian) who starts work in a governed repository and needs the goal, the requirements, a rule and its reason; and the agent finishing a plan, who must leave those documents current.

**Result:** each governed repository declares its durable set in `.agentic/repo.yaml`; each document holds a fixed minimum; every plan states which durable documents it updates; completion verifies it.

**Example (stable, user-visible):** the canonical example in the front matter. Today the same question in company-planning needs a search across `docs/plans/` (about 175 plan files) and the skills; after the change the reader opens `wiki/index.md` -> System model -> `RULE-ADOPT-GATE`, which names its owner (`scripts/method_conformance/gate.py`), its test, and the decision record that says why.

### The durable set (the design this plan adopts)

Section names follow arc42, the standard architecture-documentation template, so readers meet known headings. Nothing here is a new document type except the goal page; each row extends what already exists.

| Role | What it must hold (minimum) | Home (default; repo.yaml may repoint) | Existing owner it extends |
|---|---|---|---|
| Goal and thesis | north star (the outcome steered toward); thesis (the bet on why this approach gets there); what would disprove the thesis; non-goals; lineage (the repository it replaces and why it was restarted, or none) | `docs/architecture/GOAL.md` (AES repositories: it links `.aes/target.yaml` `outcomes` as the north star) | target.yaml `outcomes` (AES); roadmap north star (initiative-roadmap) |
| Requirements | each requirement has an ID, a success criterion and a disproof condition | `.aes/target.yaml` where present, else `docs/architecture/REQUIREMENTS.md` | target.yaml `normative_items` and `success_criteria` |
| System model | ODD shape: entities (domain model), processes with their rules, records with writers (data flow), views; every entity, rule and process has an ID; each rule names exactly one owner (file or component), at least one check, and the decision record that explains it where one exists | `docs/model/ODD.md` (+ machine-readable twin) | Company Planning system model (PMI-017, `distribution/references/system-model.md`) and its traceability view (`architecture-views.md:40`) |
| Schema and contracts | not a separate document: the model's rules and records point at the code-level schema and contract files by path | inside the system model | drift test of PMI-017 |
| Decisions | one record per accepted decision, each naming the rule or component IDs it governs and a wrong-when condition | `docs/decisions/` | `.agentic/repo.yaml` `decision_roots` |
| Glossary | generated from the model's entity and rule names; never hand-maintained | generated | none (deferred, see R6) |
| Plans | temporary; each names its durable-document delta; archived after completion | `docs/plans/` | Company Planning plans |

**Sizing, "within reason":** a Trivial change (AES commit rule) declares nothing. A Small plan (`quick-adopt`) carries one line, `Durable documents: <role>#<ID>, ...` or `Durable documents: none -- <reason>`. A full plan carries a delta table (role, ID, change). A repository may mark a role `not_applicable: <reason>` in repo.yaml (for example a notes vault has no data flow); the system model keeps PMI-017's only exemption.

## Requirements

Status for all: planned, not yet run, unless stated.

| ID | Requirement (asked for, or implied by the work's claims) | Check that verifies it | Status |
|---|---|---|---|
| R1 | `.agentic/repo.yaml` gains a `durable_documents` block naming each role's path or `not_applicable: <reason>` | `durable_docs_check.py` validates the block against company-planning `plugins/company-planning/contracts/durable-documents/durable_documents.v0_1.schema.json` | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42` |
| R2 | The goal document holds north star, thesis, thesis disproof and non-goals | checker: each field present and non-placeholder | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42` |
| R3 | Every requirement has an ID, a success criterion and a disproof condition | checker; for AES repos `aes plan validate` already enforces this | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42` |
| R4 | Every system-model rule has an ID, exactly one owner path that exists, at least one check path that exists, and every process names the rules it enforces | checker trace pass over the trace file (`docs/model/trace.yaml`) | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42` |
| R5 | Every decision record names the rule or component IDs it governs, and each ID resolves | checker | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42` |
| R6 | Glossary generated from the model | generator diff | deferred: derived convenience; no reader question in the canonical example needs it; picked up at M5 if cold readers stumble on vocabulary |
| R7 | Every adopted plan (full and quick) carries a Durable documents section or line naming role#ID entries or `none -- <reason>` | new Company Planning checklist item `CORE-DURABLE-DOCS` in the adoption gate; `quick-adopt --durable-doc` flag | planned |
| R8 | Completion refuses a plan whose declared documents did not change in the plan's commit range, and refuses `none` without a reason | `durable_docs_check.py --plan <id> --range <base>..<head>` called from execute-plan-loop step 4 and from the repository's `make check` on the plan's branch | planned |
| R9 | A durable document is reported stale when files its rules name as owners changed after the document's last commit | checker staleness pass (git log per path) | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42` (staleness pass included) |
| R10 | The daily documentation check reports durable-set findings per repository and keeps one concern open while any governed repository fails | project-meta `scripts/md_file_cap.py` extension | done 2026-10-11: project-meta PR #2529 (`md_file_cap.py` prints `durable=status(n)`; `workspace_map_alert.py` keeps one concern open) |
| R11 | The rule is presented as following arc42 headings; the documents use arc42 section names for goal, context, runtime (data flow), decisions and glossary | checker heading check on GOAL.md and REQUIREMENTS.md | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42` |
| R12 | A feedback path exists: PMI entry with a wrong-when condition in `docs/PLANNING_METHOD_FEEDBACK.md` | file review in the M3 pull request | passing: PMI-018 in company-planning PR #109 |
| R14 | (added 2026-10-10 from the fol-operational-metamodel lineage study: most of Brian's project restarts record no reason, and purpose and finish lines arrive late) A repository that replaces an earlier one has a "Lineage (AES extension)" field in its goal document naming the predecessor repository and why it was restarted (what the predecessor could not do); an original repository says `Lineage: none -- original` | `GOAL-NO-LINEAGE` in the plugin's `durable_docs_check.py` with a seeded-defect test at M4 | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42`; company-planning says `none -- original`, AES canonical names Inside-Success/agentic-engineering-system |
| R13 | (added 2026-10-10, AES-CTX-004 "Truth lives where it is edited", Decision 0013, landing from branch `edit-site-authority`) Every reader document in the durable set carries a non-placeholder `description` front-matter line, and the repository's wiki catalog is generated from those lines, never hand-maintained; `durable_docs_check.py` reports a missing or placeholder description; the goal document's thesis cites AES-CTX-004 | three checks added to the plugin's `durable_docs_check.py` at M4, each with a seeded-defect test: `DOC-NO-DESCRIPTION` (a durable reader document lacks a non-placeholder `description`), `CATALOG-STALE` (the existing generator, enforced-planning `python -m enforced_planning.docstring_wiki --repo-root . --check`, wrapped in AES canonical as `make docstring-wiki-check`, exits non-zero; that generator gains front-matter `description` as its first summary source, a change the edit-site-authority lane is making in enforced-planning, so no second catalog generator is built), and `GOAL-NO-CTX-004` (the goal document's thesis does not cite AES-CTX-004) | passing on both pilots' main: `evidence/m4-company-planning-check.txt` (fc3d5b7) and `evidence/m4-aes-canonical-check.txt` (3e1eff078), zero findings with `--arc42`; the checks landed in company-planning PR #113 |

**Deferred requirements carried forward:** R6 (generated glossary) is deferred; every completion record this plan names (each milestone row's completion note, `evidence/m4-<repo>-check.txt`, `evidence/m5-disproof-sample.md`, and the M3 pull request description) carries the line `Deferred: R6 generated glossary -- no reader question needs it yet`.

## Success and disproof

**Success evidence (each tests the claimed property directly):**

1. **Refusal works.** Negative control A: a plan without the Durable documents section is run through `cli.py adopt` and refused, naming `CORE-DURABLE-DOCS`. Negative control B: a plan declaring `system_model#RULE-X` whose commit range does not touch the model is run through `durable_docs_check.py --plan` and refused, naming the document and ID. Each control is then fixed and passes. This tests the property (completion depends on the declared update), not a count.
2. **The documents answer the question.** A fresh agent (Haiku, no prior context) in each pilot answers the canonical question; the answer cites rule ID, owner file, check and decision record, and every cited file was opened in its tool calls.
3. **Pilots clean.** `durable_docs_check.py` reports zero findings on each pilot's main, and was shown to report each finding type at least once on a seeded defect (owner path missing, check path missing, unresolvable decision link, stale document).

**Disproof (the approach is wrong if):** two weeks after M4, in a sample of the 10 most recent completed plans across the pilots, five or more declare `none`, or their durable-document diffs are mechanical (only IDs, dates or links changed, read by a person or agent from the diff); or the cold reader fails the canonical question on a checker-clean pilot. Either outcome means the rule produces paperwork, not current documents; the PMI entry then records the finding and the rule is revised or withdrawn.

**Trace review.** Each criterion is judged from the full output of a named run, saved in this folder under `evidence/`:

- Negative controls: `evidence/m3-negative-controls.txt`, the exact commands, full stdout and stderr, exit codes. Must show the refusal message naming the item or document and ID, then the passing re-run on the fixed plan.
- Checker on pilots: `evidence/m4-<repo>-check.txt` with the command, revision and every finding by ID; the seeded-defect runs `evidence/m2-seeded-<type>.txt` must show the specific finding for the seeded element.
- Cold reader: `evidence/m4-<repo>-cold-reader.json`, the session id and every tool call with arguments and results. Must show the path from `wiki/index.md` to each cited file and the files actually opened, not only the final answer.

- Disproof sample (run two weeks after M4): `evidence/m5-disproof-sample.md`, produced by one agent session whose transcript id is recorded at its top. It lists the 10 most recent completed plans across the pilots, each with its plan id, its declared durable-documents line, the exact commit range and the `git diff --stat` plus the full diff of each declared document, and the reader's classification per plan (real update, mechanical, or `none`) with the diff lines that support it; then the cold-reader re-run's json path. What must be seen beyond the tally: the diff lines for every plan classified as a real update.

This shaping milestone (M0) itself is a pure document edit with no run; that exemption is the reason it has no trace review. Its evidence is the adoption records written by `cli.py adopt` beside this plan: `proposals/aes-durable-docs/PLAN.receipt.json` and `proposals/aes-durable-docs/PLAN.adoption-decision.json`, committed on branch `shaping/aes-durable-docs`.

## When a run fails or surprises us

1. Keep the failed run: its saved output file and session or trace id stay committed; never overwrite it.
2. Read everything before choosing a fix: the full command, inputs (the plan file, the repo.yaml block, the model twin), each tool call and its arguments and results, intermediate checker output, and the final verdict.
3. Cite the divergence: the exact line where observed output departs from what this plan expects.
4. Classify it: evidence never came back (the checker did not read the file), evidence came back and went unused or was contradicted (it read the file and judged wrongly), the expectation is invalid (the plan or a test question is wrong), or unresolved.
5. Repair only with a resolved diagnosis: an unresolved case permits more investigation, not a causal fix. Link the targeted repair to a new run saved beside the original, which stays.
6. Review completeness is recorded separately from the run verdict: a reviewed failure can satisfy a diagnosis step, never a passing criterion.

## System model

Model: Company Planning's system model, `company-planning/docs/model/ODD.md` (reachable from company-planning `wiki/index.md`), scope: the planning method's adoption and completion processes, which this work changes. AES canonical's governed model is `.aes/target.yaml` plus `docs/architecture/greenfield-v0.2/`; this plan changes neither (see AES target).

Elements this work adds, changes or relies on, and what the examined run must show of each:

| Element | Kind | Change | What the examined run must show |
|---|---|---|---|
| Plan adoption (gate) | process | changed: new item `CORE-DURABLE-DOCS` | negative control A's output names `CORE-DURABLE-DOCS` as the refusing item |
| Plan completion | process | changed: calls the durable-docs check | negative control B's output names the undeclared-change document and ID |
| Durable documents declaration (`durable_documents` in repo.yaml) | entity | added | checker output lists each role with its resolved path |
| Durable-document delta (plan section) | record, writer: the plan author; read by the gate | added | the gate's observation for `CORE-DURABLE-DOCS` cites the plan section |
| System-model rule (ID, owner, check, decision) | entity | changed: gains ID and link fields | checker output lists each pilot rule with owner and check resolved |
| Durable-docs check report | view (CLI output) | added | every finding line names role, ID and file |

Source-linked views (from Company Planning `distribution/references/architecture-views.md`), each generated from or linked to its source:

- Data and state: the durable-set diagram on `proposals/aes-durable-docs/review-page/index.html`; its source is the durable-set table in this plan and, from M1, company-planning `plugins/company-planning/contracts/durable-documents/durable_documents.v0_1.schema.json`.
- Interactions and transitions: adopt -> work -> complete, sourced from `skills/execute-plan-loop/SKILL.md` steps 1-4 and `scripts/method_conformance/gate.py` (adoption) and `quick.py` (quick plans); drawn on the same review page.
- Requirement-to-verification: the Requirements table above (requirement -> check -> status), source-linked to each check's file.
- Deployment: omitted, nothing is deployed.

Freshness and drift checks, by name: Company Planning's existing model drift test `company-planning/tests/test_system_model.py` (compares the model with the code in both directions) must pass with the new process and record elements added in M3; the new `durable_docs_check.py` is the drift check for the durable set itself (R4, R5, R9); and the review page is regenerated from its sources in the same change whenever the table or schema changes, with a test that fails if the page's element list differs from the schema's roles.

Reconciliation: Company Planning's `docs/model/ODD.md`, `docs/model/VIEW_COVERAGE.md` and `tests/test_system_model.py` are updated in the same M3 pull request that changes adoption and completion; that pull request's full check output is saved as `evidence/m3-company-planning-check.txt`.

## Capability reuse

No catalogue entry fits, because the capability catalogue (`agentic-capability-architecture-canonical`: `reuse_candidates.yml` holds `approval_action_workflow`, `twitterapi_io_search_candidates_wrapper`, `documents_to_text`; `capability_registry.yml` holds `core`, `approvals`, `notifications`, `scheduling`) has no documentation, traceability or planning entry, and this work needs a document-set contract and a plan-to-document trace check. New capability: the durable-documents check (`durable_docs_check.py`); first consumer: Company Planning's completion step in execute-plan-loop, run on the company-planning pilot.

## Authority and non-goals

**Authority:** Brian (quoted above) over the rule; Company Planning owns planning obligations (system-model reference: "Company Planning owns these planning obligations; repositories own their models and implementation"); each repository owns its documents; AES canonical owns the `.agentic/repo.yaml` layout contract.

**Non-goals:**

- Rewriting or summarising existing plans into the durable documents in bulk; pilots fill their documents from current code and decisions, and old plans stay as history.
- A company-wide ontology or shared glossary (PMI-017: "Never one company-wide ontology").
- Replacing `.aes/target.yaml`, ADR practice or the ODD model with a new format.
- Adopting StrictDoc, Doorstop or sphinx-needs (see Prior art).
- Hosted CI; checks run locally.
- Repositories other people or organisations own.
- Changing `enforced-planning/scripts/complete_plan.py` while the Codex trace-review lane holds it.
- Changing `.aes/target.yaml` (including a `thesis` field); that would be a separate AES plan.

## Irreversible actions and spend

No irreversible action is proposed. Two actions are recorded here with boundary, authority and containment:

| Action | Boundary | Who authorizes | Containment |
|---|---|---|---|
| Model spend: cold-reader runs and the adoption gate's semantic verifier | OpenRouter through the shared `llm_client`, Brian's configured route | Brian's standing authorization for normal agent model use (workspace AGENTS.md, "Default provider-unspecified LLM work to Brian's configured OpenRouter route"); no further approval needed at this size | Haiku only for cold readers; at most 4 cold-reader sessions (two pilots, one retry each), each bounded by `max_turns=30`, no timeouts or token caps; every call carries this plan id and is logged in the shared client's `calls_<date>.jsonl`; expected total under one US dollar; anything beyond 4 sessions comes back to Brian first |
| Git changes: commits and merges in AES canonical, company-planning and the two pilots | each repository's main branch | Brian's standing merge rule (workspace AGENTS.md: merge after the repository's local checks pass, no per-merge yes) | one pull request per milestone, merged with a merge commit after `make check`; reverted with `git revert`; nothing published, deleted or sent outward |

## Uncertainties

Material uncertainties. These five are the complete set; each could make the approach fail its purpose.

| Material uncertainty | Owner | Evidence that resolves it |
|---|---|---|
| Rule IDs in Markdown plus a machine-readable twin is enough for the trace check without a requirements tool | this plan's owner (claude-code, shaping-aes-durable-docs) | M2: the checker resolves every pilot rule's owner, check and decision; if more than one pilot needs queries the twin cannot express (impact analysis across repositories), switch to StrictDoc |
| Plans will declare real updates rather than `none` | this plan's owner | the disproof sample two weeks after M4 |
| The completion hook covers quick-adopted plans, which have no loop completion event | this plan's owner | M3: negative control B run on a quick-adopted plan through `make check` on its branch |
| The Codex trace-review lane's completion changes and this plan's completion check compose | integration owner (this plan's owner), with the Codex lane | M3: the lane's merged state is rebased onto and both checks run in one completion; message sent before M3 starts |
| A goal page per repository is not redundant with the roadmap's north star | this plan's owner | M4 cold reader: if the roadmap already answers the thesis question in both pilots, GOAL.md becomes a pointer to it |

## Activation facts

Declared: `shared_mechanism=true` (a new document contract and check shared by every governed repository), `empirical_comparison_proposed=false` (no comparison of alternatives is run; StrictDoc is a fallback chosen by a stated trigger, not a bake-off), `llm_central=false` (the check this plan builds, `durable_docs_check.py`, is deterministic and makes no model call; the adoption gate's semantic verifier is existing Company Planning machinery that judges this plan like any other, not something this plan builds or changes; the cold reader verifies the result, it is not the mechanism), `irreversible_or_spend_action=true` (the plan spends on model calls; no irreversible action; see Irreversible actions and spend). `claims_external_standard`: the documents use arc42 section names (R11), arc42 being an external template; declared true so its checks apply. `aes_governed_target`: AES canonical is governed by `.aes/target.yaml`; declared true.

## Prior art and ownership

**What was searched (2026-10-10):** existing ownership: Company Planning's nine skills and `distribution/references/` (grep for PRD, ADR, domain model, ontology, glossary, thesis, north star, system model), AES canonical's `.agentic/repo.yaml`, `.aes/target.yaml` and `proposals/`, and the capability catalogue; internal lineage: enforced-planning `adr/0005-hierarchical-context-compression.md`, AES `research/synthesis/2026-09-28-legacy-idea-harvest/enforced-planning.md:62`, the agent_ecology2 visualisation, the brownfield-docs plan, and the cross-repo ideas register `vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md` (grep for doc, drift, coupling, staleness, trace); external prior art: arc42, C4, SysML requirement relations, and a web search comparing StrictDoc, Doorstop and sphinx-needs.

**Disposition of each candidate found:**

| Candidate | Where | Disposition | Reason |
|---|---|---|---|
| Company Planning system model (PMI-017, ODD shape, drift test, VIEW_COVERAGE) | company-planning `distribution/references/system-model.md`, Plan #55 | extend | already required and adoption-gated; gains rule IDs with owner, check and decision links |
| Traceability view (requirement, operation, contract, check, observation) | company-planning `architecture-views.md:40` | reuse | the R4 and R5 links are this view made checkable |
| `.aes/target.yaml` outcomes, normative items, success criteria with disproof | AES canonical | reuse as the requirements role; extend with `thesis` | stronger than a PRD; already validated by `aes plan validate` |
| `.agentic/repo.yaml` layout contract and brownfield layout (decisions, architecture, plans roots) | AES canonical, `proposals/aes-brownfield-docs` | extend | adds `durable_documents`; layout check stays the owner of folder placement |
| `relationships.yaml` typed links and the context packet | enforced-planning `context_packet.py`, used in AES canonical | compose | the durable set becomes a routing target for edit context; no change to the packet |
| META-ADR-0005 hierarchical context compression | enforced-planning `adr/0005-…`, agent_ecology2 visualisation | supersede in part | its layer list is replaced by this set; its staleness-as-cache-invalidation rule is adopted as R9 |
| Daily documentation check | project-meta `scripts/md_file_cap.py` | extend | gains durable-set findings at M5 |
| Executable doc-coupling declarations (ideas register, "Executable doc-coupling declarations keep documentation from drifting off source") | enforced-planning doc-coupling (Pattern #10) | compose | R9 staleness reads the rule-to-owner links the same way coupling reads doc-to-source links; no second coupling store |
| Doc-role type system (ideas register, "Doc-Role Type System with Mechanical Enforcement") | project-meta `scripts/doc_lint.py` | supersede for durable roles | roles are declared once per repository in repo.yaml instead of a header on every file; doc_lint stays for project-meta's own vision documents |
| Rules authored once, generated into docstrings (ideas register) | ideas register entry, line 127 | bounded exception (later) | attractive for R4 but needs a generator per language; revisit after M4 if owners drift from the model |
| Span-precise staleness propagation (ideas register) | ideas register entry, line 1374 | bounded exception (later) | file-level staleness is enough for R9 at pilot scale; adopt if file-level reports more than 20% false stale findings on a pilot |
| arc42 | arc42.org | reuse (section names) | the standard architecture template; goals, context, runtime view, decisions, glossary map directly |
| C4 model | c4model.com | bounded exception | diagrams by zoom level; views stay chosen by question under `architecture-views.md`, not by C4 level |
| StrictDoc, Doorstop, sphinx-needs | strictdoc.readthedocs.io; Doorstop on PyPI; sphinx-needs | bounded exception (not adopted now) | each is a requirements store with its own format, which would be a second authority beside target.yaml; StrictDoc's source traceability is still labelled experimental in its own guide; adopt StrictDoc if the M2 trigger fires |
| SysML requirement relations (satisfy, verify, refine) | OMG SysML | reuse (vocabulary only) | link names for R4 and R5 |

**Parallel-implementation check:** the checker fails if a repository declares a durable role and a second file of the same role exists outside the declared path (for example a `REQUIREMENTS.md` beside `.aes/target.yaml`, or a second `ODD.md`), and the daily check at M5 reports any repository whose requirements live in more than one declared place.

## Coordination

| Work unit | Owner | Writes | Depends on | Evidence |
|---|---|---|---|---|
| M0 shaping | claude-code, claim `shaping/aes-durable-docs` (AES canonical, write path `proposals/aes-durable-docs`) | this folder | none | adoption receipt |
| M1 contract | same | `.agentic/repo.yaml` schema in AES canonical (`docs/architecture/`), this folder | M0 | schema plus validation of both pilots' blocks |
| M2 checker | same | built here, moved at M3 to company-planning `plugins/company-planning/scripts/durable_docs_check.py` with its tests | M1 | seeded-defect runs |
| M3 Company Planning wiring | same, new claim in company-planning | `skills/bounded-design`, `skills/execute-plan-loop/SKILL.md` step 4, `scripts/method_conformance/` (checklist item, `quick-adopt` flag), `distribution/references/`, `docs/PLANNING_METHOD_FEEDBACK.md`, its model and VIEW_COVERAGE | M2; reconciliation with the Codex lane | negative controls |
| M4 pilots | same | company-planning and AES canonical durable documents | M3 | checker clean, cold reader |
| M5 rollout | same, one PR per repository, Haiku for per-repository inventory | each repository; project-meta `md_file_cap.py` | M4 | daily check |

**Concurrent writers and conflict surfaces** (from `check_coordination_claims.py --check --project <name>`, 2026-10-10):

| Writer (claim) | Owner | Its write paths | Expiry | Conflict surface with this plan | Dependency and order | Work-unit evidence |
|---|---|---|---|---|---|---|
| `company-planning:trace-review-provider-guards` | Codex session | `.company-planning/active-execution.json`, `.company-planning/history`, `artifacts/trace_review/reviews`, `proposals/trace-review-enforcement` | 2026-10-11T06:18Z | none by file; both change what completion requires | M3 lands after this lane merges or expires; completion runs trace review first, durable-docs check second | its claim record and merged PR (company-planning #104 merged 2026-10-09 for the same goal) |
| `enforced-planning:trace-review-guards` | Codex session | 25 paths including `scripts/complete_plan.py`, `enforced_planning/trace_review_provider.py`, `scripts/coordination_hook.py`, `wiki/index.md` | 2026-10-11T06:34Z | `scripts/complete_plan.py` is enforced-planning's completion seam; this plan does not edit it | no dependency; if a later milestone needs it, a new claim is taken after this one ends | its claim record |
| AES canonical `commit-rule-emergency-gaps` | Claude Code session | `src/agentic_engineering_system/commit_rule.py`, `tests/greenfield/test_commit_rule.py`, `proposals/aes-planning/rollout/install_everywhere.py`, `proposals/aes-planning/ROLLOUT.md`, `proposals/commit-rule-emergency-gaps` | active | none (this plan writes only `proposals/aes-durable-docs`) | none | its claim record |

Before M3 the integration owner sends the Codex company-planning lane (ListAgents, then SendMessage) the M3 file list and the completion order above, and records the message and reply as `evidence/m3-coordination.md`.

**Integration owner:** this plan's owner (claude-code, claim `shaping/aes-durable-docs`), who merges each pull request after the repository's local checks.

## Contracts and dependencies

**System boundaries crossed (the complete list):**

1. B1 AES canonical layout contract -> each governed repository (repo.yaml block).
2. B2 plan author -> Company Planning adoption gate (plan section, `quick-adopt` flag).
3. B3 Company Planning completion -> `durable_docs_check.py` (call and exit status).
4. B4 `durable_docs_check.py` -> each repository's git history and files (read only).
5. B5 project-meta daily check -> each repository (read only, M5).
6. B6 cold-reader agent -> OpenRouter through `llm_client` (model calls).

**Schemas and contracts crossed:**

| Boundary | Contract | Owner | File or URL | Changed here |
|---|---|---|---|---|
| B1 | Repository layout (`.agentic/repo.yaml`, schema 0.1-pilot) | AES canonical | `.agentic/repo.yaml`; schema company-planning `plugins/company-planning/contracts/durable-documents/durable_documents.v0_1.schema.json` | yes: adds `durable_documents` |
| B2 | Plan checklist profile (`bounded-design@5`) and adoption gate | Company Planning | `plugins/company-planning/contracts/method-conformance/profiles/bounded-design.v1.json`; gate `plugins/company-planning/scripts/method_conformance/gate.py` | yes: adds `CORE-DURABLE-DOCS` (profile version bump) |
| B3 | Durable-docs check CLI (arguments, exit codes 0 clean, 1 findings, 2 invalid input; one finding per line naming role, ID, file) | Company Planning (since M3) | company-planning `plugins/company-planning/scripts/durable_docs_check.py` | yes: new |
| B4 | git plumbing (`git log`, `git diff --name-only <range>`, `git ls-files`) | git | https://git-scm.com/docs | no |
| B5 | daily check report format | project-meta | `scripts/md_file_cap.py` | yes at M5: adds durable-set findings |
| B6 | shared LLM client call contract (`call_llm_structured`) | llm_client | `BrianMills2718/llm_client`, file `llm_client/core/client.py` (https://github.com/BrianMills2718/llm_client/blob/main/llm_client/core/client.py) | no |
| B2 | `quick-adopt` plan text | Company Planning | `plugins/company-planning/scripts/method_conformance/quick.py` | yes: `--durable-doc` flag writes the line |
| B3 | Execution cursor and completion | Company Planning | `plugins/company-planning/scripts/manage_plan_execution.py`, `plugins/company-planning/skills/execute-plan-loop/SKILL.md` | yes: step 4 calls the check; cursor schema unchanged |
| B1 | System model shape (ODD, twin) | Company Planning | `plugins/company-planning/distribution/references/system-model.md` | yes: rule ID and link fields |
| B1 | AES target | AES canonical | `.aes/target.yaml` | no (thesis field deferred to a later AES plan through `aes plan`) |
| B3 | `TraceReviewV1` | Company Planning (Codex lane active) | schema `plugins/company-planning/contracts/execution-loop/trace-review.v1.schema.json`, validator `scripts/validate_trace_review.py` | no |

**Producer and consumer of each contract:**

| Boundary | Contract | Produced by | Consumed by |
|---|---|---|---|
| B1 | `durable_documents` block and its schema | each repository's maintainer writes the block; AES canonical owns the schema | `durable_docs_check.py` (M2), project-meta daily check (M5) |
| B1 | System model shape (ODD, twin, rule links) | each repository's model author, following Company Planning's reference | `durable_docs_check.py` R4, Company Planning's `tests/test_system_model.py` |
| B1 | AES target | AES canonical through `aes plan` | `durable_docs_check.py` reads it as the requirements role (read only) |
| B2 | Plan checklist profile and `CORE-DURABLE-DOCS` | Company Planning (`bounded-design.v1.json`) | `gate.py` during `cli.py adopt` and `quick-adopt` |
| B2 | `quick-adopt` durable-documents line | `quick.py` when an author passes `--durable-doc` | `gate.py` (adoption), `durable_docs_check.py --plan` (completion) |
| B3 | Execution cursor and completion step | `manage_plan_execution.py`, the executing agent | the native Stop gate and the supervisor's `--event complete` |
| B3 | Durable-docs check CLI | `durable_docs_check.py` | execute-plan-loop step 4; each pilot's `make check` |
| B3 | `TraceReviewV1` | executing agent, validated by `validate_trace_review.py` | completion boundary (unchanged; runs before the durable-docs check) |
| B4 | git plumbing | git in each repository | `durable_docs_check.py` (staleness R9 and the plan range check R8) |
| B5 | daily check report | `md_file_cap.py` | the concern opened by `concern_issue.py`, read by the agent that works it |
| B6 | `call_llm_structured` | `llm_client` | the cold-reader harness (M4) and the adoption gate's semantic verifier |

**Landing order:**

1. M1 schema lands first (producer: AES canonical; consumers: the checker, later the daily check). Nothing reads it yet, so nothing breaks.
2. M2 checker lands next, reading the schema; run only by hand on the pilots.
3. M3 lands the gate item and completion call in one Company Planning pull request, with the profile version bump. Plans adopted before the bump keep validating against `bounded-design@5`; only new adoptions see `CORE-DURABLE-DOCS`, so no in-flight plan breaks.
4. M4 fills the pilots' documents and turns the completion check on there.
5. M5 extends the daily check to report, then turns on refusal per repository as each one is filled.

## Standard conformance

**Standard claimed (arc42):** arc42, the architecture-documentation template (arc42.org, template version 8). The work claims only that its goal, requirements and system-model documents use arc42's section names for the sections they cover; it does not claim a full arc42 document.

**Machine-readable rules:** arc42 publishes none; it publishes a written template. The check encodes these written rules instead: (1) `GOAL.md` carries the heading "Introduction and Goals" with sub-headings "Requirements Overview", "Quality Goals" and "Stakeholders" or a line `not_applicable: <reason>` under each; (2) where a repository documents context, data flow or decisions in the durable set, the headings are "Context and Scope", "Runtime View" and "Architecture Decisions"; (3) the generated glossary is headed "Glossary"; (4) arc42 section numbers, when used, match the template's numbering (1 Introduction and Goals, 3 Context and Scope, 6 Runtime View, 9 Architecture Decisions, 12 Glossary).

**Extensions, labelled as extensions:** the thesis, the thesis disproof, rule IDs with owner, check and decision links, and the `durable_documents` block are AES additions, not part of arc42. Each document marks them under a heading or front-matter key ending "(AES extension)", and this plan presents them only as such.

**Gate:** `durable_docs_check.py --arc42` tests these rules on every durable document; it runs in each pilot repository's `make check`, which is that repository's merge gate (workspace rule: local checks are the merge gate), and in the daily check at M5. **Disproof (added to the plan's disproof):** a document labelled as using arc42 section names violates one of the four rules above, or an AES extension appears without its "(AES extension)" label.

## AES target

AES canonical is governed by `.aes/target.yaml`; this plan changes none of it. Its work lives under `proposals/` (outside the governed roots `src/agentic_engineering_system/` and `tests/greenfield/`) and in company-planning and the pilot repositories. Requirements served, each with its existing verification subject:

| Plan requirement | Target normative item | Target success criterion | Verification subject |
|---|---|---|---|
| R3, R7 | `GF-REQ-002` (accepted normative obligations with success and disproof semantics before implementation) | `SC-GF-002` | `VS-GF-RECORDS` |
| R4, R5 | `GF-REQ-005` (the working context carries the full applicable meaning with provenance) | `SC-GF-005` | `VS-GF-CONTEXT-STRUCTURAL` |

The other requirements serve no AES target normative item or success criterion, because they change Company Planning and the pilot repositories, which the target does not govern. Each is verified by its own named check, not an AES verification subject:

| Plan requirement | Target item | Verification (not an AES subject) |
|---|---|---|
| R1 | none | `durable_docs_check.py` schema validation |
| R2 | none | `durable_docs_check.py` goal-field check |
| R6 | none (deferred) | generator diff, at M5 if picked up |
| R8 | none | `durable_docs_check.py --plan --range` and negative control B |
| R9 | none | `durable_docs_check.py` staleness pass, seeded-defect run |
| R10 | none | project-meta daily check output (`evidence/m5-rollout.md`) |
| R11 | none | `durable_docs_check.py --arc42` |
| R12 | none | review of the PMI entry in the M3 pull request | This plan declares no target delta, so it has no `aes plan validate` result to give. Adding a `thesis` field to the target is outside this plan (see Non-goals); for AES-governed repositories the goal role points at `docs/architecture/GOAL.md` until a separate AES plan decides otherwise.

## Durable documents

Durable documents: goal, system_model#RULE-DEPENDENCY-CHANGE-STALES, system_model#RULE-PLAN-ADOPTED-FOR-COMMIT, decisions

All three roles are declared in AES canonical's `.agentic/repo.yaml` `durable_documents` block (`goal: docs/architecture/GOAL.md`, `system_model: {prose: docs/model/ODD.md, trace: docs/model/trace.yaml}`, `decisions: docs/decisions/`; the block also declares `requirements: .aes/target.yaml`, `plans: docs/plans/`, a `catalog` check, and `glossary` as not_applicable), and `durable_docs_check.py --repo .` validates that block against the schema with zero findings (`evidence/m4-aes-canonical-check.txt`). In AES canonical this plan writes `docs/architecture/GOAL.md` (goal), `docs/model/ODD.md` and `docs/model/trace.yaml` (system model) and a `description:` and `Governs:` line on each of `docs/decisions/0001`-`0013` (decisions), all at M4. Company-planning's half (its own GOAL, trace and decision records) is governed by company-planning Plan #63 there. Completion check, required to exit 0: `durable_docs_check.py --repo . --plan proposals/aes-durable-docs/PLAN.md --range 23e413a2c..HEAD` (23e413a2c is this plan's adoption commit).

## Milestones

| Milestone | Output | Promotion trigger |
|---|---|---|
| M0 Shape and adopt | done 2026-10-10: this plan, adopted (`PLAN.receipt.json`); review page with the durable-set diagram | adoption receipt |
| M1 Contract | schema done 2026-10-10; it now lives in the Company Planning plugin (`contracts/durable-documents/durable_documents.v0_1.schema.json`) so every installed consumer validates against the same copy; AES canonical's `.agentic/repo.yaml` contract points to it at M4 | schema test passes |
| M2 Checker | done 2026-10-10: `durable_docs_check.py`, 25 seeded-defect tests pass, every finding type shown (`evidence/m2-seeded-defects.txt`, one file for all seeded runs) | all seeded runs show their finding |
| M3 Company Planning wiring | done 2026-10-10: company-planning PR #109 (Plan #61); controls in `plugins/company-planning/docs/evidence/method-conformance/canonical-probe/durable-{no-block,undeclared,unchanged}.txt` there | both negative controls recorded |
| M4 Pilots | done 2026-10-11: company-planning and AES canonical documents filled and clean (`evidence/m4-*-check.txt`, `evidence/m4-*-cold-reader-review.md`). Deferred: R6 generated glossary -- no reader question needs it yet | checker clean plus cold reader |
| M5 Rollout | rollout done 2026-10-11: 22 of 22 repositories merged; daily check reports durable findings (`evidence/m5-rollout.md`). Disproof sample due on or after 2026-10-25; resume event: the first session on or after that date reading this line | disproof sample read two weeks after M4 |
