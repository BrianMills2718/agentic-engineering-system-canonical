# Proposal: the digest also judges usefulness to Brian's interests

Plan size: small
Independent read: 2026-11-17, pass (a fresh read of this page against the code diff; no changes needed)

## Goal

Brian, 2026-11-16: the digest has two jobs, "things that are generally interesting and useful to me across the spectrum of my life"
and "an automated input to aes"; 2026-11-17: "i approve both recs" (build the interests side, fed from where his information already lives).
The judge today sees only project goals, so it cannot call a post useful because it speaks to something Brian cares about.

## Change

- The private profile may carry an optional `interests:` list (name and one-line goal, same shape as a project).
- The judge prompt lists interests after projects and says a post is also useful when it concretely serves a listed interest.
  A useful post names the best-fitting projects or interests, at most two in all.
- The useful digest prints `Projects:` and `Interests:` lines separately.
- The interest lines are copied from the one-line column of the personal wiki's interest index (the wiki owns them); nothing sensitive is put in the profile.

## Not in this change

No new storage system, no reading of the wiki by the command, no change to ranking or to the subreddit list.

## Undo

`git revert` of the merge; a profile without `interests:` behaves as before.

## Cost

Model spend: a few hundred extra prompt tokens per judge call on the subscription route ($0 marginal; guess, not measured).
