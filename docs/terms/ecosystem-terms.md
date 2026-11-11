# Ecosystem terms (Brian's reasoning and decision vocabulary)

Status: first entries, 2026-10-05. A controlled vocabulary: one meaning per
term, usable in any project. It is a terms list, not an architecture authority.
Planning-runtime words (accepted, approved, claimed, ready, ...) live in
`agent-skills/contracts/terminology.md`; do not duplicate them here.

## How to read an entry

Each entry has the same fields: **Plain** (an everyday example first, then the
definition), **Brian's work** (one example), **Brian's words** (only where he
said it; quoted from documents listed in Sources), **Is not**, **Used in**, and
**Status**, one of:

- `stated by Brian`: the definition is his own words or his recorded decision.
- `drafted from his usage`: an agent wrote it from how he uses the term. Brian
  should correct it; until he does, treat it as a draft.
- `open question`: the meaning is not settled; the open point is named.

Each entry has a stable id (`term:...`). To publish as SKOS later, an id becomes
a concept IRI, Plain becomes `skos:definition`, and the optional `Links` line
holds `skos:closeMatch` / `skos:broadMatch` to outside vocabularies. No tooling
is built; the format is kept simple so a script can convert it.

## Index

| id | term | status |
|---|---|---|
| term:mece | MECE | drafted from his usage |
| term:canonical-factorization | canonical factorization | stated by Brian (example), definition drafted |
| term:move | move | drafted from his usage |
| term:motif | motif | open question |
| term:instance | instance | drafted from his usage |
| term:method | method | drafted from his usage |
| term:policy | policy | stated by Brian (separation), rest drafted |
| term:position | position | drafted from his usage |
| term:stance | stance | drafted from his usage |
| term:formalization-axis | formalization axis | stated by Brian (placement), definition drafted |
| term:money | money | drafted from his usage |
| term:time | time | drafted from his usage |
| term:attention | attention | drafted from his usage |
| term:reversibility | reversibility | drafted from his usage |

## Terms

### term:mece (MECE)

- **Plain.** Sorting laundry into whites, darks and colors, where every item
  goes in exactly one pile and nothing is left over. MECE (mutually exclusive,
  collectively exhaustive) means a way of splitting a whole into parts with no
  overlap and no gaps.
- **Brian's work.** The inquiry-graph walkthrough shows him starting from MECE
  as a way to search for the basic pieces of a domain, then noticing it fails
  when the thing is not a partition (conversation-walkthrough section 19).
- **Brian's words.** None recorded as a definition.
- **Is not.** The general method for finding primitives. It is the special case
  of canonical factorization where the target really is a partition.
- **Used in.** inquiry-graph (walkthrough 19, seed-review).
- **Status.** drafted from his usage.

### term:canonical-factorization (canonical factorization)

- **Plain.** A kitchen has a few basic operations (chop, heat, mix, season) and
  thousands of recipes are combinations of them. Canonical factorization means
  reducing a whole to a small set of primitives that other things compose from,
  and checking the result for gaps (underfactored), needless pieces
  (overfactored) and mixed-up kinds of piece (misfactored). These checks are
  relative to the stated representation, not facts about reality.
- **Brian's work.** Social-science methods: quantitative (statistics, causal
  analysis, forecasting), qualitative (tagging/coding), simulation, elicitation,
  literature review.
- **Brian's words.** "even in social science i think there are a small number
  of categories of methodologies that have a canonical factorization that is
  pretty small." (vision/notes/2026-10-04-owner-vision-clarification.md)
- **Is not.** A single move. It is a strategy made of several steps (propose
  pieces, test, revise); do not label every decompose move as using it. It is
  not a claim that every domain has a small basis; the program thesis keeps
  primitive sufficiency probationary ("let primitives earn their place").
- **Open question.** Whether primitives may overlap. Not asserted as a rule
  here. Default recommendation: say "overlap is allowed only if declared in
  the representation" until Brian answers.
- **Used in.** inquiry-graph (walkthrough 19 and 22); the program thesis.
- **Links.** broadMatch: none yet.
- **Status.** stated by Brian (the example and the idea); the one-line
  definition is drafted.

### term:move (move)

- **Plain.** In a conversation about a problem, someone says "wait, what do you
  mean by that?" That is one move: a single thing a person does while thinking
  something through. A move has who did it, what it started from, what it
  produced, and where in the text it happened.
- **Brian's work.** inquiry-graph records 15 in-house move kinds: ask, clarify,
  distinguish, challenge, retract, hypothesize, generalize, deduce, test,
  reframe, decompose, connect, scope, summarize, propose
  (inquiry-graph/docs/ontology.md).
- **Brian's words.** None recorded.
- **Is not.** A claim or a position (those are content). Not a stance event:
  retracting is a move (the episode), and a "retracts" stance event is the
  actor's change toward one target; they are related, not redundant.
- **Used in.** inquiry-graph. As of 2026-09-29 the live extractor captured 0
  moves in 2,176 graphs (capture-contract.md, project-status).
