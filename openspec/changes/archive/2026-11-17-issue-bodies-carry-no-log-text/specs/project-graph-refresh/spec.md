## ADDED Requirements

### Requirement: concern-body-carries-first-lines-and-log-path

The concern body SHALL carry the first line of each problem and the path of the day's log, each passed through
`public_text.redact`, and SHALL NOT carry a step's output beyond that first line.

Source: Brian, 2026-11-17: "make AES's own public issue bodies carry only the first error line and a pointer to the private log path ... and redact home paths/addresses."

#### Scenario: concern-body-carries-first-lines-and-log-path

- **WHEN** a step fails with three lines of output, the second naming a path under the home folder
- **THEN** the body holds the first line and the log path written from `~`, and not the second line
