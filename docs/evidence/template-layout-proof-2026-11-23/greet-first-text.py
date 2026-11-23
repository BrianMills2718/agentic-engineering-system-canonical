"""Greet a person by name.

[[[cog import lockstep.cogtext as c; c.docstring("src:greeter:greet.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: greeting/greet-by-name

### Requirement: Greet by name

The package SHALL greet a person by name: `greet(name)` returns `Hello, <name>!`, and a blank name (empty or only
spaces) raises `ValueError`.

Source: inferred by agent (proof plan for the template layout, AES docs/planning/template-layout-2026-11-23.md step 6)

#### Scenario: A name is greeted

- **GIVEN** the name `Ada`
- **WHEN** `greet("Ada")` is called
- **THEN** it returns `Hello, Ada!`

#### Scenario: A blank name is refused

- **GIVEN** the name `"  "`
- **WHEN** `greet` is called with it
- **THEN** it raises `ValueError`

Tested by: tests/test_greet.py

Declares (typed signatures, from the plan):
  greet(name: str) -> str
[[[end]]] (sum: 2lRHjyCKEQ)
"""