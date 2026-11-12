"""mkdocs-gen-files script: write every wiki page from the plan at build time."""

from pathlib import Path

import mkdocs_gen_files

from lockstep.wiki import pages

for name, text in pages(Path.cwd(), "greeter").items():
    with mkdocs_gen_files.open(name, "w") as fh:
        fh.write(text)
