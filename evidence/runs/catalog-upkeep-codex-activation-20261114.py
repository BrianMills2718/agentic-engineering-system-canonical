#!/usr/bin/env python3
import argparse, collections, copy, hashlib, json, pathlib, queue, subprocess, threading, time, tomllib
CANON='/home/brian/code2/agentic-engineering-system-canonical'
WT='/home/brian/code2/worktrees/aes-wiki-upkeep-20261114'
USER=pathlib.Path('/home/brian/.codex/config.toml')
SOURCE=CANON+'/.codex/hooks.json'
KEY=SOURCE+':post_tool_use:0:0'
class Failure(Exception): pass
def require(ok,msg):
    if not ok: raise Failure(msg)
def snapshot():
    data=tomllib.loads(USER.read_text()); states=copy.deepcopy(data.get('hooks',{}).get('state',{})); other=copy.deepcopy(data)
    if 'hooks' in other:
        other['hooks'].pop('state',None)
        if not other['hooks']: other.pop('hooks')
    return hashlib.sha256(json.dumps(other,sort_keys=True,default=str).encode()).hexdigest(),states,data.get('features',{}).get('hooks')
class RPC:
    def __init__(self,cwd):
        self.p=subprocess.Popen(['codex','app-server'],cwd=cwd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,bufsize=1)
        self.q=queue.Queue(); self.n=0
        def reader():
            try:
                for line in self.p.stdout:
                    try: self.q.put(json.loads(line))
                    except ValueError: self.q.put({'_invalid':True})
            finally: self.q.put({'_eof':True})
        threading.Thread(target=reader,daemon=True).start()
        try:
            self.call('initialize',{'clientInfo':{'name':'aes_hook_activation','version':'1.0'},'capabilities':{'experimentalApi':True}})
            self.send({'method':'initialized'})
        except Exception:
            self.close(); raise
    def send(self,obj):
        self.p.stdin.write(json.dumps(obj)+'\n'); self.p.stdin.flush()
    def call(self,method,params):
        self.n+=1; ident=self.n; self.send({'id':ident,'method':method,'params':params}); deadline=time.monotonic()+45
        while True:
            try: msg=self.q.get(timeout=max(.01,deadline-time.monotonic()))
            except queue.Empty: raise Failure('RPC timeout: '+method)
            require(not msg.get('_invalid') and not msg.get('_eof'),'RPC transport failure: '+method)
            if msg.get('id')==ident:
                require('error' not in msg,'RPC rejected '+method+' (details suppressed)')
                require('result' in msg,'RPC missing result: '+method)
                return msg['result']
            require(not ('id' in msg and 'method' in msg),'Unexpected server request; no approval/model requests allowed')
            require(time.monotonic()<deadline,'RPC deadline exceeded: '+method)
    def close(self):
        if self.p.poll() is None:
            self.p.terminate()
            try: self.p.wait(timeout=5)
            except subprocess.TimeoutExpired: self.p.kill(); self.p.wait(timeout=5)
def target(entry,command):
    require(not entry['errors'],'hooks/list reported errors')
    matches=[h for h in entry['hooks'] if h['key']==KEY]; require(len(matches)==1,'Expected one canonical AES handler'); h=matches[0]
    require(h['source']=='project' and h['sourcePath']==SOURCE,'Unexpected handler source')
    require(h.get('command')==command,'Handler command does not match reviewed pin')
    require(h['eventName']=='postToolUse' and h.get('handlerType')=='command','Unexpected hook event/type')
    require(h.get('matcher')=='apply_patch|Edit|Write|Bash|shell|exec_command','Unexpected hook matcher')
    return h
def configs(rpc):
    rows=[]; version=None
    for cwd in [CANON,WT]:
        r=rpc.call('config/read',{'cwd':cwd,'includeLayers':True}); layers=r.get('layers') or []
        users=[l for l in layers if l['name']['type']=='user' and l['name'].get('file')==str(USER) and not l['name'].get('profile')]
        require(len(users)==1,'Expected one user config layer')
        if version is not None: require(version==users[0]['version'],'User config changed between reads')
        version=users[0]['version']
        projects=[l for l in layers if l['name']['type']=='project' and l.get('config',{}).get('features',{}).get('hooks') is True and not l.get('disabledReason')]
        require(projects,'No active project hooks feature layer')
        require(r['config'].get('features',{}).get('hooks') is True,'Effective hooks feature not enabled')
        rows.append({'cwd':cwd,'project_hooks_enabled':True,'active_project_hook_layer':True})
    return version,rows
