# Model framework: checked models through plan, build and review

Status: shaping (not adopted)
Role: living design record for one conversation thread; update it in place
Authority: proposed only
Started: 2026-10-10, from a session that began as a review of `fol-operational-metamodel`

**Resume here.** This file holds the decisions, disagreements, verified facts and open
questions so they survive context compaction. Update it whenever any of them change.
The section "Open decisions" says what is waiting.

## 1. What Brian is after

- Understand and steer agent-built systems through **formal, checked visual models**, used
  alongside text, not instead of it. It started with trying to understand the
  observation-to-action repo, where the pictures kept being unclear.
- The deeper problem is the "spiral" repos: qualitative_coding, Digimon, onto-canon and ac17.
  Brian: "most of my projects if properly planned and modeled could be completed in a couple
  days but i have been working for years on them in cascading spirals of failures that never
  converge."
- It needs **an architecture framework, not one model**: several kinds of model, each in an
  established notation, tied together.

## 2. Agreed principles

1. **What exists is generated; what is intended is hand-written.** Diagrams of what exists
   come from the code. Diagrams of intent are written by hand, in a defined notation, before
   building. A program compares the two (Brian: "the automatic comparison i think is huge").
2. **Arrows only mean something in a defined notation.** That is why established languages
   are reused.
3. **Status is computed from checks, never claimed.**
4. **The model has a job in every phase.**
   - Planning: Brian confirms the agent will build what he wants.
   - Building: tests and success criteria enforce the model.
   - Review: a working UI or demo where relevant, linked to the status of each model element.
   - Work is cut into thin vertical slices.
5. **Full traces.** Review, success criteria and agent debugging see the full trace of each
   fixture (the whole data flow, not only the output), and can run new inputs.
6. **Every formal layer needs a program that checks it and someone who uses it.** Reuse
   across the ecosystem justifies going deeper than one project would.
7. **Reuse first.** Brian's own existing pieces come first, then off-the-shelf tools, and
   building is the last resort.

## 3. Disagreements and how they resolved

