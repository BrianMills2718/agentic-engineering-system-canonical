---
description: Bring AES's specs and code into agreement and make the alignment check block merges, so plans cannot quietly drift
---
# Plan: alignment cleanup

Source: Brian, 2026-11-23: "cleanup. and as you go make sure to docuemtn any concern open quesiton icnonsitencies
recommndations or anythgin else we should discuss", after asking why the work keeps going off track. Plan size: small
planned work (one repository, undone with `git revert`, nothing outward). Governs before slice 2 of
[back-on-design](back-on-design-2026-11-23.md).

## Why

`lockstep check trace` compares OpenSpec requirements with the code's `Implements:` lines and the tests' markers. On
main `634c54c7b` it reported 142 findings (101 unimplemented, 33 unknown, 7 untested, 1 unclosed quote) and blocks
nothing, so a plan that drops or invents a requirement merges cleanly. That is one root cause of the drift Brian named.

## Steps

1. Search the folders that hold code: `[tool.lockstep] source = ["src", "scripts"]` in `pyproject.toml` (the check read
   only `src/`, while `scripts/` carries its own `Implements:` lines). Done: 142 -> 108 findings; the parser fix and
   the first marks took it to 86.
   Step 2 result: 86 -> 16. Of the drop from 55 to 23, 32 findings came from one thing: the plan copies in
   docstrings had never been regenerated after their layout rows changed (item 14).
2. For each remaining finding, read the requirement and the code, then: mark the code that does it; correct a wrong
   ID; add a missing test; or, when nothing implements it, record it under "To discuss" (removing a requirement is a
   product call, not mine).
3. Fix #1019 (requirements with empty statement text). Done (item 3 below).
4. Done: `make check-trace` (run by `make check`) compares the findings with `docs/planning/trace-accepted.txt`
   (16 lines: items 5, 6 and 13). A new finding fails, and so does a fixed one still on the list, so the list can
   only shrink (the list is inferred by agent: it keeps the known gaps visible without failing every
   merge).
