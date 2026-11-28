## Why

Brian, 2026-11-27 18:51: "we spent a lot of time talking about an opinionated file structure and this doesn't cut
it"; 19:05: "even in the documentation section we had opinionated documentation. like research goes in one place.
generated files go in another". The homes were decided (wiki_methodology `REPOSITORY_CONCERN_ROOTS.md`: `docs/`,
`research/`, `evidence/`, `generated/`), but a fresh copy of the template declares none of them, its `make check`
runs no rule about where a document lives, and the edit hook says nothing when an agent writes a note in the wrong
place. The only rule that exists, the workspace's `md_file_cap.py` layout column, reads `.agentic/repo.yaml`, which
the template does not ship, and guesses a document's kind from its folder name.

## What Changes

- `lockstep.yaml` may declare `document_homes:`: each home (a folder, or one file) with what belongs there.
- When it does, the whole-tree `lockstep check` (run by `make check`) reports every tracked Markdown file outside all homes (instruction files,
  hidden folders and `tests/` excepted), naming the file and the homes.
- The edit hook warns when an agent writes such a file, and names the homes.
- A fresh copy declares its homes and ships an empty `research/` folder; its AGENTS.md lists them.
- Component folders (decision 0003) and a generated requirements document (decision 0004) are not in this change:
  both decisions record no words of Brian's (`Source: inferred by agent`).

Plan size: small
