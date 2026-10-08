---
plan_id: evidence-recorder-counts
status: shaping
selected_path: repair
planning_path_decision: proposals/evidence-recorder-counts/planning-path-decision.json
method_conformance_receipt: proposals/evidence-recorder-counts/method-conformance-receipt.json
goal:
  outcome: default pytest evidence records distinguish substantive passing tests from all-skipped runs
  canonical_example: a real pytest file containing only a skipped assertion records INCONCLUSIVE with passed 0, failed 0, errored 0, skipped 1 and exit 0
  forbidden_substitutes: parsing human summary text; a mocked exit code; a command that only prints a passing summary
  boundaries: AES default Python pytest recorder, typed result metadata, focused tests and user documentation; custom commands keep unknown counts; existing observations unchanged
  done_when: real passing, failing, all-skipped and mixed pytest fixtures produce the expected saved counts and assessments; focused tests and local repository gates pass; changes committed and pushed for parent integration
  do_not_gate_on: hosted CI; Brian reading a code report; external adoption; separately owned CLI formatting
  owner: codex:evidence-recorder-counts
---

# Skipped tests do not support evidence

## Actor, result and example

An agent using `aes evidence record` needs to know whether its tests actually ran. At source revision `431deeb6`, a real pytest file with one skipped assertion returned exit 0 and the default recorder saved SUPPORTS. The reproduction is in `reproduction.before.json`; source inspection alone was not used as runtime proof.

After this repair that run saves INCONCLUSIVE and typed counts: passed 0, failed 0, errored 0, skipped 1, exit 0. One real passing test can SUPPORT; a failing test REFUTES. A mixture of passing and skipped tests records both; it proves only the tests that ran, never universal coverage.

## Authority and boundaries

Brian asked for high-confidence reversible harness fixes and identified AES issue #257. The coordinator explicitly delegated this isolated repair. The native lane owns `.aes/target.yaml`, `.aes/plans/PLAN-AES-EVIDENCE-COUNTS.yaml`, `src/agentic_engineering_system/evidence.py`, `tests/greenfield/test_evidence.py`, `docs/greenfield/GETTING_STARTED.md`, and `proposals/evidence-recorder-counts`. Other writers own other concerns; preserve their files and claims. AES acceptance must precede implementation.

No vision work, observation migration, new test framework, general coverage certification, hosted CI, release, deployment, deletion, or outbound communication. The separately owned CLI console formatting stays outside this repair. Rollback is a revert of this isolated increment; old observations remain unchanged. The deterministic implementation adds no paid model calls. Company Planning's existing semantic adoption check uses its approved configured light route.

## Prior art and design

