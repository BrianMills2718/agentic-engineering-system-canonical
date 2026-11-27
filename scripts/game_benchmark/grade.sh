#!/bin/bash
# Grade one blind copy with Codex (a different model family from the Sonnet builders), per contract item.
# Usage: grade.sh <blind id> or grade.sh --check-browser. Writes $BENCH/grade/<id>/verdicts.json and trace.jsonl, then scores it.
BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}
here=$(cd "$(dirname "$0")" && pwd) || exit 1
export NODE_PATH=${PLAYWRIGHT_NODE_PATH:-/home/brian/code2/representation-router/node_modules}
export PLAYWRIGHT_CHROMIUM_EXECUTABLE
_check_browser() {
  node - <<'BROWSER'
const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined});
  try {
    const page = await browser.newPage();
    await page.setContent('<button>test</button>');
    await page.locator('button').evaluate(button => {
      button.onclick = () => { button.textContent = 'ready'; };
    });
    await page.getByRole('button', {name: 'test'}).click();
    if (await page.getByRole('button').textContent() !== 'ready') throw new Error('browser input did not take effect');
    if (!(await page.screenshot()).length) throw new Error('browser screenshot is empty');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
BROWSER
}
if [[ ${1:-} == --check-browser ]]; then
  _check_browser
  exit $?
fi
id=$1; g=$BENCH/grade/$id
[[ -d $g/game ]] || { echo "no blind copy at $g"; exit 1; }
if [[ -e $g/verdicts.json ]]; then
  [[ -f $g/grade.exit && $(<"$g/grade.exit") == 0 ]] || {
    echo "Existing verdicts have no successful grader exit; inspect the attempt before reuse"; exit 2;
  }
  python3 "$here/score.py" "$g"
  exit $?
fi
[[ -e $g/trace.jsonl ]] && { echo "A grading trace already exists; inspect it before another paid call"; exit 2; }
[[ -n ${GRADE_MODEL:-} ]] || { echo "Set GRADE_MODEL to the frozen Codex model"; exit 2; }
/home/brian/.local/bin/storage-policy --need-gib 1 gate || exit 75
[[ -s $BENCH/frozen-items.json ]] || { echo "Missing frozen item list; start with run_all.sh"; exit 2; }
cp "$BENCH/frozen-items.json" "$g/items.json" || exit 1
mkdir -p "$g/evidence" || exit 1
_check_browser || exit 1
port=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1])') || exit 1
prompt="$(cat "$here/grader-prompt.txt")

PORT=$port
NODE_PATH=$NODE_PATH
PLAYWRIGHT_CHROMIUM_EXECUTABLE=${PLAYWRIGHT_CHROMIUM_EXECUTABLE:-}"
timeout 7200 codex exec --model "$GRADE_MODEL" --json --output-schema "$here/verdict-schema.json" -o "$g/verdicts.json" \
  --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -C "$g" "$prompt" > "$g/trace.jsonl" 2> "$g/grade.err"
rc=$?
printf '%s\n' "$rc" > "$g/grade.exit" || exit 1
echo "codex exit $rc"
[[ $rc -eq 0 && -s $g/verdicts.json ]] || { echo "grading failed: $g/grade.err"; exit 1; }
python3 "$here/score.py" "$g"
