---
schema_version: "1.0"
artifact_type: design_plan
id: shaping-nav-preflight
plan_id: shaping-nav-preflight
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/shaping-nav-preflight.receipt.json
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "A [Shaping <id>] commit that adds a new proposal document may also add link lines into proposals/<id>/ in existing Markdown pages or create the first wiki/index.md, so one commit lands the proposal and its navigation; and 'aes commit check --preflight -m <message>' reports the commit rule's verdict on the staged change without logging, before any commit is attempted"
  canonical_example: "In a Brian-owned repo with wiki/index.md linking README.md, staging proposals/demo/plan.md plus one added README.md line '- [demo plan](../proposals/demo/plan.md)' and committing '[Shaping demo] draft' is refused today ('may touch only proposals/demo/'); after the change it is accepted, while the same commit that also rewrites another README.md line is still refused"
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, src/agentic_engineering_system/cli.py, tests/greenfield/test_commit_rule.py; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/greenfield/test_commit_rule.py, through real git commits and the installed commit-msg hook: (1) [Shaping demo] with the proposal plus an added navigation line in README.md is accepted (asserts the atomic route exists); (2) the same with a deleted or non-link line outside the folder, or a link to another proposal, is refused (asserts scope stays proposal-only); (3) a repo with no wiki/index.md accepts [Shaping demo] adding the proposal plus a new wiki/index.md of a heading and a link line (asserts the first-index bootstrap); (4) 'aes commit check --preflight -m \"[Shaping demo] x\"' on a staged unreached proposal exits 1 naming doc-reach and writes no commit-rule log line, and exits 0 once the link line is staged (asserts preflight equals the commit verdict without logging). The full test file passes. The check's full output on the parent commit and on the change commit is committed as docs/plans/shaping-nav-preflight.check.txt, and the commit is tagged [Goal shaping-nav-preflight] with an Asked: line quoting the request. python3 \"$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py\" --repo . --plan docs/plans/shaping-nav-preflight.md --range 6faebd3a257ac3ac8f8383233ea1045923be7b7b..HEAD exits 0 and its output is in the same file."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# A shaping commit can carry its own wiki link; the commit rule runs as a preflight

## When a run fails or surprises us

This procedure is separate from the anticipated failure named in the disproof
under Success and disproof: it applies to any run that fails or surprises us.
Preserve the failed check and its execution trace id. Before selecting a fix,
read the complete inputs, prompts, tool arguments/results, intermediate stages
and final output, including the full check command/output and the changed files.
Cite the observed divergence and classify evidence absent, returned but unused
or contradicted, invalid expectation, or unresolved. An unresolved diagnosis
cannot authorize a causal repair; it permits only further investigation. Bind the targeted repair to a new
traced verification run; retain the failed original. Review every failing or
surprising item and a sample of passes. A complete review is distinct from a
passing run. Criterion `outcome` covers the entire requested success check.

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-12 (weekly fix-owner run he set up) "For EACH item, read the issue and the linked problem issue, then choose exactly one disposition and carry it out" for AES canonical #531 and #532

**Desired result:** A [Shaping <id>] commit that adds a new proposal document may also add link lines into proposals/<id>/ in existing Markdown pages or create the first wiki/index.md, so one commit lands the proposal and its navigation; and 'aes commit check --preflight -m <message>' reports the commit rule's verdict on the staged change without logging, before any commit is attempted

**Stable example:** In a Brian-owned repo with wiki/index.md linking README.md, staging proposals/demo/plan.md plus one added README.md line '- [demo plan](../proposals/demo/plan.md)' and committing '[Shaping demo] draft' is refused today ('may touch only proposals/demo/'); after the change it is accepted, while the same commit that also rewrites another README.md line is still refused

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Requirements

