## ADDED Requirements

### Requirement: moved-issues-are-matched-by-concern-key

The hub SHALL read each waiting issue's concern key from the `<!-- concern-key: K -->` marker in its body, and SHALL treat it as equivalent to a label or issue reference: an issue whose key is under `quiet_concern_keys` is quiet; an `fyi_rules` entry matches an issue whose key starts with its `concern_key_prefix` (with its title prefix); a `shared_causes` entry gathers issues whose key it lists under `concern_keys`; a failing unit's own issue is also the one whose key is `failed-unit:<unit>`.

Source: Brian, 2026-11-17 (the hub-page brief); the key replaces labels and numbers that a move between repositories drops (observed 2026-11-17, project-meta to code2-workspace)

#### Scenario: moved-issues-are-matched-by-concern-key

- **WHEN** the waiting issues have moved to another repository with no labels, each with its concern key
- **THEN** the records notice is FYI, the usage issue is quiet, the unit's issue and the credit issue are under Broken services, and the records ask with no title prefix stays under Needs you
