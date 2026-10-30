const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:1000}});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(7000);
 const V=[['fr_a.png',[0,330,1500],[0,330,0]],['fr_b.png',[700,520,1100],[0,330,100]],['fr_c.png',[150,620,700],[120,540,250]]];
 for(const [f,c,t] of V){ await p.evaluate(([c,t])=>window.__setView(c,t),[c,t]); await p.waitForTimeout(1200); await p.screenshot({path:f,clip:{x:16,y:82,width:1076,height:806}}); }
 await b.close();})();
