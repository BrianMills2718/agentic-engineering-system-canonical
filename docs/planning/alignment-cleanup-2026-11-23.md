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
2. For each remaining finding, read the requirement and the code, then: mark the code that does it; correct a wrong
   ID; add a missing test; or, when nothing implements it, record it under "To discuss" (removing a requirement is a
   product call, not mine).
3. Fix #1019 (requirements with empty statement text). Done (item 3 below).
4. Make the check block merges: `lockstep check trace` in `make check`. Requirements recorded as not built stay
   visible without failing every merge only through a committed list that may shrink and never grow (inferred by
   agent; see "To discuss").
5. Mark the plans this replaces as replaced; make the design review a step before a Lockstep plan is adopted.

## Acceptance

- `lockstep check trace` exits 0 (or reports only the committed not-built list), and `make check` runs it.
- A new requirement with no `Implements:` line fails `make check` (shown by a test).
- Every judgment call is listed below with its evidence.

## To discuss (concerns, open questions, inconsistencies, recommendations)

Each item: what, evidence, my recommendation. Added as found.

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
   nobody linked, or Lockstep has code with no written requirement. Being classified in step 2.
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