5. Done, corrected: the earlier wording "mark the plans this replaces as replaced" was wrong. `linked-chain-core` and
   `links-existing-lines` are built (#1011 to #1017) and now say so; `minimal-core` now says its milestone was met and
   that one inference in it (file list folded into `tasks.md`) is reversed by `back-on-design`. The design review
   before adoption is item 5 of `back-on-design`; it lives only there (item 17).

## Acceptance

- `lockstep check trace` exits 0 (or reports only the committed not-built list), and `make check` runs it.
- A new requirement with no `Implements:` line fails `make check` (shown by a test).
- Every judgment call is listed below with its evidence.

## To discuss (concerns, open questions, inconsistencies, recommendations)

Each item: what, evidence, my recommendation. Added as found. The open ones are also Q49 to Q55 in `docs/planning/open-questions.json`.

1. **The trace check never searched `scripts/`.** No `[tool.lockstep] source` was set, so 45 requirements implemented
   in `scripts/` read as unimplemented and 11 wrong IDs there went unseen. Fixed in step 1.
2. **The trace check's line reader joined stacked `Implements:` lines.** In a function docstring, two indented
   `Implements:` lines in a row were read as one wrapped list, giving a nonsense ID (`client_manifest.py:91`,
   `machine_manifest.py:309`). Fixed in `src/lockstep/checks/markers.py`, with a test.
3. **12 requirements had empty statement text (#1019).** The spec reader stopped at the `Source:` line, and 12
   requirements put `Source:` first. The reader now takes the text after the `Source:` paragraph when there is none
   before it; one spec (`external-idea-intake`) had no blank line between them and was reordered. Recommendation:
   one fixed order for every requirement (statement, blank line, `Source:`), checked by `lockstep check`; today
   the order is a habit, not a rule.
4. **29 of the 57 plan rows for Lockstep's own files name no requirement.** The generated docstring then says
   `Implements: (no requirement)`, which the trace check reads as a bad ID. Either the code serves requirements
   nobody linked, or Lockstep has code with no written requirement. Classified in step 2: 15 rows now name the
   requirements they serve; the generated line for the rest now reads "Names no requirement; the layout row says
   why." so it is no longer parsed as an ID. The 14 rows left are item 15.
5. **Six template requirements are built where the trace check cannot see them.** `portable-template` is
   implemented in `copier.yml` and `template/` files, which are not Python and not under `src` or `scripts`.
   Question: should the check read `Implements:` lines in template files (comments in YAML and shell), or should
   these requirements be listed as checked by their tests only? Recommendation: let the check read comment lines in
   configured non-Python files; the tests already exist (`tests/test_template_portable.py`).
6. **`aes-documentation-projection` repeats `lockstep-doc-facts`.** Its requirements are the AES copy of a general
   Lockstep feature and its three scenarios have no tests. Recommendation: keep only the general one and say in
   AES's plan that AES uses it.
7. **Code and spec disagree on which instruction file wins.** `scripts/scan_doc_freshness_ecosystem.py:69-75` prefers
   `CLAUDE.md` when both exist; the `instruction-audit` spec says `AGENTS.md`. No test created both files. Fixed: the
   code now follows the spec, with a test.
8. **Small spec errors found while classifying:** one `portable-template` requirement has no `Source:` line; the `inert-characterization` test checks
   less than its scenarios promise (dirty state and exact checkout identity are not asserted).
9. **Two test markers were invisible to the check.** Markers passed through `pytest.param(marks=...)` are not read
   (`tests/greenfield/test_characterize.py`); they are now decorators. Recommendation: the check should read them,
   or `lockstep check` should refuse that form, so the next one is not silently missed.
10. **A reader's wrong call, caught.** A classification reader said the `prune-merged-worktrees` scenario's `--dryrun`
   was a typo; it is a deliberate mistyped flag the scenario tests (`scripts/prune_merged_worktrees.py:310`). Each
   reader's mark is checked against the code before it is applied.
11. **Quote markers shown as code were read as real markers.** A document describing the syntax
   (`` `<!-- lockstep quote: <id> -->` ``) produced an "unclosed quote" finding. Fixed in `src/lockstep/checks/quotes.py`:
   markers inside code spans and fenced blocks are skipped; the quoted passage itself is still read in full.
12. **This session ran twice in the same worktree.** After a restart the session was resumed in two terminals, and
   both copies applied the same classifications to `aes-wt-clean` (one made a WIP commit). They found each other
   through a duplicate line and an unexpected commit, agreed by message that one stops, and every edit was checked
   against the readers' findings. Recommendation: resuming a session that is already running should be refused or
   warned about; worktrees give no protection when both writers are the same session.
13. **Six requirements for one script live in another repository's spec.** `scripts/concern_issue.py` and
   `tests/test_concern_issue.py` name `compliance-list/...` IDs, but the `compliance-list` spec exists only in
   `~/code2/workspace/openspec/specs/compliance-list/`, so this repository's check reads them as unknown. They are
   on the accepted list. Recommendation: the requirement "An open concern's title follows the repository's current
   status" describes this script, so move that one requirement into an AES spec named for the script, and leave the
   list-making requirements in code2-workspace. Moving it renames the IDs in both repositories, so it waits for
   one change that touches both.
14. **Plan copies in docstrings went stale with no check failing.** After layout rows gained requirement IDs, the
   docstrings still held the old copies until `lockstep check project` was run by hand (it rewrote 49 files). The
   copies are what an editing agent reads, so a stale copy hands it the wrong requirement. Also, a planned file
   with no cog block (`src/lockstep/plan_check.py`, now fixed) is never given a copy, and nothing reports that.
   Recommendation: `make check` should fail when a copy is stale or a `fixed:` file has no block (cog's own
   `--check` does the first).
15. **14 Lockstep files carry behavior from the retired `.aes/target.yaml` route with no OpenSpec requirement.**
   `action_check`, `behavior_check`, `change_list`, `change_log`, `criterion_checks`, `declared_reason`,
   `docstring_up`, `linked_tests`, `plan_edit`, `plan_to_code`, `requirement_status`, `unplanned_symbols`, `wiki`,
   `wiki_reach`. Their docstrings cite "behavior N.N" from the old plan; some say they are "part of make check",
   which the Makefile does not call. Also `unplanned_symbols` and `stale_edit` still word their messages in
   `.aes` plan terms. Either they serve the minimal core and need requirements, or they belong to the route
   decision 0009 retires. Recommendation: list which ones the five-check minimal core actually calls; write one
   requirement for those, and retire the rest through `docs/retired/` (a deletion, so it needs your yes).
16. **`make check` did not run the trace check before this change**, though `docs/architecture/LOCKSTEP.md` and
   the back-on-design plan treat trace as one of the core checks. That is how 142 findings built up unseen.
   Fixed by step 4.
17. **The design review before a plan is adopted is written in one plan, not in the rule agents read.**
   `back-on-design-2026-11-23.md` item 5 says every later Lockstep plan gets a cold read against the settled
   documents that lists each departure. Agents planning new work read code2-workspace
   `agents/topics/working-method.md` ("plan size": one independent read), which does not ask for departures from
   the settled documents. Drift came in exactly there: the minimal-core plan folded the file list away as an
   agent inference and no reader checked it against `LOCKSTEP.md`. Recommendation: add one sentence to that
   "independent read": it lists every departure from the project's settled design documents, with file and line.
   That changes a rule every agent follows, so it is not made in this change.
18. **The acceptance line "shown by a test" merged without the test.** `make check-trace` did fail on a made-up
   unbuilt requirement when tried by hand, but no test under `tests/` ran the gate, so a later edit to the Makefile
   could have quietly made it pass everything. Fixed after the merge: `tests/test_check_trace_gate.py` runs the
   real gate against the committed list (passes), a list missing one finding (fails, as a new unimplemented
   requirement would), and a list with an extra finding (fails); the list and output paths became Makefile
   settings (`TRACE_ACCEPTED`, `TRACE_NOW`) so the test needs no copy of the repository. Recommendation: read each
   acceptance line against the diff before merging; a closing checklist would have caught this.
