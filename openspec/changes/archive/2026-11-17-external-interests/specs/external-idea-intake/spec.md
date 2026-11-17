## ADDED Requirements

### Requirement: The profile may list interests and the judge treats them like projects

Source: Brian, 2026-11-17: "i approve both recs" (build the interests side of the digest).
The private profile MAY carry an `interests` list whose entries each need a name and a one-line goal. The judge SHALL list interests after
projects, SHALL accept an interest name as a useful post's target, and the useful digest SHALL print projects and interests on separate lines.
A profile without `interests` SHALL behave as before. An interest entry without a name or goal SHALL make the command refuse the profile.

#### Scenario: interests-listed-and-named

- **WHEN** the profile lists one project and one interest and the model calls a post useful to the interest
- **THEN** the prompt contains an Interests section with that interest's goal, and the useful digest shows `Interests: <name>` for the post

#### Scenario: bad-interest-refused

- **WHEN** an interest entry has no goal
- **THEN** the profile is refused with a configuration error naming the entry
