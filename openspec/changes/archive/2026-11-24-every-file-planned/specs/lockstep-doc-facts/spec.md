## MODIFIED Requirements

### Requirement: Declared record arrays project as rows

A projection MAY declare `items` as the name of a top-level JSON or YAML array. It MAY declare `key`, the name of the field that identifies each record (default `id`). It MAY declare `link`, one of its fields whose values are repository-relative paths; that column SHALL render as a relative Markdown link from the target to the path, and a path that is absolute or climbs out with `..` SHALL fail. Its `fields` SHALL include that key and identify scalar fields in each record. The projector SHALL render one escaped Markdown table row per source record in source order and preserve the source link and markers. Each record SHALL have a distinct nonempty string key and each selected field SHALL be a non-null scalar. Missing arrays, invalid records, missing fields and duplicate keys SHALL fail before any target write. The check and installed refresh paths SHALL apply the same validation and freshness rules as ordinary projections; refresh traces SHALL record selected array facts and source identity.

Source: inferred by agent from Brian's 2026-11-12 request for hooks that keep documentation current and Company Planning's work-unit status records.  The optional `key` and `link` are inferred by agent, so `lockstep.yaml` layout rows (keyed by `path`) can project (change every-file-planned, 2026-11-24).

#### Scenario: Array facts remain current

- **GIVEN** a declared projection of unit IDs and statuses from a native record array
- **WHEN** a status changes
- **THEN** the read-only check reports stale without writing and refresh updates the matching row in source order

#### Scenario: A record array keyed by another field projects

- **GIVEN** a projection with `key: path` and `link: path` over records that have `path` and `purpose` and no `id`
- **WHEN** projection runs
- **THEN** one row per record is written in source order with each path a relative link, and a duplicate `path` or a path climbing out with `..` exits 2 without writing

#### Scenario: Invalid array facts fail before writing

- **GIVEN** an array with missing or non-scalar selected fields, invalid or duplicate IDs, or an invalid array
- **WHEN** projection or refresh is requested
- **THEN** it exits 2 and leaves every target unchanged
