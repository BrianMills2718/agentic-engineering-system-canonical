# Alignment addendum (2026-10-13)

`crosswalk.json` is the output of the doc-standard-alignment run (2026-10-13): five inventories
(Company Planning, AES canonical, workspace rules and skills, Inside Success plans, external
standards), one crosswalk over 15 concerns, 21 conflicts with resolutions, 16 changes by owner
repository, and the order to walk owners through, after a citation check and a refuting critic.
It is synthesis: no checker was run and no file changed.

## Sixth source the run did not read: interview-kit

`BrianMills2718/interview-kit` is Brian's one-person compression of the same method
(`method/README.md`: "adapted from a fuller planning method"). It supplies:

- **Small-project form of decision 0003:** `docs/MODEL.md` (six Mermaid diagrams: context, agent
  loop, main sequence, rules, states, data; Runtime, Contracts, Quality and Unknowns tables; every
  element `decided` or `guessed`), `docs/DESIGN.md`, `docs/DECISIONS.md` (choice, why, rejected,
  what proves it wrong). Templates in `templates/`; method in `method/system-model.md`.
- **Owner question order:** intent (who uses it, what they get, what done looks like) ->
  requirements quoted R1.. -> questions one at a time, each with a recommended answer -> answers
  recorded as assumptions A1.. (`MEMORY_SHEET.md` prompts 2-3).
- **Model protection:** "test what the diagrams forbid"; "never change a diagram or a test just to
  make the code pass" (`MEMORY_SHEET.md` prompt 10). The two-direction drift test it uses already
  exists in Company Planning (`distribution/references/system-model.md` item 2).

## Brian's decisions on 2026-10-13 ("i approve")

1. Inside Success repositories use the interview-kit three files as the small-project form of
   decision 0003, drafted by an agent from code and owner docs, nothing moved. This answers the
   crosswalk's C16 for the content; C16's enforcement half (report_only, no plan gating) still
   needs schema v0.2.
2. The Project Brain walks the owner through open questions in the interview-kit order.
3. Proposal to Company Planning filed: BrianMills2718/company-planning#167 (never weaken a model
   to pass; negative tests for what the diagrams forbid; decided/guessed marking).

Pilot: Mock Call Agent (owner Jawad), the PCH-1 pilot from the 2026-10-08 roadmap
(`Inside-Success/2nd-brain-plan-repo` `integrated/ROADMAP.md`). Nothing reaches the owner before
Brian has seen the first three questions.
