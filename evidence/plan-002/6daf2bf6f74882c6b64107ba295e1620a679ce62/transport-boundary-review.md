# Existing Jev adapter: bounded repair and verification

Date: 2026-09-23 UTC
Status: source-level repair candidate; not merged or deployed

## Authority and scope

This follows Brian's approved policy/feedback consolidation handoff on
[Project Meta #1977](https://github.com/BrianMills2718/project-meta/issues/1977#issuecomment-5788958633).
Jev remains a first-choice candidate for fast contextual judgments. This is a
repair to the existing adapter in [AES PR #29](https://github.com/BrianMills2718/agentic-engineering-system-canonical/pull/29),
not a second provider client or another policy engine.

PR #29 baseline: `7561ad92481cde4c11784315764810b8863f39ec`.
Verified repair: `6daf2bf6f74882c6b64107ba295e1620a679ce62`.
Review branch: `fix/jev-review-boundaries-20260923`.
The original PR branch, canonical main, active-plan routing, live client
configuration and policy semantics were not changed. The separate branch is a
review candidate, not a native execution claim or a claim to another agent's lane.

## What was reproduced and repaired

| Failure reproduced with synthetic inputs | Small repair |
| --- | --- |
| A socket TimeoutError escaped the adapter instead of producing an explicit unavailable result. | Normalize transport failures into the existing JevUnavailableError path. |
| A NaN Noul value was accepted as OBSERVED. | Positively validate the probability range before conversion. |
| An HTTP error response body was copied into error_summary and therefore the durable result. | Retain HTTP status, not the arbitrary response body; transport error text is reduced to the exception type. |
| The generated JevClient representation exposed api_key. | Exclude the credential field from repr. |

These are reproduced adapter behaviors, not evidence that the real TypeSafe
service returned NaN or that a real credential/private payload was disclosed.
The tests contain synthetic markers only and replace urlopen; they do not
contact TypeSafe or use a real API key.

Runtime change: 19 inserted / 10 removed lines in the existing adapter.
A separate focused test file adds six checks. No package dependency was added.

## Verification observed

Environment: native Windows; Python 3.14.7; Pydantic 2.13.5; pytest 9.1.1.
Imports were explicitly resolved from the exact review checkout using PYTHONPATH,
not from the older editable installation in the reused test environment.

1. Unmodified PR #29: existing policy-control suite **17 passed**; generated AGENTS sync passed.
2. Six independent boundary checks on that unmodified baseline: **4 failed, 2 passed**.
3. After the repair: combined policy-control suite **23 passed**.
4. After committing the repair at `6daf2bf6f74882c6b64107ba295e1620a679ce62`:
   the same suite again returned **23 passed**, and the checkout was clean.
5. `git diff --check` and generated AGENTS sync passed before the repair commit.

Command, with the review checkout's `src` and root on PYTHONPATH:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 \
python -m pytest -q -p no:cacheprovider tests/policy_control
```

No broad repository suite, Linux run, native Claude/Codex hook, account-specific
model discovery, real model judgment, provider latency or semantic-quality result
is claimed by this record. A green transport test is not a working feedback loop.

## Remaining integration questions

The current adapter asks one support yes/no question. It does not separately
expose missing context versus evidence that contradicts a claim. Before using it
for the approved live feedback boundary, preserve that distinction so missing
context causes authorized evidence gathering or a narrower claim, not an invented
false-claim verdict. This is a needed semantic distinction, not a requirement to
encode all engineering cases into rules.

Review/reuse the adapter through the approved shared model-routing and observation
boundary. The existing direct urllib path is not evidence that shared llm_client
routing, cost observation or installed-client enforcement has been integrated.
The offline default timeout is not an approved interactive-hook latency budget.
Keep model/question identity and uncertain/error results explicit. Do not infer
Jev accuracy or full source provenance from a typed result or a source digest.

The public API schema was rechecked at
https://api.typesafe.ai/openapi.json (2026-09-23 UTC). It documents Noul as a
probability in [0,1], caller-defined questions and caller-supplied state. This
review tested only the existing Noul adapter; it did not expand question types.

## Why live parity remains pending

Project Meta #1977 and Agent Skills #319 contain historical parity failures.
Those reports were reread; they are not fresh diagnoses of today's installed
client state. At both preflight and the final check, the machine's explicit
WSL maintenance lock prohibited launching Ubuntu during another agent's offline
backup. The lock was left untouched, and no WSL launch was attempted.

After that maintenance ends, the next primary task remains an actual installed
path: configured -> enabled/trusted -> invoked -> correct context -> useful
feedback -> retained observation -> owned concern -> verification/recurrence.
Do not close #1977 or claim either client repaired based on this adapter review.

## Publication

The verified repair was committed and pushed through native Git. GitHub CLI
API access was unavailable because the native CLI is not logged in; a separate
PR had not been created at this checkpoint. Do not bypass or overwrite the
original PR owner's branch. Reconcile this dependent candidate before merging.
