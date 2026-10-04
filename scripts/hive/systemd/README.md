# Hive controls on Brian's PC (systemd user units)

`hive-controls.timer` runs `hive-controls.service` daily. The service checks
every control (`scripts/hive/controls.py`) and pushes the result to the hosted
dashboard (`scripts/hive/push_controls.sh`).

The service runs from its own clone of AES `main` at `~/.hive-brain/aes`. It
fetches and resets that clone before every run. It never runs from the shared
`~/code/agentic-engineering-system-canonical` checkout, because other sessions
switch that one to their own branches.

Install, or reinstall after changing these files:

```bash
git clone --depth 1 https://github.com/BrianMills2718/agentic-engineering-system-canonical ~/.hive-brain/aes
cp scripts/hive/systemd/hive-controls.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now hive-controls.timer
systemctl --user start hive-controls.service   # one run now; Result=success, ExecMainStatus 0 or 1 (1 = a finding)
```
