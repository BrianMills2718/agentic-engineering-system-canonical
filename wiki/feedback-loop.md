---
type: Topic
title: The feedback loop
description: How agent feedback becomes reports, labels, licensed fixes and effect counts, and which jobs run today
status: current
last_checked: 2026-11-11
---

# The feedback loop

The feedback loop is part 2 of AES; it is kept and runs nightly from `scripts/learning_loop` in this repository ([.project-brain/now.md:9](../.project-brain/now.md#L9)).
Code2-workspace decision 0009 keeps `collect_feedback.py`, `label_items.py` and `feedback_log.py` running ([docs/decisions/0009-aes-and-lockstep-fate.md:59-61](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L59-L61)).

## Why it exists

- Earlier systems recorded lessons and rarely closed the loop: the legacy register held 2,572 learnings with 4 resolutions, and no rule was ever retired ([proposals/aes-learning-loop/DESIGN.md:22-25](../proposals/aes-learning-loop/DESIGN.md#L22-L25)).
- Goal: each lesson, friction, problem, experiment and research finding becomes a short linked report; the loop sorts reports, analyses recurring problems, turns licensed claims into enforced rules or checks, and observes whether the failure stops recurring ([proposals/aes-learning-loop/PLAN.md:9](../proposals/aes-learning-loop/PLAN.md#L9)).
- A lesson or rule counts only once a check enforces it; until then it is a note ([proposals/aes-learning-loop/PLAN.md:48](../proposals/aes-learning-loop/PLAN.md#L48)).
- Agents adopt and retire rules by their best judgment; Brian observes a view ranked by impact and uncertainty and is notified ([proposals/aes-learning-loop/PLAN.md:47](../proposals/aes-learning-loop/PLAN.md#L47)).

## Jobs today

- Two timers run today, the collector and the labels job ([scripts/learning_loop/systemd/README.md:3-4](../scripts/learning_loop/systemd/README.md#L3-L4)).
- The weekly analysis, effects and fix-owner units, and agent-skills' `taxonomy-feedback.timer`, were disabled and inactive when checked on 2026-11-10 ([scripts/learning_loop/systemd/README.md:4-7](../scripts/learning_loop/systemd/README.md#L4-L7)).
- Git history does not record who turned them off or why ([scripts/learning_loop/systemd/README.md:9-10](../scripts/learning_loop/systemd/README.md#L9-L10)).
- Collector: daily at 03:30, running `collect_feedback.py --file --max-file 10` ([scripts/learning_loop/systemd/feedback-collector.timer:5](../scripts/learning_loop/systemd/feedback-collector.timer#L5)) ([scripts/learning_loop/systemd/feedback-collector.service:20](../scripts/learning_loop/systemd/feedback-collector.service#L20)).
- Labels: daily at 05:00, running `label_items.py issues --other-concern-repo BrianMills2718/agent-skills` ([scripts/learning_loop/systemd/feedback-labels.timer:5](../scripts/learning_loop/systemd/feedback-labels.timer#L5)) ([scripts/learning_loop/systemd/feedback-labels.service:17](../scripts/learning_loop/systemd/feedback-labels.service#L17)).
- Weekly analysis (off): Sundays at 05:00, `problems.py --file --days 14` ([scripts/learning_loop/systemd/feedback-problems.timer:5](../scripts/learning_loop/systemd/feedback-problems.timer#L5)) ([scripts/learning_loop/systemd/feedback-problems.service:23](../scripts/learning_loop/systemd/feedback-problems.service#L23)).
- Effects and rule check (off): daily at 07:30, `problems.py --effects-only` then `policies.py` ([scripts/learning_loop/systemd/feedback-effects.timer:5](../scripts/learning_loop/systemd/feedback-effects.timer#L5)) ([scripts/learning_loop/systemd/feedback-effects.service:10-12](../scripts/learning_loop/systemd/feedback-effects.service#L10-L12)).
- Fix owner (off): daily at 09:00, `fix_owner.py --max-items 10` ([scripts/learning_loop/systemd/feedback-fix-owner.timer:5](../scripts/learning_loop/systemd/feedback-fix-owner.timer#L5)) ([scripts/learning_loop/systemd/feedback-fix-owner.service:17](../scripts/learning_loop/systemd/feedback-fix-owner.service#L17)).
- On 2026-11-10 at 03:44 the collector logged `reports=10756 filed=80 items=472 errors=0 exit=0` ([docs/decisions/0009-aes-and-lockstep-fate.md:21-23](https://github.com/BrianMills2718/code2-workspace/blob/b8b523d7ec59f54248dac2d7a780441b787d6921/docs/decisions/0009-aes-and-lockstep-fate.md#L21-L23)).
- All outputs go to `~/projects/data/feedback-collector/`, which holds private transcript quotes and is never committed ([scripts/learning_loop/systemd/README.md:24-26](../scripts/learning_loop/systemd/README.md#L24-L26)).
- Install and rerun commands are on [run-and-deploy.md](run-and-deploy.md) ([scripts/learning_loop/systemd/README.md:36-48](../scripts/learning_loop/systemd/README.md#L36-L48)).

## Records and reports

- Every record has three parts: one sentence, links to where it came from, and who filed it when ([proposals/aes-learning-loop/PLAN.md:122-123](../proposals/aes-learning-loop/PLAN.md#L122-L123)).
- The record kinds are observation, claim (with basis, confidence and evidence word) and action (Investigate, Mitigate, Repair, Detect or Prevent) ([proposals/aes-learning-loop/PLAN.md:125-135](../proposals/aes-learning-loop/PLAN.md#L125-L135)).
- Agents write the closeout Feedback field with `obs`, `claim` and `action` lines ([proposals/aes-learning-loop/PLAN.md:143-151](../proposals/aes-learning-loop/PLAN.md#L143-L151)).
- A line with no resolvable link is kept but marked `unprovenanced` and can never support a licence ([proposals/aes-learning-loop/PLAN.md:153-155](../proposals/aes-learning-loop/PLAN.md#L153-L155)).
- A licence is derived, never set: `active` needs two independent supporting observations and no unanswered challenge ([proposals/aes-learning-loop/PLAN.md:137-141](../proposals/aes-learning-loop/PLAN.md#L137-L141)).
- The contract is `feedback-report.v1`, a Pydantic model in `scripts/learning_loop/records.py` ([proposals/aes-learning-loop/PLAN.md:230-231](../proposals/aes-learning-loop/PLAN.md#L230-L231)).
- The log is GitHub issues in a private repository, one issue per problem ([proposals/aes-learning-loop/PLAN.md:189-193](../proposals/aes-learning-loop/PLAN.md#L189-L193)); the collector files to `BrianMills2718/agent-feedback-log` ([scripts/learning_loop/systemd/README.md:55-56](../scripts/learning_loop/systemd/README.md#L55-L56)).

## Flow

- Report at work time, extract nightly, sort with Jev, group and analyse weekly, licence and decide, enforce, observe the effect nightly ([proposals/aes-learning-loop/PLAN.md:157-176](../proposals/aes-learning-loop/PLAN.md#L157-L176)).
- A rule whose failure recurs revokes its licence and reopens the problem ([proposals/aes-learning-loop/PLAN.md:174-176](../proposals/aes-learning-loop/PLAN.md#L174-L176)).

## Collector

- It reads Claude Code and Codex transcripts from the last day and turns each closeout Feedback field (and the older Learnings heading) into one report filed as one issue ([scripts/learning_loop/systemd/README.md:53-56](../scripts/learning_loop/systemd/README.md#L53-L56)).
- The report cap was raised from 80 to 900 a night on 2026-11-10, when 10,652 reports were waiting ([scripts/learning_loop/systemd/README.md:57-58](../scripts/learning_loop/systemd/README.md#L57-L58)).
- Exit 1 means some model or filing calls failed and exit 2 a crash; both fail the unit ([scripts/learning_loop/systemd/README.md:59-60](../scripts/learning_loop/systemd/README.md#L59-L60)).
- Brian's own corrections become reports with the literal quote, deduplicated by quote ([scripts/learning_loop/systemd/README.md:62-66](../scripts/learning_loop/systemd/README.md#L62-L66)).
- Subagent results are joined from parent tool events and kept unverified until a parent check runs ([scripts/learning_loop/systemd/README.md:69-74](../scripts/learning_loop/systemd/README.md#L69-L74)).
- A failed checker yields `verification_failed`, not a judgment of the child ([scripts/learning_loop/systemd/README.md:84-86](../scripts/learning_loop/systemd/README.md#L84-L86)).
- At most 10 Learnings lines a night go to the project-meta register, skipping repeats ([scripts/learning_loop/systemd/README.md:93-97](../scripts/learning_loop/systemd/README.md#L93-L97)).
- Why the filing gate looks this way: closeout Learnings lines were 8/8 reusable against 7/25 for narration, and Jev's yes/no answer did not separate them ([scripts/learning_loop/systemd/README.md:101-104](../scripts/learning_loop/systemd/README.md#L101-L104)) ([datasets/learning-loop/experiments/2026-10-07-filing-gate/README.md:9](../datasets/learning-loop/experiments/2026-10-07-filing-gate/README.md#L9)).

## Labels and failure families

- The labels job gives each open feedback issue a `family:<letter>`, `fact` or `other` label; two or more open `other` items open the `taxonomy:unmatched-failures` concern in agent-skills ([scripts/learning_loop/systemd/README.md:20](../scripts/learning_loop/systemd/README.md#L20)).
- It replaced agent-skills' weekly taxonomy report on 2026-10-26, after which nothing new had reached the failure-mode list since 2026-10-13 ([scripts/learning_loop/systemd/README.md:28-30](../scripts/learning_loop/systemd/README.md#L28-L30)).
- The families come from [docs/failure-modes.md](../docs/failure-modes.md), the current taxonomy authority ([docs/failure-modes.md:18-20](../docs/failure-modes.md#L18-L20)).
- A new family needs two independent instances ([docs/failure-modes.md:61-63](../docs/failure-modes.md#L61-L63)).
- The classifier is Jev (`typesafe/jev-1.13`) with frozen question set v2 ([datasets/learning-loop/README.md:9-10](../datasets/learning-loop/README.md#L9-L10)) ([datasets/learning-loop/README.md:19](../datasets/learning-loop/README.md#L19)).
- v2 meets Brian's 8/10 floor on the held-out set and does not reach 9/10 ([datasets/learning-loop/experiments/2026-10-02-question-design/README.md:31-33](../datasets/learning-loop/experiments/2026-10-02-question-design/README.md#L31-L33)).
- Family Z ("the fix landed where the symptom showed") was added on 2026-11-05 with a narrow wording ([datasets/learning-loop/experiments/2026-11-05-family-z/README.md:3-5](../datasets/learning-loop/experiments/2026-11-05-family-z/README.md#L3-L5)) ([datasets/learning-loop/experiments/2026-11-05-family-z/README.md:25-29](../datasets/learning-loop/experiments/2026-11-05-family-z/README.md#L25-L29)).
- The 2,575 legacy learnings are kept as one labelled file, not as GitHub issues ([datasets/learning-loop/README.md:7-11](../datasets/learning-loop/README.md#L7-L11)) ([.project-brain/truth.md:24-25](../.project-brain/truth.md#L24-L25)).
- The weekly run is a systemd timer rather than a Paperclip routine, because a fixed script needs no agent ([.project-brain/truth.md:21-23](../.project-brain/truth.md#L21-L23)).

## Weekly analysis, effects and fix owner (when switched on)

- Weekly analysis groups 14 days of reports into problems, analyses each recurring one with a stronger model, and derives licences; each active licence opens one "Feedback loop: adopt" concern ([scripts/learning_loop/systemd/README.md:110-127](../scripts/learning_loop/systemd/README.md#L110-L127)).
- The analysis runs on the Claude subscription as `claude-code/sonnet` ([scripts/learning_loop/systemd/feedback-problems.service:20-22](../scripts/learning_loop/systemd/feedback-problems.service#L20-L22)).
- A fix counts as enforced only with an enforcement receipt comment naming time, revision and verification ([scripts/learning_loop/systemd/README.md:138-145](../scripts/learning_loop/systemd/README.md#L138-L145)).
- A verified recurrence after enforcement revokes the licence and reopens the concern once ([scripts/learning_loop/systemd/README.md:133-136](../scripts/learning_loop/systemd/README.md#L133-L136)).
- The fix owner hands up to 10 adopt concerns to one headless Claude Code session and reads every issue back from GitHub rather than trusting the session's summary ([scripts/learning_loop/systemd/README.md:156-172](../scripts/learning_loop/systemd/README.md#L156-L172)).
- By 2026-10-12 all 24 adopt concerns were closed and 10 fixes carried receipts ([.project-brain/now.md:13](../.project-brain/now.md#L13)).

## Repairs and extensions

- The 2026-10-08 repair counts support per fix, keeps repository identity, compares timestamps against an explicit enforcement receipt and brings human corrections into the report model ([proposals/aes-learning-loop/REPAIR.md:12-15](../proposals/aes-learning-loop/REPAIR.md#L12-L15)).
- Native subagent assignments and parent-checked outcomes feed the same reports ([proposals/aes-subagent-feedback/PLAN.md:26](../proposals/aes-subagent-feedback/PLAN.md#L26)).
- One native preflight failure was dispositioned against the taxonomy and its shared instruction scoped to the execution transport ([proposals/aes-feedback-prevention/PLAN.md:135](../proposals/aes-feedback-prevention/PLAN.md#L135)).

## Self-application

- Ordinary rules, the loop's own rules and a fixed core form three levels, and only Brian edits the fixed core ([proposals/aes-learning-loop/DESIGN.md:82-96](../proposals/aes-learning-loop/DESIGN.md#L82-L96)).
- The exact level-3 list is Brian's to set ([proposals/aes-learning-loop/DESIGN.md:98-99](../proposals/aes-learning-loop/DESIGN.md#L98-L99)).

## Documents

- [Start page](../proposals/aes-learning-loop/review-page/guide.html), [adopted plan](../proposals/aes-learning-loop/PLAN.md), [original design (history)](../proposals/aes-learning-loop/DESIGN.md), [repair](../proposals/aes-learning-loop/REPAIR.md), [jobs guide](../scripts/learning_loop/systemd/README.md), [datasets](../datasets/learning-loop/README.md).
