# Context A/B rerun — result (2026-09-25)

Base: AES canonical `2509ea4` (the repository governing itself; ~4,000 lines
of v0.2 source and tests under the governed roots plus 18 retained v0.1 files).
Change: "an external boundary is a route" in `reconcile.py` — a real bug
found by the phase-6b builder. Pre-registration: `preregistration.md` (written
before either arm ran). Arms: two fresh Claude Opus 5.5 agent sessions in
separate clones, no access to the orchestrator's conversation or the proposals
directory. Arm A: change request + `aes context RU-AES-RECONCILE` packet
(as a file) + repository. Arm B: change request + repository, README first.

| measure | arm A (packet) | arm B (repository only) |
| --- | --- | --- |
| files read (arm's own list, excluding what it was told to read) | 8 entries: reconcile.py, planning.py, records.py, .aes/target.yaml, test_reconcile.py, fixture target, Makefile + hook + CLAUDE.md grep, old observations | 8 entries: reconcile.py, records.py (one model), test_reconcile.py, fixture target, .aes/target.yaml, CLAUDE.md grep, hook, old observations |
| obligations missed (of 8) | 0 | 0 |
| topology violations / hook rejections | 0 | 0 |
| rework (commits after the first) | 1 (evidence re-recording, obligation 7) | 1 (same) |
| wall time | 238 s | 199 s |
| diff | reconcile.py +10/−3, test +20, 9 observations | reconcile.py +9/−3, test +21, 9 observations |
| tests | 145 passed | 145 passed |

Fix patches: `arm-a-fix.patch`, `arm-b-fix.patch` (near-identical; arm A's
prints the boundary text, arm B's a flag). Arm A's fix is the one landed
(commit `61e1edb`), re-recorded at that commit rather than the clone's.

**Verdict: not distinguishable.** Same obligations met, same files, same
size of change; arm B was faster. Arm A reported two things the packet
lacked: the route rule lives in `planning.py`, a component the packet omits
(RU-AES-RECONCILE does not reference SC-GF-004 or RU-AES-PLANNING), and the
packet says nothing about the evidence consequences of the change (10
observations staled). Arm B found both by grep in under a minute.

This is the second indistinguishable result (probe 0 on whygame5 at ~300
lines; this at ~4,000 governed lines). The roadmap's pre-registered
wrong-when (§5) fires: ER-SC-GF-005-02 is to be re-scoped, not re-run.
What the two runs do show: on a well-planned repository with a strict target
and a hook, a fresh agent reconstructs obligations from the repository
itself at no measurable cost — the target file *is* the context. The packet's
remaining value is bounding, not discovery; that is a different claim and
needs a different measure (e.g. tokens consumed, or behaviour on a repository
whose target is large enough that reading it whole is costly).

Both arms' full commits are retained as git bundles in the session scratchpad
and as patches here; arm reports are summarized above verbatim in numbers.
