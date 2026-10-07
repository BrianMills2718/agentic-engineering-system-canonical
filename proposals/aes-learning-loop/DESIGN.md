# AES learning loop: from lessons to enforced, observed rules

Status: **design proposal, non-normative.** Drafted by Claude Code for Brian on
2026-10-02 using Company Planning `bounded-design` (Standard depth, path
`durable_solo`, overlays: LLM calls and governed rules). Nothing here is accepted
architecture until Brian dispositions it and the rule-bearing parts enter AES
through `aes plan prepare / validate / accept`.

## Why this exists

Brian's earlier systems recorded lessons well and almost never closed the loop.
The legacy register held 2,572 learnings with 4 resolutions; 40 of 59 friction
clusters were open; 133 of 166 concern issues were open; and no rule was ever
retired. Source: `research/synthesis/2026-09-28-legacy-idea-harvest/README.md`
(lesson 1, "Recording works; closing does not") and the 2026-10-01 counts in
`personal-vps/apps/paperclip/docs/carry-over-from-earlier-agent-systems.md`.

Brian, 2026-10-02: the goal is to document learnings, frictions and problems,
bundle them into failure modes and policy proposals, then update policies with
observability, enforcement and feedback on them. The system should apply to
itself, but without infinite regress. Off-the-shelf parts are preferred, and AES
canonical is the fresh-start home; `project-meta` is legacy.

## Objective, actor, result

- **Actor:** Brian, who decides rules, and his agents, which record lessons and
  run the loop.
- **Recurring job:** every week, new lessons, frictions and problems are sorted;
  recurring failure shapes become proposed rules; Brian decides them; accepted
  rules are enforced and observed; the evidence feeds back.
- **Inspectable result:** a GitHub label view showing open items per failure
  family, plus `Decision:` items Brian answers in his terminal. Each accepted
  rule shows where it is enforced and how often it fired.

## Non-goals

- Rebuilding `project-meta`'s policy registry, friction file or concern queue.
  They are idea sources and a one-time data import only.
- Extending or repairing the legacy `agent-skills/scripts/taxonomy_feedback_pass.py`
  or the `ecosystem-ops` feedback worker.
- A new UI. Brian answers in the terminal now; a dashboard is a later, separate
  outcome.
- Automatic rule changes without Brian.

## Requirements (with provenance)

| # | Requirement | Provenance |
|---|---|---|
| R1 | Every new lesson, friction or problem is recorded once as a GitHub issue in AES canonical, typed as `kind:lesson`, `kind:friction` or `kind:problem` | Brian 2026-10-02 (data home accepted: "a") |
| R2 | Within a week, each item is labelled `fact` (not a failure), `other` (a failure no family fits), or one or more failure families `family:<letter>`. At least 8 of 10 labels must be acceptable on items judged before the run | Brian 2026-10-02 ("8 out of 10 is good … 9 out of 10 if better"; "allow multiple to apply … and a clear other") |
| R3 | A family whose open, sorted items recur past a threshold yields one drafted rule proposal: an AES plan proposal adding or changing a normative item, presented to Brian as a `Decision:` item | Brian 2026-10-02; harvest A3 #15 (lesson-to-check promotion) |
| R4 | An accepted rule names where it is enforced: the AES commit check (repository rules), the Jev gate (agent action rules), or instructions only. It also names what is observed and its feedback path | Brian 2026-10-02 ("observability, enforcement and feedback") |
| R5 | Enforcement emits evidence: `aes status` for repository rules and the Jev gate decision log for action rules. False asks or blocks become `kind:friction` issues automatically | Brian 2026-10-02; legacy lesson "controls went dark without anyone noticing" |
| R6 | The loop applies to itself without regress (see "Self-application") | Brian 2026-10-02 |
| R7 | History is preserved: the 2,572 legacy learnings are labelled once and kept in AES canonical | Brian 2026-10-02 (accepted import); amended, see Decisions |

## Material failure modes and controls

| Failure | Traces to | Control |
|---|---|---|
| Misfiling, i.e. the wrong family | R2 | Every family within 0.15 of Jev's top probability is applied, so a near-tie yields several labels instead of a guess. Answers with confidence ≥ 0.9 are marked `confident`. A weekly spot check samples 10 filed items; a misfile becomes a `kind:friction` against the loop itself (level 2) |
| Thresholds drift when wording changes | R2 | The question set is frozen and versioned (`scripts/learning_loop/question_set_v2.json`, `questions: v2`). Any change re-runs the judged sets in `datasets/learning-loop/experiments/` before it is trusted, and is measured on items judged before the run, not on items the wording was tuned against (issue #64) |
| The loop goes dark | R1–R5 | Every run writes one summary issue comment with counts (read, filed, fact, other, proposals, errors) and an exit status. A week with no run opens a `kind:problem` issue |
| Proposal flood | R3 | At most 3 drafted proposals per week; extras wait |
| Jev outage or refusal | R2 | Items stay unlabelled and are counted as `errors`; they are never silently skipped or guessed |
| Rules that never act | R4–R5 | Each accepted rule carries a trigger (for example "fired 0 times in 30 days" or "always allowed"). Hitting it opens a keep-change-retire `Decision:` item |
| A new failure shape no family fits | R2 | Jev's `other` option (defined as a real failure none of the families describes) labels it `other`. A second similar `other` item proposes a new family (from the legacy taxonomy pass's own rule) |

