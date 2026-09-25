# AES planning protocol (v0.2 probe 0)

For a human or agent changing an AES project's target (`ART-PLANNING-PROTOCOL`,
`SC-GF-004`). The target is `.aes/target.yaml`; a change to it is written as a
proposal, validated, accepted, and committed before any code it plans is
written. Implementation follows the accepted target; it never edits the target
on the side.

## Steps

1. **Prepare.** On a clean, committed tree run `aes plan prepare` (or
   `--out packet.yaml`). It prints the open gaps of the current reconciliation
   with their ids (`<kind>:<ref>`, e.g. `unrealized:ART-WG5-RUNNER`,
   `insufficient:SC-WG5-001`), every evidence requirement without a route,
   every id the target declares by family, and `proposal_skeleton`.
2. **Write the proposal.** Copy `proposal_skeleton` to a file outside `.aes/`
   and fill it:
   - `proposal_id` (letters, digits, `.`, `_`, `-`; it names the plan file),
     `title`, `rationale` (why this change, in terms of the gaps and the
     target);
   - `closes_gaps`: ids from `open_gaps` that this plan intends to close once
     implemented. Acceptance closes nothing by itself; a gap closes only when
     a later reconciliation no longer reports it. May be empty for a pure
     extension (e.g. the first plan after `aes init`, which has no gaps);
   - `target_delta.add.<family>`: whole new entries, in exactly the target's
     shape. Families: `outcomes`, `normative_items`, `success_criteria` (with
     their nested `evidence_requirements`), `components`, `planned_artifacts`,
     `verification_subjects`, `external_boundaries`;
   - `target_delta.change.<family>`: the whole replacement for an existing
     entry, matched by `id` (by `evidence_requirement_ref` for external
     boundaries). Omitted fields are not kept: repeat them. To add an
     evidence requirement to an existing criterion, change the criterion;
   - `outside_governed_roots`: `{artifact_ref, reason}` for each added or
     changed planned artifact whose path is not under a governed root. Only
     non-source artifacts may be there.
   There is no `remove` in this probe. Removing or renaming an entry is a
   hand edit of the target, committed on its own and reviewed as such.
3. **Validate until clean.** `aes plan validate <proposal>` applies the delta
   in memory and lists every violation: a `change` for an id the target lacks
   or an `add` for one it has; any strict target violation of the result
   (unique ids across families, every ref resolves, every criterion has at
   least one evidence requirement); every evidence requirement in the result
   without a route (a verification subject naming it in
   `evidence_requirement_refs`, or an `external_boundaries` entry saying who or
   what supplies it); a `closes_gaps` id that is not open now; a planned
   artifact outside the governed roots that is source or has no reason. Fix
   the proposal, not the target, and rerun.
4. **Accept.** `aes plan accept <proposal>` refuses on uncommitted tracked
   changes or anything untracked under `.aes/`, on any violation, and when
   `.aes/plans/<proposal_id>.yaml` exists. Otherwise it edits the target in
   place (comments, order and styles kept; added entries at the end of their
   family as written in the proposal; changed entries replaced where they
   stand), writes `.aes/plans/<proposal_id>.yaml` (the proposal plus
   `accepted_at_revision`, the HEAD it was validated against, and
   `accepted_at`, UTC), and prints what changed. It does not commit.
5. **Commit target and plan together**, in one commit and nothing else in it:
   `git add .aes/target.yaml .aes/plans/<proposal_id>.yaml && git commit`.
   Delete the proposal file; the plan keeps it.
6. **Implement**, then record evidence and read `aes status`: the plan is done
   when its work is, but its gaps are closed only by what reconciliation then
   reports.

A target change makes stale every observation that lists `.aes/target.yaml`
among its dependencies; that is correct (they observed the old target) and
they are recorded again after the change.

## Example

The proposal accepted for whygame5's runner (it validates against
`tests/greenfield/fixtures/whygame5-54043e2`; the transcript is in
`proposals/aes-v0.2-greenfield/24-pre-probe-decisions.md` §15). The runner's
defining constraint NI-WG5-006 had no success criterion, so nothing could show
a written runner obeys it; the plan adds the criterion, its route and the test
artifact before the runner is written.

```yaml
schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-WG5-RUNNER
title: Make the runner's fail-stop constraint verifiable before writing the runner
rationale: >
  CMP-WG5-RUNNER and ART-WG5-RUNNER are planned but unrealized, and the
  runner's defining constraint NI-WG5-006 (every call through llm_client with a
  retained receipt, no retries, no fallback model, a failed call stops the run
  with prior receipts intact) has no success criterion, so nothing could show
  that a written runner obeys it. This adds the criterion, a deterministic
  negative-control test for it and the test artifact, and gives the runner
  component the test.
closes_gaps:
  - unrealized:ART-WG5-RUNNER
  - unrealized:ART-WG5-CLI
target_delta:
  add:
    success_criteria:
      - id: SC-WG5-007
        statement: >
          A model call that fails stops the run: the runner does not retry it,
          does not call another model, writes no revision, and keeps the
          receipts of every call made before the failure.
        target_refs: [NI-WG5-006]
        disproof: >
          After a failed call the runner calls the model again (same or another
          model), writes a revision event, or loses an earlier call's receipt.
        evidence_requirements:
          - id: ER-WG5-007-01
            kind: deterministic_test
            requirement: >
              With llm_client replaced by a recording stub whose second call
              raises, one run makes exactly two call attempts, both naming the
              configured model; the first call's receipt is retained, no
              revision event is written, and the run reports the failure.
    planned_artifacts:
      - id: ART-WG5-TEST-RUNNER
        locator: {exact_path: tests/test_runner.py}
        kind: test
        purpose: failed call stops the run without retry or fallback; receipts retained
        semantic_justification_refs: [SC-WG5-007]
    verification_subjects:
      - id: VS-WG5-RUNNER-FAIL-STOP
        criterion_refs: [SC-WG5-007]
        evidence_requirement_refs: [ER-WG5-007-01]
        proof_kind: deterministic_test
        proof_role: negative_control
        locator: tests/test_runner.py
        purpose: a failed call stops the run with no retry, no fallback and earlier receipts intact
  change:
    components:
      - id: CMP-WG5-RUNNER
        responsibility: the two-call loop over llm_client with receipts, no retries, no fallback; stops after one call on NO_FINDING
        target_refs: [NI-WG5-003, NI-WG5-006]
        planned_artifact_refs: [ART-WG5-RUNNER, ART-WG5-CLI, ART-WG5-TEST-RUNNER]
```
