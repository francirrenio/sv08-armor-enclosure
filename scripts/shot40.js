const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 await p.$$eval('.item',els=>{const b=[...els].find(e=>e.querySelector('.num').textContent=='54'); b.click();}); await p.waitForTimeout(1500); await p.screenshot({path:'tb54a.png'}); await p.evaluate(()=>window.__setView([-250,140,-900],[-40,40,-280])); await p.waitForTimeout(1200); await p.screenshot({path:'tb54b.png'}); await p.evaluate(()=>window.__setView([-450,120,-560],[-165,25,-280])); await p.waitForTimeout(1200); await p.screenshot({path:'tb54c.png'});
 console.log(JSON.stringify(errs)); await b.close();})();
