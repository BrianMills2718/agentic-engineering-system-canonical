# The three commands that keep plan, code and wiki in step.
COG_FILES := $(shell grep -rl '\[\[\[cog' src tests 2>/dev/null)

scaffold:  ## create every file the plan declares (with a docstring hooked to the plan)
	python -m lockstep.scaffold

project:  ## write plan text into docstrings (cog), from .aes/target.yaml; an edited copy first becomes a draft plan change
	$(if $(COG_FILES),python -m lockstep.docstring_up,@true)
	$(if $(COG_FILES),cog -r -c $(COG_FILES),@echo 'project: no planned files yet')

wiki:  ## build the wiki from the plan, the evidence and the docstrings
	mkdocs build --strict -q

check:  ## fail if a docstring is out of date with the plan, the plan is invalid, or a file is unplanned
	$(if $(COG_FILES),cog --check -c $(COG_FILES),@true)
	aes target validate
	aes topology check
	mkdocs build --strict -q
	python -m pytest -p no:cacheprovider tests
