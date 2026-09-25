# Clean-user run 3 of the Greenfield getting-started page (2026-09-25)

At AES `3dd2b9a` (the phase-7b commit, run before merge and merged with a
merge commit). Observation of record: `.aes/observations/OBS-AES-CLEAN-USER-3dd2b9a.yaml`
(supersedes run 2). Same setup and caveat as runs 1 and 2.

Result: 34 commands, every page command exit 0, five hook-gated commits;
`aes plan` round trip from the page's block; `aes status` after evidence
`1 supported … 1 current … plans: 1 accepted, 0 unreachable`; after the page's
deliberate edit `0 supported, 1 insufficient`, `1 stale`, matching the page.

Found (queued, not blocking): `aes context` omits `ART-PKG` from the SC-001
packet although NI-001 links it, and its lines carry no per-line source;
`aes plan accept` accepts with an untracked file present (the page's
"uncommitted changes" reads as tracked changes only); the no-remote notes are
not on the page.
