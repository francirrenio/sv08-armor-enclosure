const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:1000}});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 const V=[[[0,120,330],[0,560,280],'cb1'],[[300,470,420],[245,540,280],'cb2'],[[250,540,700],[250,540,286],'cb3']];
 for(const [c,t,n] of V){ await p.evaluate(([c,t])=>window.__setView(c,t),[c,t]); await p.waitForTimeout(1500); await p.screenshot({path:n+'.png',clip:{x:16,y:80,width:1080,height:900}}); }
 await b.close();})();
