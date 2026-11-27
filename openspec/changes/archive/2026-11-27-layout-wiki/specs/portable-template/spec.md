## ADDED Requirements

### Requirement: A fresh copy generates and checks its wiki

A repository made with `copier copy` SHALL set `generated_wiki: true` in its `lockstep.yaml`, hold committed `generated/wiki/` pages written by its `lockstep check project`, and run `lockstep check project --check`, `python -m lockstep.wiki_reach` and `lockstep check docmeta` in its `make check`. Its `AGENTS.md` SHALL tell the agent to read `generated/wiki/index.md` first, and its `docs/index.md` SHALL name that index.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting. Which checks run is inferred by agent.

#### Scenario: A fresh copy has the wiki and checks it

- **GIVEN** the template rendered with its defaults
- **WHEN** its files are read
- **THEN** its `lockstep.yaml` sets `generated_wiki: true`, its Makefile runs `python -m lockstep.wiki_reach` and `lockstep check docmeta`, and its `AGENTS.md` and `docs/index.md` name `generated/wiki/index.md`
