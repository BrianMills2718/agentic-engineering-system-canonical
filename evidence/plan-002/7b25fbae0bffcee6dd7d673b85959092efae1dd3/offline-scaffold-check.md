# Plan 002 V1 — isolated offline scaffold check

Status: **PARTIAL VERIFICATION ONLY**
Observed: 2026-09-22
Subject revision: `7b25fbae0bffcee6dd7d673b85959092efae1dd3`
Branch: `plan002/v1-first-offline-replay`

## What was checked

The current policy-control source, first frozen replay case, and focused tests were fetched from the branch through the GitHub connector and reconstructed in an isolated local temporary package.

Observed environment:

- Python 3.13.5
- pytest 9.0.2
- pydantic 2.13.4 (repository pins 2.13.5; this is therefore close compatibility evidence, not exact dependency verification)

Observed checks:

- focused policy-control suite: **17 passed**
- `python -m compileall -q src`: PASS for the reconstructed policy-control package
- `pyproject.toml`: parsed successfully and exposed `aes-policy-replay = agentic_engineering_system.policy_control.cli:main`
- `python -m agentic_engineering_system.policy_control.cli --help`: PASS
- first frozen case loaded as `ReplayCaseV1`: PASS

## Defect found and repaired before the check

The first script-entry edit had inserted a literal `\n` into `pyproject.toml` instead of a real newline. Revision `7b25fbae0bffcee6dd7d673b85959092efae1dd3` includes the repair.

## What this does prove

- strict replay models instantiate as expected;
- post-decision label leakage is rejected by the evaluator-input contract;
- receipt provenance cannot be half-bound;
- fake TypeSafe model discovery and Noul request/response handling work;
- provider unavailable/protocol-error states remain explicit;
- malformed Noul probabilities do not become observed success;
- the selected authentic P10-S4 block case conforms to the replay-case schema;
- the offline CLI/package entrypoint is syntactically and structurally usable.

## What this does not prove

- full repository tests or governance checks;
- exact dependency verification under pydantic 2.13.5;
- authenticated TypeSafe access;
- a real `GET /v1/models` response;
- a real Jev judgment for the selected case;
- generated replay-report usefulness;
- live policy behavior of any kind.

The next discriminating evidence remains the authenticated TypeSafe provider smoke followed by one real offline replay.
