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

## Feedback reports and the weekly loop (plan aes-learning-loop, 2026-10-08)

The nightly collector also turns each closeout **Feedback** field (and the older **Learnings**
heading) into one `feedback-report.v1` report, files it as one issue in the private log
`BrianMills2718/agent-feedback-log` (`--max-reports`, default 80), and writes `reports-<date>.jsonl`.
Filing into the legacy project-meta register is off unless `--legacy-register` is passed.

`feedback-problems.timer` runs `problems.py --file` on Sundays at 05:00: Jev failure families, Jev
relations between similar records (a `challenges` answer is confirmed by the stronger model), problems
grouped from `supports`/`same_problem` relations, recurring = two independent linked observations,
one stronger-model analysis per recurring problem (at most 3 a run) that reads the linked issues,
licences derived by the Observation-to-Action evaluator, active licences opened as keyed concerns in
AES canonical for agents to adopt, high-impact ones also pushed to Brian (`attention`, no decision),
and effects: a verified recurrence after the rule's recorded enforcement revokes its licence. Brian's view:
`VIEW.md` in the private log, ranked by impact then uncertainty. Output: `problems-<date>.jsonl`,
`problems-runs.jsonl`, `effects-<date>.jsonl`, `problems.sqlite` (cache).

```bash
cp scripts/learning_loop/systemd/feedback-problems.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now feedback-problems.timer
```

## Evidence and nightly effects (approved feedback repair, 2026-10-08)

Each fix needs two independent observations among its own `rests_on` records,
with references resolved before counting. An issue's identity includes its
repository. Unresolved references remain in the report but cannot license a rule.

Human corrections and standing directions already found by transcript extraction
also become reports, preserving the literal quote and transcript byte offset.
The last 14 days of item logs are backfilled automatically and deduplicated by
report id. Recover just this backlog with
`collect_feedback.py --file --corrections-only`; it makes no new model calls.
The private log needs the label `source:human`.

`feedback-effects.timer` runs at 07:30 daily, after the collection and weekly
analysis windows. `problems.py --file --effects-only` reuses analyses and does
not draft or hand off proposals. Watches survive report-window expiry and group
identifier changes; revocations persist and reopen the concern only once.

Closing a concern is not enforcement evidence. Before closing it, the adopting
agent adds a comment with the actual time, exact source revision and verification:

```text
<!-- feedback-enforcement {"enforced_at":"2026-10-08T16:00:00Z","revision":"<exact revision>","verification":"<proof link>"} -->
```

Events are compared as timezone-aware timestamps. An incident at or before
enforcement, a later restatement of its evidence, and a record with an unknown
timestamp cannot revoke the rule. No receipt means enforcement is unverified.
This measures reported recurrences; zero reports alone does not prove success.

```bash
cp scripts/learning_loop/systemd/feedback-effects.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now feedback-effects.timer
```

## Native subagent feedback

The collector also reads parent native tool events for Codex spawn/followup and
Claude Agent/Task calls. It joins observable child results, preserving unverified
completion, failure, cancellation and missing dispatch results. A request to
interrupt is not evidence of cancellation. Codex child metadata supplies actual
model/effort and delivered instruction hashes when present; unknown values stay
unknown. This adds reports to the same daily JSONL, state.sqlite and private log.

The parent can execute checks on an exact observed return and file immediately:

```bash
python scripts/learning_loop/subagents.py \
  --parent-transcript /path/to/native-parent.jsonl --client codex \
  --call-id CALL_ID --verdict inconclusive \
  --check-argv '["python", "path/to/check_return.py"]' \
  --feedback '- obs (control): parent-checked observation [path/to/evidence.jsonl]' \
  --file
```

Each check receives the exact child return on stdin; its argv, output and exit
are retained. Choose an interpreter with the check's dependencies. A failed
checker produces `verification_failed`, not a judgment of child quality. Zero
exit alone does not establish task success: the parent's disposition defaults
to `inconclusive`. Checks bind parent, call, child and result digest. The helper
prints a structural receipt the collector can reread from the parent transcript.
Receipts must come from parent tool output; child returns and assistant prose
cannot supply checks for themselves or an earlier assignment.
Checked child outcomes keep the native result's occurrence time, so a delayed
check cannot turn an old incident into a post-enforcement recurrence. Unknown
result times remain unknown. A checker failure is its own event at check time.
Immediate filing requires marked obs/claim/action lines. Unmarked notes retain
the emitted receipt but defer filing to the collector's existing free-text splitter.
Child roles keep their own result contract and need no coordinator closeout.

The [implementation plan and system model](../../../proposals/aes-subagent-feedback/PLAN.md)
define the boundary. This captures evidence; it does not itself alter roles,
router choices or model policy. Weekly generalization and explicit enforced
prevention remain the existing loop's job. Native Codex was exercised live;
Claude capture was checked against an existing native trace and fixtures, not
a new live Claude invocation.
