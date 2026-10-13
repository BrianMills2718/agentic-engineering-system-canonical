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

## Correction (Brian, 2026-10-13)

The interview kit is a light version Brian built for a timed interview that forbids his full
tooling. It is not the standard for Inside Success repositories. The standard there is Company
Planning decision 0003 (`Inside-Success/company-planning`,
`docs/decisions/0003-plans-keep-durable-documents-current.md`, the org copy teammates can open).
The kit stays a source of ideas only: decided/guessed marking, the owner question order, and
model protection (BrianMills2718/company-planning#167).

Still standing from 2026-10-13: the Project Brain does a first pass from the owner's code and
docs, then asks the owner one question at a time with a suggested answer; nothing is moved.
Pilot: Mock Call Agent (owner Jawad), the PCH-1 pilot from the 2026-10-08 roadmap
(`Inside-Success/2nd-brain-plan-repo` `integrated/ROADMAP.md`).