## Self-application without infinite regress

1. **Level 1, ordinary rules** (for example "ask before merging"): the loop
   proposes; Brian decides.
2. **Level 2, the loop's own rules** (the Jev question set, thresholds, the
   weekly cap, the triggers): these are normative items in the same AES target,
   and they collect frictions like any rule. A level-2 change needs (a) a trigger
   that fired with a recorded count, (b) Brian's decision, and (c) no other
   level-2 change to the same item in the previous 14 days. At most 1 level-2
   proposal per week.
3. **Level 3, the fixed core**, which the loop never proposes changes to:
   - every rule has an enforcement location, an observation and a feedback path;
   - changes need a measured trigger;
   - Brian decides levels 1 and 2;
   - the cooling-off period and caps exist.

   Only Brian edits level 3, directly.

The **exact level-3 list is Brian's to set** (`human_required`). The list above
is the recommendation.

## Contracts and schema

- **Issue labels:** `kind:{lesson,friction,problem}`,
  `family:{A..Y}` (one per family in the moved taxonomy; several may apply), `fact`, `other`,
  `level:{1,2}`, `source:{legacy,session,gate}`.
- **Issue body front matter:** `source_ref`, `recorded_at`, `recommended_action`.
  Jev's answer (questions version, choice, families, p, confidence, runner-up)
  goes in a comment by the label run, so the filer's text is never rewritten.
  Labels `other` and `confident` were created 2026-10-02.
- **Jev question set v2** (`scripts/learning_loop/question_set_v2.json`): one
  choice question, written to TypeSafe's choice guidance. Each of the 22
  families is an option with a descriptive name, `what` it covers and what it
  is `not_for`, plus `other` and `not_a_failure` options. The learning goes in
  as named fields (`learning`, `recommended_action`).

  Filing rule: choice `not_a_failure` → `fact`; choice `other` → `other`;
  else every family within 0.15 of the top probability → `family:X` (one or
  several); confidence ≥ 0.9 → `confident`.

  Measured 2026-10-02 on 20 items judged before the run: an acceptable family
  was among the labels for 16/20 items, with 1.6 labels on average. Detail:
  `datasets/learning-loop/experiments/2026-10-02-question-design/`.

  v1 (a yes/no `is_failure` and `fits_well`, plus a choice with title and
  guiding question, filed at p ≥ 0.6) is retired. Its `other`-is-never-chosen
  result was a wording problem, not a Jev limit.
- **Taxonomy:** moves from `agent-skills/skills/review/references/failure-modes.md`
  into AES canonical as one document; the families are the label source.
- **Proposals:** `aes plan prepare` output with one normative item per rule,
  plus fields `enforced_by`, `observed_by`, `feedback_path`, `retire_trigger`.

## Provider evaluation (donor re-entry rule, `aes-v0.2-greenfield/05-donor-reentry.md`)

