## 1. Tests first

- [x] 1.1 The Claude wire answer for a context-only pass has no `permissionDecision`; a deny keeps it
- [x] 1.2 `docs/links.json` lists capability, requirement, scenario, test, file and symbol nodes with their links
- [x] 1.3 The status page's requirement table shows `file:line`
- [x] 1.4 A rendered copy has both hook files running `lockstep-hook` from the copy, and ignores `docs/links.json`

## 2. Build

- [x] 2.1 `hook.py`: drop `allow` from the Claude wire answer
- [x] 2.2 `status.py`: keep `file:line`; `links()` builds the node list; `project.py` writes it
- [x] 2.3 Template hook files, `.gitignore`, README line on turning Codex hooks on
