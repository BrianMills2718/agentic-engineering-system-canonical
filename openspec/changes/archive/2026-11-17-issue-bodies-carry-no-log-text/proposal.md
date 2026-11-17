## Why

A failed timer job's concern issue carried the unit's last 30 journal lines. Two of them are in this public repository
(#944, #945): they show the laptop's host name, process ids and every line the job printed, and a job's output can name
home paths, Windows user names or addresses. The full log is on the machine that ran the job; the issue only needs to say
which job failed, the one line that says why, and where the full log is. Separately, a unit whose repository remote uses
the `github.com-personal` SSH host alias was not matched to its repository, so `brent-fdot-feed.service` (repository
`brent-chatgpt`, private) was filed in the fallback repository, which was this public one at the time.

## What Changes

- `failed_unit_watch.py`: the failed-unit and Healthchecks.io bodies carry one line, the newest line the job itself printed
  (the journal entry whose `SYSLOG_IDENTIFIER` is not `systemd`; systemd's own newest line when the job printed nothing),
  without host name or process id, and the command that shows the full log on the machine. No journal block.
- `failed_unit_watch.py`: `repo_from_remote` accepts the `github.com-<alias>` SSH host form as well as `github-<alias>`.
- `project_graph_refresh.py`: the concern body carries the first line of each problem and the day's log path, not the
  step's output tail.
- New `scripts/public_text.py`: `redact` (home folder to `~`, `/home/<name>` and `/Users/<name>` to `~`,
  `C:\Users\<name>` to `C:\Users\<you>`, email addresses to `<email>`, IPv4 addresses to `<ip>`) and `first_line`.
  `concern_issue.py` applies `redact` to every title, body and close evidence it files, so every caller is covered.

Source: Brian, 2026-11-17 (task to this session): "Failed AES scripts open public issues (failed_unit_watch) that still carry
log text ... make AES's own public issue bodies carry only the first error line and a pointer to the private log path ...
and redact home paths/addresses." The choice of the line (by journal field, not by matching words) is inferred by agent:
the workspace rule forbids reading meaning from prose with regular expressions.
