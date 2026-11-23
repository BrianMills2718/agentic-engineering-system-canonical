## 1. Tests first

- [x] 1.1 Decisions are read from their existing Governs, status and superseded_by lines (front matter and MADR)
- [x] 1.2 An edit, a shell command and a governed-only file get the decisions, in order, superseded flagged; logged
- [x] 1.3 At most three decisions in full; no decisions folder gives no text
- [x] 1.4 `docs/links.json` has decision nodes linking to file, folder and capability nodes
- [x] 1.5 A rendered copy's decision 0001 governs `docs/architecture/model.c4`

## 2. Build

- [x] 2.1 `lockstep/decisions.py`
- [x] 2.2 Hook: edit route (no plan, no artifact, layout packet) and shell route
- [x] 2.3 `status.links()` decision nodes
- [x] 2.4 Template decision line and README line
