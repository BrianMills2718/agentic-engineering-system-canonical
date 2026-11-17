## ADDED Requirements

### Requirement: agent-work-is-not-needs-you

A waiting issue carrying a label under the optional `agent_labels` setting (label to reason), and not taken by a quiet label or by Broken services, SHALL be shown in an "Agent work" section after Broken services with that reason, and SHALL NOT be counted under Needs you. The issue SHALL be in the run's seen items, so moving into or out of Agent work is neither new nor cleared. Without the setting, Needs you is unchanged.

Source: Brian, 2026-11-16 ("i approve 7 tight": only significant items go to him), applied by the coordinator's Batch A brief of 2026-11-17 (an issue labelled `owner:agent` is not Brian's; sort by label, not by number)

#### Scenario: agent-work-is-not-needs-you

- **WHEN** a waiting issue carries the `owner:agent` label and `agent_labels` names that label
- **THEN** it is listed under Agent work with the reason, Needs you does not count it, and without the setting it stays under Needs you
