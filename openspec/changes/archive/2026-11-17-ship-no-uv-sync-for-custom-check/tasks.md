## 1. Code

- [x] 1.1 `prepare_environment` takes the check; the uv sync is Makefile-check only
- [x] 1.2 A failed step removes the folder it created

## 2. Tests

- [x] 2.1 Existing environment tests use a Makefile check
- [x] 2.2 New tests: custom check skips sync, failed sync leaves no folder, `is_makefile_check`

## 3. Spec

- [x] 3.1 Archive with `openspec archive ship-no-uv-sync-for-custom-check --yes`
