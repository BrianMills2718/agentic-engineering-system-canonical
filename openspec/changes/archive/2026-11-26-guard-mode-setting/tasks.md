## 1. Build

- [x] 1.1 Tests first: guard.mode block refuses, warn and absent warn, PCW_MODE overrides, a bad value refuses
- [x] 1.2 `SideFile.guard_mode` parsed by `load_side_file`; `blocks()` reads env, then guard.mode, then warn
- [x] 1.3 `side_file_problems` names a bad `guard.mode`
- [x] 1.4 `lockstep init` writes `guard: {mode: block}`, drops `PCW_MODE=block` from the hook command, upgrades its own old command when lockstep.yaml has `guard:`
- [x] 1.5 Regenerate docstrings (`lockstep check project`), layout rows, archive
