## ADDED Requirements

### Requirement: A refusal lists the files the plan allows

When the edit hook refuses (or warns about) a write to a file the plan does not name, its message SHALL also list the files the plan does allow, read from whichever plan is in use (`lockstep.yaml` `layout:` rows or the planned artifacts of `.aes/target.yaml`): those in the refused file's folder first, at most 15, then "and N more".

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: A refusal lists the files the plan allows

- **GIVEN** a plan that names `src/greeter/__init__.py` and PCW_MODE=block
- **WHEN** an agent writes `src/greeter/extra.py`, by an edit or by a shell command
- **THEN** the refusal message lists `src/greeter/__init__.py` under "The plan does allow these files" and no more than 15 paths, with "and N more" for the rest
