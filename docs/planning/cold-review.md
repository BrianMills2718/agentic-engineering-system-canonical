# Cold review: AES canonical planning package, after the Lockstep move

Reviewer: planning-compliance-reviewer subagent, two rounds on 2026-11-12. Reviewed revision: 2224d54882df8bab522fc03fb8b27aed9ca674fd
(HEAD at review, 8b68db029, differs from it only in the review-page HTML, manifest and checks.txt refresh).

Verdict: pass

## Round 1 (read 9507db931): pass with notes

- The previous report's findings (stale domain anchors, `assess` anchor, `blob/main` links before merge, A1/A2/A5 jargon, R13 UNSURE) were fixed or carried as notes.
- About 40 edges of the new Lockstep group in `system-map.md` matched the imports in `src/lockstep/*.py`; no invented edge.
- Checks counts reproduce from `checks.txt:65-69` (135 of 140 Markdown files, 24 unreachable, 4 durable findings).
- Notes: `commit-check` anchor pointed at `checks/cli.py:114`, not `:191`; Q19 cited `wiki/lockstep.md:41`, not `:45`; Q7 cited `checks.txt:64`, not `:65`; F7 evidence cited `behavior_check.py`, which does not import the library; `next.goal.md` said the hook log is `.lockstep/` where the code writes `.pcw/`; slice 0 sat as a stray list item. All fixed in 2224d5488.

## Round 2 (read 8b68db029): pass

- All round 1 notes landed: `domain.implemented.json:42`, `planning-package.json:171` and `domain.graph.json:396` say `checks/cli.py:191` (`def run`); Q19 cites `wiki/lockstep.md:45`; Q7 cites `checks.txt:65`; `next.goal.md:92` and SYSTEM_MODEL.md:139 say `.pcw/` (`src/lockstep/hook.py:178`) with Q23; slice 0 is its own paragraph.
- Lockstep group edges match imports (`hook.py:107-116`, `check.py:404-413`, `hook.py:387`, `plan_edit.py:46`, and the other cited ones).
- Acceptance A1 to A5 are `not built` with entrypoint `planned`, matching `next.goal.md` ("not yet: A1 to A5 are not built, Q22"); A6 to A8 `built`.
- Counts: 23 open questions (17 open, 6 resolved); 55 concepts (42 implemented, 13 dashed); 56 citations resolve; 81 units named on the system map; 8 acceptance entries (5 not built, 3 built, 0 judged).
- Note (not blocking): `next.goal.md` says A6 "fails today" while A6 is marked `built`; read as page built, check failing.
- Not done by the reviewer: no browser render, `run_checks.sh` not rerun.
