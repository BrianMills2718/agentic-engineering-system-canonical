---
schema_version: "1.0"
artifact_type: design_plan
id: rules-register
plan_id: rules-register
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/rules-register.receipt.json
goal:
  outcome: "docs/rules/RULES.md in AES canonical lists the workspace instruction rules, the feedback loop's rules and project-meta's 263 legacy rules, each with how it is enforced, built from docs/rules/register.yaml"
  canonical_example: "The page's feedback-loop table shows loop-387 as enforced via Jev gate rule M1 and loop-378 as withdrawn, each linking its issue."
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: docs/rules/register.yaml, docs/rules/RULES.md, scripts/rules/build_rules_page.py, tests/test_rules_page.py, wiki/index.md; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "tests/test_rules_page.py passes and the built page lists 12 workspace rules, 21 feedback-loop rules and 263 legacy rules. The check's full output is committed as docs/plans/rules-register.check.txt, and the commit is tagged [Goal rules-register] with an Asked: line quoting the request."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# One page listing every rule agents follow

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-08 "yes we absolutely need this. you should check out what project meta already has on this"

**Desired result:** docs/rules/RULES.md in AES canonical lists the workspace instruction rules, the feedback loop's rules and project-meta's 263 legacy rules, each with how it is enforced, built from docs/rules/register.yaml.

**Stable example:** The page's feedback-loop table shows loop-387 as enforced via Jev gate rule M1 and loop-378 as withdrawn, each linking its issue.

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Success and disproof

**Success evidence:** tests/test_rules_page.py passes and the built page lists 12 workspace rules, 21 feedback-loop rules and 263 legacy rules.

**Trace review:** the run whose full trace is judged is the success check above, run once on the commit that makes the change; no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/rules-register.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Success and disproof are both judged from that file.

**Disproof:** A register rule or a legacy rule id is missing from the page, or the page claims enforcement the register does not state.

## System model

**System model:** `docs/rules/register.yaml`

**Model elements this change adds, changes or relies on, and what the saved check output must show of each:**

- register rule entries (id, rule, origin, enforcement_status, enforcement_mechanism, evidence): every entry must appear on the built page with its status
- RULES.md page: summary counts must equal the register's and project-meta's counts (12, 21, 263)

## Uncertainties

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: git status --short (excluding docs/plans) lists exactly docs/rules/register.yaml, docs/rules/RULES.md, scripts/rules/build_rules_page.py, tests/test_rules_page.py and wiki/index.md, the five files below; the generator reads project-meta only, never writes it |
| Whether a register entry claims enforcement that does not exist | Owner: this session; evidence: each "enforced" or "checked" entry names the hook, gate or script that does it (commit rule, Jev M1 merge guard, md_file_cap.py, check_article_review.py); unverified clauses were removed |
| Whether the legacy section goes stale | Owner: this session; evidence: the page states it was read from project-meta policy/registry.yaml at build time; rebuilding is one command |
| Whether issue states change after the build (a licensed rule adopted or withdrawn) | Owner: the feedback loop; evidence: the register records the issue link for each rule, so a reader can open the current state |

This is the complete list: the change adds a data file, a generator, its test, the generated page and one wiki link; no stored state, service or other repository changes.

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/rules-register.check.txt`):

- `docs/rules/register.yaml`
- `docs/rules/RULES.md`
- `scripts/rules/build_rules_page.py`
- `tests/test_rules_page.py`
- `wiki/index.md`

The vertical delivers: docs/rules/RULES.md in AES canonical lists the workspace instruction rules, the feedback loop's rules and project-meta's 263 legacy rules, each with how it is enforced, built from docs/rules/register.yaml. It is done when this holds: tests/test_rules_page.py passes and the built page lists 12 workspace rules, 21 feedback-loop rules and 263 legacy rules.

Make the change, run the success check, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files.

## Activation facts

No shared mechanism, no comparison, no LLM at the centre, no irreversible action or spend: a bounded change Brian asked for.
