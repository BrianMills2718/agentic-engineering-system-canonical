## ADDED Requirements

### Requirement: The validator can use an installed graph schema

When the operator sets a nonempty `SHIP_TYPED_GRAPH_SCHEMA`, both `ship` and `lockstep plan check` SHALL pass that local path as the value of the Company Planning validator's `--typed-graph-schema` option for the initial check and any freshness retry. An unset or empty variable SHALL leave the option absent so that the selected validator uses its own default. The validator SHALL continue to judge the graph.

Source: Brian, 2026-11-27, AES clean Linux validator goal. Inferred by agent: reuse the upstream CLI option and the existing trusted shell settings for validator dependencies.

#### Scenario: Both validator entry points use the installed graph schema

- **GIVEN** an operator-provisioned schema whose path contains a space and a real package due for a fresh review
- **WHEN** either command runs the validator and retries without the freshness check
- **THEN** both invocations receive the same schema path as one argument
