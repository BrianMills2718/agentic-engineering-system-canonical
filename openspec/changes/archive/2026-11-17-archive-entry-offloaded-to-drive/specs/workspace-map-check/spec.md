## ADDED Requirements

### Requirement: offloaded-archive-entry-is-not-gone

An `archive_map_registry.yaml` entry whose folder is absent from `~/archive` SHALL be reported as gone unless the
entry names, in `offloaded:`, the exact Google Drive tar (a path ending in `.tar.gz`) that holds the folder.
Source: inferred by agent from Brian's 2026-11-17 request to correct the archive registry's missing bare mirrors.

#### Scenario: offloaded-archive-entry-is-not-gone

- **WHEN** a registry entry's folder is absent from `~/archive` and the entry names `offloaded: google_brian:Data/90_Archive/offloaded/archive/202610/x-20261008T000000Z.tar.gz`
- **THEN** the check reports no "gone" finding for it, while an absent entry with no `offloaded:` is still reported as gone
