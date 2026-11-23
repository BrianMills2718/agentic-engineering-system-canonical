## ADDED Requirements

### Requirement: Trace: Comment lines in configured files implement requirements

The trace check SHALL also read `Implements:` lines in the files, and the files under the folders, listed in
`[tool.lockstep] comment_sources` in `pyproject.toml`: a line whose text, after optional leading space and a
comment opener (`#`, `{#`, `//` or `<!--`), starts with `Implements:`, naming one or more IDs separated by
commas, with any closing `#}` or `-->` removed. A line with no comment opener (such as a docstring line in a `.py.jinja` file) is not read. With no
`comment_sources`, no such file is read.

Source: Brian, 2026-11-23: "i approve", item (c) of `docs/planning/back-on-design-2026-11-23.md`; open question Q50
in `docs/planning/open-questions.json` (recommendation "Yes, for configured paths only").

#### Scenario: Trace: A Jinja comment in a configured folder implements a requirement

- **GIVEN** `comment_sources = ["template"]` and `template/Makefile.jinja` holding `{# Implements: core/do-the-thing #}`
- **WHEN** the trace check runs
- **THEN** it reports no unimplemented finding for `core/do-the-thing`

#### Scenario: Trace: A docstring line in a configured folder is not read

- **GIVEN** `comment_sources = ["template"]` and `template/core.py.jinja` whose docstring says `Implements: other/unknown`
- **WHEN** the trace check runs
- **THEN** it reports no finding for `other/unknown`

#### Scenario: Trace: An unconfigured file is not read

- **GIVEN** no `comment_sources` and `copier.yml` holding `# Implements: core/do-the-thing`
- **WHEN** the trace check runs
- **THEN** it reports `core/do-the-thing` as unimplemented
