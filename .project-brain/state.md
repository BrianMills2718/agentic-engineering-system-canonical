# State (2026-10-02)

Detail and evidence: `proposals/hive-brain-v1/ROADMAP.md` ("Capabilities",
"Evidence", "Progress log"). This page is the short version.

- **Hive brain v1** (`working`): 0 of 5 done conditions met.
  - Paperclip on personal-vps runs three agents (Coordinator, Research and Code
    Review, Brian Contact). Every run has failed since 2026-10-02 20:30 UTC
    because of an expired Claude login (upstream bug). The fix is wired; it
    waits on Brian creating a one-year token with `set-claude-token.sh`.
  - Terminal relay: `python3 scripts/hive/decisions.py` lists agents not
    working, then tasks waiting on Brian.
  - Learning loop slices 1–2 built: legacy learnings labelled; new `kind:*`
    issues labelled weekly by a timer on personal-vps (summaries on issue #74).
  - Jev gate: observe mode in every Claude and Codex session; rule K1
    (never remove the worktree you stand in) enforced since 2026-10-03.
  - Silence check: `python3 scripts/hive/controls.py`; weekly readout:
    `python3 scripts/hive/readout.py`; backups restore
    (`host/restore-check.sh` in personal-vps).
  - Project brains: this one is the first; `scripts/hive/brain_fresh.py`
    reports a stale brain.
- **AES v0.2 product** (`approved` as realized, Decision 0010): governed by
  `.aes/target.yaml`; `aes status` is the one-screen view. Not the current
  focus.
