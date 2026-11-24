## ADDED Requirements

### Requirement: Old-route checks stay while a repository runs them

For a repository with `.aes/target.yaml`, Lockstep SHALL keep the checks that plan route uses, each runnable as
`python -m lockstep.<name>` and `python -m pcw.<name>`: `action_check`, `behavior_check`, `change_list`,
`change_log`, `criterion_checks`, `declared_reason`, `docstring_up`, `linked_tests`, `plan_edit`, `plan_to_code`,
`requirement_status`, `unplanned_symbols`, `wiki` and `wiki_reach`. One SHALL be retired, with a dated record under
`docs/retired/`, only once no repository in `~/code2` runs it (code2-workspace decision 0009: `.aes/target.yaml`
retires one repository at a time).

Source: Brian, 2026-11-23: "i approve", to Q54 in `docs/planning/open-questions.json` ("write one requirement for
the ones the core calls; retire the rest"); the 2026-11-23 search found all 14 still run, so none retired (inferred by
agent from that search).

#### Scenario: An AES-plan repository's checks still run

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** its Makefile or edit hook runs one of the 14 checks
- **THEN** the check runs as before, as each module's own tests show