- **Links.** The 15 kinds are the candidates to publish as SKOS concepts, with
  closeMatch/broadMatch to outside move taxonomies (the move-taxonomy survey's
  recommendation; not done).
- **Status.** drafted from his usage; the list of 15 is in-house.

### term:motif (motif)

- **Plain.** A song has a short tune that keeps coming back in different keys.
  A reasoning motif is a short pattern of moves that keeps coming back across
  many conversations, found by looking at many instances and grouping them.
- **Brian's work.** "Induction, abduction, analogy ... are now treated primarily
  as candidate-generation or reasoning-trajectory motifs" (walkthrough, line
  187); the plan is to mine motifs upward from his own short messages
  (semantic-spectrum-and-motifs.md section 4).
- **Brian's words.** None recorded as a definition.
- **Is not.** Not a method until Brian keeps it: the note says a method counts
  only if its instances recur across topics and years and Brian decides which
  stay.
- **Used in.** inquiry-graph (design note, working status).
- **Status.** open question. Recommended default: motif = a mined, unconfirmed
  pattern; method = a motif Brian has confirmed.

### term:instance (instance)

- **Plain.** "I chose the cheaper plane ticket on Tuesday" is one case; "when
  two options tie, pick the reversible one" is the general habit drawn from
  many such cases. An instance is what Brian thought or did about one specific
  thing.
- **Brian's work.** The 2026-09-29 choice to leave moves out of the live
  extractor for one goal is an instance; the capture-contract rule is the
  general habit drawn from it.
- **Brian's words.** The note names three layers, "instances (what he thought
  about a specific thing), methods (general moves), policies (prescriptions)",
  as a working hypothesis, not fixed bins.
- **Is not.** Not an example node in a graph by default (an example node can
  record an instance, but the term is about the layer).
- **Used in.** inquiry-graph design note section 3.
- **Status.** drafted from his usage.

### term:method (method)

- **Plain.** A recipe says how cooking is done; it does not tell you what you
  must cook. A method is a general, descriptive way of moving a piece of
  thinking forward (define by role, factor into primitives, ask for a concrete
  example, test by acting).
- **Brian's work.** Process tracing and grounded theory as compositions of
  qualitative coding, statistics, simulation, elicitation (design note section
  3).
- **Brian's words.** None recorded.
- **Is not.** Not a policy: a method describes what is done; a policy says what
  must be done.
- **Used in.** inquiry-graph (method nodes are reusable strategies).
- **Status.** drafted from his usage. Where a method is cut from its instances
  stays revisable.

### term:policy (policy)

- **Plain.** "Look both ways before crossing" is a standing rule that says what
  to do, whatever the street. A policy is a prescriptive standing rule. It is
  kept separate from methods, which describe moves.
- **Brian's work.** "use what exists", "reuse my own repo" (design note section
  3).
- **Brian's words.** The separation (policies are prescriptive rules, kept
  separate from methods) is recorded in the design note as his clarification.
- **Is not.** Not a method, and not a one-off decision.
- **Open question.** Whether "prescriptive" is a separate axis or the far end of
  the same one as methods (asked 2026-10-05, unanswered).
- **Used in.** inquiry-graph; AES AGENTS-style rules.
- **Status.** stated by Brian (separate from methods); the rest drafted.

### term:position (position)

- **Plain.** Asked "do you think we should move?", you might say "yes, if the
  job pays more." Your position is where you stand on that claim, including
  the condition. A position is an actor's standing on a claim or question,
  rebuilt from a series of stance events.
- **Brian's work.** The position-memory goal: remembering what Brian has
  actually said about a topic (extraction-position-memory contract).
- **Brian's words.** None recorded as a definition.
- **Is not.** Not belief proven: an assistant's statement is not Brian's
  position merely because he kept talking (formalism.md).
- **Used in.** inquiry-graph formalism; the brian-positions skill.
- **Status.** drafted from his usage.

### term:stance (stance)

- **Plain.** At a meeting you can nod, ask a question, say no, say "not sure
  yet", or take back what you said. Each of those is a stance toward one
  specific claim at one moment. Six kinds are recorded: posits, endorses,
  questions, rejects, suspends, retracts.
- **Brian's work.** A user challenging an assistant's suggestion yields a
  retracts stance event for the assistant without assigning the user an
  endorsement (ontology.md, imagination example).
- **Brian's words.** None recorded.
- **Is not.** Not the position (the standing built from many stances). Not the
  program's "human-guided stance" in the thesis, which means a product
  posture; use "posture" for that.
- **Used in.** inquiry-graph (StanceEvent).
- **Status.** drafted from his usage.

### term:formalization-axis (formalization axis)

- **Plain.** A shopping list, a recipe card, and a working kitchen robot are one
  idea at three levels of precision. The formalization axis is that range, from
  a rough list of concepts, through glossaries and taxonomies, typed relations
  and logical constraints, up to an executable, simulated or verified model.
  Working an idea moves it along the range.
- **Brian's work.** inquiry-graph's per-chat graphs sit roughly at "frames"
  (typed relations over claims, questions, methods); the topic digests nearer a
  catalog. This terms list itself is at the glossary level.
