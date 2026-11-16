# feedback-loop-notices Specification

## Purpose

Let the feedback loop file concerns and send its one phone message with code that lives in this repository, so the loop has no dependency on Project Meta (retirement plan, slice 2).

Source: Brian, 2026-11-16 ("i approve", Decision 17 A: the notice goes to Telegram through the existing bot, send call only); Brian, 2026-11-14: Project Meta is legacy and is retired in exchange for AES; Decision 4 (2026-11-16, "i approve"): AES owns concern closure. Inferred by agent: the loop needs only two routes from the old notice router (a keyed concern, and an `attention` phone message).

## Requirements

### Requirement: The loop runs without Project Meta

The feedback loop scripts that file concerns or send notices (`problems.py`, `label_items.py`, `fix_owner.py`, `policies.py`, `alert.py`, `notify.py`; `collect_feedback.py` for notices only) SHALL call only the concern adapter `scripts/concern_issue.py` and the push sender `scripts/learning_loop/notify.py` from this repository. They SHALL NOT call any script under a Project Meta checkout.

#### Scenario: no-project-meta-path

- **WHEN** the loop scripts are read
- **THEN** none of them builds a path to `project-meta/scripts`

### Requirement: A message counts as sent only on Telegram acceptance

`notify.py` SHALL send one Telegram `sendMessage` (plain text) and report it delivered only when Telegram answers HTTP 200 with `ok` true and a `message_id`. It SHALL NOT call `getUpdates` or `deleteWebhook`, because the bot's webhook belongs to another service. With the token or chat id missing, or on any network error or other answer, it SHALL report not delivered, exit non-zero and never raise. It SHALL NOT print the token or chat id.

#### Scenario: attention-push-arrives

- **WHEN** Telegram answers 200 with `ok` true and a `message_id`
- **THEN** the result is delivered with the message id as evidence, only `sendMessage` was called, and the token and chat id do not appear in it

#### Scenario: failed-push-is-not-delivered

- **WHEN** the token or chat id is missing, the network fails, or Telegram answers without `ok` or a `message_id`
- **THEN** the result is not delivered and says why

### Requirement: Loop failures are concerns

When a loop script fails (weekly problems, nightly collector, fix owner) or the policy check finds unregistered rules, it SHALL open or update a keyed concern through `scripts/concern_issue.py` and SHALL NOT call a Project Meta script.

#### Scenario: loop-failures-are-concerns

- **WHEN** `file_alert` is called with a key, source, title and body
- **THEN** it runs the AES concern adapter with `open` for the loop's rule repository, that key and source, and returns the adapter's exit code
