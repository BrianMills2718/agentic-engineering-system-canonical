## 1. Layout files without a cog block

- [x] 1.1 Tests first: an existing file with a current `Implements:` block is editable; a stale one is refused naming `lockstep check project` and allowed after it runs
- [x] 1.2 `projection_stale` uses `checks.project.stale_copy` for a layout file with no cog block; the hook's refusal and after-edit hint name `uv run lockstep check project` in layout mode
