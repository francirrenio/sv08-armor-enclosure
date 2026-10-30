const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(6000);
 await p.click('.item >> nth=36'); await p.waitForTimeout(1500);
 await p.screenshot({path:'f0.png'});
 await p.evaluate(()=>window.__setView([-620,60,-40],[-282,35,-40])); await p.waitForTimeout(800); await p.screenshot({path:'f1.png'});
 await p.evaluate(()=>window.__setView([420,45,110],[282,30,110])); await p.waitForTimeout(800); await p.screenshot({path:'f2.png'});
 await p.evaluate(()=>window.__setView([340,50,92],[282,40,92])); await p.waitForTimeout(800); await p.screenshot({path:'f3.png'});
 console.log(JSON.stringify(errs));
 await b.close();})();
