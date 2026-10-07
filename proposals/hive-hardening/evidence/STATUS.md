# Hive hardening: unit status (outside the adopted plan's bytes, so the plan need not be re-adopted)

| Unit | Status | Evidence |
|---|---|---|
| U0 | merged (AES #151); not live until the main AES checkout runs main | PR #151 |
| U1 | **live** 2026-10-07 (personal-vps #100, deployed 04:14 UTC). Script and board-key posts on BRI-2 reach Brian's phone and are never relayed as his words; an agent comment under an open question is logged as not his answer (observe mode); Brian's Telegram replies are recognised by his Telegram account | `u1-live-relay-log-2026-10-07.txt`: 04:14:34 board-key question "NOT BRIAN"; 04:15:05 Brian's "Yes" relayed as his; 04:26:29 Coordinator's deliberate "compact now" logged NOT BRIAN'S ANSWER; 04:26:45 Brian's "Done" relayed as his. Replay over all 31 earlier BRI-2 comments: 8 Brian, 3 board-key, the 2026-10-06 06:02 "compact now" logged |
| U2 | **live** 2026-10-07 (personal-vps #101, #102; `hive-stall.timer` hourly) | replay over 2026-10-04..07 board data fires once, 10-06 16:45 UTC (BRI-38, BRI-44 blocked), clears 18:30 (`personal-vps apps/hive-stall/evidence/replay-2026-10-04-to-07.txt`) |
| (unplanned) | Coordinator home task moved from BRI-13 to BRI-61 after a `spawn E2BIG` run failure; cause unconfirmed (personal-vps #104) | personal-vps #103 |
| U3–U7, U9, U10 | U4 waits on the `trace-review-in-plans` claim over `records.py` and `.aes/target.yaml` | — |
