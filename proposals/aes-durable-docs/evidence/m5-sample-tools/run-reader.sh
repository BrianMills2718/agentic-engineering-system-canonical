#!/bin/bash
# usage: run-reader.sh <checkout> <question> <out.jsonl>
cd "$1" && start=$(date +%s) && claude -p --model haiku --max-turns 40 --output-format stream-json --verbose \
  --disallowedTools Bash Grep Glob Edit Write NotebookEdit WebFetch WebSearch Agent Task < "$2" > "$3" 2> "$3.stderr"
echo "exit=$? seconds=$(( $(date +%s)-start ))" >> "$3.stderr"
