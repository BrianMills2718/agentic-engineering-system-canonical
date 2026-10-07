---
plan_id: aes-adopt-existing
status: shaping
selected_path: repair
planning_path_decision: proposals/aes-adopt-existing/planning-path-decision.json
method_conformance_receipt: proposals/aes-adopt-existing/method-conformance-receipt.json
goal:
  outcome: an existing repository joins AES in one command without planning its old files; from then on only files a plan touches need a plan, and aes status shows how much is still legacy
  canonical_example: in a clone of a real repository, aes adopt lists every tracked file under src/ and tests/ in .aes/legacy_baseline.json with its blob hash, aes status says 100% legacy, and the init commit passes the installed hooks; editing one legacy file with no plan is logged (observe) or refused (enforce); planning that file with aes plan accept removes exactly that path from the baseline
  forbidden_substitutes: a baseline that only counts files; a test that checks the baseline length instead of its membership; planning every legacy file as an artifact in the target; turning the topology check off for adopted repositories
  boundaries: AES canonical governed roots, GETTING_STARTED.md and this plan folder only; DIGIMON is run against in a throwaway worktree and nothing is committed there unless its adopted Plan 216 scope covers it (it does not); no private-repository file paths committed here
  done_when: tests/greenfield/test_adopt.py passes against a real repository clone with the counts below; the installed hooks commit an adoption, log or refuse an unplanned legacy edit by mode, and accept the planned edit; aes status on DIGIMON's adoption reads 100% legacy; make aes, make aes-check and make check exit 0
  do_not_gate_on: Brian reading this page; DIGIMON committing its baseline; other repositories adopting AES
  owner: claude-code:aes-adopt-existing
---

# Adopt existing repositories: a legacy baseline, then plan only what you touch

## Who it serves, the result, one example

**Actor:** Brian, and every agent that works in one of his repositories once that repository is brought under AES.

**Result:** `aes adopt` brings an existing repository under AES in one step. It writes `.aes/legacy_baseline.json`: every tracked file under the governed roots at a named commit, each bound to its Git blob hash, accepted as-is. Those files are not orphans. A commit that leaves them alone needs nothing extra. A commit that edits one of them without a plan is logged in observe mode and refused in enforce mode, using the commit rule's existing `.aes/commit_rule.yaml` mode. Planning the file through `aes plan accept` removes its baseline entry, so the baseline only shrinks. `aes status` prints the share still legacy.

