---
plan_id: aes-planning
status: shaping
selected_path: coordinated
planning_path_decision: proposals/aes-planning/planning-path-decision.json
method_conformance_receipt: proposals/aes-planning/method-conformance-receipt.json
review_page: proposals/aes-planning/review-page/aes-planning-plan.html
---

# AES planning: no real implementation work without an adopted plan

## Who it serves, the result, one example

**Actor:** Brian, and every agent (Claude Code, Codex, the Paperclip workers) doing implementation work in his repositories.

**Result:** real implementation work lands only under a plan that Company Planning adopted and AES accepted, and accepting it produces the `/goal` text that runs it. Trivial work still flows without a plan, but "trivial" is decided by checked facts about the change, not by the label an agent types.

**Example (the case that started this, 2026-10-06):** an agent commits `[Unplanned] Paperclip: add make, uv and PyYAML` (personal-vps #87: a new Dockerfile, a changed compose file and deploy script, then a live deploy). Today every hook accepts it. After this plan, the commit-message hook answers: "refused: this change adds or changes a running thing (compose, Dockerfile, deploy script); `[Unplanned]` is for emergencies and `[Trivial]` allows no running-thing files. Commit under `[Plan #N]` for an adopted plan, or record the emergency." The same agent working under the adopted hive-hardening plan commits `[Plan #N] U2: worker tools`, and the hook finds the plan's adoption receipt and accepts it. A README typo fix under `[Trivial]` still goes straight through.

## Brian's direction (authority)

- 2026-10-06: "we should enforce this ['I wrote a plan page, but I didn't plan it the way your system says to']".
- 2026-10-06: "i guess we could have aes plans be one of the routes in company planning and then we can work towards getting everything in that format ... yeah we need to lock down unplanned. there are some trivial cases where that is correct but for real implementation work we should always have a plan."
- 2026-10-06: "in general we want to be upfront planning what is optimal then using /goal ... company planning ... should generate the /goal text where it is known as part of the plans."
- 2026-10-06: "once we get aes canonical working we refactor all my projects into aes and force all work going forward into aes compliance."

Authority over the work: Brian. Owners of the touched pieces: Company Planning (`BrianMills2718/company-planning`, the method and its adoption gate), AES canonical (`aes plan accept`, the pre-commit hook), the shared commit-message hook (`project-meta/hooks/commit-msg`, installed in 22 repositories; project-meta is legacy, so its rule moves into AES and the hook reads it from there).

## What exists, and what this plan does with it

| Existing piece | Where | Disposition |
|---|---|---|
| Route from facts: `PlanningPathDecisionV1`, six routes from fourteen yes/no facts | company-planning `contracts/planning-path/`, `scripts/validate_planning_path.py` | **reuse** as the definition of trivial and of real work |
| Adoption gate: facts → compiled checklist → evidence → receipt (PR #40, 2026-10-06) | company-planning `scripts/method_conformance/` | **reuse**; add one overlay and one output |
| Situation-declared checklists policy (#2394, 2026-10-06) | project-meta policy registry | **reuse**: this plan is its first enforcement at merge for implementation commits |
| Commit tags `[Plan #N]`, `[Goal …]`, `[Trivial]`, `[Unplanned]` | `meta-process.yaml` in each repo, checked by `hooks/commit-msg` | **extend**: tags stay, the hook checks them against facts and receipts |
| `aes plan validate / accept`, governed-root pre-commit hook | AES canonical | **extend**: accept requires an adopted receipt |
| Plan gate draft: review pages and 2–4 working-UI review points (10-04, not accepted) | AES branch `shaping/plan-gate`, `PLAN-AES-PLAN-GATE` | **reuse** as the review-points part of the AES overlay |
| `/goal` objective shape | `authoring-goals` skill, "Goal Objective" | **reuse** as the template the gate fills |
| Enforced Planning plan admission (observe mode) | vendored in AES, `meta-process.yaml` `plans.integrity` | **supersede** for repositories under AES planning |

Nothing new is built where an existing piece covers it. The parallel-implementation check: after U3, a search across the installed hooks for any second commit-tag validator, and the gate's own test that an `[Unplanned]` commit with a running-thing file is refused by exactly one hook.

## Design

1. **AES plans are a Company Planning overlay, switched on by a fact.** Brian asked for AES plans as a route. Routes in Company Planning say *how much* planning (repair, prototype, coordinated…); AES is *where the plan lands*. So it is added the way the gate already adds conditional requirements: a new activation fact `aes_governed_target` (true when the target repository has `.aes/`) switches on an `aes` overlay for every implementation route. Its items: the plan declares its target delta, including running things (files, services, containers, agent rules), so `aes plan validate` passes; it names 2–4 review points that are working UI slices (from the plan-gate draft); its `/goal` text exists. Migrating a project into AES (`aes init`) turns the overlay on for that project from then on, which is "work towards getting everything into that format".
2. **Adoption writes the `/goal` text.** When `adopt` exits 0, it writes `<plan>.goal.md` in the `authoring-goals` objective shape, filled from the plan's own fields (outcome, example, forbidden substitutes, boundaries, done-when, stop and revalidate conditions). A required item checks it exists and points at the plan rather than copying it.
3. **`aes plan accept` requires the receipt.** A proposal is accepted only when its Company Planning adoption decision is `adopted` and the receipt's hash matches the plan revision.
4. **Unplanned is locked down at commit time, by facts.**
   - `[Plan #N]` / `[Goal …]`: the hook finds the plan's adoption receipt (in the repository, or in AES canonical for cross-repository plans) and refuses if none is adopted.
   - `[Trivial]`: allowed only when the change touches at most 3 files and 60 changed lines, adds no new file under a governed root, and touches no running-thing file (compose, Dockerfile, `*.service`, `*.timer`, hook, agent rules, deploy script, CI). Measured from the staged diff, never from the message text.
   - `[Unplanned]`: emergency only. It needs a trailer `Emergency: <one line>`, is logged, and reaches Brian as an `fyi` the same day; a second one in a repository within a week opens a concern for an agent to plan the area properly.
   - Rollout: one week in observe mode (log what would be refused, refuse nothing), then enforce, repository by repository, starting with AES canonical.
5. **First real cases.** The hive-hardening plan (AES `shaping/hive-hardening`) is re-planned through this gate, then whygame5 (already AES), then DIGIMON and process tracing (where the workers are), then the rest.

## Work units

| ID | Change | Where | Done when |
|---|---|---|---|
| P1 | `aes_governed_target` fact and `aes` overlay in the bounded-design method profile | company-planning | a plan in an AES repository compiles a checklist that includes the overlay items; one outside does not |
| P2 | `adopt` writes `<plan>.goal.md` from the plan's fields | company-planning | adopting this plan writes a goal file whose objective validates against the `authoring-goals` shape |
| P3 | `aes plan accept` requires an adopted receipt matching the plan revision | AES canonical, through `aes plan` | accept refuses a proposal with no receipt and with a stale receipt; accepts with a fresh one |
| P4 | commit-message rule for the four tags, read from AES, installed in the 22 hooked repositories, observe mode first | AES canonical + hook installer | replaying the last 300 commits of AES canonical and personal-vps lists the would-refuse commits; the 2026-10-06 personal-vps #87 commit is among them; a README typo commit is not |
| P5 | hive-hardening re-planned through the gate as the first case | AES canonical | its receipt is adopted, `aes plan accept` passes, its `/goal` text exists |
| P6 | enforce mode in AES canonical, then repository by repository | each repository | a week of observe log reviewed; enforce switched on with that log as evidence |

## Coordination

| Writer | Owns | Conflict surface with this plan | Integration |
|---|---|---|---|
| Session holding claim `company-planning:plan-48-method-conformance` (adoption gate, merged as company-planning #40; claim still open) | `plugins/company-planning/contracts/method-conformance`, `scripts/method_conformance`, `tests/test_method_conformance.py` | P1 (profile overlay) and P2 (`adopt` writes goal text) edit the same files | messaged with this plan before P1; P1/P2 start only after its claim is closed or it agrees in a reply; then one pull request each in company-planning |
| Session that wrote the situation-checklists policy (project-meta #2394) | the policy entry and its enforcement matrix | P4 is that policy's enforcement at commit for implementation work | P4 records itself against that policy entry; no change to the policy text |
| Session moving company-planning's canonical source back to BrianMills2718 (#43) | install source, updater, docs | none in code; P1/P2 must land in BrianMills2718/company-planning, not the Inside-Success copy | check the remote before the first P1 push |
| This session (code-71) | the AES pieces: P3, P4's rule file, P5, P6 | `.aes/target.yaml` and the governed roots (single writer, checked by claims before P3) | integration owner for the plan as a whole; work-unit evidence per row of "Work units" |

## Success, and what would disprove it

**Success:** in AES canonical, after enforce mode, every commit in a week carries `[Plan #N]` / `[Goal …]` resolving to an adopted plan, `[Trivial]` passing the diff check, or a logged emergency; and the hive-hardening work runs from its generated `/goal` text.

**Disproof:**
- the observe week shows more than 1 in 5 would-refused commits that a reader judges genuinely trivial (the thresholds or the running-thing list are wrong); or
- agents route around it: `[Trivial]` commits split one change into many small ones (two or more consecutive `[Trivial]` commits on the same files in a day counts as a split), or emergencies exceed one per repository per week; or
- adopting a normal plan takes more than one working session of agent time on average across the first three plans (the gate costs more than it saves).

## Irreversible actions and spend

None irreversible: every piece is a commit or a config switch, and observe mode refuses nothing. Hooks change in 22 repositories; rollback is one config value per repository (`observe`/`off`) or reverting the hook commit. Spend: the gate's semantic verifier makes light model calls through the shared LLM client on Brian's OpenRouter route, under one dollar per plan; no new paid service.

## Uncertainties

| Uncertainty | Owner or evidence that resolves it |
|---|---|
| Whether 3 files / 60 lines is the right trivial size | P4 observe log over the last 300 commits, then the first enforce week |
| Whether the hook can find a cross-repository plan's receipt offline (plan in AES, commit in personal-vps) | P4: resolve from a local AES checkout path recorded in the repository's `meta-process.yaml`; fail visibly when it is missing |
| Whether the gate's semantic verifier is reachable from the worker container | P5 run on the VPS; when unavailable the receipt says `unavailable`, never `pass` |
| Whether other sessions are changing the same Company Planning files | claims check before P1/P2; the plan-48 owner is messaged with this plan |
| How a plan's own drafting commits are tagged before it is adopted (this plan's first commit had to use `[Unplanned]`) | P4 adds a `[Shaping <plan-id>]` tag allowed only for files under that plan's `proposals/<plan-id>/` folder; checked by the hook from the diff |

## Non-goals

- No new planning method, route engine, renderer or approval tool.
- No Stop hook; enforcement is at commit, merge, plan adoption and claim admission only.
- Not migrating every repository in this plan; it does AES canonical and the first cases, and makes migration mechanical for the rest.
- No change to what reaches Brian (`proposals/hive-hardening/WHAT_GOES_TO_BRIAN.md` stays the rule); emergencies use its `fyi` label.
