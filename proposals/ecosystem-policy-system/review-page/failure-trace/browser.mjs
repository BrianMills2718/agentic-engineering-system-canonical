import { writeFile, readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const [modulePath, executablePath, url, project]=process.argv.slice(2);
const {chromium}=await import(modulePath),dir=dirname(fileURLToPath(import.meta.url));
const results=[],assert=(name,ok,evidence='')=>results.push({name,outcome:ok?'passed':'failed',evidence});
const trace=JSON.parse(await readFile(join(dir,'trace.json'),'utf8'));
const model=JSON.parse(await readFile(join(dir,'../layout.json'),'utf8'));
const ids=['meaning','execution','coverage','classification','reporting','closure'];
assert('trace contains exact expected stage membership',trace.stages.map(s=>s.id).join('|')===ids.join('|'));
assert('five handoffs connect the expected endpoints',trace.links.every((x,i)=>x.from===ids[i]&&x.to===ids[i+1])&&trace.links.length===ids.length-1);
assert('all stages bind to existing semantic model parts',trace.stages.every(s=>model.elements[s.modelRef]));
for(const [id,s] of Object.entries(trace.sources)){
 const text=execFileSync('git',['-C',project,'show',s.revision+':'+s.path],{encoding:'utf8'});
 assert('pinned source line exists: '+id,!!text.split('\n')[s.line-1]&&s.url.endsWith('#L'+s.line),s.url);
}
const browser=await chromium.launch({headless:true,executablePath});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const response=await page.goto(url);await page.evaluate(()=>document.fonts.ready);
 assert('review page returns HTTP 200',response.status()===200);
 assert('six stages render with exact membership',(await page.locator('.stage').evaluateAll(ns=>ns.map(n=>n.dataset.stage))).join('|')===ids.join('|'));
 assert('root break is selected on load',await page.locator('[data-stage=classification]').getAttribute('aria-pressed')==='true');
 assert('fixture boundary and unimplemented repair are visible',/No real concern was closed/.test(await page.locator('.boundary').innerText())&&/Not implemented/.test(await page.locator('#detail').innerText()));
 assert('desktop whole flow fits on one screen',await page.locator('.flow').evaluate(e=>e.getBoundingClientRect().bottom<=innerHeight));
 assert('desktop has no page overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 for(const id of ids){
  await page.locator('[data-stage='+id+']').click();
  const stage=trace.stages.find(s=>s.id===id),detail=await page.locator('#detail').innerText();
  assert('stage opens its own explanation: '+id,detail.includes(stage.detail));
  if(id==='execution')assert('live hook execution stays visibly unverified',/Live hook execution was not verified/.test(detail));
  if(id==='closure')assert('closure disclosure remains isolated',/isolated in-memory issue adapter/.test(detail)&&/no GitHub issue was closed/.test(detail));
  for(const link of await page.locator('#detail .source').all()){
   const href=await link.getAttribute('href');assert('source link opens exact pinned commit',href.includes('/blob/'+trace.subject.revision+'/')&&/#L\d+$/.test(href));
  }
 }
 await page.locator('[data-stage=classification]').click();
 const controls=page.locator('[data-help]');
 for(let i=0;i<await controls.count();i++){
  const c=controls.nth(i);await c.scrollIntoViewIfNeeded();await c.hover();await page.waitForTimeout(160);
  assert('styled tooltip within 200ms: '+i,await page.locator('#tooltip').isVisible()&&await page.locator('#tooltip').innerText()===await c.getAttribute('data-help'));
 }
 await page.locator('[data-stage=classification]').focus();await page.waitForTimeout(160);
 assert('keyboard focus shows the styled tooltip',await page.locator('#tooltip').isVisible());
 assert('painted stage text stays inside its button',await page.locator('.stage').evaluateAll(ns=>ns.every(n=>{
  const b=n.getBoundingClientRect();return [...n.querySelectorAll('strong,small,.state')].every(t=>{const r=t.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom;});
 })));
 await page.mouse.move(0,0);await page.locator('[data-stage=classification]').blur();await page.screenshot({path:join(dir,'desktop.png'),fullPage:true});
 for(const path of ['trace.json','probe-output.json']){
  const r=await page.request.get(new URL(path,url).href);assert('evidence opens: '+path,r.status()===200&&(await r.json()).schema.startsWith('ecosystem-'));
 }
 const mobile=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});mobile.on('pageerror',e=>errors.push(e.message));await mobile.goto(url);
 assert('phone layout has no page overflow',await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await mobile.locator('[data-stage=closure]').tap();await mobile.waitForTimeout(170);
 assert('phone tap opens stage details',/real router called close_concern/.test(await mobile.locator('#detail').innerText()));
 assert('phone tap shows a styled tooltip',await mobile.locator('#tooltip').isVisible());
 await mobile.screenshot({path:join(dir,'phone.png'),fullPage:true});
 const home=new URL('../index.html',url).href;await page.goto(home);const newLink=page.getByRole('link',{name:'Failure trace Missing evidence → clear → close'});await newLink.hover();await page.waitForTimeout(160);
 assert('model navigation link has a styled tooltip',await page.locator('#tooltip').isVisible());
 await newLink.click();assert('model navigation opens the failure trace',new URL(page.url()).pathname.endsWith('/failure-trace/index.html'));
 assert('no JavaScript page errors',errors.length===0,errors);
}catch(e){results.push({name:'browser execution',outcome:'errored',evidence:e.stack});}finally{await browser.close();}
const counts={passed:results.filter(r=>r.outcome==='passed').length,failed:results.filter(r=>r.outcome==='failed').length,errored:results.filter(r=>r.outcome==='errored').length,skipped:0};
const output={results,counts,exit_status:counts.failed||counts.errored?1:0};await writeFile(join(dir,'browser-result.json'),JSON.stringify(output,null,2)+'\n');console.log(JSON.stringify(output));process.exitCode=output.exit_status;
