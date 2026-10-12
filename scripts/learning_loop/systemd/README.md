# Feedback loop jobs on Brian's PC (systemd user units)

Four timers run the agent feedback loop. Start page for the whole loop:
[guide.html](../../../proposals/aes-learning-loop/review-page/guide.html).

| Job | When | What it runs | What it writes | If it fails |
|---|---|---|---|---|
| Collector (`feedback-collector`) | daily 03:30 | `collect_feedback.py --file --max-file 10` | `items-<date>.jsonl`, `reports-<date>.jsonl`, `runs.jsonl`, `state.sqlite`; one issue per report in the private log | unit fails, keyed agent concern |
| Weekly analysis (`feedback-problems`) | Sunday 05:00 | `problems.py --file --days 14` | `problems-<date>.jsonl`, `problems-runs.jsonl`, `problems.sqlite`; "Feedback loop: adopt" concerns | unit fails, keyed agent concern |
| Effect counter and rule check (`feedback-effects`) | daily 07:30 | `problems.py --file --days 14 --effects-only`, then `policies.py` | `effects-<date>.jsonl`, `policies-runs.jsonl` | unit fails, keyed agent concern; a rule-check failure does not fail the unit but alerts on its own |
| Fix owner (`feedback-fix-owner`) | daily 09:00 | `fix_owner.py --max-items 10` | `fix-owner-<date>.jsonl` (full session trace), `fix-owner-runs.jsonl` | unit fails, keyed agent concern |

All four run from `~/.hive-brain/aes`, a clone of AES `main` that each run refreshes first
(`~/.hive-brain/project-meta` likewise for project-meta tools), with `llm_client` from
`~/code/llm_client` through uv's shared cache. Every output goes to `$FEEDBACK_OUT` =
`~/projects/data/feedback-collector/`. Never commit anything from that folder: it holds private
transcript quotes. Alerts go through `project-meta/scripts/notify_operator.py`.

The weekly taxonomy refresh that also reads this feedback is agent-skills' `taxonomy-feedback`
timer (Sunday 05:30), not one of these units.

## Install, check, rerun

```bash
# install or reinstall all four after changing these files
cp scripts/learning_loop/systemd/feedback-*.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
for t in collector problems effects fix-owner; do systemctl --user enable --now feedback-$t.timer; done
# one-time setup of the project-meta tools copy
git clone --depth 1 git@github-personal:BrianMills2718/project-meta.git ~/.hive-brain/project-meta

systemctl --user list-timers 'feedback-*'           # next and last run of each
systemctl --user start feedback-collector.service    # run one job now
journalctl --user -u feedback-collector -n 40        # what it printed
python3 scripts/learning_loop/fix_owner.py --dry-run # what the next fix-owner run would hand over
```

## Collector

Reads every Claude Code and Codex session transcript from the last day and turns each closeout
**Feedback** field (and the older **Learnings** heading) into one `feedback-report.v1` report. It
files each report as one issue in the private log `BrianMills2718/agent-feedback-log`
(`--max-reports`, default 80). Filing into the legacy project-meta register is off unless
`--legacy-register` is passed. Exit 1 means some LLM, Jev or filing calls failed; exit 2 means a
crash. Both fail the unit.

- **Human corrections.** Corrections and standing directions Brian gave in a transcript also
  become reports, keeping the literal quote and its byte offset. The last 14 days of item logs are
  backfilled automatically and deduplicated by report id. To recover only that backlog without new
  model calls, run `collect_feedback.py --file --corrections-only`. The private log needs the label
  `source:human`.
- **Subagent results.** The collector reads parent tool events for Codex spawn/followup and Claude
  Agent/Task calls and joins each child's observable result: completion, failure, cancellation or
  a missing result, all unverified. A request to interrupt is not evidence of cancellation. Codex
  child metadata supplies the actual model, effort and instruction hashes when present; unknown
  values stay unknown. A parent can check one exact child return and file it at once:

  ```bash
  python scripts/learning_loop/subagents.py \
    --parent-transcript /path/to/native-parent.jsonl --client codex \
    --call-id CALL_ID --verdict inconclusive \
    --check-argv '["python", "path/to/check_return.py"]' \
    --feedback '- obs (control): parent-checked observation [path/to/evidence.jsonl]' \
    --file
  ```

  The check receives the child return on stdin; its argv, output and exit code are kept. A failed
  checker produces `verification_failed`, not a judgment of the child. A zero exit alone does not
  establish success, so the default disposition is `inconclusive`. Receipts must come from parent
  tool output; child returns and assistant prose cannot supply checks for themselves. Checked
  outcomes keep the original result's time, so a late check cannot turn an old incident into a
  post-enforcement recurrence. Immediate filing needs marked obs/claim/action lines; unmarked notes
  wait for the collector. Boundary: [subagent feedback plan](../../../proposals/aes-subagent-feedback/PLAN.md).
  This captures evidence only; it does not change roles, router choices or model policy. Native
  Codex was exercised live; Claude capture was checked against an existing trace and fixtures.
