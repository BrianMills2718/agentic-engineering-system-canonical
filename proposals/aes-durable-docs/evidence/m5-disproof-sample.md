---
description: M5 disproof sample for aes-durable-docs, run 2026-10-11 under the amended timing and population; the disproof condition fires (9 of 10 none or mechanical), because the rule was not in effect for 8 of the 10 plans (stale installed plugin or repository not yet declared)
---

# M5 disproof sample

**Session transcript id:** `0031e708-eb6b-409b-8823-6d04cc3aa693` (one Claude Code session, Opus, 2026-10-11).
**Rule applied:** the disproof condition in `../PLAN.md` (Trace review), unchanged, with the timing and population amendment merged in AES PR #534 (merge `f66873ef8`) before any sample diff was read.
**Selection script** (`m5-sample-tools/select.py <inventory>`, then `gen.py` for the per-plan sections; reuse both for the re-sample with its population filter): each of the 22 repositories in `m5-inventory.json` (paths checked against their `origin` remotes: all 22 resolve to the rolled-out repositories) plus company-planning and AES canonical; every `*.receipt.json` on `origin/main` with `completed_at` at or after 2026-10-10T23:54:42Z; excluded plans removed; plans with no commit tagged with their id dropped; ordered by the commit time of the last tagged commit on `origin/main`, newest first. 14 plans qualified, so the sample is the first 10 and the threshold stays 5.

## Verdict: the disproof condition fires

| # | Repository | Plan | Durable-documents line | Classification |
|---|---|---|---|---|
| 1 | company-planning | policy-enforcement-pilot | decisions, system_model (4 IDs), plans | real update |
| 2 | digimon_application_20260215 | 222_main_branch_health | absent (gate leak) | none |
| 3 | agent-skills | rulesync-hooks | absent (gate leak) | none (but made an undeclared real goal-document change) |
| 4 | project-meta | register-interview-kit | absent (gate leak) | none |
| 5 | company-planning | aes-overlay-creates-target | `none -- ...` | none (one mechanical comment in trace.yaml) |
| 6 | agent-skills | rulesync-client-sync | absent (adopted before the repo declared durable documents) | none |
| 7 | project-meta | audit-rulesync-check | absent (adopted before) | none |
| 8 | project-meta | register-subreddit-map | absent (adopted before) | none |
| 9 | digimon_application_20260215 | 221_documentation_consolidation | absent (adopted before) | none (mechanical frontmatter plus ADR consolidation) |
| 10 | agent-skills | rtk-shell-output | absent (adopted before) | none |

**9 of 10 count as `none` or mechanical; the threshold is 5. The disproof fires.**

The result does not depend on the rollout's timing. Five sampled plans (6-10) were adopted hours before their repository's durable-documents PR merged, so the gate had nothing to require of them. Restricting the sample to the five plans whose repository already declared durable documents at adoption (1-5) still gives 4 of 5 as `none`, above half (3).

What the sample shows:

- **The adoption gate leaks.** Plans 2, 3 and 4 were adopted after their repository declared durable documents and carry no line. Outside the top 10, AES `commit-rule-skip-roots` (adopted 01:57Z, AES declared at 01:11Z) is a fourth. The rule (`OV-DURABLE-DOCS-DECLARED`) is enforced by company-planning's compiler, but these plans were adopted without it firing (cause in the next section).
- **Silence hides real updates.** Plan 3 changed a requirement's source of truth in its goal document without declaring the role, so nothing checked that change.
- **Where the rule applied, it worked.** Plan 1, the only plan that declared roles, updated each one with content (a three-rule decision amendment and two new traced rules with owners and tests).

## Why the gate leaked: the rule was not installed

Each adoption receipt records the profile that gated it. Read from `origin/main` for all ten sampled plans:

| Profile in receipt | Plans | `OV-DURABLE-DOCS-DECLARED` in receipt |
|---|---|---|
| bounded-design@13 | 1, 5 (both company-planning) | yes |
| bounded-design@12 | 10 | no (adopted before agent-skills declared; the item was not activated) |
| bounded-design@11 | 2, 3, 4, 6, 7, 8, 9 | no; this profile predates the rule |

The rule was not installed when plans 2, 3 and 4 were adopted. Claude Code's installed copy of the company-planning plugin (`~/.claude/plugins/cache/inside-success/company-planning/`) was version `0.2.0+codex.20261009212200`, which uses profile bounded-design@11. That compiler has no `durable_documents_declared` fact, because the local marketplace clone had not refreshed since 2026-10-09. Codex's copy (`~/.codex/plugins/cache/...`, `0.2.0+codex.20261011015657`) already had the rule. Only the two plans adopted inside company-planning, which runs its own source, were actually gated.

Among those two gated plans, one made a real update and one declared `none`. That is 1 of 2 at the threshold, too few to judge the rule. The sample therefore measured whether the rule had been deployed, not what the rule does.

**Root fix applied 2026-10-11:** ran `claude plugin marketplace update inside-success`, then `claude plugin update company-planning@inside-success`. The update installed `0.2.0+codex.20261011095732`, and its compiler contains `durable_documents_declared` (profile bounded-design@13) for new sessions. The missing automatic refresh is filed as project-meta #2537, because it would recur for any plugin rule change.

## Cold-reader re-run (both pilots pass)

Same method as M4: `claude -p --model haiku`, Read tool only (Bash, Grep, Glob, Edit, Write, NotebookEdit, web and agents disallowed), `--max-turns 40`, question on stdin, fresh detached checkout of `origin/main`. Spend: 2 sessions, 0.070 USD, which brings the total to 4 of the 4 allowed cold-reader sessions.

| Pilot | Checkout | Trace | Question | Files opened | Result |
|---|---|---|---|---|---|
| AES canonical | `f66873ef8` | `m5-aes-canonical-cold-reader.jsonl` (session `5691b080-4593-45d6-aa60-0025222e470f`) | `m4-aes-canonical-cold-reader-question.txt` | `wiki/index.md`, Decision 0008, `docs/model/ODD.md`, `docs/model/trace.yaml`, `src/agentic_engineering_system/evidence.py`, `tests/greenfield/test_evidence.py`, `tests/greenfield/test_reconcile.py` | pass (8 turns, 0.047 USD): rule `RULE-DEPENDENCY-CHANGE-STALES` (STALE on a changed dependency path or target ref, UNREACHABLE off-ancestry), owner `evidence.py` with cited lines, both trace checks opened and described, why from Decision 0008 §2. It also found an untested gap: non-Python dependencies such as `pyproject.toml` stale evidence only when declared. |
| company-planning | `3711601128` | `m5-company-planning-cold-reader.jsonl` (session `7bc3d22b-dbb3-4f77-9f82-3be0bf55c6d0`) | `m5-company-planning-cold-reader-question.txt` | `wiki/index.md`, `docs/model/trace.yaml`, Decision 0001, `gate.py`, `tests/test_method_conformance.py` | pass (7 turns, 0.023 USD): rule `RULE-ADOPT-RECEIPT`, owner `gate.py` (`decision` is `adopted` only when the result is `pass`), the three trace tests opened with line numbers, why from Decision 0001. One Grep attempt was refused by the tool restriction ("Grep is disabled for this session"). |

The company-planning question file is reconstructed: Plan #63 recorded the question in its review but did not save the prompt. It uses the AES question's wording with Plan #63's recorded question substituted.

The cold-reader half of the disproof condition does not fire. The first half does.

## Per-plan evidence

Each section gives the plan's durable-documents line, its commit range, `git diff --stat` over the range, and the full diff of each declared document from the plan's own commits. For the `plans` role, that is the plan document; generated plan records (receipt, bundle, verdicts JSON) appear only in the `--stat`. Plans that declare no role list the repository's declared durable paths that the plan's commits touched, with the full diff of each.

### 1. company-planning `policy-enforcement-pilot`

