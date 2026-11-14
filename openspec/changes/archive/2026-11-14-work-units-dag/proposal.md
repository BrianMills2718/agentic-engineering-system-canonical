# Plans carry a work-unit DAG

Source: Brian, 2026-11-14: "we should always have a dag as part of the plans so we can optimally parallelize and stay on track"; approved the recommendation ("i apporve your recs", same day): every plan unit declares `depends_on` and `touches`, and Lockstep checks them.

A plan's build order is a list today, so nothing says which units are independent. `docs/planning/work-units.json` records each unit with `depends_on` and `touches`; `lockstep plan units` checks it is a DAG and prints what is ready, the longest remaining chain and independent units that touch the same file. Status of a merged unit needs evidence. Repositories without the file are not failed yet (adopt-when-changed pace, `~/code2/AGENTS.md`); a missing file exits 2 from `lockstep plan units`.
