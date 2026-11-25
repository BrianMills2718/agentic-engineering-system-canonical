## 1. Tests first

- [x] 1.1 Move the two AES scripts' tests and the workspace mutation tests under `tests/lockstep/checks/`; new tests
  for off-by-default, the llm_client hint, per-repository mutation settings, and init writing the three off

## 2. Build

- [x] 2.1 `config.py` (DEFAULT_OFF, `on` as block, `mutation:` keys) and `cli.py` (three runners)
- [x] 2.2 Move `maintainability.py` and `helper_reuse.py` (local git helper, prompts as package data); port `mutation.py`
- [x] 2.3 `init_repo.py` and `template/Makefile`; AES `Makefile`, `pyproject.toml`, `lockstep.yaml`
- [x] 2.4 Layout rows, regenerated copies, `.project-brain/now.md`
