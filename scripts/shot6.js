const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const html=require('fs').readFileSync(process.argv[2]||'pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(3000);
 await p.evaluate(()=>{ window.__setView && window.__setView([235,45,520],[205,35,284]); });
 await p.waitForTimeout(800); await p.screenshot({path:process.argv[3]||'f1.png'}); await b.close();})();