| Id | Requirement | Source | Check | Status |
| --- | --- | --- | --- | --- |
| R1 | A [Shaping <id>] commit that adds a new proposal document may also add link lines into proposals/<id>/ in existing Markdown pages or create the first wiki/index.md, so one commit lands the proposal and its navigation; and 'aes commit check --preflight -m <message>' reports the commit rule's verdict on the staged change without logging, before any commit is attempted | asked: Brian 2026-10-12 (weekly fix-owner run he set up) "For EACH item, read the issue and the linked problem issue, then choose exactly one disposition and carry it out" for AES canonical #531 and #532 | the success check under Success and disproof, its output saved as `docs/plans/shaping-nav-preflight.check.txt` | planned, not yet run |
| R2 | Scope stays proposal-only: outside proposals/<id>/ only added Markdown lines that link into proposals/<id>/ (and headings in a newly created wiki/index.md) are admitted, never deletions or other content | stated with the request | refusal tests (2) in tests/greenfield/test_commit_rule.py | planned, not yet run |
| R3 | Shared mechanism: the commit rule runs in every repository's commit-msg hook machine-wide, so a wrong change could block or wrongly admit commits everywhere; the change only widens [Shaping] by navigation lines into its own folder and adds an opt-in --preflight flag that leaves the hook path unchanged | stated with the request | the full tests/greenfield/test_commit_rule.py suite (all existing hook tests) passes unchanged | planned, not yet run |
| R4 | Preflight never pollutes the commit-rule log the nightly effect count reads | stated with the request | test (4) asserts the day's commit-rule log has no new line after a preflight | planned, not yet run |
| R5 | Model freshness: docs/model/ODD.md ENT-COMMIT and PROC-COMMIT-CHECK rows still describe the behaviour after the change | stated with the request | grep -n 'ENT-COMMIT\|PROC-COMMIT-CHECK' docs/model/ODD.md docs/model/trace.yaml on the change commit, output appended to docs/plans/shaping-nav-preflight.check.txt | planned, not yet run |

Requirements the change's own claims imply are listed above as R2 onward.

## AES target

This repository is governed by an AES target (`.aes/target.yaml`). How R1 onward map to it:

- R1 -> AP-REQ-001 and SC-AP-001 (a correctly tagged [Shaping] commit is accepted by the installed hook); verification subject: the new Shaping-navigation tests (1) and (3) in tests/greenfield/test_commit_rule.py
- R2 -> AP-REQ-001 and SC-AP-001 (a commit outside its tag's scope is refused); verification subject: the refusal tests (2) in tests/greenfield/test_commit_rule.py
- R3 -> AP-REQ-001 and SC-AP-001 (the existing hook behaviour is unchanged); verification subject: the full tests/greenfield/test_commit_rule.py run
- R4 -> AP-REQ-001 and SC-AP-001 (the hook's verdict on a real commit is the one logged; a preflight reports the same verdict and logs nothing); verification subject: preflight test (4) in tests/greenfield/test_commit_rule.py
- R5 -> AP-REQ-001 and SC-AP-001 (the model rows describe the governed commit check); verification subject: the ODD.md/trace.yaml grep saved in the check file. Target delta for the whole plan: none; every touched file is already a planned artifact in .aes/target.yaml

Target delta: none for the whole plan (R1-R5): the change edits only files already planned in `.aes/target.yaml`, adds no normative item or success criterion, and `aes plan validate` is not run because no proposal is written; the pre-commit hook's `aes target validate` and `aes topology check` run on the commit itself.

## Durable documents

This repository declares durable documents (`durable_documents` in `.agentic/repo.yaml`); its declared roles are `goal`, `requirements`, `system_model`, `decisions`, `plans`, `catalog`. Each role named below is one of them (checked by quick-adopt).

Durable documents: none -- no durable doc changes; the model's ENT-COMMIT and PROC-COMMIT-CHECK rows keep their meaning

At completion, `python3 "$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py" --repo . --plan docs/plans/shaping-nav-preflight.md --range 6faebd3a257ac3ac8f8383233ea1045923be7b7b..HEAD` must exit 0; its full output is appended to `docs/plans/shaping-nav-preflight.check.txt` (the durable-documents check, Plan #61; `durable_docs_check.py` ships in the Company Planning plugin).

## Success and disproof

**Success evidence:** tests/greenfield/test_commit_rule.py, through real git commits and the installed commit-msg hook: (1) [Shaping demo] with the proposal plus an added navigation line in README.md is accepted (asserts the atomic route exists); (2) the same with a deleted or non-link line outside the folder, or a link to another proposal, is refused (asserts scope stays proposal-only); (3) a repo with no wiki/index.md accepts [Shaping demo] adding the proposal plus a new wiki/index.md of a heading and a link line (asserts the first-index bootstrap); (4) 'aes commit check --preflight -m "[Shaping demo] x"' on a staged unreached proposal exits 1 naming doc-reach and writes no commit-rule log line, and exits 0 once the link line is staged (asserts preflight equals the commit verdict without logging). The full test file passes.

**Trace review:** two runs of the success check above are judged from their full output: one on the parent commit before the change (the disproof run: it must show the defect or the check failing, which proves the check can fail) and one on the commit that makes the change (the success run); no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/shaping-nav-preflight.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Both runs are saved in that one file, each headed by its commit: the disproof condition is judged from both (it holds if the success run still shows the defect, or if the before run already passes, meaning the check cannot detect it), and success from the success run.

**Disproof:** After the change, a real [Shaping <id>] commit carrying only its proposal and an added link line is still refused, or a [Shaping <id>] commit that edits non-navigation content outside proposals/<id>/ is accepted; judged from the test output and the hook's stderr in the saved check file

## System model

**System model:** `docs/model/ODD.md`, a file in this repository describing this repository only (not a shared model). Reachable from the documentation entry point `wiki/index.md`, which links `docs/model/ODD.md`.

**Model elements this change adds, changes or relies on, and what the saved check output must show of each:**

- ENT-COMMIT: changed so a [Shaping] commit's scope admits navigation-only lines into its own proposal; the test output must show the accept/refuse split above
- PROC-COMMIT-CHECK: changed to also run on demand as a preflight; the preflight test output must show the same verdict as the hook with no log line

**Views, freshness and reconciliation:** the applicable view is the requirement-to-verification link in the Requirements table (each requirement and the check that shows it, the check being source-linked by its command); no other view applies because the change adds, changes or relies on no entity, process, record, event or view beyond the elements listed above. Freshness check (R4): after the change, `grep -n "ENT-COMMIT\|PROC-COMMIT-CHECK" docs/model/ODD.md docs/model/trace.yaml` on the change commit must show ENT-COMMIT still described as "a commit and its first-line tag" and PROC-COMMIT-CHECK still run by the commit-msg hook (the preflight is the same check run on demand); that grep and its output are appended to `docs/plans/shaping-nav-preflight.check.txt`. If an element above is added, removed or renamed, the model, its view coverage and the saved check output are reconciled in the same commit, and otherwise the model needs no update because the elements keep their meaning.

## Capability reuse

Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`):

- No catalogue entry fits, because this changes AES's own commit rule, which is the commit-tag capability itself
- What the work needs that no entry provides: edits to this repository's own files (`src/agentic_engineering_system/commit_rule.py`, `src/agentic_engineering_system/cli.py`, `tests/greenfield/test_commit_rule.py`); catalogue entries are cross-project capabilities, and none edits a repository's own source.

## Prior art and ownership

Prior art: the conflict is AES #476 (shaping checkpoints versus required wiki navigation), reproduced in process_tracing and worked around there with an undersized [Trivial] commit; feedback problem prob-2bed343a37 (agent-feedback-log #505) groups 12 sightings of the same incompatibility. The established pattern is the AES commit rule as the single authority (AP-REQ-001); its doc-reach check already mirrors project-meta `md_file_cap.py` reachability and already tells a repository with no index to "add one in this commit". This plan extends that authority rather than adding a second one. Internal lineage searched (2026-10-12): `git log origin/main -- src/agentic_engineering_system/commit_rule.py` (doc-reach added by plan doc-reach-new-docs, 894f78945; Shaping scope unchanged since the tag was introduced); `grep -i "shaping\|navigation\|preflight\|dry.run"` over `vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md` found no shared preflight idea.

External prior art: git's own `git commit --dry-run` (reports what would be committed, runs no hooks); pre-commit's `pre-commit run` (runs the same hooks on demand, before a commit); commitlint's `commitlint --edit`/stdin mode (judges a candidate message without committing). Dispositions:

| Candidate | Disposition | Why |
| --- | --- | --- |
| AES commit rule `judge()` | reuse | the one authority for commit verdicts; the preflight calls it unchanged |
| pre-commit `run` / commitlint stdin pattern | extend (pattern only) | "run the same check on demand before committing" is what `--preflight` does; adopting either tool would add a second rule set |
| `git commit --dry-run` | bounded exception (not adopted) | it skips commit-msg hooks, so it cannot report the rule's verdict |
| a separate [Navigation] tag or two-commit sequence | supersede | a second commit is the friction reported in #476 and the problem's records; admitting link lines inside the Shaping commit keeps one atomic commit |
| declaring proposals `unlinked_ok` | bounded exception (not adopted) | weakens the reachability requirement the daily check enforces |

Owner: AES canonical owns the rule; `check_coordination_claims.py --check --project agentic-engineering-system-canonical` returned "No active claims" before this lane.

## Uncertainties

Material uncertainties. This one is the complete set; it is material because a file outside the list would
make the change exceed this plan's scope.

| Material uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep on origin/main 6faebd3a2: the Shaping scope check and doc-reach live only in src/agentic_engineering_system/commit_rule.py (_judge_tag, judge); 'commit check' CLI only in src/agentic_engineering_system/cli.py; tests in tests/greenfield/test_commit_rule.py |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/shaping-nav-preflight.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `src/agentic_engineering_system/cli.py`
- `tests/greenfield/test_commit_rule.py`

The vertical delivers: A [Shaping <id>] commit that adds a new proposal document may also add link lines into proposals/<id>/ in existing Markdown pages or create the first wiki/index.md, so one commit lands the proposal and its navigation; and 'aes commit check --preflight -m <message>' reports the commit rule's verdict on the staged change without logging, before any commit is attempted It is done when this holds: tests/greenfield/test_commit_rule.py, through real git commits and the installed commit-msg hook: (1) [Shaping demo] with the proposal plus an added navigation line in README.md is accepted (asserts the atomic route exists); (2) the same with a deleted or non-link line outside the folder, or a link to another proposal, is refused (asserts scope stays proposal-only); (3) a repo with no wiki/index.md accepts [Shaping demo] adding the proposal plus a new wiki/index.md of a heading and a link line (asserts the first-index bootstrap); (4) 'aes commit check --preflight -m "[Shaping demo] x"' on a staged unreached proposal exits 1 naming doc-reach and writes no commit-rule log line, and exits 0 once the link line is staged (asserts preflight equals the commit verdict without logging). The full test file passes.

Make the change, run the success check before and after it, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files. This plan adds no coordinated-work ceremony: no work-unit graph, no review or release contract, no claim beyond the repository's own rules.

## Activation facts

Each fact, with its value and why:

- `shared_mechanism`: true -- the commit rule runs in every repository's commit-msg hook machine-wide, and `aes commit check --preflight` becomes a contract producers and agents call. R3 bounds the blast radius: [Shaping] widens only by added link lines into its own proposal folder (and headings in a newly created wiki/index.md), the hook path itself is unchanged, and the full existing hook test suite must pass.
- `empirical_comparison_proposed`: false -- no alternatives are compared; the success check verifies the one change.
- `llm_central`: false -- the change makes no model call.
- `irreversible_or_spend_action`: false -- the change is reverted by `git revert` and spends nothing.
- `claims_external_standard`: false -- the work claims no external standard, schema or contract.
- `aes_governed_target`: true -- derived, this repository has `.aes/target.yaml`; see AES target.
- `durable_documents_declared`: true -- derived, `.agentic/repo.yaml` has `durable_documents`; see Durable documents.

