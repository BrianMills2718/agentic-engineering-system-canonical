---
type: Topic
title: Subreddits and sources to check
description: The subreddits behind the external ideas reviewed so far, what each gave, and how to check them again
status: current
last_checked: 2026-11-16
---

# Subreddits and sources to check

Source: Brian, 2026-11-16, asked to keep track of every subreddit looked at, "because i want to start
regularly checking in on these for ideas". This page is that list. The reviews it feeds are in
[External ideas](external-ideas.md).

## Looked at so far

"Yield" is the reviewer's judgment of what the subreddit gave AES from the posts read, not a
measure of the whole subreddit. Every count is of posts read, so one post can mislead.

| Subreddit | Posts read | What it gave | Yield | Last checked |
| --- | --- | --- | --- | --- |
| r/claudeskills | Bansat blueprint skill | A launch-gate and N/A-with-a-reason pattern; the author answers comments in detail | Medium | 2026-11-16 |
| r/ClaudeAI | Internal-rules "leak"; modular Claude Code setup | Mostly self-promotion and unverified claims | Low | 2026-11-16 |
| r/PostAI | Stage Show video | A link to a real, public skill with a check on recorded output | Medium | 2026-11-16 |
| r/OntologyEngineering | Epistemic Lattice Tethering | One author's prompt framework; its own numbers contradict each other | Low | 2026-11-16 |
| r/mcp | FastMCP code mode; CLIHub | Names-first tool discovery; claims modeled, not measured | Medium | 2026-11-16 |
| r/SATNA_PROJECT | Two curated tool lists | Lists of repositories; read in the third batch | See [External ideas](external-ideas.md) | 2026-11-16 |
| r/BestGitHubRepos | Claude How To guide | A guide repository; read in the third batch | See [External ideas](external-ideas.md) | 2026-11-16 |
| r/AI_Agents | A question about AI architecture diagrams | No tool named that AES lacks; commenters use Mermaid, draw.io, PlantUML | Low | 2026-11-16 |

## How to check again

1. Read a subreddit's recent posts through the social-media server's `reddit_subreddit_posts`, or read
   a post list the reader supplies, through the Reddit API with the existing credentials (read-only).
2. Capture each post with all comments and every relevant link: Reddit refuses plain fetches, so use
   the server's Reddit code. For repositories, record URL, commit and file hashes in a `source.json`;
   do not copy the files.
3. Add the subreddit and the posts read to the table above, with the date.

How often to check is not decided yet.
