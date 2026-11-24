## Why

Every edit-hook refusal ends with a pointer to `python -m lockstep.wiki`. In a layout repository (AES itself and
every template copy) that command crashes: `lockstep.wiki` reads requirement status through `aes reconcile`, which
needs `.aes/project.yaml`. Found 2026-11-23 while sorting the 14 old-route modules for Q54 (Brian: "i approve").

## What Changes

- In a layout repository a refusal points to the layout rows in `lockstep.yaml` and to `uv run lockstep show <file>`,
  which prints the file's requirements and their tests. A repository with `.aes/target.yaml` keeps the wiki pointer.
