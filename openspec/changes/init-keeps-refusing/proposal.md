## Why

The 2026-11-27 audit (R2, R3; reviewer reproduced R3) found two ways `lockstep init` quietly weakens a repository:

- A `lockstep.yaml` with an empty `guard:` line counts as "sets the guard", so init removes `PCW_MODE=block` from the
  old hook command; the hook then reads no mode and falls back to `warn`. Refusing becomes warning, unasked.
- When `.claude/settings.json` already points `inside-success` at another source, init reports a conflict but still
  adds `enabledPlugins."company-planning@inside-success": true`, so the plugin loads from that other source.

## What Changes

- Init upgrades the old hook command only when `guard:` sets a `mode`.
- Init does not add the `enabledPlugins` entry while the marketplace source conflicts.

Plan size: small
