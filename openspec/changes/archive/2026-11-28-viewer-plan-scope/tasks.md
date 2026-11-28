## 1. Build

- [x] 1.1 Failing test: a docs/architecture write is a plan write; generated/files.md, tests/x.py, pyproject.toml and wiki/index.md are not
- [x] 1.2 `_is_plan` counts authored documents outside the wiki, generated, test and config folders
- [x] 1.3 `plan_file` on each tool event; the page's plan-read mark uses it
- [x] 1.4 After review: a later document mention or whole rewrite never makes a write `row added later`; excluded folders at any depth, dependency and licence names, case-insensitive endings; `openspec/` counts documents only; a spec read pinned as a plan and requirement read
