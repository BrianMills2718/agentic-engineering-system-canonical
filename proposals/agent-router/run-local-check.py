"""Detached local merge gate; records exact revision, command, timing and exit."""
import datetime,json,os,subprocess,time
from pathlib import Path
root=Path(__file__).resolve().parents[2]
started=time.monotonic()
revision=subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()
command=["make","check","PYTHON=/home/brian/code/agentic-engineering-system-canonical/.venv/bin/python"]
print(json.dumps({"event":"gate_start","utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"revision":revision,"command":command}),flush=True)
result=subprocess.run(command,cwd=root)
receipt={"state":"passed" if result.returncode==0 else "failed","command":command,"revision":revision,"exit_status":result.returncode,"elapsed_seconds":round(time.monotonic()-started,3),"log_path":os.environ["AGENT_ROUTER_GATE_LOG"]}
(root/"proposals/agent-router/local-check.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"event":"gate_finished",**receipt}),flush=True)
raise SystemExit(result.returncode)
