# feedback-loop-notices Specification

## Purpose

Let the feedback loop file concerns and send its one phone push with code that lives in this repository, so the loop has no dependency on Project Meta (retirement plan, slice 2).

Source: Brian, 2026-11-14: Project Meta is legacy and is retired in exchange for AES; Decision 4 (2026-11-16, "i approve"): AES owns concern closure. Inferred by agent: the loop needs only two routes from the old notice router (a keyed concern, and an `attention` phone push).

## Requirements

### Requirement: The loop runs without Project Meta

The feedback loop scripts (`problems.py`, `label_items.py`) SHALL call only the concern adapter `scripts/concern_issue.py` and the push sender `scripts/learning_loop/notify.py` from this repository. They SHALL NOT call any script under a Project Meta checkout.

#### Scenario: no-project-meta-path

- **WHEN** the loop scripts are read
- **THEN** none of them builds a path to `project-meta/scripts`

### Requirement: A push counts as sent only on broker acceptance

`notify.py` SHALL report a push as delivered only when ntfy answers HTTP 200 with a JSON `id`. With no topic configured, or on any network error or other answer, it SHALL report not delivered, exit non-zero and never raise. It SHALL NOT print the topic.

#### Scenario: attention-push-arrives

- **WHEN** ntfy answers 200 with an `id`
- **THEN** the result is delivered with the id as evidence, and the topic does not appear in it

#### Scenario: failed-push-is-not-delivered

- **WHEN** no topic is configured, the network fails, or ntfy answers 200 without an `id`
- **THEN** the result is not delivered and says why

### Requirement: Loop failures are concerns

When a loop script fails (weekly problems, nightly collector, fix owner) or the policy check finds unregistered rules, it SHALL open or update a keyed concern through `scripts/concern_issue.py` and SHALL NOT call a Project Meta script.

#### Scenario: loop-failures-are-concerns

- **WHEN** `file_alert` is called with a key, source, title and body
- **THEN** it runs the AES concern adapter with `open` for the loop's rule repository, that key and source, and returns the adapter's exit code
