## Why

Brian, 2026-11-17: "i thought this would be striaghtforward with lockstep. like if there is a change in the nromative docuemtnation then that normative docuemtnation gets updated and then the gaps relevant to that normative docuemntation need to be replanned and in compliance wiht the aes planning checklist".

Tested on 2026-11-17 in a scratch clone of code2-workspace ([issue 842](https://github.com/BrianMills2718/code2-workspace/issues/842)): a requirement's text was changed from "10 of the 20 cores" to "8 of the 20". Every Lockstep check still exited 0 and `lockstep status` still showed the requirement `passing`, before any code or test had changed. Lockstep notices a new requirement (trace, test-first). It does not notice a changed one.

He approved building the missing steps on 2026-11-17 ("i approve", Decision 6 option A). This change is the first of them: a changed requirement becomes a gap, the gap needs a plan, and the gap closes only on new evidence.

## What Changes

- New check `lockstep check changed --base <rev>`. It compares every requirement's and scenario's text with the base revision and lists each requirement that is new, changed or removed, with the code that implements it, the tests marked for it (each labelled changed or unchanged since the base) and the plan that names it.
- The check fails when a listed requirement is named by no plan in the same change set (`unplanned`), and when a requirement's statement changed while no scenario under it is new or changed (`no-scenario-changed`): nothing would test the change.
- `lockstep check test-first` now also covers a scenario whose text changed: at least one test marked for it must fail on the base source. A test marked `existing=True` is no exemption there, because the text says the behavior is no longer the existing one.
- A plan can declare a change `Wording-only: <id>, ...`. The declaration is printed and counted, not hidden. It is the one typed statement in this design, and the one way to reword a requirement without a new test.
- `lockstep status` marks a requirement or scenario whose text in an active change differs from the spec `changed, not archived`, so a plan that closes it shows it open. Before this it showed `passing` on the strength of tests written for the old text.

Nothing is stored. "Changed" is computed on every run from the two revisions (decision 0006 in code2-workspace: status is computed, never typed; a gap closes only through new evidence). The existing tools that flag a changed requirement (Doorstop, OpenFastTrace, DOORS Next, Jama) all clear the flag by a manual action, in bulk if wanted; `prior-art.json` has the comparison.

## Definitions used in the requirements

- **Text of a requirement**: the lines under its heading up to its `Source:` line or first scenario. **Text of a scenario**: the lines under its heading up to the next heading. Runs of whitespace count as one space, so re-wrapping a paragraph is not a change.
- **The plan at a revision**: `openspec/specs/`, with the spec deltas of that revision's active changes applied over it. A requirement or scenario in a delta replaces the spec's; one under `## REMOVED Requirements` is removed.
- **A plan in the same change set**: an OpenSpec change (active, or archived since the base) or a page in `docs/plans/` that is new or different from the base revision. It names a requirement when its spec delta has a heading for it, or its `Closes:` or `Wording-only:` line lists the ID.

## Impact

- `src/lockstep/checks/`: new `changed.py`; `spec.py` (scenario text, deltas applied over specs), `test_first.py`, `status.py`, `cli.py`, `config.py` (`changed` joins the check names).
- A repository gets the new check only by adding `lockstep check changed --base origin/main` to its own `make check`. Nothing changes for a repository that does not.
- `test-first` becomes stricter for every repository that runs it: a pull request that changes a scenario's text now needs a test that fails on the base, or a `Wording-only:` line in its plan.

Closes: lockstep-checks/changed-requirements-that-differ-from-the-base-are-listed-with-their-code-and-tests,
    lockstep-checks/changed-every-listed-requirement-is-named-by-a-plan-in-the-same-change-set,
    lockstep-checks/changed-a-changed-statement-needs-a-changed-scenario-or-a-wording-only-declaration,
    lockstep-checks/changed-count-line-and-exit-status,
    lockstep-checks/test-first-a-changed-scenario-needs-a-test-that-fails-before-the-change,
    lockstep-checks/test-first-tests-for-existing-behavior-are-exempt-and-counted,
    lockstep-projection/a-plan-closes-requirement-ids-only-when-they-pass
