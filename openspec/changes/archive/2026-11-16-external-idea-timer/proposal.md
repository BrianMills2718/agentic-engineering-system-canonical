# Proposal: run the external idea digest every day

Source: Brian, 2026-11-16: "i would think it should run every day". Earlier condition (Brian, 2026-11-16, "i approve" to Decision 7B): add the timer after a digest has been seen and judged useful; Brian asked for the daily schedule after seeing the digests, so it is installed.

Daily at 04:15 (after the 03:30 collector), `Persistent=true`. The judge uses the Claude subscription route, so each run uses some weekly Claude usage; the first runs record seconds per subreddit in the run log, and usage is not measured yet. Small plan under `plan-size`: undone by `git revert` and `systemctl --user disable --now external-ideas.timer`.
