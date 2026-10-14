---
schema_version: "1.0"
artifact_type: design_plan
id: commit-rule-skip-roots
plan_id: commit-rule-skip-roots
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/commit-rule-skip-roots.receipt.json
trace_review_criteria:
  - criterion_id: outcome
    expected_outcome: pass
goal:
  outcome: "A repository under a skip root named in the machine-wide commit-rule file commits without a tag and gets a logged skip; every other repository is judged as before, and no repository file can name a skip root"
  canonical_example: "git commit -m fixture in a fresh repo under /tmp succeeds and logs {\"verdict\": \"skip\"}; the same commit in a repo under ~/code is refused."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: src/agentic_engineering_system/commit_rule.py, tests/greenfield/test_commit_rule.py; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/greenfield/test_commit_rule.py::test_machine_skip_roots_exempt_throwaway_repositories_and_nothing_else passes, the other 44 commit-rule tests still pass, and enforced-planning tests/test_artifact_creation.py passes with skip_roots: [/tmp] in ~/.config/aes/commit_rule.yaml The check's full output is committed as docs/plans/commit-rule-skip-roots.check.txt, and the commit is tagged [Goal commit-rule-skip-roots] with an Asked: line quoting the request."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Commit rule: central temp-folder opt-out (issue #488)

## When a run fails or surprises us

Preserve the failed check and its execution trace id. Before selecting a fix,
read the complete inputs, prompts, tool arguments/results, intermediate stages
and final output, including the full check command/output and the changed files.
Cite the observed divergence and classify evidence absent, returned but unused
or contradicted, invalid expectation, or unresolved. Investigate an unresolved
cause before authorizing a causal repair. Bind the targeted repair to a new
traced verification run; retain the failed original. Review every failing or
surprising item and a sample of passes. A complete review is distinct from a
passing run. Criterion `outcome` covers the entire requested success check.

This procedure is for an unexpected failure. The failure modes anticipated in
advance are different: they are the disproof conditions under Success and
disproof, and the new test checks each one directly. Those are an untagged
`~/code` commit accepted as skip, a repository's own file naming a skip root, and
an unset `$VAR` entry silently matching something.

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-10 "yes but can hyou document that as an issue before moving onto it" (approving a central temp-folder opt-out declared in one place, not per repo), then "ok do that"

**Desired result:** A repository under a skip root named in the machine-wide commit-rule file commits without a tag and gets a logged skip; every other repository is judged as before, and no repository file can name a skip root.

**Stable example:** git commit -m fixture in a fresh repo under /tmp succeeds and logs {"verdict": "skip"}; the same commit in a repo under ~/code is refused.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Requirements

| Id | Requirement | Source | Check | Status |
| --- | --- | --- | --- | --- |
| R1 | A repository under a skip root named in the machine-wide commit-rule file commits without a tag and gets a logged skip; every other repository is judged as before, and no repository file can name a skip root. | asked: Brian 2026-10-10 "yes but can hyou document that as an issue before moving onto it" (approving a central temp-folder opt-out declared in one place, not per repo), then "ok do that" | the success check under Success and disproof, its output saved as `docs/plans/commit-rule-skip-roots.check.txt` | planned, not yet run |

Requirements the change's own claims imply: none beyond R1; the change presents nothing as following a standard, schema or contract.

## AES target

This repository is governed by an AES target (`.aes/target.yaml`). The change leaves `.aes/target.yaml` unchanged: no target delta, so no `aes plan validate` result is needed. How R1 maps to the existing items, with the verification subject for each:

- AP-REQ-001 and SC-AP-001: the commit-tag rule still refuses untagged commits in real repositories; the change only exempts throwaway repositories under machine-wide skip roots
- Verification subject for AP-REQ-001: `test_machine_skip_roots_exempt_throwaway_repositories_and_nothing_else`. It asserts the refusal in a repository outside a skip root and in a repository with its own file.
- Verification subject for SC-AP-001: the existing hook tests in `tests/greenfield/test_commit_rule.py`. All 44 must still pass unchanged.