- **Learning register filing (project-meta entries).** At most 10 entries a night, and only lines
  an agent wrote under its own closeout **Learnings** heading. Lines whose exact text was already
  filed are skipped (`duplicate_of_filed`). Before filing, the light model checks the line against
  lessons filed in the last 14 days (`repeats_filed`); if that check fails the item waits as
  `deferred_repeat_check` instead of being filed unchecked. Entries are written through
  `~/.hive-brain/project-meta`'s `log_learning.py` into `~/code/project-meta/learnings/entries`
  (`--store-path`), because the canonical checkout can be read-only or minutes behind a merge.

Why the filing gate looks like this (hand checks, 2026-10-07): closeout Learnings lines were 8/8
reusable, lines extracted from narration 7/25; Jev's yes/no "reusable?" answer did not separate
them (best 64%), so it is stored as `reusable_p` but does not gate. Ten entries filed through the
gate were 8/10 reusable; the 2 misses were exact repeats, now skipped, and the reworded-repeat check
caught both repeats and flagged none of the 8 distinct entries. **Wrong if** the next 10-entry spot
check falls below 8/10; then drop `--file`.

## Weekly analysis

Groups the last 14 days of reports into problems and decides which fixes are licensed:

1. Jev labels failure families and relations between similar records; a `challenges` answer is
   confirmed by the stronger model.
2. Records linked by `supports` or `same_problem` form a problem. A problem recurs when two
   independent observations among its own `rests_on` records are linked, with references resolved
   before counting. An issue's identity includes its repository; unresolved references stay in the
   report but cannot license a rule.
3. Every recurring problem gets one stronger-model analysis that reads the linked issues (about
   90 s each on the Claude subscription, `claude-code/sonnet`, no per-call charge; the unit sets
   `FEEDBACK_STRONG_MODEL` and starts through a login shell so `claude` is on PATH. Without that
   variable the default is OpenRouter `gpt-5.6-sol`, about 30 s and $0.017 each). An analysis is reused while the problem's records are
   unchanged and saved as soon as it finishes, so a stopped run loses nothing. `--max-analyse N`
   limits a manual run; the timer sets no limit (Brian, 2026-10-12: "i dont get why we would want a
   cap?"). The unit allows 6 hours.
4. The Observation-to-Action evaluator derives licences. Each active licence opens one keyed
   "Feedback loop: adopt ..." concern in AES canonical; high-impact ones are also pushed to Brian
   as information, not a decision.

Brian's ranked view is `VIEW.md` in the private log (impact, then uncertainty).

## Effect counter and rule check

`problems.py --effects-only` reuses the week's analyses and drafts nothing. For every enforced fix
it compares the problem's reports before and after the enforcement receipt; a verified recurrence
after enforcement revokes the licence, persists, and reopens the concern once. Watches survive
report-window expiry and group-id changes.

A fix counts as enforced only with a receipt comment on its issue, written by whoever closes it:

```text
<!-- feedback-enforcement {"enforced_at":"2026-10-08T16:00:00Z","revision":"<exact revision>","verification":"<proof link>"} -->
```

Closing a concern is not enforcement evidence; no receipt means unverified. Times are compared
timezone-aware. An incident at or before enforcement, a later restatement of its evidence, or a
record with an unknown time cannot revoke. This counts reported recurrences; zero reports alone
does not prove a fix worked.

Then `policies.py` checks every rule the workspace AGENTS.md names as Policy `<id>`: a source
entry in WORKING_RULES.md, an entry in the AES rules register (`docs/rules/register.yaml`), and how
many reports named it in 30 days. A rule missing either entry opens the keyed concern
`workspace-policy-unregistered`.

## Fix owner

Hands up to 10 open "Feedback loop: adopt" concerns (oldest first, skipping any deferred in the last
6 days; an attempt that crashed or left no decision is retried next run) to one headless Claude Code
session. Fixes to agent instructions and checks (AGENTS.md, skills, hooks, the Jev gate,
company-planning checks) go first. For each item the session records exactly one
`<!-- fix-owner-disposition {...} -->` comment:

| Disposition | Issue state | Also needs |
|---|---|---|
| `implemented` | closed, completed | enforcement receipt |
| `already_enforced` | closed, completed | enforcement receipt |
| `declined` | closed, not planned | a reason |
| `deferred` | open | the blocker |

The script then reads every handed issue back from GitHub and counts an item as handled only when
its state, close reason, marker and receipt agree; it never trusts the session's own summary. Any
disagreement, or a crash, exits non-zero. Read the trace in `fix-owner-<date>.jsonl` before trusting
a run.

The session starts through a login shell (`bash -lc`), so `claude`, `gh` and `node` must be on the
login PATH; the Safety Net hook runs on node and blocks every tool without it (`~/.profile` adds
nvm's newest node).

Raised from 3 to 10 a day on 2026-10-12, when the uncapped weekly analysis opened 152 fix concerns at
once (3 a day would take about 50 days; the session runs on the Claude subscription). History: until 2026-10-11 nobody worked the adopt concerns (19 open, 1 enforced). Brian approved a
weekly owner on 2026-10-11 and then asked for daily ("i dont want to wait a week"). By 2026-10-12
all 24 adopt concerns were closed and 10 fixes had receipts. **Wrong if**, after four runs, a spot
check finds a merged change that did not do what its item asked, or a `declined` reason that does
not hold up; then stop the timer and go back to hand adoption.
