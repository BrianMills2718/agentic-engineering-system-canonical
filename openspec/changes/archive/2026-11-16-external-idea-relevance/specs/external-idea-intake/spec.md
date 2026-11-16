# external-idea-intake Specification

## ADDED Requirements

### Requirement: A project profile makes the digest rank by usefulness to Brian's projects

When a project profile is given, the command SHALL ask a light model, once per subreddit, which of that subreddit's new posts could help which profiled project, and SHALL write a digest of only the posts judged useful, grouped by project with the model's one-line reason. The score-only digest SHALL still be written. A post named by the model that was not in the listing SHALL be ignored. A model failure SHALL be logged for that subreddit, the run SHALL exit non-zero, and that subreddit's posts SHALL NOT be marked seen.

#### Scenario: useful-digest-groups-by-project

- **WHEN** the model marks one of three new posts useful to project "aes" and names a post id that was never fetched
- **THEN** the useful digest lists that one post under "aes" with its reason, the unknown id is ignored, and the score-only digest lists all three

#### Scenario: judge-failure-keeps-posts-unseen

- **WHEN** the model call raises for one subreddit
- **THEN** the log records the failure, the exit status is non-zero, and a later run offers those posts again
