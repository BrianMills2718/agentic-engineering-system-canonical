# Feedback collector on Brian's PC (systemd user units)

`feedback-collector.timer` runs `feedback-collector.service` nightly at 03:30.
The service runs `scripts/learning_loop/collect_feedback.py --file` from the
same refreshed clone of AES `main` as `hive-controls` (`~/.hive-brain/aes`),
with `llm_client` from `~/code/llm_client` through uv's shared cache. Output:
`~/projects/data/feedback-collector/` (`items-<date>.jsonl`, `runs.jsonl`,
`state.sqlite`). Never commit anything from that folder: it holds private
transcript quotes.

Install, or reinstall after changing these files:

```bash
cp scripts/learning_loop/systemd/feedback-collector.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now feedback-collector.timer
systemctl --user start feedback-collector.service   # one run now; then: journalctl --user -u feedback-collector -n 40
```

Exit 1 (some LLM, Jev or filing calls failed) and 2 (crash) fail the unit and
open a keyed agent concern through `project-meta/scripts/notify_operator.py`.

## Filing gate (2026-10-07)

The timer files at most 10 entries a night, and only lines an agent wrote under its own closeout
**Learnings** heading. Hand check of the first night's 33 filed entries: those lines were 8/8 reusable;
items the light LLM extracted from session narration were 7/25, and Jev's yes/no "reusable?" answer did
not separate them (best 64%), so it is recorded on each item as `reusable_p` but does not gate. A line
whose text was already filed is skipped (`duplicate_of_filed`). Hand check of 10 entries filed through
this gate on 2026-10-07: 8/10 reusable and correctly typed; the 2 failures were exact repeats, which the
duplicate skip now removes. Everything else stays in the daily log. Wrong if the next 10-entry spot check
falls below 8/10; then turn filing off again (drop `--file`).

## project-meta tools copy (2026-10-07)

The collector runs `log_learning.py` from `~/.hive-brain/project-meta`, which the service refreshes to
origin/main before each run, and writes entries to `~/code/project-meta/learnings/entries` through
`--store-path`. The canonical checkout is read-only while any lane claims it, and canonical-sync refreshes it only about every 17 minutes, so right after a merge it can lack a fix the collector needs. Set up once:
`git clone --depth 1 git@github-personal:BrianMills2718/project-meta.git ~/.hive-brain/project-meta`.

## Reworded repeats (2026-10-07)

Exact-text dedup let 2 of 10 filed entries through as reworded repeats (independent Gemini grade).
Before filing, the light extraction model now checks the line against lessons filed in the last 14
days (`repeats_filed`); a repeat is logged as `repeats_filed`, and if the check itself fails the item
waits as `deferred_repeat_check` for the next run rather than being filed unchecked. On the graded set
the prompt caught both repeats and flagged none of the 8 distinct entries (9/9).
