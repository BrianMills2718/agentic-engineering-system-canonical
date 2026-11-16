# Bounded cold review: feedback-loop notices (AES, 2026-11-16)

Reviewed revision: `db1f282fc302dda87160423fdaaf6218e26ca9dc`.
Verdict: **pass** for the slice 2 change (spec `feedback-loop-notices`, `scripts/learning_loop/notify.py`, `alert.py`,
the copied `scripts/concern_issue.py`, loop call sites, plan row). This does not re-certify unrelated A1-A8.

Independent planning reviewer: first read at `b391f165f`: revise (plan row claimed the loop had no Project Meta path while
the nightly collector, fix owner and policy check still called its alert script; weak no-path test; test count 22 vs 19;
lost de-duplication and notification log unnamed). Second read at `f74ad5048`: pass, 24 tests exit 0. Third read at `329ea47bd` (spec requirement 1 widened to the six scripts the test checks): pass. Fourth read at this revision (notice moved from ntfy to Telegram, Decision 17 A; spec requirement 2, tests, plan row, Q42, `evidence/runs/slice2-live-20261116.json`): pass, 5 tests exit 0. Noted: the no-leak test checks the result, not what `main` prints; the Telegram message was not rechecked by the reviewer. Fifth read at this revision (Decision 18 A: spec `learnings-register-frozen`, collector reads a frozen private copy and writes to no register): pass, 25 tests exit 0. Noted, not changed: dead branches gated on `--legacy-register` and `RegisterLocked` remain in `collect_feedback.py` (remove in slice 3); `file_pending` error handling and the systemd units were not read; `label_items.py`'s path change is untested. Noted, not changed:
the `problems.py` digest and revoked push call sites are read, not tested; no live `gh` or ntfy run; `collect_feedback.py`
still uses the legacy learnings register (a later slice).

Verdict: pass

## Prior review: work-unit DAG (historical)

Reviewed revision: `ff9d4c9f40b59508dfda61ad6d9d288dcea01c3f`.
Verdict: **pass** for the work-unit DAG change (`lockstep plan units`, spec `lockstep-plan-check/work-units-form-a-dag`)
and for the earlier `lockstep-doc-facts` array-fact change, the two plan files that changed since the previous review.
This does not re-certify unrelated A1-A8.

Independent planning reviewer (first read at `cb5a1f5f8`: revise, four blocking findings; second read at this revision: pass).
Validator at this revision: 10 of 10 parts ok, 11 of 12 substance checks ok with one existing route pending, 6 of 6
tier/map checks ok; the only failure was the review pin. Work-unit tests: 10 passed, exit 0; `lockstep plan units` on
`docs/planning/work-units.json`: 9 planned, ready S0 and S5, exit 0.

Fixed after the first read: `work_units` added to the system map; two retired unit globs dropped; `CLAUDE.md:14` and `:24`
citations re-pointed to `AGENTS.md:14` and `:24` (byte-identical lines); tests added for `plan check` with a bad units file,
malformed JSON and printed output; spec wording clarified (unmerged units; `touches` compared as exact strings).

Noted, not changed: `AGENTS.md:14` and `:24` are weak anchors for Q1/F1 and Q16 (the "AES is the whole system" statement is
at `AGENTS.md:18-20`), a weakness that predates this change; the `lockstep-doc-facts` spec says "top-level array" where the
code reads a named key of a mapping; `work-units.json` statuses are all planned with inferred `touches`.

Verdict: pass

## Prior review: AES documentation self-adoption (historical)

Bounded cold review: AES documentation self-adoption

Reviewed revision: `265b5ba8cf0e93524348c8739d12572d69b97354`.
Verdict: **pass** for documentation self-adoption, restored goal fields and
refreshed check records. This does not re-certify unrelated A1–A8.

Independent planning reviewer reproduced 10/10 package parts, 11/12 substance
checks with one existing route pending, and 6/6 tier/map checks. Validation
without freshness exited 0; full validation failed solely on the old review pin
before this record was updated.

The durable-document check returned 0 findings, exit 0. The wiki check covered
130/130 Markdown files with 0 orphans and 0 layout/durable findings, exit 0.
The reviewer independently matched all 417 catalog entries/links and 415 source
hashes. The public native transcript retains all 17 successful events, exactly
Read, Read, Edit, plus an explicit publication-redaction record.

The new specification reuses existing projection behavior. Native dispatch,
authored assessment and measured evidence remain distinct. Native Codex
execution and default-session loading remain unobserved. Restored goal fields
preserve the existing direction. Repository-format findings remain tracked by
Q17; no blanket format or effectiveness claim is made. No substantive blocking
finding in this bounded review.

Verdict: pass

## Prior source-fact review (historical)

# Bounded cold review: declared source-fact upkeep

Reviewed revision: `0badfe82442d86bd9be230dd7f3a2c12cff4ee27`.
Verdict: **pass** for the source-fact projection slice. This does not re-certify
unrelated A1–A8 or eliminate the existing route WAIT.

Independent reviewer confirmed that A9 covers all four source fact types,
installed refresh and stale bypass refusal; the stored declaration and trace
records name their fields, writers and storage; existing domain concepts cover
the relationships; the stale Q18 filing claim and incorrect test citation are
repaired; the review page exposes A9 and its acceptance table.

Consumer observations cover 11/11 current command cases, including eight refresh
replays and negative cases. Native traces cover 2/2 disposable client fixtures,
each with one source edit and generated update. Codex fixture trust bypass is
explicit; production checkout trust and deployment require separate evidence.

Before recording this pin: full validator exited 1 solely for the old pin;
without freshness it exited 0 with 10/10 parts, 11/12 substance (existing route
WAIT), and 6/6 tier/map checks. A9 semantic coverage awaits normal nightly
judgment. No remaining substantive blocking finding in this bounded review.

Verdict: pass

Sixth read (spec `external-idea-intake`, `scripts/learning_loop/external_ideas.py`, 2026-11-16, at `9f10b9967`): independent reviewer, static read, pass with fixes; no blocker against the spec. Its findings (corrupt seen list, malformed post aborting the run, unlogged setup failure, config gaps) were fixed in the next commit with tests (12 pass). Not tested: the real Reddit fetch path (`social_media_fetch`); it is run once live after merge.

Seventh review (depth-aware usefulness judge, `external_judge.py`, 2026-11-16): independent static reads. First at `9d9015aa7`: found an unguarded link reader (internal addresses) and an overstated no-steering claim. Second at `04d6d6b44`: revise (round-2 title and body outside the untrusted markers, a weak test, skipped posts marked seen). Third at `ef99af81d`: fixes correct, revise only for a missing `run()` test and one spec sentence; both added in `db1f282fc` and checked by tests (32 pass), not re-read. Not covered: DNS rebinding (a public name that resolves to an internal address at fetch time), and the live model route beyond one 9-post run.
