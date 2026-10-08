# Repair feedback evidence, effects and correction intake

Brian approved this bounded repair on 2026-10-08 after the independent review.
It implements the existing adopted learning-loop plan's evidence and observed
effect requirements; it does not adopt new agent-behavior rules.

The counterexamples were a one-observation fix borrowing its group's three
sightings, equal issue numbers across repositories being treated as one source,
a morning incident counting against an afternoon fix, and direct human corrections
remaining outside the weekly reader.

The repair resolves references before counting, counts support per fix, preserves
repository identity, compares complete timestamps against an explicit enforcement
receipt, retains effect watches and revocations, runs effect observation nightly,
and converts already-extracted human corrections to the existing report model.

Verification is through `tests/learning/`, including the actual collector main
entrypoint's backlog deduplication and the effect observer's group-change and
single-reopen behavior. Model extraction and live deployment are checked separately;
test success alone is not evidence that recurring failures have stopped.

Operator commands and the receipt contract are in
[the service guide](../../scripts/learning_loop/systemd/README.md).

[Feedback types, generalized causes and enforced prevention](feedback-system.svg) maps
problems, control friction, lessons, research, human corrections and skill-use feedback
to their shared improvement targets. A local repair alone is insufficient: the agent
tests the generalized cause, applies prevention at its source, records enforcement
proof and checks recurrence. Separate skill feedback and the legacy taxonomy gap
remain explicit; the tooltip example illustrates a possible cause, not a diagnosis.
