---
plan_id: aes-plan-scope
status: shaping
selected_path: repair
planning_path_decision: proposals/aes-plan-scope/planning-path-decision.json
method_conformance_receipt: proposals/aes-plan-scope/method-conformance-receipt.json
goal:
  outcome: in a repository adopted with aes adopt, work planned through Company Planning can edit the legacy files its plan declares, under enforce, while a legacy edit outside every plan's declared scope is still refused
  canonical_example: an adopted Company Planning plan declares in its front matter conflict_surfaces with kind repository_path, the repository, target tests/unit/test_x.py and access write; a [Plan #N] commit editing that legacy file lands under enforce and the file leaves the unplanned-legacy set; the same plan editing another legacy file is refused naming that file; a plan without an adoption decision admits nothing
  forbidden_substitutes: switching the adopted repository to observe; accepting every legacy edit under any adopted plan regardless of scope; a scope field Company Planning does not already define; a scope that can be widened without re-adopting the plan; a test that checks only the verdict count without naming the file accepted or refused
  boundaries: AES canonical src/agentic_engineering_system/commit_rule.py and adopt.py, their two test files, GETTING_STARTED.md and this plan folder; DIGIMON is replayed in a throwaway scratch copy and nothing is committed there; no private-repository file paths committed here; Company Planning is not changed
  done_when: the three tests in tests/greenfield/test_adopt.py named under Success pass through real git commits and installed hooks; the replay of DIGIMON pull request 414's three commits with Plan 216's scope declared reads 3 accepted and with the scope removed reads the one refusal; make aes, make aes-check and make check exit 0
  do_not_gate_on: Brian reading this page; DIGIMON adding its scope line or moving to enforce; the new-file orphan gap named in issue 218
  owner: claude-code:aes-218
---

# Plan scope for adopted repositories: Company Planning plans may edit the legacy files they declare

## Who it serves, the result, one example

**Actor:** every agent working in a repository adopted with `aes adopt` whose work is planned through Company Planning (DIGIMON first), and Brian, who wants those repositories switched to enforce.

**Result:** a Company Planning plan names the files it will write with the field Company Planning's work-unit records already use, `conflict_surfaces` (schema 1.1 `conflictSurface`: `kind: repository_path`, `repository`, `target`, `access`). The AES commit rule reads that list from the adopted plan's front matter. A `[Plan #N]` or `[Goal <id>]` commit may then edit a legacy file inside one of that plan's `write` or `exclusive` surfaces for this repository. Once the file has changed at `HEAD`, it leaves the unplanned-legacy set, as a file planned through `aes plan accept` does. A legacy edit outside the named plan's surfaces is refused exactly as today.

**Example.** DIGIMON's robot worker opened pull request 414 under adopted Plan 216: three commits, one of which edits an existing test file. Under enforce that commit is refused today (`aes commit replay`: 3 commits, 2 accepted, 1 refused), because a Company Planning plan declares no paths and only `aes plan accept` can clear a file from the baseline. After this plan, Plan 216 adds five `conflict_surfaces` lines, is re-adopted, and the same replay reads 3 accepted.

## Brian's direction (authority)

- 2026-10-06: "once we get aes canonical working we refactor all my projects into aes and force all work going forward into aes compliance."
- 2026-10-07: Brian asked for issue #218 to be fixed in this repository, with three tests against real cases and a replay of DIGIMON pull request 414.

## Authority and non-goals

Authority: the direction above; AES canonical is Brian's repository. The change edits only files the target already plans (`commit_rule.py`, `adopt.py`, `test_commit_rule.py`, `test_adopt.py`), so no new target artifact is needed.

Non-goals: new files under a governed root are still orphans for `aes topology check` until the target plans them (issue #218's related gap; tracked separately); `aes hooks install` with a local `core.hooksPath`; the machine-wide `repos:` override keyed by a worktree folder name; any change to Company Planning, to the shared hook runtime or to `~/.config/aes/commit_rule.yaml`; moving any repository to enforce.

## Irreversible actions and spend

This plan proposes zero irreversible actions and zero spend. Every change is code, tests and documents in AES canonical, merged by pull request; containment is `git revert` of the merge. A plan without `conflict_surfaces` behaves exactly as today. DIGIMON is only read: the replay runs in a scratch clone under `~/code/.scratch/` that is marked complete afterwards. No model call except Company Planning's own adoption verifier, no deployment, no data deletion, no outbound message.

## Design

1. **Scope vocabulary, reused.** Front matter `conflict_surfaces:` is a list of Company Planning `conflictSurface` objects. Only `kind: repository_path` with `access: write` or `exclusive` grants edits; `read`, other kinds, other repositories and malformed entries grant nothing. `repository` names this repository by origin's `owner/repo`, its `repo` part, or the main checkout's folder name. `target` is a file, a directory (everything under it) or a glob (`*`, `?` within one directory, `**` across directories); Company Planning's own records use files and directories.
2. **Bound to adoption.** The surfaces are part of the plan's bytes, and the commit rule already requires the adoption decision's `plan_sha256` to match those bytes. Widening the scope therefore needs re-adoption; an unadopted plan's surfaces are never read.
3. **Commit rule.** `commit_rule.adopted_plan` returns the adopted plan's front matter alongside the existing verdict; `judge` accepts legacy edits inside the named plan's write surfaces and still refuses the rest, naming them, with a fix line ("declare it in Plan #N's conflict_surfaces and re-adopt"). The verdict's log line gains `scope`, so every accepted legacy edit names the surface that admitted it.
4. **Leaving the baseline.** A commit-msg hook cannot change the commit it judges, and a Company Planning repository never runs `aes plan accept`. So `adopt.scope_released` computes it: a baseline file whose blob at `HEAD` differs from the baseline's and that lies in a write surface of an adopted plan in this repository is released. `adopt.unplanned_legacy` (what the commit rule checks at commit time and what `aes status` counts) leaves it out; `aes status` prints `N released by an adopted plan's conflict_surfaces`. The JSON file keeps the entry, so `topology` still knows the file and does not call it an orphan; planning it in the target prunes it as before. `aes commit replay` judges history without the release, so each replayed commit is held to the plan it names.

## Activation facts

Declared in `activation-facts.json`: `shared_mechanism` true (the commit rule is shared by every repository on the machine); `empirical_comparison_proposed` false; `llm_central` false; `irreversible_or_spend_action` false (see above).

## Prior art

Searched, each in turn: **existing ownership** in this repository (`commit_rule.py`, which owns the tag and legacy-edit verdicts, and `adopt.py`, which owns the baseline); **internal lineage** (issue #218, issue #180 and pull request #217 that added the baseline, `proposals/aes-adopt-existing/`, and Company Planning's work-unit schema `plugins/company-planning/skills/work-unit-graph/references/work-unit.schema.json` with its plan front-matter reader `scripts/method_conformance/common.py`, which ignores keys it does not use; DIGIMON Plan 216's "Conflict surface" column is prose, not a field); **external prior art** (GitHub CODEOWNERS and Gerrit path ownership rules, SonarQube's clean-as-you-code new-code scope). Each candidate found, with one disposition:

| Candidate | What it does | Disposition |
| --- | --- | --- |
| Company Planning work-unit `conflict_surfaces` (schema 1.1 `conflictSurface`) | declares, per work unit, the repository paths it reads, writes or holds exclusively | **reuse** the field name and object shape unchanged, in plan front matter |
| GitHub CODEOWNERS / Gerrit path ownership | path patterns that decide who may change which files | **reuse** the matching style (file, directory, glob); no new pattern language |
| SonarQube clean-as-you-code | the quality gate applies to code that changed | **reuse** the rule: a legacy file leaves the baseline when a plan that scopes it changes it |
| AES `commit_rule.receipt_status` adoption binding (`plan_sha256`) | a plan counts only for the bytes that were adopted | **reuse**: the scope sits inside those bytes, so it cannot widen silently |
| AES `commit_rule.judge` legacy-edit check | refuses edits to unplanned legacy files | **extend** with the named plan's write scope; everything else unchanged |
| AES `adopt.legacy_paths` / `prune_baseline` | baseline minus target-planned files; pruned at `aes plan accept` | **extend** with `scope_released`, computed rather than written, so topology keeps knowing the file |

Alternatives weighed and not taken (they are designs, not prior art): issue #218's option 2, `aes plan accept` importing a Company Planning receipt, adds a second plan record per change and still needs a target artifact per new file; option 3, "write an AES plan per change", documents the gap instead of closing it.

**Parallel-implementation check:** `git grep -n "conflict_surfaces" -- src/agentic_engineering_system` must show one reader (`commit_rule.write_scope`) and the scan in `commit_rule.adopted_write_scopes` that calls it, and `git grep -n "legacy_baseline.json\"" -- src` one loader in `adopt.py`.

## Uncertainties

These are the plan's material uncertainties; there are no others.

| Material uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Plan authors may declare whole roots (`digimon/`) as scope, which would make the legacy check meaningless for that plan. | The AES coordinator session that owns `proposals/aes-planning` | The first enforce week's commit-rule log in DIGIMON: count accepted legacy edits by the `scope` entry that admitted them; if one surface covers more than a quarter of the baseline, add a size warning. |
| Scanning every plan's front matter on each commit could slow commits in repositories with hundreds of plans. | This plan's owner | The DIGIMON replay's wall time in the evidence file; over 2 s per commit means caching the scan. |

## Success and what would disprove it

Every criterion names its run, where the full trace is kept, and what must be seen in the trace beyond the outcome.

- **SC-1 inside the scope, accepted and released.** Run: `test_plan_scope_admits_a_legacy_edit_inside_it_and_releases_the_file` in `tests/greenfield/test_adopt.py`, which clones this repository, adopts it, installs the real hooks, adds an adopted numbered plan with one write surface and one read surface, sets `mode: enforce`, and commits an edit to the legacy file. Trace: `proposals/aes-plan-scope/evidence/test-plan-scope-<sha>.txt` (pytest `-v -rA` with the `git commit` and `aes` output and the JSON log line the test prints). Seen: `git commit` exit 0 and HEAD moved; the log line with `mode: enforce`, `verdict: accept`, `scope` holding only the write surface, and the reason naming the file; after the commit the file is absent from `unplanned_legacy` and present in `legacy_paths` (set equality with everything else unchanged); `aes status` printing `1 released`; `aes topology check` exit 0 with no `orphan:` for it; a following `[Trivial]` edit to it landing.
- **SC-2 outside the scope, refused.** Run: `test_plan_scope_refuses_a_legacy_edit_outside_it`. Trace: same file. Seen: one commit editing one file inside and one outside the scope (the outside file is declared only for another repository) exits 1, HEAD does not move, the refusal names only the outside file and the fix line, and the log line has `check: legacy-edit`.
- **SC-3 unadopted or widened plan, refused.** Run: `test_unadopted_or_widened_plan_scope_admits_nothing`. Trace: same file. Seen: a plan without an adoption decision and a plan whose scope was widened after adoption both exit 1 under enforce, with `not adopted`/`receipt or adoption decision missing` and `plan changed since adoption` respectively, plus the legacy refusal for the unadopted one.
- **SC-4 DIGIMON pull request 414.** Run: `aes commit replay main..<PR 414 head> --json` in a scratch clone of DIGIMON at its main (835ed9ba), three times: as merged; with Plan 216's five `conflict_surfaces` lines added and its adoption decision rebound to the new bytes (standing in for Company Planning re-adoption); and with the test-file line removed as a control. Trace: `proposals/aes-plan-scope/evidence/digimon-replay-2026-10-07.txt`, with DIGIMON file paths replaced by roles because DIGIMON is private. Seen: per commit, the verdict, check, the scope list length and the reason naming the admitted file's role; counts 2/1, then 3/0, then 2/1 with the refusal on the same commit.
- **Gates.** Run: `make aes`, `make aes-check`, `make check` on the final branch head. Trace: `proposals/aes-plan-scope/evidence/gates-<sha>.txt`. Seen: each run's passed/failed/skipped counts and exit status, the three SC tests and `test_conflict_surface_matching_and_repository_names` by name among the passed.

**Disproved if** any of these is seen in the first adopted repository that enforces with plan scopes. Run examined: every commit from the enforce switch onward, replayed with `aes commit replay <switch-sha>..HEAD --json`. Trace: that repository's `<git-common-dir>/aes/commit-rule-<date>.jsonl` plus `git log -p` of its plans' front matter. What must be seen, beyond commits landing:

- a log line with `verdict: accept` for a commit whose `M` path is still in `unplanned_legacy` at its parent and matches none of the line's `scope` entries;
- a plan's `conflict_surfaces` changed in a commit while its adoption decision's `plan_sha256` still matches, with a later legacy edit accepted under the new surface;
- a file released by `scope_released` reported as `orphan:` by `aes topology check`.

## Verification

The four tests above (real clones, real installed hooks), the existing `test_commit_rule.py` and `test_adopt.py` still passing, the DIGIMON replay (SC-4), and the gates.
