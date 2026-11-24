## ADDED Requirements

### Requirement: A fixed planned file without a plan copy is reported

`lockstep check project`, with or without `--check`, SHALL print `no-copy <path>` for each `layout:` row whose path
matches a `fixed:` glob in `lockstep.yaml`, names an existing Python file, and whose file holds no cog plan copy
naming that row's ID, and SHALL then exit 1. A row outside every `fixed:` glob SHALL NOT be reported.

Source: Brian, 2026-11-23: "i approve", to Q53 in `docs/planning/open-questions.json` ("Should `make check` fail
when a docstring's plan copy is stale or a `fixed:` file has no copy block?"; alignment cleanup item 14).

#### Scenario: A fixed file with no plan copy fails the check

- **GIVEN** `fixed: ["src/greeter/*"]` and a layout row for `src/greeter/__init__.py` whose file has a docstring with no cog plan copy
- **WHEN** `lockstep check project --check` runs
- **THEN** it prints `no-copy src/greeter/__init__.py` and exits 1, and once the file holds the copy that `lockstep layout` writes it reports nothing for that file
