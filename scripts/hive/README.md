# scripts/hive: the hive brain's glue

Thin scripts around off-the-shelf tools (Paperclip, the Jev gate, CC Safety
Net, systemd). The plan they serve is `proposals/hive-brain-v1/ROADMAP.md`.
Each script's header says more.

| File | What it does | Run |
|---|---|---|
| `board.sh` | one request to the Paperclip board API over `ssh personal-vps` (company, agent and task ids in its header) | `scripts/hive/board.sh GET /api/companies/$C/issues` |
| `decisions.py` | what is waiting on Brian: agents not working, then tasks assigned to him or blocked; exit 1 while an agent is broken | `python3 scripts/hive/decisions.py` |
| `controls.py` | silence check: last activity of each control against its normal gap (Jev gate, Safety Net, Paperclip, backups, learning loop, project brains, settings, Telegram relay); appends to `~/.hive-brain/controls.jsonl`; exit 1 on anything silent | `python3 scripts/hive/controls.py` |
| `readout.py` | weekly readout: tasks, jobs with cost and hours, runs and failures, gate decisions, learning-loop items, clean days | `python3 scripts/hive/readout.py --days 7` |
| `brain_fresh.py` | is a repo's `.project-brain/` older than the work since it? exit 1 if stale, 2 if there is no brain | `python3 scripts/hive/brain_fresh.py <repo> [--fetch]` |
| `settings.json` and `settings_check.py` | how the hive should be configured (agents, heartbeats, caps, gate mode, timers) and a check of the live system against it | `python3 scripts/hive/settings_check.py` |
| `conditions.json` | progress on the five v1 conditions, updated by hand with evidence; the dashboard reads it (edit it as JSON, not by text matching) | — |
| `dashboard.py` | builds Brian's five-screen page from live data; `--vps` builds it on the server, where it is hosted at https://hive.brianmills.dev | `python3 scripts/hive/dashboard.py --out page.html` |
| `push_controls.sh` | copies this machine's latest controls result to the hosted dashboard, which cannot see WSL-only controls itself | runs after `controls.py` from the timer |
| `dashboard-use-case.json`, `DASHBOARD_FEEDBACK.md` | the dashboard's Representation Router use case, and the living log of Brian's critiques | read |
| `systemd/` | the WSL user timer that runs `controls.py` daily and then `push_controls.sh` | see its README |
