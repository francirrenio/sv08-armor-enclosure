const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 await p.$$eval('.item',els=>{const b=[...els].find(e=>e.querySelector('.num').textContent=='58'); b.click();}); await p.waitForTimeout(1500);
 await p.evaluate(()=>window.__setView([360,700,-40],[278,590,60])); 
 for(const f of [0,0.5,1]){ await p.evaluate(f=>window.__setAnim(f),f); await p.waitForTimeout(900); await p.screenshot({path:'an'+Math.round(f*10)+'.png'}); }
 await p.evaluate(()=>window.__setView([380,700,130],[258,585,124])); await p.waitForTimeout(900); await p.screenshot({path:'anE.png'});
 
 console.log(JSON.stringify(errs)); await b.close();})();
