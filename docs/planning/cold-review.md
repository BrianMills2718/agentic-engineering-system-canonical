# Bounded cold review: work-unit DAG (AES, 2026-11-14)

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
