const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(6000);
 await p.click('.item >> nth=35'); await p.waitForTimeout(1500);
 await p.evaluate(()=>window.__setView([-350,75,-66],[-282,62,-66])); await p.waitForTimeout(800);
 await p.mouse.click(447,442); await p.waitForTimeout(800);
 await p.screenshot({path:'c4.png'});
 await b.close();})();