def main():
    p=argparse.ArgumentParser(); p.add_argument('--expected-sha',required=True); p.add_argument('--go',action='store_true'); p.add_argument('--receipt',default='/tmp/aes_codex_activation_receipt.json'); a=p.parse_args()
    require(len(a.expected_sha)==40 and all(c in '0123456789abcdef' for c in a.expected_sha),'Invalid reviewed SHA')
    require(a.go,'Prepared only: --go required; no server started or config modified')
    command='uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical@'+a.expected_sha+' lockstep refresh --client codex'
    before_hash,before_states,global_feature=snapshot(); require(global_feature is False,'Expected global features.hooks=false')
    rpc=None; mutated=False
    try:
        rpc=RPC(CANON); entries=rpc.call('hooks/list',{'cwds':[CANON,WT]})['data']
        require({e['cwd'] for e in entries}=={CANON,WT} and len(entries)==2,'Unexpected cwd inventory')
        hs=[target(e,command) for e in entries]; require(hs[0]['currentHash']==hs[1]['currentHash'],'Different canonical handler hashes')
        current=hs[0]['currentHash']; require(bool(current),'Empty current hash'); version,_=configs(rpc)
        require(snapshot()==(before_hash,before_states,global_feature),'User config changed before CAS write')
        rpc.call('config/batchWrite',{'filePath':str(USER),'expectedVersion':version,'edits':[{'keyPath':'hooks.state','mergeStrategy':'upsert','value':{KEY:{'enabled':True,'trusted_hash':current}}}],'reloadUserConfig':False})
        mutated=True; rpc.close(); rpc=None
        after_hash,after_states,after_global=snapshot(); require(after_hash==before_hash,'Non-hook-state config changed'); require(after_global is False,'Global hooks feature changed')
        require({k:v for k,v in before_states.items() if k!=KEY}=={k:v for k,v in after_states.items() if k!=KEY},'Other hook states changed')
        require(after_states.get(KEY)=={'enabled':True,'trusted_hash':current},'Target state differs from requested')
        rpc=RPC(CANON); _,config_rows=configs(rpc); entries=rpc.call('hooks/list',{'cwds':[CANON,WT]})['data']
        require({e['cwd'] for e in entries}=={CANON,WT} and len(entries)==2,'Unexpected fresh cwd inventory'); inventory=[]
        for e in entries:
            h=target(e,command); require(h['currentHash']==current and h['enabled'] is True and h['trustStatus']=='trusted','Fresh AES handler not enabled/trusted')
            counts=collections.Counter((x['source'],x['trustStatus'],x['enabled']) for x in e['hooks'] if x['key']!=KEY)
            inventory.append({'cwd':e['cwd'],'other_handlers':len(e['hooks'])-1,'other_handler_status_counts':[{'source':k[0],'trustStatus':k[1],'enabled':k[2],'count':v} for k,v in sorted(counts.items())],'warning_count':len(e['warnings'])})
        require(snapshot()==(after_hash,after_states,after_global),'Config changed during verification')
        receipt={'ok':True,'project_handler':{'key':KEY,'sourcePath':SOURCE,'reviewed_sha':a.expected_sha,'currentHash':current,'enabled':True,'trustStatus':'trusted'},'preservation':{'non_hook_state_sha256_before':before_hash,'non_hook_state_sha256_after':after_hash,'other_hook_states_preserved':True,'other_hook_state_count':len([k for k in before_states if k!=KEY]),'global_hooks_feature_false':True},'project_configs':config_rows,'inventory':inventory,'ordinary_app_server':True,'model_invoked':False}
        pathlib.Path(a.receipt).write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt))
    except Exception:
        print(json.dumps({'ok':False,'config_write_completed':mutated,'details':'Failed closed; no automatic retry or rollback'})); raise
    finally:
        if rpc: rpc.close()
if __name__=='__main__':
    try: main()
    except Failure as e: raise SystemExit(str(e))
