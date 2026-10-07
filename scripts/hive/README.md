# scripts/hive

The hive (Paperclip agents, dashboard, controls, readout) moved to
[BrianMills2718/personal-vps](https://github.com/BrianMills2718/personal-vps) on 2026-10-07:
scripts in `hive/`, plans in `proposals/hive-brain-v1/` and `proposals/hive-hardening/`.

Only `brain_fresh.py` stays here: it checks whether a repository's `.project-brain/` is current,
and other repositories' `AGENTS.md` call it by this path
(`python3 ~/code/agentic-engineering-system-canonical/scripts/hive/brain_fresh.py .`).
