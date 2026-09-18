---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills explicit repair approval
date: 2026-09-18
reversible: true
supersedes:
  - docs/decisions/0007-provider-independent-verification-and-blob-evidence-carry-forward.md
---

# Decision 0008 — Verification is provider-independent and evidence reuse follows the executed subject closure

## Context

GitHub Actions is unavailable because the account has exhausted hosted-run funding.
That administrative constraint must not become code evidence or a delivery gate.

Decision 0007 correctly separated verification authority from a CI vendor, but its
Plan 001 evidence-reuse rule was too weak: it compared a hand-selected list of
files rather than the transitive executable subject. Review found a concrete
counterexample:

- `cli.py` was byte-identical to the authentic execution revision, but imports
  `render_html.write_outputs`;
- `render_html.py` changed after that execution;
- the pinned external-consumer test also calls `render_html()`;
- that pinned test retained assertions for wording removed by the corrected
  renderer.

Therefore file identity for the entrypoint alone could not support a current
end-to-end execution claim.

Enforced Planning already provides `verification_batch.py`, which binds a
verification decision and command to an exact clean Git revision. AES should use
or extend that incumbent execution-governance mechanism rather than invent a
generic duplicate verification framework.

## Decision

### 1. Hosted CI remains optional infrastructure

GitHub Actions or another hosted runner may execute verification, but provider
availability, billing state, queue state, or runner failure is neither PASS nor
FAIL.

Local or otherwise authorized execution is first-class evidence.

### 2. Fresh execution binds to an exact revision and command

When fresh verification is required, prefer the Enforced Planning verification
batch mechanism (or its future provider-owned successor) to bind:

- the exact clean Git revision;
- the exact verification decision;
- the exact command;
- allowed untracked inputs where explicitly justified.

AES does not create a parallel generic verification-batch authority.

### 3. Evidence reuse is claim-specific and follows the transitive executed subject

Prior execution may inform a later revision only for a claim whose complete
relevant executed subject is unchanged.

That subject includes, as applicable:

- directly executed modules;
- transitively imported local modules that can affect the claimed behavior;
- verification/test code used by the claim;
- package/dependency declarations and lock state that affect resolution;
- relevant configuration;
- external executable/tool assumptions;
- immutable external-consumer identity/input;
- environment facts when behavior materially depends on them.

A hand-selected file list is insufficient unless it is itself derived from and
justifies this closure.

### 4. Unchanged subclaims may retain narrower historical evidence

A changed renderer does not invalidate historical evidence for resolver-only
semantics if the resolver claim does not execute the renderer.

Conversely, prior CLI or pinned end-to-end execution does not carry across a
changed renderer when those paths execute the renderer.

The evidence record must state the exact narrower claim being retained.

### 5. Changed tests can reveal an unverified current behavior

If a current test disagrees with current implementation/output, the correct state
is not "evidence carried forward." Repair the test or implementation according to
the accepted semantics, then obtain fresh execution for the affected end-to-end
claim.

### 6. Utility remains independent

Technical execution, source inspection, test consistency, and exact revision
binding do not establish stakeholder utility. A changed human-facing projection
still requires direct follow-up observation.

## Plan 001 current disposition

Review established:

- core Repository Context resolver/model/adapter behavior remains byte-identical
  to the authentically executed revision and may retain **narrow historical
  resolver evidence**;
- the renderer changed after that execution;
- the CLI executes the changed renderer;
- the pinned external-consumer test executes the changed renderer;
- the pinned test contained stale renderer wording assertions and has been
  corrected in the repair change;
- therefore **current end-to-end CLI / pinned-consumer acceptance requires one
  fresh local/external execution after the repair**;
- GitHub Actions is not required for that execution.

## Consequences

- Decision 0007 is superseded.
- The earlier Plan 001 evidence-carry-forward receipt is retained as historical
  evidence of the review attempt but is not authoritative for current
  end-to-end acceptance.
- Enforced Planning remains the natural owner of generic exact-revision
  verification-batch machinery.
- Plan 001 technical closure requires a fresh local/external run of the repaired
  focused/pinned path; follow-up stakeholder utility remains separately required.
