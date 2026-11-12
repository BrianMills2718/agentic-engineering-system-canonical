---
type: SystemModel
title: The feedback loop
description: What the kept, running part of AES does, job by job, with what it reads and writes and when it runs.
status: current
updated: 2026-11-11
sources: [scripts/learning_loop/systemd/README.md, scripts/learning_loop/systemd/feedback-collector.service, scripts/learning_loop/systemd/feedback-collector.timer, scripts/learning_loop/systemd/feedback-labels.service, scripts/learning_loop/systemd/feedback-labels.timer, scripts/learning_loop/systemd/feedback-problems.service, scripts/learning_loop/systemd/feedback-problems.timer, scripts/learning_loop/systemd/feedback-effects.service, scripts/learning_loop/systemd/feedback-effects.timer, scripts/learning_loop/systemd/feedback-fix-owner.service, scripts/learning_loop/systemd/feedback-fix-owner.timer, scripts/learning_loop/collect_feedback.py, scripts/learning_loop/feedback_log.py, scripts/learning_loop/records.py, scripts/learning_loop/label_items.py, scripts/learning_loop/problems.py, scripts/learning_loop/licences.py, scripts/learning_loop/effects.py, scripts/learning_loop/policies.py, scripts/learning_loop/fix_owner.py, scripts/learning_loop/subagents.py, proposals/aes-learning-loop/DESIGN.md, proposals/aes-learning-loop/PLAN.md, proposals/aes-learning-loop/REPAIR.md, proposals/aes-feedback-prevention/PLAN.md, proposals/aes-subagent-feedback/PLAN.md, datasets/learning-loop/README.md]
---

# The feedback loop

