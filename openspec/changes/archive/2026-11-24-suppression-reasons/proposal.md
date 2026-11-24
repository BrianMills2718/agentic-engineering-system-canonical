# An added suppression names its reason

Plan size: full
Planning package: docs/planning/planning-package.json

Full, not small: the check ships in the Lockstep package and the template's `make check`, which other repositories use.

## Why

An agent that cannot make a lint, type or import-contract error go away can silence it with `# noqa`,
`# type: ignore` or an import-linter `ignore_imports` entry, and nothing asks why. Brian approved borrowing the
ideas from the Reddit post "half a year of AI coding got me nowhere" into the AES plan and left the slice to the
agent (Brian, 2026-11-24: "i approve adding the redit ideas to the plan and i will trust your jdugement on the
impelemtnation prirotiy"). Requiring a reason on each added suppression is the cheapest of those ideas. The exact
reason format and scope are inferred by agent (basis: what ruff, mypy and import-linter accept, tested 2026-11-24).

## What changes

- New `lockstep check suppressions --base <rev>`. It reads the lines added since where the branch started, in
  tracked Python files and in import-linter settings, and fails on an added `# noqa`, `# type: ignore`,
  `# pyright: ignore` or `# pylint: disable` that is not followed on the same line by a further `#` comment of
  at least three words, and on an added `ignore_imports` entry with no reason. Lines that were already there are
  never judged.
- The reason is a further `#` comment (`# noqa: F401  # re-exported for the fixture`), because mypy rejects
  `# type: ignore[x] -- reason`. In `.importlinter` and `setup.cfg` the reason is a comment line directly above
  the entry, because configparser keeps an inline `#` in the value.
- AES's `make check-format` and the template's `make check` run it.

## Impact

`src/lockstep/checks/suppressions.py` (new), `src/lockstep/checks/cli.py`, `src/lockstep/checks/config.py`,
`Makefile`, `template/Makefile`, `lockstep.yaml`, `openspec/specs/lockstep-checks/spec.md`.
