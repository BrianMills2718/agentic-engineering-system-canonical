---
plan_id: aes-learning-loop
status: shaping
selected_path: coordinated
planning_path_decision: proposals/aes-learning-loop/planning-path-decision.json
method_conformance_receipt: proposals/aes-learning-loop/method-conformance-receipt.json
supersedes_in_part: proposals/aes-learning-loop/DESIGN.md
goal:
  outcome: every lesson, friction, problem, experiment and research finding an agent meets becomes a short report whose claims link to their evidence and say how they are known; the loop extracts and sorts the reports, analyses problems that recur, turns licensed claims into enforced rules or checks, and observes whether the failure stops recurring
  canonical_example: on 2026-10-07 ten learnings lanes stranded their entries; the agents' Feedback sections yield observations linked to the failing log lines, a claim "the commit rule refuses the [Discovery] tag" (inferred, high, linked to the commit-rule log), Jev groups the reports into one problem, the claim's licence becomes active on two independent observations, a Prevent action (the lane fallback, project-meta #2442) is adopted by the loop's agent and enforced, the change appears at the top of Brian's impact-and-uncertainty view with one notification, and stranded-lane observations after the fix are counted nightly
  forbidden_substitutes: a register of notes that no check enforces (the 1,321-lesson history); a report that explains instead of linking; a licence status set by hand; Jev writing claim text; a rule counted as working without an observed effect
  boundaries: AES canonical scripts/learning_loop, the learned skill, the Feedback closeout field, the private feedback log, docs/failure-modes.md input section, and this proposal folder; the Observation-to-Action metamodel is read and reused, not changed, except through its own decision process
  done_when: slices S1-S5 meet their success criteria below with full traces reviewed
  do_not_gate_on: vision milestone 4; Brian reading or approving anything (he observes and is notified); migration of the 68 existing issues (S6, deferred)
  owner: claude-code:code-8c
---

# Agent feedback as an Observation-to-Action loop

## Who it serves, the result, one example

**Actors.** Every Claude and Codex agent working in Brian's repositories (they report), the nightly
and weekly loop runs (they sort, analyse, and adopt or retire rules by their best judgment), and Brian
(he observes a view ranked by impact and uncertainty and is notified of the items that matter; he is
not an approver).

**Result.** One private feedback log of linked, qualified reports; problems grouped across sessions;
rules and checks that exist because the evidence licensed them; and, for each rule, an observed count
of whether the failure it targets still happens.

**Example.** The canonical example in the front matter is the stranded-lanes failure of 2026-10-07,
traced end to end: observation, claim, grouping, licence, Prevent action, enforcement, effect.

## Brian's direction (authority)

All 2026-10-07, this session unless dated otherwise:

- the Feedback section should hold "as much information as it can provide and qualified and provenanced";
- provenance should link out "than explains it or else it consumes my attention";
- agents "dont always know the whole causal chain ... this is part of the post processing lop";
- agents should be "doing research as well and tryingt new things and prusing leanring policeis and recording whtat they elarned";
- reports "would be autoamtically extracted and hten that system 1 models might be helpful here";
- failures go to failure modes for the audit skill, and root solutions to company planning;
- "problems and leanrings is tnot the opteial canoncial favotricaiotn";
- "i dont care wihether feedback is public or private";
- "i approve. lets plan this out using company planning".
- "i dont want to be in the feedback loop for goals. i want to be able to observe it sorted by like impact ucnertainty and notified buti need agents to maek their best judgment".
- 2026-10-05 (vision thesis, approved): "a lesson or rule counts only once a check enforces it, until then it is a note", after "1,321 logged lessons, 638 self-described repeats, none turned into a binding check".
- 2026-10-02 (this folder's DESIGN.md): rules were to be proposed to Brian. **Superseded** by his 2026-10-07 direction above: agents adopt and retire rules; Brian observes.

## Authority and non-goals

Authority: the direction above; AES canonical is Brian's repository; the learned skill and the
Feedback field are shared contracts, changed together for Claude and Codex (claude-codex-parity).

Non-goals:

- changing Observation-to-Action's specification; the loop is a consumer of it;
- rule changes with no feedback path: every adopted rule carries its effect count and retire trigger (the workspace condition for agent-made policy);
- a dashboard;
- rewriting existing issues or register entries (they are only annotated).

## Irreversible actions and spend

No irreversible action: new records are appended, nothing is deleted. Spend: model calls through the
shared client only. Jev classification is about $0.0001 per question; the light extraction model
about $0.14 for three days of transcripts (measured 2026-10-06); recurring-problem analysis is
capped per week (see the external-call budget).

| Spend | Boundary | Who authorizes | Containment |
| --- | --- | --- | --- |
| Nightly Jev and extraction calls | stop and report if one night exceeds $1 | Brian's configured OpenRouter route and the shared client's budgets (standing) | the run fails loudly, files a concern, and sorts nothing more that night |
| Weekly problem analysis | at most 3 analyses a week, 40 records each | same | extra problems wait for the next week |
| The S2 measurement | under $1 once | same | one run; its labels are kept as a fixture |

## Current truth and reuse

| Existing capability | Where | Disposition |
| --- | --- | --- |
| Licence and its derived status (`active`, `conditional`, `unestablished`, `revoked`), conditions, `supersedes` | observation-to-action-metamodel `04-SPEC.md` §2-§4 (R-401 to R-405) | **reuse**: a claim drives a rule only through a licence whose status is derived, never set |
| Claim types as an index, never ordered (R-101) | same, §1 | **reuse**: a claim about the tool is not a claim about every repository |
| Evidence words (implemented, demonstrated, supported, current judgment, forecast, hypothesis, principle, objective) | vision `wiki/synthesis/hypotheses-and-evidence-register.md` lines 97-110 | **reuse** for claim status in reports |
| Record shapes `claim`, `hypothesis`, `origin`, `review_status`, relations `supports`, `challenges` | inquiry-graph `src/inquiry_graph/model.py` lines 46-100 | **reuse** the relation names |
| Envelope: content, provenance, publication info | nanopublication; W3C PROV (adopted in metamodel `07-PRIOR-ART.md` line 32) | **adopt** |
| Action intents Investigate, Mitigate, Repair, Detect, Prevent | Google SRE action-item types (USENIX ;login: spring 2017) | **adopt** |
| Nightly extraction from transcripts, Jev triage, gates, repeat check | `scripts/learning_loop/collect_feedback.py` (AES #156-#233) | **extend**: read the Feedback field, emit the new records |
| Weekly Jev family labelling, run summary, triggers for rules that never act | this folder's `DESIGN.md` R2-R5 and `scripts/learning_loop/label_items.py` | **extend** |
| `kind:lesson/friction/problem` issues filed by the learned skill | `learned` SKILL.md; 68 issues | **supersede** by the record model below; old issues annotated (S6) |
| Failure-mode families and the two-instance rule for a new family | `docs/failure-modes.md` | **reuse**; its input section is repointed at the new log (resolves the conflict with the learned skill) |

Searched on 2026-10-07: existing owners (`scripts/learning_loop/`, the `learned` skill, the weekly
labeller, `docs/failure-modes.md`), Brian's internal lineage (observation-to-action-metamodel,
inquiry-graph, epistemic-warrant, factgraph, onto-canon6, the vision wiki), and external prior art
(nanopublications, W3C PROV, Toulmin, Google SRE postmortems, ITIL problem management, NASA ASRS,
PDCA and Kolb, ExpeL, CoALA, Reflexion, Voyager). Dispositions use only reuse, extend, compose,
supersede or bounded exception:

| Candidate | Disposition |
| --- | --- |
| metamodel licence, R-101, R-401 to R-405 | reuse |
| vision register evidence words | reuse |
| inquiry-graph relation names | reuse |
| epistemic-warrant: no single combined score | reuse |
| nanopublication envelope and W3C PROV | compose (envelope fields inside the record model) |
| Google SRE action intents | reuse |
| ITIL incident versus problem; NASA ASRS narrative then coding | compose (reports first, problems grouped later) |
| collector, labeller, failure-mode list | extend |
| `kind:lesson/friction/problem` scheme | supersede |
| factgraph, onto-canon6 | bounded exception: they govern domain facts, not agent feedback; not used |
| ExpeL, CoALA, Reflexion, Voyager | bounded exception: they store one agent's own memory, not a governed log shared across agents; cited as precedent for claims revised by later evidence |
| PDCA, Kolb, Toulmin | bounded exception: cited as background; the metamodel already carries the loop and the claim/evidence split |

## Design

### Record model

Every record has three parts: what it says (one sentence), where it came from (links only), and who
filed it when. Three kinds:

1. **Observation**: something seen. Fields: `what`, `evidence[]` (links), `expected` (optional link or
   sentence), `subject_kind` (`work` or `control`, a rule, tool, hook or skill), `notified` (was anyone
   told). A problem is an observation whose `expected` it contradicts; friction is an observation with
   `subject_kind: control`.
2. **Claim**: what the reporter now believes. Fields: `text`, `basis` (`seen`, `inferred`, `guessed`),
   `confidence` (low, medium, high, self-reported), `evidence_word` (from the vision register),
   `claim_type` (about this run, this repository, or agent work generally), `supports[]`,
   `challenges[]` (links to observations or claims). A lesson is a claim whose licence is active.
3. **Action**: something tried or done. Fields: `intent` (Investigate, Mitigate, Repair, Detect,
   Prevent), `status` (proposed, done), `tests_claim` (link), `result` (links to the observations it
   produced). An experiment or research step is an Investigate action.

**Licence** (Observation-to-Action): links a claim to the rule or check it would justify. Its status is
derived by R-401: `active` needs at least two independent supporting observations (different sessions
or days, each with a resolvable link) and no unanswered challenge; `conditional` with one; `revoked`
when the rule's effect observations show the failure still recurring. A revision supersedes, never
rewrites (R-405).

### Report format (the Feedback closeout field)

```text
Feedback:
- obs: <one sentence> [<link>] [<link>]  expected: <link or sentence>
- claim (inferred, high, supported): <one sentence>  ← <obs or link>
- action (Investigate, done): <one sentence> → <result link>
- action (Prevent, proposed): <one sentence>
```

Links are file:line, commit, pull request, issue, log path with line, URL, or a chat anchor
(session id, message id). A line with no resolvable link is kept but marked `unprovenanced` and can
never support a licence.

### Flow

1. **Report** (agent, at work time): the Feedback field above.
2. **Extract** (nightly, `collect_feedback.py`): parse the field by its fixed markers (code); split
   free-text reports into records with the light model only where markers are missing.
3. **Sort** (nightly, Jev, fixed choices only): record kind check, `subject_kind`, failure family
   (`question_set_v2`), action intent, and the relation of a new record to its nearest existing one
   (`supports`, `challenges`, `same_problem`, `unrelated`).
4. **Group and analyse** (weekly): records grouped into problems; a problem with two or more
   independent observations gets one stronger-model analysis that drafts the causal chain and a
   general fix, each line marked as a claim with links.
5. **Licence and decide** (weekly, agents): a claim whose licence derives `active` and whose action is
   Prevent becomes an `aes plan prepare` plan that the loop's agent adopts through the company-planning
   gate by its best judgment; Detect becomes an audit check added the same way; Repair and Mitigate
   stay with the repository. Each decision is recorded with its impact, uncertainty and retire trigger.
6. **Enforce** (agents, on adoption): through the existing enforcement points (DESIGN.md R4: commit check,
   Jev gate, or instructions only).
7. **Observe the effect** (nightly): every enforced rule names the observation pattern it should
   stop; matching observations after enforcement are counted per rule; a rule whose failure recurs
   revokes its licence and reopens the problem.

### What Brian sees

- **A view ranked by impact and uncertainty** (a page on the plans site, rebuilt nightly): every open
  problem, active licence and adopted rule, sorted by impact first (how many sessions and repositories
  hit it, how often, and what it cost: time, money, or a wrong claim reaching a person) and then by
  uncertainty (licence `conditional` or `unestablished`, few independent observations, a rule whose
  effect is not yet measured). High impact with high uncertainty sorts to the top.
- **Notifications** (through `project-meta/scripts/notify_operator.py`, once per state change, plain
  sentences): a high-impact rule adopted, a rule revoked because its failure recurred, and a weekly
  one-line digest. Nothing asks him for a decision.

### Storage

One private log: GitHub issues in a private repository (decided 2026-10-07; Brian has no preference
and the workspace rule forbids publishing private information). One issue per problem, records as
comments, labels for kind, family and licence status. The public AES record keeps the design and code.

## Requirements (with provenance)

| # | Requirement | Provenance |
| --- | --- | --- |
| Q1 | Reports carry everything the agent can offer, each claim qualified by basis, confidence and evidence word | explicit_user 2026-10-07 |
| Q2 | Provenance is links, never retold evidence; one sentence per record | explicit_user 2026-10-07 |
| Q3 | Research, experiments and learning steps are recorded, not only failures | explicit_user 2026-10-07 |
| Q4 | Reports are extracted automatically from the Feedback field | explicit_user 2026-10-07 |
| Q5 | Fixed-choice sorting uses a System 1 model (Jev) | explicit_user 2026-10-07 |
| Q6 | Causes and general fixes are worked out after reporting, on grouped problems | explicit_user 2026-10-07 |
| Q7 | Failure families feed the audit skill; general fixes go to company planning | explicit_user 2026-10-07 |
| Q8 | A claim drives a rule only through a licence whose status is derived | governing_authority: metamodel R-401; vision 2026-10-05 |
| Q9 | Every enforced rule has an observed effect count, and a recurring failure revokes it | governing_authority: vision milestone 7; DESIGN.md R5 |
| Q10 | Agents adopt and retire rules by their best judgment; Brian is not an approver | explicit_user 2026-10-07 |
| Q12 | Brian observes a view ranked by impact and uncertainty and is notified of high-impact changes | explicit_user 2026-10-07 |
| Q11 | The log is private | derived_current_boundary: workspace no-private-information rule; Brian indifferent |

## Material failure modes and controls

| Failure | Traces to | Control |
| --- | --- | --- |
| Reports explain instead of linking, and consume Brian's attention | Q2 | Extraction marks link-free lines `unprovenanced`; they cannot support a licence; the weekly summary counts them per agent |
| The register fills with notes nothing enforces (the 1,321-lesson history) | Q8, Q9 | Success is measured in licensed, enforced rules with effect counts, not in records filed |
| Guesses are read as findings | Q1, Q8 | Basis is required; `guessed` claims never count as support |
| One noisy session inflates support | Q8 | Independence requires different sessions or days |
| Jev misjudges relations (6 of 15 on a similar task) | Q5 | S2 measures it on a labelled set before any licence depends on it; below the bar, the stronger model judges relations |
| A rule is counted as working without evidence | Q9 | Effect counting is part of S5; a rule with no defined observation pattern cannot be proposed |
| Private quotes reach a public surface | Q11 | Log in a private repository; the public repository holds only code, design and ids |
| Two authorities name different inputs for the failure-mode list | Q7 | `docs/failure-modes.md` input section repointed in S1 |
| Claude and Codex agents report differently | Q4 | The learned skill and the Feedback field change in one change, with the Codex skill copy regenerated |

## Contracts and schema

- `feedback-report.v1` (new, `contracts/learning-loop/`): the three record kinds and the envelope above,
  as a Pydantic model in `scripts/learning_loop/records.py`.
- Feedback field grammar: the four line markers above, in AGENTS.md and the learned skill.
- Licence: the metamodel's licence relation and R-401 calculus, evaluated by the metamodel's own
  evaluator where possible (`evaluate.py`), not reimplemented.
- Issue labels in the private log: `kind:observation|claim|action`, `family:<letter>`,
  `licence:active|conditional|unestablished|revoked`.

## Fixtures

- Positive: the 2026-10-07 stranded-lanes reports (observations linked to `file9.log` lines and the
  commit-rule log; the inferred claim; the Prevent action #2442) derive one problem and an active
  licence.
- Negative control: the same claim supported only by one session's observations derives
  `conditional`; a line with no link derives `unprovenanced` and no support.
- Negative control: a guessed claim ("my time limit caused it") never supports a licence.

## Thin slices

| Slice | What it delivers | Epistemic state |
| --- | --- | --- |
| S1 | Feedback field format in AGENTS.md and the learned skill; `records.py`; the collector reads the field and writes records to the private log; failure-modes input repointed | fully_specifiable_now |
| S2 | Labelled set of 30 record pairs from real reports; Jev's relation judgments measured; bar 8 of 10 acceptable; below it, the stronger model judges relations | exploration_required |
| S3 | Weekly grouping into problems and one stronger-model analysis per recurring problem | conditional on S2 |
| S4 | Licence derivation through the metamodel evaluator; agents adopt Prevent plans through `aes plan prepare` and the company-planning gate, and Detect checks into the audit skill; Brian's impact-and-uncertainty view and notifications | conditional on S3 |
| S5 | Effect counting per enforced rule; recurrence revokes the licence | conditional on S4 |
| S6 | Annotate the 68 existing issues and the legacy register with the new record split | deliberately_deferred |

Sequencing: starts now. An earlier line here sequenced it after vision milestone 4; that came from the planning agent's own recommendation, which Brian approved without comment, and no slice depends on milestone 4 (which ended unmet on 2026-10-06 and has no active lane). Corrected 2026-10-08 after Brian asked how the plan was blocked on vision.

## Status (2026-10-08)

| Slice | State | Evidence |
| --- | --- | --- |
| S1 | merged (AES #360, agent-skills #452, projects-dotclaude #104; llm_client #251/#252 hang fix) | first production run 2026-10-08 03:18 (`runs.jsonl` run of that time, journal `feedback-collector`): 83 reports (55 Claude, 28 Codex), 40 issues filed to the private log, 69 records, 22 without a link (all written before the line grammar shipped), 0 errors, $0.024; a random 15 links: 13 resolve, the 2 that do not are a bare `#316` (no repository) and a bare number qualified with the session folder's repository that belonged to another repository |
| S2 | done | S2 result above |
| S3-S4 | merged (AES #370) and running weekly; first production runs 2026-10-08 05:01-05:21 (`problems-runs.jsonl`, `problems-manual-2026-10-08{,b,c}.log`) | trace review of run b: Jev joined two unrelated incidents (#202, #221) whose record sentences were empty pointers; the analysis bridged them and two licences derived active; their concerns (AES #378, #379) were withdrawn before adoption and Brian was told once. Root fix: relations are judged with the linked issues' text. Run c on the same 69 records: 5 problems, 0 recurring, 0 errors (correct: nothing recurs yet). A real recurrence is still to come from nightly data; the weekly timer checks it |
| S5 | built | needs 30 days of nightly runs after the first enforced rule |
| Routes | OpenRouter credit exhausted 2026-10-08 (project-meta #2452) | Jev's endpoint still answers; the stronger judge and the analysis run on `FEEDBACK_STRONG_MODEL=claude-code/sonnet` (allowlisted) until credit returns |

Known limitation: a bare `#N` is qualified with the repository of the session's working folder; when the
agent meant another repository the link is wrong but still marked as a link. Agents writing the new line
grammar should write `owner/repo#N`; the skill's examples do.

## Success and what would disprove it

| Criterion | Run whose full trace is examined, and where | What must be seen beyond the outcome |
| --- | --- | --- |
| S1: reports become linked records | the first nightly collector run after S1 merges; `~/projects/data/feedback-collector/runs.jsonl` and the llm_client call log for that date (`~/projects/data/agentic-engineering-system-canonical/agentic-engineering-system-canonical_llm_client_data/calls_<date>.jsonl`; logs are per project) | each record's links resolve; no record carries retold evidence; link-free lines marked `unprovenanced`; Claude and Codex transcripts both parsed |
| S2: Jev's relation judgments are good enough | the S2 labelling run; its traces under `feedback-collector/relation-check/*` | per-pair answers against the hand labels; at least 8 of 10 acceptable, or the fallback chosen |
| S3-S4: a recurring problem yields a licensed proposal | the first weekly run that drafts a proposal; its run summary issue comment in the private log, and the stronger model's calls (trace id `feedback-loop/analyse/<problem>`) in `~/projects/data/agentic-engineering-system-canonical/agentic-engineering-system-canonical_llm_client_data/calls_<date>.jsonl` | the licence status derived by the evaluator from two independent observations; the proposal links back to every record it rests on |
| S5: the loop observes effect | the nightly runs for 30 days after the first enforced rule; each run's record is a line in `~/projects/data/feedback-collector/runs.jsonl`, its model calls in the llm_client call log for that date (`~/projects/data/agentic-engineering-system-canonical/agentic-engineering-system-canonical_llm_client_data/calls_<date>.jsonl`; logs are per project), and the per-rule counts in `~/projects/data/feedback-collector/effects-<date>.jsonl` | the per-rule count of matching observations before and after enforcement, the observations that matched (with their links), and any licence the counts revoked |
| Disproof | the same traces | adopted rules rest on single sessions or guesses; rules are adopted with no observation pattern; most adopted rules are revoked by their own effect counts; Brian reverses agent decisions after seeing the view; after 60 days no licensed rule has reached enforcement (judged from the nightly and weekly run records in `~/projects/data/feedback-collector/runs.jsonl` and the llm_client call logs (same per-project folder) for days 1 to 60 after S4 merges, each run showing the licences derived and any rule adopted) |

## Verification

Each slice's tests run under the repository's `make check`; the canonical example and its negative
controls are fixtures in `tests/learning/`; live behaviour is judged from the traces named above,
not from outcomes alone.

## The S2 measurement (the one comparison this plan proposes)

- **Decision it changes:** who judges whether a new record supports, challenges, or belongs to the same
  problem as an existing one. At or above 8 of 10 acceptable on the labelled set, Jev judges relations
  nightly. Below it, the stronger model judges them inside the weekly analysis and Jev only classifies.
- **Why it must be measured:** first principles say Jev suits fixed choices, and the inquiry-graph probe
  (`inquiry-graph/docs/goals/cross-conversation-linker.md` lines 155-200) found 6 of 15 stance matches
  on chat sentences, which is a different input. How Jev does on short agent reports with links cannot
  be reasoned out; only a labelled run shows it.
- **Parity:** a judge is compared only if it returns one of the four relations for every one of the 30
  pairs (no refusals, no free text) at the stated cost bound; below that it is out, not scored. Both
  judges get the same pairs, the same four answer options with the same definitions,
  the same fields (one sentence plus links, no transcript), and are scored against the same hand labels
  made before either runs.
- **Why it is cheaper than choosing now and correcting later:** the reversible choice now would be
  either judge. Choosing the stronger model now costs about $1 to $3 a week more for as long as it runs;
  choosing Jev now and being wrong corrupts licence statuses, which lead agents to adopt wrong rules
  that every agent then has to follow until their effect counts revoke them. The measurement costs
  under $1 and one run.
- **Why it is cheaper than guessing:** 30 pairs cost under $0.05 with Jev and under $1 with the stronger
  model, and the labels are reused as S3's regression fixture. Guessing wrong would make every licence
  rest on bad relations, and finding that later means re-deriving every licence.

### S2 result (2026-10-08)

Run: 30 pairs from 115 real reports (`scripts/learning_loop/relation_check.py`), hand-labelled with
every defensible answer before either judge ran (20 unrelated, 5 supports, 5 same problem; no true
challenge pair occurred). Pairs, answers and scores: private log repository,
`relation-check/2026-10-08/`. Traces: `feedback-collector/relation-check/{jev,strong}/<pair>` in the
per-project call log for 2026-10-08, 30 calls each, no errors.

| Judge | Acceptable | Related pairs right | False `challenges` on unrelated | Cost |
| --- | --- | --- | --- | --- |
| Jev (`typesafe/jev-1.13`) | 24 of 30 (bar 24) | 9 of 10 | 2 | $0.0006 |
| `openai/gpt-5.6-sol`, reasoning medium | 27 of 30 | 9 of 10 | 0 | $0.03 |

Decision (the rule fixed above): Jev judges relations nightly. Because a `challenges` relation blocks a
licence and Jev's only two `challenges` answers were both wrong, a Jev `challenges` answer is confirmed
by the stronger model before it counts. Wrong when: S3's hand check finds more than 2 of 10 licences
resting on a wrong Jev relation, or a confirmed true challenge is missed; then the stronger model judges
all relations. The 30 labelled pairs are S3's regression fixture; S3 adds real challenge pairs.

## Model calls

Call graph, in order (each arrow waits for the step before it; nothing runs in parallel across steps):

```text
nightly, per new Feedback line:
  parse markers (code) --missing markers--> [1] split (light model) --> record(s)
  record --> [2] triage (Jev, 4 fixed questions, independent of each other)
  record --> [3] relate to nearest existing record (Jev or stronger model per S2)
weekly, per problem with >= 2 independent observations:
  records of one problem (<= 40) --> [4] analyse (stronger model) --> new claim and action records
  claim --> licence status derived by the metamodel evaluator (code, no model)
```

All calls write to `~/projects/data/agentic-engineering-system-canonical/agentic-engineering-system-canonical_llm_client_data/calls_<date>.jsonl` with the
trace ids below.

| Call | Model (OpenRouter through `llm_client`) | Structured result | Traced as |
| --- | --- | --- | --- |
| Split a free-text Feedback field | `deepseek/deepseek-v4-flash` | `_Splits` (records: kind, text, verbatim excerpt; links read by code from the excerpt) | `feedback-collector/split/<report id>` |
| Kind, subject, family, intent | `typesafe/jev-1.13` via `call_decisions` | `ChoiceQuestion` answers with probabilities | `feedback-collector/triage/<id>` |
| Relation to nearest record | Jev, or the stronger model per S2 | one of four relations | `feedback-collector/relate/<id>` |
| Problem analysis | the stronger model chosen in S3 | claims and actions as records, each with links | `feedback-loop/analyse/<problem>` |

Provider and spend authority: Brian's configured OpenRouter route (workspace rule) and the shared
client's budgets. Promotion condition: a behaviour becomes the nightly default only after one authentic
run on real transcripts whose full trace has been read and whose records resolve their links.

## Ownership and coordination

- **Owner and integration owner:** this plan's lane (`claude-code`, claim `aes-learning-loop-o2a`); every
  slice merges through it.
- **Conflict surfaces:**
  - `scripts/learning_loop/` (this lane);
  - the `learned` skill in `~/projects/.agents/skills/learned/` and the Feedback field in `AGENTS.md`
    (shared, written by other sessions on 2026-10-07; changed only in S1 under a claim, with a message to
    any active owner);
  - `docs/failure-modes.md` (input section only);
  - the metamodel (read-only).
- **Dependencies:** S2 needs S1's records; S3 needs S2's verdict; S4 needs the metamodel evaluator's
  licence calculus to accept the licence record; S5 needs S4's enforced rules.
- **Each concurrent writer, its surface, and its evidence:**

| Writer | Surface it owns | Evidence its work leaves |
| --- | --- | --- |
| this lane (`claude-code`, claim `aes-learning-loop-o2a`) | `scripts/learning_loop/`, `tests/learning/`, this folder, the input section of `docs/failure-modes.md` | each slice's pull request with its `make check` result and the trace named under Success |
| the agent-skills repository (`BrianMills2718/agent-skills`, Brian's; last changed by #449 on 2026-10-07) | `skills/learned/SKILL.md` | its pull requests; this lane edits it only in S1, as an agent-skills pull request under its own claim there |
| the projects-dotclaude repository (`BrianMills2718/projects-dotclaude`, Brian's; Feedback field added in ea44c3b on 2026-10-07) | the Feedback field in `AGENTS.md` | its commits; this lane edits it only in S1, as a projects-dotclaude pull request under its own claim there |
| observation-to-action-metamodel sessions | the metamodel and its evaluator | read-only here; any needed change goes through the metamodel's decision process as a separate pull request there |
| the weekly labelling timer | labels on the log | its run-summary comment with counts and exit status |

## Boundaries

| Boundary | Owning authority | Rollback or containment | Disposition |
| --- | --- | --- | --- |
| Private chat content in reports | workspace rule: nothing private becomes public | the log lives in a private repository; the public repository holds code and ids only | contained |
| Change to every agent's Feedback field | AGENTS.md (project-meta source) and the learned skill | revert the one change; old reports remain readable | reversible, made in S1 |
| Migration of 68 issues and the legacy register | AES learning-loop design R7 | annotations are new comments; originals untouched | deferred (S6) |
| Rule enforcement | the loop's agent, by best judgment (Brian, 2026-10-07) | each rule names its effect pattern and retire trigger; a recurring failure revokes it automatically | agent-decided, observed |

## Detecting a silent parallel implementation

One structural check: a test in `tests/learning/` fails if any script other than `records.py` writes
feedback records (greps the repository for writers of the log's `kind:` labels and the legacy
`log_learning.py` call). One consumer-path observation: the weekly run summary counts records by the
code path that wrote them; any record from an unknown path is flagged in the summary.

## Activation facts

`shared_mechanism: true` (shared skill and closeout contract); `empirical_comparison_proposed: true`
(S2 measures Jev against hand labels and a fallback); `llm_central: true` (Jev and the analysis model);
`irreversible_or_spend_action: true` (model spend; bounded and authorized in Irreversible actions
and spend; no irreversible action: records are append-only).

## External-call budget

- Calls: Jev, about 4 fixed-choice questions per record; light extraction model only where markers are
  missing; stronger model, at most 3 problem analyses per week.
- Context bound: one problem's records, capped at 40 records per analysis.
- Cost and latency: measured in S1 and S3 canaries; stop and report if a nightly run exceeds $1.
- Completion evidence: the S1 and S3 traces above.
- Failure: a failed call leaves the record unsorted and counted, never guessed (DESIGN.md).
- Resume: records are keyed by transcript and offset; reruns process only new content.

## Prior art

Brian's: observation-to-action-metamodel (licence, R-401, PROV), vision register (evidence words),
inquiry-graph (claim, relations), epistemic-warrant (no single combined score), this folder's DESIGN.md.
External: nanopublications and W3C PROV (envelope and provenance), Google SRE postmortems (action
intents), ITIL problem management (incident versus problem), NASA ASRS (narrative plus later coding),
ExpeL and CoALA (agent experience stores revised over time). Research notes: session code-8c,
2026-10-07, research agent report; external sources partly cited from memory and to be checked in S1.

## Uncertainties

Owner of every item below: this plan's lane (`claude-code`, claim `aes-learning-loop-o2a`).

| Uncertainty | Kind | Why it is material (what changes if it is wrong) | Evidence that resolves it |
| --- | --- | --- | --- |
| Jev judges record relations well enough | resolved 2026-10-08 (S2 result above) | wrong relations corrupt every licence; the relation judge switches to the stronger model | S2's labelled run: at least 8 of 10 acceptable, otherwise the fallback |
| Independence means different sessions or days, each with a resolvable link | agent_decided_reversible | too loose and one noisy session licenses a rule every agent must follow; too strict and nothing is ever licensed | S3's first grouped problems: a hand check of 10 licences finds none resting on one session's echo |
| The private log is GitHub issues in a private repository | agent_decided_reversible | if issues cannot carry the volume or the S3 grouping, storage moves to a database and the ranked view reads that | S1: a record filed and read back from the private repository (done 2026-10-08, agent-feedback-log #1), and a scan of the public repository finding no record text |
| Agents write the Feedback grammar consistently | assumption | free text needs the light model on every line, its cost grows and its links depend on position rules | S1's first nightly run: the share of Feedback lines that needed the light model; above 30% triggers a grammar revision. Trial 2026-10-08 (before the grammar shipped): 100% free text, 23 of 92 records without a link |

## System model

Exemption: this plan changes one loop inside AES canonical whose components are listed in Design →
Flow; the AES system model is not changed.

## Delivery economics

```yaml
delivery_economics:
  implementation_surface: ~600 authored lines across records.py, the collector, the labeller and tests; one new contract
  first_authentic_vertical: S1, a real nightly run producing linked records in the private log
  verification_before_vertical: none beyond S1's own fixtures
  reversibility_consequence: shared (all agents' Feedback field), reversible
  strategy: build_then_learn
```
