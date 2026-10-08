<!-- Copied 2026-10-02 from agent-skills skills/review/references/failure-modes.md (legacy; sha256 in datasets/learning-loop/README.md). This copy is the AES label source for family:<letter> (proposals/aes-learning-loop/DESIGN.md). -->
# Failure Modes

The audit instrument for `review` and `audit`. Twenty-two families, each with a
**detecting question** — ask it of the artifact, then ask it of your own findings.

## Provenance, and how much weight this carries

Families A–G and J/K/L/M/N/O come from the ecosystem's original failure
taxonomy (v3), derived on 2026-08-21 from a frozen corpus of 315 recorded
diagnoses: 80 read and double-annotated, 235 scanned for missing categories,
then corrected against two external reviews. That is the derivation corpus for
those original families, not the current size of the learnings register and not
the source of the full taxonomy. Q was added afterward, and R–V came from later
register passes described below.
The complete locally recoverable derivation corpus, annotation, scripts,
research context, and revision-pinned AES snapshots are now under
[`provenance/2026-08-21-failure-taxonomy/`](provenance/2026-08-21-failure-taxonomy/README.md).
That directory is immutable source evidence; this file remains the current
taxonomy authority.

Do not cite 315 as the size or coverage of the current feedback corpus. Check
the latest taxonomy-feedback run for the live register count and its review
state. The scheduled pass emits candidates; until those candidates receive a
semantic disposition and an accepted change lands here, generation alone has
not updated the taxonomy.

Eight families marked **[register]** were derived separately from
`project-meta/learnings/entries/` and have no home in v3. R, S and T came from
the 112 failed lessons; U and V were added on 2026-08-28 from a
`make taxonomy-feedback` pass over all 786 entries, which flagged 81 as matching
no family. Their instance counts (35 and ~9) come from a phrase search over the
register with the matches sampled by hand, so treat them as the right order of
magnitude rather than exact.

**Two v3 claims were retracted. Do not cite them.** The causal ordering
`D·B·E → A → C → F` is a preregistered hypothesis, not a finding — the families
occupy those roles by construction, so any careful annotator draws the arrows
that way, and reverse edges were never searched for. And the
framing/assumption/proxy axis is not a general cause taxonomy; all three are
epistemic errors, one of three classes.

## Accepted inputs and maintenance contract

The recurring automatic input is the private feedback log
(`BrianMills2718/agent-feedback-log`): one issue per agent report, its records
(observations, claims, actions) in the `feedback-report.v1` contract of
`scripts/learning_loop/records.py`, filed nightly by
`scripts/learning_loop/collect_feedback.py` since 2026-10-08 (plan
`proposals/aes-learning-loop/`, slice S1). Assigning families to those records
and grouping recurring problems is slice S3 and is not built yet; until it is,
nothing reads the log into this taxonomy. The immutable Project Meta learning
register at `project-meta/learnings/entries/` was the input until 2026-10-08
and is history: it is read for duplicates and derivation, never added to.
Review findings, audit findings, policy friction, human corrections, concern
outcomes, skill feedback, and runtime incidents reach this taxonomy only as
records in the log; their native stores are evidence references, not parallel
taxonomy queues. The frozen 315-diagnosis bundle above is derivation evidence
and is never re-ingested as if it were new feedback.

The shared feedback runtime semantically dispositions each registered learning
as `covered`, `novel_candidate`, `taxonomy_changed`, or
`rejected_as_taxonomy_input`. A new family requires two independent instances.
The bounded queue reserves one fifth of each batch for the newest unresolved
entries and uses the remainder to drain the oldest unresolved evidence, so
current incidents do not wait behind history and history cannot be permanently
starved. Its evidence reports name the total reviewed and pending counts plus
the oldest and newest pending IDs.

This list is a floor. A defect fitting no family is still a defect. Generation,
token-overlap ranking, or an undispositioned candidate does not change the
taxonomy; an accepted edit to this file does.

---

## A — Verification that cannot fail
> *Could this check have gone red if the claim were false?*

- **A1** the check passes without the claim being true — existence checks graded as verification, swallowed exceptions, an absent optional input indistinguishable from a clean pass
- **A2** a substitute stood in for the real object — reading code instead of running it, mocks, sandboxes, fixtures, dashboards answering live questions
- **A3** the checker shares the author's blind spot — self-written tests instead of the project's own gate
- **A4** the property asserted is not the property that matters

*A1 and A4 collapse in practice; most records label either way. Treat the split
as a restatement, not a partition.*

## B — Reasoning that was never tested
> *What does this method assume, and what ordinary case breaks it?*

- **B1** wrong class of method for the domain
- **B2** the frame arrived with the task and was never questioned
- **B4** a sufficient-looking cause ended the search
- **B5** a signal counted as evidence for something it does not measure

*B3 (population described from examples that came to hand) was retired in v3 as
over-fitted — zero clean instances in 235 records. The learnings register
disagrees: 13 later instances, including a working-tree inventory reported from
a truncated pipeline and presented as complete. Treat B3 as open, not settled.*

