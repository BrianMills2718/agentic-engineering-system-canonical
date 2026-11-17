## 1. Tests first

- [x] 1.1 One test per scenario, on a throwaway repository with a `main` that moved after the branch started; both fail before the source changes

## 2. Source

- [x] 2.1 `checks/changed.py`: `compare_with` (merge base of the given revision and HEAD); `check` uses it
- [x] 2.2 `checks/test_first.py`: `check` uses it

## 3. Finish

- [x] 3.1 `make check` exits 0; archive; `openspec validate --all --strict --no-interactive`
