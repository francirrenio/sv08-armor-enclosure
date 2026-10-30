const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(6000);
 await p.click('.item >> nth=35'); await p.waitForTimeout(1500);
 await p.screenshot({path:'c0.png'});
 await p.evaluate(()=>window.__setView([-420,45,-90],[-282,37,-90])); await p.waitForTimeout(800);
 await p.screenshot({path:'c1.png'});
 await p.evaluate(()=>window.__setView([-345,40,-92],[-282,37,-92])); await p.waitForTimeout(800);
 await p.screenshot({path:'c2.png'});
 await p.evaluate(()=>window.__setView([-350,75,-66],[-282,62,-66])); await p.waitForTimeout(800);
 await p.screenshot({path:'c3.png'});
 console.log(JSON.stringify(errs));
 await b.close();})();
