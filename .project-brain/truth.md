# Decisions and rejected alternatives

Full table with reasons: `proposals/hive-brain-v1/ROADMAP.md` "Decisions and
assumptions" and `proposals/aes-learning-loop/DESIGN.md`. Rejected
alternatives, which are the point of this page:

- **Project brains live in each repo's `.project-brain/` folder** (`working`,
  agent-decided 2026-10-02 after a landscape review). Rejected:
  - gbrain (garrytan/gbrain): its source is also markdown in git, but it adds a
    database, Bun and fast-moving releases. Later, as a search index over these
    files, if questions start crossing projects.
  - Hermes (NousResearch/hermes-agent): an agent runtime with per-profile
    memory capped at 2,200 characters, not a shared store.
  - mem0, Letta, Cognee: need a memory server both the VPS container and WSL
    can reach, and their memory can't be diffed or reviewed.
  - Paperclip issue documents: fine for one task's plan, but local sessions can
    reach them only over ssh.
- **Agents sign in to Claude with a one-year setup token** (`working`, 2026-10-02).
  Rejected: Paperclip's "My Claude subscription" connection, which stores an
  access token that expires after about 8 hours (paperclipai/paperclip#13725).
- **The weekly learning-loop run is a systemd timer** (`working`, 2026-10-02).
  Rejected: a Paperclip routine, because a fixed script needs no agent, and the
  timer keeps working when agents are down.
- **Legacy learnings stay in a labelled archive file** (`working`). Rejected:
  2,572 GitHub issues.