## Success and disproof

**Success evidence:** tests/greenfield/test_commit_rule.py::test_machine_skip_roots_exempt_throwaway_repositories_and_nothing_else passes, the other 44 commit-rule tests still pass, and enforced-planning tests/test_artifact_creation.py passes with skip_roots: [/tmp] in ~/.config/aes/commit_rule.yaml

**Trace review:** the run whose full trace is judged is the success check above, run once on the commit that makes the change; no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/commit-rule-skip-roots.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Success and disproof are both judged from that file.

**Disproof:** An untagged commit in a ~/code repository is accepted as skip, or a repository's own .aes/commit_rule.yaml skip_roots entry takes effect.

## System model

AES has no `docs/model` system model file. The model for this change is the commit rule's own module docstring in `src/agentic_engineering_system/commit_rule.py`. It is the documentation entry point that says what the rule reads and writes, and the change updates it to describe `skip_roots`.

Model elements the change touches:

- **Stored state: the per-repository verdict log** (`<git-common-dir>/aes/commit-rule-<date>.jsonl`, existing). The change adds one verdict value, `skip`, plus a `skip_root` field. The new test reads the log line back and asserts `verdict`, `subject` and `skip_root`.
- **Configuration: the machine-wide file** (`~/.config/aes/commit_rule.yaml`, existing). The change adds one key, `skip_roots`, read only from that file. The new test asserts that `load_rule_config` returns it for a plain repository and returns `()` for a repository with its own file.
- **View: the hook's stderr line** (existing). The change adds `aes commit rule: skip — ...`, and the new test asserts that text.

Freshness and drift: the docstring and the tests change in the same commit as the code. The 45 commit-rule tests are the drift check: any later change that stops writing `skip`, or lets a repository file name a skip root, fails them. Reconciliation: no other view (dashboard, page, report) reads the verdict log's values, so nothing else needs updating.

## Capability reuse

Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`). `grep -i "commit\|hook\|governance"` on both files found no entry for the commit rule or for git hooks.

- No catalogue entry fits, because the catalogue does not list the AES commit rule; this change extends that existing in-repository mechanism (`aes commit check`, `load_rule_config`) and adds no new capability.

## Irreversible actions and spend

None. The change is code plus a test in one revertible commit. Adding `skip_roots: [/tmp]` to `~/.config/aes/commit_rule.yaml` afterwards is a one-line local edit, undone by deleting the line. No spend, no external publication.

## Uncertainties

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: git diff --stat origin/main shows only src/agentic_engineering_system/commit_rule.py and tests/greenfield/test_commit_rule.py |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/commit-rule-skip-roots.check.txt`):

- `src/agentic_engineering_system/commit_rule.py`
- `tests/greenfield/test_commit_rule.py`

The vertical delivers: A repository under a skip root named in the machine-wide commit-rule file commits without a tag and gets a logged skip; every other repository is judged as before, and no repository file can name a skip root. It is done when this holds: tests/greenfield/test_commit_rule.py::test_machine_skip_roots_exempt_throwaway_repositories_and_nothing_else passes, the other 44 commit-rule tests still pass, and enforced-planning tests/test_artifact_creation.py passes with skip_roots: [/tmp] in ~/.config/aes/commit_rule.yaml

Make the change, run the success check, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files. The plan adds no coordinated-work ceremony: one agent, one claimed maintenance lane, one PR, no extra reviews, stages or hand-offs.

## Activation facts

Shared mechanism: no new one. The change adds one setting to the existing commit rule. It does not create a mechanism of its own. Because that rule is a machine-wide hook, the setting still affects every repository. Brian chose to declare it only in the machine-wide file, so the exception lives in one place (issue #488). Feedback path:

- every skip is logged as a `skip` verdict in the repository's `.git/aes/commit-rule-<date>.jsonl`;
- issue BrianMills2718/agentic-engineering-system-canonical#488 stays the place to report a wrong skip.

The wrong-when condition is the disproof above.

No comparison, no LLM at the centre, no irreversible action or spend, and no claim to follow an external standard.
