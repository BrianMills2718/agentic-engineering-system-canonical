- [x] Write the failing tests: a rendered copy has the two tracked hook scripts with no machine-bound text; a copy
      committed after a move and from a worktree runs its lefthook jobs
- [x] Add `template/.githooks/pre-commit` and `template/.githooks/pre-push`
- [x] Set `core.hooksPath .githooks` in `copier.yml` and drop `lefthook install --force`
