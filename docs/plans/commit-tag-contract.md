---
schema_version: "1.0"
artifact_type: design_plan
id: commit-tag-contract
plan_id: commit-tag-contract
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/commit-tag-contract.receipt.json
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "A commit whose first line carries a tag the AES commit grammar (commit_rule.TAG_RE) recognises is no longer rejected by a repository's copied prefix-only commit-msg hook, because the generated hook wrapper asks 'aes commit tag' instead of trusting each repo's own regex list"
  canonical_example: "In project-meta, whose meta-process.yaml Goal regex is lowercase-only, a commit '[Goal PATH-brent-v1-2026-10-02] x' is rejected today by hooks/commit-msg; after the change the wrapper accepts it, while '[Bogus] x' is still rejected by the local hook."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, src/agentic_engineering_system/cli.py, tests/greenfield/test_commit_rule.py, proposals/aes-planning/rollout/install_everywhere.py, tests/rollout/test_install_everywhere.py; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/greenfield/test_commit_rule.py: 'aes commit tag' exits 0 and prints the tag for [Goal Upper-Case-1], [Plan #3], [Trivial], and exits 1 for [Bogus] and an untagged line (asserts the CLI uses the same grammar as the rule). tests/rollout/test_install_everywhere.py: a real git repo with the project-meta prefix-only hook and a lowercase-only Goal list, wired through the generated wrapper, commits '[Goal PATH-Upper-1] x' successfully and refuses '[Bogus] x' (asserts the full chained path, not the classifier alone). The check's full output on the parent commit and on the change commit is committed as docs/plans/commit-tag-contract.check.txt, and the commit is tagged [Goal commit-tag-contract] with an Asked: line quoting the request. python3 \"$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py\" --repo . --plan docs/plans/commit-tag-contract.md --range 056c1447501290d31146b947d567a7c0d2ae118a..HEAD exits 0 and its output is in the same file."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Local commit hooks accept every tag the AES commit rule accepts

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

**Request (verbatim):** Brian 2026-10-12 (weekly fix-owner run he set up) "For EACH item, read the issue and the linked problem issue, then choose exactly one disposition and carry it out" for AES canonical #414

**Desired result:** A commit whose first line carries a tag the AES commit grammar (commit_rule.TAG_RE) recognises is no longer rejected by a repository's copied prefix-only commit-msg hook, because the generated hook wrapper asks 'aes commit tag' instead of trusting each repo's own regex list.

**Stable example:** In project-meta, whose meta-process.yaml Goal regex is lowercase-only, a commit '[Goal PATH-brent-v1-2026-10-02] x' is rejected today by hooks/commit-msg; after the change the wrapper accepts it, while '[Bogus] x' is still rejected by the local hook.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Requirements

| Id | Requirement | Source | Check | Status |
| --- | --- | --- | --- | --- |
| R1 | A commit whose first line carries a tag the AES commit grammar (commit_rule.TAG_RE) recognises is no longer rejected by a repository's copied prefix-only commit-msg hook, because the generated hook wrapper asks 'aes commit tag' instead of trusting each repo's own regex list. | asked: Brian 2026-10-12 (weekly fix-owner run he set up) "For EACH item, read the issue and the linked problem issue, then choose exactly one disposition and carry it out" for AES canonical #414 | the success check under Success and disproof, its output saved as `docs/plans/commit-tag-contract.check.txt` | planned, not yet run |
| R2 | Shared mechanism: the generated wrapper is used by every repository with a local hooksPath, so a wrong change could block commits machine-wide; the wrapper falls back to running the local hook unchanged whenever 'aes commit tag' is missing or fails, and only skips hooks carrying the project-meta prefix-only marker | stated with the request | tests/rollout/test_install_everywhere.py covers recognised, unrecognised, and aes-missing cases | planned, not yet run |
| R3 | Model freshness: docs/model/ODD.md ENT-COMMIT and PROC-COMMIT-CHECK rows still describe the behaviour after the change | stated with the request | grep the two rows in the merged revision and confirm they name the first-line tag and commit-msg hook, recorded in the PR body | planned, not yet run |

Requirements the change's own claims imply are listed above as R2 onward.

## AES target

This repository is governed by an AES target (`.aes/target.yaml`). How R1 onward map to it:

- R1 -> AP-REQ-001 (every commit's first line carries one of the tags) and SC-AP-001; verification subject: the new `aes commit tag` test in `tests/greenfield/test_commit_rule.py` plus the existing SC-AP-001 tests in the same file, run together.
- R2 -> AP-REQ-001 and SC-AP-001 (with the commit-message hook installed, a correctly tagged commit is accepted; R2 extends that to the chained local hook); verification subject: the chained-wrapper tests in `tests/rollout/test_install_everywhere.py` (recognised, unrecognised and aes-missing cases).
- R3 -> AP-REQ-001 and SC-AP-001 (the model rows describe the commit and its check that this target item governs); verification subject: the ODD.md/trace.yaml grep above, saved in the check file.
- Target delta: none. `aes plan validate` is not run because no proposal is written: every touched governed file (`src/agentic_engineering_system/commit_rule.py`, `src/agentic_engineering_system/cli.py`, `tests/greenfield/test_commit_rule.py`) is already a planned artifact in `.aes/target.yaml`, and the pre-commit hook's `aes target validate` + `aes topology check` run on the commit itself; their output is saved in the check file.
- AP-REQ-001 (commit-tag rule) and its success criterion SC-AP-001: serves them by exposing the rule's own tag grammar to chained local hooks; verification subject for AP-REQ-001 is the new test in tests/greenfield/test_commit_rule.py (same grammar as the rule), and SC-AP-001's existing tests stay green in the same run; no target delta, all touched governed files are already planned artifacts

## Durable documents

This repository declares durable documents (`durable_documents` in `.agentic/repo.yaml`); its declared roles are `goal`, `requirements`, `system_model`, `decisions`, `plans`, `catalog`. Each role named below is one of them (checked by quick-adopt).

Durable documents: none -- no durable doc changes; the model's ENT-COMMIT row already names the first-line tag

At completion, `python3 "$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py" --repo . --plan docs/plans/commit-tag-contract.md --range 056c1447501290d31146b947d567a7c0d2ae118a..HEAD` must exit 0; its full output is appended to `docs/plans/commit-tag-contract.check.txt` (the durable-documents check, Plan #61; `durable_docs_check.py` ships in the Company Planning plugin).

## Success and disproof

**Success evidence:** tests/greenfield/test_commit_rule.py: 'aes commit tag' exits 0 and prints the tag for [Goal Upper-Case-1], [Plan #3], [Trivial], and exits 1 for [Bogus] and an untagged line (asserts the CLI uses the same grammar as the rule). tests/rollout/test_install_everywhere.py: a real git repo with the project-meta prefix-only hook and a lowercase-only Goal list, wired through the generated wrapper, commits '[Goal PATH-Upper-1] x' successfully and refuses '[Bogus] x' (asserts the full chained path, not the classifier alone).

**Trace review:** two runs of the success check above are judged from their full output: one on the parent commit before the change (the disproof run: it must show the defect or the check failing, which proves the check can fail) and one on the commit that makes the change (the success run); no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/commit-tag-contract.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Both runs are saved in that one file, each headed by its commit: the disproof condition is judged from both (it holds if the success run still shows the defect, or if the before run already passes, meaning the check cannot detect it), and success from the success run.

**Disproof:** After install, a real commit in project-meta with an uppercase Goal id is refused by the local hook, or a commit with a non-AES prefix not in the local list is accepted. The run examined is the post-install real commit's hook output (stderr) plus that repo's .git/aes/commit-rule-<date>.jsonl entry; it must show the AES verdict line and no 'Commit message must start with a valid prefix' error for the Goal commit, and that error for the [Bogus] commit.

## System model

**System model:** `docs/model/ODD.md`, a file in this repository describing this repository only (not a shared model). Reachable from the documentation entry point `wiki/index.md`, which links `docs/model/ODD.md`.

**Model elements this change adds, changes or relies on, and what the saved check output must show of each:**

- ENT-COMMIT (first-line tag): changed so its grammar has one source, TAG_RE; the tag test output must show the same accept/refuse split as the rule
- PROC-COMMIT-CHECK: relied on; the chained wrapper test output must show the local hook skipped only for AES-recognised tags

**Views, freshness and reconciliation:** the applicable view is the requirement-to-verification link in the Requirements table (each requirement and the check that shows it, the check being source-linked by its command); no other view applies because the change adds, changes or relies on no entity, process, record, event or view beyond the elements listed above. Freshness check (R3): after the change, `grep -n "ENT-COMMIT\|PROC-COMMIT-CHECK" docs/model/ODD.md` on the change commit must show ENT-COMMIT still described as "a commit and its first-line tag" and PROC-COMMIT-CHECK still run by the commit-msg hook; that grep and its output are appended to `docs/plans/commit-tag-contract.check.txt`. The model's trace file `docs/model/trace.yaml` keeps PROC-COMMIT-CHECK enforcing RULE-COMMIT-TAG; the same grep covers it. If an element above is added, removed or renamed, the model, its view coverage and the saved check output are reconciled in the same commit, and otherwise the model needs no update because the elements keep their meaning.

## Capability reuse

Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`):

- No catalogue entry fits, because this changes AES's own commit rule and its generated hook wrapper, which are the commit-tag capability itself
- What the work needs that no entry provides: edits to this repository's own files (`src/agentic_engineering_system/commit_rule.py`, `src/agentic_engineering_system/cli.py`, `tests/greenfield/test_commit_rule.py`, `proposals/aes-planning/rollout/install_everywhere.py`, `tests/rollout/test_install_everywhere.py`); catalogue entries are cross-project capabilities, and none edits a repository's own source.

## Irreversible actions and spend

None. Every change is a git commit reverted by `git revert`. After merge the generated wrappers are regenerated with `install_everywhere.py install` (the installer's own route; it rewrites only `~/.config/git/hooks-local/<repo>/` files and is undone by re-running it from the previous revision or `install_everywhere.py uninstall`). No money is spent and nothing is sent outward.

## Prior art and ownership

Prior art: git itself has no shared commit-message grammar; the established pattern here is the AES commit rule (`commit_rule.TAG_RE`, AP-REQ-001) as the single authority, already chained before each repository's own hook by `install_everywhere.py`. The fix adopts that authority instead of adding a new one: the wrapper asks the existing rule's grammar through a thin CLI. Alternatives considered: (a) edit `valid_prefixes` in each of the ~37 repositories' `meta-process.yaml` -- rejected, it repeats the divergence that caused AES #193/#297; (b) edit project-meta's template `hooks/commit-msg` and its 17 copies -- rejected for now, 17 repositories to change versus one generator. Internal lineage searched (2026-10-12): `grep -i "commit.*prefix|commit.*tag|valid_prefixes"` over `vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md` found no shared commit-grammar idea; `git log -G TAG_RE -- src/agentic_engineering_system/commit_rule.py` shows the grammar's lineage (137f47589 introduced `aes commit check`, then the #193 capitals fix); `git -C project-meta log -- hooks/commit-msg meta-process.yaml` shows dd76602c6 "accept goal labels", which added a hand-copied lowercase-only Goal regex to project-meta's own list -- the divergence this plan removes. The hook copies were found by hashing every `~/code/*/hooks/commit-msg` (17 identical copies of project-meta's template).

External prior art searched (known commit-message validators): commitlint (a shared config package that every repository extends, so one grammar source), gitlint (per-repository `.gitlint` rules), and pre-commit's `commit-msg` stage hooks (e.g. conventional-pre-commit). Dispositions:

| Candidate | Disposition | Why |
| --- | --- | --- |
| AES commit rule `commit_rule.TAG_RE` | reuse | already the single authority for the tag grammar (AP-REQ-001); this plan exposes it to chained hooks |
| commitlint shared-config pattern | extend (pattern only) | its "one shared config, every repo extends it" idea is what the wrapper does by calling `aes commit tag`; adopting commitlint itself would add a Node dependency to every repository and a second grammar |
| gitlint | bounded exception (not adopted) | per-repository rule files are the divergence this plan removes |
| pre-commit commit-msg hooks | bounded exception (not adopted) | these repositories wire hooks through `core.hooksPath` and `install_everywhere.py`, not the pre-commit framework |
| editing each repo's `valid_prefixes` | supersede | the wrapper's call to the rule's grammar supersedes per-repo Goal regexes for AES tags; | repeats the divergence behind AES #193/#297 |
| editing project-meta's template and its 17 copies | bounded exception (not adopted now) | 17 repositories to change versus one generator; the wrapper covers every live consumer |

Owner: AES canonical owns both the rule and the generator; no other lane holds a claim on these files (`check_coordination_claims.py --check --project agentic-engineering-system-canonical` returned "No active claims" before this lane).

## Uncertainties

Material uncertainties. This one is the complete set; it is material because a file outside the list would
make the change exceed this plan's scope.

| Material uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: grep of origin/main: TAG_RE lives only in src/agentic_engineering_system/commit_rule.py; LOCAL_COMMIT_MSG wrapper template only in proposals/aes-planning/rollout/install_everywhere.py; commit CLI in src/agentic_engineering_system/cli.py |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/commit-tag-contract.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `src/agentic_engineering_system/cli.py`
- `tests/greenfield/test_commit_rule.py`
- `proposals/aes-planning/rollout/install_everywhere.py`
- `tests/rollout/test_install_everywhere.py`

The vertical delivers: A commit whose first line carries a tag the AES commit grammar (commit_rule.TAG_RE) recognises is no longer rejected by a repository's copied prefix-only commit-msg hook, because the generated hook wrapper asks 'aes commit tag' instead of trusting each repo's own regex list. It is done when this holds: tests/greenfield/test_commit_rule.py: 'aes commit tag' exits 0 and prints the tag for [Goal Upper-Case-1], [Plan #3], [Trivial], and exits 1 for [Bogus] and an untagged line (asserts the CLI uses the same grammar as the rule). tests/rollout/test_install_everywhere.py: a real git repo with the project-meta prefix-only hook and a lowercase-only Goal list, wired through the generated wrapper, commits '[Goal PATH-Upper-1] x' successfully and refuses '[Bogus] x' (asserts the full chained path, not the classifier alone).

Make the change, run the success check before and after it, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files. This plan adds no coordinated-work ceremony: no work-unit graph, no review or release contract, no claim beyond the repository's own rules.

## Activation facts

Each fact, with its value and why:

- `shared_mechanism`: true -- `aes commit tag` becomes a contract that the generated hook wrapper in `~/.config/git/hooks-local/<repo>/commit-msg` calls for every repository with a local hooksPath (11 repositories today run the project-meta prefix-only hook through it). R2 bounds the blast radius: the wrapper falls back to the local hook unchanged when the command is absent or fails, and only skips hooks carrying the prefix-only marker.
- `empirical_comparison_proposed`: false -- no alternatives are compared; the success check verifies the one change.
- `llm_central`: false -- the change makes no model call.
- `irreversible_or_spend_action`: false -- the change is reverted by `git revert` and spends nothing.
- `claims_external_standard`: false -- the work claims no external standard, schema or contract.
- `aes_governed_target`: true -- derived, this repository has `.aes/target.yaml`; see AES target.
- `durable_documents_declared`: true -- derived, `.agentic/repo.yaml` has `durable_documents`; see Durable documents.

