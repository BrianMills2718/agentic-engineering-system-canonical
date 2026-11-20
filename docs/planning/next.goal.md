---
description: Next plan for AES canonical -- Lockstep, the one planning-and-checking tool, built in six slices (merged 2026-11-11 and 2026-11-12); next, two local proofs (retrofit and from scratch) adopted 2026-11-20
---

# Plan: build the one planning-and-checking tool

Planning package: docs/planning/planning-package.json

Status: adopted 2026-11-11 as the design's build order (Brian approved the design as written: "i approve
single tool desing re d4", 2026-11-11 21:10 UTC, `~/.claude/history.jsonl`, session 483c48d8). Built 2026-11-11 and 2026-11-12: all six slices merged (PRs #831 to #837; `wiki/lockstep.md:28-34`). Builder: the
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

## Slices (each merged when it worked; all six are merged)

Each slice below keeps its original wording and ends with what was built. The six slices are the design's ([DESIGN.md](../../proposals/one-planning-tool/DESIGN.md) lines 64-77). Each
line below adds what this package checks it by; the acceptance entries are in
[acceptance-criteria.json](acceptance-criteria.json).

1. **Move.** `pcw` moves into this repository as package `lockstep`, with its tests; `pcw` and `pcw-hook` stay
   as alias entry points so lifelike and Team-Brains' vendored runner keep working. Checked by: lifelike's edit
   hook still refuses an unplanned write after it installs from here (A2's failure case), and acceptance A1's
   one-command install. Built: #831, `src/lockstep/` with `src/pcw/__init__.py:1` as the alias. `lockstep init` (`src/lockstep/init_repo.py`, spec lockstep-init) is the one-command install A1 checks. Q22 (where Brian watches it work) is resolved: `lockstep-acceptance.html`.
2. **Plan format.** Lockstep reads requirements from OpenSpec and layout rows from `lockstep.yaml`;
   `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it. Checked by: acceptance A4 (the
   requirement text appears word for word in the first docstring of the file that implements it). Q6
   (whether this repository's own `.aes/` goes) is resolved: built in #835 with `.aes/target.yaml` still read for other repositories; this repository's own `.aes/` was retired on 2026-11-12 (docs/retired/2026-11-12.md).
3. **Guard.** Port code2check's shell-target parsing. Done when lifelike replays the four cases from
   lockstep#111 (`cat >`, `echo >`, `python -c` refused; read-only `cp` allowed). Checked by: acceptance A2. Built: #834.
4. **Commit checks.** Port code2check's `trace`, `arch`, `test-first`, `sources` and `docmeta` with their tests,
   as `lockstep check <name>`. Checked by: acceptance A3. Built: #833.
5. **Plan check.** Port the acceptance-criteria and plan-requirement checks from Company Planning's validator.
   Built: #832, keeping Company Planning's own copy as well; Q19 (whether the adoption gate calls it) stays open.
6. **Switch users.** code2-template installs `lockstep` instead of `code2check` (11 repositories adopt it when
   next changed); lifelike, plan-code-wiki and Team-Brains' runner move to the new package. Checked by:
   acceptance A5 (installs anywhere, names no machine path). Built: #836 and the user switches (code2-template#29, lifelike#5, Team-Brains#1183); Team-Brains is an Inside Success repository, so Q2 is now about work that shipped.

Slice 0, kept running alongside and not built by the Lockstep session: the feedback loop's two nightly jobs and the rules register. The built tool differs from the design in one place now: two projectors remain (Q24); the guard's log folder was fixed to `.lockstep/` (Q23, e662882db).

0. **File corrections (repair recorded).** The historical 867 deferred human corrections were filed
   after the corrections-first repair (#826): commit `ec3022d5a` records 867/867 filed and 0 errors
   on 2026-11-11 (Q18 resolved). Acceptance A6 still lets Brian inspect recent filed corrections;
   this package reconciliation does not rerun the collector or assert freshness of today's issues.

## Done when

- Each slice above has merged through `ship` in this repository (done), with its named acceptance entry `built` and
  served from committed git (done: A1 to A5 are `built`, each with a recorded run that says PASS on 2026-11-12, page `lockstep-acceptance.html`; A6 to A8 are also `built` on their pages; Q18 records the historical A6 repair, and A6 to A8 remain unjudged).
- Brian has judged A1 to A8 on their pages; a judged status records his own words.
- `docs/planning/planning-package.json` validates (exit 0) and its cold review read the plan as built.

## Out of scope

- `.aes/target.yaml` retirement in other repositories (decision 0009 (a): one repository at a time, when each
  is next changed).
- Company Planning's other skills (landscape review, roadmaps, the review page builder): they stay in the
  Company Planning plugin (DESIGN.md line 50).
- New feedback-loop jobs (Q21 is Brian's call). The claims-era `enforced_planning/` and `scripts/` were retired on 2026-11-12 (Q10, resolved).

## Domain concepts this plan relies on

AES as a whole, Lockstep today, the one tool, `lockstep.yaml`, layout row, OpenSpec requirement, first
docstring, edit guard, `lockstep check`, `lockstep plan check`, acceptance entry, slice, code2check, the
target (read until slice 2), the feedback loop, human correction, feedback report, policy layer, rules register
and agent rules, as defined in [DOMAIN.md](DOMAIN.md).

## Cost and trace

No step of this plan calls a model to produce its answer: the tool's checks are deterministic code, and the
feedback loop's nightly calls are already running and measured: USD 0.127 over two nights for 1,443 calls (`llm-cost cost
--days 2 --group-by project,task`, project aes, 2026-11-11; investigation.json). Each slice's tests and lifelike's hook replays record their
inputs and results in the guard log, outside the checkout since #974 (src/lockstep/hook.py, `log_dir`) and the pull request; the Lockstep session reads every
failing run in full before marking a slice done.

## Next plan: prove Lockstep on two local repositories (adopted 2026-11-20)

Status: adopted. Source: Brian, 2026-11-20, "yes" to running both proofs before any further
Project Brain gets the brain pull-request runner (session 5651a525; question asked in the same
session: "dont we need to prove this on a local project both started from scratch and retrofitting
an existing fproejct into the aes format?"). Size: full plan, because Lockstep is read by other
repositories; this section is the one authority for it, under the same planning package.

1. **Guard log outside the checkout (issue #974).** The edit guard writes `.lockstep/` inside the
   checkout it edits (src/lockstep/hook.py:172-187), so a worktree deleted after `ship` takes its log
   with it and guard use cannot be counted. Fix first: write the log under a per-user state folder
   with an override, and have `--would-block` read it there. Done when a guarded edit in a worktree
   leaves a log line that survives the worktree's removal. Coupling: the Team-Brains runner reads
   refusals from a mounted `.lockstep/` and pins `LOCKSTEP_SHA`, so bumping that pin needs the mount
   moved in the same change.
2. **Retrofit proof (world-substrate, two weeks).** Turn on the checks that its `lefthook.yml`
   already configures but that never run (no hook installed), with `trace` set to warn because it
   has 196 findings today. Record the seconds a commit takes before and after. Define a "real
   mistake" (a check finding that led to a code or doc change an agent kept, judged from the commit
   that followed) before collecting any data; ordinary work only, no edits made to trip the guard.
   Passes if the checks catch at least 3 real mistakes and add under 15 seconds per commit. Also
   recorded: hours and tokens spent working down the trace findings. Review on 2026-12-04.
3. **From-scratch proof.** A new repository from code2-template: `make check` passes before any
   feature, then one small real feature is built with `trace` passing and the guard log showing its
   decisions on every commit. A guard log with zero decisions fails the proof.

Results as of 2026-11-20:

- Step 1 done: #976. A guarded edit in a removed worktree left its log line under
  `~/.local/state/lockstep/<repository>/`.
- Step 2 not started. Its commit checks are switched off machine-wide: `~/.config/git/repo-hooks.off`
  makes the global git hooks skip each repository's own pre-commit. Setting world-substrate's own hooks
  path is waiting on Brian.
- Step 3 passes, in the local repository `lockstep-pilot-report`:
  - The first feature passed the literal test (25 guard decisions, `make check` exit 0). But
    `lockstep init` writes `governed: []`, so the guard had nothing it could refuse.
  - With `src/` governed, a second feature showed the guard refusing every edit to files that existed
    before their layout row: the template's own files, and every file in a retrofit.
  - Fixed in #977 (edit hook) and #979 (commit check, exports wording). The feature then landed in
    pilot commit `e2a6397` with `make check` exit 0.
  - The guard logged 82 decisions that day: 61 pass, 9 allow, 12 deny, of which 6 were the bug.

Thresholds in step 2 (3 mistakes, 15 seconds) are agent guesses Brian said yes to as proposed; he
can change them. Not in scope: adding any Project Brain to the runner; that waits for both proofs.

## Authorized source-fact upkeep follow-on

Brian's 2026-11-12 Company Planning conversation asks for automatic wiki upkeep and
a finished consolidation demonstration ("ok proceed"). This bounded follow-on
extends existing Lockstep projection, configuration and hooks: selected source-owned
status, description, interface and evidence fields feed declared target blocks;
post-edit refresh maintains them and the read-only project check refuses stale
blocks. It adds no AI answer path or universal enforcement. The
[acceptance table](source-facts-acceptance.md) and A9 distinguish provider tests,
installed-command replay and native dispatch; consumer evidence is supplied by
Company Planning rather than inferred from a successful documentation build.
Specification: `openspec/specs/lockstep-doc-facts/spec.md`.