## C — Parts pass, the whole does not
> *Has anyone executed the join, end to end, as a person would?*

- **C1** completion declared over a selected subset
- **C2** nobody executed the composition
- **C3** a hidden dependency on the local environment
- **C4** structure certified while ordinary use is broken

## D — Rules that do not act
> *What makes this fire, and who reads the result?*

- **D1** a prohibition in prose, with no mechanism — 85 violations at derivation
- **D2** a record nothing reads back
- **D3** an instruction nobody verified was read

For feedback consumers, follow one current source observation through extraction,
review, disposition and the next consumer. A report being generated does not
establish that anyone reviewed it or changed subsequent behavior. Distinguish
records discovered, substantive content read, decisions reviewed and changes
actually consumed; do not advance reviewed state from generation alone.

## E — Transitions that leave residue
> *Where else does this state live, and who was told?*

- **E1** changed in one place, still true in another
- **E2** retired logically, present physically
- **E3** a provisional artifact loses its provisionality at the point of use
- **E4** shared state mutated without telling its owner

## F — Controls out of proportion
> *What decision does this protect, and does it cost less than that decision?*

- **F1** verification heavier than the thing it protects
- **F2** a gate blocking unrelated work over inherited staleness
- **F3** enforcement whose remedy is unreachable
- **F4** a control that makes the correct action expensive

*A 258-minute deadlock is on record. F2's ~26 instances are 16-from-one-cluster;
one recurring incident, not a broad pattern.*

## G — The deliverable fails its reader
> *Can the reader act on this without decoding it?*

Nothing verified wrong; the communication failed. A completion claim without
scope. Internal vocabulary presented as a human approval burden. Status written
in machinery terms, making "must I act" unanswerable. Measured across 296
reports.

## J — Two authorities in force, mutually unsatisfiable
> *If I comply with this rule, does another rule currently in force now fail?*

Not the absence of a rule — the presence of two, never reconciled. Signature:
the agent cannot comply either way, and repairing one side makes the aggregate
strictly worse. ~11 instances.

## K — Ordering and atomicity in the control path
> *Does any irreversible mutation happen before the check that authorises it — or does a check depend on state a later step creates?*

Individually-correct steps in a sequence that voids the guarantee. A session
close that writes state before checking the caller's location, stranding the
lane. ~9 instances.

## L — The selector does not select what its name says
> *Does this identifier or filter actually partition the set it is trusted to partition?*

Every component behaves as designed while operating on the wrong object. A
`--repo-root` flag that added to a discovery set instead of scoping it, turning
a single-repo repair into a 79-repository mutation. ~9 instances.

## M — Zero read as success, or as absence
> *Can this path emit zero and still look like completion — and what makes zero loud?*

Also check for **nonzero records carrying zero substantive content**. Exercise
the current writer schema through the actual reader: IDs, categories, source
references and a successful exit can survive while the observation itself is
lost. Metadata is not a substitute for a body. Retain an ordinary valid-input
control so rejecting everything cannot pass. This occurred when a legacy-field
taxonomy reader omitted `learning` and `recommended_action` from learning/v3;
see Project Meta learning `lrn-20260912T171217358764Z-134c435fa7` and Agent Skills
PR 246. This example adds a detecting question, not a new family or a claim
that every schema adapter is defective.

A search skipping symlinked directories returns 0, "which reads as 'no hits'
rather than 'not traversed'." The most mechanically detectable shape in the
corpus: make the count explicit, exit non-zero on zero, say why nothing was
found. ~9 instances.

## N — The sanctioned route is impassable
> *Has anyone executed the exact documented entrypoint from a clean start since the guards last changed?*

The broken thing is the governance interface, so the agent's only remaining
moves are to violate policy or stop. ~15 instances, the largest new cluster.

## O — Work accumulating above a stopped producer
> *Between this effort's first and last commit, did any output a user consumes change?*

Correct, merged, productive work that could not have moved a user-visible
outcome, because what it sits on is stopped. Twenty-three PRs of dashboard
panels rendering a pipeline that had produced nothing since a key died.

## Q — Correlated premise across parallel agents
> *Did these agents share an assumption, and did anyone try to break it?*

N agents sharing a *supplied* blind spot. The signature is the opposite of A3:
the more agents agree, the more convincing the wrong answer becomes. Redundancy
makes A3 better and Q worse. Six subagents dispatched without the data model in
any prompt agreed with each other, and nearly two weeks of work was deleted on
the strength of it.

**Fresh context is not an independent premise.** Any design that fans out review
must carry the antidote: give every agent the canonical model and never the
orchestrator's conclusion, and task at least one per batch with falsifying the
parent premise.

## R — Enumeration treated as exhaustion **[register]**
> *What is not on this list that a competent person would try first?*

A list meant as a minimum, read — or written — as the complete set. Enumeration
steers behaviour: an agent handed a list of channels works that list and stops.

Recorded: analytical fields treated as exhaustive rather than as minimum
prompts. Then an evidence-escalation stage shipped enumerating official records
channels — SAM.gov, USAspending, FPDS, FOIA reading rooms — and omitting
ordinary web search. Same mode, already recorded, uncaught.

