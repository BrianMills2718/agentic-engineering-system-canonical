# Feedback collector on Brian's PC (systemd user units)

`feedback-collector.timer` runs `feedback-collector.service` nightly at 03:30.
The service runs `scripts/learning_loop/collect_feedback.py --file` from the
same refreshed clone of AES `main` as `hive-controls` (`~/.hive-brain/aes`),
with `llm_client` from `~/code/llm_client` through uv's shared cache. Output:
`~/projects/data/feedback-collector/` (`items-<date>.jsonl`, `runs.jsonl`,
`state.sqlite`). Never commit anything from that folder: it holds private
transcript quotes.

Install, or reinstall after changing these files:

```bash
cp scripts/learning_loop/systemd/feedback-collector.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now feedback-collector.timer
systemctl --user start feedback-collector.service   # one run now; then: journalctl --user -u feedback-collector -n 40
```

Exit 1 (some LLM, Jev or filing calls failed) and 2 (crash) fail the unit and
open a keyed agent concern through `project-meta/scripts/notify_operator.py`.
