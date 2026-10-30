const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(7000);
 await p.$$eval('.item',els=>els[40].click()); await p.waitForTimeout(1500); await p.screenshot({path:'h0.png'});
 await p.evaluate(()=>window.__setView([0,40,560],[0,38,282])); await p.waitForTimeout(800); await p.screenshot({path:'h1.png'});
 await p.evaluate(()=>window.__setView([170,30,420],[150,30,282])); await p.waitForTimeout(800); await p.screenshot({path:'h2.png'});
 await p.evaluate(()=>window.__setView([600,60,700],[100,40,280])); await p.waitForTimeout(800); await p.screenshot({path:'h3.png'});
 console.log(JSON.stringify(errs)); await b.close();})();
