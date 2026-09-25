# Clean-user run of the Greenfield getting-started page (2026-09-25)

Evidence for `ER-SC-GF-001-01` (external consumer observation), retained here
until AES canonical has its own `.aes/observations/` (roadmap phase 6), when it
is converted to an observation record at this exact revision. Converted in
roadmap phase 6b: `.aes/observations/OBS-AES-CLEAN-USER-0503735.yaml` (this
file stays as the report the record cites).

- AES revision installed: `0503735f9` (`aes --version` → `0.1.dev367+g0503735f9`)
- Material given to the runner: `docs/greenfield/GETTING_STARTED.md` only, plus
  the pin id. The runner was a fresh Claude Opus 5.5 agent session with no
  access to this conversation, the proposals directory, AES source, or any
  other repository. It ran on the maintainer's machine, so the `git+https`
  install used that machine's GitHub credentials: this is **not** a
  no-private-access run, because the AES repository is private. That boundary
  is the open item for SC-GF-001, not the page or the tool.
- The runner reported that the session loader also surfaced the repository's
  `AGENTS.md`/`CLAUDE.md` when it opened the page; it states it did not use
  them for any step.

## Result

Every command on the page exited 0. Three commits, each gated by the packaged
pre-commit hook (`aes hooks install`). Final standing:

```
evidence: 1 criteria: 1 supported, 0 insufficient, 0 refuted; 1 observation(s)
  SC-001: SUPPORTED
    ER-001-01: SUPPORTED - supported by OBS-GREET-e122df8d
  observations:
    OBS-GREET-e122df8d: CURRENT - no dependency changed since e122df8d0e47
```

Steps, in the page's order: `git init`; venv; `pip install … @0503735f9`;
`aes --version`; `.gitignore` + `pyproject.toml`; `aes init --project-id greeter
--actor … --outcome …` (`.aes/` held exactly `project.yaml` and `target.yaml`);
`aes hooks install` (printed the global-hooksPath note); first commit (hook: `OK
topology: 0 governed file(s)`); target written from the page's block; `aes
target validate`; `aes topology check` (2 planned, unrealized); `aes context
SC-001` (64 lines); source + test written; second commit (hook: `2 governed
file(s), 0 orphan(s)`); `aes evidence record VS-GREET --depends-on
src/greeter/__init__.py` (`SUPPORTS for ER-001-01 at e122df8d0e47`); `aes
evidence status`; third commit.

## What the page under-specified (runner's report)

1. No way to find a valid `<sha>` — fixed in the page in the same change.
2. The page does not say `aes hooks install` overrides a global
   `core.hooksPath`; the tool prints it, so left as is.
3. Ordering of the evidence step relative to the "Greet by name" commit was
   implicit; the literal order worked.
4. The prose says "replace the empty lists" while the block overwrites the
   whole file; the block was used.
5. The failure claims on the page (orphan blocks a commit, STALE, REFUTED,
   refusal on uncommitted changes) were not exercised by the runner; the
   orphan and STALE cases were exercised by the page's author on the same
   revision (PR #45 report), REFUTED was not run by anyone.

Runner's scratch tree: session scratchpad `clean-user/greeter` (ephemeral; the
outputs above are the retained record).
