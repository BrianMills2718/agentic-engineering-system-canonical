## Why

code2-workspace `scripts/needs_you_push.py` (every 5 minutes) sends each new `waiting:brian` issue to Brian's Telegram
through Project Meta's `operator_notify_router.deliver_telegram`. Project Meta is being retired (AES consolidation plan,
row 11, "Before item 11", item 2), so the push moves onto this repository's `scripts/learning_loop/notify.py`. The old
sender turned off Telegram's link preview card and reported the message id and Telegram's error description; the push
body is a GitHub link, so without these Brian's phone would show a preview card and the push's state file would lose
its message id.

Source: inferred by agent, from the AES consolidation plan row 11 (the ordered ports before the archive yes).

## What Changes

- `push()` takes `no_preview` (off by default, so the loop's own alerts are unchanged) and sends
  `disable_web_page_preview: true` when it is set.
- A delivered result also carries `message_id`; an HTTP error carries Telegram's `description`, token removed.

## Impact

`scripts/learning_loop/notify.py`, `tests/test_feedback_loop_notices.py`. The loop's existing calls send the same body
as before.
