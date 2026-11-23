---
description: Get Lockstep back on its settled design - planned files before code - starting with Lockstep's own repository
---
# Plan: back on the settled design

Plan size: full (changes how Lockstep governs its own repository and, in slice 2, every template copy). Source: Brian,
2026-11-23: "i approve", to: (a) a plan that starts from `docs/architecture/LOCKSTEP.md`, reviewed for every departure
from it, code2-workspace decision 0006 and AES decision 0004, the departures brought to him; (b) the full system turned
on in AES (edit hook, `lockstep.yaml` layout for the Lockstep package, quote markers on the key design passages);
(c) the planned file layout back in the template. He raised it after finding that the minimal core had dropped the
layout and that Lockstep is not used on itself.

## What the settled documents say (read 2026-11-23)

- `docs/architecture/LOCKSTEP.md:22-29`: start from planned structure: name the behavioral units, the files that hold
  them, their typed seams, the requirements they implement and the tests that establish success; then implement inside
  those boundaries. Chain: requirement -> success criterion -> proving test or check -> file -> symbol.
- `LOCKSTEP.md:52-62` ("What moves down"): OpenSpec owns behavior; `lockstep.yaml` owns file purpose, requirement links,
  test paths and optional exports; `scaffold.py` creates missing planned files and fills their docstrings; the edit
  hook supplies requirement context and checks planned boundaries.
- `proposals/one-planning-tool/DESIGN.md` (adopted by Brian 2026-11-11, "i approve single tool desing re d4"), example
  steps 2-4: the plan is an OpenSpec change plus `layout:` rows (file, purpose, implements, tests), accepted by a
  person; `lockstep layout` creates the planned files, each docstring holding the requirement text, success criteria
  and test names; a write to a file the plan does not name is refused, showing the plan.
- code2-workspace decision 0006: per requirement and scenario, which symbols implement it and which tests test it; a
  plan lists the IDs it closes (`Closes:`); requirement text written into the implementing docstring.
- AES decision 0004: structured normative records; decisions, plans, research and evidence keep their own lifecycles.
- `docs/planning/acceptance-criteria.json:287-299` rows R9 and R10, Brian's words: "person approves, then agent
  lays out files", "writes first doc strings".

## What exists and what is off (checked 2026-11-23, origin/main)

- Built: layout rows read by `layout_plan.py` (`openspec/specs/lockstep-plan-format/spec.md`), `lockstep layout`
  (`scaffold.py:68`), hook refusal of an undeclared governed file (`hook.py`, warn by default, refuse with
  `PCW_MODE=block` or a `fixed:` glob, `hook.py:233-244`), whole-tree `lockstep check`.
- Off in AES: `lockstep.yaml` has `governed: []` and `layout: []`; `.claude/settings.json` runs only `lockstep refresh`
  (pinned commit), not `lockstep-hook`; no hook log exists for AES; no requirement or quote marker ties to
  `LOCKSTEP.md`. Lockstep has 56 Python files; 31 carry `Implements:` lines.
- Off in the template: no `lockstep.yaml`; its `.claude/settings.json` and `.codex/hooks.json` run the edit hook, text hand-over only, so nothing can be refused; the minimal-core plan folded the file list into `tasks.md`
  (`minimal-core-2026-11-20.md:103`, an agent inference citing K8, not Brian's call).

## Slice 1 (this plan): Lockstep governs its own package

1. `lockstep.yaml`: `governed: [src/lockstep/]` (folder form; `unplanned_files.py:59` matches by prefix), `fixed: ["src/lockstep/*"]` (so the hook refuses rather than warns, `hook.py:233-244`), and one `layout:` row per existing file in `src/lockstep/`: path,
   purpose (the module docstring's first line), `implements` (its `Implements:` IDs, empty when none), `tests` (the
   test files marked with those requirements' scenarios). Rows for existing files are derived from the code by a
   one-off script whose output is reviewed in the diff; no file content changes.
2. The edit hook runs in AES: `.claude/settings.json` and `.codex/hooks.json` gain the PreToolUse `lockstep-hook`
   entry (the AES package itself, `uv run --quiet lockstep-hook`), beside the existing refresh entry. A write to an
   undeclared file under `src/lockstep/` is refused, as DESIGN step 4 says, with the refusal showing how to add the
   row. Edits to planned files get the requirement text and the decisions that govern them.
3. A requirement makes this checkable, so dropping it fails a test rather than relying on review: new requirement
   `lockstep-plan-format/lockstep-governs-its-own-package` (AES's `lockstep.yaml` names every file under
   `src/lockstep/` in `layout:`, and its client settings run `lockstep-hook`), with a test.
4. Quote markers in `LOCKSTEP.md` on the passages that restate a requirement (the layout row fields and the
   "structure before code" sentence where a requirement states it), so a wording change in either place is caught.
   Correction of an earlier claim to Brian: a quote marker catches changed wording, not a plan that silently stops
   using the layout; item 3 and the review in item 5 are what catch that.
5. Every later Lockstep plan gets a design review before it is adopted: a cold read against the documents listed
   above that lists each departure (dropped or invented) with file and line. Departures go to Brian.

## Acceptance (judged from the run trace)

- In AES, a scratch Claude session's Write to `src/lockstep/not_planned.py` is refused naming the layout, and its edit
  of `src/lockstep/hook.py` receives that file's requirement text; the hook log under
  `~/.local/state/lockstep/agentic-engineering-system-canonical/` records both.
- `lockstep check` (whole tree) and `make check` exit 0 with the layout in place.
- The new requirement's test fails when a row is removed.

## Departures from the settled documents (review 2026-11-23, brought to Brian)

- Rows for existing files are derived from the code, not laid out from an approved plan first (DESIGN.md:25-27, R9). Unavoidable for code that already exists; every new file after slice 1 follows the design order.
- `lockstep layout` and first docstrings (R10) wait for slice 2, as does the template layout (Brian's item c).
- The new requirement and its test, and the review before each plan, are not in any settled document (inferred by agent).
- Already built and not in the settled documents: the layout dropped from the minimal core; refusal made off by default; the hook log moved outside the checkout (#974); decision hand-over limits, node types and `links.json` shape; `lockstep status` written to `docs/status.md`, not the wiki; Codex enforcement left to git hooks. Each is listed with file and line in the review output.

## Parking list (later slices, planned in full when reached)

- Slice 2: the template ships `lockstep.yaml` with layout rows; a plan adds rows; `lockstep layout` creates the files
  with requirement text, success criteria and test names; `links.json` shows planned files before code exists;
  `run-plan` checks against the layout. Prove it in a fresh copy with Claude.
- Slice 3: settle the add-on's invented parts that the review lists (node type names, limits, the wider meaning of
  `Governs:`) with Brian's answers.
