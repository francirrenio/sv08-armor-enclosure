const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(7000);
 await p.$$eval('.item',els=>{const b=[...els].find(e=>e.querySelector('.num').textContent=='50'); b.click();}); await p.waitForTimeout(1500); await p.screenshot({path:'jn0.png'}); await p.evaluate(()=>window.__setView([60,585,150],[20,588,260])); await p.waitForTimeout(1200); await p.screenshot({path:'jn1.png'}); await p.evaluate(()=>window.__setView([160,560,-60],[250,615,0])); await p.waitForTimeout(1200); await p.screenshot({path:'jn2.png'});
 console.log(JSON.stringify(errs)); await b.close();})();
