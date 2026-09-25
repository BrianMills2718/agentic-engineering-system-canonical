# AES v0.2 pre-probe decisions and independent review record

Status: **accepted pre-probe decisions / non-normative until v0.2 cutover**
Date: 2026-09-25
Review basis: `REVIEW.md`, all primary candidate files, `docs/decisions/0001`–`0009`
Reviewer: independent agent session (Claude Fable 5.1), first read not authored
by the proposal's author session. Brian approved the consumer-selection rule
(option A below) in conversation on 2026-09-25.

## Review verdict

**Accept for bounded implementation probing**, conditional on the decisions in
this file and on the build order in section 3. The architecture is coherent.
The material risk is not in the design; it is that this is the second full
architecture in nine days with no consumer, and the one claim that justifies
AES's existence (SC-GF-005/SC-GF-008: bounded projected context helps a fresh
agent on a real change) was scheduled after ten realization units.

Independent re-run of the cross-file reference check over
`12-greenfield-mvp-semantic-instance.candidate.yaml` and
`20-realization-topology.candidate.yaml` (own script, PyYAML `safe_load`,
ID pattern `^(OUT|GF-REQ|SC|ER|FM|FMR|CAP|PB|RU|ART|SYM|VS)-`):

| measure | this review | PR body |
| --- | --- | --- |
| declared IDs | 110 (122 when the 12 `PB-*` IDs in file 21 are included) | 122 |
| typed refs | 216 (counting method differs) | 188 |
| unresolved refs | 0 | 0 |
| duplicate IDs | 0 | 0 |
| exact paths / duplicates | 23 / 0 | 23 / 0 |

The zeros hold independently. The counts are not architecture evidence.

## 1. Decisions taken now (high-confidence, reversible)

### D1. "Governed" is a declared namespace, not every tracked file

The no-orphan rule (`SC-GF-003`, thesis §6) applies only to files under
governed roots declared in `.aes/project.yaml`, for example:

```yaml
governed_roots:
  - src/
  - tests/
```

Everything outside governed roots is ungoverned by default in the Greenfield
MVP: `.gitignore`, LICENSE, README, lockfiles, CI configuration, editor
configuration. `.aes/` itself is governed by the initialization contract, not by
project topology. Inside a governed root, every durable file needs an exact
planned path or a bounded generation rule, exactly as the candidate says.

Wrong-when: a real consumer needs a governed file outside `src/`/`tests/` that
cannot be expressed as an additional governed root; or the probe finds the
check catching nothing because governed roots were declared too narrowly.

### D2. Evidence sufficiency is conjunction-only for the MVP

A success criterion is `SUPPORTS` with `SUFFICIENT` adequacy only when **every**
listed evidence requirement has at least one `CURRENT` observation whose
assessment is `SUPPORTS`. No thresholds, no disjunction, no repetition counts,
no weighting. Open question 3 is closed with this rule; reopen only when a real
criterion on a real consumer cannot be expressed this way.

Wrong-when: the first authentic consumer has a criterion that genuinely needs
"any one of" or "N of M" and the workaround distorts the criterion's meaning.

### D3. The public term is `component`

`realization_unit` remains the semantic-model name in prose if useful; the
record field, CLI vocabulary and documentation use `component`. Decision 0003
already chose this word for the same boundary. Open question 1 is closed.

Wrong-when: `component` demonstrably collides with a consumer ecosystem's own
"component" concept in a way that confuses the fresh-agent evaluation.

### D4. Supersession is stated, not left implicit

The PR's nonclaim "does not supersede Decisions 0001–0009" is true of the
proposal and false of its acceptance. The v0.2 cutover decision must
explicitly supersede:

- Decision 0001 §3 (incumbents as capability sources with retained ownership)
  and §6 (no local package until Company Planning derives topology);
- Decision 0002 (AES-local profile over Company Planning as the planning route);
- Decision 0009 (Enforced Planning retains installed authority; Company
  Planning owns planning derivation).

Decisions 0003, 0004, 0005, 0006 and 0008 are largely re-derived by v0.2 under
new names and should be recorded as *carried forward with renames*, not
superseded. Decision 0007 is already superseded by 0008.

### D5. v0.1 governance was bypassed to produce v0.2, and that is evidence

