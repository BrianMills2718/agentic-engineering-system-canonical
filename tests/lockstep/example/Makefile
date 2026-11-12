# The three commands that keep plan, code and wiki in step.
COG_FILES := $(shell grep -rl '\[\[\[cog' src)

project:  ## write plan text into docstrings (cog), from .aes/target.yaml; an edited copy first becomes a draft plan change
	python -m lockstep.docstring_up
	cog -r -c $(COG_FILES)

wiki:  ## build the wiki from the plan, the evidence and the docstrings
	mkdocs build --strict -q

check:  ## fail if a docstring is out of date with the plan, the plan is invalid, or a file is unplanned
	cog --check -c $(COG_FILES)
	aes target validate
	aes topology check
	mkdocs build --strict -q
	python -m pytest -p no:cacheprovider tests