| Capability | Candidate | Disposition |
|---|---|---|
| Item storage, search and counts | GitHub Issues and labels | **reuse** |
| Classification | Jev (TypeSafe) via OpenRouter `systemone` | **configure** (question set v2, written to TypeSafe's own choice guidance) |
| Rule home and acceptance | AES `.aes/target.yaml` normative items and `aes plan` | **reuse** |
| Action-rule enforcement and log | `jev-engineering` gate (pinned 82655a6) with Brian's `policy.local.json` | **configure** |
| Scheduling | systemd timer on personal-vps (`learning-loop.timer`, personal-vps `apps/learning-loop/`), like the nightly backup | **reuse** (was: Paperclip routine; a fixed script needs no agent, and the timer keeps running when Paperclip agents are down, as on 2026-10-02) |
| Classifier in legacy `taxonomy_feedback_pass.py` (token overlap) | — | **reject**: its own docstring shows the correct family ranked 3rd of 17. Its *ideas* enter as requirements: durable per-item outcome, a new family proposed on a second `other` instance |
| Legacy friction clusters and policy registry | — | **reject as architecture**; data and ideas only |
| Glue that labels issues and drafts proposals | — | **residual** (small script, the only new code) |

## External-call budget

- **Calls:** 1 Jev call per item (one choice question). Legacy backfill:
  2,573 calls, about $0.25 at the observed $0.0001 per call. Weekly: tens of calls.
- **Latency:** observed 0.3–0.6 s per call. The backfill runs 8 calls at a time and
  resumes by skipping entries already labelled with the same question-set version.
- **Failure:** no retry beyond one. A failed item stays unlabelled and is
  counted; no fallback to another model.
- **Canary:** the first 20 items reuse the 2026-10-02 hand-checked set.

## Decisions (agent, reversible)

- **Legacy history goes to a committed archive file, not 2,572 issues.** The
  accepted plan said "import as closed issues, last 3 months". All 2,572 entries
  turned out to be within 3 months (the register started in July), so the
  smaller import doesn't exist. The archive
  (`datasets/learning-loop/legacy-learnings-labelled-v2.jsonl`) is labelled by the same Jev
  questions, and family counts include it. Reverse: create the issues from that
  file.

## Thin slices

| # | Slice | State |
|---|---|---|
| 1 | Move the taxonomy in; create the labels; label the legacy archive with Jev (report counts per family and `fact`, `other`); check against judged items | done 2026-10-02: v1 then v2 (issue #64) |
| 2 | New items → issues: agents file `kind:*` issues; a weekly run labels them and posts the run summary | built 2026-10-02: `label_items.py issues` labelled #64, #71–#73 (4 filed, $0.0004); weekly timer on personal-vps posts to issue #74. Open: agents filing items on their own (the `learned` skill still writes to project-meta). Input side added 2026-10-06: the nightly feedback collector (below) files what closeouts and transcripts carry into that same project-meta register, so the register, not issues, is still the one recurring input (`docs/failure-modes.md`) |
| 3 | Threshold → drafted AES plan proposal → `Decision:` item for Brian | conditional on slice 1 counts (sets the threshold) |
| 4 | Accepted action rules compiled into the Jev gate's `policy.local.json`; gate false asks and blocks → `kind:friction` issues | conditional on the gate's observe-mode log |
| 5 | Level-2 and level-3 controls as normative items; trigger evaluation | human_decision_required (level-3 list) |

## Input: the nightly feedback collector (2026-10-06)

Brian approved it 2026-10-06 ("ok do that") after finding that closeout
**Learnings**, **Concerns**, **Policy** and **Decisions** fields, his own
corrections, and friction agents mention in passing reached no log unless an
agent ran the `learned` skill by hand.

`scripts/learning_loop/collect_feedback.py` (pure parsing in `transcripts.py`)
runs nightly from `feedback-collector.timer` on Brian's PC (units in
`scripts/learning_loop/systemd/`, installed like personal-vps `hive/systemd/`):

| Step | How | Disposition |
|---|---|---|
| Read new transcript bytes (Claude Code `~/.claude/projects/*/*.jsonl`, Codex `~/.codex/sessions/**`) | byte offsets in `state.sqlite`; only complete lines | residual (claude-miner and llm_client's `tool_usage` parse tool calls, not message text) |
| Closeout fields | code: the fixed bold headings; `None` fields counted and skipped; a field naming a register entry is marked already recorded | residual |
| Corrections, friction, in-passing learnings in interactive sessions | light LLM (`deepseek-v4-flash`) through `llm_client` structured output; a quote not found verbatim in the window is dropped and counted | configure |
| Kind (learning / friction / correction / concern / noise) | Jev `call_decisions` choice question | configure |
| Already in the register? | nearest entry by word overlap, then Jev's probability that it states the same lesson. **Annotation only**: Jev's stance accuracy was weak in Brian's own test (6/15, inquiry-graph `docs/goals/cross-conversation-linker.md`), so it drops nothing until measured on a labeled sample | configure, unmeasured |
| Output | one JSON line per item in `~/projects/data/feedback-collector/items-<date>.jsonl` (exact quote, transcript, byte offset, session, time, client, kind, Jev probability), run summary in `runs.jsonl` | reuse (one file per day rule) |
| Filing | learning/friction/correction items from closeout Learnings or Policy fields or the LLM step, Jev p ≥ 0.8, at most 25 a night, through `project-meta/scripts/log_learning.py` with `--transcript-ref` and the transcript byte offset as `--source-ref`. Concerns and Decisions stay in the daily log (their homes are concern issues and decision records) | reuse |
| Going dark | non-zero exit opens a keyed agent concern (`notify_operator.py`); personal-vps `hive/controls.py` reads `runs.jsonl` | reuse |

Privacy: transcript text goes only to OpenRouter through `llm_client` and to
the local data folder. This repository is public, so no transcript text or
extracted quote is ever committed here; the tests use synthetic transcripts.

**Wrong when:** Brian's or an agent's spot check of 10 filed entries finds
fewer than 7 worth keeping (then raise the filing threshold or narrow the
sources), or the nightly cost passes $0.50.

## Still unresolved

- `human_required`: the level-3 fixed-core list (blocks slice 5 only).
- `assumption`: the acceptable-family judgments behind the 8/10 measurement
  are Claude's, not Brian's. If Brian's own spot check of 10 filed items finds
  fewer than 8 acceptable, the wording is revised before slice 2.
- `assumption`: 9 of 10 needs a better cut of the families, not better
  wording. Most remaining misses are pairs that describe one failure from two
  angles (what failed versus why). A quick five-group hierarchy did worse
  (12/20 groups right), so a re-cut needs a real factorization analysis.
- `assumption`: GitHub issues stay usable at tens of new items per week. If the
  view becomes noise, labels plus saved searches are the first fix, not a new UI.
- `agent_decided_reversible`: archive file instead of 2,572 issues (above).
