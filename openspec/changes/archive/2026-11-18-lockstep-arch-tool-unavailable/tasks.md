## 1. Code

- [x] 1.1 `DiagramToolUnavailable`, and an `_npx` helper that raises it when npx is absent or cannot start
- [x] 1.2 `_likec4_ran` decides a non-zero `validate` by running `--version` against no diagram
- [x] 1.3 A failing JSON export of a validated diagram raises it too, instead of `CalledProcessError`
- [x] 1.4 `_arch` prints `RESULT arch-<action> tool_unavailable=1 exit=1` for it

## 2. Tests

- [x] 2.1 New: a missing npx, a LikeC4 that cannot start, a failing export
- [x] 2.2 New: an invalid diagram is still `invalid_diagram`, mocked and against real LikeC4 (slow)

## 3. Spec

- [x] 3.1 Archive as `2026-11-18-lockstep-arch-tool-unavailable`