On the authoring side the tell is a list with no "this is a floor" clause and no
instruction to record routes taken beyond it.

## S — Scope or authority drift **[register]**
> *Does the deliverable's shape still match what was asked, and did anyone say so out loud?*

Recorded: an audit recommendation treated as authority to replace the session
objective; another session's related active claim treated as an assignment after
generic approval; prerequisite evidence work classified as drift because it
delayed the headline deliverable.

## T — Built before measured **[register]**
> *What is the baseline number, and when was it taken?*

The contender constructed before the baseline it must beat. Recorded: a runtime
acceptance criterion adopted without comparing it to the live baseline before
spend; a project lineage restarted on a narrative reframing of the predecessor's
failure instead of re-running the predecessor's own falsifying measurement.

## U — A claim asserted, then disproved by a check that was always available **[register]**
> *Was this stated as settled before the cheapest check that could have refuted it was run?*

Not a wrong answer reached honestly — a confident one published while the
refuting command sat one keystroke away. The tell is that the correction, when
it comes, costs a single inspection: reading the raw blocks, diffing the two
configurations, opening the section boundary.

Recorded: a session stated a number as evidence three times in one session, each
disproved by one check; an `llm_client` resume capability claimed from CLI
argument rendering alone, before the `CODEX_HOME` custody it actually depends
on; two OneDrive remotes described as separate Gmail- and Outlook-backed stores
from their labels, proved identical by one configuration comparison; 146
manifest lines called bibliography entries when the bibliography ends at 108.

35 entries in the register carry this shape, and at least two of them are
corrections *of earlier register entries* — so the durable findings surface can
itself carry a confident wrong diagnosis until someone re-runs the obvious
command. An audit agent produces this mode as readily as the work it audits.

The authoring tell is a claim whose supporting evidence is of a different kind
than the claim: a capability asserted from a rendered argument, a population
from a label, a chronology from an aggregate verdict.

## V — Verified from the wrong vantage point **[register]**
> *Whose account, host, and namespace was this observed from, and is that the one the claim is about?*

Every component behaves correctly and the observation is real. It was simply
made from somewhere the claim does not describe: a different identity, host,
filesystem namespace, browser profile, or checkout. The result is a status
reported globally that holds only locally — in both directions, since
"unavailable" asserted from the wrong identity is the same error as "connected".

Recorded: an HTTP 200 from inside WSL taken as proof the user's Windows browser
could reach the port; a SharePoint connector shown Connected in a browser
profile while a fresh CLI process on the same machine was a different principal
entirely; `docker` on `PATH` resolving to a Windows wrapper that timed out while
the native Linux client worked; an authenticated account inferred from a local
secret-key label; which checkout an installer ran from silently deciding how
stale a new repository started. ~9 instances.

The distinction from **C3** (a hidden dependency on the local environment) is
direction. C3 is *my* environment breaking *my* run. This is my environment
answering a question that was asked about someone else's.

## W — An implicit default spends an unbounded budget **[register]**
> *What happens when the caller omits this choice, and is that default bounded for the shared resource it reaches?*

An apparently exact request silently takes a compatibility, model-tier, query,
or retry default whose cost is materially larger than the caller intended.
The failure is not merely that a default exists: it selects an expensive or
unbounded allocation without an explicit decision, cap, or visible warning.
Recorded independently in an omitted dispatch tier that spent the costly
default and an exact-looking trace lookup that fell back to a leading-wildcard
full scan of a shared 28 GB database.

## X — One bad record erases the rest of an independent batch **[register]**
> *Can one stale or invalid member prevent the valid members from being seen, retained, or acted on?*

Batch handling treats a local defect as a global terminal condition, hiding
otherwise independent evidence. A feedback reader aborting on one malformed
row and a portfolio rollup suppressing every current dossier because one audit
became stale have the same shape: preserve and surface the exceptional member,
but continue rendering the independently valid remainder with its qualified
state.

## Y — One real object carries multiple identities **[register]**
> *Can overlapping representations of one thing enter the aggregate as distinct things?*

The data remains individually valid, but two schema fields, scopes, or identity
keys describe the same real-world constraint or object. Aggregation then counts
it twice and creates a false capacity, coverage, or inventory conclusion.
Canonicalize the object identity before aggregation, or explicitly supersede a
child scope when its parent is present. This is distinct from **L**: L selects
the wrong object; Y retains the right object more than once under different
identities.

---

## Turn it on your own findings

Reviewers produce all of these. The three most common in review output are
**B5** (a proxy read as the defect), **M** (absence claimed from a search that
could not have found it), and **A** (a verification that would have passed
anyway).

A finding that survives its own detecting question is worth reporting. One that
does not is worth one more command first.

**The register's own corrections are family U.** Two entries retract earlier
entries in the same register — a durable findings register that can carry a
confident wrong diagnosis for a day is itself a failure surface, and an audit
agent makes the same error as readily as the work it audits. That gap was named
here without a family for it until 2026-08-28; U now covers it, and the
detecting question applies to this file as much as to anything it is used on.
