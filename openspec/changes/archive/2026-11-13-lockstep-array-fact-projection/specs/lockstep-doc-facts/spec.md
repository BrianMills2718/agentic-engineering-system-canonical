## ADDED Requirements

### Requirement: Declared record arrays project as rows

A projection MAY declare `items` as the name of a top-level JSON or YAML array. Its `fields` SHALL include `id` and identify scalar fields in each record. The projector SHALL render one escaped Markdown table row per source record in source order and preserve the source link and markers. Each record SHALL have a distinct nonempty string `id` and each selected field SHALL be a non-null scalar. Missing arrays, invalid records, missing fields and duplicate IDs SHALL fail before any target write. The check and installed refresh paths SHALL apply the same validation and freshness rules as ordinary projections; refresh traces SHALL record selected array facts and source identity.

Source: inferred by agent from Brian's 2026-11-12 request for hooks that keep documentation current and Company Planning's work-unit status records.

#### Scenario: Array facts remain current

- **GIVEN** a declared projection of unit IDs and statuses from a native record array
- **WHEN** a status changes
- **THEN** the read-only check reports stale without writing and refresh updates the matching row in source order

#### Scenario: Invalid array facts fail before writing

- **GIVEN** an array with missing or non-scalar selected fields, invalid or duplicate IDs, or an invalid array
- **WHEN** projection or refresh is requested
- **THEN** it exits 2 and leaves every target unchanged
