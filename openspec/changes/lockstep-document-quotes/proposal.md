## Why

Brian, 2026-10-22 (code2-workspace decision 0006): "this doc string linkage system where the normative and docs tring stuff and gaps and planns would stay algined over time". Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then that normative docuemtnation gets updated and then the gaps relevant to that normative docuemntation need to be replanned".

Lockstep keeps code in line with a requirement (the generated text in each implementing docstring, `lockstep check project --check`) and, since the changed-requirement check, lists the code and tests of a requirement whose text changed. It reads no document. In the 2026-11-17 test ([code2-workspace issue 842](https://github.com/BrianMills2718/code2-workspace/issues/842)) a requirement changed from "10 of the 20 cores" to "8 of the 20" and seven hand-typed copies of the old number in documents (agent rules among them) stayed as they were, with every check exiting 0.

He approved building the missing steps on 2026-11-17 ("i approve", Decision 6 option A). This change is the document step.

## What Changes

- A document can mark a passage as a quote of a requirement: `<!-- lockstep quote: <requirement id> -->the passage<!-- /lockstep quote -->`. The markers are HTML comments, so they do not show on a rendered page and cost one line of text in a file an agent reads raw.
- `lockstep check trace` reads every marked quote in tracked Markdown outside `openspec/` and fails with `stale-quote` when the passage does not appear word for word in the text of that requirement or of one of its scenarios (in the specs or in an active change's delta), with `unknown` when no spec defines the ID, and with `unclosed-quote` when the end marker is missing.
- `lockstep check changed` lists, under each requirement it lists, every document that quotes it, as `<path>:<line>` labelled `current` or `stale`.

The passage is the author's own words in the author's own sentence; the check verifies it, it does not write it. A passage that is not marked is not checked: finding unmarked copies of a requirement's wording needs a reader (a person or a model), not this check. Nothing is stored; the comparison is made on every run.

## Impact

- `src/lockstep/checks/`: new `quotes.py` (find and compare marked quotes); `trace.py` and `changed.py` call it; `cli.py` prints the new findings.
- A repository with no marked quote sees no difference. A repository gets the check by marking a passage; `trace` already runs in every repository's commit check.
- The trace count line gains nothing new: quote findings count in `findings=<n>`.

Closes: lockstep-checks/trace-a-marked-quote-matches-its-requirement,
    lockstep-checks/changed-documents-that-quote-a-listed-requirement-are-listed-with-it