All 67 commits on this branch are tagged `[Unplanned]` under v0.1's own
Enforced Planning governance. Real design work routed around the control the
moment it started. This is the strongest concrete support for v0.2's stance
that hooks are invocation adapters, not enforcement (`PB-GF-GIT` limitations,
`22-portable-provider-boundaries.md` §3). Record it in the cutover decision.

## 2. Consumer-selection rule (Brian, 2026-09-25: option A approved)

The first authentic consumer is **a small new Python tool Brian already needs,
governed by AES from its first commit**. Rejected alternatives: a purpose-built
toy (fails the validation profile's own real-scope requirement) and deferring
the choice until code exists (delays the only decisive test).

Survey of the current weekly plans (`weekly-plans/personal/THIS_WEEK.md`,
`weekly-plans/inside-success/THIS_WEEK.md`) on 2026-09-25 found **no item that
is a genuinely new small Python tool**. Candidates checked and why each fails
the "new project from inception" requirement:

| candidate | why rejected |
| --- | --- |
| hook-event reader / before-after readout (Priority 6) | `enforced-planning/scripts/hook_receipts.py` already has a scanner and `hook_feedback_report.py` consumes it; this is an extension |
| personal-wiki source extractor (Priority 5) | Gmail/Calendar connector is blocked pending re-authorization; `tools/google_access.py` already exists |
| personal-wiki page linter (Priority 5) | `~/.claude/skills/karpathy-wiki/scripts/lint.py` already lints it |
| weekly ChatGPT supervisor dispatch | exists with 11 passing tests |
| Never Absolute formation checklist (Priority 4) | not a tool; a legal filing |

**Open:** Brian names the tool. Selection criteria the tool must meet:
Python, new Git repository, real user this week, at least two implementation
files and one test file, one public function whose signature is a genuine
commitment, one criterion that a passing test alone cannot establish (human
review or runtime observation), and no dependency on Brian's private AES
repositories.

## 3. Build order: probe 0 first

Do not implement the ten realization units in topology order. Probe 0 is the
cheapest path to the SC-GF-005/SC-GF-008 A/B test:

1. Hand-write `.aes/target.yaml` for the consumer (outcome, normative items,
   criteria with evidence requirements, planned artifacts, verification
   subjects). Seven of the seventeen semantic families; defer failure modes,
   capability requirements, provider bindings, generation rules and symbol
   commitments to probe 1.
2. Implement only `records.py` (strict load + ref validation) and `context.py`
   (`aes context <subject>`), roughly `RU-AES-RECORDS` and `RU-AES-CONTEXT`.
3. Run the same real change twice on the consumer: arm A receives the context
   packet; arm B receives the repository and README only. **Arm B must be a
   separate agent session with no access to this conversation, this proposals
   directory, or the AES canonical repository.** The same operator running
   both arms from one session invalidates the result.
4. Record both arms as observations at exact revisions. Compare on the
   validation profile's measures (files read, missed obligations, topology
   violations, rework).
5. Only if arm A is materially better: proceed to probe 1 (topology check,
   characterize, evidence, reconcile). If it is not: stop and reframe before
   writing any further architecture document.

Stop rule for the whole lineage: **no new architecture proposal document until
probe 0 has a recorded result.**

## 4. Deferred to the probe (learn, do not decide now)

- stdlib `ast` versus Griffe for characterization;
- exact Python version range and dependency pins;
- whether ruamel.yaml round-trip preserves a hand-edited `target.yaml` well
  enough for `aes plan accept` to write it (load-bearing: if it mangles
  comments/ordering the "review target changes as one diff" benefit is lost);
- where evidence assessments are stored (open question 12);
- the assessor-identity minimum (open question 13).

## 5. Answers to the twelve load-bearing review questions

1. Kernel not minimal (17 families); freeze it, let probe 0 use seven.
2. `component` (D3).
3. Exact topology correctly scoped once D1 bounds "governed"; unbounded, too strong.
4. One `target.yaml`: yes; ruamel round-trip is load-bearing (section 4).
5. Planning transaction ordering: correct; best part of the design.
6. Evidence model: sufficient with D2.
7. Python + Git: yes.
8. Residuals: reconcile, evidence, context are AES-specific; records and topology are thin wrappers, acceptable.
9. Topology boundaries: meaningful, but 23 files and 8 signatures before a consumer is over-planned; probe 0 realizes five or six.
10. Falsification profile: strong on paper; weak on n=1 and operator contamination (section 3 step 3).
11. Provider rejections: justified.
12. Decide now: D1–D4 and the consumer. Learn in probe: section 4.
