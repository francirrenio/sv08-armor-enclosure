const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(3000);
 await p.click('.item >> nth=15'); await p.waitForTimeout(1500); const views=JSON.parse(process.argv[2]);
 for(const [i,v] of views.entries()){ await p.evaluate((v)=>window.__setView(v[0],v[1]),v); await p.waitForTimeout(900); await p.screenshot({path:'v'+i+'.png'}); }
 await b.close();})();
