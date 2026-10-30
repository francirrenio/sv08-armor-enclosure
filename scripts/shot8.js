const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(3000); await p.mouse.click(500,470); await p.waitForTimeout(1200); await p.screenshot({path:'sel.png'});
 console.log('ERR',JSON.stringify(errs), await p.evaluate(()=>{const s=document.querySelector('.parts label.sel'); return s? s.textContent:null;}));
 await b.close();})();
