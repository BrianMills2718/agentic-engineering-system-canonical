# Tests

This repository contains executable tests for Lockstep, its retained AES library,
feedback mechanisms and instruction generation. Test results belong to the exact
revision, environment and command that produced them; they do not redefine intent.

- [Lockstep contract and its proving examples](../docs/architecture/LOCKSTEP.md#evidence-and-change-discipline).
- [Current command definitions](../Makefile): `make check` runs instruction sync,
  tests excluding slow cases, and mypy; `make check-full` adds slow end-to-end cases.
- [Behavior specifications](../openspec/specs/lockstep-plan-format/spec.md).

Consumer repositories under `tests/lockstep/example-layout/` and
`tests/lockstep/lockstep-plan-sample/` are fixtures, not product documentation or
claims of deployed consumer behavior.
