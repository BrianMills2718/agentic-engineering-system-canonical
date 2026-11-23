# Updating an older copy leaves its starter files alone

Plan size: small

## Why

`copier update` of a real copy made before #1027 (template at `2e8791447`) added empty cog blocks to
`src/<package>/__init__.py`, `cli.py` and `core.py`, naming layout rows the copy does not have, and dropped the
hand-written `Implements: core/reports-its-version` line from `core.py`. Afterwards `lockstep check trace` exited 1
(`unimplemented core/reports-its-version`). The earlier test built its old template from today's files and missed this.

## What changes

- `copier.yml` excludes `src/<package>/*.py` on update, as it already excludes `lockstep.yaml`; a fresh copy still
  gets them.
- The template's `AGENTS.md` layout bullet applies "where `lockstep.yaml` holds `layout:` rows", so it is true for an
  updated older copy too.
- The update test builds its old template from the real prior version (`git archive 2e8791447`).
