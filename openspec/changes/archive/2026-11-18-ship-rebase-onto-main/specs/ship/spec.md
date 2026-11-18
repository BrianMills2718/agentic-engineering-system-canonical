## ADDED Requirements

### Requirement: Rebase a branch that is behind the default branch before checking it

After refusing a dirty tree and before the gates and the check, `scripts/ship.py` SHALL fetch `origin` and, when the default branch (`origin/HEAD`, else `origin/main`) is not an ancestor of HEAD and the branch is not on the remote, rebase the branch onto the default branch, then check and merge the rebased commit. A repository's `.gitattributes` merge drivers apply to this rebase, so a file marked `merge=union` keeps the lines both sides added. When the rebase stops on a conflict it SHALL abort the rebase, leave the branch at its earlier commit, refuse the merge with nothing pushed, and name the conflicting paths. When the branch is already on the remote, or the fetch fails, it SHALL print and log one line saying it did not rebase and why, and go on.

Source: inferred by agent (code2-workspace issue 472, 2026-11-17): two sessions adding a top entry to the same log file conflicted on GitHub's merge, which does not apply `.gitattributes` merge drivers; a local rebase does. A pushed branch is not rebased because that would need a force-push.

#### Scenario: A branch behind the default branch is rebased and merged

- **GIVEN** a branch whose default branch gained a commit touching another file after the branch was cut
- **WHEN** ship runs
- **THEN** it rebases the branch onto the default branch, merges the rebased commit, and exits 0

#### Scenario: Two top entries in a union log both survive

- **GIVEN** a log file marked `merge=union` in `.gitattributes`, and the default branch and the branch each added a different entry at its top
- **WHEN** ship runs
- **THEN** it merges, and the merged log holds both entries

#### Scenario: A conflicting rebase pushes nothing

- **GIVEN** a branch and its default branch that changed the same line of a file with no merge driver
- **WHEN** ship runs
- **THEN** it exits 1, names the file, the branch is at its earlier commit with no rebase in progress, and nothing is pushed

#### Scenario: A branch already on the remote is not rebased

- **GIVEN** a branch that is behind the default branch and was pushed earlier
- **WHEN** ship runs
- **THEN** it says it did not rebase because the branch is on the remote, and merges as before
