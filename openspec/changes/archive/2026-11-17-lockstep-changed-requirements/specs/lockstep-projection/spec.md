## MODIFIED Requirements

### Requirement: A plan closes requirement ids only when they pass

`lockstep status` SHALL read the `Closes:` line of each plan and OpenSpec change and report each listed ID that is unimplemented, untested or not passing as open for that plan. It SHALL give a requirement or scenario the state `changed, not archived` when an active change's spec delta holds text for it that differs from the spec's (runs of whitespace counting as one space), whatever its tests' results, and SHALL report it as open for a plan that lists it.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows). The `changed, not archived` state: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then ... the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842); its name and rule are inferred by agent.

#### Scenario: Open ids of a plan are listed

- **GIVEN** a plan closing an ID that fails and an ID that does not exist
- **WHEN** `lockstep status` runs
- **THEN** both are listed as open with their state

#### Scenario: A requirement reworded in an active change is open, not passing

- **GIVEN** a requirement with an implementer and a passing test, and an active change whose spec delta gives it a different statement and whose proposal lists it on its `Closes:` line
- **WHEN** `lockstep status` runs
- **THEN** the requirement's state is `changed, not archived` and the plan lists it as open