| Topic | Positions | Landed |
|---|---|---|
| Examples vs definitions | An example teaches a term; Brian: an example is not a formal definition | Provide both, every time |
| Semantic spectrum | Agent: a spectrum from vocabularies to logic. Brian: too narrow, since operational semantics, domain, dataflow and UML models matter | The framework covers model kinds beyond that spectrum |
| Cost of formalizing | Agent: formalizing everything costs too much. Brian: worth it when reused across projects | Brian's view, with the condition that each layer has a checker and a consumer |
| Why projects spiral | Agent: a missing purpose and finish line. Brian: "both", and a prose goal is underspecified while a diagram makes it precise | Both. The qualitative_coding test showed 5 choices the prose never made, and the code had already gone a different way on 2 of them (qc #130) |
| factgraph | Agent recommended it first. Brian: something off the shelf must be better | Research agreed: LinkML, Atlas, Great Expectations, erdantic, import-linter, PM4Py and TLA+ cover the field. factgraph's only uncovered job is a live test of whether a real database enforces each rule, run 0 times so far |
| One format vs framework | Agent drifted to "one model format". Brian: we discussed a framework | Framework. Only shared element IDs and the index of models need one form |
| Precision depth (2026-10-10) | Agent: make models precise only to the depth of the next slice. Brian: upfront planning is almost always worth it, so an agent can run for a day unattended; for real unknowns, plan how to resolve them and the decision criteria | See section 4 |

## 4. Planning depth: current position

The rule "precise only to the next slice" is **withdrawn**. It mixed up *deciding* with
*guessing*.

Replacement rule:
- **Decide everything that can be decided now, precisely.**
- **Write down how to resolve each real unknown**: the question, the experiment, its budget,
  the criterion that decides it, and the default if the result is unclear.
- **Mark every precise item** as *decided*, with its source, or *guessed*, with the evidence
  that would change it.

Pushback that still stands:
1. **A plan alone doesn't keep a day-long run on track.** Checks do. Without computed checks,
   a detailed plan just gives the agent more confident text to drift with. Plans existed
   throughout the spirals; for example, Digimon plan #215 was superseded by #216.
2. **A precise guess is worse than a vague one.** The agent builds it faithfully, it passes
   its own checks, and nobody notices it was a guess.
3. **Brian's review is the bottleneck.** A plan he can't actually check is no better than
   none, so its size is bounded by what he can review in diagrams.
4. **Every unknown needs a stop rule and a fallback**, or exploring it becomes the next spiral.

Prior art:
- **Set-based concurrent engineering** (Sobek, Ward and Liker 1999): keep alternatives open,
  narrow them on feasibility.
- **Last responsible moment** (Poppendieck): the point where not deciding removes an
  important alternative. Deciding *how* to decide is cheap, so it belongs up front, which
  fits Brian's position.

## 5. The framework (proposed shape)

1. **A catalogue of model kinds**, each in an established notation, and each with a
   generated "actual" side:
   - domain (ER or LinkML; actual drawn by erdantic);
   - data flow;
   - behaviour (state machine);
   - physical schema (actual checked by Atlas);
   - run trace.
2. **Correspondence rules between kinds, written as tests.** Example: "Judgement" in the
   domain model must match the `CodeApplication` table, the "judge" step in the data flow,
   and the `judge_segment` step in a real trace.
3. **An index of models (a megamodel)**:
   - for each model: its kind, its notation, which element IDs it covers, its slice, and its
     computed status;
   - links between models: `representationOf`, `conformsTo`, `refines`, `generatedFrom`,
     `checkedAgainst`.
4. **Levels and aspects are two separate axes.**
   - Level: conceptual, logical, physical.
   - Aspect: structure, behaviour, interaction.
   - Each model is also tagged intent or generated.

## 6. Existing pieces to build on

| Piece | Where | Gap |
|---|---|---|
| ODD-style system models | `docs/model/ODD.md` in 10 repos | Formats differ (see section 7); the validator only checks the file exists; everything is Markdown tables; no generated side |
| View coverage matrix | `docs/model/VIEW_COVERAGE.md` in 8 of those repos | Tracks "shown in a diagram", not "built and verified" |
| Source-linked review page | AES `proposals/system-model-review/` | One flow only |
| Trace review | AES `proposals/trace-review*` | Runs per plan, not per model element |
| LinkML project model, view catalogue, generated views | ai-astronauts `brian/project-model/` | Runs (agent check 2026-10-10, scratch copy): model checker 0 errors, 15 views selected, 3 shown / 12 gaps, tests 34/34 and 18/18 pass, regenerated outputs match committed ones. Friction: needs `COMPANY_PLANNING_ROOT`; tests run only as scripts, not under pytest. The closest existing seed for the megamodel index |

## 7. Verified facts and corrections (2026-10-10)

- **What ODD means.** ODD = Overview, Design concepts, Details. It is the Grimm et al. (2006)
  protocol for describing agent-based models, updated in 2010 and 2020
  (https://www.jasss.org/23/2/7.html).
  - company-planning's file calls itself "ODD-style, small-project size". It keeps Purpose,
    Entities and Processes, adds Boundary, Events, Views and others, and drops Design
    concepts, Initialization, Input and Submodels.
- **Correction: the 10 ODD files do not share one format.**
  - Roughly 7 use a loose company-planning-style outline.
  - agent_ecology3 follows real ODD; brent-chatgpt is ad hoc; enforced-planning has 3
    sections.
  - The validator (company-planning `method_conformance/quick.py:274-276`) checks only that
    the file exists.
- **Correction: SysML v2 / KerML 1.0 date.** OMG pages say formal, published September 2025.
  The earlier "2025-07-21" is unconfirmed.
- **Confirmed:** PM4Py does conformance checking by token replay and alignments. Atlas does
  declarative schema diff, drift detection and migration linting. Set-based design as
  described above.
- **Not yet verified against primary text**, so treat these as drafts:
  - ISO 42010 definitions (paywalled);
  - Harel & Rumpe's syntax / semantic domain / mapping triad;
  - Favre's `conformsTo` (only `RepresentationOf` confirmed);
  - linguistic vs ontological instantiation, likely Atkinson & Kühne 2003 rather than
    Kühne 2006.

## 8. Open decisions

1. **Extend the ODD convention into this framework, or start fresh?** Recommendation:
   extend, because the files already exist in 10 repos. Normalizing their formats becomes
   part of the work.
2. **Pilot.** qualitative_coding slice 1, with four kinds (domain, data flow, a quote's
   states, trace), two or three correspondence tests (one model ↔ trace), and a status
   overlay. A full plan is needed before building.

## 9. Related records

- qc issue #130: the qualitative_coding goal and its schema disagreements.
- AES #517: the main checkout is not refreshed (found during this thread).
- `fol-operational-metamodel`: the Common Logic class diagram and meaning layer (done).
- Goal-vs-code page for qualitative_coding: [review-page/qc-goal-vs-code.html](review-page/qc-goal-vs-code.html), served at https://hive.brianmills.dev/plans/shaping-model-framework/proposals/model-framework/review-page/qc-goal-vs-code.html
  (two ER diagrams and the disagreement table; first worked example of an intent model
  compared with a generated one).
