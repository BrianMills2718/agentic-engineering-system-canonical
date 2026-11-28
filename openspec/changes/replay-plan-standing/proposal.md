## Why

Brian, 2026-11-28: "continue through all remainign hihg condience items". The replay viewer ideas still open from
the 2026-11-28 list were: a flag on each write the plan does not list, a track of each requirement's progress, and the
wiki as the agent saw it (the requirement lens, idea 1, is already the plan pane). On the step-5 proof session Brian
noticed only by eye that the agent had not written the plan first; the page should show where each write stood
against the plan, how far each requirement got, and which wiki pages the agent opened.

## What Changes

- Each write event carries `planned`: `planned` (a layout row names the file and a plan write earlier in the session
  or the plan before it did), `row added later` (only a later plan write names it), `unplanned` (no row, under a
  governed folder) or `outside` (no row, not governed). The timeline flags `unplanned` in orange and `row added later`
  in grey.
- `/api/status` gives each requirement's state from `lockstep status` now, with its code and test files; the plan
  view shows a track per requirement: not started, code written, tests written, then the state now.
- `/api/wiki` lists the generated wiki pages; the wiki pane shows them all, the ones read so far highlighted.

Plan size: small
