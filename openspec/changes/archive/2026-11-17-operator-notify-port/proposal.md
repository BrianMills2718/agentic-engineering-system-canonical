## Why

code2-workspace `scripts/usage_pace.py` (every 6 hours) tells Brian about his Claude weekly usage through Project
Meta's `scripts/operator_notify_router.py`: an `attention` notice is a low-priority ntfy push, a `needs-human` notice
is a desktop toast, a Telegram message and a `waiting:brian` concern, sent once per state. Project Meta is being
retired (AES consolidation plan, row 11, "Before item 11", item 1), and AES `scripts/learning_loop/notify.py` covers
only the Telegram send. The router, its stamp helpers (`notify_operator.py`) and its record
(`operator_notification_record.py`) move here unchanged, beside the concern adapter they already import.

Source: inferred by agent, from the AES consolidation plan row 11 (the ordered ports before the archive yes).

## What Changes

- The three scripts are copied from Project Meta `ee2957b1f`; `notify_operator.py` and
  `operator_notification_record.py` are byte-identical, so the state files (`~/.local/state/operator-notify/<key>.json`,
  `history.log`) and the record (`notifications.jsonl`, `latest.txt`) are the same files with the same format.
- The router's one hard-coded private value, the concern repository (Project Meta), becomes `concern_repo:` under
  `operator_notify:` in the private `graph-config.yaml`; `OPERATOR_CONCERN_REPO` still wins. With neither, the
  concern route fails and says so.
- New `legacy_concern_repos:`: while a listed repository holds an open concern for the key, it is updated (or closed)
  there, so the open Project Meta concern for `usage-pace` (#2713) is not duplicated in AES.
- `waiting_label:` names the needs-human label (default `waiting:brian`).

## Impact

New `scripts/operator_notify_router.py`, `scripts/notify_operator.py`, `scripts/operator_notification_record.py` and
their tests (ported from Project Meta; its audit-escalation tests stay there). `tests/conftest.py` points
`OPERATOR_NOTIFY_RECORD_DIR` at a throwaway folder for the whole suite. Callers switch separately (code2-workspace
`usage_pace.py`). Other Project Meta callers (ecosystem-ops, personal-root FOIA, personal-wiki) are unchanged.