**Example.** DIGIMON (`~/code/Digimon_for_KG_application`) has about 1,800 tracked files and 220 numbered plans. Today `aes init` there followed by a commit is refused: every existing file is an orphan (issue #155 reproduced the same on tinydb's 20 files). After this plan, `aes adopt --governed-root Core/ ...` lists every tracked file under those roots in one JSON file, the adoption commit passes the hooks, and `aes status` reads `legacy: N of N governed files (100.0%)`. When an agent later edits `Core/x.py` under a plan that lists it, the baseline drops to N-1, and the dropped entry is exactly `Core/x.py`.

## Brian's direction (authority)

- 2026-10-06: "once we get aes canonical working we refactor all my projects into aes and force all work going forward into aes compliance."
- 2026-10-07, approving issue #180: "i approve proceed".

## Authority and non-goals

Authority: Brian's direction above; AES canonical is his repository, and its governed roots change only through an accepted AES plan (`.aes/plans/PLAN-AES-ADOPT-EXISTING.yaml`), which implements this plan.

Non-goals: planning any legacy file in bulk; judging whether legacy code is good; migrating DIGIMON's numbered plans (item 5 below is already how the commit rule works); changing the observe/enforce rollout schedule in `proposals/aes-planning/ROLLOUT.md`; installing AES hooks in DIGIMON.

## Irreversible actions and spend

This plan proposes zero irreversible actions and zero spend. Every change is code, tests and documents in AES canonical, merged by pull request; containment is `git revert` of that merge. A repository with no `.aes/legacy_baseline.json` behaves exactly as before. DIGIMON is only read: the adoption run happens in a claimed maintenance worktree that is closed with `make session-close` and nothing is committed or pushed there. No model call, deployment, data deletion or outbound message.

## Design

1. **`aes adopt [--revision REV] [--dry-run]`.** In a repository without `.aes/`, it takes `aes init`'s arguments, initializes the project, and writes the baseline. In a repository that already has `.aes/`, it writes only the baseline. It refuses when a baseline already exists. The baseline holds `adopted_at_revision` (the full SHA of REV, default HEAD), `adopted_at`, `governed_roots`, and `files: {path: blob}` from `git ls-tree -r REV` under those roots, minus files the target already plans. One sorted JSON file, one line per file; 1,800 files is about 150 KB. `--dry-run` writes nothing and prints the same summary.
2. **Not orphans.** `topology.compare_topology` takes the legacy set (baseline paths the target does not plan). Those files are reported as legacy, not orphans, in `aes topology check` (the pre-commit hook), `aes characterize` drift and `aes reconcile`/`aes status`. A file in neither the target nor the baseline is an orphan exactly as today (requirement 4).
3. **Unplanned legacy edit.** `commit_rule.judge` receives the legacy set. A commit that modifies (`M` or `T`) a path still in it is refused with reason `unplanned legacy edit: <paths>`, under any tag except Git's own messages and `[Unplanned]` with an `Emergency:` line. Mode comes from the existing commit-rule config: observe logs the verdict to `<git-common-dir>/aes/commit-rule-<date>.jsonl` and lets the commit land; enforce refuses it. A deleted legacy file (`D`) is allowed: removing old code is how a strangler fig ends. A tagged `[Goal <id>]` commit does not by itself make a legacy file planned; the target does.
4. **Planned through a plan.** After `aes plan accept`, the CLI prunes baseline entries whose path the target now plans or Git no longer tracks, and prints which. The target, the plan file and the shrunken baseline are committed together.
5. **Status.** `aes status` adds `legacy: L of G governed files still in the baseline (P%), C changed since adoption at <sha>`. `C` counts legacy files whose indexed blob differs from the baseline (edits that landed in observe mode), so leakage is visible.
6. **Old plans are history.** A `[Plan #N]` commit already counts only when `docs/plans/N_*.md` declares a `method_conformance_receipt` whose adoption decision reads `adopted` for the plan's current bytes (`commit_rule.receipt_status`). DIGIMON's earlier plans without a receipt therefore do not count until adopted through Company Planning. This plan changes nothing there and says so in GETTING_STARTED.
7. **Issue #155.** GETTING_STARTED gains "Starting on an existing codebase": `aes adopt`, commit, then `aes hooks install`. `aes init` warns, naming `aes adopt`, when the governed roots already hold tracked files.

## Activation facts

Declared in `activation-facts.json`: `shared_mechanism` true, because the plan adds a shared contract (`.aes/legacy_baseline.json`, read by topology, characterize, reconcile, status and the commit rule). `empirical_comparison_proposed` false: the plan compares no alternative designs; its runs check the built result against expected outcomes. `llm_central` false: no model is called anywhere in the change. `irreversible_or_spend_action` false: see "Irreversible actions and spend".

## Prior art

Searched: existing ownership in this repository (`topology.py`, `characterize.py`, `commit_rule.py`, `planning.py`), internal lineage (issues #180 and #155, `proposals/aes-planning/` commit rule and its observe/enforce rollout), and external prior art. Each candidate found, with one disposition:

| Candidate | What it does | Disposition |
| --- | --- | --- |
| SonarQube "clean as you code" | quality gate applies to new and changed code only | **reuse** the rule: untouched legacy needs nothing, touched code must meet the bar (a plan) |
| ESLint bulk suppressions (`eslint-suppressions.json`), mypy baselines, Betterer | freeze today's violations in one file; fail only on new ones; the file only shrinks | **reuse** the mechanism: one baseline file, entries removed as files are fixed, never added after adoption |
| Strangler-fig pattern (Fowler) | replace a legacy system piece by piece as it is touched | **reuse** as the migration shape: deletion of legacy files is allowed, edits route through a plan |
| AES `topology.compare_topology` orphan rule | every governed file must be planned | **extend** with a legacy set; the rule is otherwise unchanged |
| AES commit rule (`commit_rule.judge`, `.aes/commit_rule.yaml` observe/enforce, daily JSONL log) | judges each commit and logs or refuses by mode | **reuse**: the legacy-edit check is one more reason in the same verdict, same mode, same log |
| AES `aes init` | writes `.aes/project.yaml` and the target | **reuse**: `aes adopt` calls it, then writes the baseline |
| AES commit rule's plan receipt check (`commit_rule.receipt_status`) | a `[Plan #N]` counts only with an adopted Company Planning receipt for the plan's current bytes | **reuse** unchanged for requirement 5: a repository's old numbered plans are history until adopted |

**Parallel-implementation check:** `git grep -n "legacy_baseline" -- src/agentic_engineering_system` must show one loader in `adopt.py`; a second baseline reader or a second orphan rule is a parallel implementation.

## Uncertainties

These are the plan's material uncertainties; each could make adoption fail its purpose. There are no others.

| Material uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Refusing every unplanned legacy edit under enforce may push agents to `[Unplanned]` emergencies or to skip AES on large repositories. | The AES coordinator session that owns `proposals/aes-planning` | The commit-rule log of the first adopted repository's first observe week: if more than 1 in 5 commits would be refused only for legacy edits, the rule needs a lighter route (for example a `[Trivial]` allowance) before enforce. |
| Characterizing every legacy Python file may make `aes status` slow on large repositories. | This plan's owner | The DIGIMON run's timing below: over 30 seconds for `aes status` means characterize should skip unchanged legacy files. |

## Success and what would disprove it

Every criterion names its run, where the full trace is kept, and what must be seen in the trace beyond the outcome.

- **SC-1 baseline of a real repository.** Run: `test_adopt_real_repository_lists_every_tracked_file` in `tests/greenfield/test_adopt.py`, which clones this repository (`git clone --local`), removes its `.aes/` in a commit, and runs `aes adopt` with `src/` and `tests/` as roots. Trace: `proposals/aes-adopt-existing/evidence/test-adopt-<sha>.txt` (pytest `-v -rA` output with the command output the test prints). Seen in the trace: the baseline's path set equals `git ls-files src tests` at the adoption revision (set equality, with the first missing or extra path printed on failure), every blob equals `git ls-tree`'s, and `aes status` prints `100.0%`.
- **SC-2 the init commit passes (issue #155).** Run: `test_adoption_commit_passes_installed_hooks` in the same file. Trace: same file. Seen: `aes hooks install` output, then `git commit` exit 0 with the pre-commit output `0 orphan(s), N legacy`.
- **SC-3 unplanned legacy edit.** Run: `test_unplanned_legacy_edit_observe_logs_enforce_refuses`. Trace: same file, plus the test's printed JSONL log line. Seen: in observe, the commit exits 0 and the log line has `verdict: refuse` with `unplanned legacy edit: <that path>`; in enforce, `git commit` exits 1 with the same reason and HEAD does not move.
- **SC-4 planning shrinks the baseline by exactly that file.** Run: `test_plan_accept_removes_exactly_the_planned_file`. Trace: same file. Seen: `before - after == {that path}` and `after <= before`, the CLI's `baseline: removed 1` line naming the path, and the following edit commit under enforce exits 0.
- **SC-5 a new file outside a plan.** Run: `test_new_unplanned_file_is_still_an_orphan`. Trace: same file. Seen: the pre-commit output `orphan: <new path>` and exit 1, with the legacy files still not reported as orphans.
- **SC-6 first real use, DIGIMON.** Run: `aes adopt --dry-run` and then a real `aes adopt` (uncommitted) in a DIGIMON maintenance worktree, then `aes status` before and after. Trace: `proposals/aes-adopt-existing/evidence/digimon-adopt-2026-10-07.txt`, with DIGIMON's file paths replaced by counts because DIGIMON is private and this repository is public. Seen: the per-root file counts equal `git ls-files` counts per root, `aes status` before (no project: exit 1) and after (`100.0%`), each command's wall time, and the baseline's byte size.
- **Gates.** Run: `make aes`, `make aes-check`, `make check` on the final branch head. Trace: `proposals/aes-adopt-existing/evidence/gates-<sha>.txt` (full output of the three runs). Seen: each run's passed/failed/skipped counts and exit status, the five `test_adopt.py` tests by name among the passed, and `aes status` in `make aes` reporting no orphan for this repository (which has no baseline, so it must print no legacy line).

**Disproved if** any of these is seen in the first adopted repository's first observe week. Run examined: every commit in that repository from its adoption commit onward, replayed with `aes commit replay <adoption-sha>..HEAD --json`. Trace: that repository's commit-rule log `<git-common-dir>/aes/commit-rule-<date>.jsonl` (one JSON line per commit verdict, kept per day) plus `git log -p` of `.aes/legacy_baseline.json`; the replay output is saved to `proposals/aes-adopt-existing/evidence/first-week-replay.txt`. What must be seen, beyond the commit landing:

- a commit editing a baseline file that landed under enforce: its log line shows `verdict: accept` while `git show --name-status` lists an `M` on a path still in the baseline at that commit;
- a baseline entry that disappeared without its file being planned or deleted: a `git log -p` hunk removing a baseline line where the same commit's target diff adds no planned artifact with that path and the file is still in `git ls-files`;
- an adoption commit refused as orphans: a log or hook output line `orphan: <path>` for a path present in the baseline of that commit.

## Verification

`tests/greenfield/test_adopt.py` (SC-1 to SC-5, real clone and real installed hooks), the existing `test_topology.py`, `test_commit_rule.py` and `test_characterize.py` still passing, `aes evidence record VS-ADOPT`, and the DIGIMON run (SC-6).
