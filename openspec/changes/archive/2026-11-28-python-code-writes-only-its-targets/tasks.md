## 1. Python code writes only its targets

- [x] 1.1 Test first: the Sonnet run's script shape is not refused; a script that writes a planned file through a variable still is; an unresolvable target keeps the old rule
- [x] 1.2 Read Python code with `ast` and resolve its write targets
- [x] 1.3 Replay the refused Sonnet command through the hook
- [x] 1.4 Review fixes: narrowing only for code the hook can vouch for; the 70 review probes as tests, 0 worse than the old rule
