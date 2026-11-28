## ADDED Requirements

### Requirement: A document outside its home is reported

When `lockstep.yaml` declares `document_homes:` (a mapping from a folder ending in `/`, or a file path, to what
belongs there), Lockstep SHALL report, as a layout problem, every tracked Markdown file that sits under no declared
home, naming the file and listing the homes. `README.md`, `AGENTS.md` and `CLAUDE.md` anywhere (any letter case), files under a
hidden folder or a `tests/` folder, and a file a layout row names are not reported. A home written without its
trailing `/` that names a folder holds that folder. A `lockstep.yaml` without `document_homes:` is not
checked.

Source: Brian, 2026-11-27 19:05: "like research goes in one place. generated files go in another". The closed list
(a document must sit in a declared home, rather than its kind being guessed from its name) is inferred by agent: a
document's kind cannot be read from its path, and prose meaning is not inferred with patterns.

#### Scenario: A note outside every home is reported

- **GIVEN** `document_homes:` declaring `research/` and `docs/architecture/`, and a committed `docs/notes.md`
- **WHEN** the layout is checked
- **THEN** the problem names `docs/notes.md` and lists `research/` and `docs/architecture/`; moved to
  `research/notes.md`, it is not reported, and without `document_homes:` nothing is reported
