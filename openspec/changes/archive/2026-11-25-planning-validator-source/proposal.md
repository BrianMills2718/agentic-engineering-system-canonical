# The planning validator's source is a setting

Plan size: full

Planning package: docs/planning/planning-package.json

Full because `ship` and `lockstep plan check` run in other repositories, and `lockstep.yaml` is a contract every
repository carries. The plan is `docs/planning/next.goal.md`, slice 2.

## Why

Brian, 2026-11-25: "the whole systm should be configurable so you can congfigure what is on or off or any other
settings. for any piece." The validator `ship` and `lockstep plan check` run is fetched from a hardcoded
`~/code2/company-planning` at `origin/main`. Inside Success repositories reach Company Planning through the private
mirror `Inside-Success/company-planning`, which only an environment variable could select, so every person and agent
had to know to set it.

## What changes

- `planning.validator: {repo, ref}` in `lockstep.yaml`, read from the default branch at origin like the planning gates,
  names the repository the validator comes from and its branch.
- The order is: `SHIP_PLANNING_VALIDATOR`, then `SHIP_COMPANY_PLANNING`, then the configured repository, then
  `~/code2/company-planning`. Every run logs which source won; an environment variable that overrides a configured
  repository prints a warning.
- A configured repository is kept as a bare clone under `$XDG_CACHE_HOME/lockstep/`, fetched under a lock with no
  password prompt and a timeout. Credentials come only from the user's own git setup.
- `lockstep init` writes the setting commented out, with no address, because Company Planning is private.
