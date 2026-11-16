# external-idea-intake Specification

## Purpose

Let Brian name subreddits to watch in AES configuration and get a ranked digest of new posts for review, as an input to the feedback loop that reads outside ideas.

Source: Brian, 2026-11-16, "i assume this should be configurable within aes. i.e. this is an auotmated aspect of the aes feedback loop and you should be able to put the subreddits to examine as part of that in th econfigruation", and "i approve" to Decision 7 option B (config and command now, run on request, timer only after one digest is judged useful).

## Requirements

### Requirement: The watch list is configuration and an invalid one is refused

The command SHALL read the subreddits to watch from `scripts/learning_loop/external_sources.yaml`. Each entry SHALL have a unique name, a non-empty reason, a listing (`top` or `new`), a window (`day`, `week`, `month` or `year`), a post limit from 1 to 100 and a minimum score of 0 or more. An invalid file SHALL make the command exit non-zero before any fetch.

#### Scenario: invalid-config-refused

- **WHEN** the configuration has an entry with an unknown listing, a missing reason or a duplicate name
- **THEN** the command exits non-zero, names the entry, and makes no fetch

### Requirement: The digest ranks new posts by score and age only

For each configured subreddit the command SHALL fetch one listing, drop posts already seen in an earlier run, drop posts below the minimum score or older than the window, and write a digest ranked by score and then age. It SHALL NOT judge relevance.

#### Scenario: digest-filters-and-ranks

- **WHEN** a listing holds a seen post, a low-score post, an old post and two eligible posts
- **THEN** the digest lists only the two eligible posts, higher score first, and a second run with the same listing lists none

### Requirement: Every run is traced and a repeated failure is reported as down

Each run SHALL append one record per step to the day's run log (config, each listing call with count or error, filter counts, digest path). A listing call that fails twice with the same error SHALL be reported as down, the other subreddits SHALL still be fetched, and the run SHALL exit non-zero.

#### Scenario: repeated-failure-is-down

- **WHEN** one subreddit's fetch raises the same error twice
- **THEN** the log records it as down, the other subreddits appear in the digest, and the exit status is non-zero

### Requirement: Output stays outside the repository and the register is never written

Fetched posts, the digest, the seen list and the run log SHALL be written under an output folder outside the repository. The command SHALL NOT write to any learnings register.

#### Scenario: output-outside-repo

- **WHEN** the command runs with an output folder
- **THEN** every file it wrote is under that folder

### Requirement: A project profile makes the digest rank by usefulness to Brian's projects

When a project profile is given, the command SHALL ask a light model, once per subreddit, which of that subreddit's new posts could help which profiled project, and SHALL write a digest of only the posts judged useful, grouped by project with the model's one-line reason. The score-only digest SHALL still be written. A post named by the model that was not in the listing SHALL be ignored. A model failure SHALL be logged for that subreddit, the run SHALL exit non-zero, and that subreddit's posts SHALL NOT be marked seen.

#### Scenario: useful-digest-groups-by-project

- **WHEN** the model marks one of three new posts useful to project "aes" and names a post id that was never fetched
- **THEN** the useful digest lists that one post under "aes" with its reason, the unknown id is ignored, and the score-only digest lists all three

#### Scenario: judge-failure-keeps-posts-unseen

- **WHEN** the model call raises for one subreddit
- **THEN** the log records the failure, the exit status is non-zero, and a later run offers those posts again

### Requirement: Posts already assessed into raw sources are never offered again

The command SHALL treat every Reddit post whose capture folder exists in `raw/sources/` (named `<date>-reddit-<id>-<slug>`) as already seen.

#### Scenario: already-assessed-dropped

- **WHEN** a listing holds a post whose id matches a `raw/sources` capture folder
- **THEN** it appears in neither digest

### Requirement: The usefulness judge reads more only when it asks to, and only what it asks for

For each post the judge SHALL return useful, not useful or need more (comments, linked pages or both). For need-more posts the command SHALL read exactly the requested material and the judge SHALL return a final verdict from it. The model SHALL be run with no tools and every post, comment and page text SHALL be marked to it as untrusted. The reader SHALL refuse non-http(s) links and hosts that resolve to non-public addresses, and SHALL re-check each redirect. The useful digest SHALL list each post once with its projects. Each useful post SHALL record what it was judged from.

#### Scenario: depth-judge-reads-more-when-asked

- **WHEN** the model asks for the comments of one post and marks another useful from its title
- **THEN** only that post's comments are read, the final verdict for it uses them, and the other post is recorded as judged from its title
