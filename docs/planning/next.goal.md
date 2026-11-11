---
description: Next plan for AES canonical -- build Lockstep, the one planning-and-checking tool, in six slices, with the feedback loop and policy layer kept running
---

# Plan: build the one planning-and-checking tool

Planning package: docs/planning/planning-package.json

Status: adopted 2026-11-11 as the design's build order (Brian approved the design as written: "i approve
single tool desing re d4", 2026-11-11 21:10 UTC, `~/.claude/history.jsonl`, session 483c48d8). Builder: the
Lockstep session, which owns `proposals/one-planning-tool/` and the Lockstep code. This file is the planning
package's view of that build; the design is the authority ([DESIGN.md](../../proposals/one-planning-tool/DESIGN.md)).

## Goal

For Brian and the coding agents that work in his repositories, change today's three overlapping tools
(Lockstep's `pcw` for planning files and guarding edits, code2check for commit checks, Company Planning for
plan packages), each with its own plan format, into one tool named Lockstep, shipped from this repository,
with one config file and one plan format, that any repository installs with one command. (source:
proposals/one-planning-tool/DESIGN.md:14-19)

Brian's direction: "on dcision 4 it seems liek youa re poitn otu that htis should be combined into one single
thing not a bunch of differnt things which i agree with. and it should preusmably be part of aes canonicale
which is configurable and protable/sharebale" (source: proposals/one-planning-tool/DESIGN.md:5-8; Brian,
2026-11-11 20:46 UTC, session a769ac09).

AES stays the whole system while this is built: "to me aes is the whole sysem lockstep is one part. aes include
the whole feedback and policy system" (source: .project-brain/now.md:9; Brian, 2026-11-11 08:14 UTC, session
a769ac09). So the plan also keeps the feedback loop and the policy layer working and checks that they do
(acceptance entries A6 to A8). Agent judgment, unconfirmed: that the feedback-loop and policy-layer checks
belong in this plan rather than a separate one.

## Slices (each merges when it works)

The six slices are the design's ([DESIGN.md](../../proposals/one-planning-tool/DESIGN.md) lines 64-77). Each
line below adds what this package checks it by; the acceptance entries are in
[acceptance-criteria.json](acceptance-criteria.json).

1. **Move.** `pcw` moves into this repository as package `lockstep`, with its tests; `pcw` and `pcw-hook` stay
   as alias entry points so lifelike and Team-Brains' vendored runner keep working. Checked by: lifelike's edit
   hook still refuses an unplanned write after it installs from here (A2's failure case), and acceptance A1's
   one-command install. Settles Q22 (where Brian watches it work).
2. **Plan format.** Lockstep reads requirements from OpenSpec and layout rows from `lockstep.yaml`;
   `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it. Checked by: acceptance A4 (the
   requirement text appears word for word in the first docstring of the file that implements it). Settles Q6
   (whether this repository's own `.aes/` goes in this slice).
3. **Guard.** Port code2check's shell-target parsing. Done when lifelike replays the four cases from
   lockstep#111 (`cat >`, `echo >`, `python -c` refused; read-only `cp` allowed). Checked by: acceptance A2.
4. **Commit checks.** Port code2check's `trace`, `arch`, `test-first`, `sources` and `docmeta` with their tests,
   as `lockstep check <name>`. Checked by: acceptance A3.
5. **Plan check.** Port the acceptance-criteria and plan-requirement checks from Company Planning's validator.
   Settles Q19 (whether Company Planning's adoption gate calls it).
6. **Switch users.** code2-template installs `lockstep` instead of `code2check` (11 repositories adopt it when
   next changed); lifelike, plan-code-wiki and Team-Brains' runner move to the new package. Checked by:
   acceptance A5 (installs anywhere, names no machine path). Asks Brian Q2 before any Inside Success repository.

Kept running alongside, not built here: the feedback loop's two nightly jobs and the rules register.
Fix first, before slice 1 is judged: corrections are extracted but not filed (Q18), so acceptance A6 fails
today.

## Done when

- Each slice above has merged through `ship` in this repository, with its named acceptance entry `built` and
  served from committed git.
- Brian has judged A1 to A8 on their pages; a judged status records his own words.
- `docs/planning/planning-package.json` validates (exit 0) and its cold review read the plan as built.

## Out of scope

- `.aes/target.yaml` retirement in other repositories (decision 0009 (a): one repository at a time, when each
  is next changed).
- Company Planning's other skills (landscape review, roadmaps, the review page builder): they stay in the
  Company Planning plugin (DESIGN.md line 50).
- `enforced_planning/` and the claims-era `scripts/` (Q10), and new feedback-loop jobs (Q21 is Brian's call).

## Domain concepts this plan relies on

AES as a whole, Lockstep today, the one tool, `lockstep.yaml`, layout row, OpenSpec requirement, first
docstring, edit guard, `lockstep check`, `lockstep plan check`, acceptance entry, slice, code2check, the
target (read until slice 2), the feedback loop, human correction, feedback report, policy layer, rules register
and agent rules, as defined in [DOMAIN.md](DOMAIN.md).

## Cost and trace

No step of this plan calls a model to produce its answer: the tool's checks are deterministic code, and the
feedback loop's nightly calls are already running and measured: USD 0.127 over two nights for 1,443 calls (`llm-cost cost
--days 2 --group-by project,task`, project aes, 2026-11-11; investigation.json). Each slice's tests and lifelike's hook replays record their
inputs and results in `.lockstep/` (DESIGN.md line 48) and the pull request; the Lockstep session reads every
failing run in full before marking a slice done.
