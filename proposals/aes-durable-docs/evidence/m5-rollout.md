# M5 rollout record

Inventory: `m5-inventory.json` (22 active governed repositories, built by Haiku readers on 2026-10-11).
Each repository got one PR that adds its durable document set (system model at `docs/model/ARCHITECTURE.md`, per company-planning#116), checked with `durable_docs_check.py --arc42` and the repository's own local check before merge.
"Daily check" is `project-meta/scripts/md_file_cap.py --repo <path> --ref origin/main`, run after merge; `durable=ok(0)` means zero durable-set findings on main.

## Wave 1 (2026-10-11)

| Repository | PR | Merge | Method | Daily check |
|---|---|---|---|---|
| fol-operational-metamodel | #19 | 11b9d480c | merge | durable=ok(0) |
| epistemic-warrant | #40 | 9ca2c95e5 | merge | durable=ok(0) |
| brianmills-spec/representation-router | #114 | b273c514d | merge | durable=ok(0) |
| dodaf | #519 | 547c0018b | merge | durable=ok(0) |
| agent_ecology3 | #118 | 35daa11dd | rebase (linear history required) | durable=ok(0) |
| qc | #131 | 474b1e414 | squash (linear history required) | durable=ok(0) |
| process_tracing | #279 | c9bfb2583 | merge | durable=ok(0) |
| onto-canon6 | #552 | 6b9983265 | merge | durable=ok(0) |

## Wave 2 (2026-10-11)

| Repository | PR | Merge | Method | Daily check | Notes |
|---|---|---|---|---|---|
| world-substrate | #149 | ef6ef43b4 | rebase | durable=ok(0), md=104 (over cap, was 103) | system model prose points at existing `docs/model/ODD.md`; goal at `docs/architecture/GOAL.md` |
| inquiry-graph | #193 | 3dc043727 | merge | durable=ok(0), md=76 | |
| brent-chatgpt | #236 | 6ded12a5b | merge | durable=ok(0), md=174 (over cap) | private repository; `roadmap/GOAL.md` renamed `ACTIVE_GOAL.md`; decisions and glossary not_applicable; 1 test failure reproduces on unmodified main |
| digimon_application_20260215 | #446 | 675b38b33 | rebase | durable=ok(0), md=100 (cap exception) | repository commit hook refused `[Goal <plan_id>]` until its meta-process.yaml pattern was extended (project-meta #2525) |
| observation-to-action-metamodel | #140 | 607ad32d9 | merge | durable=ok(0), md=197 (over cap) | spot check: cited `evaluate.py:108/197/473` resolve to the named functions |
| personal-vps | #130 | 039ebf810 | merge | durable=ok(0), md=46 | |
| personal-file-infra | #136 | 63ac93d21 | squash | durable=ok(0), md=13 | |
| parallax-research-workbench | #24 | 4cda95d12 | rebase | durable=ok(0), md=227 (over cap) | 1 test failure reproduces on unmodified main |

## Friction found during rollout

- project-meta #2524: the shared commit-msg wrapper runs the main checkout's hook instead of the worktree's.
- project-meta #2525: older meta-process.yaml commit hooks refuse the workspace `[Goal <plan_id>]` tag.
- Merged remote branches `durable-docs` remain on world-substrate, personal-file-infra and process_tracing: remote branch deletion is blocked by the session safety hook; harmless.

## Wave 3 (2026-10-11)

| Repository | PR | Merge | Method | Daily check | Notes |
|---|---|---|---|---|---|
| portfolio | #295 | b33399dea | rebase | durable=ok(0), md=275 (over cap) | goal is arc42 section 1 of ARCHITECTURE.md (no net new .md beyond it); `check_all.sh` fails 1 of 52 on unmodified main (portfolio #296) |
| vision | #115, #116 | cc08af2b2, 1b9365618 | rebase | durable=ok(0), md=2449 (cap exception) | `tools/check.sh` PASS; #116 needed because the federation map gate snapshots other repositories (vision #117) |
| weekly-plans | #212 | fe3d0d758 | rebase | durable=ok(0), md=344 (over cap) | no local gate; its pytest (2 failures) and drift checks fail identically on unmodified main; new documents hold structure only, no private content |
| chatgpt-bug-audit | #2 | b7736999c | merge | durable=ok(0), md=12 | loop state untouched; trace covers 3 of 6 requirements, the other 3 declared as having no check |
| agent-skills | #474 | 95823d4e7 | merge | durable=ok(0), md=534 (over cap) | `make session-close` clean; requirements inside GOAL.md; reachable via roadmap/README.md |
| project-meta | #2526 | 15cfecacd | merge | durable=ok(0), md=1038 (over cap) | goal in ARCHITECTURE.md because `vision/` is frozen there; decisions at new `docs/decisions/`; full suite 11 failed / 3050 passed, every failure also fails on unmodified main `d0bf845` (24 failed in the same three files), `project-graph-check` fails on main too (project-meta #2528) |

## Daily check (R10)

project-meta PR #2529 (merge `d0bf845`) extends `scripts/md_file_cap.py` with the durable-set pass. Its run on 2026-10-11 against every rolled-out repository at `origin/main` reported `durable=ok(0)` for each one, and the summary line counts `durable ok/findings/undeclared` (for example `durable ok=1 findings=0 undeclared=0`). `layout=undeclared` appears where a repository's `.agentic/repo.yaml` declares `durable_documents` without `authorities`. That is the layout check's own state, not a durable-set finding.
Merge gate for #2529: `tests/test_md_file_cap.py` passed (19 tests). The full suite had 12 failures, 11 of which also fail on unmodified main and 1 of which is flaky; `project-graph-check` fails on main as well. Both problems are recorded in project-meta #2528.
