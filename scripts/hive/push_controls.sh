#!/usr/bin/env bash
# Copy this machine's latest controls result up to the hosted hive dashboard
# (personal-vps apps/hive-dashboard), which cannot see WSL-only controls
# (Jev gate, CC Safety Net, project brains, hive settings) itself.
#
#   scripts/hive/push_controls.sh [<controls-latest.json>]
#
# Run after controls.py (hive-controls.service ExecStartPost). The VPS copy is
# replaced atomically, so the dashboard never reads half a file; the dashboard
# shows the report's own "at" time and marks it STALE when it is old.
# Exit status: 0 pushed, 1 nothing to push, 2 the copy failed.
set -euo pipefail
src=${1:-$HOME/.hive-brain/controls-latest.json}
dest_dir=${HIVE_DASHBOARD_DATA:-/srv/apps/hive-dashboard/data}
if [ ! -s "$src" ]; then echo "push_controls: nothing to push ($src missing or empty)" >&2; exit 1; fi
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["at"] and isinstance(d["rows"], list)' "$src" \
  || { echo "push_controls: $src is not a controls result" >&2; exit 1; }
if ssh -o BatchMode=yes -o ConnectTimeout=15 personal-vps \
     "sudo -n sh -c 'install -d -m 755 $dest_dir && cat > $dest_dir/wsl-controls.json.tmp && chmod 644 $dest_dir/wsl-controls.json.tmp && mv $dest_dir/wsl-controls.json.tmp $dest_dir/wsl-controls.json'" < "$src"; then
  echo "push_controls: pushed $(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(len(d["rows"]), "rows from", d["at"])' "$src") to personal-vps:$dest_dir/wsl-controls.json"
else
  echo "push_controls: copy to personal-vps failed" >&2; exit 2
fi
