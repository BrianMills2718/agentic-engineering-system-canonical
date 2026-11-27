# AES game benchmark: one-page plan (2026-11-26, revised after one cold read)

Source: Brian, 2026-11-26: "maybe like a video game is a better test ... we need to have all the required features up
front and then tell both to satisfy them all. but its got to be non trivial". Replaces the TinyDB test (too easy; its
hidden tests graded private-name guesses; next.goal.md, "aes_test result").

Plan size: small planned work (no outward send, spend about $60 or less, nothing another repository reads).
Independent read: reviewer subagent, 2026-11-26 13:20; its 8 findings are folded in below (marked R1 to R8).

## Decision this settles

Does the AES bundle (template, project instructions, planning package, `make check`, Lockstep gates, hooks) make a
builder deliver more of a long, interdependent feature list than the same builder bare, in the same time? (R2: this
tests the bundle, not the gates alone; a gates-off third arm is on the parking list.)

- Measured per item, reported as per-run scores with their spread, not a single pass/fail (R1).
- The bundle helps if every ON run beats the mean OFF run by more than the OFF runs' own spread; it hurts if the
  reverse; otherwise no measurable effect. With 3 runs per arm this detects only a large effect, which is what would
  justify the paperwork; a small one would not.

## Prior art: A2Z GameSpec-Bench (decision: combine)

- KRAFTON, arXiv 2609.39564, MIT. 100 browser game design documents (50 Big, Phaser 2D) with fixed contracts
  (requirements, rules, invariants, scenarios, state sources) and a sprite library per game.
- Their grader is "available soon" (README, 2026-11-26). We use their specs and contracts with our own grader; our
  scores are NOT comparable to their published 71.1 / 51.1 (R7). Re-grade with theirs when it ships.
- Also seen, not chosen: GameCraft-Bench, SWE-Game (Godot), CEGame-Bench, PRDBench, TDDev.

## Setup (run protocol, frozen before the first build: R8)

- Game: `abyssal_chain` (sample copy: /home/brian/projects/data/aes-gamebench/sample/) (Big; 17,725-word document; 47 requirements, 25 rules, 21 invariants, 23 scenarios).
  Second game only after this one shows the method works.
- Pilot first (R6): a light model reads the document against each contract item and marks it decidable or not from
  the document alone; undecidable items are dropped before any build and the list is saved.
- 3 builds per arm, 6 in all, run one at a time, alternating ON/OFF. Claude Code, Sonnet (pinned model id), the same
  Phaser version and sprite library copied in, 3 hours wall clock total per build including any planning (R4).
- Same prompt both arms, including "test your work as you go" so ON is not the only arm told to test (R3):
  "Build this game in Phaser 2D from the attached design document, using the attached sprite library. Every
  requirement in the document must work. Test your work as you go."
  - ON: repository from the AES template (`copier copy`), project instructions loaded, `make check` and hooks on.
  - OFF: plain repository, the same user-level instructions, no project instructions, no hooks.
- Logged per build: time per phase, which gates fired and what they refused (R3, R4), stream-json trace.
- A build that does not launch scores 0, no retry; a capped build is graded as it stands (R8).

## Grading (R5)

- On running behaviour first: scenarios replayed in Playwright from the contract's input sequences, plus a play
  session per build; source is read only for items no scenario reaches, from a copy with AES files removed (template
  files, hooks, Makefile, docs/planning) so the arm is not visible.
- Grader is a different model family from the builder (Codex, GPT), one session per build, per-item pass, partial or
  fail with evidence (screenshot, replay log, file:line). Score = mean over items (pass 1, partial 0.5).
- Calibration: one build graded twice (agreement and kappa reported); 30 verdicts hand-checked, 15 per arm.
- Full trace kept: builder and grader logs, per-item verdict JSON, screenshots.

## Cost and time (guess)

Builds about $6 to $10 each (TinyDB builds: $3.66 and $5.72 for about 20 minutes); grading about $3 each; pilot under
$1. Total about $40 to $80. Wall time about one day.

## Blockers

- Disk: `storage-policy` refuses at C: 8.7 GB free; builds start after tonight's rebuild frees C:.

## Parking list (later slices)

- Third arm: template and instructions without gates or hooks (R2). Second and third game. Official A2Z grader.

## Results

- Step 1, decidability pilot (2026-11-26 19:10): Claude Haiku, one call, the whole document plus all 116 items; cost
  $0.16 (measured, `pilot-out.json`). 111 decidable, 5 flagged: requirement R1 and rule R1 ("Endless is armed" is never
  defined; the Descend Deeper choice implies it), invariant SYN-INIT-runseed (counter origin not defined), scenario
  chain_cluster (flag is wrong: the 12-link cap is stated at document line 190 and the scenario tests it), scenario
  enemy_roster_zone1 (spawn distance against enemy range). All 5 dropped for both arms: 111 items graded.
  Files: pilot-prompt.txt, pilot-verdicts.json in /home/brian/projects/data/aes-gamebench/.