Decision 0009 keeps the feedback loop: `collect_feedback.py`, `label_items.py` and `feedback_log.py` stay and keep running. [docs/decisions/0009-aes-and-lockstep-fate.md:59-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L59-L61)
Why it exists: Brian's earlier systems recorded lessons well and almost never closed the loop (2,572 learnings with 4 resolutions). [proposals/aes-learning-loop/DESIGN.md:22-25](../proposals/aes-learning-loop/DESIGN.md#L22-L25)
Its goal: every lesson, friction, problem, experiment and finding becomes a short report whose claims link to evidence; the loop sorts the reports, analyses recurring problems, turns licensed claims into enforced rules and observes whether the failure recurs. [proposals/aes-learning-loop/PLAN.md:9](../proposals/aes-learning-loop/PLAN.md#L9)
Brian observes a view ranked by impact and uncertainty and is notified; agents adopt and retire rules by their own judgment. [proposals/aes-learning-loop/PLAN.md:23-25](../proposals/aes-learning-loop/PLAN.md#L23-L25)
- [Goal](goal.md) (related page)
- [Policy and rules](policy-and-rules.md) (related page)

## What runs, and when

Two timers run today, the collector and the labels job; the problems, effects and fix-owner timers are installed but disabled and inactive (checked 2026-11-10). [scripts/learning_loop/systemd/README.md:3-7](../scripts/learning_loop/systemd/README.md#L3-L7)
Git history does not record who turned the three off or why. [scripts/learning_loop/systemd/README.md:9-10](../scripts/learning_loop/systemd/README.md#L9-L10)

| Job | When | Command | Writes | State | Source |
| --- | --- | --- | --- | --- | --- |
| Collector (`feedback-collector`) | daily 03:30 | `collect_feedback.py --file --max-file 10` | `items-<date>.jsonl`, `reports-<date>.jsonl`, `runs.jsonl`, `state.sqlite`; one issue per report in the private log | on | [scripts/learning_loop/systemd/feedback-collector.timer:5](../scripts/learning_loop/systemd/feedback-collector.timer#L5) [scripts/learning_loop/systemd/feedback-collector.service:20](../scripts/learning_loop/systemd/feedback-collector.service#L20) [scripts/learning_loop/systemd/README.md:16](../scripts/learning_loop/systemd/README.md#L16) |
| Labels (`feedback-labels`) | daily 05:00 | `label_items.py issues --other-concern-repo BrianMills2718/agent-skills` | a `family:<letter>`, `fact` or `other` label and a comment on each open feedback issue; `labels-<date>.log` | on | [scripts/learning_loop/systemd/feedback-labels.timer:5](../scripts/learning_loop/systemd/feedback-labels.timer#L5) [scripts/learning_loop/systemd/feedback-labels.service:17](../scripts/learning_loop/systemd/feedback-labels.service#L17) [scripts/learning_loop/systemd/README.md:20](../scripts/learning_loop/systemd/README.md#L20) |
| Weekly analysis (`feedback-problems`) | Sunday 05:00 when on | `problems.py --file --days 14` | `problems-<date>.jsonl`, `problems-runs.jsonl`, `problems.sqlite`; "Feedback loop: adopt" concerns | off | [scripts/learning_loop/systemd/feedback-problems.timer:5](../scripts/learning_loop/systemd/feedback-problems.timer#L5) [scripts/learning_loop/systemd/feedback-problems.service:23](../scripts/learning_loop/systemd/feedback-problems.service#L23) [scripts/learning_loop/systemd/README.md:17](../scripts/learning_loop/systemd/README.md#L17) |
| Effect counter and rule check (`feedback-effects`) | daily 07:30 when on | `problems.py --file --days 14 --effects-only`, then `policies.py` | `effects-<date>.jsonl`, `policies-runs.jsonl` | off | [scripts/learning_loop/systemd/feedback-effects.timer:5](../scripts/learning_loop/systemd/feedback-effects.timer#L5) [scripts/learning_loop/systemd/feedback-effects.service:10-12](../scripts/learning_loop/systemd/feedback-effects.service#L10-L12) [scripts/learning_loop/systemd/README.md:18](../scripts/learning_loop/systemd/README.md#L18) |
| Fix owner (`feedback-fix-owner`) | daily 09:00 when on | `fix_owner.py --max-items 10` | `fix-owner-<date>.jsonl`, `fix-owner-runs.jsonl` | off | [scripts/learning_loop/systemd/feedback-fix-owner.timer:5](../scripts/learning_loop/systemd/feedback-fix-owner.timer#L5) [scripts/learning_loop/systemd/feedback-fix-owner.service:17](../scripts/learning_loop/systemd/feedback-fix-owner.service#L17) [scripts/learning_loop/systemd/README.md:19](../scripts/learning_loop/systemd/README.md#L19) |

## Where the jobs run

- Every job runs from `~/.hive-brain/aes`, a clone of AES `main` that each run resets to `origin/main` under `flock` before starting. [scripts/learning_loop/systemd/feedback-collector.service:7-14](../scripts/learning_loop/systemd/feedback-collector.service#L7-L14)
- A git lock older than an hour in those clones is deleted first, because a stale lock stopped the collector from 2026-10-17 to 2026-10-26. [scripts/learning_loop/systemd/feedback-collector.service:10-12](../scripts/learning_loop/systemd/feedback-collector.service#L10-L12) [scripts/learning_loop/systemd/README.md:30-32](../scripts/learning_loop/systemd/README.md#L30-L32)
- `llm_client` comes from `~/code/llm_client` through uv's shared cache. [scripts/learning_loop/systemd/feedback-collector.service:18-20](../scripts/learning_loop/systemd/feedback-collector.service#L18-L20)
- Outputs go to `$FEEDBACK_OUT` = `~/projects/data/feedback-collector/`; nothing from that folder is ever committed, because it holds private transcript quotes. [scripts/learning_loop/systemd/README.md:24-26](../scripts/learning_loop/systemd/README.md#L24-L26)
- Failures open a keyed agent concern through project-meta `scripts/notify_operator.py`. [scripts/learning_loop/systemd/README.md:26](../scripts/learning_loop/systemd/README.md#L26)

## Collector

- It reads the new bytes of every Claude Code and Codex transcript changed since the last run, resuming from byte offsets in `state.sqlite`. [scripts/learning_loop/collect_feedback.py:11-12](../scripts/learning_loop/collect_feedback.py#L11-L12)
- It parses closeout fields under fixed bold headings with code, and extracts Brian's corrections, friction and in-passing learnings with the light model; a quote not found verbatim is dropped. [scripts/learning_loop/collect_feedback.py:13-16](../scripts/learning_loop/collect_feedback.py#L13-L16)
- Jev triages each item as learning, friction, correction, concern or noise; the "already covered" check is an annotation only and drops nothing. [scripts/learning_loop/collect_feedback.py:17-21](../scripts/learning_loop/collect_feedback.py#L17-L21)
- Filing into the legacy project-meta register is off since 2026-10-08 unless `--legacy-register` is passed. [scripts/learning_loop/collect_feedback.py:23-26](../scripts/learning_loop/collect_feedback.py#L23-L26)
- Each closeout Feedback (or older Learnings) field becomes one `feedback-report.v1` report, filed as one issue in the private log. [scripts/learning_loop/collect_feedback.py:27-31](../scripts/learning_loop/collect_feedback.py#L27-L31)
- The private log defaults to `BrianMills2718/agent-feedback-log`, and free text is split by `deepseek-v4-flash`. [scripts/learning_loop/feedback_log.py:24-26](../scripts/learning_loop/feedback_log.py#L24-L26)
- Exit 0 is clean, 1 means some calls failed (re-read next run), 2 means a crash; any non-zero exit opens a keyed agent concern. [scripts/learning_loop/collect_feedback.py:33-36](../scripts/learning_loop/collect_feedback.py#L33-L36)
- Report filing is capped at 900 a night (`--max-reports`) and paced at 450 an hour, raised from 80 on 2026-11-10. [scripts/learning_loop/systemd/README.md:55-58](../scripts/learning_loop/systemd/README.md#L55-L58)
- Human corrections become reports too, keeping the literal quote and byte offset, with a 14-day backfill deduplicated by report id and then by quote. [scripts/learning_loop/systemd/README.md:62-66](../scripts/learning_loop/systemd/README.md#L62-L66)
- Subagent spawn and result events from both clients become reports; a completion is unverified until a parent check binds it, and a failed checker records `verification_failed`, not a judgment of the child. [scripts/learning_loop/systemd/README.md:69-73](../scripts/learning_loop/systemd/README.md#L69-L73) [scripts/learning_loop/systemd/README.md:84-86](../scripts/learning_loop/systemd/README.md#L84-L86)
- This subagent capture records evidence only; it changes no role, router choice or model policy. [scripts/learning_loop/systemd/README.md:91-92](../scripts/learning_loop/systemd/README.md#L91-L92)
- Learning-register filing takes at most 10 entries a night, only from an agent's own Learnings heading, skipping exact repeats and checking reworded repeats first. [scripts/learning_loop/systemd/README.md:93-100](../scripts/learning_loop/systemd/README.md#L93-L100)
- Why that gate: Learnings lines were 8/8 reusable against 7/25 for extracted narration, and the gate is wrong if the next 10-entry spot check falls below 8/10. [scripts/learning_loop/systemd/README.md:101-106](../scripts/learning_loop/systemd/README.md#L101-L106)

## Records

- An agent's closeout Feedback field holds one record per line: `obs:`, `claim (basis, confidence, evidence word):` and `action (intent, status):`. [scripts/learning_loop/records.py:3-9](../scripts/learning_loop/records.py#L3-L9)
- Markers are parsed by code; a record with no link is kept but marked `unprovenanced` and can never support a licence. [scripts/learning_loop/records.py:11-14](../scripts/learning_loop/records.py#L11-L14)
- The contract is `feedback-report.v1`. [scripts/learning_loop/records.py:25](../scripts/learning_loop/records.py#L25)
- A licence links a claim to the rule it would justify; `active` needs two independent supporting observations and no unanswered challenge. [proposals/aes-learning-loop/PLAN.md:137-141](../proposals/aes-learning-loop/PLAN.md#L137-L141)
- The machine-readable schema is [contracts/learning-loop/feedback-report.v1.schema.json](../contracts/learning-loop/feedback-report.v1.schema.json). [proposals/aes-learning-loop/PLAN.md:230-231](../proposals/aes-learning-loop/PLAN.md#L230-L231)

## Labels

- One Jev choice per item sorts it into a failure-mode family, `other` (a failure no family fits) or `fact`; every family within `near_top` of the top probability is applied. [scripts/learning_loop/label_items.py:8-12](../scripts/learning_loop/label_items.py#L8-L12)
- Jev (`typesafe/jev-1.13`) is called through `llm_client` `call_decisions` as task `aes.feedback_labels`; a failed call is counted, never guessed. [scripts/learning_loop/label_items.py:25-29](../scripts/learning_loop/label_items.py#L25-L29) [scripts/learning_loop/label_items.py:55-58](../scripts/learning_loop/label_items.py#L55-L58)
- The question set is frozen; changing it means re-running the judged test sets first. [scripts/learning_loop/label_items.py:4-6](../scripts/learning_loop/label_items.py#L4-L6)
- The taxonomy is read from agent-skills' copy when it exists, else [docs/failure-modes.md](../docs/failure-modes.md). [scripts/learning_loop/label_items.py:50-54](../scripts/learning_loop/label_items.py#L50-L54)
- The labels job replaced agent-skills' weekly `taxonomy-feedback` report on 2026-10-26, after nothing new reached the failure-mode list from 2026-10-13. [scripts/learning_loop/systemd/README.md:28-30](../scripts/learning_loop/systemd/README.md#L28-L30)
- Two or more open `other` items open the `taxonomy:unmatched-failures` concern in agent-skills. [scripts/learning_loop/systemd/README.md:20](../scripts/learning_loop/systemd/README.md#L20)
- The adopted question-set design scored 16/20 on held-out items, meeting Brian's 8/10 floor but not 9/10. [datasets/learning-loop/experiments/2026-10-02-question-design/README.md:31-33](../datasets/learning-loop/experiments/2026-10-02-question-design/README.md#L31-L33)
- Family Z ("the fix landed where the symptom showed") was added on 2026-11-05 with a narrow wording after a re-test. [datasets/learning-loop/experiments/2026-11-05-family-z/README.md:3-5](../datasets/learning-loop/experiments/2026-11-05-family-z/README.md#L3-L5) [datasets/learning-loop/experiments/2026-11-05-family-z/README.md:25-29](../datasets/learning-loop/experiments/2026-11-05-family-z/README.md#L25-L29)
- The 2,575 legacy learnings were labelled once and kept as a file, not as GitHub issues. [datasets/learning-loop/README.md:7-11](../datasets/learning-loop/README.md#L7-L11)

## Analysis, licences, effects and fix owner (timers off)

- The weekly analysis labels families, relates similar records with Jev, groups records joined by `supports` or `same_problem`, and analyses each recurring problem with a stronger model. [scripts/learning_loop/problems.py:6-18](../scripts/learning_loop/problems.py#L6-L18)
- Jev judges relations because it scored 24 of 30 on hand labels; a Jev `challenges` answer is confirmed by the stronger model before it counts. [proposals/aes-learning-loop/PLAN.md:331-335](../proposals/aes-learning-loop/PLAN.md#L331-L335)
- The stronger model runs on the Claude subscription (`claude-code/sonnet`) when the unit sets `FEEDBACK_STRONG_MODEL`. [scripts/learning_loop/systemd/feedback-problems.service:20-23](../scripts/learning_loop/systemd/feedback-problems.service#L20-L23)
- Licence status is derived by the Observation-to-Action metamodel's own evaluator, never set by hand. [scripts/learning_loop/licences.py:1-13](../scripts/learning_loop/licences.py#L1-L13)
- A fix counts as enforced only with an explicit `feedback-enforcement` receipt comment, never an issue-close date. [scripts/learning_loop/effects.py:1](../scripts/learning_loop/effects.py#L1) [scripts/learning_loop/systemd/README.md:138-147](../scripts/learning_loop/systemd/README.md#L138-L147)
- `policies.py` checks each workspace rule for a WORKING_RULES source entry, an entry in the AES register and recent report mentions. [scripts/learning_loop/policies.py:1-17](../scripts/learning_loop/policies.py#L1-L17)
- The fix owner hands a batch of "adopt" concerns to one headless Claude Code session and then checks each item on GitHub itself, never trusting the session's summary. [scripts/learning_loop/fix_owner.py:1-15](../scripts/learning_loop/fix_owner.py#L1-L15)
- The fix owner is wrong if a spot check after four runs finds a merged change that did not do what its item asked. [scripts/learning_loop/systemd/README.md:181-183](../scripts/learning_loop/systemd/README.md#L181-L183)

## Repairs and extensions (2026-10-08 and 2026-10-09)

- The approved repair counts support per fix, keeps repository identity in references, compares times against an enforcement receipt and brings human corrections into the report model. [proposals/aes-learning-loop/REPAIR.md:12-15](../proposals/aes-learning-loop/REPAIR.md#L12-L15)
- The subagent-feedback plan wires parent-verified subagent outcomes into the same private log. [proposals/aes-subagent-feedback/PLAN.md:26](../proposals/aes-subagent-feedback/PLAN.md#L26)
- The feedback-prevention case took one native-agent failure through the taxonomy reviewer to a scoped instruction repair (Remote MCP preflight applies only to that transport). [proposals/aes-feedback-prevention/PLAN.md:135](../proposals/aes-feedback-prevention/PLAN.md#L135)
- Transcript text goes only to OpenRouter through `llm_client` and the local data folder; tests use synthetic transcripts. [proposals/aes-learning-loop/DESIGN.md:197-199](../proposals/aes-learning-loop/DESIGN.md#L197-L199)

## Related pages

- [Requirements](requirements.md): Q1-Q14 and the test results for `tests/learning`.
- [Run and deploy](run-and-deploy.md): installing and running the units.
- [Open questions](open-questions.md): the disabled timers and the taxonomy source.
