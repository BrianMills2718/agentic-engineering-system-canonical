# 2026-10-07 filing-gate evidence

Scripts behind the feedback collector's filing gates (AES #181, #216, #220). Each reads learnings
entries by id from project-meta (a private repository) at run time; the scripts themselves contain no
transcript text, only entry ids and hand labels.

| Script | What it measured | Result |
| --- | --- | --- |
| `eval_reusable.py` | Jev's "reusable beyond this task?" answer on the first night's 33 filed entries, hand-labelled | best 9/14 = 64% at p >= 0.8, so source (closeout Learnings: 8/8 reusable vs 7/25 for LLM-extracted) became the main gate |
| `retriage.py` | rescored the 2026-10-06 backlog with the collector's own triage before gated filing | task-specific job-search advice scored 0.21-0.41 and was kept out |
| `independent_grade.py` | blind grade of the 10 entries filed through both gates by gemini-3.1-pro-preview | 8/10 pass; the 2 misses were reworded repeats |
| `paraphrase_probe.py` | the light model's "same lesson as an earlier entry?" check on those 10 | 9/9 comparisons correct (both repeats caught, no false flags) |

They import `llm_client` and read `~/code/project-meta` and `~/projects/data/feedback-collector`
as written on the day; run with `uv run --no-project --with-editable ~/code/llm_client --with pydantic python <script>`.
