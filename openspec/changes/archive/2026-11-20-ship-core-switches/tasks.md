## 1. Switches

- [x] 1.1 Tests first in `tests/test_ship.py`: `ship_planning_gate: false` skips the planning gate on a new repository with no package; `ship_one_page_plans: false` lets an incomplete one-page plan merge; no answers file keeps both on
- [x] 1.2 `addon_on()` in `scripts/ship.py`, read before each of the two gates

## 2. Hidden acceptance gate

- [x] 2.1 Tests first: a passing record at HEAD merges; a failing record, a record at another commit, and a record with uncommitted files are refused with nothing pushed; no record merges with the printed line
- [x] 2.2 `accept_refusal()` in `scripts/ship.py`, before the rebase step; module docstring updated
