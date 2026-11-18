## Why

`lockstep check arch` turned every non-zero exit of `npx likec4 validate` into `DiagramInvalid`, so a
missing `npx`, no network or an unwritable npm cache all printed `RESULT arch-check invalid_diagram=1`.
The 2026-11-18 nightly failure in `BrianMills2718/enforced-planning` was exactly that: the diagram was
valid, npm could not write a shared cache that contained root-owned directories, and the misleading
label made the run look like a repository defect.

The module already separates the two states for its other tool, raising `ImportLinterMissing` rather
than reporting a contract violation. The npx path needs the same distinction.

## What Changes

- A new `DiagramToolUnavailable` is raised when `npx` is absent, when it cannot be started, or when
  `validate` exits non-zero without LikeC4 having run at all.
- Whether LikeC4 ran is decided by running `likec4 --version`, which reads no diagram, rather than by
  matching words in npm's or LikeC4's output.
- A failing JSON export of an already-validated diagram is a tool failure too, instead of an
  unhandled `CalledProcessError` with no `RESULT` line.
- The check reports `RESULT arch-<action> tool_unavailable=1 exit=1` for all of these and still exits
  non-zero: a check that did not run must fail, not pass.
- A diagram LikeC4 did read and reject is still reported `invalid_diagram=1`.
