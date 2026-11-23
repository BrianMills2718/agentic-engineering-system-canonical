## 1. Comment sources

- [x] 1.1 Tests first: the two scenarios in `tests/lockstep/checks/test_lockstep_check_trace.py`, failing.
- [x] 1.2 `markers.py`: read `comment_sources` and add their comment-line implementers (private helper).
- [x] 1.3 AES: `comment_sources = ["copier.yml", "template"]`; `Implements:` lines for the six `portable-template`
      requirements where they are built.
- [x] 1.4 Remove the six lines from `docs/planning/trace-accepted.txt`; `make check` exits 0.
