## 1. Tests first

- [x] 1.1 Port code2check's tests for trace, arch, test-first, sources and docmeta to `tests/lockstep/checks/`
- [x] 1.2 Tests for the block, warn and off modes and the other `lockstep.yaml` settings

## 2. Code

- [x] 2.1 Port the checks and their helpers (`spec`, `markers`) to `src/lockstep/checks/`
- [x] 2.2 `checks/config.py` reads `lockstep.yaml`; `checks/cli.py` runs a named check and applies its mode
- [x] 2.3 `lockstep.check.cli` hands `check <name>` to it; the side file accepts the new keys
