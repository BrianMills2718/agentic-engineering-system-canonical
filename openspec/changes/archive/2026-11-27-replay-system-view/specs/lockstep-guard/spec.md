## ADDED Requirements

### Requirement: The replay has a plan, code and wiki view

The replay page SHALL offer a toggle between its timeline view and a plan, code and wiki view that steps through
the same events with the same controls. That view SHALL show the agent's current step; for the file of that step,
its `lockstep.yaml` layout row and the text of the requirements it implements (or that no row names it), its code,
and the requirement pages and specs the agent has read so far; and a band of hook cards (hand-over, refusal,
warning, read marks) marking the ones the current event shows. The server SHALL answer `/api/plan?file=<path>`
with that layout row (or null), whether a governed folder and a `fixed:` glob cover the file, and each implemented
requirement's id and text.

Source: Brian, 2026-11-28: "can you create a version of the session replay (togglable) that looks more like
file://wsl.localhost/Ubuntu-24.04/home/brian/code/inbox/ai-astronauts-hive-brain-explainer.html from the plan code
wiki page". The panes, the hook band and the plain-JSON route are inferred by agent from that page's tab 7.

#### Scenario: The plan route gives a file's row and requirement text

- **WHEN** the page asks `/api/plan?file=src/greet.py` and `lockstep.yaml` has a layout row for it that implements
  a requirement with text in `openspec/specs/`
- **THEN** the answer holds that row, `governed` and `fixed` as the plan sets them, and the requirement's id and text
- **AND** for a governed file no row names, `row` is null and `governed` is true

#### Scenario: The page offers the view as a toggle

- **WHEN** the page is served
- **THEN** it holds a toggle that switches to the plan, code and wiki view, and the timeline view is shown first
