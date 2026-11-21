## Why

Brian, 2026-11-21: "i thoguht as canoncial was one repo that contained all this stuff?", then "yes" to moving the
template here. A second user today needs two addresses: this public repository for Lockstep and `ship`, and the
private `code2-template` for the starter files, which they cannot read. With the template here, one public address
does both: `uvx copier copy --trust gh:BrianMills2718/agentic-engineering-system-canonical <dir>`.

## What Changes

- `copier.yml` (at the repository root, `_subdirectory: template`) and the 23 starter files under `template/` move
  here unchanged from `code2-template` at `6e15ab3`, except the header comment, which names this repository.
- The `portable-template` spec and its tests move with them; the check that a rendered copy names nothing of the
  owner's machine (`machine_bound`) becomes a test helper.
- README and wiki say how to make a repository from here.
- `code2-template` keeps working; pointing it here, and archiving it, come after this merges.

## Test seam

- `uvx copier copy --trust --defaults --skip-tasks` from a folder holding `copier.yml` and `template/`; files read
  from the rendered folder.

## Impact

- New: `copier.yml`, `template/`, `tests/test_template_portable.py`, spec `portable-template`.
- Changed: `README.md`, `wiki/lockstep.md`, the file inventory.

Plan size: small
