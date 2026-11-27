You are grading one build of a 2D browser game against a fixed list of contract items. You do not know who built it.

- The game is in ./game. Serve it with: `python3 -m http.server $PORT --directory game` (PORT is given below), and open
  http://localhost:$PORT/index.html in a headless browser. Playwright for Node is available: run node scripts with
  `NODE_PATH=$NODE_PATH node your-script.mjs` (import { chromium } from 'playwright'). Write your scripts and
  screenshots under ./evidence/.
- The design document is game/docs/game-design.md. The items to grade are in ./items.json: requirements, rules,
  invariants and scenarios. Each scenario says what to set up and what to verify.
- Grade on running behaviour first: drive the game with keyboard and mouse input, take screenshots, and read what the
  page shows. Read the source code only for an item that play cannot reach in reasonable time (for example a value
  deep in a late floor), and say so in that item's evidence.
- For every item give: "pass" (works as the item states), "partial" (some of it works, or works with a visible error),
  or "fail" (missing, broken, or contradicts the item). A game that does not load fails every item.
- Evidence for each item: a screenshot path, a script and its output, or a file:line. One or two sentences.
- Be strict and even-handed. Do not give credit for code that exists but never takes effect in play.

Return the JSON object the output schema asks for, with one verdict for every item in items.json, in its order.
