# Hive brain user timers (WSL)

`hive-controls.timer` runs `scripts/hive/controls.py` every day at 09:00 local
time (or at the next start, if WSL was off then). Each run appends to
`~/.hive-brain/controls.jsonl`; `scripts/hive/readout.py` shows how many days
had only clean runs (v1 condition 4: a week of exit 0). After each run,
`push_controls.sh` copies `~/.hive-brain/controls-latest.json` to
`personal-vps:/srv/apps/hive-dashboard/data/wsl-controls.json` for the hosted
dashboard; the dashboard marks that report STALE after 26 hours, so a stopped
timer or a failed copy shows on the page instead of looking fine.

Install or update:

    cp scripts/hive/systemd/hive-controls.* ~/.config/systemd/user/
    systemctl --user daemon-reload && systemctl --user enable --now hive-controls.timer

Check: `systemctl --user list-timers hive-controls.timer`;
last run: `journalctl --user -u hive-controls.service -n 20`.
