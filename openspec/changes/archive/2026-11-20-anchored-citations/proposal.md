Plan size: small
Independent read: 2026-11-20, pass (a fresh reviewer subagent; it found a wrong directive such as `#:~:selector=` skipped as a non-citation, now failing with tests, plus a test slug and two prior-art inaccuracies, all fixed; a symlink read that predates this change is left as is)

## Why

Brian, 2026-11-20: "start 1-2", after the agent traced Skipper's 14 cold-review runs to citations that point at moved text: a `path:line` citation passes while the file is long enough, whatever the line now holds, and Skipper's `AGENTS.md` carries a rule about line citations breaking twice (2026-11-17).

## What Changes

- A repository file named in the acceptance file (`representation.router_record`, `representation.variants`) may be cited as `path#:~:text=<percent-encoded text>` (WICG text-fragment syntax, optional `prefix-,` and `,-suffix`). It passes when the text is in the file exactly once, runs of whitespace counting as one space. Not found, found more than once and a malformed anchor each fail and name the citation.
- Plain `path` and `path:line` are unchanged.
- The same function and shared cases are in Company Planning's validator, which Skipper runs (`citation_anchor.py`, company-planning branch feat/anchored-citations-20261120). Company Planning's plugin is installed on its own, so the file is held in both repositories, each with a test over the same case file; a change to the cases must be made in both.

## Impact

- `src/lockstep/plan_check.py`, new `src/lockstep/citation_anchor.py`, `tests/lockstep/`.
- No repository's existing citations change meaning.
