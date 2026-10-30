const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1600,height:900}});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(6000);
 await p.evaluate(()=>window.__setView([0,45,1500],[0,45,280])); await p.waitForTimeout(900); await p.screenshot({path:'fr0.png'});
 await p.evaluate(()=>window.__setView([150,45,700],[150,45,280])); await p.waitForTimeout(900); await p.screenshot({path:'fr1.png'});
 await b.close();})();
