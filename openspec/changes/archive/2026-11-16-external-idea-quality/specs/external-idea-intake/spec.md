# external-idea-intake Specification

## ADDED Requirements

### Requirement: Posts already assessed into raw sources are never offered again

The command SHALL treat every Reddit post whose capture folder exists in `raw/sources/` (named `<date>-reddit-<id>-<slug>`) as already seen.

#### Scenario: already-assessed-dropped

- **WHEN** a listing holds a post whose id matches a `raw/sources` capture folder
- **THEN** it appears in neither digest
