## 1. Read-before-write report

- [x] 1.1 Tests first: `tests/lockstep/test_read_before_write.py`, one per scenario, marked `@pytest.mark.req`
- [x] 1.2 `src/lockstep/read_before_write.py`: parse the four session formats, mark each write, print the report
- [x] 1.3 `lockstep reads` branch in `src/lockstep/check.py`
- [x] 1.4 Run it on the step 3 proof sessions (Claude 2bc9a1cc, Codex 01a21f4b) and one real working session
