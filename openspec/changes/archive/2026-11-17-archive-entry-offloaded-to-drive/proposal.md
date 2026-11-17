## Why

offload-cold (personal-file-infra) moves every `~/archive` folder idle for 2 days to a tar on Google Drive
(`google_brian:Data/90_Archive/offloaded/archive/<YYYYMM>/<name>-<stamp>.tar.gz`) and records it in
`~/projects/data/logs/offloaded.jsonl`. `archive_map.py --check` only knew "present in ~/archive" or "gone",
so every offloaded folder was reported as "gone from ~/archive (remove it, or restore it)": 87 such findings on
2026-11-17, including the 22 Inside Success bare mirrors whose registry text still said to restore with a local
`git clone`. The only ways to clear the finding were to delete the registry entry (losing where the data went)
or to download the tar again.

## What Changes

- A registry entry may carry `offloaded:` naming the exact Drive tar (not just the folder name: a later offload
  of a recreated folder writes a newer tar of the same name). An entry whose folder is absent from `~/archive`
  and that names an `offloaded:` tar ending in `.tar.gz` is not reported as gone.
- An absent entry without `offloaded:` is still reported as gone.

Source: inferred by agent, from Brian's 2026-11-17 task "archive_map_registry.yaml lists local bare mirrors that do
not exist ... correct the registry" (working default; undo by reverting this change).

## Impact

- `scripts/archive_map.py` (check), `tests/test_workspace_map.py`.
- No network call: the check does not open Drive; the offload ledger and the tar itself are the evidence.
