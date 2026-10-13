# code2 workspace

`~/code2` is the fresh workspace that repositories join by moving in. This file is linked as
`~/code2/AGENTS.md`; its source of truth is `proposals/code2-ecosystem/workspace/AGENTS.md` in
agentic-engineering-system-canonical (AES canonical). Change it there, through a commit, never by
editing the link target in place.

## Safety rules (Brian's, always on)

- Never shut down or restart WSL (`wsl --shutdown`, `--terminate`, or a script that does either)
  without asking Brian and getting a yes for that restart. It kills every agent running in Linux.
- Never send anything outward (email, Slack, Telegram, posts, public pages, package releases)
  without Brian approving the exact content in the same conversation.
- Never delete data or history (files, branches, worktrees, databases, git history) without asking
  first. Losing data or development history is the worst class of problem here.
- Never echo, commit, log or send a secret. Credentials live in `~/.secrets/api_keys.env`.
- Never restart VS Code windows without warning: a reload stops every agent in VS Code.

## Everything else

AES canonical owns the rules, enforcement and procedures for this workspace: start at its
`wiki/index.md` (`~/code2/agentic-engineering-system-canonical/wiki/index.md` once it has moved in,
`~/code/agentic-engineering-system-canonical/wiki/index.md` before). Enforcement is configured
centrally there and turned on one repository at a time. Each repository's own `AGENTS.md` governs
work inside it.

Until AES canonical's workspace rules cover a topic, the older workspace rules in `~/code/AGENTS.md`
still describe how Brian wants work done (planning, verification, merging, closeout fields); follow
them unless AES canonical says otherwise.
