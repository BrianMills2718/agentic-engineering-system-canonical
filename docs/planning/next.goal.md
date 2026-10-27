---
description: Next goal for AES canonical while it is on hold -- make the repository's own checks and documents tell the truth, without new product work
---

# Goal: AES on hold, checks honest

Planning package: docs/planning/planning-package.json

Status: proposed 2026-10-27, waiting on Brian's call Q1 (default: this goal runs).

## Why this goal

AES canonical is on hold ([now.md](../../.project-brain/now.md) line 3), but its own checks
now say things that are false or stale: four checks fail, `aes status` reports 2 of 12
criteria supported where Decision 0010 accepted its 9, the target and the goal document still
rest on the commit rule that was removed on 2026-10-14, and AGENTS.md describes a pre-commit
gate that does not run here. While it stays on hold (the
recommended answer to Q1), the useful work is to make every check and document here true,
and to keep the `aes` CLI working for dodaf and whygame5 (Q12). No new product work.

## Done when

Each line is checked by the command beside it; the package is rebuilt at the end.

1. **Commit-rule outcome withdrawn (Q15).** OUT-AP-001, and TR-REQ-001 with it or re-pointed,
   withdrawn through `aes plan prepare` / `validate` / `accept`, target and plan committed together;
   `aes target validate` exits 0.
2. **Evidence re-recorded (Q6).** `aes evidence record <VS-ID>` run for each deterministic-test
   subject behind the nine criteria Decision 0010 accepted; `make aes` shows the supported count,
   and any of the nine that does not return to SUPPORTED names its failing test. The criteria added
   later are listed with the evidence kind each still needs (SC-TR-SOURCE-001: a trace review;
   SC-GF-001: a clean-user runtime observation). The unreachable plan PLAN-AES-SELF-GOVERN stays a
   warning by design (`reconcile.py` lines 18-20).
3. **Plan statuses true (Q4).** Each of the 23 plans whose adoption receipt the recheck lists has a front-matter
   status of `done` or `superseded` (with the merge or decision that settled it), or stays
   adopted with a reason; `cli.py lint --repo-root . --recheck` exits 0 or lists only those kept.
4. **Docstring wiki current (Q3).** `make docstring-wiki` committed; `durable_docs_check.py --repo .
   --arc42` exits 0.
5. **Markdown count inside the cap (Q7).** Superseded plan bundles nothing cites moved to
   `~/archive/agentic-engineering-system-canonical/<timestamp>/` after a content comparison, with
   restore commands; `.md-file-cap.yaml` limit and reason updated for the rest;
   `md_file_cap.py --repo .` exits 0.
6. **Goal and instructions without the commit rule (Q5, Q14, Q16).** GOAL.md's thesis and
   disproof rewritten on the two boundaries that remain, the disproof resting on `make aes`
   topology runs; CLAUDE.md (which generates AGENTS.md) names `make aes` as the orphan check while
   the pre-commit hook is not installed; `.aes/commit_rule.yaml` removed;
   `python scripts/meta/check_agents_sync.py --check` exits 0.
7. **Roadmap linked (Q8).** wiki/index.md links the roadmap named in `.agentic/repo.yaml`, marked
   on hold; `validate_project_navigation.py .` reports 0 warnings.
8. **code2 format, cheap parts (Q17).** `docs/index.md` pointing at wiki/index.md and a
   `code2check` Makefile target (make aes plus the link check); arc42, `.c4` and OpenSpec specs
   recorded as deferred while on hold; `repo_format.py .` names only the deferred items.
9. **Decision 0011 item 4 closed or kept (Q2)** as Brian answers; by default it is left as written.
10. **Package rebuilt** from the final revision; `validate_planning_package.py` exits 0.

## Out of scope

- New v0.2 components, the v0.1 Plan 002 line, and the vendored `enforced_planning/` package
  (Q10: left in place while on hold).
- Anything in the other repositories that carry `.aes/`.

## Domain concepts this plan relies on

Target, outcome, accepted plan, plan adoption receipt, observation, freshness, criterion standing,
success criterion, verification subject, pre-commit hook, the checked-boundary thesis and the
commit rule (retired), as defined in [DOMAIN.md](DOMAIN.md).

## Trace and evidence

Every `aes evidence record` run writes its observation under `.aes/observations/` with the
command, revision and result; the agent reads each failing one in full, and a sample of passing
ones, before reporting the count. Each check's command, exit status and counts go into
`docs/planning/checks.txt` when the package is rebuilt.
