## ADDED Requirements

### Requirement: AES plans every tracked file

This repository's `lockstep.yaml` SHALL have one `layout:` row with a nonempty purpose for every Git-tracked file, SHALL list every top-level folder (with a trailing `/`) and top-level file under `governed:`, and SHALL project the rows' paths and purposes into `generated/files.md`, which `wiki/index.md` links.

Source: Brian, 2026-11-13, AES #849: "Every Git-tracked file must be reachable and summarized from `wiki/index.md`"; where the rows live: Brian, 2026-11-11, approving `proposals/one-planning-tool/DESIGN.md` (line 41: which files exist and why lives in `lockstep.yaml` `layout:` rows). The checkable form is inferred by agent.

#### Scenario: Every tracked file has a planned row and the catalog page is current

- **GIVEN** this repository at HEAD
- **WHEN** its tracked files, `lockstep.yaml` and `generated/files.md` are read
- **THEN** every tracked file has a layout row with a purpose, every top-level entry is governed, the projection of the layout into `generated/files.md` is current, and `wiki/index.md` links `generated/files.md`
