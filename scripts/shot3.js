const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(3000);
 await p.click('.item >> nth=12'); await p.waitForTimeout(1500); await p.screenshot({path:'a1.png'});
 await p.click('#b-iso'); await p.waitForTimeout(800); await p.screenshot({path:'a2.png'});
 console.log('ERR',JSON.stringify(errs)); await b.close();})();
