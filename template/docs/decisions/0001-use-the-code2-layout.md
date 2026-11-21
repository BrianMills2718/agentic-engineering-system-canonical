# Use the code2 repository layout

- Status: accepted
- Source: Brian, 2026-10-15: "yes lets make sure that our plans and docuemtnation for code2 dogfood what we are going to requrie repos/proejcts in code2 to comply with"
- Date: made from the code2 copier template in agentic-engineering-system-canonical

## Context and problem statement

Plans, diagrams and code drift apart unless something checks them against each other.

## Decision outcome

Chosen: the code2 layout from the template in `agentic-engineering-system-canonical`. Behavior is planned in OpenSpec, structure in a
LikeC4 diagram, decisions in MADR files like this one, and the code reference is generated from
docstrings. `lockstep check` fails a commit whose code, tests or imports drift from that plan. The
reasons and the options considered are in that repository's decision 0015
(`docs/decisions/0015-off-the-shelf-documentation-stack.md`).

### Consequences

- Good: a reader or agent finds every document from `docs/index.md`, and the checks keep them true.
- Bad: each requirement and scenario needs an ID written in code and tests.
