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
| R2 | Within a week, each item is labelled either `fact` (not a failure) or one failure family `family:<letter>`, or else `unsorted` | Brian 2026-10-02; Jev test 2026-10-02 |
| R3 | A family whose open, sorted items recur past a threshold yields one drafted rule proposal: an AES plan proposal adding or changing a normative item, presented to Brian as a `Decision:` item | Brian 2026-10-02; harvest A3 #15 (lesson-to-check promotion) |
| R4 | An accepted rule names where it is enforced: the AES commit check (repository rules), the Jev gate (agent action rules), or instructions only. It also names what is observed and its feedback path | Brian 2026-10-02 ("observability, enforcement and feedback") |
| R5 | Enforcement emits evidence: `aes status` for repository rules and the Jev gate decision log for action rules. False asks or blocks become `kind:friction` issues automatically | Brian 2026-10-02; legacy lesson "controls went dark without anyone noticing" |
| R6 | The loop applies to itself without regress (see "Self-application") | Brian 2026-10-02 |
| R7 | History is preserved: the 2,572 legacy learnings are labelled once and kept in AES canonical | Brian 2026-10-02 (accepted import); amended, see Decisions |

## Material failure modes and controls

| Failure | Traces to | Control |
|---|---|---|
| Misfiling, i.e. the wrong family | R2 | Jev answers below the threshold go to `unsorted`. A weekly spot check samples 10 filed items; a misfile becomes a `kind:friction` against the loop itself (level 2) |
| Thresholds drift when wording changes | R2 | The question set is frozen and versioned (`questions: v1`). Any change re-runs the labelled spot-check set before the threshold is trusted (Jev learning 2026-10-02) |
| The loop goes dark | R1–R5 | Every run writes one summary issue comment with counts (read, sorted, unsorted, proposals, errors) and an exit status. A week with no run opens a `kind:problem` issue |
| Proposal flood | R3 | At most 3 drafted proposals per week; extras wait |
| Jev outage or refusal | R2 | Items stay unlabelled and are counted as `errors`; they are never silently skipped or guessed |
| Rules that never act | R4–R5 | Each accepted rule carries a trigger (for example "fired 0 times in 30 days" or "always allowed"). Hitting it opens a keep-change-retire `Decision:` item |
| A new failure shape no family fits | R2 | A low `fits_well` score together with `is_failure` yes marks the item `novel-candidate`. A second instance proposes a new family (from the legacy taxonomy pass's own rule) |

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
  `family:{A..Y}` (one per family in the moved taxonomy), `fact`, `unsorted`,
  `novel-candidate`, `level:{1,2}`, `source:{legacy,session,gate}`.
- **Issue body front matter:** `source_ref`, `recorded_at`, `recommended_action`,
  `jev: {questions: v1, is_failure, family, p, confidence, run}`.
- **Jev question set v1:**
  - `is_failure` (yes/no): "describes a reasoning or control failure, not a
    plain fact";
  - `fits_well` (yes/no, with family titles listed);
  - `family` (one choice per family; criterion text = title plus guiding
    question).

  Filing rule: `is_failure < 0.7` → `fact`; else `p ≥ 0.6` → `family:X`;
  else `unsorted`. These numbers come from the 20-item test and are
  re-calibrated from spot checks.
- **Taxonomy:** moves from `agent-skills/skills/review/references/failure-modes.md`
  into AES canonical as one document; the families are the label source.
- **Proposals:** `aes plan prepare` output with one normative item per rule,
  plus fields `enforced_by`, `observed_by`, `feedback_path`, `retire_trigger`.

## Provider evaluation (donor re-entry rule, `aes-v0.2-greenfield/05-donor-reentry.md`)

| Capability | Candidate | Disposition |
|---|---|---|
| Item storage, search and counts | GitHub Issues and labels | **reuse** |
| Classification | Jev (TypeSafe) via OpenRouter `systemone` | **configure** (question set v1) |
| Rule home and acceptance | AES `.aes/target.yaml` normative items and `aes plan` | **reuse** |
| Action-rule enforcement and log | `jev-engineering` gate (pinned 82655a6) with Brian's `policy.local.json` | **configure** |
| Scheduling | Paperclip routine on personal-vps | **reuse** |
| Classifier in legacy `taxonomy_feedback_pass.py` (token overlap) | — | **reject**: its own docstring shows the correct family ranked 3rd of 17. Its *ideas* enter as requirements: durable per-item outcome, `novel-candidate` on a second instance, corpus-measured "unmatched" threshold |
| Legacy friction clusters and policy registry | — | **reject as architecture**; data and ideas only |
| Glue that labels issues and drafts proposals | — | **residual** (small script, the only new code) |

## External-call budget

- **Calls:** 1 Jev call per item (3 questions in one request). Legacy backfill:
  2,572 calls, about $0.13 at the observed $0.00005 per call. Weekly: tens of calls.
- **Latency:** observed 0.3–0.6 s per call. The backfill runs serially with
  resume from the last labelled entry id.
- **Failure:** no retry beyond one. A failed item stays unlabelled and is
  counted; no fallback to another model.
- **Canary:** the first 20 items reuse the 2026-10-02 hand-checked set.

## Decisions (agent, reversible)

- **Legacy history goes to a committed archive file, not 2,572 issues.** The
  accepted plan said "import as closed issues, last 3 months". All 2,572 entries
  turned out to be within 3 months (the register started in July), so the
  smaller import doesn't exist. The archive
  (`datasets/legacy-learnings-labelled.jsonl`) is labelled by the same Jev
  questions, and family counts include it. Reverse: create the issues from that
  file.

## Thin slices

| # | Slice | State |
|---|---|---|
| 1 | Move the taxonomy in; create the labels; label the legacy archive with Jev (dry run first: report counts per family and `fact`, `unsorted`, `novel-candidate`); Brian spot-checks 10 | fully_specifiable_now |
| 2 | New items → issues: agents file `kind:*` issues; a weekly Paperclip routine labels them and posts the run summary | fully_specifiable_now |
| 3 | Threshold → drafted AES plan proposal → `Decision:` item for Brian | conditional on slice 1 counts (sets the threshold) |
| 4 | Accepted action rules compiled into the Jev gate's `policy.local.json`; gate false asks and blocks → `kind:friction` issues | conditional on the gate's observe-mode log |
| 5 | Level-2 and level-3 controls as normative items; trigger evaluation | human_decision_required (level-3 list) |

## Still unresolved

- `human_required`: the level-3 fixed-core list (blocks slice 5 only).
- `assumption`: Jev's "p ≥ 0.6 is right" holds beyond 20 items. Slice 1's spot
  check tests it; if fewer than 8 of 10 are right, the threshold goes up before
  slice 2.
- `assumption`: GitHub issues stay usable at tens of new items per week. If the
  view becomes noise, labels plus saved searches are the first fix, not a new UI.
- `agent_decided_reversible`: archive file instead of 2,572 issues (above).
