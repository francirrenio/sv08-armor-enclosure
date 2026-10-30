const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:1000}});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(9000);
 const V=[['tr_a.png',[0,560,-1400],[0,560,0]],['tr_b.png',[-700,800,-1000],[0,560,-100]]];
 for(const [f,c,t] of V){ await p.evaluate(([c,t])=>window.__setView(c,t),[c,t]); await p.waitForTimeout(1500); await p.screenshot({path:f,clip:{x:16,y:82,width:1076,height:806}}); }
 await b.close();})();
