"""Copy the typed signatures the plan declares for a file into its docstring (behavior 3.2).

`aes context` hands each planned artifact with its `exports`: a name for a constant or class,
a full typed signature for a function. They are copied verbatim, one per line, after the plan
text and never wrapped, since a wrapped signature would no longer read as declared. The docstring
renderer (`lockstep.cogtext.render`, behavior 3.1) appends these lines, so `make project`, the
stale-copy check (`pcw check`, the hook) and the plan text the hook hands an agent all carry them.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:signature_text.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/the-plan-is-openspec-plus-layout-rows

### Requirement: The plan is OpenSpec plus layout rows

In a repository whose `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL take the
planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it implements, its tests, optionally
its typed exports), the governed folders from `governed:`, and the requirement text from OpenSpec. A repository with
`.aes/target.yaml` SHALL be read as before.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 2: "Lockstep reads requirements from OpenSpec ... and layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it").

#### Scenario: The layout is laid out with first docstrings

- **GIVEN** a layout row for `src/greeter/__init__.py` implementing `greeting/greet-by-name`, tested by `tests/test_greet.py`
- **WHEN** `lockstep layout` runs
- **THEN** the file is created with a docstring holding its `Implements:` line, the requirement and its scenarios word for word, the test names and its declared signature, and an existing file is left as it is

#### Scenario: An unplanned file is refused against the layout

- **GIVEN** `governed: [src/]` and no row for `src/greeter/extra.py`
- **WHEN** an agent writes that file under `PCW_MODE=block`
- **THEN** the edit hook refuses it and names `lockstep.yaml` as where the file must be planned

#### Scenario: A planned file's edit hands over its requirement

- **GIVEN** a laid-out planned file
- **WHEN** an agent edits it
- **THEN** the edit is allowed and the agent is handed the OpenSpec requirement text

#### Scenario: The whole-tree check reads the layout

- **GIVEN** a laid-out, committed layout repository
- **WHEN** `lockstep check` runs, and again after an unplanned file is added under `src/`
- **THEN** the first allows and the second blocks with that file as `unplanned`

#### Scenario: A layout row must name real requirements

- **GIVEN** a row whose `implements` names a requirement no spec defines, and a row with no purpose
- **WHEN** the layout is checked
- **THEN** both are reported, naming the row's path

#### Scenario: An AES plan is still read

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** Lockstep reads its plan
- **THEN** the planned files come from `.aes/target.yaml` exactly as before
[[[end]]]
"""

from __future__ import annotations


def signature_lines(ctx: dict) -> list[str]:
    """The "Declares:" lines for the exports of the artifact an `aes context` is about; empty when it has none."""
    subject = ctx.get("subject") or {}
    exports = [str(e).strip() for e in subject.get("exports") or [] if str(e).strip()]
    if not exports:
        return []
    if any('"""' in e or "\\" in e for e in exports):
        raise ValueError(f"{subject.get('id')}: an export holds a triple quote or a backslash, "
                         "which cannot be copied into a docstring verbatim")
    return ["Declares (typed signatures, from the plan):", *(f"  {e}" for e in exports)]
