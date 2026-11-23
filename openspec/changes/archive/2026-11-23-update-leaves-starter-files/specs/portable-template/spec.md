## MODIFIED Requirements

### Requirement: Updating an older copy adds no layout plan

`copier update` of a copy made before the template shipped `lockstep.yaml` SHALL NOT add `lockstep.yaml` and SHALL
leave the copy's starter source files under `src/<package>/` unchanged, while adding or updating the template's other
files.

Source: inferred by agent (cold review finding 1 of docs/planning/template-layout-2026-11-23.md: a plan added to an older copy's existing files would refuse them; `_skip_if_exists` protects only a file that already exists; and the 2026-11-23 advisor finding that an update of a copy made from template `2e8791447` replaced `core.py`'s `Implements:` line with a cog block naming a missing row, failing `lockstep check trace`)

#### Scenario: An update of an older copy keeps it without a plan

- **GIVEN** a committed copy made from template version `2e8791447`, which had no `lockstep.yaml`
- **WHEN** it is updated to the current template
- **THEN** it has no `lockstep.yaml`, its starter source files are unchanged, `lockstep check trace` exits 0 in it,
  and its `AGENTS.md` names `uv run lockstep layout`
