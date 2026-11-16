# Proposal: rank external ideas by usefulness to Brian's projects

Source: Brian, 2026-11-16: "i should be thinking about usefulness to my proejcts not just score", then "i aprpove" to Decision 8A (build the project-profile model step, run it beside the score-only digest on the first run's posts, then show both).

## What changes

- An optional project profile (`projects.yaml`, outside the repository, so project descriptions stay private) lists each project with a one-line goal.
- With a profile, the command asks a light model, once per subreddit, which of that subreddit's new posts could help which project, with a one-line reason. It writes `digest-useful-*.md`, grouped by project. The score-only `digest-*.md` is still written beside it for comparison.
- Plain version first (core.md): one call per subreddit, the post titles and first 500 characters plus the profile, no extra stages. A stage is added only for a gap shown on real posts.
- Every call is traced through the shared LLM client (trace id per subreddit) and the run log records posts judged, posts kept and cost.
- Out of scope: the timer, reading linked pages, and making the model step the default before Brian has seen the side-by-side.

## Cost basis (worked out, not measured)

8 calls per run, about 8,000 input tokens each (25 posts at about 250 tokens plus a 2,000-token profile), so about 64,000 input tokens per run on a light model. First run measures the real figure with `llm-cost`.

## Plan size

Small under `plan-size`: undone by `git revert`, nothing outward, spend a few cents per run, no file another repository reads. One independent read before merge.
