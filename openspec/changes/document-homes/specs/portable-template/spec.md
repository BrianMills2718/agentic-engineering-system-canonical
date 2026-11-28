## ADDED Requirements

### Requirement: A fresh copy declares where each kind of document lives

A fresh copy of the template SHALL declare `document_homes:` in its `lockstep.yaml` (design in `docs/architecture/`,
decisions in `docs/decisions/`, requirements and change proposals in `openspec/`, research in `research/`, retained
observations in `evidence/`, generator output in `generated/` and the documentation site's generated copies, and its
front pages), ship `research/README.md` saying what belongs there, and list the homes in its AGENTS.md, so that its
own `make check` reports no misplaced document when it is created.

Source: Brian, 2026-11-27 18:51 and 19:05 (see the proposal). The homes are the concern roots of wiki_methodology
`docs/architecture/REPOSITORY_CONCERN_ROOTS.md` at 0cddc6b1d, which AES adopts (`.agentic/repo.yaml`); choosing only
the ones a fresh copy uses on day one is inferred by agent.

#### Scenario: A fresh copy has its homes and no misplaced document

- **GIVEN** a fresh copy of the template
- **WHEN** its layout is checked
- **THEN** `lockstep.yaml` declares `research/` and `generated/` among its homes, `research/README.md` exists, and no
  document is reported outside its home
