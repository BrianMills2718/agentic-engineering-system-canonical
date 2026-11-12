# greeting Specification

## Purpose

Greet a person by name.

## Requirements

### Requirement: Greet by name

Source: inferred by agent, the smallest example for Lockstep's layout plan.

`greet(name)` SHALL return `Hello, <name>!`.

#### Scenario: A name is greeted

- **GIVEN** the name `Ada`
- **WHEN** `greet` is called with it
- **THEN** it returns `Hello, Ada!`
