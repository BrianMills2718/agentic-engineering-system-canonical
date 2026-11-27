#!/bin/bash
# Grade one blind copy with Codex (a different model family from the Sonnet builders), per contract item.
# Usage: grade.sh <blind id> [game]. Writes $BENCH/grade/<id>/verdicts.json and trace.jsonl, then scores it.
id=$1; game=${2:-abyssal_chain}; BENCH=${BENCH:-/home/brian/projects/data/aes-gamebench}
here=$(cd "$(dirname "$0")" && pwd); g=$BENCH/grade/$id
NODE_PATH=${PLAYWRIGHT_NODE_PATH:-/home/brian/code2/representation-router/node_modules}
[[ -d $g/game ]] || { echo "no blind copy at $g"; exit 1; }
[[ -e $g/verdicts.json ]] && { echo "$g already graded; refusing to overwrite"; exit 1; }
/home/brian/.local/bin/storage-policy --need-gib 1 gate || exit 75
python3 "$here/items.py" "$BENCH/games/$game" "$g/items.json" || exit 1
mkdir -p "$g/evidence"
port=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1])')
prompt="$(cat "$here/grader-prompt.md")

PORT=$port
NODE_PATH=$NODE_PATH"
timeout 7200 codex exec --json --output-schema "$here/verdict-schema.json" -o "$g/verdicts.json" \
  --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -C "$g" "$prompt" > "$g/trace.jsonl" 2> "$g/grade.err"
rc=$?; echo "codex exit $rc"
[[ $rc -eq 0 && -s $g/verdicts.json ]] || { echo "grading failed: $g/grade.err"; exit 1; }
python3 "$here/score.py" "$g"
