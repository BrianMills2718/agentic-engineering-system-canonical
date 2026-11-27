## MODIFIED Requirements

### Requirement: Refuse a branch whose hidden acceptance run failed or is out of date

After it has caught up with the default branch and before it runs the check, `scripts/ship.py` SHALL read every readable `summary.json` under `${XDG_STATE_HOME:-~/.local/state}/lockstep-runs/<repository>/` (the main checkout's folder name) whose `branch` is the branch being shipped or whose `head` is a commit reachable from HEAD and not from the default branch; an unreadable one SHALL be skipped with a printed warning. When there is at least one, ship SHALL refuse the merge with nothing pushed, naming `lockstep accept check <change>` as the way to record a new run, unless the newest by run id has `accept.exit` 0, a positive integer `accept.passed`, zero `accept.failed` and `accept.errors`, `uncommitted` 0, and `head` equal to HEAD as it will be merged (so a branch that was rebased must be checked again). With none, ship SHALL print and log `ship: no hidden-test run recorded for this branch` and go on; a run made by another user or under another `XDG_STATE_HOME` is not found, which this message makes visible. Missing or malformed acceptance counts SHALL refuse a matching record, including a record rewritten after ship's own rebase. A legacy record with valid exit, pass, failure and error fields may omit the skipped count.

Source: minimal-core-2026-11-20.md section 6 step 2, hidden tests "must pass before `ship`" (inferred by agent from the 2026-11-20 plan-fidelity test, where they were the check that measured success), under Brian, 2026-11-20: "the goal is to give a well specified plan to an agent on some proejct nad have it faithfulyy and successfully impelemnt it".

Source: the positive-evidence check is inferred by agent from the all-skipped audit reproduction and Brian's 2026-11-26 instruction "make any high confidence imrpvoements".

#### Scenario: A passing record at HEAD merges

- **GIVEN** a run record for the branch with `accept.exit` 0, `uncommitted` 0 and `head` equal to HEAD
- **WHEN** ship runs with a passing check
- **THEN** it merges

#### Scenario: A failing or out-of-date record is refused

- **GIVEN** a run record for the branch whose hidden tests failed or did not run, or whose `head` is another commit, or which counted uncommitted files
- **WHEN** ship runs
- **THEN** it exits 1, names `lockstep accept check`, and the branch is not on the remote

#### Scenario: No record goes on

- **GIVEN** no run record for the branch
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: no hidden-test run recorded for this branch`

#### Scenario: A successful exit without a passing count is refused

- **GIVEN** a matching hidden-test receipt with exit zero and zero, missing or malformed passing evidence, either from the original run or from a rerun
- **WHEN** ship reads the receipt
- **THEN** it refuses the merge and names `lockstep accept check` as the recovery command
