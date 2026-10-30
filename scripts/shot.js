const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const errs=[]; p.on('console',m=>{if(m.type()==='error')errs.push(m.text())}); p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(2500); await p.screenshot({path:'pg1.png'});
 await p.click('.item >> nth=1'); await p.waitForTimeout(1200); await p.screenshot({path:'pg2.png'});
 await p.click('.item >> nth=2'); await p.waitForTimeout(1200); await p.screenshot({path:'pg3.png'});
 console.log('ERR',JSON.stringify(errs)); await b.close();})();
