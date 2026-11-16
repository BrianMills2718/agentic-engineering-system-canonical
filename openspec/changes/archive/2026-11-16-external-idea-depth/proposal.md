# Proposal: the usefulness judge decides how much to read

Source: Brian, 2026-11-16: "a question or demo could both be useful depending on what they are. for the question the value would presumably come from the answers. yes i want you to use the subscription. i approve 11a. but the agent should be able to react dynamically i would think on how much to explore". Also: three posts the title-only judge rejected "should all be in the list".

## What changes

The judge is a Claude model run through the subscription route (`claude-code/sonnet`, no per-call dollar cost). Round 1 sees each post's title and opening text and decides useful, not useful, or need more (comments, linked pages, both). Round 2: this code reads exactly what was asked (the model has no tools, so a hostile page cannot steer anything) and the model gives a final verdict. The digest says what each verdict was judged from.

## Measured on the first full run (136 posts, 110-entry profile)

57 useful (the title-only judge gave 20). It asked for more on 38 posts. The three posts Brian named are all in. Run time about 22 minutes (7 subreddits, measured from the run log); model dollar cost 0 on the subscription route. Small plan under `plan-size`: undone by `git revert`, nothing outward.