Adopt [pytest's native JUnit XML output](https://docs.pytest.org/en/stable/how-to/output.html#creating-junitxml-format-files), verified 2026-10-08, rather than interpreting prose summaries. The existing recorder and ObservationRecord own the behavior and durable result seam. Python's standard XML parser reads pytest suite attributes; Pydantic validates nonnegative counts and arithmetic consistency. No parallel runner or new service is needed. Dispositions: reuse AES record() and ObservationRecord; adopt pytest native JUnit; compose standard XML parsing with the existing Pydantic boundary. Reject prose-summary interpretation and a custom pytest plugin because the native structured output already supplies the required counts. `rg -n "^def record" src/agentic_engineering_system/evidence.py` found the single recorder; no second recorder is introduced.

The default Python command asks pytest to write a temporary JUnit file. Parse tests, failures, errors and skipped; derive substantive passed tests from those structured counts. Save the counts, count-source status and process exit code in the observation result. Append a bounded outcome line to its saved output tail. Exit 0 with no substantive passes, missing counts or invalid counts is INCONCLUSIVE; ordinary substantive passing runs SUPPORT unless explicitly downgraded. Preserve nonzero-exit REFUTES behavior. Custom commands preserve their existing exit-based assessment with explicitly unsupported/unknown counts; their prose is never used to manufacture counts.

## Trace review

The actual all-skipped reproducer is `reproduction.trace.json` at source revision `431deeb6`. Its full recorder subprocess boundary was captured: all 15 Git/dependency/version/test commands, inputs, complete stdout/stderr, timings, exit codes, test source and saved assessment. The repair author read all 15 of 15 steps before this adoption request, including the actual skipped assertion source, clean dependency checks, pytest command, full skip output and the incorrect SUPPORTS decision. This is completed evidence, not a promise to inspect future output. The two absent remote refs are expected in a synthetic fixture, not hidden failures. Fixture cwd/hashes are historical provenance; replay inputs are the durable test helper and embedded source, not a surviving scratch checkout.

Beyond the final outcome, inspection establishes that the assertion did not run, the runner still exited 0, and record() promoted that exit without test counts. The future passing/failing/skipped/mixed checks will retain and inspect their structured results; tests define their completion. Native proposal `runs_traced_work: false` describes the implementation subject: deterministic recorder and pytest tests, with no model, agent or data pipeline. The Company Planning governance verifier separately keeps its shared-client call trace.

Each acceptance criterion has a named run and trace boundary below. Only the before-repair failure run has executed; every after-repair row is **PROSPECTIVE: no observation yet**. The planned trace artifact is a replayable structured test receipt, not an attestation that future checks passed.

| Criterion | Named run and trace location | Beyond-outcome evidence required | State |
| --- | --- | --- | --- |
| Reproduce incorrect support before repair | before-skip-only; reproduction.trace.json and reproduction.review.json | All 15 subprocesses, committed skipped assertion, pytest exit0, full skip output and saved SUPPORTS. | EXECUTED; full trace read. |
| Real passing test supports with exact counts | after-native-pass; verification.after.json | Default recorder command, native JUnit count mapping, saved passed1/failed0/errored0/skipped0, exit0 and SUPPORTS. | PROSPECTIVE; no observation yet. |
| Real failing test refutes with exact counts | after-native-fail; verification.after.json | Assertion source, JUnit failed1, exit1 and saved REFUTES, beyond the final assessment alone. | PROSPECTIVE; no observation yet. |
| All-skipped test cannot support | after-native-skip-only; verification.after.json | Skipped assertion source, JUnit skipped1/passed0, exit0 and saved INCONCLUSIVE. | PROSPECTIVE; no observation yet. |
| Mixed passing and skipped tests retain both | after-native-mixed; verification.after.json | Distinct pass and skip fixture membership, saved passed1/skipped1, exit0 and bounded SUPPORTS. | PROSPECTIVE; no observation yet. |
| Missing/invalid native results do not support | after-native-unavailable; verification.after.json | Controlled absent/malformed JUnit input, explicit missing/invalid status, exit0 and INCONCLUSIVE. | PROSPECTIVE; no observation yet. |
| Custom command counts remain unknown | after-custom-unknown; verification.after.json | Supplied command identity, its actual exit, unsupported count status and absent counts despite printed pass prose. | PROSPECTIVE; no observation yet. |

All paths in this table are relative to proposals/evidence-recorder-counts. Focused tests execute these named scenarios and inspect saved records. The repair author records exact fixture results and test-process exit in verification.after.json after execution; that artifact does not exist yet.

## Verification and disproof

Extend the existing fixture repository in `tests/greenfield/test_evidence.py`. Run actual pytest pass, fail, all-skip and mixed fixtures through `record()` and assert exact saved count membership, exit and assessment. Exercise malformed or unavailable native JUnit data without promoting it. Keep custom-command compatibility explicit. Run the focused file, then the repository's required local gates once at integration.

The repair is disproved if an all-skipped default pytest run still SUPPORTS, counts disagree with the real fixture, malformed/missing native results promote support, or printed custom prose becomes counted test evidence. Default pytest count records do not claim requirement sufficiency or custom-command coverage.

## Still unresolved

`agent_decided_reversible`: use native pytest JUnit output and retain existing custom-command assessments with unknown counts. The repair owner resolves parser and fixture compatibility through focused execution before committing. `human_set`: audit and repair the harness, preserve other writers and never bypass hooks. Nothing requires Brian's decision.

## Delivery

The child pushes a recoverable branch checkpoint and reports exact checks. The coordinator integrates this history into the single AES pull request. Any native observation naming a child commit must preserve that commit's reachability; do not claim a cherry-picked replacement makes the original observation current.

## Method activation facts

Declared facts for this implementation subject: shared_mechanism=true (existing evidence recorder/result seam); empirical_comparison_proposed=false (a reproduced correctness failure, no benchmark); llm_central=false (deterministic source and tests); irreversible_or_spend_action=false (no such implementation action). The native fact record links this plan and the validated repair route. Existing governance review calls are already authorized by Brian's harness task and use the configured approved light route; they are not a new product LLM dependency.

## Action authority and containment

No irreversible implementation action, release, deployment, deletion, migration or new paid runtime is proposed. The named authorizer is Brian through his harness task and explicit high-confidence reversible-fix delegation. Recoverable Git commits/pushes go to the coordinator for one AES PR; containment is to stop on failing local checks and revert this isolated increment. The existing paid Company Planning admission check has the same already granted task authority, the existing approved light route and shared-client spend gate; it stops after a repeated route failure. It does not authorize further model products, external publication or messages.

## Material uncertainty ledger

| Material uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Pytest JUnit counts may handle skipped, failing or setup-error cases differently. | codex:evidence-recorder-counts | Real pytest fixtures through record(), asserting exact typed result membership and assessment. |
| A missing or malformed report may accidentally preserve SUPPORTS. | codex:evidence-recorder-counts | Controlled unavailable/malformed report cases assert INCONCLUSIVE at exit0 and explicit status. |
| Existing custom-command and observation callers may regress. | codex:evidence-recorder-counts | Existing focused recorder tests plus explicit custom-count unknown assertions, with old observation fixtures unchanged. |

There are no other material uncertainties at this bounded seam. Counts are evidence about tests that ran, not proof of complete requirement coverage.

## Prior art dispositions and lineage

Existing owner and internal lineage were inspected in evidence.py record(), ObservationRecord, the existing test_evidence.py fixture helpers and PASS command, and AES issue #257. The old tests' command merely prints a passing summary, explaining why they did not expose skip-only execution. External source: pytest's official JUnit output documentation linked above. Candidate dispositions: **extend** the existing AES recorder; **reuse** pytest's native JUnit output; **compose** Python standard XML parsing with **reuse** of existing Pydantic validation; **supersede** exit-only SUPPORTS for the default pytest route; **bounded exception** for custom commands whose existing exit assessment remains, with unknown counts explicitly declared. No parallel recorder/plugin/runner is introduced; the source search found one record() owner, and code review plus exact changed-path membership checks preserve that boundary.

The consulted sources and candidate dispositions are itemized to distinguish reusable mechanisms from evidence that merely motivated the repair.

| Inspected item | Disposition | Reason |
| --- | --- | --- |
| Existing AES record() implementation | extend | Repair the owning default recorder instead of introducing a parallel runner. |
| Existing ObservationRecord result seam | reuse | Save the typed result through its existing compatible result mapping. |
| Existing test_evidence.py real repository fixture helpers | reuse | Preserve authentic committed consumer fixtures and add default-run cases. |
| Existing PASS custom helper that prints “4 passed” | bounded exception | Retain custom-command compatibility but explicitly unknown counts; it supplies no proof of substantive passing tests. |
| AES issue #257 | not applicable: evidence source, no mechanism to adopt | It identifies the reported skip-only defect; the actual reproducer verifies it. |
| Official pytest JUnit documentation | not applicable: documentation source | It supports the decision to reuse pytest native JUnit; it is not a separate implementation candidate. |
| Pytest native JUnit output | reuse | Structured counts already exist in the actual test runner. |
| Python standard XML parser | compose | Combine it with existing recorder and validated count model. |
| Existing Pydantic validation | reuse | Keep the native typed seam for nonnegative consistent outcome data. |
| Exit-only SUPPORTS on the default pytest route | supersede | Exit0 alone does not establish a substantive pass. |
| Prose-summary interpretation | not applicable: rejected alternative | No prose inference is needed when native structured results exist. |
| New custom pytest plugin or parallel recorder | not applicable: rejected alternative | Native JUnit plus the existing owner already covers the bounded requirement. |

## Concurrent ownership and integration handoff

Fresh native claims identify three work units. This child codex:evidence-recorder-counts owns only the six precise paths listed above, and produces the native plan plus recorder/checkpoint evidence. The coordinator /root, native lane shaping/harness-context, owns proposals/harness-context, .project-brain/now.md and wiki/index.md; its prospective work is integration and the single AES PR. The Claude lane shaping/aes-learning-loop-unblock owns proposals/aes-learning-loop/PLAN.md and is outside this repair. Those native claims are their current work-unit ownership evidence, not claims that their future outputs are already complete.

Dependencies: this repair depends on native AES acceptance and the existing pytest/Pydantic environment; parent integration depends on this pushed checkpoint and local checks. Conflict surfaces are .aes/target.yaml and its accepted plan during parent integration; the parent must preserve both target deltas. The recorder source, test and guide have this child as sole writer. There is no cross-writer API handoff or independently executing implementation subgraph requiring a new work graph. Recipient /root receives the commit and exact verification after completion; no completed handoff is asserted now.
