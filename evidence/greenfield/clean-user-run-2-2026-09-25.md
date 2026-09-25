# Clean-user run 2 of the Greenfield getting-started page (2026-09-25)

Repeat of `clean-user-run-2026-09-25.md` at AES `2d3486b` after phases 3–6.
Observation of record: `.aes/observations/OBS-AES-CLEAN-USER-2d3486b.yaml`
(supersedes `OBS-AES-CLEAN-USER-0503735`). Same runner setup and the same
caveat: a fresh agent given only the page, on the maintainer's machine, since
the repository is private by decision.

Result: 26 commands, every exit code 0, five commits gated by the packaged
hook; the runner found the pin with `git ls-remote` as the page now says;
`aes plan prepare → validate → accept` worked from the page's block
(`PLAN-001-GREET`, 6 additions); `aes status` after evidence:
`1 supported … 1 current, 0 stale, 0 unknown, 0 unreachable; 0 superseded`;
after the page's deliberate edit: `0 supported, 1 insufficient`, `1 stale`,
matching the page's example line for line.

Under-specified (runner's report): section 6's staleness demonstration and
`aes reconcile` are prose only; venv re-activation per shell is not mentioned;
`aes init`'s own next-step hint ("plan it in .aes/target.yaml") contradicts the
page's `aes plan` route — tool fix queued for phase 7; the global
`core.hooksPath` override is printed by the tool, not the page.
