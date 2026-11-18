## 1. Tests first

- [x] 1.1 `tests/test_ship.py`: one test per scenario of "Refuse a merge whose OpenSpec change lacks a prior-art record", with a fake prior-art script in a fake workspace folder; each fails before the code

## 2. Source

- [x] 2.1 `scripts/ship.py`: `prior_art_refusal`, called in `main` after the one-page plan check

## 3. Finish

- [x] 3.1 archive; `lockstep check project`; `make check`; `ship`
