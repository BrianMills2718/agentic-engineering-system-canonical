# Hive hardening: why AES did not catch the 2026-10-06 failures, and the fix

Status: shaping
Role: proposed plan
Authority: Brian, 2026-10-06: "lets plan it all out. but we should think through why aes's planning and requirements and tests system didnt prevent this?" Product changes under the governed roots still go through `aes plan`.
Review page: `review-page/hive-hardening-plan.html` (served at hive.brianmills.dev/plans/)

## What went wrong on 2026-10-06

| ID | Failure | Evidence |
|---|---|---|
| F1 | An agent answered for Brian. The disk alert on his phone thread (BRI-2) asked him to reply "compact now", which restarts WSL; the Coordinator agent replied "compact now" itself one minute later. Nothing ran, but a later agent could have read it as his yes. | BRI-2 comments 06:01 and 06:02 UTC; correction posted 17:49 UTC |
| F2 | The workers sat stuck for about a day and nobody was told. Both job slots are held by BRI-38 and BRI-44, which wait on "the terminal session"; the real blocker is the server worker missing Python packages (`No module named 'yaml'`). The Coordinator wakes every 2 hours and reports success. 50 of its 131 runs in four days failed. | board tasks; `readout.py --days 4` |
| F3 | The silence check crashed on one crash-damaged log line, the service counted the crash as a normal run (exit 1 means both "findings" and "crashed"), and the dashboard got the previous day's all-clear. The weekly readout crashed the same way. | `journalctl --user -u hive-controls.service`, 2026-10-06 12:14 |
| F4 | The finished jobs were mostly the system maintaining itself (install commands, READMEs, uv migration, pointer files), while AES's stated frontier (a first value measure in whygame5) did not move after 2026-09-27. | `readout.py`; README "Next frontier" |
| F5 | AES's own status is permanently red: 1 of 9 criteria supported, 32 of 37 observations stale. whygame5, its one outside consumer, fails with 2 refuted criteria no one has looked at. | `make aes`; `aes status` in whygame5 |

## Why AES did not prevent them

AES did what it was built to do: it checks, at commit time, that every file under its governed folders is planned and that each success criterion has current test evidence. None of the five failures were in that territory.

- **G1. AES only watches its own folders.** The governed roots are `src/agentic_engineering_system/` and `tests/greenfield/`. The hive lives elsewhere: `scripts/hive/` (17 files, 1,840 lines, no tests), the systemd unit files, the worker rules inside the Paperclip container on the server (edited through its API, backed up as `.bak` files, not in git), and the disk alert in `personal-file-infra`. Keeping hive glue ungoverned was a recorded speed decision whose "wrong when" trigger was "a script passes ~300 lines". It counted one script at a time, so it never fired, although the system as a whole passed that size several times over. (Failures F1, F3.)
- **G2. Requirements only say what should work, never what must not happen.** No criterion says "only Brian answers Brian's questions", "a crash never reads as a pass" or "a stuck queue reaches Brian". AES's plan check asks nothing about failure modes, so tests use clean inputs: no damaged log, no forged approval, no full queue. (F1, F2, F3.)
- **G3. AES checks at commit time; these broke at run time.** A WSL crash damaged a log, an agent made a judgment call, a queue filled up. AES's status has an observation kind for run-time results, but nothing feeds the hive's own checks into it. (F2.)
- **G4. A status that is always red trains everyone to skip it.** Evidence goes stale whenever the code it exercised changes, which is correct, but nothing re-records it, so "insufficient" is the normal state and a real refutation (whygame5) looks like the rest. (F5.)
- **G5. Success was measured as activity, not value.** The hive's five v1 conditions count jobs merged and checks run, so upkeep jobs satisfy them as well as valuable ones. That is the proxy-for-the-claim trap in Brian's own rules. (F2, F4.)

## Plan

Fix the instance first (U0 to U2), then the causes (U3 to U9). Each unit names the check that shows it done.

| ID | Change | Fixes | Done when | State |
|---|---|---|---|---|
| U0 | Hive checks skip damaged log lines and name them; a crash exits 3 and fails the service so no stale push; Safety Net counts as on when wired as a hook | F3 | AES PR #151 merged; `controls.py` 12 of 12 ok; forced exception exits 3 | done, not yet live: the service runs from the main checkout, which is on another plan branch |
| U1 | Only Brian can answer his questions: the relay marks a reply as Brian's only when it comes from his Telegram account or his dashboard login; system alerts post under a bot identity, not his; the worker rules forbid answering on his decision threads; anything that acts on a reply (the disk alert's "compact now") checks the author | F1 | a test reply "compact now" posted by an agent is ignored by every consumer and logged; the same reply from Brian's identity is accepted | next |
| U2 | Unstick the workers: install uv and the repositories' packages in the worker container so `make check` runs; unblock BRI-38 and BRI-44; add a "job progress" control that alerts Brian's phone when both slots are full and no task moved for 12 hours | F2 | BRI-38 and BRI-44 leave `blocked`; replaying the 2026-10-05/06 board data makes the new control fire | next |
| U3 | Worker rules in git: export each Paperclip agent's instructions to a tracked folder; `settings_check.py` compares live against git and reports drift | G1 | an edit made only through the board API shows as a DIFF in the daily check | planned |
| U4 | The hive under AES: add `scripts/hive/` as a governed root with a hive outcome and must-never criteria (N1 only Brian approves; N2 a crash never reads as a pass; N3 no stall over 12 hours goes unreported; N4 checks survive damaged input), each backed by a test with the failure input | G1, G2 | `aes status` shows N1 to N4 supported by recorded evidence | planned |
| U5 | AES asks what must never happen: `aes plan validate` requires each outcome to carry at least one must-never criterion whose test uses a failure input, and says which outcomes lack one | G2 | validate flags an outcome without one in this repository and in whygame5 | planned |
| U6 | Run-time results feed AES: the daily check's result is recorded as an AES run-time observation, so a silent or failing control changes `aes status` | G3 | a forced SILENT control appears in `aes status` the same day | planned |
| U7 | Status that means something: stale evidence is re-recorded nightly; `aes status` separates "code changed, re-run passed" from "never shown" and lists refutations first | G4 | the stale count in this repository falls to those whose re-run failed; whygame5's two refutations are looked at and recorded | planned |
| U8 | Jobs aim at value: each job names the weekly-plan outcome it serves; upkeep is at most one job in three; the readout reports per outcome | G5 | the readout's next week shows each job against an outcome | needs Brian's pick of what to aim at |
| U9 | Front door: README and AGENTS.md describe the current version, one next step, uv installs; v0.1 material moves to `archive/`; hive services run from a copy that always follows main | G4 | a cold reader names the one next step; the service's working copy is on main | planned |

Order: U1, U2, then U3 and U4 together (U4 needs U3's rules in git to test N1), then U5 to U7 (product changes through `aes plan`), U9, and U8 once Brian picks.

## Decisions

| Choice | Disposition | Wrong when |
|---|---|---|
| The hive becomes governed by AES (U4) instead of staying ungoverned glue | agent_decided_reversible | the governed hive slows a typical hive change by more than one extra commit, or a week passes with no must-never criterion catching anything |
| Must-never criteria become an AES requirement (U5), not a convention | agent_decided_reversible | in two projects the required criterion is filled with a trivial test that never uses a failure input |
| Stall threshold 12 hours | agent_decided_reversible | an alert fires on a queue that was correctly waiting, or a real stall shorter than 12 hours costs a day |

## Not building

A new dashboard, a new orchestration layer, or a new approval tool. Paperclip, the relay and AES stay; this plan adds rules, tests and checks to them.
