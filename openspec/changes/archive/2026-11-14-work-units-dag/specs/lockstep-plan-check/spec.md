## ADDED Requirements

### Requirement: Work units form a checked DAG

Source: Brian, 2026-11-14: "we should always have a dag as part of the plans so we can optimally parallelize and stay on track"; approved with "i apporve your recs".

`lockstep plan units` SHALL read `docs/planning/work-units.json` (record type `work_units`, a list `units`) and exit 1, naming each problem, unless: each unit has a unique `id`, a `title`, a `depends_on` list of existing unit ids (empty means it can start now), a `touches` list of repository paths, and a `status` of `planned`, `in progress` or `merged`; a `merged` unit has `evidence`; and the dependencies contain no cycle. It SHALL print the units that are ready (not merged, every dependency merged), the longest chain of unmerged units, and each pair of unmerged units with no dependency path between them whose `touches` overlap. It exits 2 when the file is missing or not JSON. `lockstep plan check` SHALL report the same problems when the file is present.

#### Scenario: Independent units are both ready

- **GIVEN** units A and B with empty `depends_on` and different `touches`
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 0 and lists both as ready

#### Scenario: A cycle fails

- **GIVEN** unit A depending on B and B depending on A
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 and names the cycle

#### Scenario: A dependency on a missing unit fails

- **GIVEN** a unit whose `depends_on` names an id no unit has
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 and names the unit and the missing id

#### Scenario: Independent units touching one file are flagged

- **GIVEN** unready-to-merge units A and B with no path between them that both touch `src/x.py`
- **WHEN** `lockstep plan units` runs
- **THEN** it reports the conflict naming both units and the file

#### Scenario: A merged unit needs evidence

- **GIVEN** a `merged` unit without `evidence`
- **WHEN** `lockstep plan units` runs
- **THEN** it exits 1 naming the unit
