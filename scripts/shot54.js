const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:1000}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 await p.$$eval('.item',els=>{const b=[...els].find(e=>e.querySelector('.num').textContent=='66'); b.click();}); await p.waitForTimeout(1500);
 for(const f of [0,1]){ await p.evaluate(f=>window.__setAnim(f),f); await p.waitForTimeout(900); await p.screenshot({path:'sv'+f+'.png',clip:{x:16,y:80,width:1080,height:900},timeout:180000}); }
 console.log(JSON.stringify(errs)); await b.close();})();
