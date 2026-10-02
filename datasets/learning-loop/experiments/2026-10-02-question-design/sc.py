import json, os, re, glob, urllib.request, sys
key = [l.split("=",1)[1].strip().strip('"\'') for l in open(os.path.expanduser("~/.secrets/api_keys.env")) if l.startswith("OPENROUTER_API_KEY=")][0]
t = open(os.path.expanduser("~/code/agentic-engineering-system-canonical/docs/failure-modes.md")).read()
fam = {}
for s in re.split(r"^## ", t, flags=re.M):
    m = re.match(r"([A-Z]) — (.+?)\s*(\*\*\[register\]\*\*)?\n+> \*(.+?)\*", s)
    if not m: continue
    body = s[m.end():]
    paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith(">")]
    fam[m.group(1)] = f"{m.group(2).strip()}. Guiding question: {m.group(4).strip()} {(paras[0] if paras else '')[:300]}"
Q = {"is_failure": {"type":"noul","instructions":"This learning describes a reasoning or control failure (an agent or system got something wrong), not just a plain fact about a tool or product."}}
crit = dict(fam); crit["other"] = "A real reasoning or control failure that none of the listed families describes well."
Q["family"] = {"type":"choice","instructions":"Which failure-mode family does this recorded learning best illustrate? Read each family's description. Choose 'other' if no family fits well.","criteria":crit}
GT = {"Slack pastes carried times":"U","GitHub-hosted runner images":"A M","three claimed overlaps between Company Planning":"U L",
"two outside research passes":"T B","sync_priority_to_single_subscription":"E","project-browser deploy were reported":"C A G",
"self-hosted gotchas":"fact","Two self-corrections deploying Paperclip":"U","I added Cloudflare Access":"R","A /proc cwd scan":"V",
"an @~/... import":"D fact","Told Brian second-brain-mega had 2 stale pins":"V","test_compaction_preflight_report":"M",
"generate_wiki_routing_stub.py emitted":"R","byte-identical to the existing stub":"V U","second-brain-mega pins Inside-Success/llm_client":"E",
"My ad hoc audit marked":"L","Mirror PR #3 fixed":"E J","worktree cleanup removed 21":"E","`codex exec PROMPT`":"W fact",
"lrn-20260826T153101933360Z-9ae3387b7d":"U","lrn-20260825T163008796978Z-c5adea4698":"M A","lrn-20260916T013344314194Z-be2946d9b6":"U V",
"lrn-20260908T011241603353Z-7467c89055":"K","lrn-20260909T051708158378Z-b220c35de9":"A","lrn-20260906T174434094188Z-032877a6f4":"Q",
"lrn-20260823T222844060404Z-a710ef48fc":"N","lrn-20260914T045354777955Z-fb40214eb3":"E U","lrn-20260905T012617322666Z-1e4465e00d":"L",
"lrn-20260902T222058124118Z-21912923ae":"M"}
files = sorted(glob.glob(os.path.expanduser("~/code/project-meta/learnings/entries/*.json")))
docs = [json.load(open(f)) for f in files]
def find(k):
    for d in docs:
        if d.get("entry_id") == k: return d
    for d in reversed(docs):
        if k in str(d.get("learning") or d.get("finding") or d.get("lesson") or ""): return d
done = {}
if os.path.exists("sc_out.jsonl"):
    for l in open("sc_out.jsonl"): r = json.loads(l); done[r["key"]] = r
with open("sc_out.jsonl","a") as fh:
    for k, acc in GT.items():
        if k in done: continue
        d = find(k)
        if not d: print("NOT FOUND", k, flush=True); continue
        txt = str(d.get("learning") or d.get("finding") or d.get("lesson") or "")
        state = f"Recorded learning:\n{txt[:1800]}\nRecommended action: {str(d.get('recommended_action') or '')[:400]}"
        req = urllib.request.Request("https://openrouter.ai/api/v1/systemone", data=json.dumps({"model":"typesafe/jev-1.13","state":state,"questions":Q}).encode(), headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"}, method="POST")
        try: r = json.loads(urllib.request.urlopen(req, timeout=120).read())
        except Exception as e: print("ERR", k, e, flush=True); continue
        a = r["answers"]
        rec = {"key":k,"acc":acc.split(),"is_failure":a["is_failure"]["noul"],"scores":a["family"]["probabilities"],"choice":a["family"]["choice"],"cost":r.get("usage",{}).get("cost")}
        fh.write(json.dumps(rec)+"\n"); fh.flush(); print("ok", k[:40], flush=True)
print("DONE", flush=True)