- **Brian's words.** He asked for the semantic spectrum to be understood as one
  range of formality (design note section 1, recorded as a clarification).
- **Is not.** Not the only dimension. It is axis 4 of seven (purpose, method
  family, theory posture, formalization, data form, execution, human view) in
  `vision/wiki/synthesis/formalization-megamodel-and-selection.md` (archived,
  derived); the owner's rule is not to flatten the seven into one ladder.
  "Executable" is partly axis 6.
- **Used in.** vision (archived page), inquiry-graph design note.
- **Links.** closeMatch: the published "ontology spectrum".
- **Status.** stated by Brian (placement and no-flattening rule); definition
  drafted.

### Utility primitives

Four basic currencies for weighing a choice. Drafted from his usage; the first
three are named together in the capture contract ("time and attention to redo,
converted to USD"); reversibility is the standing test in his workspace rules
for when to proceed without asking. Whether these four are complete or
independent is itself an open question (see canonical factorization).

### term:money (money)

- **Plain.** Paying $7.69 to run something once. Money is dollars spent, the one
  currency everything else can be converted into when comparing options.
- **Brian's work.** The full OpenRouter extraction pass cost $7.69.
- **Brian's words.** None recorded as a definition.
- **Is not.** Not the only cost; time and attention are converted to it only
  when a decision needs one number.
- **Used in.** capture contract; LLM spend rules.
- **Status.** drafted from his usage.

### term:time (time)

- **Plain.** A job that takes three hours of the clock to finish, whether or
  not anyone watches. Time is elapsed duration to get an outcome.
- **Brian's work.** The three-hour Google Drive backup caused by 94,000 small
  files.
- **Brian's words.** None recorded as a definition.
- **Is not.** Not attention: a long unattended run costs time but little
  attention.
- **Used in.** capture contract (redo time); the speedrunning rule.
- **Status.** drafted from his usage.

### term:attention (attention)

- **Plain.** Reading a ten-page report you must judge costs your focus, even if
  it takes only ten minutes. Attention is Brian's own time and focus when he
  has to read, decide or click.
- **Brian's work.** "ten minutes of attention valued at $10" flips a skip to a
  capture in the capture-contract worked example.
- **Brian's words.** None recorded as a definition.
- **Is not.** Not an agent's compute time; only Brian's own focus counts.
- **Used in.** capture contract; reporting and escalation rules.
- **Status.** drafted from his usage.

### term:reversibility (reversibility)

- **Plain.** Moving a couch can be undone by moving it back; deleting a
  database cannot. Reversibility is how cheaply and completely a choice can be
  undone after it is made.
- **Brian's work.** Merges are done without asking when reversible; only
  irreversible actions get a question.
- **Brian's words.** None recorded as a definition (the merge rule is his;
  the definition here is drafted).
- **Is not.** Not safety: a reversible action can still be wrong.
- **Used in.** merge and deploy rules; capture-contract "redo" cost is its
  money/time measure.
- **Status.** drafted from his usage.

## First worked use of the primitives: capture an extra field now

Rule, adopted by Brian 2026-10-05: before an expensive run, capture an extra
field now if `f*C < p*R`.

- `C`: the cost (money) of the pass. `f`: the extra cost of capturing the field,
  as a fraction of `C`. `p`: the chance a later use needs the field. `R`: the
  cost of redoing, `C` plus the extra redo cost, where time and attention to
  redo are converted to dollars.
- Plain example: while already at the shop, adding one more item costs a little;
  coming back later costs a whole trip. If the chance you will need the item is
  high enough, buy it now.
- Money only: capture if `f < p`. Worked numbers: `C = 7.69`, `p = 0.3`,
  break-even extra cost `$2.31`; `f = 0.10` captures, `f = 0.40` skips, and ten
  minutes of attention valued at $10 flips the second to capture.
- Uses money, time and attention directly; reversibility enters through `R`
  (a field that can be added later at low cost lowers `R`).
- Source: `inquiry-graph/docs/design/capture-contract.md`. Wrong-when
  conditions are recorded there.

## Open questions, with defaults

1. Primitives may overlap? Default: only if declared in the representation.
2. Is "prescriptive" a separate axis from method? Default: separate layer
   (policy) as now.
3. Motif versus method? Default: motif = mined, unconfirmed; method =
   confirmed by Brian.
4. Are money, time, attention, reversibility complete and independent?
   Default: probationary set, add a fifth only when a real decision needs it.

## Sources

`vision/notes/2026-10-04-owner-vision-clarification.md`;
`vision/wiki/synthesis/automation-of-knowledge-work-program-thesis.md`;
`vision/wiki/synthesis/formalization-megamodel-and-selection.md` (archived,
read only); `inquiry-graph/docs/ontology.md`, `docs/formalism.md`,
`docs/conversation-walkthrough.md` (sections 19, 22), `docs/seed-review.md`,
`docs/design/semantic-spectrum-and-motifs.md`,
`docs/design/capture-contract.md`.
