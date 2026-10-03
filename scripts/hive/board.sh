#!/usr/bin/env bash
# Talk to Brian's Paperclip board API (hive brain v1). The board refuses other
# hostnames, so the request runs inside the container over `ssh personal-vps`;
# the board key stays on the VPS and is never printed.
#
#   scripts/hive/board.sh GET  /api/companies/$HIVE_COMPANY/issues
#   scripts/hive/board.sh GET  /api/issues/<issue-id>/comments
#   scripts/hive/board.sh GET  "/api/companies/$HIVE_COMPANY/heartbeat-runs?agentId=<agent-id>&limit=5"
#   echo '{"body":"..."}' | scripts/hive/board.sh POST /api/issues/<issue-id>/comments
#
# Company (prefix BRI): da165590-b0b3-4bf9-bb7f-e455292df499. Agents:
# Coordinator 8964a584-ddfe-4fb1-b14f-c1503ae5ec23, Research and Code Review
# 4d008def-4e59-47c2-bccf-ec5313e12ce2, Brian Contact 4331dfbd-6a12-4965-b28a-d296c5aa9d3a.
# Brian's user id: Fr6jPHXrgB7tlyFcDMdJEiKNmBk2vjAl. Issue ids: the "id" field of
# the issues list (BRI-13 is its "identifier"). Exit status is curl's (22 = HTTP error).
#
# HIVE_BOARD_LOCAL=1 runs the same request on this machine instead of over ssh:
# use it ON the VPS (as root, which can read board.env), e.g. the hive-dashboard
# timer (personal-vps apps/hive-dashboard).
set -euo pipefail
method=${1:?usage: board.sh GET|POST|PATCH|PUT <api-path>}; path=${2:?api path}
body=""
[ "$method" != GET ] && body=$(base64 -w0)
if [ "${HIVE_BOARD_LOCAL:-}" = 1 ]; then run=(bash -s); else
  run=(ssh -o BatchMode=yes -o ConnectTimeout=15 personal-vps "sudo -n bash -s"); fi
"${run[@]}" <<REMOTE
set -euo pipefail
set -a; . /root/.paperclip-cli/board.env; set +a
printf '%s' "$body" | base64 -d | K="\$PAPERCLIP_API_KEY" docker exec -i -e K paperclip sh -c \
  'curl -sS -f -X $method -H "Authorization: Bearer \$K" -H "Content-Type: application/json" \
   \$( [ "$method" = GET ] || echo --data-binary @- ) "http://127.0.0.1:3100$path"'
REMOTE