- Plan file: `docs/plans/policy-enforcement-pilot.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T10:19:00Z; last plan-tagged commit 2026-10-11T06:23:47-04:00.
- Durable-documents line: `Durable documents: decisions, system_model#PROC-ADOPT, system_model#PROC-QUICK-ADOPT, system_model#RULE-MODEL-ELEMENT-IDS, system_model#RULE-ELEMENT-STATUS-FROM-RUN, plans`
- Commit range: `cdcf6c7d604d..3711601128de` (parent of the first to the last of the 16 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: d93e941d2, 22b24a1c2, 8b850ed30, 035c87b75, 9b9c6c463, c4b2ff492, 1e339f114, 64e332846, 07d820bea, ab3dcbb82, 7dd8b9d5c, 437afab74, 0e014037f, bccb94080, ec4112fa8, 371160112

`git diff --stat` over the range:

```text
 README.md                                                       |   2 +-
 docs/decisions/0002-every-project-has-a-checked-system-model.md |  27 +
 docs/model/ODD.md                                               |   6 +-
 docs/model/VIEW_COVERAGE.md                                     |  64 +-
 docs/model/trace.yaml                                           |  23 +-
 docs/plans/aes-overlay-creates-target.adoption-attempts.jsonl   |   3 +
 docs/plans/aes-overlay-creates-target.adoption-decision.json    |  15 +
 docs/plans/aes-overlay-creates-target.bundle.json               | 642 +++++++++++++++++++
 docs/plans/aes-overlay-creates-target.check.txt                 |  12 +
 docs/plans/aes-overlay-creates-target.facts.json                |  21 +
 docs/plans/aes-overlay-creates-target.goal.md                   |  18 +
 docs/plans/aes-overlay-creates-target.md                        | 130 ++++
 docs/plans/aes-overlay-creates-target.path-decision.json        |  57 ++
 docs/plans/aes-overlay-creates-target.receipt.json              | 541 ++++++++++++++++
 docs/plans/aes-overlay-creates-target.verdicts.json             | 182 ++++++
 docs/plans/policy-enforcement-pilot.adoption-attempts.jsonl     |   5 +
 docs/plans/policy-enforcement-pilot.adoption-decision.json      |  15 +
 docs/plans/policy-enforcement-pilot.aes-proposal.yaml           | 124 ++++
 docs/plans/policy-enforcement-pilot.aes-validate.txt            |   5 +
 docs/plans/policy-enforcement-pilot.bundle.json                 | 949 ++++++++++++++++++++++++++++
 docs/plans/policy-enforcement-pilot.check.txt                   | 246 +++++++
 docs/plans/policy-enforcement-pilot.facts.json                  |  25 +
 docs/plans/policy-enforcement-pilot.goal.md                     |  36 ++
 docs/plans/policy-enforcement-pilot.md                          | 304 +++++++++
 docs/plans/policy-enforcement-pilot.path-decision.json          |  57 ++
 docs/plans/policy-enforcement-pilot.receipt.json                | 744 ++++++++++++++++++++++
 docs/plans/policy-enforcement-pilot.verdicts.json               | 659 +++++++++++++++++++
 plugins/company-planning/.claude-plugin/plugin.json             |   2 +-
 plugins/company-planning/.codex-plugin/plugin.json              |   2 +-
 .../planning-method-conformance-receipt.v1.schema.json          |   7 +-
 .../method-conformance/profiles/bounded-design.v1.json          |  12 +-
 .../company-planning/distribution/references/system-model.md    |  31 +
 .../designs/enforcement/PLANNING_METHOD_CONFORMANCE_RECEIPT.md  |   9 +-
 plugins/company-planning/scripts/method_conformance/gate.py     |  30 +-
 plugins/company-planning/scripts/method_conformance/lint.py     |   4 +-
 .../scripts/method_conformance/model_elements.py                | 160 +++++
 plugins/company-planning/scripts/model_status_page.py           | 214 +++++++
 tests/e2e/model_status_tooltips.mjs                             |  41 ++
 tests/test_method_conformance.py                                |   2 +-
 tests/test_model_status_page.py                                 |  71 +++
 tests/test_quick_adopt_checks.py                                | 134 ++++
 wiki/index.md                                                   |   2 +
 42 files changed, 5580 insertions(+), 53 deletions(-)
```

Full diff of declared role `decisions` (`docs/decisions/`), plan commits only:

```diff
commit 9b9c6c4 [Goal policy-enforcement-pilot] Step 2: write the plan, build and review rules into decision 0002

diff --git a/docs/decisions/0002-every-project-has-a-checked-system-model.md b/docs/decisions/0002-every-project-has-a-checked-system-model.md
index fa7084f..4c56238 100644
--- a/docs/decisions/0002-every-project-has-a-checked-system-model.md
+++ b/docs/decisions/0002-every-project-has-a-checked-system-model.md
@@ -33,3 +33,30 @@ arc42-shaped model cannot hold something an ODD-style one held (a pattern, a wri
 view) without adding a section, or two projects in a row report the outline itself as
 friction.
 Plan: [system-model-arc42](../plans/system-model-arc42.md); [goal launcher](../plans/system-model-arc42.goal.md).
+
+**Amended 2026-10-11: the plan, build and review rules are checked, not self-attested.**
+Brian set the goal on 2026-10-11: "Make plan/build/review rules checked, stress-tested on
+qualitative_coding slice 1". Before this amendment an agent could write "pass" for a model it
+had not checked (issue #119). Three rules now apply to every system model:
+
+- **RULE-MODEL-ELEMENT-IDS (plan).** Every model element (entity, process, record or event,
+  view, rule) has a stable ID and is marked `decided` or `guessed`. The model ends with an
+  unknowns table: each open question and what would decide it. In a project that is an AES
+  v0.2 target, an element's ID is the AES success-criterion ID it is tested under.
+- **RULE-ELEMENT-STATUS-FROM-RUN (build).** Each element is covered by at least one named test,
+  and its status is computed from the last recorded run by AES `evidence.assess()`: SUPPORTED
+  (the test passed), REFUTED (it failed) or INSUFFICIENT (no test, or the recorded run is
+  stale). Nobody writes an element's status by hand.
+- **RULE-REVIEW-STATUS-PAGE (review).** Each review point links a page generated from those
+  computed statuses, listing every element and its status.
+
+The decided/guessed mark and the unknowns table are company-planning extensions, not AES
+fields. The model passes agent_ecology2's layer test (META-ADR-0005: a layer must compress
+something unique, be read by something, and have a way to stay fresh): the element check
+reads it, and a stale run turns an element INSUFFICIENT. Checks land in steps 3 to 5 of
+[policy-enforcement-pilot](../plans/policy-enforcement-pilot.md): they warn first, and they
+refuse only after the qualitative_coding slice 1 stress test catches qc issue 130 items 1 and
+2 unaided. Until its check lands, a rule is written only; `docs/model/trace.yaml` gains each
+rule, with its owner and check, in the commit that adds that check. Wrong when: on qc slice 1
+the warn-mode check misses issue 130 item 1 or 2, or a first model meeting the three rules
+costs more than the 3 agent hours above.
```

Full diff of declared role `system_model` (`docs/model/ODD.md`), plan commits only:

```diff
commit 1e339f1 [Goal policy-enforcement-pilot] Gate warns when a plan's system model lacks element IDs, marks, unknowns or tests

diff --git a/docs/model/ODD.md b/docs/model/ODD.md
index 4cd66ce..be460e1 100644
--- a/docs/model/ODD.md
+++ b/docs/model/ODD.md
@@ -68,6 +68,7 @@ adoption decisions, and the git repository holding the plan.
 | append attempt | every `adopt` call, refused or adopted, appends one `method_adoption_attempt` line to `<plan>.adoption-attempts.jsonl`; the decision file keeps only the latest (meeting-claims-true K5) | `gate.py` `append_attempt` inside `adopt` |
 | route fit | `adopt --route-fit fits\|does-not-fit` records the adopter's answer (a reason is required for does-not-fit) as a `route_fit_answer` in the skill-feedback outbox and in the attempt line (K6) | `cli.py adopt`, `gate.py` `record_route_fit` |
 | route-fit reader | two or more does-not-fit answers for one route on different plans open one keyed concern; it reads the local outbox (K6) | `plugins/company-planning/scripts/route_fit_reader.py`, run after `skill-observability.service` |
+| model-element check | a passing `CORE-SYSTEM-MODEL` whose linked model lacks element lines `- ID (decided\|guessed): ...`, a mark on each, an unknowns table, or a test naming each ID (in an AES target: a verification subject's `criterion_refs`) becomes `warn` with codes MODEL-NO-ELEMENT-IDS, ELEMENT-NO-MARK, MODEL-NO-UNKNOWNS, ELEMENT-NO-TEST, MODEL-NOT-FOUND; warn never blocks (Decision 0002 amendment, warn mode until the qc pilot) | `model_elements.py` `check_plan` inside `gate.evaluate` |
 | verdict reuse | a semantic verdict is reused while item, statement, judged text and model are unchanged (Plan #56) | `first_try.py` `CachedVerifier` inside `gate.evaluate` |
 | review source validation | verifies each supplied Git blob and digest; optional reviewed-subject pins reject stale source revisions; never proves projection fidelity | `validate_review_surfaces.py --source-repo --subject-revision` |
 
@@ -98,8 +99,8 @@ model) with the verdict and the trace id of the call that produced it.
 
 | View | What it shows |
 | --- | --- |
-| adopt CLI output | ADOPTED/REFUSED, each failing item with the verifier's "missing" text, receipt and decision paths, goal path; quick-adopt prints the commit form only when adopted, and a refused run says not to commit and how to re-run (Plan #62) |
-| receipt JSON | every item: disposition, evidence refs with sha256, semantic verdict, model, trace id, and `reused` when the verdict came from the cache |
+| adopt CLI output | ADOPTED/REFUSED, each failing item with the verifier's "missing" text, a `warn <item>: <codes> -> <fix>` line per warned item, receipt and decision paths, goal path; quick-adopt prints the commit form only when adopted, and a refused run says not to commit and how to re-run (Plan #62) |
+| receipt JSON | every item: disposition (`warn` = passed with model-element findings), evidence refs with sha256, semantic verdict, model, trace id, and `reused` when the verdict came from the cache |
 | skeleton plan | one section per applicable item, each quoting the item's statement, with a fill-in marker |
 | check CLI output | unfilled skeleton slots, every unresolved item with the verifier's "missing" text, and how many verdicts were reused |
 | goal launcher file | the `/goal` text for an adopted plan, bound to the plan sha256 |
commit ab3dcbb [Goal policy-enforcement-pilot] Model status page: each element's standing from AES runs

diff --git a/docs/model/ODD.md b/docs/model/ODD.md
index be460e1..85d0d41 100644
--- a/docs/model/ODD.md
+++ b/docs/model/ODD.md
@@ -107,6 +107,7 @@ model) with the verdict and the trace id of the call that produced it.
 | system-model review | a source-bound selection of the adoption-gate model; source validation is separate from behavioral evidence and complete model coverage |
 | lint CLI/JSON output | per-target structural consistency checks, failed diagnostic codes, target counts, limitations and exit status |
 | durable check CLI output | one `FINDING <code> role= id= file=` line per finding and a summary line with counts per code and the exit status (0 clean, 1 findings, 2 invalid input) |
+| model status page | one row per model element: its ID, its decided/guessed mark, and its standing from AES `evidence.assess()` (Supported, Refuted, Not shown yet, Not tracked), with a tooltip on every chip; written by `model_status_page.py` |
 
 The system-model review source declaration lives in `proposals/system-model-review/model-review.json`. It maps selected model headings into the existing review-surface contract; it is a hand-authored projection, not a second model authority.
 
commit 0e01403 [Goal policy-enforcement-pilot] Match model elements to AES criteria through target_refs

diff --git a/docs/model/ODD.md b/docs/model/ODD.md
index 85d0d41..c1d3463 100644
--- a/docs/model/ODD.md
+++ b/docs/model/ODD.md
@@ -68,7 +68,7 @@ adoption decisions, and the git repository holding the plan.
 | append attempt | every `adopt` call, refused or adopted, appends one `method_adoption_attempt` line to `<plan>.adoption-attempts.jsonl`; the decision file keeps only the latest (meeting-claims-true K5) | `gate.py` `append_attempt` inside `adopt` |
 | route fit | `adopt --route-fit fits\|does-not-fit` records the adopter's answer (a reason is required for does-not-fit) as a `route_fit_answer` in the skill-feedback outbox and in the attempt line (K6) | `cli.py adopt`, `gate.py` `record_route_fit` |
 | route-fit reader | two or more does-not-fit answers for one route on different plans open one keyed concern; it reads the local outbox (K6) | `plugins/company-planning/scripts/route_fit_reader.py`, run after `skill-observability.service` |
-| model-element check | a passing `CORE-SYSTEM-MODEL` whose linked model lacks element lines `- ID (decided\|guessed): ...`, a mark on each, an unknowns table, or a test naming each ID (in an AES target: a verification subject's `criterion_refs`) becomes `warn` with codes MODEL-NO-ELEMENT-IDS, ELEMENT-NO-MARK, MODEL-NO-UNKNOWNS, ELEMENT-NO-TEST, MODEL-NOT-FOUND; warn never blocks (Decision 0002 amendment, warn mode until the qc pilot) | `model_elements.py` `check_plan` inside `gate.evaluate` |
+| model-element check | a passing `CORE-SYSTEM-MODEL` whose linked model lacks element lines `- ID (decided\|guessed): ...`, a mark on each, an unknowns table, or a test naming each ID (in an AES target: a verification subject's `criterion_refs`, directly or through a success criterion whose `target_refs` lists the element) becomes `warn` with codes MODEL-NO-ELEMENT-IDS, ELEMENT-NO-MARK, MODEL-NO-UNKNOWNS, ELEMENT-NO-TEST, MODEL-NOT-FOUND; warn never blocks (Decision 0002 amendment, warn mode until the qc pilot) | `model_elements.py` `check_plan` inside `gate.evaluate` |
 | verdict reuse | a semantic verdict is reused while item, statement, judged text and model are unchanged (Plan #56) | `first_try.py` `CachedVerifier` inside `gate.evaluate` |
 | review source validation | verifies each supplied Git blob and digest; optional reviewed-subject pins reject stale source revisions; never proves projection fidelity | `validate_review_surfaces.py --source-repo --subject-revision` |
```

Full diff of declared role `system_model` (`docs/model/trace.yaml`), plan commits only:

```diff
commit 1e339f1 [Goal policy-enforcement-pilot] Gate warns when a plan's system model lacks element IDs, marks, unknowns or tests

diff --git a/docs/model/trace.yaml b/docs/model/trace.yaml
index 585a7e4..5498668 100644
--- a/docs/model/trace.yaml
+++ b/docs/model/trace.yaml
@@ -5,7 +5,7 @@ entities:
   - {id: ENT-METHOD-PROFILE, name: method profile, stored_in: plugins/company-planning/contracts/method-conformance/profiles/}
 processes:
   - {id: PROC-COMPILE, name: compile, enforces: [RULE-SOURCE-PIN, RULE-DURABLE-DECLARED]}
-  - {id: PROC-ADOPT, name: adopt, enforces: [RULE-ADOPT-RECEIPT, RULE-SYSTEM-MODEL-REQUIRED]}
+  - {id: PROC-ADOPT, name: adopt, enforces: [RULE-ADOPT-RECEIPT, RULE-SYSTEM-MODEL-REQUIRED, RULE-MODEL-ELEMENT-IDS]}
   - {id: PROC-QUICK-ADOPT, name: quick-adopt, enforces: [RULE-QUICK-BOUNDED]}
   - {id: PROC-DURABLE-CHECK, name: durable-documents check, enforces: [RULE-DURABLE-COMPLETION]}
 rules:
@@ -31,6 +31,16 @@ rules:
     checks:
       - tests/test_method_conformance.py::test_plan_without_system_model_blocks_adoption
     decisions: [docs/decisions/0002-every-project-has-a-checked-system-model.md]
+  - id: RULE-MODEL-ELEMENT-IDS
+    statement: A plan's linked system model gives each element a stable ID marked decided or guessed, ends with an unknowns table, and every element is named by a test (an AES verification subject's criterion_refs in an AES target); a miss is a non-blocking warn on CORE-SYSTEM-MODEL until refuse mode.
+    owner: plugins/company-planning/scripts/method_conformance/model_elements.py
+    checks:
+      - tests/test_quick_adopt_checks.py::test_quick_adopt_warns_when_model_has_no_element_ids
+      - tests/test_quick_adopt_checks.py::test_element_without_mark
+      - tests/test_quick_adopt_checks.py::test_model_without_unknowns_table
+      - tests/test_quick_adopt_checks.py::test_element_without_test_names_only_the_untested_one
+      - tests/test_quick_adopt_checks.py::test_aes_target_coverage_comes_from_verification_subjects
+    decisions: [docs/decisions/0002-every-project-has-a-checked-system-model.md]
   - id: RULE-DURABLE-DECLARED
     statement: In a repository whose .agentic/repo.yaml declares durable_documents, a plan carries a Durable documents line (OV-DURABLE-DOCS-DECLARED).
     owner: plugins/company-planning/scripts/method_conformance/compiler.py
commit ab3dcbb [Goal policy-enforcement-pilot] Model status page: each element's standing from AES runs

diff --git a/docs/model/trace.yaml b/docs/model/trace.yaml
index 5498668..e314389 100644
--- a/docs/model/trace.yaml
+++ b/docs/model/trace.yaml
@@ -41,6 +41,14 @@ rules:
       - tests/test_quick_adopt_checks.py::test_element_without_test_names_only_the_untested_one
       - tests/test_quick_adopt_checks.py::test_aes_target_coverage_comes_from_verification_subjects
     decisions: [docs/decisions/0002-every-project-has-a-checked-system-model.md]
+  - id: RULE-ELEMENT-STATUS-FROM-RUN
+    statement: An element's shown status comes from a recorded run; the model status page shows the standing AES evidence.assess() reports for each element ID and computes none itself (an ID AES does not track is shown as Not tracked).
+    owner: plugins/company-planning/scripts/model_status_page.py
+    checks:
+      - tests/test_model_status_page.py::test_each_element_gets_exactly_the_aes_standing
+      - tests/test_model_status_page.py::test_not_an_aes_target_reads_no_standings
+      - tests/test_model_status_page.py::test_page_words_colours_tooltips_and_footer
+    decisions: [docs/decisions/0002-every-project-has-a-checked-system-model.md]
   - id: RULE-DURABLE-DECLARED
     statement: In a repository whose .agentic/repo.yaml declares durable_documents, a plan carries a Durable documents line (OV-DURABLE-DOCS-DECLARED).
     owner: plugins/company-planning/scripts/method_conformance/compiler.py
commit 0e01403 [Goal policy-enforcement-pilot] Match model elements to AES criteria through target_refs

diff --git a/docs/model/trace.yaml b/docs/model/trace.yaml
index e314389..12c58c6 100644
--- a/docs/model/trace.yaml
+++ b/docs/model/trace.yaml
@@ -32,7 +32,7 @@ rules:
       - tests/test_method_conformance.py::test_plan_without_system_model_blocks_adoption
     decisions: [docs/decisions/0002-every-project-has-a-checked-system-model.md]
   - id: RULE-MODEL-ELEMENT-IDS
-    statement: A plan's linked system model gives each element a stable ID marked decided or guessed, ends with an unknowns table, and every element is named by a test (an AES verification subject's criterion_refs in an AES target); a miss is a non-blocking warn on CORE-SYSTEM-MODEL until refuse mode.
+    statement: A plan's linked system model gives each element a stable ID marked decided or guessed, ends with an unknowns table, and every element is named by a test (in an AES target, a verification subject's criterion_refs, directly or through a success criterion whose target_refs lists the element); a miss is a non-blocking warn on CORE-SYSTEM-MODEL until refuse mode.
     owner: plugins/company-planning/scripts/method_conformance/model_elements.py
     checks:
       - tests/test_quick_adopt_checks.py::test_quick_adopt_warns_when_model_has_no_element_ids
@@ -40,12 +40,14 @@ rules:
       - tests/test_quick_adopt_checks.py::test_model_without_unknowns_table
       - tests/test_quick_adopt_checks.py::test_element_without_test_names_only_the_untested_one
       - tests/test_quick_adopt_checks.py::test_aes_target_coverage_comes_from_verification_subjects
+      - tests/test_quick_adopt_checks.py::test_aes_normative_item_is_covered_through_a_criterion_target_refs
     decisions: [docs/decisions/0002-every-project-has-a-checked-system-model.md]
   - id: RULE-ELEMENT-STATUS-FROM-RUN
-    statement: An element's shown status comes from a recorded run; the model status page shows the standing AES evidence.assess() reports for each element ID and computes none itself (an ID AES does not track is shown as Not tracked).
+    statement: An element's shown status comes from a recorded run; the model status page shows the standing AES evidence.assess() reports for each element ID (for a normative item, the least favourable standing of the success criteria whose target_refs list it) and computes no standing of its own (an ID AES does not track is shown as Not tracked).
     owner: plugins/company-planning/scripts/model_status_page.py
     checks:
       - tests/test_model_status_page.py::test_each_element_gets_exactly_the_aes_standing
+      - tests/test_model_status_page.py::test_element_judged_through_criteria_takes_the_least_favourable_standing
       - tests/test_model_status_page.py::test_not_an_aes_target_reads_no_standings
       - tests/test_model_status_page.py::test_page_words_colours_tooltips_and_footer
     decisions: [docs/decisions/0002-every-project-has-a-checked-system-model.md]
```

Full diff of declared role `plans` (`docs/plans/policy-enforcement-pilot.md`), plan commits only:

```diff
commit d93e941 [Goal policy-enforcement-pilot] Adopt the policy enforcement pilot plan (steps 1-5)

diff --git a/docs/plans/policy-enforcement-pilot.md b/docs/plans/policy-enforcement-pilot.md
new file mode 100644
index 0000000..0c911fe
--- /dev/null
+++ b/docs/plans/policy-enforcement-pilot.md
@@ -0,0 +1,220 @@
+---
+schema_version: "1.0"
+artifact_type: design_plan
+id: policy-enforcement-pilot
+status: proposed
+method_conformance_receipt: docs/plans/policy-enforcement-pilot.receipt.json
+trace_review_criteria:
+  - criterion_id: outcome
+    expected_outcome: pass
+goal:
+  outcome: "Plan, build and review rules are checked by code, not self-attested: a plan whose system model has no element IDs is flagged at adoption, every model element shows a status computed from the last test run, and each review point links a generated status page."
+  canonical_example: "qualitative_coding slice 1: an intent model naming element QC-QUOTE-MEETS-RULE; the warn-mode adoption check flags it as having no covering test; after a test is tagged and run, the generated status page shows QC-QUOTE-MEETS-RULE as failing because CodeApplication has no meets/fails field (qc issue 130, item 1)."
+  forbidden_substitutes: "A status page typed by hand; a checklist item marked pass without its check running (company-planning issue 119); a demo on a fixture model instead of qualitative_coding; a check that only confirms a file exists or a doc was touched (co-change)."
+  boundaries: "Writes only company-planning (this worktree), AES canonical proposals/model-framework, and qualitative_coding on its own branch. Checks stay in warn mode until step 4 passes. No push to the Inside-Success mirror by hand; no deletes of data or history."
+  done_when: "Step 4 run on qualitative_coding slice 1, its full output saved in docs/plans/policy-enforcement-pilot.check.txt: the warn-mode adoption check and the status computation both run, and the trace shows each check invocation, the element IDs it read, and its findings; the findings list names both qc issue 130 disagreements (items 1 and 2) without the check being given that issue; the generated status page lists every slice-1 element with a status traced to a test id; durable_docs_check.py --repo . --plan docs/plans/policy-enforcement-pilot.md --range cdcf6c7d604d3dc8d1a34871a582359b86311ea8..HEAD exits 0 with output in the same file."
+  do_not_gate_on: "Brian opening the diagram (step 2) or the status page (step 4); applying the rules to a second project; adoption by other agents."
+---
+
+# Policy enforcement pilot: checked plan, build and review rules
+
+Each section below answers the checklist items quoted in it; the gate judges only that
+section's text. Replace every `TODO(answer ...)` line before running `cli.py check`. Quote
+values in the front matter: an unquoted ` #` starts a YAML comment and cuts the value.
+
+## Actor and result
+
+> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.
+
+**Actor:** Brian, who steers agent-built projects but cannot read their code, and the agents that plan, build and review under company-planning.
+
+**Result:** the three phase rules are checked by code rather than written as "pass" by the agent:
+- Plan: a plan's system model names its elements with stable IDs, marks each decided or guessed, and lists open unknowns with what would decide them.
+- Build: each element is covered by at least one named test, and its status (passing, failing, untested) is computed from the last run.
+- Review: each review point links a generated status page listing every element and its computed status.
+
+**Example (the canonical example in the front matter):** on qualitative_coding slice 1 the intent model names `QC-QUOTE-MEETS-RULE` ("every quote records whether it meets the rule"). The warn-mode adoption check flags it as untested. After a test tagged with that ID runs, the generated status page shows it failing, because `qc_clean/schemas/domain.py` CodeApplication has no meets/fails field (qc issue 130, item 1). Brian opens that page and sees one line in orange saying so.
+
+## Requirements
+
+> **CORE-REQUIREMENTS-TRACED** (blocking): The plan lists its requirements: what was asked for, and what the delivered work's own claims imply. A claim here is what the work is presented as being or doing to its users, for example work presented as following a standard, schema or contract (which implies conformance to it) or an output labelled as showing something (which implies it shows it correctly); the plan's own format and front matter are not such claims, and the details a check examines (what a trace must show) belong to that check rather than being separate requirements. Each requirement names the check that verifies it (a test, script, gate step, or named review of a run) and its status: passing, failing, planned and not yet run, or deferred with a stated reason; deferred requirements are carried onto every release or completion record the plan names. A plan fails this item if it has no requirements list, if any requirement has neither a check nor an explicit deferral with its reason, or if the plan presents the work as following a named standard, schema or contract, or as having another property its users rely on, that its requirements list omits.
+
+| # | Requirement | Source | Check that verifies it | Status |
+|---|---|---|---|---|
+| R1 | Pick how "element ID → test → status" is recorded, incumbent first (agent_ecology2 `relationships.yaml` + `check_doc_coupling.py`), then sphinx-needs, StrictDoc, OpenFastTrace, Doorstop, pytest markers + JUnit XML, AES `verification_subjects` | Brian 2026-10-10 ("is this ... doc_graph ... relevant"; "i approve") | Step 1 disposition table committed to AES `proposals/model-framework/README.md` §9, one row per candidate with reuse/extend/reject and reason | planned, not run |
+| R2 | The three rules (plan, build, review above) written as one amendment to decision 0002 and `distribution/references/system-model.md` | README §9 step 2 | `durable_docs_check.py` (decisions role changed in range) and a grep for each rule's ID in both files, output in `docs/plans/policy-enforcement-pilot.check.txt` | planned, not run |
+| R3 | Quick-adopt stops writing "pass" for items it did not check (fixes #119) | company-planning issue 119 | New test `tests/test_quick_adopt_checks.py`: a quick-adopt request whose model has no element IDs gets a `warn` disposition on CORE-SYSTEM-MODEL, not `pass` | planned, not run |
+| R4 | Adoption check (warn mode) flags model elements with no ID, no decided/guessed mark, or no covering test | step 3 | Same test file: three fixture models, each missing one property, each produces exactly the expected finding code | planned, not run |
+| R5 | Status computation: each element's status comes from the last recorded test run, never from prose | step 3 | Test: a fixture run with one failing tagged test yields that element `failing`; removing the run yields `untested`, not `passing` | planned, not run |
+| R6 | Generated review status page from the computed statuses | step 3 | Playwright check (pattern: `world_builder_e2e.mjs tooltips`) that every element row renders with its status and a hover tooltip; blue/orange/grey only | planned, not run |
+| R7 | Stress test on qualitative_coding slice 1 catches qc issue 130 items 1 and 2 unaided | step 4 | The step-4 run's saved output: the findings list names both, and the run's inputs (saved with it) do not include issue 130's text | planned, not run |
+| R8 | First model for slice 1 costs at most 3 agent hours | decision 0002 wrong-when | Start and end commit timestamps of the slice-1 model work, recorded in `docs/plans/policy-enforcement-pilot.check.txt` | planned, not run |
+| R9 | Checks switch from warn to refuse only after R7 passes | step 5 | Test: with refuse mode on, the R4 fixtures are REFUSED by `cli.py adopt` | planned, not run |
+| R10 | Plans with pictures, reviews on a working UI (workspace AGENTS.md) are covered by R6 for review; plan-with-pictures stays prose | workspace AGENTS.md | deferred: no check in this pilot, because the diagram rule needs a separate decision on what counts as a picture; carried on the completion record |
+
+## Success and disproof
+
+> **CORE-SUCCESS-DISPROOF** (blocking): The plan defines the evidence that would show success and a concrete condition that would disprove the approach. Each success measure is the property the plan claims, or a check that directly tests that property, not a stand-in for it: a count, a picture, a readability judgment, or the pipeline agreeing with itself (hashes, labels, byte equality) does not show correctness or conformance it does not test. A plan fails this item if it has no disproof condition, or if a success measure is such a stand-in for the claimed property and the plan names no direct check of that property.
+
+> **CORE-TRACE-REVIEW** (blocking): Every success or acceptance criterion in the plan is judged from the full trace of a run, not only its final outcome: it names the run whose full trace is examined (for example the session, its tool and LLM calls, commits, check output, or messages), where that trace lives, and what must be seen in that trace beyond the final outcome. A criterion that names only an outcome, such as tests passing, a PR merged, a test fixture reproducing the journey, or a status reading succeeded, fails this item. A criterion for which no run exists, such as a pure document edit, passes only when the plan states that exemption and its reason explicitly.
+
+**Success:** R7 directly tests the claimed property ("the checks catch real goal-vs-code disagreements") on a project whose disagreements were found independently before the checks existed (qc issue 130, found 2026-10-10 by hand). R3–R5 test each check's property with fixtures where the trivial answer (pass everything, or pass on file existence) is wrong.
+
+**Disproof (any one ends the approach as designed):**
+- the step-4 run misses either qc issue 130 item 1 or item 2;
+- the first slice-1 model takes more than 3 agent hours (R8);
+- the status page shows an element as passing whose covering test did not run in the recorded run.
+
+Not success measures: the number of elements, the page looking good, or `cli.py check` printing READY.
+
+- **R1, R2 (document edits):** exempt from a run trace: they are decisions and prose. Their check is the committed disposition table and `durable_docs_check.py` output in `docs/plans/policy-enforcement-pilot.check.txt`.
+- **R3–R5, R9 (tests):** the run is `uv run pytest tests/test_quick_adopt_checks.py -v` on the change commit; its full output (each test name, its assertion, counts and exit code) is saved in `docs/plans/policy-enforcement-pilot.check.txt`. The trace must show each fixture's finding code, not only "passed".
+- **R6:** the run is the Playwright check; its trace is its console output plus a screenshot path in `docs/plans/policy-enforcement-pilot.check.txt`; it must show each element row and the tooltip text it hovered.
+- **R7, R8 (stress test):** the run is the step-4 session on qualitative_coding: its Claude Code session id, every check invocation with arguments and output, the element IDs read, and the findings, saved in `docs/plans/policy-enforcement-pilot.check.txt`. What must be seen beyond the outcome: the inputs passed to the checks (model file and test results) and the absence of issue 130's text from those inputs.
+
+## When a run fails or surprises us
+
+> **CORE-TRACE-DEBUGGING** (blocking): The plan includes a separate When a run fails or surprises us procedure, distinct from anticipated failure modes. It requires preserving the failed run and its trace id; reading full inputs, prompts, each tool call arguments/results, intermediate stages and final output before selecting a fix; citing the observed divergence; classifying evidence absent, evidence returned but unused or contradicted, invalid expectation, or unresolved; and linking a targeted repair to a new traced verification run while retaining the original failure. Unresolved diagnoses permit investigation but cannot authorize a causal repair. Review completeness is separate from the run verdict.
+
+When a run fails or surprises us:
+1. Keep the failed run: save its full output and session id to `docs/plans/policy-enforcement-pilot.check.txt` under a dated FAILED heading before changing anything.
+2. Read the full trace before choosing a fix: the model file and test results the check read, each command's arguments and output, and the final findings.
+3. Cite the exact line where the run diverged from what was expected.
+4. Classify it: the evidence never reached the check (element or test missing from its input); it reached the check and was not used; the expectation was wrong (for example an issue 130 item is not actually a disagreement); or unresolved.
+5. An unresolved diagnosis allows more investigation, not a fix.
+6. A fix is linked to a new traced run, saved beside the original failure, which stays in the file.
+
+Whether the review was complete is recorded separately from whether the run passed.
+
+## System model
+
+> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: exempt -- <reason>`, which fits only a project with no stored state and no user-facing view. Unless exempt, the plan names each system-model element (entity, process, record or event, or view) that the work adds, changes, or relies on, and its trace review names, for each such element, what the examined run must show of it (for example an event of that record type with its id, or the view displaying that entity). A plan with neither a model link nor the exemption line fails this item, as does one that lists model elements without saying what the examined run must show of each, or one that names no element without stating that the work touches none and why. For a maintained repository, the plan also cites the documentation entry point from which the model is reachable; a shared model explicitly identifies this repository's scope. It names applicable source-linked views, explains material omissions without imposing a fixed diagram quota, names concrete model freshness or drift checks, and states how the model, view coverage and verification evidence will be reconciled in the same change (or gives a concrete reason each needs no update). A bare model path without these discovery, view, freshness and reconciliation obligations fails this item. Representation Router may render selected views but does not supply planning authority or prove executed behavior.
+
+**System model:** `docs/model/ODD.md` (this repository only), reachable from `wiki/index.md`. Decision 0002 (amended 2026-10-10) makes arc42 + C4 the outline for new models; this repository's model is not migrated by this plan.
+
+**Model elements this work adds, changes or relies on, and what the saved run must show of each:**
+- process `quick-adopt` (changes): the R3 test output must show a CORE-SYSTEM-MODEL disposition of `warn` for a model without element IDs.
+- process `adopt` (changes, step 5): the R9 test output must show REFUSED for the same fixture in refuse mode.
+- process `durable-documents check` (relies on it, unchanged): its output in the check file must show exit 0.
+- process `model element check` (adds): the R4 output must show one finding code per fixture.
+- process `status computation` (adds): the R5 output must show the element status per fixture run.
+- record `checklist_item_observation` (changes: new `warn` disposition value): the R3 output must show an observation with that value.
+- view `element status page` (adds): the R6 screenshot and console must show every element row.
+- entities: none added; `plan` and `method profile` are relied on unchanged.
+
+**Views, freshness and reconciliation:** the applicable views, with their source links: the receipt JSON (written by `plugins/company-planning/scripts/method_conformance/gate.py` `evaluate`; changes: shows `warn`) and the new element status page (generated by a new script under `plugins/company-planning/scripts/`, named in step 3 and added to `docs/model/ODD.md` §7 with its path). Omitted views and why they are immaterial: adopt CLI output and check CLI output print each item's disposition generically, so `warn` appears without a code change, and their tests confirm it; the skeleton plan, goal launcher file, lint output, system-model review and durable check output read nothing this work changes. Entities are omitted because no entity is added or changed: `plan` and `method profile` keep their meaning, and the profile only gains a disposition value already described under the record above. The existing drift test `tests/test_system_model.py` runs in the success check. Each process, record or view added above is added to `docs/model/ODD.md` §5–7 in the same commit that adds its code, and the drift test must pass on that commit.
+
+## Capability reuse
+
+> **CORE-CAPABILITY-REUSE** (blocking): The plan answers capability reuse against the capability catalogue in agentic-capability-architecture-canonical, which has two files: `reuse_candidates.yml`, whose entries under `candidates:` are cross-project capabilities with their selected off-the-shelf implementations, each named by its `id` (for example `documents_to_text`) and marked candidate or promoted; and `capability_registry.yml`, whose entries under `capabilities:` are the packages that repository holds, each named by its key (for example `approvals`) with the capability ids it `provides` (for example `approval.resolve`). An entry from either file counts. The plan names each catalogue capability the work reuses, by its id, key or provided id; names each new capability the work adds together with its first consumer (the project, command or workflow in this plan that uses it); and, where no entry covers what the work needs, states `No catalogue entry fits, because <reason>`, the reason saying what the work needs that no entry provides. A plan may give more than one of these answers. A plan fails this item if it gives none of them, if it claims reuse without naming the catalogue entry or id reused (reusing code or a contract that is not a catalogue entry does not count), if it adds a capability without naming its first consumer, or if it says no entry fits without a reason.
+
+Checked against the capability catalogue in agentic-capability-architecture-canonical (`reuse_candidates.yml` and `capability_registry.yml`):
+
+- No catalogue entry fits, because what the work needs is traceability from a model element ID to a test result and a computed status, and the catalogue holds no requirements-traceability or test-status capability; the incumbent in Brian's repos (agent_ecology2 `relationships.yaml` + `check_doc_coupling.py`, in 37 repos) is not a catalogue entry and is assessed under prior art.
+- New capability, if step 1 selects building rather than adopting: `model element status` (element ID → covering test → status). First consumer: qualitative_coding slice 1 in step 4 of this plan. If step 1 picks an off-the-shelf tool it is proposed as a catalogue candidate in the same change.
+
+## Authority and non-goals
+
+> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).
+
+**Authority:** Brian (asked for this 2026-10-10: "i am mroe interested in cgeting the plannign and implementation and review policeis figured otu and enforced"; approved this plan 2026-10-10: "i approve"). Company-planning owns the checklist and checks; AES canonical owns the design record; qualitative_coding is only the test subject.
+
+**Non-goals:**
+- Not improving qualitative_coding beyond slice 1's models and tagged tests (its fixes for issue 130 are its own work).
+- Not migrating any existing ODD.md model to arc42.
+- Not turning on refuse mode before step 4 passes, and not rolling out to other projects in this plan.
+- No checklist item for "plan with pictures" (R10, deferred).
+
+## Irreversible actions and spend
+
+> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.
+
+None proposed. All changes are git commits, reversible by revert; warn mode precedes refuse. No paid services, no deploy beyond committed review pages served from git, no data deletion. If step 1 picks a paid tool, that becomes a separate spend decision raised to Brian before any purchase.
+
+## Uncertainties
+
+> **CORE-UNCERTAINTIES** (blocking): The plan lists its material uncertainties, and each one has an owner or the evidence that would resolve it.
+
+| Uncertainty | Owner | What resolves it |
+|---|---|---|
+| Whether extending the incumbent doc graph beats an off-the-shelf tool | this lane, step 1 | The step 1 disposition table, judged on: links element to test (not file to file), computes status from a run, works across repos |
+| Whether the 47 `relationships.yaml` copies have diverged | this lane, step 1 | Diff the copies' schema keys against agent_ecology2's |
+| Whether element-level checks catch issue 130's disagreements unaided | this lane, step 4 | R7 run |
+| Whether the model cost stays at 3 agent hours or less | this lane, step 4 | R8 timestamps |
+| Whether the hours estimate (11–16 h, ±50%, unmeasured) holds | this lane | Per-step start/end commit times recorded in the check file |
+| Interaction with the codex lane `trace-review-provider-guards` in this repository | this lane | `check_coordination_claims.py --check` before each step's first commit; message that session if paths overlap |
+
+## Activation facts
+
+> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend. claims_external_standard is triggered when the plan claims, or presents its work as, following, implementing or conforming to a standard, schema or contract owned outside the repository being changed (for example a model presented as DM2, or output said to match a published schema); conforming to the repository's own contracts does not trigger it; aes_governed_target when the target repository is governed by an AES target (`.aes/target.yaml`). These two facts are optional: an undeclared one is shown as false and is judged like a declared false.
+
+- shared_mechanism: true (new checks every plan's adoption runs).
+- empirical_comparison_proposed: false. Step 1 is a landscape review by reading; R7 checks the built result against a known expected outcome, which is verification, not a comparison among alternatives.
+- llm_central: false. The checks are deterministic code; the existing semantic verifier is unchanged.
+- irreversible_or_spend_action: false (see Irreversible actions and spend).
+- aes_governed_target: false. The target repository is company-planning, which has no `.aes/target.yaml`. The AES canonical writes are only to `proposals/model-framework/`, outside its governed roots (`src/agentic_engineering_system/`, `tests/greenfield/`), so its AES target does not govern them; qualitative_coding has no `.aes/target.yaml` (checked 2026-10-10).
+- claims_external_standard: false. The work follows this repository's own decision 0002; it does not claim conformance to sphinx-needs, StrictDoc or any outside standard. If step 1 adopts one, the plan is amended and this fact re-declared true before step 3.
+
+## Prior art and ownership
+
+> **OV-PRIOR-ART-DISPOSITION** (blocking): Existing ownership, internal lineage, and relevant external prior art were searched, and each candidate found is dispositioned as reuse, extend, compose, supersede, or bounded exception.
+
+> **OV-PRIOR-ART-PARALLEL-CHECK** (advisory): The plan names one concrete structural check or consumer-path observation that would detect a silent parallel implementation of the same concern.
+
+| Candidate | Where | Disposition |
+|---|---|---|
+| agent_ecology2 doc graph: `scripts/relationships.yaml`, `check_doc_coupling.py`, `validate_relationships.py` | 47 / 37 repos in ~/code | **extend** (leading candidate, evaluated first in step 1): add element-to-test edges; its co-change check is a stand-in and is not reused as the correctness check |
+| agent_ecology2 META-ADR-0005 context compression ("domain model vs code drift" listed as missing; layer justification test) | `docs/visualizations/context_compression.html` | **reuse** as rationale: its three-part layer test becomes part of the rules in step 2 |
+| AES v0.2 `verification_subjects` + `.aes/observations` (status computed from recorded runs) | AES canonical `.aes/target.yaml` | **compose**: candidate record shape for status; assessed in step 1 |
+| company-planning CORE-SYSTEM-MODEL and quick-adopt | this repository | **extend**: the checks land inside the existing gate, not beside it |
+| pytest markers + JUnit XML (`pytest --junitxml`) | external, standard pytest | **compose** (default record of runs): a marker carries the element ID, JUnit XML carries the result; no new dependency |
+| sphinx-needs | external | **bounded exception** (not adopted): needs a Sphinx docs build; these repos use Markdown with a hand-kept wiki. Step 1 may overturn this with evidence |
+| StrictDoc | external | **bounded exception** (not adopted): own `.sdoc` format beside Markdown models. Step 1 re-checks its Markdown and test-link support |
+| OpenFastTrace | external | **bounded exception** (not adopted): Java tool, adds a JVM to Python repos. Step 1 may overturn |
+| Doorstop | external | **bounded exception** (not adopted): one YAML file per item, against the workspace rule against thousands of small files. Step 1 may overturn |
+| project-meta context-engineering design (`CONTEXT_ENGINEERING_AND_DERIVED_DOCUMENTATION_2026-08-24.md`) | project-meta | **compose**: its `required_reading`/`navigation` blocks in `relationships.yaml` stay as they are; element-to-test edges are added beside them, and step 1 confirms no conflict |
+
+Structural check: `git grep -l 'element_id\|verification_subject\|relationships.yaml'` across company-planning, AES canonical and qualitative_coding at step 3; any second mechanism recording element-to-test links besides the one step 1 selects is a parallel implementation and is merged or retired in the same step.
+
+## Coordination
+
+> **OV-COORD-OWNERSHIP** (blocking): The plan names exact ownership, dependencies, conflict surfaces, the integration owner, and the work-unit evidence for each concurrent writer.
+
+- **This lane:** claude-code session `model-framework`, claim `company-planning:policy-enforcement-pilot` (write paths `docs/plans/policy-enforcement-pilot*`; extended to the check code paths in step 3 by a new claim before editing them), parent lane `agentic-engineering-system-canonical:shaping/model-framework`. Integration owner: this lane.
+- **Concurrent writer:** codex claim `company-planning:trace-review-provider-guards` (write paths `.company-planning/active-execution.json`, `.company-planning/history`, `artifacts/trace_review/reviews`, `proposals/trace-review-enforcement`); work-unit evidence: `check_coordination_claims.py --check --project company-planning` output, 2026-10-10. No path overlap. Conflict surface: `CORE-TRACE-REVIEW` semantics; if step 3 touches trace-review code, message that session first.
+- **Dependencies:** step 3 depends on step 1's choice and step 2's rule text; step 4 depends on step 3 code merged to company-planning main; step 5 depends on R7 passing.
+- **qualitative_coding (BrianMills2718/qc), concurrent writer:** claude-code claim `qualitative_coding:durable-docs` (program; "AES M5 durable document set"; write paths `.agentic/repo.yaml`, `docs/architecture`, `docs/model`, `docs/adr`, `wiki/index.md`; expires 2026-10-12T02:28Z). Work-unit evidence: `check_coordination_claims.py --check --project qualitative_coding` output, 2026-10-10. Conflict surface: `docs/model/`, where step 4 would put slice 1's intent model. Resolution: before step 4, message that session via `ListAgents`/`SendMessage`; step 4 either writes its model inside that lane's structure with its agreement or, if the claim is still live and unanswered, writes to `docs/model/slice1/` on its own branch `goal/policy-pilot-slice1` under a child claim on paths `docs/model/slice1/` and `tests/model/`. This lane's own qc write paths: `docs/model/slice1/`, `tests/model/` only.
+
+## Contracts and dependencies
+
+> **OV-CONTRACTS-SCHEMAS** (blocking): For each system boundary the plan crosses, it names every schema or contract the crossing uses or changes, with its owner and its file or URL, and says whether this plan changes it.
+
+> **OV-CONTRACTS-DEPENDENCIES** (blocking): The plan names the dependencies on each side of every boundary it crosses (what produces and what consumes each schema or contract) and the order in which the changes land so no consumer breaks in between.
+
+| Boundary | Schema or contract | Owner, file | Changed by this plan? |
+|---|---|---|---|
+| plan → adoption gate | method profile `bounded-design` | company-planning, `plugins/company-planning/contracts/method-conformance/profiles/bounded-design.json` | yes, step 3 (warn disposition for element checks) and step 5 (refuse) |
+| gate → receipt readers | `checklist_item_observation` / receipt JSON | company-planning, `plugins/company-planning/contracts/method-conformance/planning-method-conformance-receipt.v1.schema.json` | yes: adds `warn` disposition value, step 3 |
+| system model file → element check | element ID / decided-guessed / unknowns rules | company-planning, `docs/decisions/0002-every-project-has-a-checked-system-model.md` and `plugins/company-planning/distribution/references/system-model.md` | yes, step 2 |
+| test run → status computation | default: a pytest marker `@pytest.mark.element("<ID>")` on each covering test, plus the JUnit XML file pytest writes | pytest (JUnit XML format, https://docs.pytest.org/en/stable/how-to/output.html#creating-junitxml-format-files); the marker is registered in each repo's `pyproject.toml` | no change to JUnit XML; adds the marker registration |
+| (not used at this boundary) doc graph | agent_ecology2 `scripts/relationships.yaml` | no: this plan as adopted neither uses nor changes it. If step 1 selects extending it, that is a contract change, and the plan is amended and re-adopted before step 3 |
+| qualitative_coding models and tests → checks | the same rules as consumed | qc repo (BrianMills2718/qc), `docs/model/slice1/intent.md` (new file, step 4; path confirmed with the `durable-docs` lane) | yes, step 4 creates it |
+| status computation → status page and review point | computed statuses file, one JSON record per element (`element_id`, `status`, `test_ids`, `run_ref`) | company-planning; schema file `plugins/company-planning/contracts/method-conformance/element-status.v1.schema.json` (new) | yes, step 3 creates it |
+
+Per contract (producer → consumer):
+- method profile `bounded-design.json`: produced by this lane's commits → consumed by `compiler.py` `compile_profile` and every `cli.py adopt`/`quick-adopt` run.
+- receipt JSON / `checklist_item_observation`: produced by `gate.py` `evaluate`/`record_observation` → consumed by `plan_execution_supervisor.py`, `cli.py lint`, the adopt and check CLI output.
+- element rules (decision 0002 + `system-model.md`): produced by step 2 → consumed by the new model element check and by agents writing models.
+- element marker + JUnit XML: produced by pytest runs in the target repo (qc in step 4) → consumed by the status computation.
+- computed statuses: produced by the status computation → consumed by the element status page and the review point that links it.
+- Landing order so no consumer breaks: (1) step 2 rule text (docs only); (2) receipt schema gains `warn` as an allowed value, with receipt readers tested to treat `warn` as non-blocking, before any check emits it; (3) the checks emit `warn`; (4) status computation and page; (5) step 4 on qc; (6) only then the profile turns `warn` into a blocking `fail`. Each lands as its own commit with tests passing.
+
+## Durable documents
+
+> **OV-DURABLE-DOCS-DECLARED** (blocking): The adopting repository declares durable documents (a `durable_documents` block in `.agentic/repo.yaml`). The plan carries a `Durable documents:` line that names each durable role it updates, with the system-model rule or element ID where the role is the system model (for example `Durable documents: system_model#RULE-LOAN-OVERDUE, decisions`), or says `Durable documents: none -- <reason>` with a reason that explains why the work changes no goal, requirement, rule, decision or other durable document. Each named role is one the repository declares. The plan's success evidence or done-when includes running `durable_docs_check.py --plan <this plan> --range <adoption revision>..HEAD` at completion and requires it to exit 0. A plan fails this item if the line is missing, if `none` has no reason or a reason that does not explain why no durable document changes, if a named role is not declared, or if the completion check is not part of its success evidence.
+
+This repository declares durable documents (`durable_documents` in `.agentic/repo.yaml`): `goal`, `requirements`, `system_model`, `decisions`, `plans`.
+
+Durable documents: decisions, system_model#quick-adopt, system_model#adopt, plans
+
+At completion, `python3 plugins/company-planning/scripts/durable_docs_check.py --repo . --plan docs/plans/policy-enforcement-pilot.md --range cdcf6c7d604d3dc8d1a34871a582359b86311ea8..HEAD` must exit 0; its full output is appended to `docs/plans/policy-enforcement-pilot.check.txt`.
commit 8b850ed [Goal policy-enforcement-pilot] WIP: amend plan for step 1 result before merging main

diff --git a/docs/plans/policy-enforcement-pilot.md b/docs/plans/policy-enforcement-pilot.md
index 0c911fe..a13de89 100644
--- a/docs/plans/policy-enforcement-pilot.md
+++ b/docs/plans/policy-enforcement-pilot.md
@@ -30,7 +30,7 @@ values in the front matter: an unquoted ` #` starts a YAML comment and cuts the
 
 **Result:** the three phase rules are checked by code rather than written as "pass" by the agent:
 - Plan: a plan's system model names its elements with stable IDs, marks each decided or guessed, and lists open unknowns with what would decide them.
-- Build: each element is covered by at least one named test, and its status (passing, failing, untested) is computed from the last run.
+- Build: each element is covered by at least one named test, and its status is computed from the last recorded run by AES `evidence.assess()`: SUPPORTED (passing), REFUTED (failing) or INSUFFICIENT (untested, or the recorded run is stale).
 - Review: each review point links a generated status page listing every element and its computed status.
 
 **Example (the canonical example in the front matter):** on qualitative_coding slice 1 the intent model names `QC-QUOTE-MEETS-RULE` ("every quote records whether it meets the rule"). The warn-mode adoption check flags it as untested. After a test tagged with that ID runs, the generated status page shows it failing, because `qc_clean/schemas/domain.py` CodeApplication has no meets/fails field (qc issue 130, item 1). Brian opens that page and sees one line in orange saying so.
@@ -41,16 +41,18 @@ values in the front matter: an unquoted ` #` starts a YAML comment and cuts the
 
 | # | Requirement | Source | Check that verifies it | Status |
 |---|---|---|---|---|
-| R1 | Pick how "element ID → test → status" is recorded, incumbent first (agent_ecology2 `relationships.yaml` + `check_doc_coupling.py`), then sphinx-needs, StrictDoc, OpenFastTrace, Doorstop, pytest markers + JUnit XML, AES `verification_subjects` | Brian 2026-10-10 ("is this ... doc_graph ... relevant"; "i approve") | Step 1 disposition table committed to AES `proposals/model-framework/README.md` §9, one row per candidate with reuse/extend/reject and reason | planned, not run |
+| R1 | Pick how "element ID → test → status" is recorded, incumbent first (agent_ecology2 `relationships.yaml` + `check_doc_coupling.py`), then sphinx-needs, StrictDoc, OpenFastTrace, Doorstop, pytest markers + JUnit XML, AES `verification_subjects` | Brian 2026-10-10 ("is this ... doc_graph ... relevant"; "i approve") | Step 1 disposition table committed to AES `proposals/model-framework/README.md` §9, one row per candidate with reuse/extend/reject and reason | done 2026-10-10: reuse AES v0.2 evidence (AES canonical commit a5b8b3611, `proposals/model-framework/README.md` §9 "Step 1 result") |
 | R2 | The three rules (plan, build, review above) written as one amendment to decision 0002 and `distribution/references/system-model.md` | README §9 step 2 | `durable_docs_check.py` (decisions role changed in range) and a grep for each rule's ID in both files, output in `docs/plans/policy-enforcement-pilot.check.txt` | planned, not run |
 | R3 | Quick-adopt stops writing "pass" for items it did not check (fixes #119) | company-planning issue 119 | New test `tests/test_quick_adopt_checks.py`: a quick-adopt request whose model has no element IDs gets a `warn` disposition on CORE-SYSTEM-MODEL, not `pass` | planned, not run |
 | R4 | Adoption check (warn mode) flags model elements with no ID, no decided/guessed mark, or no covering test | step 3 | Same test file: three fixture models, each missing one property, each produces exactly the expected finding code | planned, not run |
-| R5 | Status computation: each element's status comes from the last recorded test run, never from prose | step 3 | Test: a fixture run with one failing tagged test yields that element `failing`; removing the run yields `untested`, not `passing` | planned, not run |
+| R5 | Status computation: each element's status comes from the last recorded test run, never from prose. Reused, not built: AES v0.2 `aes evidence record` / `aes evidence status` (`evidence.assess()`), element ID = AES criterion ID; SUPPORTED = passing, REFUTED = failing, INSUFFICIENT = untested or stale | step 1 result | In qc (step 4): `aes evidence record` on a deliberately failing element test yields that criterion REFUTED; an element with no recorded run reads INSUFFICIENT, not SUPPORTED; both lines saved in the check file | planned, not run |
 | R6 | Generated review status page from the computed statuses | step 3 | Playwright check (pattern: `world_builder_e2e.mjs tooltips`) that every element row renders with its status and a hover tooltip; blue/orange/grey only | planned, not run |
 | R7 | Stress test on qualitative_coding slice 1 catches qc issue 130 items 1 and 2 unaided | step 4 | The step-4 run's saved output: the findings list names both, and the run's inputs (saved with it) do not include issue 130's text | planned, not run |
 | R8 | First model for slice 1 costs at most 3 agent hours | decision 0002 wrong-when | Start and end commit timestamps of the slice-1 model work, recorded in `docs/plans/policy-enforcement-pilot.check.txt` | planned, not run |
 | R9 | Checks switch from warn to refuse only after R7 passes | step 5 | Test: with refuse mode on, the R4 fixtures are REFUSED by `cli.py adopt` | planned, not run |
-| R10 | Plans with pictures, reviews on a working UI (workspace AGENTS.md) are covered by R6 for review; plan-with-pictures stays prose | workspace AGENTS.md | deferred: no check in this pilot, because the diagram rule needs a separate decision on what counts as a picture; carried on the completion record |
+| R10 | Plans with pictures, reviews on a working UI (workspace AGENTS.md) are covered by R6 for review; plan-with-pictures stays prose | workspace AGENTS.md | deferred: no check in this pilot, because the diagram rule needs a separate decision on what counts as a picture; carried onto both completion records this plan names: the final section of `docs/plans/policy-enforcement-pilot.check.txt` and the closeout section of `docs/plans/policy-enforcement-pilot.goal.md` |
+| R11 | (implied by the work's claims) Element status uses AES v0.2's target, verification-subject and observation contracts unchanged, so qc's `.aes/` conforms to them | follows from R5 and the claims_external_standard fact | `aes target validate` and `aes topology check`, run by qc's pre-commit hook (installed by `aes hooks install` in step 4) on every qc commit, plus `aes plan validate` on each qc proposal (dry run passing: `docs/plans/policy-enforcement-pilot.aes-validate.txt`) | dry run passing 2026-10-11; on qc, planned, not run |
+| R12 | (implied by the work's claims) The status page shows exactly what the last recorded run showed, no element shown passing whose test did not run | the page is labelled as showing element status | The R6 Playwright check also compares every row's status with `evidence.assess()` output for the same revision, and a fixture with one unrun element must show it INSUFFICIENT (grey), not SUPPORTED | planned, not run |
 
 ## Success and disproof
 
@@ -61,15 +63,24 @@ values in the front matter: an unquoted ` #` starts a YAML comment and cuts the
 **Success:** R7 directly tests the claimed property ("the checks catch real goal-vs-code disagreements") on a project whose disagreements were found independently before the checks existed (qc issue 130, found 2026-10-10 by hand). R3–R5 test each check's property with fixtures where the trivial answer (pass everything, or pass on file existence) is wrong.
 
 **Disproof (any one ends the approach as designed):**
+- after step 4, `aes target validate`, `aes topology check` or `aes status` reports a violation on qc's `.aes/` (an artifact labelled as conforming to AES breaks one of its rules);
 - the step-4 run misses either qc issue 130 item 1 or item 2;
 - the first slice-1 model takes more than 3 agent hours (R8);
 - the status page shows an element as passing whose covering test did not run in the recorded run.
 
+**Claims the delivered work makes, and where each is a requirement:** (R11 and R12 in the Requirements table are these claims; the list below explains them)
+- "A plan cannot be adopted with an untested or failing element once step 5 lands": checked by the R5 fixtures run against `cli.py adopt` after the warn→refuse switch, output in `docs/plans/policy-enforcement-pilot.check.txt`.
+- "The status page shows what the last run showed, not what an agent wrote": checked by the third disproof condition above (an element shown passing whose test did not run ends the approach).
+- "The rules hold on a real project, not just fixtures": checked by R7 on qualitative_coding slice 1.
+- "Element status uses AES v0.2's own records unchanged" (a claim of conformance to the AES observation and target contracts): checked by `aes plan validate` on the qc proposal (passing dry run in `docs/plans/policy-enforcement-pilot.aes-validate.txt`) and, in step 4, by `aes status` and `aes evidence status` on qc, with output saved in `docs/plans/policy-enforcement-pilot.check.txt`.
+- Deferred R10 (plan with pictures) is carried, not dropped. This plan names exactly two completion records, and both carry it as a row in the R10 status: the completion record (`docs/plans/policy-enforcement-pilot.check.txt` final section and the goal doc's closeout) lists R10 as deferred with its reason and its follow-up issue, so the plan cannot read complete without naming it.
+
 Not success measures: the number of elements, the page looking good, or `cli.py check` printing READY.
 
 - **R1, R2 (document edits):** exempt from a run trace: they are decisions and prose. Their check is the committed disposition table and `durable_docs_check.py` output in `docs/plans/policy-enforcement-pilot.check.txt`.
 - **R3–R5, R9 (tests):** the run is `uv run pytest tests/test_quick_adopt_checks.py -v` on the change commit; its full output (each test name, its assertion, counts and exit code) is saved in `docs/plans/policy-enforcement-pilot.check.txt`. The trace must show each fixture's finding code, not only "passed".
 - **R6:** the run is the Playwright check; its trace is its console output plus a screenshot path in `docs/plans/policy-enforcement-pilot.check.txt`; it must show each element row and the tooltip text it hovered.
+- **R10 (deferred):** exempt from a run trace, because no run exists: this pilot builds no check for it, so there is nothing to execute. The exemption holds only while R10 stays deferred; any plan that builds the check must name its run.
 - **R7, R8 (stress test):** the run is the step-4 session on qualitative_coding: its Claude Code session id, every check invocation with arguments and output, the element IDs read, and the findings, saved in `docs/plans/policy-enforcement-pilot.check.txt`. What must be seen beyond the outcome: the inputs passed to the checks (model file and test results) and the absence of issue 130's text from those inputs.
 
 ## When a run fails or surprises us
@@ -96,8 +107,8 @@ Whether the review was complete is recorded separately from whether the run pass
 - process `quick-adopt` (changes): the R3 test output must show a CORE-SYSTEM-MODEL disposition of `warn` for a model without element IDs.
 - process `adopt` (changes, step 5): the R9 test output must show REFUSED for the same fixture in refuse mode.
 - process `durable-documents check` (relies on it, unchanged): its output in the check file must show exit 0.
-- process `model element check` (adds): the R4 output must show one finding code per fixture.
-- process `status computation` (adds): the R5 output must show the element status per fixture run.
+- process `model element check` (adds): the R4 output must show one finding code per fixture; it also flags a model element ID that is not an AES criterion with a verification subject.
+- process `status computation` (reused: AES v0.2 `evidence.assess()`, no new code): the R5 output must show each element's AES standing.
 - record `checklist_item_observation` (changes: new `warn` disposition value): the R3 output must show an observation with that value.
 - view `element status page` (adds): the R6 screenshot and console must show every element row.
 - entities: none added; `plan` and `method profile` are relied on unchanged.
@@ -146,14 +157,87 @@ None proposed. All changes are git commits, reversible by revert; warn mode prec
 
 ## Activation facts
 
-> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend. claims_external_standard is triggered when the plan claims, or presents its work as, following, implementing or conforming to a standard, schema or contract owned outside the repository being changed (for example a model presented as DM2, or output said to match a published schema); conforming to the repository's own contracts does not trigger it; aes_governed_target when the target repository is governed by an AES target (`.aes/target.yaml`). These two facts are optional: an undeclared one is shown as false and is judged like a declared false.
+> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend. claims_external_standard is triggered when the plan claims, or presents its work as, following, implementing or conforming to a standard, schema or contract owned outside the repository being changed (for example a model presented as DM2, or output said to match a published schema); conforming to the repository's own contracts does not trigger it; aes_governed_target when the target repository is governed by an AES target (`.aes/target.yaml`), or the plan creates one (for example by running `aes init`). These two facts are optional: an undeclared one is shown as false and is judged like a declared false.
 
 - shared_mechanism: true (new checks every plan's adoption runs).
-- empirical_comparison_proposed: false. Step 1 is a landscape review by reading; R7 checks the built result against a known expected outcome, which is verification, not a comparison among alternatives.
+- empirical_comparison_proposed: false. Step 1 compared candidate tools by reading their documentation and AES's own status output; it ran no experiment, benchmark or A/B trial, and it is finished (result recorded 2026-10-10 in AES canonical commit a5b8b3611). No remaining step compares alternatives: R7 checks the one built design against an outcome known in advance (qc issue 130), which is verification, not a comparison.
 - llm_central: false. The checks are deterministic code; the existing semantic verifier is unchanged.
 - irreversible_or_spend_action: false (see Irreversible actions and spend).
-- aes_governed_target: false. The target repository is company-planning, which has no `.aes/target.yaml`. The AES canonical writes are only to `proposals/model-framework/`, outside its governed roots (`src/agentic_engineering_system/`, `tests/greenfield/`), so its AES target does not govern them; qualitative_coding has no `.aes/target.yaml` (checked 2026-10-10).
-- claims_external_standard: false. The work follows this repository's own decision 0002; it does not claim conformance to sphinx-needs, StrictDoc or any outside standard. If step 1 adopts one, the plan is amended and this fact re-declared true before step 3.
+- aes_governed_target: true. The fact covers a target the plan creates (bounded-design@13, company-planning plan aes-overlay-creates-target): step 4 runs `aes init` on qualitative_coding. Today neither repository this plan changes has `.aes/` (checked 2026-10-11), so the [AES target](#aes-target) section gives the whole new target as the delta, validated by `aes plan validate` after the same `aes init` on a scratch copy; requirements that change only company-planning map to its own named checks.
+- claims_external_standard: true. Element status is recorded in AES v0.2's target, verification-subject and observation contracts, which AES canonical owns, not company-planning. The plan claims conformance to those contracts only; [AES target](#aes-target) names them, and `aes plan validate` / `aes status` check them. It claims no outside standard such as sphinx-needs, StrictDoc, OpenFastTrace, Doorstop or an ISO/IEEE norm; step 1 rejected adopting one.
+
+## Standard conformance
+
+> **OV-STANDARD-CONFORMANCE-RULES / -GATE** (blocking): see the profile; this section is the evidence.
+
+**Contract followed:** AES v0.2's records. AES canonical (BrianMills2718/agentic-engineering-system-canonical) owns them, not company-planning. There are three:
+- the target (`.aes/target.yaml`), with its outcomes, normative items, success criteria, evidence requirements, components, planned artifacts and verification subjects;
+- the proposal (`.aes/plans/*.yaml`);
+- the observation record (`.aes/observations/*.yaml`).
+
+**Where the machine-readable rules live:** the Pydantic models in AES canonical `src/agentic_engineering_system/records.py` (Target, Proposal and their items) and `src/agentic_engineering_system/evidence.py` (observations, standings, freshness). The installed `aes` CLI applies them. No separate written rule set is needed.
+
+**Rules qc's artifacts must satisfy:**
+- the target loads strictly, and every reference resolves;
+- every evidence requirement has a route to a verification subject;
+- every tracked file under `docs/model/slice1/` and `tests/model/` is a planned artifact with that exact path;
+- each verification subject's locator is an existing test file;
+- observations are written only by `aes evidence record` and name a commit reachable from qc's main branch.
+
+**Gate:** qc's merge gate is its local `make check` (hosted CI is not relied on). Step 4 adds `aes target validate && aes topology check && aes status` to that target, so every qc PR merge runs the conformance check, and a failure blocks the merge. Additionally, qc's pre-commit hook, which `aes hooks install` installs in step 4, runs `aes target validate` and `aes topology check` on every commit. It refuses the commit on any violation. Each qc proposal also passes `aes plan validate` before `aes plan accept`. The step-4 completion check runs `aes status` and saves its output in `docs/plans/policy-enforcement-pilot.check.txt`. qc PRs that carry observations merge with a merge commit, never a squash, so those observations stay reachable.
+
+**Disproof addition:** after step 4, `aes target validate`, `aes topology check` or `aes status` reports a violation on qc's `.aes/`, meaning an artifact labelled as conforming breaks a rule.
+
+**Extension rules (company-planning's own, not AES):** the decided/guessed mark, the element ID rule and the unknowns table. They are written rules with no machine-readable schema today. Step 2 writes them into `docs/decisions/0002-every-project-has-a-checked-system-model.md` and `plugins/company-planning/distribution/references/system-model.md`. Step 3's model element check encodes them, and its fixtures are in `tests/test_quick_adopt_checks.py`. The artifact that must satisfy them is `docs/model/slice1/intent.md` in qc.
+
+**Labelling rule, in the artifacts as well as the plan:**
+- `intent.md` opens with a line, "Extensions to AES v0.2: decided/guessed marks and the unknowns table follow company-planning decision 0002; they are not AES fields."
+- the status page carries the footer, "Status from AES `evidence.assess()`; the page itself is a company-planning view, not part of AES."
+- step 4's check greps both artifacts for those lines and saves the output in `docs/plans/policy-enforcement-pilot.check.txt`. A missing label fails step 4.
+
+**Extensions (not part of AES, labelled as such):**
+- decided/guessed marks and the unknowns table live in `docs/model/slice1/intent.md`. They are company-planning decision 0002 rules, not AES fields.
+- the status page is a company-planning view over `assess()`. AES does not define it.
+- the model file is planned as AES kind `configuration`, because AES has no documentation kind (AES issue #525). This is a labelling workaround, not an AES rule.
+
+## AES target
+
+> **OV-AES-TARGET-TRACE** (blocking): see the profile; this section is the evidence.
+
+**Which target, and its state today:** the AES target is qualitative_coding (BrianMills2718/qc). It is **not governed yet**: qc has no `.aes/target.yaml` (checked 2026-10-11). This plan creates the target in step 4, so the fact is declared true for what the plan does, not for the starting state. Step 4 runs `aes init --project-id qualitative-coding --governed-root docs/model/slice1/ --governed-root tests/model/`. The governed roots are kept narrow so the rest of qc (its pipeline code and other docs) does not have to be planned first. company-planning stays outside AES and is not given a target by this plan; its own work is checked by its own tests (see the mapping table).
+
+**Target delta (the whole new target; adds only, because the target is new):** `aes init` writes the target with its one outcome `OUT-001` ("Every quote records whether it meets the rule it was coded under", for Brian reviewing qc slice 1, as the dry-run `aes init` wrote it); every addition below traces to `OUT-001`. Then  [`policy-enforcement-pilot.aes-proposal.yaml`](policy-enforcement-pilot.aes-proposal.yaml) (`PLAN-QC-SLICE1-MODEL`) adds 10 items:
+- normative items `QC-QUOTE-MEETS-RULE` (qc issue 130, item 1) and `QC-SPEAKER-KNOWN` (item 2), the two elements R7 is judged on;
+- success criteria `SC-QC-QUOTE-MEETS-RULE` and `SC-QC-SPEAKER-KNOWN`, each with its disproof and one evidence requirement;
+- component `RU-QC-SLICE1-MODEL`;
+- planned artifacts `docs/model/slice1/intent.md`, `tests/model/test_qc_quote_meets_rule.py` and `tests/model/test_qc_speaker_known.py`;
+- verification subjects `VS-QC-QUOTE-MEETS-RULE` and `VS-QC-SPEAKER-KNOWN`, each with its test file as locator.
+
+**Running things it adds:**
+- the three files above;
+- qc's pre-commit and commit-msg hooks, written by `aes hooks install`. The pre-commit hook runs `aes target validate` and `aes topology check`.
+
+It adds no services or containers. Agent rules are unchanged.
+
+This proposal is the whole delta this plan needs. If the slice-1 model gains further elements in step 4 (for example issue 130 items 3–5), each one goes in as a new proposal that must pass `aes plan validate` before `aes plan accept`. They are not needed for R7.
+
+**Validation:** `aes plan validate` passes on this exact proposal: exit 0, "10 addition(s) … success_criteria=2 evidence_requirements=2 verification_subjects=2; every evidence requirement has a route". It was run 2026-10-11 in a scratch repository right after the same `aes init`. The output is in [`policy-enforcement-pilot.aes-validate.txt`](policy-enforcement-pilot.aes-validate.txt). The dry run found one AES gap: there is no `documentation` artifact kind, so the model file is planned as `configuration` (AES issue #525).
+
+**Requirement → target mapping (every requirement):**
+
+| Req | Changes the qc target? | qc target item(s) it serves | Success criterion | Verification subject |
+|---|---|---|---|---|
+| R1 | no: research already done; its result changed only this plan (company-planning, not AES-governed) and an AES canonical `proposals/` page, outside AES canonical's governed roots | none | n/a | own named check: the step-1 disposition table committed at AES canonical a5b8b3611 (`proposals/model-framework/README.md`) |
+| R2 | no: changes only company-planning (not AES-governed) | none | n/a | company-planning's own check: `durable_docs_check.py` plus a grep for the three rules in decision 0002 |
+| R3 | no: changes only company-planning (not AES-governed); a quick-adopt bug fix (#119) | none | n/a | company-planning's own check: `tests/test_quick_adopt_checks.py` |
+| R4 | yes: adds the normative items and planned artifacts | `QC-QUOTE-MEETS-RULE`, `QC-SPEAKER-KNOWN`, `ART-QC-SLICE1-INTENT` | both criteria | `VS-QC-QUOTE-MEETS-RULE`, `VS-QC-SPEAKER-KNOWN` |
+| R5 | yes: adds the verification subjects | `QC-QUOTE-MEETS-RULE`, `QC-SPEAKER-KNOWN` | `SC-QC-QUOTE-MEETS-RULE`, `SC-QC-SPEAKER-KNOWN` (their standing in `evidence.assess()`) | `VS-QC-QUOTE-MEETS-RULE`, `VS-QC-SPEAKER-KNOWN`, recorded with `aes evidence record` |
+| R6, R12 | no: changes only company-planning (not AES-governed); the page only reads qc's recorded standings | none | n/a | company-planning's own check: the Playwright page check |
+| R7 | yes (the same additions) | `OUT-001` (created by `aes init`, part of the new target), both normative items | both criteria must read REFUTED before qc's fixes land | both verification subjects |
+| R8 | no: changes only company-planning (the timing is written to its `docs/plans/policy-enforcement-pilot.check.txt`) | none | n/a | company-planning's own check: start and end commit timestamps in that file |
+| R9 | no: changes only company-planning (not AES-governed) | none | n/a | company-planning's own check: `tests/test_quick_adopt_checks.py` |
+| R10 | no: deferred | none | n/a | none: deferred, because the diagram rule needs a separate decision on what counts as a picture |
+| R11 | yes (the whole target) | `QC-QUOTE-MEETS-RULE`, `QC-SPEAKER-KNOWN` (and `OUT-001`, `RU-QC-SLICE1-MODEL`, the three planned artifacts) | `SC-QC-QUOTE-MEETS-RULE`, `SC-QC-SPEAKER-KNOWN`, which must stay well-formed: `aes target validate` and `aes topology check` exit 0 | `VS-QC-QUOTE-MEETS-RULE`, `VS-QC-SPEAKER-KNOWN`, each of which `aes topology check` must resolve to its test file; the structural checks themselves run in qc's pre-commit hook and `aes plan validate` |
 
 ## Prior art and ownership
 
@@ -163,15 +247,15 @@ None proposed. All changes are git commits, reversible by revert; warn mode prec
 
 | Candidate | Where | Disposition |
 |---|---|---|
-| agent_ecology2 doc graph: `scripts/relationships.yaml`, `check_doc_coupling.py`, `validate_relationships.py` | 47 / 37 repos in ~/code | **extend** (leading candidate, evaluated first in step 1): add element-to-test edges; its co-change check is a stand-in and is not reused as the correctness check |
+| agent_ecology2 doc graph: `scripts/relationships.yaml`, `check_doc_coupling.py`, `validate_relationships.py` | 47 / 37 repos in ~/code | **keep as is** (step 1, 2026-10-10): it links file globs, not elements to tests, and `verify_sync` never runs when code and doc both changed; kept only for co-change warnings. Its 13 diverged copies are project-meta #2523 |
 | agent_ecology2 META-ADR-0005 context compression ("domain model vs code drift" listed as missing; layer justification test) | `docs/visualizations/context_compression.html` | **reuse** as rationale: its three-part layer test becomes part of the rules in step 2 |
-| AES v0.2 `verification_subjects` + `.aes/observations` (status computed from recorded runs) | AES canonical `.aes/target.yaml` | **compose**: candidate record shape for status; assessed in step 1 |
+| AES v0.2 `verification_subjects` + `.aes/observations` (status computed from recorded runs, stale when a dependency changes) | AES canonical `.aes/target.yaml`, `src/agentic_engineering_system/evidence.py` | **reuse** (step 1 result): the element-to-test-to-status mechanism; no new status code or schema |
 | company-planning CORE-SYSTEM-MODEL and quick-adopt | this repository | **extend**: the checks land inside the existing gate, not beside it |
-| pytest markers + JUnit XML (`pytest --junitxml`) | external, standard pytest | **compose** (default record of runs): a marker carries the element ID, JUnit XML carries the result; no new dependency |
-| sphinx-needs | external | **bounded exception** (not adopted): needs a Sphinx docs build; these repos use Markdown with a hand-kept wiki. Step 1 may overturn this with evidence |
-| StrictDoc | external | **bounded exception** (not adopted): own `.sdoc` format beside Markdown models. Step 1 re-checks its Markdown and test-link support |
-| OpenFastTrace | external | **bounded exception** (not adopted): Java tool, adds a JVM to Python repos. Step 1 may overturn |
-| Doorstop | external | **bounded exception** (not adopted): one YAML file per item, against the workspace rule against thousands of small files. Step 1 may overturn |
+| pytest markers + JUnit XML (`pytest --junitxml`), pytest-requirements 0.3.1 | external, standard pytest | **not needed** (step 1): the AES verification subject's locator already links element to test, and JUnit alone has no commit binding or staleness |
+| sphinx-needs 8.5 + sphinx-test-reports 2.0 | external | **bounded exception** (step 1): links JUnit results to need IDs and computes status, but requirements must become needs (MyST directives or imported JSON), a second ID registry beside AES's; revisit if rendered traceability documents are wanted |
+| StrictDoc 0.30.2 | external | **bounded exception** (step 1): its Markdown input and JUnit import are both labelled experimental in its user guide |
+| OpenFastTrace 4.10 | external | **bounded exception** (step 1): traces coverage only, no test-result input; needs Java 17 |
+| Doorstop 3.2 | external | **bounded exception** (step 1): no documented test-status support; one file per item |
 | project-meta context-engineering design (`CONTEXT_ENGINEERING_AND_DERIVED_DOCUMENTATION_2026-08-24.md`) | project-meta | **compose**: its `required_reading`/`navigation` blocks in `relationships.yaml` stay as they are; element-to-test edges are added beside them, and step 1 confirms no conflict |
 
 Structural check: `git grep -l 'element_id\|verification_subject\|relationships.yaml'` across company-planning, AES canonical and qualitative_coding at step 3; any second mechanism recording element-to-test links besides the one step 1 selects is a parallel implementation and is merged or retired in the same step.
@@ -196,18 +280,18 @@ Structural check: `git grep -l 'element_id\|verification_subject\|relationships.
 | plan → adoption gate | method profile `bounded-design` | company-planning, `plugins/company-planning/contracts/method-conformance/profiles/bounded-design.json` | yes, step 3 (warn disposition for element checks) and step 5 (refuse) |
 | gate → receipt readers | `checklist_item_observation` / receipt JSON | company-planning, `plugins/company-planning/contracts/method-conformance/planning-method-conformance-receipt.v1.schema.json` | yes: adds `warn` disposition value, step 3 |
 | system model file → element check | element ID / decided-guessed / unknowns rules | company-planning, `docs/decisions/0002-every-project-has-a-checked-system-model.md` and `plugins/company-planning/distribution/references/system-model.md` | yes, step 2 |
-| test run → status computation | default: a pytest marker `@pytest.mark.element("<ID>")` on each covering test, plus the JUnit XML file pytest writes | pytest (JUnit XML format, https://docs.pytest.org/en/stable/how-to/output.html#creating-junitxml-format-files); the marker is registered in each repo's `pyproject.toml` | no change to JUnit XML; adds the marker registration |
-| (not used at this boundary) doc graph | agent_ecology2 `scripts/relationships.yaml` | no: this plan as adopted neither uses nor changes it. If step 1 selects extending it, that is a contract change, and the plan is amended and re-adopted before step 3 |
+| test run → status computation | AES v0.2 observation record (`.aes/observations/*.yaml`, written by `aes evidence record <VS-ID>`) and the target's `verification_subjects` (`locator` = one test file per element) | AES canonical `src/agentic_engineering_system/evidence.py`, `docs/greenfield/GETTING_STARTED.md` §5 | no change to AES; qc gains `.aes/` in step 4 |
 | qualitative_coding models and tests → checks | the same rules as consumed | qc repo (BrianMills2718/qc), `docs/model/slice1/intent.md` (new file, step 4; path confirmed with the `durable-docs` lane) | yes, step 4 creates it |
-| status computation → status page and review point | computed statuses file, one JSON record per element (`element_id`, `status`, `test_ids`, `run_ref`) | company-planning; schema file `plugins/company-planning/contracts/method-conformance/element-status.v1.schema.json` (new) | yes, step 3 creates it |
+| status computation → status page and review point | AES `EvidenceReport` from `evidence.assess(root)` (criterion standings and observation freshness) | AES canonical `src/agentic_engineering_system/evidence.py` | no new schema: the page generator reads `assess()` directly; `element-status.v1.schema.json` is dropped |
 
 Per contract (producer → consumer):
 - method profile `bounded-design.json`: produced by this lane's commits → consumed by `compiler.py` `compile_profile` and every `cli.py adopt`/`quick-adopt` run.
 - receipt JSON / `checklist_item_observation`: produced by `gate.py` `evaluate`/`record_observation` → consumed by `plan_execution_supervisor.py`, `cli.py lint`, the adopt and check CLI output.
 - element rules (decision 0002 + `system-model.md`): produced by step 2 → consumed by the new model element check and by agents writing models.
-- element marker + JUnit XML: produced by pytest runs in the target repo (qc in step 4) → consumed by the status computation.
-- computed statuses: produced by the status computation → consumed by the element status page and the review point that links it.
-- Landing order so no consumer breaks: (1) step 2 rule text (docs only); (2) receipt schema gains `warn` as an allowed value, with receipt readers tested to treat `warn` as non-blocking, before any check emits it; (3) the checks emit `warn`; (4) status computation and page; (5) step 4 on qc; (6) only then the profile turns `warn` into a blocking `fail`. Each lands as its own commit with tests passing.
+- qualitative_coding slice-1 model (`docs/model/slice1/intent.md`) and its element tests (`tests/model/`): produced by the step-4 session in the qc repo → consumed by the model element check (element IDs, decided/guessed marks, unknowns) and by `aes evidence record` (each test file is a verification subject's locator).
+- AES observations: produced by `aes evidence record` runs in the target repo (qc in step 4) → consumed by `evidence.assess()`.
+- computed standings: produced by `evidence.assess()` → consumed by the model element check, the element status page and the review point that links it.
+- Landing order so no consumer breaks: (1) step 2 rule text (docs only); (2) receipt schema gains `warn` as an allowed value, with receipt readers tested to treat `warn` as non-blocking, before any check emits it; (3) the checks emit `warn`; (4) the status page over `evidence.assess()`; (5) step 4 on qc; (6) only then the profile turns `warn` into a blocking `fail`. Each lands as its own commit with tests passing.
 
 ## Durable documents
 
commit ec4112f [Goal policy-enforcement-pilot] Step 4 results on qualitative_coding slice 1

diff --git a/docs/plans/policy-enforcement-pilot.md b/docs/plans/policy-enforcement-pilot.md
index a13de89..4ca4c07 100644
--- a/docs/plans/policy-enforcement-pilot.md
+++ b/docs/plans/policy-enforcement-pilot.md
@@ -299,6 +299,6 @@ Per contract (producer → consumer):
 
 This repository declares durable documents (`durable_documents` in `.agentic/repo.yaml`): `goal`, `requirements`, `system_model`, `decisions`, `plans`.
 
-Durable documents: decisions, system_model#quick-adopt, system_model#adopt, plans
+Durable documents: decisions, system_model#PROC-ADOPT, system_model#PROC-QUICK-ADOPT, system_model#RULE-MODEL-ELEMENT-IDS, system_model#RULE-ELEMENT-STATUS-FROM-RUN, plans
 
 At completion, `python3 plugins/company-planning/scripts/durable_docs_check.py --repo . --plan docs/plans/policy-enforcement-pilot.md --range cdcf6c7d604d3dc8d1a34871a582359b86311ea8..HEAD` must exit 0; its full output is appended to `docs/plans/policy-enforcement-pilot.check.txt`.
```

Classification: **real update.** Decision 0002 gains the three rules (`+**Amended 2026-10-11: the plan, build and review rules are checked, not self-attested.**`, `+- **RULE-MODEL-ELEMENT-IDS (plan).**`, `+- **RULE-ELEMENT-STATUS-FROM-RUN (build).**`); `trace.yaml` adds `+  - id: RULE-MODEL-ELEMENT-IDS` and `+  - id: RULE-ELEMENT-STATUS-FROM-RUN` with owners and named tests, and `PROC-ADOPT` now enforces the first. Each declared role changed with content. One gap: the decision names `RULE-REVIEW-STATUS-PAGE`, which `trace.yaml` does not yet list (the decision itself says a rule enters the trace with its check).

### 2. Digimon_for_KG_application `222_main_branch_health`

- Plan file: `docs/plans/222_main_branch_health.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T06:29:17Z; last plan-tagged commit 2026-10-11T05:07:22-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `675b38b33c00..f6cade0bdb6b` (parent of the first to the last of the 1 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: f6cade0bd

`git diff --stat` over the range:

```text
 Core/AgentSchema/tool_contracts.py                        |  11 +-
 Core/AgentTools/relationship_tools.py                     |  24 +-
 Core/Graph/BaseGraph.py                                   |  14 +-
 Core/Graph/TreeGraph.py                                   |   5 +-
 Core/Graph/TreeGraphBalanced.py                           |   1 -
 Core/Schema/ChunkSchema.py                                |  33 +-
 Makefile                                                  |  10 +-
 docs/plans/222_main_branch_health.adoption-attempts.jsonl |   1 +
 docs/plans/222_main_branch_health.adoption-decision.json  |  15 +
 docs/plans/222_main_branch_health.bundle.json             | 773 ++++++++++++++++++++++++++++++++++
 docs/plans/222_main_branch_health.facts.json              |  25 ++
 docs/plans/222_main_branch_health.md                      | 180 ++++++++
 docs/plans/222_main_branch_health.path-decision.json      |  57 +++
 docs/plans/222_main_branch_health.receipt.json            | 627 +++++++++++++++++++++++++++
 docs/plans/222_main_branch_health.verdicts.json           | 245 +++++++++++
 docs/plans/AGENTS.md                                      |   3 +-
 docs/plans/Digimon_for_KG_application#222.goal.md         |  18 +
 docs/plans/ROADMAP.md                                     |   8 +-
 generated/docstring_wiki.md                               |  44 +-
 hooks/pre-commit                                          |  37 +-
 scripts/meta/run_trace_verify_gate.sh                     |  87 ++++
 tests/integration/test_relationship_vdb_tools.py          |  55 +++
 tests/unit/test_chunk_data_contract.py                    |  44 ++
 tests/unit/test_entity_relation_summary.py                |  71 ++++
 tests/unit/test_plan216_sna.py                            |  25 +-
 tests/unit/test_shared_evidence_service.py                |  26 +-
 tests/unit/test_trace_verify_gate_runner.py               |  89 ++++
 wiki/current-state.claims.yaml                            |   2 +
 wiki/index.md                                             |   2 +-
 29 files changed, 2453 insertions(+), 79 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `NORTH_STAR.md`, `.aes/target.yaml`, `docs/adr`, `docs/model/ARCHITECTURE.md`, `docs/model/trace.yaml`. Touched by this plan's commits: **none**.

Classification: **none** (no line). Adoption-gate leak: the repository declared durable documents at 04:52Z (`675b38b3`), before this plan's adoption at 06:29Z, and the plan still carries no line. Its commits touch no declared durable path, so `none` would have been the truthful answer.

### 3. .agents `rulesync-hooks`

- Plan file: `docs/plans/rulesync-hooks.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T07:49:12Z; last plan-tagged commit 2026-10-11T04:44:29-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `489e29390fe7..66422e3a47a0` (parent of the first to the last of the 3 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: ef73b9d45, 6af2f1dae, 66422e3a4

`git diff --stat` over the range:

```text
 .rulesync/hooks.jsonc                                           | 181 ++++++
 AGENTS.md                                                       |   2 +-
 Makefile                                                        |   6 +-
 README.md                                                       |  16 +-
 contracts/client-config/README.md                               |  75 ++-
 contracts/client-config/hook-parity-baseline.json               |   2 +-
 .../{hook-manifest.v1.json => hooks-not-enabled.json}           | 202 ++-----
 docs/architecture/GOAL.md                                       |  13 +-
 docs/claude-hooks-disabled-2026-09.md                           |   4 +-
 docs/model/ARCHITECTURE.md                                      |  23 +-
 docs/model/trace.yaml                                           |   8 +-
 docs/plans/rulesync-hooks.adoption-attempts.jsonl               |   1 +
 docs/plans/rulesync-hooks.adoption-decision.json                |  15 +
 docs/plans/rulesync-hooks.bundle.json                           | 817 ++++++++++++++++++++++++++++
 docs/plans/rulesync-hooks.check.txt                             | 107 ++++
 docs/plans/rulesync-hooks.facts.json                            |  23 +
 docs/plans/rulesync-hooks.goal.md                               |  36 ++
 docs/plans/rulesync-hooks.md                                    | 204 +++++++
 docs/plans/rulesync-hooks.path-decision.json                    |  57 ++
 docs/plans/rulesync-hooks.receipt.json                          | 654 ++++++++++++++++++++++
 docs/plans/rulesync-hooks.verdicts.json                         | 317 +++++++++++
 hooks/hot_hooks_write_gate.py                                   |   5 +-
 hooks/pre-commit                                                |   2 +-
 install.sh                                                      | 509 +----------------
 scripts/check_hook_parity.py                                    | 124 +++--
 scripts/codex_app_server.py                                     |  20 +-
 scripts/codex_hook_trust.py                                     | 123 +++++
 scripts/hook_inventory.py                                       | 101 ++++
 scripts/manage_client_config.py                                 | 731 -------------------------
 scripts/rulesync_sync.sh                                        |  23 +-
 tests/test_check_hook_parity.py                                 | 240 ++++----
 tests/test_codex_hook_trust.py                                  | 119 ++++
 tests/test_hot_hooks_write_gate.py                              |   7 +-
 tests/test_install.py                                           | 648 ++--------------------
 tests/test_manage_client_config.py                              | 539 ------------------
 tests/test_rulesync_source.py                                   |  42 ++
 wiki/index.md                                                   |   1 +
 37 files changed, 3193 insertions(+), 2804 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `docs/architecture/GOAL.md`, `docs/architecture/GOAL.md`. Touched by this plan's commits: `docs/architecture/GOAL.md`.

Full diff of `docs/architecture/GOAL.md`, plan commits only:

```diff
commit ef73b9d [Goal rulesync-hooks] Generate Claude and Codex hooks from .rulesync/hooks.jsonc

diff --git a/docs/architecture/GOAL.md b/docs/architecture/GOAL.md
index 8633040..969cbf0 100644
--- a/docs/architecture/GOAL.md
+++ b/docs/architecture/GOAL.md
@@ -47,18 +47,19 @@ collides with a client built-in, is registered without either check failing
 
 #### REQ-CLIENT-PARITY
 
-Hook declarations in `contracts/client-config/hook-manifest.v1.json` are the desired
-state for both clients, and a hook that runs in only one client is reported.
+Hook declarations in `.rulesync/hooks.jsonc` are the desired state for both clients
+(written by `scripts/rulesync_sync.sh`), and a hook that runs in only one client is
+reported.
 
 Success: `make client-config-check` reports no drift and `make hook-parity-check`
 exits 0 against the committed baseline.
 
-Disproof: Codex `hooks/list` shows a manifest hook missing, or a hook that runs only
+Disproof: Codex `hooks/list` shows a source hook missing or not running, or a hook that runs only
 in Claude Code, while `make hook-parity-check` exits 0.
 
 #### REQ-HOT-HOOKS-CLAIM
 
-Files under `hooks/`, plus `scripts/manage_client_config.py` and `sync_skills.py`,
+Files under `hooks/`, plus `sync_skills.py`,
 are live in every session, so they change only under a live coordination claim
 ([AGENTS.md](../../AGENTS.md)).
 
@@ -126,8 +127,8 @@ behavior, with zero client-only skills and zero forked files (Project Meta
 Agent instructions stay consistent across two clients only when each one has a
 single authored home and every client surface is derived from it and checked, never
 copied: truth lives where it is edited (AES-CTX-004). Skills are authored in
-`skills/`, hooks in `contracts/client-config/hook-manifest.v1.json`, and
-`sync_skills.py` plus `scripts/manage_client_config.py` derive and verify the client
+`skills/`, hooks in `.rulesync/hooks.jsonc`, and `sync_skills.py` plus
+`scripts/rulesync_sync.sh` derive and verify the client
 surfaces, so drift shows up as a failing check instead of a silent behavior split.
 
 ## Thesis disproof (AES extension)
```

Classification: **none** (no line). Adoption-gate leak: the repository declared durable documents at 05:32Z (`984b49a`), before adoption at 07:49Z. The plan's commit `ef73b9d` did make an undeclared real update to the goal document: `REQ-CLIENT-PARITY` moves its source of truth (`-Hook declarations in \`contracts/client-config/hook-manifest.v1.json\`` / `+Hook declarations in \`.rulesync/hooks.jsonc\``) and its disproof wording. Under the frozen rule a missing line counts as `none` regardless.

### 4. project-meta `register-interview-kit`

- Plan file: `docs/plans/register-interview-kit.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T07:25:35Z; last plan-tagged commit 2026-10-11T03:28:14-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `d0bf8459dc35..d68592ed6187` (parent of the first to the last of the 2 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: 6ee9082fa, d68592ed6

`git diff --stat` over the range:

```text
 .agentic/repo.yaml                                        |  23 ++
 PROJECT_GRAPH.json                                        |  60 ++++
 README.md                                                 |   4 +
 docs/decisions/0001-durable-document-roles.md             |  40 +++
 docs/model/ARCHITECTURE.md                                | 222 +++++++++++++
 docs/model/requirements.yaml                              |  45 +++
 docs/model/trace.yaml                                     |  81 +++++
 docs/ops/WORKSPACE_MAP.md                                 |  10 +-
 docs/plans/register-interview-kit.adoption-attempts.jsonl |   3 +
 docs/plans/register-interview-kit.adoption-decision.json  |  15 +
 docs/plans/register-interview-kit.bundle.json             | 597 ++++++++++++++++++++++++++++++++++
 docs/plans/register-interview-kit.check.txt               |  37 +++
 docs/plans/register-interview-kit.facts.json              |  21 ++
 docs/plans/register-interview-kit.goal.md                 |  18 +
 docs/plans/register-interview-kit.md                      | 135 ++++++++
 docs/plans/register-interview-kit.path-decision.json      |  57 ++++
 docs/plans/register-interview-kit.receipt.json            | 519 +++++++++++++++++++++++++++++
 docs/plans/register-interview-kit.verdicts.json           | 209 ++++++++++++
 wiki/index.md                                             |   1 +
 19 files changed, 2093 insertions(+), 4 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `docs/model/ARCHITECTURE.md`, `docs/model/requirements.yaml`, `docs/decisions`, `docs/model/ARCHITECTURE.md`, `docs/model/trace.yaml`. Touched by this plan's commits: **none**.

Classification: **none** (no line). Adoption-gate leak: the repository declared durable documents at 05:17Z (`518bae09f`), before adoption at 07:25Z. No declared durable path touched.

### 5. company-planning `aes-overlay-creates-target`

- Plan file: `docs/plans/aes-overlay-creates-target.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T06:29:36Z; last plan-tagged commit 2026-10-11T03:02:53-04:00.
- Durable-documents line: `Durable documents: none -- the change is the checklist profile and its design doc, which are this repository's contracts, not durable documents of a declared role`
- Commit range: `22b24a1c22cd..3b15440c0d49` (parent of the first to the last of the 4 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: 6953b5acd, b2229392c, 88d0d22ab, 3b15440c0

`git diff --stat` over the range:

```text
 README.md                                                       |   2 +-
 docs/model/trace.yaml                                           |   1 +
 docs/plans/aes-overlay-creates-target.adoption-attempts.jsonl   |   3 +
 docs/plans/aes-overlay-creates-target.adoption-decision.json    |  15 +
 docs/plans/aes-overlay-creates-target.bundle.json               | 642 ++++++++++++++++++++++++++++
 docs/plans/aes-overlay-creates-target.check.txt                 |  12 +
 docs/plans/aes-overlay-creates-target.facts.json                |  21 +
 docs/plans/aes-overlay-creates-target.goal.md                   |  18 +
 docs/plans/aes-overlay-creates-target.md                        | 130 ++++++
 docs/plans/aes-overlay-creates-target.path-decision.json        |  57 +++
 docs/plans/aes-overlay-creates-target.receipt.json              | 541 +++++++++++++++++++++++
 docs/plans/aes-overlay-creates-target.verdicts.json             | 182 ++++++++
 plugins/company-planning/.claude-plugin/plugin.json             |   2 +-
 plugins/company-planning/.codex-plugin/plugin.json              |   2 +-
 .../method-conformance/profiles/bounded-design.v1.json          |  12 +-
 .../designs/enforcement/PLANNING_METHOD_CONFORMANCE_RECEIPT.md  |   9 +-
 tests/test_method_conformance.py                                |   2 +-
 wiki/index.md                                                   |   1 +
 18 files changed, 1641 insertions(+), 11 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `docs/architecture/GOAL.md`, `docs/architecture/REQUIREMENTS.md`, `docs/decisions/`, `docs/model/ODD.md`, `docs/model/trace.yaml`. Touched by this plan's commits: `docs/model/trace.yaml`.

Full diff of `docs/model/trace.yaml`, plan commits only:

```diff
commit b222939 [Goal aes-overlay-creates-target] Pin bounded-design@13 sources at the fix commit and bump the plugin release

diff --git a/docs/model/trace.yaml b/docs/model/trace.yaml
index 90c577a..585a7e4 100644
--- a/docs/model/trace.yaml
+++ b/docs/model/trace.yaml
@@ -24,6 +24,7 @@ rules:
       - tests/test_method_conformance.py::test_stale_source_revision_fails_visibly
       - tests/test_method_conformance.py::test_compiled_items_pin_exact_source_revisions
     decisions: [docs/decisions/0001-plan-adoption-requires-a-receipt.md]
+  # Re-read 2026-10-11 for bounded-design@13 (plan aes-overlay-creates-target): that revision rewords only CORE-ACTIVATION-FACTS and OV-AES-TARGET-TRACE; CORE-SYSTEM-MODEL and the rules owned by the profile below are unchanged.
   - id: RULE-SYSTEM-MODEL-REQUIRED
     statement: A plan links its project's system model or carries the one exemption line, and names the model elements it touches (CORE-SYSTEM-MODEL).
     owner: plugins/company-planning/contracts/method-conformance/profiles/bounded-design.v1.json
```

Classification: **none** (declared). The one durable-path change is mechanical: a comment line in `trace.yaml`, `+  # Re-read 2026-10-11 for bounded-design@13 ... CORE-SYSTEM-MODEL and the rules owned by the profile below are unchanged.` No rule, owner or check changed.

### 6. .agents `rulesync-client-sync`

- Plan file: `docs/plans/rulesync-client-sync.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T02:40:04Z; last plan-tagged commit 2026-10-11T01:42:03-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `bce214a82a10..f18ca113cbfc` (parent of the first to the last of the 6 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: 51d2b1bb4, d74fa6ad2, 815cf7e51, 043db71f7, da081bb6e, f18ca113c

`git diff --stat` over the range:

```text
 .agentic/repo.yaml                                              |  12 +
 .rulesync/mcp.jsonc                                             |  56 ++
 .../client-config/agents => .rulesync/subagents}/debugger.md    |   8 +-
 .../client-config/agents => .rulesync/subagents}/frontend.md    |   8 +-
 .../client-config/agents => .rulesync/subagents}/infra.md       |   8 +-
 .../agents => .rulesync/subagents}/project-brain.md             |  14 +-
 .../client-config/agents => .rulesync/subagents}/release.md     |   8 +-
 .../agents => .rulesync/subagents}/representation-router.md     |  14 +-
 .../client-config/agents => .rulesync/subagents}/researcher.md  |  12 +-
 .../client-config/agents => .rulesync/subagents}/reviewer.md    |  10 +-
 .../client-config/agents => .rulesync/subagents}/test-runner.md |  10 +-
 Makefile                                                        |   9 +-
 README.md                                                       |  16 +-
 contracts/client-config/README.md                               |  45 +-
 contracts/client-config/rtk/config.toml                         |  51 ++
 contracts/client-config/rtk/install.sh                          |  25 +
 contracts/client-config/rtk/rtk-claude-hook                     |  41 ++
 distribution/component-classification-report.md                 |  65 ++-
 docs/SUBAGENTS_AND_ORCHESTRATION.md                             |   6 +-
 docs/architecture/GOAL.md                                       | 159 ++++++
 docs/model/ARCHITECTURE.md                                      | 150 +++++
 docs/model/trace.yaml                                           | 110 ++++
 docs/plans/rtk-shell-output.adoption-attempts.jsonl             |   1 +
 docs/plans/rtk-shell-output.adoption-decision.json              |  15 +
 docs/plans/rtk-shell-output.bundle.json                         | 685 +++++++++++++++++++++++
 docs/plans/rtk-shell-output.facts.json                          |  25 +
 docs/plans/rtk-shell-output.goal.md                             |  18 +
 docs/plans/rtk-shell-output.md                                  | 152 ++++++
 docs/plans/rtk-shell-output.path-decision.json                  |  57 ++
 docs/plans/rtk-shell-output.receipt.json                        | 581 ++++++++++++++++++++
 docs/plans/rtk-shell-output.verdicts.json                       | 164 ++++++
 docs/plans/rtk-shell-output/traces.txt                          |  52 ++
 docs/plans/rulesync-client-sync.adoption-attempts.jsonl         |   1 +
 docs/plans/rulesync-client-sync.adoption-decision.json          |  15 +
 docs/plans/rulesync-client-sync.bundle.json                     | 817 ++++++++++++++++++++++++++++
 docs/plans/rulesync-client-sync.check.txt                       | 110 ++++
 docs/plans/rulesync-client-sync.facts.json                      |  23 +
 docs/plans/rulesync-client-sync.goal.md                         |  36 ++
 docs/plans/rulesync-client-sync.md                              | 170 ++++++
 docs/plans/rulesync-client-sync.path-decision.json              |  57 ++
 docs/plans/rulesync-client-sync.receipt.json                    | 654 ++++++++++++++++++++++
 docs/plans/rulesync-client-sync.verdicts.json                   | 317 +++++++++++
 docs/plans/rulesync-client-sync/compare_client_config.py        |  92 ++++
 mcp_registry.yaml                                               |  94 ----
 render_mcp_config.py                                            | 135 -----
 roadmap/README.md                                               |   5 +
 scripts/build_component_inventory.py                            |   9 +-
 scripts/mcp_bearer_header.sh                                    |  16 +
 scripts/rulesync_sync.sh                                        |  90 +++
 scripts/sync_agents.py                                          | 164 ------
 tests/test_client_agent_frontmatter.py                          |   9 +-
 tests/test_render_mcp_config.py                                 |  39 --
 tests/test_rtk_claude_hook.py                                   |  73 +++
 tests/test_rulesync_source.py                                   |  56 ++
 tests/test_sync_agents.py                                       | 112 ----
 wiki/index.md                                                   |   2 +
 56 files changed, 5093 insertions(+), 590 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `docs/architecture/GOAL.md`, `docs/architecture/GOAL.md`. Touched by this plan's commits: **none**.

Classification: **none** (no line). Adopted at 02:40Z, before this repository declared durable documents (05:32Z), so the gate had nothing to require; listed as a leak only because the frozen rule lists every missing line. No declared durable path touched.

### 7. project-meta `audit-rulesync-check`

- Plan file: `docs/plans/audit-rulesync-check.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T03:28:21Z; last plan-tagged commit 2026-10-11T01:36:51-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `531a77d7510f..5a48636f0c90` (parent of the first to the last of the 2 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: 43ee77dbb, 5a48636f0

`git diff --stat` over the range:

```text
 PROJECT_GRAPH.json                                        |  63 ++++
 docs/ops/WORKSPACE_MAP.md                                 |  23 +-
 docs/plans/audit-rulesync-check.adoption-attempts.jsonl   |   2 +
 docs/plans/audit-rulesync-check.adoption-decision.json    |  15 +
 docs/plans/audit-rulesync-check.bundle.json               | 685 ++++++++++++++++++++++++++++++++++
 docs/plans/audit-rulesync-check.check.txt                 |  36 ++
 docs/plans/audit-rulesync-check.facts.json                |  23 ++
 docs/plans/audit-rulesync-check.goal.md                   |  18 +
 docs/plans/audit-rulesync-check.md                        | 151 ++++++++
 docs/plans/audit-rulesync-check.path-decision.json        |  57 +++
 docs/plans/audit-rulesync-check.receipt.json              | 573 ++++++++++++++++++++++++++++
 docs/plans/audit-rulesync-check.verdicts.json             | 290 ++++++++++++++
 docs/plans/register-subreddit-map.adoption-attempts.jsonl |   2 +
 docs/plans/register-subreddit-map.adoption-decision.json  |  15 +
 docs/plans/register-subreddit-map.bundle.json             | 597 +++++++++++++++++++++++++++++
 docs/plans/register-subreddit-map.check.txt               |  17 +
 docs/plans/register-subreddit-map.facts.json              |  21 ++
 docs/plans/register-subreddit-map.goal.md                 |  18 +
 docs/plans/register-subreddit-map.md                      | 128 +++++++
 docs/plans/register-subreddit-map.path-decision.json      |  57 +++
 docs/plans/register-subreddit-map.receipt.json            | 519 ++++++++++++++++++++++++++
 docs/plans/register-subreddit-map.verdicts.json           | 155 ++++++++
 scripts/sync_client_parity_concern.py                     |   6 +-
 tests/test_sync_client_parity_concern.py                  |   8 +-
 wiki/concepts/cross_client_config_sync.md                 |  12 +-
 wiki/index.md                                             |   2 +
 26 files changed, 3478 insertions(+), 15 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `docs/model/ARCHITECTURE.md`, `docs/model/requirements.yaml`, `docs/decisions`, `docs/model/ARCHITECTURE.md`, `docs/model/trace.yaml`. Touched by this plan's commits: **none**.

Classification: **none** (no line). Adopted at 03:28Z, before the repository declared durable documents (05:17Z); listed as a leak under the frozen rule. No declared durable path touched.

### 8. project-meta `register-subreddit-map`

- Plan file: `docs/plans/register-subreddit-map.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T02:35:26Z; last plan-tagged commit 2026-10-11T01:11:33-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `531a77d7510f..203458e6d4e9` (parent of the first to the last of the 1 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: 203458e6d

`git diff --stat` over the range:

```text
 PROJECT_GRAPH.json                                        |  63 ++++
 docs/ops/WORKSPACE_MAP.md                                 |  23 +-
 docs/plans/register-subreddit-map.adoption-attempts.jsonl |   2 +
 docs/plans/register-subreddit-map.adoption-decision.json  |  15 +
 docs/plans/register-subreddit-map.bundle.json             | 597 ++++++++++++++++++++++++++++++++++
 docs/plans/register-subreddit-map.check.txt               |  17 +
 docs/plans/register-subreddit-map.facts.json              |  21 ++
 docs/plans/register-subreddit-map.goal.md                 |  18 +
 docs/plans/register-subreddit-map.md                      | 128 ++++++++
 docs/plans/register-subreddit-map.path-decision.json      |  57 ++++
 docs/plans/register-subreddit-map.receipt.json            | 519 +++++++++++++++++++++++++++++
 docs/plans/register-subreddit-map.verdicts.json           | 155 +++++++++
 wiki/index.md                                             |   1 +
 13 files changed, 1611 insertions(+), 5 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `docs/model/ARCHITECTURE.md`, `docs/model/requirements.yaml`, `docs/decisions`, `docs/model/ARCHITECTURE.md`, `docs/model/trace.yaml`. Touched by this plan's commits: **none**.

Classification: **none** (no line). Adopted at 02:35Z, before the repository declared durable documents (05:17Z); listed as a leak under the frozen rule. No declared durable path touched.

### 9. Digimon_for_KG_application `221_documentation_consolidation`

- Plan file: `docs/plans/221_documentation_consolidation.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T01:00:58Z; last plan-tagged commit 2026-10-10T23:24:36-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `089dd88c46c0..5184a7c1b094` (parent of the first to the last of the 2 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: e93259d7a, 5184a7c1b

`git diff --stat` over the range:

```text
 .agentic/repo.yaml                                              |   22 +
 .claude/HANDOFF.md                                              |   13 -
 .claude/skills/digimon-operators/SKILL.md                       |    0
 .company-planning/219_next.goal.md                              |   33 -
 .md-file-cap.yaml                                               |   39 +
 AGENTS.md                                                       |    5 +-
 Data/README.md                                                  |    4 +
 FUNCTIONALITY.md                                                |   19 -
 ISSUES.md                                                       |   32 +-
 KNOWLEDGE.md                                                    |  761 -----
 Makefile                                                        |   17 +-
 NORTH_STAR.md                                                   |    4 +
 OFF_THE_SHELF_REUSE_RECOMMENDATIONS.md                          |    4 +
 README.md                                                       |   26 +-
 START_HERE.md                                                   |    9 -
 docs/ACTIVE_DOCS.md                                             |  129 -
 docs/ADAPTIVE_KNOWLEDGE_SYSTEM_VISION.md                        |   31 -
 docs/ADR_LIFECYCLE.md                                           |   65 -
 docs/AGENTS.md                                                  |    2 +-
 docs/ARCHITECTURE.md                                            |    4 +
 docs/BENCHMARK_PROMOTION_POLICY.md                              |  126 -
 docs/CAPABILITY_STATUS.md                                       |   51 -
 docs/CLEANUP_EXTRACTED_CLAIMS.md                                |   20 -
 docs/COMPETITIVE_ANALYSIS.md                                    |   18 -
 docs/DEFERRED_CAPABILITIES_REGISTRY.md                          |    4 +
 docs/DESIGN_PLAN_ALIGNMENT.md                                   |   19 -
 docs/DOCUMENTATION_CONTRACT.md                                  |   28 +-
 docs/FUTURE_EXTENSION_CATALOG.md                                |  350 --
 docs/GLOSSARY.md                                                |    4 +
 docs/GRAPH_ATTRIBUTE_MODEL.md                                   |   26 -
 docs/GRAPH_ENRICHMENT.md                                        |    4 +
 docs/GRAPH_GAP_REGISTER.md                                      |   16 -
 docs/GRAPH_STATE_CURRENT.md                                     |   19 -
 docs/GRAPH_VISION_TARGET.md                                     |    4 +
 docs/INSIDE_SUCCESS_BETA_RUNTIME_CONTEXT.md                     |   20 -
 docs/OPERATOR_FAMILIES.md                                       |    4 +
 docs/RECURSIVE_REASONING_TRACE.md                               |   18 -
 docs/RELATED_SYSTEMS_LANDSCAPE.md                               |    4 +
 docs/REPO_SURFACE.md                                            |   28 +-
 docs/REPRESENTATION_AND_RETRIEVAL_ARCHITECTURE.md               |    4 +
 docs/SOTA_PATTERNS.md                                           |  169 -
 docs/SYSTEM_OVERVIEW.md                                         |   21 -
 docs/TOOL_CAPABILITY_MATRIX.md                                  |    4 +
 docs/V1_ARCHITECTURE_RELEASE_GATE.md                            |  148 -
 docs/adr/001-agent-orchestration-architecture.md                |    4 +
 docs/adr/002-universal-graph-schema-and-extraction.md           |  390 ---
 docs/adr/003-graph-tool-suites.md                               |  307 --
 docs/adr/004-graph-build-rearchitecture.md                      |    4 +
 docs/adr/005-typed-extraction-validation.md                     |    4 +
 docs/adr/006-open-tkg-grounded-entity-policy.md                 |    4 +
 docs/adr/007-entity-relationship-closure.md                     |    4 +
 docs/adr/008-pure-lane-build-comparisons.md                     |   61 -
 docs/adr/009-two-pass-extraction-for-completeness.md            |    4 +
 docs/adr/010-tool-applicability-architecture.md                 |    4 +
 docs/adr/011-extraction-iteration-supervisor.md                 |  103 -
 .../adr/012-open-schema-does-not-inject-default-type-palette.md |    4 +
 docs/adr/013-answer-critical-fact-representation.md             |    4 +
 docs/adr/014-tool-consolidation-surface.md                      |    4 +
 docs/adr/015-strategic-risks-thesis-test.md                     |   26 -
 ...eclarative-decision-tracing-and-agent-runtime-declaration.md |   10 +-
 docs/adr/017-nary-graph-representation-and-onto-canon-import.md |    4 +
 docs/adr/018-federated-canonical-action-manifest.md             |   12 +-
 .../019-composition-state-policy-and-transition-separation.md   |   12 +-
 docs/adr/020-graph-projection-surface-contract.md               |    4 +
 docs/adr/021-analytic-operator-role.md                          |    4 +
 docs/adr/022-representation-ir-native-execution.md              |    4 +
 ...owned-situational-reasoning-and-direct-execution-boundary.md |    4 +
 docs/archive/AGENT_INTELLIGENCE_ENHANCEMENTS.md                 |  149 -
 docs/archive/API_REFERENCE.md                                   |  221 --
 docs/archive/BACKEND_STATUS_REPORT.md                           |  163 -
 docs/archive/CHECKPOINT_PROGRESS.md                             |  177 -
 docs/archive/CLAUDE_ORIGINAL.md                                 |  573 ----
 docs/archive/DEPENDENCIES.md                                    |  253 --
 docs/archive/DIGIMON_INTEGRATION_RESPONSE.md                    |  417 ---
 docs/archive/IDEAS.md                                           |   64 -
 docs/archive/INVESTIGATIONS.md                                  |   82 +
 docs/archive/MCP_IMPLEMENTATION_TRACKER.md                      |  114 -
 docs/archive/MCP_INTEGRATION_DETAILED_PLAN.md                   |  659 ----
 docs/archive/OVERNIGHT_PROGRESS.md                              |   58 -
 docs/archive/PLANNING_SUMMARY.md                                |  160 -
 docs/archive/PLANS.md                                           |  256 ++
 docs/archive/PROGRESS.md                                        |   41 -
 docs/archive/QUICK_START.md                                     |  139 -
 docs/archive/README.md                                          |   30 -
 docs/archive/README_SOCIAL_MEDIA_ANALYSIS.md                    |  149 -
 docs/archive/README_SOCIAL_MEDIA_UI.md                          |  149 -
 docs/archive/README_STREAMLIT.md                                |  237 --
 docs/archive/REPORTS.md                                         |  145 +
 docs/archive/STRATEGIC_UPDATE_AI_AGENTS.md                      |  193 --
 docs/archive/composability_handoff_for_chatgpt.md               |  243 --
 docs/archive/demo_ui_usage.md                                   |   66 -
 docs/archive/digimon_information_for_struct_integration.md      |  713 ----
 docs/archive/field_mapping_fixes.md                             |   31 -
 docs/archive/handoffs/HANDOFF_legacy_baseline.md                |  394 ---
 docs/archive/handoffs/handoff_2026_04_03.md                     |  252 --
 docs/archive/legacy_doc_2025_06_02/change_log.md                | 1353 --------
 .../archive/legacy_doc_2025_06_02/change_log_graphvisualizer.md |   71 -
 docs/archive/legacy_doc_2025_06_02/graphrag_operator_status.md  |   93 -
 docs/archive/legacy_doc_2025_06_02/handoff_2025_06_02.md        |  171 -
 docs/archive/legacy_doc_2025_06_02/handoff_2025_06_02_part2.md  |  171 -
 docs/archive/legacy_doc_2025_06_02/handoff_2025_06_02_part3.md  |  234 --
 .../handoff_2025_06_02_react_loop_debugging.md                  |   82 -
 .../handoff_2025_06_02_react_loop_status.md                     |   75 -
 .../legacy_doc_2025_06_02/handoff_2025_06_02_session_end.md     |   57 -
 docs/archive/legacy_doc_2025_06_02/system_status_report.md      |  142 -
 docs/archive/legacy_reports/FIELD_NAMING_FIX_REPORT.md          |  134 -
 docs/archive/legacy_reports/INFORMATION_REQUEST_TEMPLATE.md     |  207 --
 docs/archive/planning/AGENT_INTELLIGENCE_PLANNING.MD            | 1600 ---------
 docs/archive/planning/COMPLETE_IMPLEMENTATION_PLAN.md           |  410 ---
 docs/archive/planning/DISCOURSE_ANALYSIS_DEMONSTRATION_PLAN.md  |  240 --
 docs/archive/planning/FIX_AND_TEST_PLAN.md                      |  186 --
 docs/archive/planning/LONG_TERM_PLAN.md                         |  318 --
 docs/archive/planning/MASTER_INTEGRATION_PLAN.md                |  764 -----
 docs/archive/planning/MCP_INTEGRATION_PLAN.md                   |  436 ---
 docs/archive/planning/MID_TERM_PLAN.md                          |  712 ----
 docs/archive/planning/NEAR_TERM_IMPLEMENTATION_PLAN.md          |  353 --
 docs/archive/planning/UKRF_INTEGRATION_COORDINATION_PLAN.md     |  341 --
 docs/archive/planning/USABILITY_ROADMAP.md                      |  149 -
 docs/archive/planning/digimon_v2/ARCHITECTURE.md                |  319 --
 docs/archive/testing_report.md                                  |  139 -
 docs/digimon_onto_canon_ownership.md                            |    4 +
 docs/examples/graph_types.md                                    |  171 -
 docs/handoff_2026_04_03.md                                      |  252 --
 docs/handoff_2026_08_20_musique_digimon_optimization.md         |  274 --
 docs/improvements/improvements_answer_generation.md             |  130 -
 docs/improvements/improvements_content_retrieval.md             |   95 -
 docs/improvements/improvements_entity_search.md                 |   37 -
 docs/improvements/improvements_plan_generation.md               |   88 -
 docs/improvements/tool_composability_matrix.md                  |   66 -
 docs/meta-patterns/01_README.md                                 |  113 -
 docs/meta-patterns/02_claude-md-authoring.md                    |  292 --
 docs/meta-patterns/03_testing-strategy.md                       |  310 --
 docs/meta-patterns/04_mocking-policy.md                         |  177 -
 docs/meta-patterns/05_mock-enforcement.md                       |  219 --
 docs/meta-patterns/06_git-hooks.md                              |  263 --
 docs/meta-patterns/07_adr.md                                    |  270 --
 docs/meta-patterns/08_adr-governance.md                         |  156 -
 docs/meta-patterns/09_documentation-graph.md                    |  128 -
 docs/meta-patterns/10_doc-code-coupling.md                      |  260 --
 docs/meta-patterns/11_terminology.md                            |  143 -
 docs/meta-patterns/12_structured-logging.md                     |  246 --
 docs/meta-patterns/13_acceptance-gate-driven-development.md     |  617 ----
 docs/meta-patterns/14_acceptance-gate-linkage.md                |  313 --
 docs/meta-patterns/15_plan-workflow.md                          |  436 ---
 docs/meta-patterns/16_plan-blocker-enforcement.md               |  139 -
 docs/meta-patterns/17_verification-enforcement.md               |  196 --
 docs/meta-patterns/22_human-review-pattern.md                   |  164 -
 docs/meta-patterns/23_plan-status-validation.md                 |   98 -
 docs/meta-patterns/24_phased-adr-pattern.md                     |  255 --
 docs/meta-patterns/25_pr-review-process.md                      |  130 -
 docs/meta-patterns/27_conceptual-modeling.md                    |  210 --
 docs/meta-patterns/28_question-driven-planning.md               |  264 --
 docs/meta-patterns/29_uncertainty-tracking.md                   |  243 --
 docs/meta-patterns/30_gap-analysis.md                           |  208 --
 docs/meta-patterns/31_external-llm-review.md                    |   87 -
 docs/meta-patterns/32_recurring-issue-tracking.md               |  150 -
 docs/meta-patterns/33_uncertainty-resolution.md                 |  159 -
 docs/meta-patterns/34_engineering-workflow.md                   |  117 -
 docs/meta-patterns/35_cruft-lifecycle.md                        |   63 -
 docs/meta-patterns/AGENTS.md                                    |    9 -
 docs/meta-patterns/TEMPLATE.md                                  |   46 -
 docs/meta-patterns/worktree-coordination/18_claim-system.md     |   15 -
 .../worktree-coordination/19_worktree-enforcement.md            |   15 -
 docs/meta-patterns/worktree-coordination/20_rebase-workflow.md  |   15 -
 docs/meta-patterns/worktree-coordination/21_pr-coordination.md  |   15 -
 .../meta-patterns/worktree-coordination/26_ownership-respect.md |   15 -
 docs/meta-patterns/worktree-coordination/README.md              |   15 -
 docs/model/ODD.md                                               |    4 +
 docs/model/VIEW_COVERAGE.md                                     |    4 +
 docs/ops/CAPABILITY_DECOMPOSITION.md                            |    4 +
 docs/plans/02_digimon_v2_greenfield_planning_phase.md           |  128 -
 docs/plans/03_prove_adaptive_routing.md                         |  296 --
 docs/plans/04_graph_build_rearchitecture.md                     |  171 -
 docs/plans/05_extraction_quality_repair.md                      |  238 --
 docs/plans/06_two_pass_extraction_proof.md                      |  217 --
 docs/plans/07_extraction_iteration_supervisor.md                |  149 -
 docs/plans/08_supervisor_sentinel_gating.md                     |  126 -
 docs/plans/09_supervisor_smoke_build_gate.md                    |  125 -
 docs/plans/100_remaining-operator-wiring.md                     |  110 -
 ...tructured-query-operator-family-and-cypher-runtime-wiring.md |  198 --
 ...ink-public-operator-wiring-and-chunk-substrate-dependency.md |  140 -
 ...l-chunk-passage-substrate-and-first-public-chunk-operator.md |  176 -
 .../104_governed-passage-vector-retrieval-with-chunk-vdb.md     |  135 -
 ...05_governed-graph-to-passage-mappings-for-chunk-operators.md |  140 -
 .../106_governed-sparse-propagation-for-chunk-aggregator.md     |  148 -
 ...7_governed-relationship-score-propagation-operator-wiring.md |  116 -
 ...ic-entity-endpoint-extraction-from-observed-relationships.md |   93 -
 ...e-remaining-core-operators-full-trace-prompt-optimization.md |  257 --
 docs/plans/10_open_schema_type_contract.md                      |  145 -
 ...ructured-output-attempt-integrity-and-root-cause-recovery.md |  621 ----
 docs/plans/111_branch_reconciliation.md                         |  242 --
 docs/plans/111_canonical-typed-operator-composition.md          | 2621 ---------------
 docs/plans/111_consumer_truth_inventory.md                      |  164 -
 docs/plans/111_g10_chunk_vdb_ranking.md                         |  146 -
 docs/plans/111_g11_chunk_text_search_ranking.md                 |  214 --
 docs/plans/111_g12_agent_route_occurrences.md                   |  215 --
 docs/plans/111_g13_action_conformance_matrix.md                 |  149 -
 docs/plans/111_g14_manifest_descriptor_closure.md               |  214 --
 docs/plans/111_g15_planner_presentation_cutover.md              |  502 ---
 docs/plans/111_g1_relationship_onehop_graph_pack.md             |  286 --
 docs/plans/111_g2_chunk_from_relation_graph_pack.md             |  331 --
 docs/plans/111_g3_entity_ppr_multi_output.md                    |  450 ---
 docs/plans/111_g4_structured_list_conditional_domains.md        |  501 ---
 docs/plans/111_g5_implicit_state_merge_views.md                 |  623 ----
 docs/plans/111_g6_control_stop_synthesis.md                     |  397 ---
 docs/plans/111_g7_relationship_by_role_vertical.md              |  289 --
 docs/plans/111_g8_pcst_objective_capability.md                  |  117 -
 docs/plans/111_g9_chunk_occurrence_ranking.md                   |  103 -
 docs/plans/111_operator_composition_contract_mockup.md          |  696 ----
 docs/plans/111_operator_composition_coverage.md                 |   89 -
 docs/plans/111_progress.md                                      | 3598 --------------------
 docs/plans/112_plan-83-verification-evidence-repair.md          |   81 -
 docs/plans/113_maintained-source-rule-scope.md                  |   80 -
 docs/plans/114_ask-ui-governed-context-mode.md                  |  170 -
 docs/plans/115_ask-ui-operator-family-navigation.md             |  126 -
 docs/plans/116_ask-request-budget-contract-regression-repair.md |  126 -
 docs/plans/117_portable_content_verified_binding.md             |  217 --
 docs/plans/11_completeness_promotion_gate.md                    |  125 -
 .../121_project_meta_foundation_v1_3_projection_consumer.md     |  769 -----
 docs/plans/123_live-five-profile-ask-ui.md                      |  146 -
 docs/plans/124_evidence-only-quick-and-deep-query-seam.md       |  166 -
 docs/plans/12_musique_representation_audit.md                   |  152 -
 docs/plans/135_bounded_coordination_mailbox_adoption.md         |  162 -
 docs/plans/136_inside-success-demo-mvp-critical-path.md         |  776 -----
 docs/plans/137_structured-source-operator.md                    |  207 --
 docs/plans/138_canonical_ask_ui_lineage.md                      |  138 -
 .../139_inside-success-umbrella-m0-digimon-reconciliation.md    |  596 ----
 docs/plans/13_benchmark_anchor_resolution.md                    |  153 -
 docs/plans/141_agent-driven-wiki-traversal-and-data-handoff.md  | 1672 ----------
 ...foundation-identity-and-structured-query-parse-validation.md |  163 -
 docs/plans/143_five-person-ask-cockpit-readiness.md             |  176 -
 docs/plans/145_composable-retrieval-runtime-migration.md        | 1061 ------
 docs/plans/145_legacy_planner_migration_execution_packet.md     |  652 ----
 docs/plans/146_structured-cypher-execution-containment.md       |  207 --
 ...ion-first-repository-cleanup-and-external-dataset-custody.md |  176 -
 ...hive-superseded-root-handoffs-and-legacy-standalone-tests.md |  158 -
 ...nt-root-log-artifacts-and-add-guarded-local-cache-cleanup.md |  150 -
 docs/plans/14_fix_llm_client_benchmark_runner.md                |   94 -
 docs/plans/150_remove-legacy-stdio-vdb-storage-path.md          |  127 -
 .../plans/151_classify-root-executable-scripts-as-historical.md |  127 -
 docs/plans/152_retire-final-root-storage-default.md             |  112 -
 docs/plans/153_archive-unreferenced-codex-oob-experiment.md     |  142 -
 docs/plans/154_archive-completed-v2-planning-package.md         |  171 -
 .../155_reconcile-uppercase-and-lowercase-results-paths.md      |  134 -
 docs/plans/156_archive-stale-generated-publication-bundles.md   |  171 -
 .../157_data-subtree-ownership-and-orphan-fixture-cleanup.md    |  137 -
 docs/plans/158_explicit-data-archive-approval-boundary.md       |   84 -
 .../159_migrate-legacy-query-dataset-loader-out-of-data.md      |  111 -
 docs/plans/159_model_allowlist_cutover.md                       |   76 -
 docs/plans/15_operator_consolidation.md                         |  138 -
 docs/plans/160_explicit-dataset-and-artifact-root-contract.md   |  163 -
 .../161_explicit-worktree-safe-runtime-configuration-path.md    |  171 -
 ...-runtime-config-consumers-and-migrate-maintained-defaults.md |  157 -
 ...t-retired-standalone-scripts-and-prepare-archive-manifest.md |  180 -
 ...lit-maintained-mcp-imports-and-archive-legacy-generations.md |  200 --
 .../165_social-discourse-capability-group-disposition-audit.md  |  149 -
 ...-social-discourse-historical-application-archive-manifest.md |  136 -
 ...rical-non-default-script-tests-as-one-recoverable-package.md |  155 -
 .../168_governed-lifecycle-projection-consumer-readback.md      |  133 -
 docs/plans/169_truthful-typed-interrogative-planner-contract.md |  135 -
 docs/plans/16_build_attributes_sota_alignment.md                |  204 --
 docs/plans/170_audit-remaining-utility-and-testing-surfaces.md  |  175 -
 .../171_retire-removed-cli-smoke-and-sole-fixture-directory.md  |  158 -
 .../172_retire-stale-backend-and-cli-integration-harnesses.md   |  165 -
 docs/plans/173_audit-remaining-ignored-pytest-contracts.md      |  169 -
 docs/plans/174_retire-unconsumed-legacy-memory-system-pair.md   |  144 -
 ...consumed-memory-architecture-and-pattern-learning-package.md |  127 -
 docs/plans/176_foundation-value-carrier-preservation.md         |  170 -
 docs/plans/177_twin-situated-response-typed-reachability.md     |  228 --
 docs/plans/178_passage-to-assertion-typed-provenance-bridge.md  |  259 --
 ...ce-llm-client-pin-for-openrouter-ref-safe-planner-schemas.md |  154 -
 docs/plans/17_retest_thesis.md                                  |  319 --
 docs/plans/180_semantic-query-grounded-synthesis.md             |  117 -
 docs/plans/180_typed_assertion_role_pattern_selection.md        |  101 -
 docs/plans/181_gpa02_governed_model_facade.md                   |  210 --
 docs/plans/182_adopt_shared_concurrent_query_budget.md          |  868 -----
 ...84_route-maintained-digimon-embeddings-through-openrouter.md |   35 -
 .../185_temporal-evidence-status-and-current-claim-synthesis.md |  486 ---
 ...-contract-convergence-and-projection-surface-ratification.md |  301 --
 docs/plans/186_semantic_projection_consumer_design.md           |  291 --
 docs/plans/187_runtime-seam-provider-adoption.md                |   67 -
 docs/plans/188_inside_success_governed_ambiguity_projection.md  |   94 -
 docs/plans/189_multi_lens_discovery.md                          |   96 -
 docs/plans/18_ptc_validation.md                                 |   56 -
 docs/plans/191_governed_wiki_projection_contract.md             |   89 -
 docs/plans/192_governed_wiki_projection_compiler.md             |   77 -
 docs/plans/193_governed_wiki_topic_pages.md                     |  128 -
 docs/plans/194_bounded_governed_wiki_pages.md                   |   65 -
 docs/plans/195_bounded_wiki_source_snapshot.md                  |   54 -
 docs/plans/196_generic_wiki_query_handoff.md                    |   60 -
 docs/plans/197_persisted_semantic_query_catalog.md              |   57 -
 ..._grounded-research-governed-release-boundary-verification.md |  107 -
 docs/plans/199_governed-provider-projection-wiki-adapter.md     |  132 -
 ...omposition-code-and-reconcile-operator-action-count-drift.md |  394 ---
 ...ng-and-ambiguous-empty-result-contract-rule-via-git-hooks.md |  285 --
 .../202_block-canonical-checkout-commits-via-pre-commit-hook.md |  146 -
 ...03_entity-alias-short-form-canonicalization-failure-class.md |  501 ---
 .../204_stage-1-pinned-offline-local-embedding-provider.md      |  194 --
 docs/plans/205_plan247_clean_dependency_composition.md          |  204 --
 docs/plans/206_documentation_authority_consolidation.md         |  124 -
 docs/plans/207_canonical_runtime_conformance_truth_reset.md     |   80 -
 docs/plans/208_fresh_representative_operational_proof.md        |  226 --
 docs/plans/209_wiki_single_entry_question_router.md             |   53 -
 docs/plans/20_tool_linearization_and_planning_restore.md        |  130 -
 ...210_complete-situational-runtime-architecture-convergence.md |  359 --
 .../211_representation-composition-architecture-convergence.md  |  311 --
 docs/plans/212_typed_sna_method_pack.md                         |  108 -
 .../213_direct_retrieval_execution_boundary_convergence.md      |  145 -
 docs/plans/214_post-v1-runtime-and-capability-convergence.md    |  238 --
 docs/plans/215_finish-full-target-convergence.md                |    1 +
 docs/plans/216_sna_retrieval_analytic_case.md                   |  255 --
 docs/plans/217_aes_adoption_observe.md                          |    1 +
 docs/plans/218_sna_community_change_case.md                     |  121 -
 docs/plans/219_sna-http-and-mcp-entrypoints.md                  |  765 -----
 docs/plans/21_autonomous_failure_iteration_sprint.md            |  259 --
 docs/plans/220_ask-sna-interface.md                             |  241 --
 .../221_documentation_consolidation.adoption-attempts.jsonl     |    2 +
 .../221_documentation_consolidation.adoption-decision.json      |   15 +
 docs/plans/221_documentation_consolidation.bundle.json          |  861 +++++
 docs/plans/221_documentation_consolidation.facts.json           |   25 +
 docs/plans/221_documentation_consolidation.md                   |  206 ++
 docs/plans/221_documentation_consolidation.path-decision.json   |   57 +
 docs/plans/221_documentation_consolidation.receipt.json         |  681 ++++
 docs/plans/221_documentation_consolidation.verdicts.json        |  218 ++
 .../22_benchmark_first_canonicalization_projection_hardening.md |  417 ---
 docs/plans/22_bounded_rebuild_rerun_progress.md                 |   94 -
 .../23_semantic_build_boundary_and_onto_canon_experiment.md     |  239 --
 .../24_shared_run_progress_integration_for_graph_builds.md      |  225 --
 .../25_authoritative-coordination-prerequisite-remediation.md   |  172 -
 ...n-isolated-governed-refresh-and-ownership-baseline-repair.md |  157 -
 docs/plans/27_retrieval_strategy_heuristics.md                  |  200 --
 .../28_truthful_overnight_stabilization_and_contract_repair.md  |  521 ---
 ...29_declarative_decision_tracing_and_modular_agent_runtime.md |  278 --
 docs/plans/30_luna_five_question_evaluation_contract.md         |  137 -
 ..._overnight_controller_grounding_and_truthful_finalization.md |  660 ----
 docs/plans/31_investigation_browser_ui_and_provenance_mcp.md    |  220 --
 docs/plans/32_investigation_browser_ui.md                       |  413 ---
 docs/plans/33_decompose_first_controller_strategy.md            |  134 -
 docs/plans/34_harness_level_decompose_loop.md                   |  390 ---
 docs/plans/35_trace-eval-extraction-deferred.md                 |  171 -
 docs/plans/36_assertion_node_import_from_sqlite.md              |  335 --
 docs/plans/36_operator_topology_semantics_matrix.md             |   85 -
 docs/plans/37_query_time_graph_schema_awareness.md              |  212 --
 docs/plans/37_query_time_graph_schema_awareness_progress.md     |   51 -
 ..._python312_bootstrap_truth_and_shared_dependency_contract.md |  165 -
 docs/plans/39_structured-decompose-dependency-binding.md        |  308 --
 docs/plans/40_brittle_semantic_parsing_remediation.md           | 1283 --------
 docs/plans/61_next_gate_review_2026_06_21.md                    |   73 -
 .../61_remaining_workstream_consolidation_and_gate_review.md    |  250 --
 docs/plans/71_pipeline_workbench_ui.md                          |  525 ---
 docs/plans/72_benchmark_gaming_remediation.md                   |   92 -
 docs/plans/73_insidesuccess-retrieval-backend-eval-track.md     |  342 --
 ...wiss-army-knife-for-inside-success-e2e-verification-first.md |  224 --
 ...ed-onto-canon6-to-digimon-governed-e2e-retrieval-pipeline.md |  206 --
 ...6_eval-integrity-machinery-error-bucket-run-adequacy-gate.md |   96 -
 ...7_foundation-ir-1-1-consumer-switch-retire-reconstruction.md |   84 -
 ...fied-remediation-of-governed-lane-eval-integrity-findings.md |   89 -
 docs/plans/79_generalize_trace_verify_gate.md                   |   89 -
 docs/plans/80_governed_ask_ui.md                                |   52 -
 docs/plans/81_governed_graph_real_operators.md                  |  103 -
 .../plans/82_clean-digimon-query-build-graph-library-surface.md |  628 ----
 docs/plans/82_query_surface_mockup.md                           |  185 --
 .../83_audit-finding-remediation-and-verification-gates.md      |  187 --
 ..._post_plan_98_plan_state_and_library_trace_gate_selection.md |  111 -
 docs/plans/85_public_library_trace_gate.md                      |  161 -
 docs/plans/86_wiki-tab-for-claim-backed-current-state-pages.md  |  169 -
 docs/plans/87_ask_ui_answer_dynamic_operators.md                |  264 --
 docs/plans/88_cross_repo_contract_reset.md                      |  886 -----
 docs/plans/90_query_operator_surface_expansion.md               |  194 --
 docs/plans/91_graph_visualization_ui.md                         |  105 -
 docs/plans/92_inside_success_live_source_ui.md                  |   81 -
 docs/plans/93_merged_foundation_ir_wiki_tab.md                  |   81 -
 docs/plans/94_foundation_ir_mediawiki_surface.md                |  128 -
 docs/plans/94_remaining-operator-wiring.md                      |  130 -
 docs/plans/95_foundation_ir_mediawiki_navigation.md             |   71 -
 docs/plans/96_foundation_ir_mediawiki_demo_paths.md             |   68 -
 docs/plans/97_foundation_ir_notion_bundle.md                    |   69 -
 docs/plans/98_governed_e2e_infrastructure_trace_audit.md        |  101 -
 docs/plans/99_repo_audit_remediation_mainline_port.md           |   47 -
 docs/plans/AGENTS.md                                            |   15 +-
 docs/plans/BATCH_ITERATION_TEMPLATE.md                          |  178 -
 docs/plans/Digimon_for_KG_application#216.goal.md               |   36 -
 docs/plans/Digimon_for_KG_application#218.goal.md               |   18 -
 docs/plans/Digimon_for_KG_application#219.goal.md               |   57 -
 docs/plans/Digimon_for_KG_application#220.goal.md               |   18 -
 docs/plans/Digimon_for_KG_application#221.goal.md               |   18 +
 docs/plans/LOCKED_EVAL_PROTOCOL.md                              |  103 -
 docs/plans/ROADMAP.md                                           |   15 +-
 docs/plans/batch_01_musique_dev.md                              |  173 -
 docs/plans/batch_01_musique_dev_rerun_a.md                      |  138 -
 docs/plans/evidence/0134_ask_ui_deployment_reconciliation.md    |  331 --
 docs/plans/goals/2026-07-07-adaptive-knowledge-system.md        |   88 -
 docs/plans/goals/2026-07-07-archive-idea-extraction-audit.md    |   75 -
 .../goals/2026-07-07-archive-idea-extraction-deep-audit.md      |  328 --
 docs/plans/goals/2026-07-07-governed-e2e-full-pipeline.md       |   73 -
 docs/plans/goals/2026-07-08-governed-e2e-infra-trace-audit.md   |  183 --
 .../goals/2026-07-10-operator-wiring-adaptive-retrieval.md      |  140 -
 .../2026-07-11-wire-remaining-core-operators-full-traces.md     |  233 --
 .../2026-07-17-canonical-dynamic-source-tool-integration.md     |  247 --
 .../2026-07-25-complete-typed-planner-consumer-migration.md     |  301 --
 docs/plans/goals/_progress_adaptive_knowledge.md                |   73 -
 docs/plans/goals/_progress_archive_audit.md                     |  202 --
 docs/plans/goals/_progress_archive_deep_audit.md                |   95 -
 docs/plans/goals/_progress_governed_e2e.md                      |   55 -
 docs/plans/goals/_progress_governed_e2e_infra_trace_audit.md    |   83 -
 docs/plans/goals/_progress_operator_wiring.md                   |  163 -
 docs/plans/goals/_progress_remaining_core_operators.md          |  809 -----
 docs/plans/goals/readout_01_insidesuccess_families.md           |   44 -
 docs/plans/goals/readout_02_decision_grade_KILL.md              |   83 -
 docs/plans/progress/114_ask_ui_governed_context_mode.md         |   67 -
 docs/plans/progress/121_foundation_consumer_progress.md         |  147 -
 docs/plans/progress/30_linearization_data_loss_progress.md      | 4753 ---------------------------
 docs/plans/progress/30_luna_five_question_progress.md           |  158 -
 docs/plans/progress/30_luna_five_question_signoff.md            |   51 -
 docs/plans/progress/40_brittle_semantic_parsing_progress.md     | 2996 -----------------
 docs/plans/progress/81_session_handoff_2026-07-08.md            |  107 -
 docs/plans/progress/90_session_handoff_2026-07-09.md            |  187 --
 .../fix_atom_gate_and_relationship_search_verification.md       |  105 -
 docs/plans/progress/operator_wiring_handoff_2026-07-10.md       |  201 --
 docs/plans/progressive_disclosure_ptc_validation.md             |  161 -
 docs/plans/supporting/214_canonical_capability_authority.md     |  121 -
 .../supporting/214_inside_success_downstream_reconciliation.md  |  126 -
 docs/plans/supporting/214_inside_success_execution_packets.md   |  308 --
 docs/plans/supporting/214_personal_upstream_stop_rule.md        |  145 -
 docs/plans/supporting/214_runtime_surface_inventory.md          |  148 -
 docs/plans/supporting/40_non_regex_brittleness_audit.md         |  326 --
 docs/reports/2026-03-19_musique_50q_postmortem.md               |  215 --
 docs/reports/2026-03-21_graphrag_rebuild_research.md            |  336 --
 ...6-04-04_decision_trace_and_modular_agent_runtime_research.md |  337 --
 docs/reports/2026-07-13_operator-composition-build-vs-adopt.md  |  279 --
 docs/reports/216_capability_ledger.md                           |    4 +
 docs/reports/216_phase1_records_to_graph.md                     |  348 --
 docs/reports/216_sna_case_pheme_ferguson.md                     |    6 +-
 docs/reports/218_sna_community_change_pheme_ferguson.md         |    6 +-
 docs/reports/219_sna_protocols.md                               |    8 +-
 docs/reports/220_ask_sna.md                                     |    6 +-
 docs/reports/musique_19q_iteration_report_2026_04_03.md         |   58 -
 eval/BENCHMARK_NOTES.md                                         |   86 -
 eval/DATASET_ERRATA.md                                          |   28 -
 eval/benchmark_iteration_tasks.md                               |   63 -
 generated/docstring_wiki.md                                     |  779 +++++
 investigation_browser/frontend/README.md                        |   73 -
 investigations/2026-02-16-dependency-chain.md                   |  390 ---
 investigations/2026-04-05-failure-diagnosis.md                  |  526 ---
 investigations/2026-04-06-session-state-contamination.md        |  104 -
 .../2026-04-06-todo-write-atomicity-entity-visibility.md        |   76 -
 investigations/2026-07-09-issue-025-trace-gate-budget.md        |   41 -
 .../2026-07-09-plan-88-multifield-independent-signoff.md        |   40 -
 .../2026-07-09-plan-88-multifield-seam-audit-remediation.md     |  125 -
 .../2026-07-09-plan-88-source-binding-independent-signoff.md    |   65 -
 investigations/2026-07-09-plan-88-source-binding-remediation.md |  101 -
 investigations/2026-07-11-chunk-passage-substrate.md            |  166 -
 investigations/2026-07-11-plan88-runtime-contract-debt.md       |  186 --
 investigations/2026-07-11-remaining-unit-debt-cleanup.md        |  104 -
 investigations/2026-07-11-repo-audit-remediation.md             |  135 -
 .../2026-07-12-available-action-schema-eval-signoff.md          |   53 -
 investigations/2026-07-12-matched-schema-eval-signoff.md        |  123 -
 investigations/2026-07-12-plan111-adversarial-plan-audit.md     |  269 --
 investigations/2026-07-12-plan111-contract-boundary-review.md   |  202 --
 .../2026-07-12-plan111-record-reference-contract-audit.md       |  722 ----
 investigations/2026-07-12-planner-schema-heldout-protocol.md    |   81 -
 investigations/2026-07-12-planner-unobserved-relationship-id.md |   99 -
 .../2026-07-12-structured-attempt-retry-ledger-gap.md           |  210 --
 investigations/2026-07-12-target-scoped-trace-source-binding.md |  238 --
 investigations/2026-07-13-public-ui-runtime-failures.md         |  188 --
 investigations/2026-07-14-dynamic-trace-step-cap.md             |   82 -
 investigations/2026-07-14-plan111-repair-row-reconciliation.md  |  118 -
 .../2026-07-14-rerank-exact-permutation-schema-gap.md           |  174 -
 investigations/2026-07-14-worktree-runtime-and-trace-gate.md    |  133 -
 investigations/2026-07-15-issue-60-directed-foundation-ir.md    |  347 --
 investigations/2026-07-15-role-edge-target-invariant.md         |  233 --
 investigations/2026-07-16-ask-ledger-instance-divergence.md     |  128 -
 investigations/2026-07-16-ask-ui-demo-use-path.md               |   45 -
 investigations/2026-07-16-demo-model-routing.md                 |  118 -
 investigations/2026-07-16-shipping-ask-premature-completion.md  |  410 ---
 investigations/2026-07-17-tailscale-wiki-people-integration.md  |  116 -
 .../2026-07-21-agent-wiki-traversal-implementation.md           |  245 --
 investigations/2026-07-21-deep-wiki-obligation-parallelism.md   |  135 -
 .../2026-07-21-structured-source-execution-feedback.md          |   96 -
 .../2026-07-22-context-atlas-distinct-audience-route.md         |   80 -
 .../2026-07-22-deep-source-failure-collapses-evidence.md        |   52 -
 investigations/2026-07-22-graph-session-multi-wiki-advice.md    |  133 -
 .../2026-07-22-hermes-tool-absence-and-composition-boundary.md  |  173 -
 .../2026-07-22-hermes-tool-discovery-and-dynamism-status.md     |  199 --
 investigations/2026-07-23-plan145-s1-live-situational-trace.md  |  211 --
 investigations/2026-07-23-structured-cypher-runtime-wedge.md    |  183 --
 investigations/2026-09-13-analysis-surface-cleanup.md           |   69 -
 investigations/2026-09-24-foundation-ir-nary-role-fidelity.md   |   79 -
 investigations/INDEX.md                                         |   41 -
 investigations/chatgpt-review-sweep-manifest.md                 |   44 -
 investigations/digimon/2026-03-23-both-fail-pre-analysis.md     |   78 -
 investigations/digimon/2026-03-23-musique-failure-diagnosis.md  |   67 -
 investigations/digimon/2026-04-01-oracle-diagnosis-llm.md       |  355 --
 investigations/digimon/2026-04-01-oracle-diagnosis.md           |  349 --
 investigations/digimon/2026-04-02-oracle-diagnosis.md           |  322 --
 .../digimon/2026-04-07-graph-viz-library-comparison.md          |  274 --
 investigations/digimon/2026-04-07-oracle-diagnosis-heuristic.md |   89 -
 .../digimon/2026-04-11-graph-ontology-and-identity-vision.md    |  541 ---
 investigations/digimon/2026-04-12-graph-vision-doc-audit.md     |  392 ---
 investigations/digimon/2026-04-12-repo-docs-and-plans-audit.md  |  438 ---
 .../digimon/2026-04-14-repo-docs-and-plans-audit-followup.md    |  471 ---
 investigations/digimon/2026-06-22-docs-plans-worktree-audit.md  |  123 -
 investigations/digimon/2026-06-22-semantic-regex-audit.md       |  287 --
 .../2026-06-24-plan40-slice1-descriptor-fidelity-assessment.md  |  171 -
 .../digimon/2026-06-24-semantic-llm-extraction-audit.md         |  405 ---
 investigations/digimon/2026-07-06-code-audit-and-remediation.md |   75 -
 .../digimon/2026-07-06-eval-integrity-and-drift-decisions.md    |  123 -
 .../digimon/2026-07-21-foundation-identity-and-cypher-parse.md  |  253 --
 .../digimon/2026-07-23-codex-mcp-startup-and-rollout-state.md   |  150 -
 .../digimon/2026-07-23-population-wiki-fact-transition.md       |  193 --
 .../digimon/2026-07-24-memory-system-contract-disposition.md    |  132 -
 .../2026-08-20-musique-digimon-optimization-stress-test.md      |  769 -----
 scripts/check_markdown_links.py                                 |   11 +-
 scripts/meta/check_repo_rules.py                                |   75 +-
 scripts/relationships.yaml                                      |    4 +-
 tests/AGENTS.md                                                 |    6 +
 tests/README.md                                                 |    4 +
 tests/e2e/AGENTS.md                                             |    9 -
 tests/integration/AGENTS.md                                     |    9 -
 tests/unit/AGENTS.md                                            |    8 -
 tests/unit/test_capability_status_contract.py                   |   23 +-
 tests/unit/test_check_repo_rules.py                             |  134 +-
 tools/vendor/enforced_planning_docstring_wiki/UPSTREAM.md       |   24 +
 .../src/enforced_planning/__init__.py                           |    1 +
 .../src/enforced_planning/docstring_wiki.py                     |  209 ++
 .../src/enforced_planning/relationship_context.py               |  594 ++++
 ui/INDEX.md                                                     |    6 +-
 wiki/architecture-gap.md                                        |    6 +-
 wiki/architecture.md                                            |    2 +-
 wiki/benchmark-reality.claims.yaml                              |   10 +-
 wiki/benchmark-reality.md                                       |    2 +-
 wiki/current-state.claims.yaml                                  |    6 +-
 wiki/current-state.md                                           |    6 +-
 wiki/index.md                                                   |   28 +-
 wiki/log.md                                                     |    4 +
 535 files changed, 4551 insertions(+), 106794 deletions(-)
```

Declared durable paths on `origin/main` today (plans role excluded): `NORTH_STAR.md`, `.aes/target.yaml`, `docs/adr`, `docs/model/ARCHITECTURE.md`, `docs/model/trace.yaml`. Touched by this plan's commits: `NORTH_STAR.md`, `docs/adr/001-agent-orchestration-architecture.md`, `docs/adr/002-universal-graph-schema-and-extraction.md`, `docs/adr/003-graph-tool-suites.md`, `docs/adr/004-graph-build-rearchitecture.md`, `docs/adr/005-typed-extraction-validation.md`, `docs/adr/006-open-tkg-grounded-entity-policy.md`, `docs/adr/007-entity-relationship-closure.md`, `docs/adr/008-pure-lane-build-comparisons.md`, `docs/adr/009-two-pass-extraction-for-completeness.md`, `docs/adr/010-tool-applicability-architecture.md`, `docs/adr/011-extraction-iteration-supervisor.md`, `docs/adr/012-open-schema-does-not-inject-default-type-palette.md`, `docs/adr/013-answer-critical-fact-representation.md`, `docs/adr/014-tool-consolidation-surface.md`, `docs/adr/015-strategic-risks-thesis-test.md`, `docs/adr/016-declarative-decision-tracing-and-agent-runtime-declaration.md`, `docs/adr/017-nary-graph-representation-and-onto-canon-import.md`, `docs/adr/018-federated-canonical-action-manifest.md`, `docs/adr/019-composition-state-policy-and-transition-separation.md`, `docs/adr/020-graph-projection-surface-contract.md`, `docs/adr/021-analytic-operator-role.md`, `docs/adr/022-representation-ir-native-execution.md`, `docs/adr/023-agent-owned-situational-reasoning-and-direct-execution-boundary.md`.

Full diff of `NORTH_STAR.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/NORTH_STAR.md b/NORTH_STAR.md
index e666ce41..a5181ec6 100644
--- a/NORTH_STAR.md
+++ b/NORTH_STAR.md
@@ -1,3 +1,7 @@
+---
+description: "States DIGIMON's durable purpose, design principles and what it deliberately does not require, while deferring status, architecture and priorities to other documents."
+---
+
 # DIGIMON North Star
 
 **Purpose:** state the durable reason DIGIMON exists. This file does not own current implementation status, deployment state, benchmark evidence, or next-task priority.
```

Full diff of `docs/adr/001-agent-orchestration-architecture.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/001-agent-orchestration-architecture.md b/docs/adr/001-agent-orchestration-architecture.md
index 0b4e9a36..bdff0dcf 100644
--- a/docs/adr/001-agent-orchestration-architecture.md
+++ b/docs/adr/001-agent-orchestration-architecture.md
@@ -1,3 +1,7 @@
+---
+description: "February 2026 decision record on whether the calling client or DIGIMON's internal model chooses orchestration, and why mid-pipeline reasoning needs a capable internal model."
+---
+
 # ADR-001: Agent Orchestration Architecture
 
 **Status**: Accepted
```

Full diff of `docs/adr/002-universal-graph-schema-and-extraction.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/002-universal-graph-schema-and-extraction.md b/docs/adr/002-universal-graph-schema-and-extraction.md
deleted file mode 100644
index 45b34cae..00000000
--- a/docs/adr/002-universal-graph-schema-and-extraction.md
+++ /dev/null
@@ -1,390 +0,0 @@
-# ADR-002: Universal Graph Schema and Configurable Extraction
-
-**Status**: Proposed
-**Date**: 2026-02-16
-**Context**: DIGIMON currently has 5 graph types with hardcoded extraction prompts. Onto-canon defines a superset attribute schema. We need a unified architecture where graph type configuration drives extraction, ontology constraints, and post-build enrichment.
-
----
-
-## Problem
-
-Three independent problems that share a root cause:
-
-1. **Extraction prompts are hardcoded Python strings** in `Core/Prompt/GraphPrompt.py`. Adding a new graph type or modifying extraction behavior requires editing Python code. Violates "Prompts as Data" principle.
-
-2. **No schema enforcement**. The `custom_ontology_path` config appends guidance text to prompts, but the LLM can ignore it. No validation, no schema-constrained enforcement, no schema_guided "approved list + propose new" workflow.
-
-3. **No n-ary relationships or reification**. All extraction produces binary `(source, relation, target)` tuples. Events involving 3+ participants are flattened into multiple binary edges that lose role information ("who did what to whom").
-
-4. **No post-build enrichment pipeline**. Entity canonicalization, Q-code resolution, and schema validation are not part of the build process. The graph goes straight from raw LLM output to persistence.
-
-## Decision
-
-### 1. Attribute Schema: Onto-Canon as Superset
-
-Every graph attribute lives in a single schema. Graph types are subsets.
-
-**Node Attributes:**
-
-| Attribute | Type | Source | Graph Types |
-|-----------|------|--------|-------------|
-| `name` | str | Extraction | All |
-| `type` | str | Extraction | TKG, RKG, Reified |
-| `description` | str | Extraction | TKG, RKG, Reified |
-| `qcode` | str | Post-build enrichment | Any (optional) |
-| `canonical_name` | str | Post-build canonicalization | Any (optional) |
-| `source_ids` | list[str] | Extraction | All |
-
-**Edge Attributes:**
-
-| Attribute | Type | Source | Graph Types |
-|-----------|------|--------|-------------|
-| `relation_name` | str | Extraction | KG, RKG, Reified |
-| `description` | str | Extraction | TKG, RKG, Reified |
-| `weight` | float | Extraction | All |
-| `keywords` | list[str] | Extraction | RKG |
-| `source_ids` | list[str] | Extraction | All |
-| `amr_predicate` | str | Post-build enrichment | Any (optional) |
-| `probability` | float | Post-build enrichment | Any (optional) |
-
-**Role Attributes (Reified graph type only):**
-
-| Attribute | Type | Source |
-|-----------|------|--------|
-| `role` | str | Extraction (ARG0, ARG1, ARG2, ...) |
-| `role_label` | str | Extraction (agent, patient, instrument, ...) |
-
-### 2. Graph Type Configs Drive Prompt Selection
-
-Each graph type is defined by a YAML config that specifies:
-
-```yaml
-# prompts/graph_types/tkg.yaml
-graph_type: "tkg"
-display_name: "Typed Knowledge Graph"
-
-# Which attributes this graph type extracts
-node_attributes: [name, type, description]
-edge_attributes: [relation_name, description, weight]
-reification: false
-
-# Prompt template for extraction
-extraction_template: "prompts/extraction/tkg_extraction.yaml"
-
-# Prompt template for gleaning (follow-up "did you miss anything?")
-gleaning_template: "prompts/extraction/gleaning.yaml"
-
-# Output parser (how to interpret LLM output)
-parser: "delimiter"  # "delimiter" | "json" | "amr"
-```
-
-```yaml
-# prompts/graph_types/reified.yaml
-graph_type: "reified"
-display_name: "Reified Event Graph"
-
-node_attributes: [name, type, description]
-edge_attributes: [relation_name, description, weight, role, role_label]
-reification: true
-
-extraction_template: "prompts/extraction/reified_extraction.yaml"
-gleaning_template: "prompts/extraction/gleaning.yaml"
-parser: "json"
-```
-
-The extraction prompt templates use Jinja2 and are stored in `prompts/extraction/`:
-
-```yaml
-# prompts/extraction/tkg_extraction.yaml
-system: |
-  You are an entity and relationship extraction system.
-
-user: |
-  Given the following text, extract all entities and relationships.
-
-  {% if schema_mode == "schema_constrained" %}
-  You MUST only use entity types from this list: {{ entity_types | join(", ") }}
-  You MUST only use relationship types from this list: {{ relation_types | join(", ") }}
-  If you encounter an entity or relationship that doesn't fit these types, skip it.
-  {% elif schema_mode == "schema_guided" %}
-  Prefer these entity types: {{ entity_types | join(", ") }}
-  Prefer these relationship types: {{ relation_types | join(", ") }}
-  If you encounter something that clearly doesn't fit any of these types but is important,
-  you may propose a new type. Mark proposed types with [NEW] prefix.
-  {% else %}
-  {# open mode - no constraints #}
-  Extract all entity types you find relevant.
-  {% endif %}
-
-  {% if custom_guidance %}
-  {{ custom_guidance }}
-  {% endif %}
-
-  Text: {{ input_text }}
-```
-
-### 3. Schema Modes: Open, Schema-Guided, Schema-Constrained
-
-Three modes configured per graph build:
-
-```yaml
-# In config file or passed as config_overrides to graph_build_*
-graph:
-  schema_mode: "schema_guided"  # "open" | "schema_guided" | "schema_constrained"
-
-  # For schema-guided/schema-constrained modes:
-  ontology:
-    entity_types:
-      - person: "A human individual"
-      - organization: "A company, government, or group"
-      - location: "A geographic place"
-      - event: "A specific occurrence or happening"
-    relation_types:
-      - employed_by: "Person works for organization"
-      - located_in: "Entity is in a location"
-      - participated_in: "Entity took part in event"
-    role_types:  # Only for reified graph type
-      - agent: "The entity performing the action (ARG0)"
-      - patient: "The entity being acted upon (ARG1)"
-      - instrument: "The means by which action is performed (ARG2)"
-```
-
-**Enforcement levels:**
-
-| Mode | Extraction | Validation | New types |
-|------|-----------|------------|-----------|
-| **Open** | No constraints in prompt | No validation | All accepted |
-| **Schema-Constrained** | Prompt constrains to list | Post-extraction rejects out-of-schema | Rejected |
-| **Schema-Guided** | Prompt prefers list, allows `[NEW]` | Post-extraction flags `[NEW]` types | Logged for review, accepted provisionally |
-
-Schema-guided mode connects to onto-canon's predicate governance pipeline: `[NEW]` types are equivalent to `predicate_proposals` with status `pending`. An agent or human can later promote, reject, or merge them.
-
-### 3b. Canonicalization Aggressiveness (Orthogonal to Schema Mode)
-
-Schema mode controls what the LLM **extracts**. Canonicalization aggressiveness controls how hard we **merge** extracted output into canonical vocabularies **post-extraction**. These are independent dimensions:
-
-```
-                    Canonicalization Aggressiveness
-                    none        conservative    aggressive
-Extraction    ┌──────────────┬───────────────┬──────────────┐
-Constraint    │              │               │              │
-  open        │ current      │               │ "open-       │
-              │ behavior     │               │  minimal"    │
-              │              │               │              │
-  schema_guided       │              │               │              │
-              │              │               │              │
-  schema_constrained      │              │               │ maximum      │
-              │              │               │ constraint   │
-              └──────────────┴───────────────┴──────────────┘
-```
-
-**"Open-minimal"** = open extraction (no prompt constraints — LLM extracts whatever it finds) + aggressive post-extraction canonicalization (merge everything into the smallest possible vocabulary). The ontology stays small not by constraining the LLM, but by canonicalizing its output.
-
-Canonicalization applies to **three independent targets**, each with its own aggressiveness setting:
-
-```yaml
-# In config
-post_build:
-  canonicalize:
-    entities:
-      enabled: true
-      aggressiveness: "conservative"  # "none" | "conservative" | "aggressive"
-      # conservative: exact abbreviations, case variants only
-      # aggressive: fuzzy semantic similarity via LLM
-      merge_threshold: 0.85
-
-    relations:
-      enabled: true
-      aggressiveness: "aggressive"
-      # conservative: exact verb stem match to PropBank
-      # aggressive: LLM maps "funded", "gave money to", "bankrolled" → fund-01
-      vocabulary: "propbank"  # "propbank" | "framenet" | "custom"
-
-    entity_types:
-      enabled: true
-      aggressiveness: "moderate"
-      # conservative: exact SUMO type match
-      # aggressive: LLM maps "spy agency" → GovernmentOrganization
-      vocabulary: "sumo"  # "sumo" | "custom"
-```
-
-**Why SUMO/PropBank/FrameNet may make custom ontology lists unnecessary**: These canonical vocabularies already define a minimal, principled set of types and predicates:
-- **PropBank**: ~7,000 verb senses with argument structure (fund-01, attack-01, employ-01)
-- **SUMO**: ~100 top-level types in a formal hierarchy (Agent, Organization, Process, etc.)
-- **FrameNet**: ~1,200 frames with named roles (Employer, Employee, Position, etc.)
-
-A "schema_constrained" ontology with a hand-curated list of 10 entity types is just a subset of SUMO. A hand-curated list of 20 relation types is just a subset of PropBank. The canonical vocabularies ARE the principled version of what hand-curated lists approximate.
-
-**The aggressiveness dimension operates at three levels, not one.** Canonicalization isn't just "map messy text into canonical senses." It also controls how coarse-grained the canonical vocabulary itself becomes — merging senses with each other:
-
-```
-Level 1: Surface → Sense         "bankrolled" → fund-01             (text normalization)
-Level 2: Sense → Sense Group     fund-01 + invest-01 → same group  (semantic merging)
-Level 3: Sense Group → Type      financial transfers → Transaction  (ontological abstraction)
-```
-
-The canonical vocabularies provide the hierarchy for all three levels:
-- **PropBank** defines ~7,000 senses (Level 1 targets)
-- **FrameNet** groups related senses into ~1,200 frames (Level 2 grouping: `fund-01` and `invest-01` share a frame)
-- **SUMO** defines ~100 top-level types (Level 3 abstraction: both map to `Transaction`)
-
-Aggressiveness controls how far up you climb:
-
-| Aggressiveness | Entities | Relations | Types |
-|---------------|----------|-----------|-------|
-| **None** | Raw extracted names | Raw extracted verbs | Raw extracted types |
-| **Conservative** | Merge exact abbreviations ("CIA" ↔ "Central Intelligence Agency") | Map to PropBank sense ("funded" → `fund-01`) | Map to exact SUMO type |
-| **Moderate** | Merge contextual references ("the Agency" ↔ "CIA") | Map to PropBank AND merge similar senses (`fund-01` + `finance-01` → same group via FrameNet frame) | Map to SUMO parent type |
-| **Aggressive** | Merge by semantic similarity (LLM decides) | Collapse entire FrameNet frames into single predicates (`fund-01` + `invest-01` + `bankroll` → `FINANCIAL_TRANSFER`) | Collapse to SUMO top-level (~20 types) |
-
-**This replaces hand-curated ontology lists**: A schema-constrained ontology with 10 entity types and 20 relation types is just an ad-hoc slice of SUMO/PropBank. Setting `aggressiveness: "aggressive"` with SUMO/PropBank/FrameNet as the vocabulary achieves the same effect systematically — the ontology stays minimal because semantically similar extractions get collapsed, and the granularity is controlled by a single parameter rather than per-domain curation.
-
-**Cypher/openCypher becomes valuable as aggressiveness increases**: With no canonicalization, edge labels are messy ("directed", "is the director of", "was directed by") — Cypher pattern matching fails on label mismatch. At conservative aggressiveness, these become `direct-01` — Cypher works on exact senses. At aggressive, `fund-01` and `invest-01` collapse to the same label — Cypher queries become more general and more powerful. The value of structured queries scales directly with canonicalization aggressiveness.
-
-**Cypher implementation note**: [txtai](https://github.com/neuml/txtai) uses NetworkX as its default graph backend (same as DIGIMON) and has integrated [GrandCypher](https://github.com/aplbrain/grand-cypher) for Cypher queries over NetworkX graphs. This is a proven approach — no need to write a custom parser.
-
-### 4. Reification for N-ary Relationships
-
-For the `reified` graph type, extraction produces events as nodes with role-typed edges to participants:
-
-**Current binary extraction:**
-```
-("relationship", "CIA", "Operation Cyclone", "CIA funded Operation Cyclone", 9)
-```
-→ One edge: CIA → Operation Cyclone
-
-**Reified extraction:**
-```json
-{
-  "event": {
-    "name": "funding_001",
-    "type": "event",
-    "predicate": "fund-01",
-    "description": "CIA funded Operation Cyclone through ISI"
-  },
-  "participants": [
-    {"entity": "CIA", "role": "ARG0", "label": "agent"},
-    {"entity": "Operation Cyclone", "role": "ARG1", "label": "patient"},
-    {"entity": "ISI", "role": "ARG2", "label": "intermediary"}
-  ]
-}
-```
-→ One event node + three role-typed edges:
-- CIA →[ARG0:agent]→ funding_001
-- Operation Cyclone →[ARG1:patient]→ funding_001
-- ISI →[ARG2:intermediary]→ funding_001
-
-This is the diamond pattern on NetworkX. No storage layer changes needed. The event node has `type: "event"` and `predicate: "fund-01"`. The edges have `role` and `role_label` attributes.
-
-**Operator compatibility**: Existing operators (onehop, PPR, VDB search) work unmodified — they traverse nodes and edges regardless of whether a node represents an entity or an event. The topology is the same. Operators that need to distinguish can check `node.type == "event"`.
-
-### 5. Post-Build Enrichment Pipeline
-
-After extraction and graph construction, optional enrichment steps run in sequence:
-
-```yaml
-# In config
-post_build:
-  - canonicalize_entities:
-      enabled: true
-      method: "llm_fuzzy"        # "llm_fuzzy" | "qcode" | "exact_only"
-      batch_size: 100            # entities per LLM call
-      merge_threshold: 0.85     # confidence threshold for auto-merge
-  - resolve_qcodes:
-      enabled: false             # Wikidata Q-code resolution
-  - validate_schema:
-      enabled: false             # reject/flag out-of-schema types (schema_constrained mode)
-  - map_predicates:
-      enabled: false             # map relation_name → AMR predicate via onto-canon
-```
-
-**Entity canonicalization** (the immediate need):
-
-```python
-async def canonicalize_entities(graph: NetworkXStorage, llm, config) -> CanonResult:
-    """Post-build entity dedup via LLM fuzzy matching.
-
-    1. Collect all node names from graph
-    2. Batch into groups of ~100
-    3. For each batch, ask LLM: "Which of these refer to the same entity?"
-    4. For each merge group: pick canonical name, merge node attributes,
-       redirect all edges, remove duplicate nodes
-    5. Return stats: {merged: int, total_before: int, total_after: int}
-    """
-```
-
-This reuses the prompt logic from `onto-canon/onto_canon/concept_dedup.py` (`match_entities_to_concepts`) but operates directly on the NetworkX graph without needing SQLite.
-
-### 6. File Layout
-
-```
-prompts/
-  graph_types/           # Graph type definitions
-    kg.yaml              # Binary KG (name + relation + weight only)
-    tkg.yaml             # Typed KG (+ type, descriptions)
-    rkg.yaml             # Rich KG (+ keywords)
-    reified.yaml         # Reified event graph (+ roles)
-    tree.yaml            # Chunk tree
-    passage.yaml         # Passage graph
-  extraction/            # Extraction prompt templates (Jinja2)
-    kg_extraction.yaml
-    tkg_extraction.yaml
-    rkg_extraction.yaml
-    reified_extraction.yaml
-    gleaning.yaml        # Shared gleaning template
-  ontology/              # Ontology constraint files (for schema_guided/schema_constrained)
-    hotpotqa_types.yaml  # Domain-specific type lists
-    general_types.yaml   # General-purpose defaults
-  canonicalization/      # Canonicalization prompts
-    entity_dedup.yaml    # "Which of these are the same entity?"
-```
-
-## Integration Points
-
-### With onto-canon
-
-- **Entity canonicalization**: Reuse `match_entities_to_concepts` prompt from `onto-canon/prompts/concept_dedup/match_concepts.yaml`
-- **Q-code resolution**: Call `onto-canon/onto_canon/wikidata_entity_search.py` in the `resolve_qcodes` post-build step
-- **Predicate governance**: `[NEW]` types from schema_guided mode feed into onto-canon's `predicate_proposals` table
-- **Schema validation**: Onto-canon's SUMO constraints can validate extracted types in the `validate_schema` step
-
-### With existing DIGIMON code
-
-- `GraphPrompt.py` becomes a loader that reads YAML templates instead of containing hardcoded strings
-- `ERGraph`, `RKGraph` read their graph type config to select templates
-- `_build_graph_from_records` / `_build_graph_from_tuples` gain a `reified` code path for diamond-pattern nodes
-- `BaseGraph.build_graph()` gains a post-build enrichment hook
-- `GraphConfig.py` (plus YAML config inputs) gains `schema_mode`, `schema_entity_types`, and `post_build` sections
-- No operator changes needed (topology-agnostic)
-
-## Implementation Order
-
-1. **Entity canonicalization post-build step** — The most immediate value. Adapts onto-canon's `match_entities_to_concepts()` for direct NetworkX graph operation. Configurable `merge_threshold`. No dependency on prompts-as-data.
-2. **Prompts as data** — Move extraction prompts from `GraphPrompt.py` to YAML/Jinja2 templates. Load via `llm_client.render_prompt()`. No behavior change, just externalization. Unblocks ontology modes.
-3. **Relation canonicalization post-build step** — Map extracted relation names to PropBank senses via onto-canon's AMR pipeline. Configurable aggressiveness. Unblocks Cypher.
-4. **Schema modes** — Add `schema_mode` config + Jinja2 conditionals in templates. Open mode is current behavior. Schema-guided/schema-constrained add constraints. Consider: SUMO/PropBank as the canonical type/relation lists rather than hand-curated per-domain lists.
-5. **Cypher query tool** — Integrate [GrandCypher](https://github.com/aplbrain/grand-cypher) for openCypher queries on NetworkX. Value scales with canonicalization aggressiveness — most useful after step 3.
-6. **Entity type canonicalization** — Map extracted types to SUMO hierarchy. Configurable aggressiveness.
-7. **Reified graph type** — New extraction template + JSON parser + diamond-pattern builder. For n-ary events (intelligence analysis use case, not needed for QA benchmarks).
-8. **Full post-build pipeline** — Q-code resolution, schema validation as optional enrichment steps.
-
-## Consequences
-
-**Positive:**
-- Graph types become data-driven, not code-driven
-- New graph types can be added by writing YAML, not Python
-- Ontology constraints are configurable per-build
-- Entity canonicalization improves multi-hop traversal
-- Reification enables event-centric reasoning (who did what to whom)
-- Post-build enrichment is modular and optional
-
-**Negative:**
-- Template loading adds indirection vs hardcoded strings
-- Reified graphs have more nodes (event nodes), increasing graph size
-- LLM fuzzy dedup in post-build adds cost and latency to graph construction
-- Mixed ontology mode requires human-in-the-loop or governance automation
-
-**Risks:**
-- Reified extraction may produce inconsistent event boundaries (LLM decides what constitutes "one event")
-- Schema-constrained mode may cause the LLM to force-fit entities into wrong types rather than skip them
-- Entity canonicalization may over-merge (merge distinct entities with similar names)
```

Full diff of `docs/adr/003-graph-tool-suites.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/003-graph-tool-suites.md b/docs/adr/003-graph-tool-suites.md
deleted file mode 100644
index 4308eac7..00000000
--- a/docs/adr/003-graph-tool-suites.md
+++ /dev/null
@@ -1,307 +0,0 @@
-# ADR-003: Three Graph Tool Suites — Creation, Retrieval, Mutation
-
-**Status**: Proposed
-**Date**: 2026-02-16
-**Context**: DIGIMON has 53 MCP tools and 27 operators covering graph creation and read-only retrieval. Graph mutation (update, delete, belief revision) is absent. Onto-canon has working belief revision but operates on SQLite, not NetworkX. This ADR defines the complete tool architecture across three suites.
-
----
-
-## Problem
-
-1. **No graph mutation**. All 27 operators are read-only. The storage layer has `upsert_node`/`upsert_edge` (used during build) but no `delete_node`, `delete_edge`, or selective update. Once a graph is built, the only mutation is `clear()` (wipe everything).
-
-2. **No structured query language**. All retrieval is operator-based (PPR, VDB search, k-hop). There is no way to express ad-hoc graph patterns like "find all PERSON nodes connected to ORGANIZATION nodes via EMPLOYED_BY edges." Operators compose well but can't express arbitrary pattern matching.
-
-3. **No belief revision on graphs**. Onto-canon has `canon_update_belief`, `canon_find_tensions`, `canon_resolve_tension` operating on SQLite beliefs. These don't apply to DIGIMON's NetworkX graphs. An edge added during extraction can't be weakened, retracted, or superseded without rebuilding.
-
-4. **Creation tools lack post-build enrichment**. Graph building goes straight from LLM extraction to persistence. No entity canonicalization, no Q-code resolution, no schema validation (see ADR-002).
-
----
-
-## Decision
-
-Organize all graph tools into three suites. Each suite has clear boundaries for what EXISTS today vs what is PROPOSED.
-
-### Suite 1: Creation (Graph Building)
-
-Tools that construct graphs from source documents.
-
-#### EXISTS Today (7 MCP tools)
-
-| Tool | What it does |
-|------|-------------|
-| `corpus_prepare` | Convert files (.txt, .md, .json, .csv, .pdf) to DIGIMON corpus format |
-| `graph_build_er` | Build entity-relationship graph (TKG) |
-| `graph_build_rk` | Build rich keyword graph (RKG) |
-| `graph_build_tree` | Build hierarchical chunk tree |
-| `graph_build_tree_balanced` | Build balanced chunk tree |
-| `graph_build_passage` | Build passage-level graph |
-| `entity_vdb_build` | Build vector database index from graph entities |
-
-Supporting infrastructure:
-- `LLMClientAdapter` wraps `llm_client.acall_llm` with fallback chain (Fix 3, implemented)
-- Checkpointing: partial graph persisted after each batch (Fix 1, implemented)
-- `ERGraph._build_graph` processes chunks in batches of 50 via `asyncio.gather`
-
-#### PROPOSED (from ADR-002)
-
-| Enhancement | Description | Depends on |
-|-------------|-------------|------------|
-| **Prompts as data** | Move extraction prompts from `GraphPrompt.py` to YAML/Jinja2 templates. Graph type config selects template. | Nothing |
-| **Schema modes** | `open`/`schema_guided`/`schema_constrained` entity and relation type constraints in extraction prompts | Prompts as data |
-| **Entity canonicalization** | Post-build LLM fuzzy dedup. Reuse `onto-canon/concept_dedup.py` logic on NetworkX graph directly. | Nothing |
-| **Q-code resolution** | Post-build Wikidata entity disambiguation via `onto-canon/wikidata_entity_search.py` | Entity canonicalization |
-| **Schema validation** | Post-build rejection/flagging of out-of-schema types (`schema_constrained`) | Schema modes |
-| **Reified graph type** | New extraction template + JSON parser for event-as-node diamond pattern (n-ary relationships) | Prompts as data |
-
----
-
-### Suite 2: Retrieval (Graph Querying)
-
-Tools that read graphs to answer questions. All read-only.
-
-#### EXISTS Today (27 operators + 4 cross-modal + composition tools)
-
-**27 Operators** (uniform signature: `async op(inputs, ctx, params) -> outputs`):
-
-| Category | Operators | What they do |
-|----------|-----------|-------------|
-| **Entity** (7) | `vdb_search`, `ppr`, `onehop`, `link`, `tfidf`, `agent`, `rel_node` | Find relevant entities via vector search, PageRank, traversal, linking, TF-IDF, LLM reasoning |
-| **Relationship** (4) | `onehop`, `vdb_search`, `score_aggregator`, `agent` | Find and score relationships between entities |
-| **Chunk** (4) | `from_relationships`, `occurrence`, `aggregator`, `text_search` | Retrieve source text chunks via graph edges, co-occurrence, aggregation |
-| **Subgraph** (3) | `khop_paths`, `steiner_tree`, `agent_path` | Extract subgraphs: k-hop neighborhoods, Steiner trees, LLM-guided paths |
-| **Community** (2) | `from_entities`, `from_level` | Community detection from entity sets or hierarchy levels |
-| **Meta** (7) | `extract_entities`, `reason_step`, `rerank`, `generate_answer`, `pcst_optimize`, `decompose_question`, `synthesize_answers` | Query preprocessing, reasoning, reranking, answer generation, AoT decomposition |
-
-**4 Cross-Modal Tools**:
-
-| Tool | What it does |
-|------|-------------|
-| `convert_modality` | Convert data between graph, table, and vector representations |
-| `validate_conversion` | Measure round-trip preservation quality |
-| `select_analysis_mode` | LLM recommends best modality for a research question |
-| `list_modality_conversions` | Discover all 15 conversion paths |
-
-**Composition & Discovery Tools**:
-
-| Tool | What it does |
-|------|-------------|
-| `list_operators` | Full operator catalog with I/O types |
-| `get_compatible_successors` | Given an operator, list valid next operators |
-| `get_config` / `set_agentic_model` | Runtime configuration |
-| `list_available_resources` | What graphs and VDBs exist on disk |
-
-#### PROPOSED
-
-| Enhancement | Description | Complexity |
-|-------------|-------------|------------|
-| **Cypher-like pattern matching** | Express ad-hoc graph patterns: `MATCH (p:Person)-[:EMPLOYED_BY]->(o:Org) RETURN p, o`. Compiles to NetworkX traversal under the hood. Not full Neo4j Cypher — a subset covering node type filters, edge type filters, variable-length paths, and property constraints. | Medium — needs parser + NetworkX query compiler. Consider using `networkx-query` or writing a minimal pattern matcher. |
-| **SPARQL endpoint** | RDF export + SPARQL query. | Low priority — Cypher-like covers most needs. Defer unless academic publication requires it. |
-| **Graph statistics tool** | Node/edge counts, degree distribution, connected components, diameter, density — basic NetworkX analytics exposed as MCP tool. Currently requires raw Python. | Low — mostly wrapping `nx.degree_histogram()`, `nx.number_connected_components()`, etc. |
-
----
-
-### Suite 3: Analysis & Mutation (Graph Maintenance)
-
-Tools that modify existing graphs: add/update/delete nodes and edges, revise beliefs, maintain quality.
-
-#### EXISTS Today
-
-**In DIGIMON storage layer (not exposed as MCP tools):**
-
-| Method | Location | What it does |
-|--------|----------|-------------|
-| `upsert_node(id, data)` | `NetworkXStorage` | Add or update a node |
-| `upsert_edge(src, tgt, data)` | `NetworkXStorage` | Add or update an edge |
-| `_merge_nodes_then_upsert()` | `BaseGraph` | Merge multiple observations of same entity |
-| `_merge_edges_then_upsert()` | `BaseGraph` | Merge multiple observations of same edge |
-| `augment_graph_by_similarity_search()` | `BaseGraph` | Add similarity edges from VDB |
-| `cluster_data_to_subgraphs()` | `BaseGraph` | Write community assignments to nodes |
-| `clear()` | `NetworkXStorage` | Wipe entire graph |
-| `persist()` | `NetworkXStorage` | Write graph to GraphML file |
-
-**In onto-canon (operates on SQLite beliefs, not NetworkX):**
-
-| Tool | What it does |
-|------|-------------|
-| `canon_update_belief` | Bayesian logit-space belief update with likelihood ratios |
-| `canon_find_tensions` | Detect contradictory beliefs (opposing predicates, conflicting values) |
-| `canon_resolve_tension` | Resolve contradiction: QUALIFY, WEAKEN, RETRACT, or SUPERSEDE |
-| `canon_merge_concepts` | Merge duplicate concepts (redirect FKs + delete) |
-| `canon_prune_orphans` | Find/remove concepts with zero non-system beliefs |
-| `canon_import_digimon_graph` | Import DIGIMON graph dict → onto-canon concepts+beliefs |
-| `canon_export_digimon_graph` | Export onto-canon beliefs → DIGIMON graph dict |
-| `canon_run_governance` | Discover, validate, promote predicates to ontology |
-
-**In `graph_analyze` operator (read-only analysis, exposed as MCP):**
-
-| Tool | What it does |
-|------|-------------|
-| `graph_analyze` | Centrality, community stats, path analysis on existing graph |
-| `graph_visualize` | Generate graph visualization |
-
-#### DOES NOT EXIST (gaps)
-
-| Gap | Impact |
-|-----|--------|
-| **No `delete_node` / `delete_edge`** | Can't remove incorrect extractions without rebuilding |
-| **No selective update MCP tool** | `upsert_node`/`upsert_edge` exist in storage but aren't exposed as tools |
-| **No belief revision on NetworkX** | Onto-canon's epistemic engine operates on SQLite; no equivalent for NetworkX graphs |
-| **No edge retraction/weakening** | An incorrect extraction stays in the graph forever |
-| **No provenance-aware deletion** | Can't say "remove all edges from chunk X" (e.g., if source was retracted) |
-| **No graph diff / versioning** | Can't compare graph states before/after mutation |
-| **No undo / rollback** | Mutations are permanent; no transaction log |
-
-#### PROPOSED
-
-**Tier 1: Basic Mutation Tools** (expose existing storage methods as MCP tools)
-
-| Tool | Description | Implementation |
-|------|-------------|----------------|
-| `graph_upsert_node` | Add or update a node with attributes | Thin wrapper around `NetworkXStorage.upsert_node` + `persist` |
-| `graph_upsert_edge` | Add or update an edge with attributes | Thin wrapper around `NetworkXStorage.upsert_edge` + `persist` |
-| `graph_delete_node` | Remove a node and all its edges | Add `delete_node` to `NetworkXStorage` using `nx.Graph.remove_node`, expose as tool |
-| `graph_delete_edge` | Remove a specific edge | Add `delete_edge` to `NetworkXStorage` using `nx.Graph.remove_edge`, expose as tool |
-| `graph_delete_by_source` | Remove all nodes/edges from a specific source chunk | Filter by `source_id` attribute, bulk delete |
-
-**Tier 2: Belief Revision on NetworkX**
-
-Two architectural options:
-
-**Option A: Round-trip through onto-canon** (reuse existing epistemic engine)
-```
-DIGIMON graph → canon_import_digimon_graph → [belief operations in SQLite] → canon_export_digimon_graph → DIGIMON graph
-```
-- Pro: Reuses all existing onto-canon tools (update_belief, find_tensions, resolve_tension, merge_concepts)
-- Con: Lossy round-trip (see `DIGIMON_ATTRIBUTE_MAPPING.md` — keywords, clusters, multi-source_ids lost)
-- Con: Performance cost of serialization + SQLite I/O + deserialization
-- Best for: Periodic deep analysis, not real-time graph maintenance
-
-**Option B: Lightweight edge-level epistemic state on NetworkX** (new)
-```python
-# Add epistemic attributes to edges during build or post-build
-edge_data = {
-    "relation_name": "employed_by",
-    "weight": 0.85,
-    "status": "active",         # active | weakened | retracted
-    "probability": 0.85,        # [0.005, 0.995]
-    "source_ids": ["chunk_42"],
-    "extraction_count": 3,      # how many chunks produced this edge
-}
-```
-- New MCP tools: `graph_weaken_edge`, `graph_retract_edge`, `graph_find_tensions`
-- Reuse `belief_ops.py` math (logit updates, status transitions) but apply to NetworkX edge attributes
-- Pro: Fast, no serialization overhead, graph stays in memory
-- Con: Simpler model than onto-canon (no meta-beliefs, no supersession chains, no provenance DAG)
-- Best for: Real-time graph maintenance during or after retrieval
-
-**Recommendation**: Both. Option A for deep epistemic analysis (periodic). Option B for lightweight graph hygiene (continuous). They serve different use cases.
-
-**Tier 3: Graph Versioning**
-
-| Tool | Description |
-|------|-------------|
-| `graph_snapshot` | Save named snapshot (copy GraphML file with timestamp) |
-| `graph_diff` | Compare two snapshots: added/removed/modified nodes and edges |
-| `graph_restore` | Restore graph from a named snapshot |
-
-This enables safe experimentation: snapshot before mutation, diff to verify, restore if wrong.
-
----
-
-## Integration Architecture
-
-### How the Three Suites Connect
-
-```
-                    ┌─────────────────────────────────────┐
-                    │         Agent Brain (Client)         │
-                    │   Claude Code / Codex / OpenClaw     │
-                    └──────────┬──────────┬──────────┬─────┘
-                               │          │          │
-                    ┌──────────▼──┐ ┌─────▼─────┐ ┌─▼──────────┐
-                    │  Suite 1:   │ │  Suite 2:  │ │  Suite 3:   │
-                    │  Creation   │ │  Retrieval │ │  Mutation   │
-                    ├─────────────┤ ├────────────┤ ├─────────────┤
-                    │corpus_prepare│ │27 operators│ │upsert/delete│
-                    │graph_build_* │ │composition │ │belief ops   │
-                    │entity_vdb_*  │ │cross-modal │ │governance   │
-                    │[post-build]  │ │[cypher]    │ │[versioning] │
-                    └──────┬──────┘ └─────┬──────┘ └──────┬──────┘
-                           │              │               │
-                    ┌──────▼──────────────▼───────────────▼──────┐
-                    │              NetworkX Graph                 │
-                    │         (GraphML persistence)              │
-                    └──────────────────┬─────────────────────────┘
-                                       │
-                              ┌────────▼────────┐
-                              │   Onto-Canon    │
-                              │   (SQLite DB)   │
-                              │                 │
-                              │ Deep epistemic  │
-                              │ analysis when   │
-                              │ needed          │
-                              └─────────────────┘
-```
-
-### DIGIMON ↔ Onto-Canon Boundary
-
-| Concern | Lives in DIGIMON | Lives in Onto-Canon |
-|---------|-----------------|-------------------|
-| Graph storage | NetworkX + GraphML | SQLite (concepts, beliefs) |
-| Entity dedup (lightweight) | `clean_str()` during build | — |
-| Entity dedup (deep) | Post-build step calling onto-canon logic | `concept_dedup.py` (LLM fuzzy) |
-| Belief state (lightweight) | Edge attributes: status, probability | — |
-| Belief state (deep) | — | Full epistemic engine: logit math, tensions, resolution, meta-beliefs |
-| Provenance | `source_id` attribute on nodes/edges | `evidence` table + `evidence_concepts` + `artifact_lineage` |
-| Schema constraints | Prompt-level (`open`/`schema_guided`/`schema_constrained`) | `predicate_proposals` + governance pipeline |
-| Q-codes | Post-build enrichment attribute | Wikidata entity search + disambiguation |
-
----
-
-## Implementation Order
-
-1. **Basic mutation tools** — Expose `upsert_node`/`upsert_edge` as MCP tools. Add `delete_node`/`delete_edge` to `NetworkXStorage`. ~100 lines.
-
-2. **Graph statistics tool** — Wrap `nx.info()`, degree distribution, component analysis as MCP tool. ~50 lines.
-
-3. **Lightweight belief state** — Add `status`/`probability` attributes to edges during build. Expose `graph_weaken_edge`/`graph_retract_edge` MCP tools using `belief_ops.py` math. ~200 lines.
-
-4. **Post-build entity canonicalization** — The ADR-002 step 3. Most immediate quality improvement.
-
-5. **Graph versioning** — Snapshot/diff/restore. ~150 lines.
-
-6. **Cypher-like pattern matching** — Evaluate `networkx-query` library or write minimal pattern compiler. ~300 lines.
-
-7. **Deep epistemic round-trip** — Optimize `canon_import_digimon_graph`/`canon_export_digimon_graph` to reduce round-trip data loss.
-
----
-
-## Consequences
-
-**Positive:**
-- Complete lifecycle: build → query → maintain → revise
-- Mutation tools enable iterative graph refinement without full rebuild
-- Lightweight belief state enables real-time quality tracking
-- Versioning enables safe experimentation
-- Cypher-like queries enable ad-hoc pattern matching beyond fixed operators
-
-**Negative:**
-- Two belief systems (NetworkX edge attributes vs onto-canon SQLite) creates consistency risk
-- Mutation tools without versioning are dangerous (no undo)
-- Cypher compiler adds parsing complexity
-
-**Risks:**
-- Lightweight belief state on NetworkX may diverge from onto-canon's epistemic model over time
-- Delete operations on graphs may invalidate VDB indices (need rebuild trigger)
-- Pattern matching performance on large graphs (>50K nodes) may be slow without indexing
-
----
-
-## References
-
-- ADR-001: Agent Orchestration Architecture (orchestration modes)
-- ADR-002: Universal Graph Schema and Configurable Extraction (creation enhancements)
-- `onto-canon/docs/core/UNIVERSAL_KG_VISION.md` (superset attribute schema)
-- `onto-canon/docs/core/DIGIMON_ATTRIBUTE_MAPPING.md` (round-trip mapping)
-- `project-meta/vision/UNIFIED_PLAN.md` (155 FRs, prioritized work items)
```

Full diff of `docs/adr/004-graph-build-rearchitecture.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/004-graph-build-rearchitecture.md b/docs/adr/004-graph-build-rearchitecture.md
index 9bff6ab4..0cb421b9 100644
--- a/docs/adr/004-graph-build-rearchitecture.md
+++ b/docs/adr/004-graph-build-rearchitecture.md
@@ -1,3 +1,7 @@
+---
+description: "Decision to rebuild graph construction around one canonical entity-graph family, with KG, TKG and RKG as profiles and a persisted build manifest as the source of truth."
+---
+
 # ADR-004: Rebuild DIGIMON Around a Canonical Entity-Graph Architecture
 
 **Status**: Accepted
```

Full diff of `docs/adr/005-typed-extraction-validation.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/005-typed-extraction-validation.md b/docs/adr/005-typed-extraction-validation.md
index c02b469e..6cd7db8b 100644
--- a/docs/adr/005-typed-extraction-validation.md
+++ b/docs/adr/005-typed-extraction-validation.md
@@ -1,3 +1,7 @@
+---
+description: "Decision that entity and relationship extraction records need explicit types and strict validation before graph persistence, with malformed records failing loudly."
+---
+
 # ADR-005: Add Typed Validation to Entity-Graph Extraction Records
 
 **Status**: Accepted
```

Full diff of `docs/adr/006-open-tkg-grounded-entity-policy.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/006-open-tkg-grounded-entity-policy.md b/docs/adr/006-open-tkg-grounded-entity-policy.md
index 682696ca..de916baf 100644
--- a/docs/adr/006-open-tkg-grounded-entity-policy.md
+++ b/docs/adr/006-open-tkg-grounded-entity-policy.md
@@ -1,3 +1,7 @@
+---
+description: "Decision record that the open-graph entity policy is proven on frozen prompt-eval cases before any deterministic validator, and that benchmark-specific noun stoplists are excluded."
+---
+
 # ADR-006: Decide Open-TKG Grounded Entity Policy with Frozen Prompt-Eval Cases
 
 **Status**: Accepted
```

Full diff of `docs/adr/007-entity-relationship-closure.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/007-entity-relationship-closure.md b/docs/adr/007-entity-relationship-closure.md
index 9be0cfa1..6f86d24b 100644
--- a/docs/adr/007-entity-relationship-closure.md
+++ b/docs/adr/007-entity-relationship-closure.md
@@ -1,3 +1,7 @@
+---
+description: "Decision that every relationship endpoint must have a matching entity record in the same extraction output, and that unmatched relationships are rejected before graph persistence."
+---
+
 # ADR-007: Require Entity-Relationship Closure in Extraction Output
 
 **Status**: Accepted
```

Full diff of `docs/adr/008-pure-lane-build-comparisons.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/008-pure-lane-build-comparisons.md b/docs/adr/008-pure-lane-build-comparisons.md
deleted file mode 100644
index 6644353e..00000000
--- a/docs/adr/008-pure-lane-build-comparisons.md
+++ /dev/null
@@ -1,61 +0,0 @@
-# ADR-008: Require Pure-Lane Extraction for Decision-Grade Build Comparisons
-
-**Status**: Accepted
-**Date**: 2026-03-21
-
-## Context
-
-Plan #5 introduced closure-aware live smoke builds to compare extraction-policy
-variants on the same 10-chunk MuSiQue slice. The first pair of live artifacts
-looked useful, but they were methodologically confounded:
-
-- `MuSiQue_TKG_smoke_closure` fell back from Gemini to DeepSeek mid-build
-- `MuSiQue_TKG_smoke_closure_grounded` also fell back after a provider policy
-  block
-- the manifest did not yet preserve a runtime snapshot that could prove which
-  model lane actually produced the artifact
-
-That meant DIGIMON could not tell whether the grounded/non-grounded difference
-came from prompt policy, model/provider mixing, or both. This is unacceptable
-for a system that is supposed to reproduce and compare GraphRAG methods
-truthfully.
-
-## Decision
-
-Treat no-fallback extraction as the required path for any decision-grade live
-graph-build comparison.
-
-This means:
-
-1. Evaluation-oriented graph builds must support a dedicated pure-lane LLM path
-   instead of silently sharing the server's reliability/fallback policy.
-2. The graph-build manifest must record the build runtime lane, including the
-   primary model and any fallback models.
-3. Live artifact comparisons that are meant to justify prompt/build decisions
-   must run with `lane_policy=pure`.
-4. Mixed-lane builds remain allowed for exploratory debugging, but they must be
-   called out explicitly as non-final evidence.
-
-## Consequences
-
-### Positive
-
-- Prompt/build comparisons can now isolate prompt policy changes from
-  provider-fallback effects.
-- Every artifact can declare whether it is decision-grade or exploratory based
-  on manifest truth rather than memory.
-- DIGIMON's methodology becomes closer to a controlled GraphRAG lab instead of
-  an ad hoc collection of live runs.
-
-### Negative
-
-- Pure-lane builds can fail more often when the chosen provider is unstable or
-  rate-limited.
-- Some exploratory runs that previously succeeded through fallbacks will now
-  fail loudly when used in decision mode.
-
-### Constraints
-
-- Do not silently downgrade a pure-lane build into a fallback-enabled run.
-- Do not treat mixed-lane artifacts as decision-grade even if they look better.
-- Keep build-lane truth in the persisted manifest, not only in console logs.
```

Full diff of `docs/adr/009-two-pass-extraction-for-completeness.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/009-two-pass-extraction-for-completeness.md b/docs/adr/009-two-pass-extraction-for-completeness.md
index 2c9d8abf..d22bc53c 100644
--- a/docs/adr/009-two-pass-extraction-for-completeness.md
+++ b/docs/adr/009-two-pass-extraction-for-completeness.md
@@ -1,3 +1,7 @@
+---
+description: "Decision to prefer two-pass extraction (entity inventory first, then relationships bounded by it) when one-pass prompting cannot reliably produce complete entities."
+---
+
 # ADR-009: Prefer Two-Pass Extraction if One-Pass Completeness Remains Unstable
 
 **Status**: Accepted
```

Full diff of `docs/adr/010-tool-applicability-architecture.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/010-tool-applicability-architecture.md b/docs/adr/010-tool-applicability-architecture.md
index 0efd5a81..e1213ef9 100644
--- a/docs/adr/010-tool-applicability-architecture.md
+++ b/docs/adr/010-tool-applicability-architecture.md
@@ -1,3 +1,7 @@
+---
+description: "Decision on how DIGIMON decides whether a tool is available, degraded or unavailable, separating build artifacts, loaded runtime resources and each tool's hard and soft requirements."
+---
+
 # ADR-010: Separate Build Capabilities, Runtime Resources, and Operator Requirements for Tool Applicability
 
 **Status**: Accepted
```

Full diff of `docs/adr/011-extraction-iteration-supervisor.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/011-extraction-iteration-supervisor.md b/docs/adr/011-extraction-iteration-supervisor.md
deleted file mode 100644
index 9aa8daf5..00000000
--- a/docs/adr/011-extraction-iteration-supervisor.md
+++ /dev/null
@@ -1,103 +0,0 @@
-# ADR-011: Port the Autoloop Supervisor Skeleton into the Active Repo and Reframe It Around Extraction-Family Gates
-
-**Status**: Accepted
-**Date**: 2026-03-22
-
-## Context
-
-DIGIMON needs a real external supervisor if it is going to keep iterating for
-long stretches without relying on an interactive chat session to "remember" not
-to stop.
-
-An earlier repo, `Digimon_for_KG_application__autoloop`, already solved several
-operational problems:
-
-- durable loop state
-- JSONL event ledger
-- signal-based stop handling
-- clean-worktree enforcement
-- verified commit-or-revert cycle
-
-But that old loop is optimized for a different DIGIMON stage. Its unit of work
-is a failing MuSiQue benchmark question, and its gates are targeted benchmark
-reruns plus full-batch benchmark reruns.
-
-Current DIGIMON is on a different critical path:
-
-- extraction-quality iteration is pinned to `gemini/gemini-2.5-flash`
-- changes must be judged by failure family, not one-off questions
-- `prompt_eval` plus protected sentinels are the required first gate
-- small smoke rebuilds are the next gate, before benchmark reruns
-
-Reusing the old autoloop unchanged would optimize the wrong surface. Rewriting
-all of its durable mechanics from scratch would duplicate already-proven loop
-infrastructure.
-
-## Decision
-
-Port the old autoloop **supervisor skeleton** into the active DIGIMON repo, but
-rewrite the **control objective and validation gates** around the current
-extraction plans.
-
-### Reuse
-
-Keep these patterns from the old autoloop:
-
-- typed YAML config
-- durable session state
-- event ledger
-- signal stop handling
-- clean-worktree enforcement
-- revert on failed validation
-- commit only after verified improvement
-
-### Replace
-
-Do not reuse these behaviors unchanged:
-
-- failing-question selection
-- question-scoped benchmark prompts
-- targeted question reruns as the first proof
-- full-batch benchmark reruns as the only regression gate
-
-Replace them with:
-
-- failure-family selection
-- family-scoped prompt-eval validation
-- protected sentinels
-- optional smoke-build validation after prompt-eval success
-
-## First Slice
-
-The first implementation slice is intentionally narrow:
-
-1. support one failure family at a time
-2. run family-filtered `prompt_eval`
-3. invoke a coding agent against that family context
-4. rerun the same family gate
-5. revert on no improvement, commit on verified improvement
-
-Smoke-build and later benchmark gates are deferred to follow-up slices.
-
-## Consequences
-
-### Positive
-
-- DIGIMON gets an actual long-running external supervisor in the active repo.
-- The current extraction-quality path becomes automatable without waiting for a
-  later benchmark-only phase.
-- Previously proven operational mechanics are reused instead of re-invented.
-
-### Negative
-
-- The first supervisor slice will not yet be a complete 24/7 end-state.
-- The current extraction harness needs a small extension so the supervisor can
-  target one failure family cleanly.
-
-### Constraints
-
-- Keep decision-grade extraction validation on `gemini/gemini-2.5-flash`.
-- Do not let the first supervisor slice silently switch production extraction
-  lanes.
-- Do not promote benchmark-question reruns back to the first gate while Plan #5
-  and Plan #6 remain the critical path.
```

Full diff of `docs/adr/012-open-schema-does-not-inject-default-type-palette.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/012-open-schema-does-not-inject-default-type-palette.md b/docs/adr/012-open-schema-does-not-inject-default-type-palette.md
index 3dc3185b..d84fe4a7 100644
--- a/docs/adr/012-open-schema-does-not-inject-default-type-palette.md
+++ b/docs/adr/012-open-schema-does-not-inject-default-type-palette.md
@@ -1,3 +1,7 @@
+---
+description: "Decision record that DIGIMON's open schema mode must not inject a hidden default entity-type palette, so open extraction is not silently constrained to a fallback set of classes."
+---
+
 # ADR-012: Open Schema Mode Does Not Inject a Hidden Default Type Palette
 
 **Status**: Accepted
```

Full diff of `docs/adr/013-answer-critical-fact-representation.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/013-answer-critical-fact-representation.md b/docs/adr/013-answer-critical-fact-representation.md
index 43817d48..74134974 100644
--- a/docs/adr/013-answer-critical-fact-representation.md
+++ b/docs/adr/013-answer-critical-fact-representation.md
@@ -1,3 +1,7 @@
+---
+description: "Decision rule for whether a fact in DIGIMON should become a node, an edge, an attribute, or chunk-only evidence, based on which retrieval operations need to reach it."
+---
+
 # ADR-013: Represent Answer-Critical Facts by Operator Utility, Not Topic
 
 **Status**: Accepted
```

Full diff of `docs/adr/014-tool-consolidation-surface.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/014-tool-consolidation-surface.md b/docs/adr/014-tool-consolidation-surface.md
index 575fa191..049ac27a 100644
--- a/docs/adr/014-tool-consolidation-surface.md
+++ b/docs/adr/014-tool-consolidation-surface.md
@@ -1,3 +1,7 @@
+---
+description: "Decision record for the consolidated, method-dispatched tool surface that benchmark agents use by default, and for the operators deliberately left out of it."
+---
+
 # ADR-014: Consolidated Tool Surface for Benchmark Agents
 
 **Status**: Accepted
```

Full diff of `docs/adr/015-strategic-risks-thesis-test.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/015-strategic-risks-thesis-test.md b/docs/adr/015-strategic-risks-thesis-test.md
deleted file mode 100644
index 072324ed..00000000
--- a/docs/adr/015-strategic-risks-thesis-test.md
+++ /dev/null
@@ -1,26 +0,0 @@
-# ADR-015: Strategic Risks for Thesis Test — Relocated
-
-**Status**: Superseded
-**Date**: 2026-03-23
-
-## Context
-
-Originally recorded strategic risks and open questions as an ADR. Per Pattern 29 (Uncertainty Tracking), concerns and risks belong in plan files as tracked uncertainties, not as ADRs. ADRs are for architectural *decisions*.
-
-## Decision
-
-Relocated all strategic risks and open questions to `docs/plans/17_retest_thesis.md` under the "Open Questions" section, using the Pattern 29 format (status lifecycle, context, resolution/mitigation).
-
-Off-the-shelf alternatives assessment retained here as an architectural reference:
-
-| Area | DIGIMON | Alternative | Assessment |
-|------|---------|-------------|------------|
-| Graph construction | Custom extraction pipeline | Microsoft GraphRAG, HippoRAG OSS | Composable operator model is the differentiator. Extraction backend swappable but operator routing is custom by design. |
-| VDB indexing | FAISS directly | ChromaDB, Qdrant | FAISS fine for current scale. |
-| Benchmark eval | Custom EM/F1/LLM-judge | RAGAS, DeepEval | Consider for publishable results. |
-| Question decomposition | Single-shot operator | IRCoT, StepChain | Consolidated prompt enables iterative retry. Dedicated loop can be added later. |
-| PPR | igraph via BaseGraph | HippoRAG's PPR | Same algorithm. No need to switch. |
-
-## Consequences
-
-Uncertainties are now tracked where they'll be seen during execution (in the plan), not in a separate ADR that agents might miss.
```

Full diff of `docs/adr/016-declarative-decision-tracing-and-agent-runtime-declaration.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/016-declarative-decision-tracing-and-agent-runtime-declaration.md b/docs/adr/016-declarative-decision-tracing-and-agent-runtime-declaration.md
index a0bf7a8e..19802705 100644
--- a/docs/adr/016-declarative-decision-tracing-and-agent-runtime-declaration.md
+++ b/docs/adr/016-declarative-decision-tracing-and-agent-runtime-declaration.md
@@ -1,3 +1,7 @@
+---
+description: "Decision for diagnosable agent runtimes: shared decision tracing, project-declared decision points and honestly declared runtime classes; read it to see how agent failures should be traced."
+---
+
 # ADR-016: Declarative Decision Tracing and Capability-Declared Agent Runtimes
 
 Date: 2026-04-04
@@ -8,9 +12,9 @@ Proposed
 
 ## Informed By
 
-1. [Plan #29: Declarative Decision Tracing And Modular Agent Runtime](../plans/29_declarative_decision_tracing_and_modular_agent_runtime.md)
-2. [Decision Trace And Modular Agent Runtime Research](../reports/2026-04-04_decision_trace_and_modular_agent_runtime_research.md)
-3. [Recursive Reasoning Trace System — Design Document](../RECURSIVE_REASONING_TRACE.md)
+1. [Plan #29: Declarative Decision Tracing And Modular Agent Runtime](../archive/PLANS.md)
+2. [Decision Trace And Modular Agent Runtime Research](../archive/REPORTS.md)
+3. [Recursive Reasoning Trace System — Design Document](../archive/REPORTS.md)
 4. `/home/brian/projects/llm_client/docs/adr/0010-cross-project-runtime-substrate.md`
 5. `/home/brian/projects/llm_client/docs/adr/0007-observability-contract-boundary.md`
 6. `/home/brian/projects/onto-canon6/docs/adr/0013-start-stable-identity-with-promoted-entity-identities-alias-membership-and-explicit-external-reference-state.md`
```

Full diff of `docs/adr/017-nary-graph-representation-and-onto-canon-import.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/017-nary-graph-representation-and-onto-canon-import.md b/docs/adr/017-nary-graph-representation-and-onto-canon-import.md
index 87e01256..7bb09709 100644
--- a/docs/adr/017-nary-graph-representation-and-onto-canon-import.md
+++ b/docs/adr/017-nary-graph-representation-and-onto-canon-import.md
@@ -1,3 +1,7 @@
+---
+description: "Decision record for storing onto-canon n-ary assertions as assertion nodes with role edges rather than collapsed binary edges, and for reading the import from SQLite."
+---
+
 # ADR-017: N-ary Graph Representation and onto-canon6 Import
 
 **Status**: Accepted
```

Full diff of `docs/adr/018-federated-canonical-action-manifest.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/018-federated-canonical-action-manifest.md b/docs/adr/018-federated-canonical-action-manifest.md
index b6051b91..cfb13568 100644
--- a/docs/adr/018-federated-canonical-action-manifest.md
+++ b/docs/adr/018-federated-canonical-action-manifest.md
@@ -1,3 +1,7 @@
+---
+description: "Decision record for one declared action manifest compiled into every consumer's view, so the list of DIGIMON actions cannot drift between planner, MCP, dispatch and benchmark copies."
+---
+
 # ADR-018: Federated Canonical Action Manifest with Declarative Consumer Projections
 
 Status: Accepted graph-pack projection of project-meta Plan #215; generic core
@@ -6,14 +10,14 @@ Date: 2026-07-12
 
 ## Informed By
 
-1. [Plan #111](../plans/111_canonical-typed-operator-composition.md)
-2. [Plan #111 consumer-truth inventory](../plans/111_consumer_truth_inventory.md)
-3. [Plan #111 adversarial audit](../../investigations/2026-07-12-plan111-adversarial-plan-audit.md)
+1. [Plan #111](../archive/PLANS.md)
+2. [Plan #111 consumer-truth inventory](../archive/PLANS.md)
+3. [Plan #111 adversarial audit](../archive/INVESTIGATIONS.md)
 4. [ADR-010: Tool Applicability Architecture](010-tool-applicability-architecture.md)
 5. [ADR-014: Consolidated Tool Surface](014-tool-consolidation-surface.md)
 6. MCP tool contracts, which give each exposed tool an independent input and output schema
 7. CWL workflow contracts, which make source/sink compatibility and multi-source merge behavior explicit
-8. [2026-07-13 operator-composition build-versus-adopt review](../reports/2026-07-13_operator-composition-build-vs-adopt.md)
+8. [2026-07-13 operator-composition build-versus-adopt review](../archive/REPORTS.md)
 
 ## Context
```

Full diff of `docs/adr/019-composition-state-policy-and-transition-separation.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/019-composition-state-policy-and-transition-separation.md b/docs/adr/019-composition-state-policy-and-transition-separation.md
index 3e822b88..3163c4ac 100644
--- a/docs/adr/019-composition-state-policy-and-transition-separation.md
+++ b/docs/adr/019-composition-state-policy-and-transition-separation.md
@@ -1,3 +1,7 @@
+---
+description: "Decision separating composition state, per-turn eligibility policy and typed query transitions in DIGIMON's query loop, so applicability, policy and execution history stay distinct."
+---
+
 # ADR-019: Separate Composition State, Eligibility Policy, and Typed Query Transitions
 
 Status: Accepted graph-consumer projection of project-meta Plan #215; generic
@@ -6,12 +10,12 @@ Date: 2026-07-12
 
 ## Informed By
 
-1. [Plan #111](../plans/111_canonical-typed-operator-composition.md)
-2. [Plan #111 contract-boundary review](../../investigations/2026-07-12-plan111-contract-boundary-review.md)
-3. [Plan #111 adversarial audit](../../investigations/2026-07-12-plan111-adversarial-plan-audit.md)
+1. [Plan #111](../archive/PLANS.md)
+2. [Plan #111 contract-boundary review](../archive/INVESTIGATIONS.md)
+3. [Plan #111 adversarial audit](../archive/INVESTIGATIONS.md)
 4. [ADR-016: Declarative Decision Tracing](016-declarative-decision-tracing-and-agent-runtime-declaration.md)
 5. The current `digimon.query` planner, stop, synthesis, and bootstrap control flow
-6. [2026-07-13 general operator-composition build-versus-adopt review](../reports/2026-07-13_operator-composition-build-vs-adopt.md)
+6. [2026-07-13 general operator-composition build-versus-adopt review](../archive/REPORTS.md)
 
 ## Context
```

Full diff of `docs/adr/020-graph-projection-surface-contract.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/020-graph-projection-surface-contract.md b/docs/adr/020-graph-projection-surface-contract.md
index e2c13417..992d9ded 100644
--- a/docs/adr/020-graph-projection-surface-contract.md
+++ b/docs/adr/020-graph-projection-surface-contract.md
@@ -1,3 +1,7 @@
+---
+description: "Decides how one graph stores semantic, evidence and weak-association edges as separate named projections, so each operator reads only the structure it is entitled to."
+---
+
 # ADR-020: Graph Projection-Surface Contract
 
 **Status:** Accepted
```

Full diff of `docs/adr/021-analytic-operator-role.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/021-analytic-operator-role.md b/docs/adr/021-analytic-operator-role.md
index 6e866eaa..c3df4f70 100644
--- a/docs/adr/021-analytic-operator-role.md
+++ b/docs/adr/021-analytic-operator-role.md
@@ -1,3 +1,7 @@
+---
+description: "Decision that analytic operators form their own role separate from retrieval, producing derived measurements that must never be read as source evidence or influence claims."
+---
+
 # ADR 021: Analytic Operators Are Distinct from Retrieval
 
 **Status:** Accepted
```

Full diff of `docs/adr/022-representation-ir-native-execution.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/022-representation-ir-native-execution.md b/docs/adr/022-representation-ir-native-execution.md
index 5fc0401c..8035275f 100644
--- a/docs/adr/022-representation-ir-native-execution.md
+++ b/docs/adr/022-representation-ir-native-execution.md
@@ -1,3 +1,7 @@
+---
+description: "Decision record that DIGIMON uses typed transformation contracts and native structures, not one universal interchange representation, to carry generality across data families."
+---
+
 # ADR 022: Canonical Semantics, Transformation Contracts, and Native Execution Representations
 
 **Status:** Proposed
```

Full diff of `docs/adr/023-agent-owned-situational-reasoning-and-direct-execution-boundary.md`, plan commits only:

```diff
commit 5184a7c1 [Plan #221] Finish documentation consolidation (#445)

diff --git a/docs/adr/023-agent-owned-situational-reasoning-and-direct-execution-boundary.md b/docs/adr/023-agent-owned-situational-reasoning-and-direct-execution-boundary.md
index b7555c55..d9651b48 100644
--- a/docs/adr/023-agent-owned-situational-reasoning-and-direct-execution-boundary.md
+++ b/docs/adr/023-agent-owned-situational-reasoning-and-direct-execution-boundary.md
@@ -1,3 +1,7 @@
+---
+description: "Decision record assigning generic next-action reasoning to the participant agent, while DIGIMON owns typed retrieval, analysis, evidence custody and execution receipts."
+---
+
 # ADR-023: Agent-Owned Situational Reasoning and Direct DIGIMON Execution Boundary
 
 **Status:** Accepted
```

Classification: **none** (no line). Adopted at 01:00Z, before the repository declared durable documents (04:52Z); listed as a leak under the frozen rule. Its commit `5184a7c1` touches `NORTH_STAR.md` and 23 ADRs: frontmatter `description:` lines added (mechanical, e.g. `+description: "States DIGIMON's durable purpose..."`) and some ADRs deleted or consolidated (`deleted file mode` on ADR-002). That is documentation consolidation, not an update to what a decision says.

### 10. .agents `rtk-shell-output`

- Plan file: `docs/plans/rtk-shell-output.md` (on `origin/main`); adoption receipt `completed_at` 2026-10-11T02:40:40Z; last plan-tagged commit 2026-10-10T22:58:57-04:00.
- Durable-documents line: **absent** (no `Durable documents:` line in the plan)
- Commit range: `bce214a82a10..13096a1eafc0` (parent of the first to the last of the 1 commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).
- Plan commits: 13096a1ea

`git diff --stat` over the range:

```text
 contracts/client-config/README.md                   |  41 +++
 contracts/client-config/rtk/config.toml             |  51 +++
 contracts/client-config/rtk/install.sh              |  25 ++
 contracts/client-config/rtk/rtk-claude-hook         |  41 +++
 docs/plans/rtk-shell-output.adoption-attempts.jsonl |   1 +
 docs/plans/rtk-shell-output.adoption-decision.json  |  15 +
 docs/plans/rtk-shell-output.bundle.json             | 685 ++++++++++++++++++++++++++++++++++++++++
 docs/plans/rtk-shell-output.facts.json              |  25 ++
 docs/plans/rtk-shell-output.goal.md                 |  18 ++
 docs/plans/rtk-shell-output.md                      | 152 +++++++++
 docs/plans/rtk-shell-output.path-decision.json      |  57 ++++
 docs/plans/rtk-shell-output.receipt.json            | 581 ++++++++++++++++++++++++++++++++++
 docs/plans/rtk-shell-output.verdicts.json           | 164 ++++++++++
 docs/plans/rtk-shell-output/traces.txt              |  52 +++
 tests/test_rtk_claude_hook.py                       |  73 +++++
 wiki/index.md                                       |   1 +
 16 files changed, 1982 insertions(+)
```

Declared durable paths on `origin/main` today (plans role excluded): `docs/architecture/GOAL.md`, `docs/architecture/GOAL.md`. Touched by this plan's commits: **none**.

Classification: **none** (no line). Adopted at 02:40Z, before the repository declared durable documents (05:32Z); listed as a leak under the frozen rule. No declared durable path touched.
