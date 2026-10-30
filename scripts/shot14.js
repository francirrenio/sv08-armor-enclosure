const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(3000);
 await p.click('.item >> nth=19'); await p.waitForTimeout(1200);
 await p.evaluate(()=>window.__setView([560,620,330],[275,585,245])); await p.waitForTimeout(600);
 await p.evaluate(()=>{document.getElementById('pl-thCantF').closest('details').open=true;}); await p.waitForTimeout(300); await p.click('#pl-thCantF .pln'); await p.waitForTimeout(500);
 await p.click('#sel-clear'); await p.waitForTimeout(800);
 await p.screenshot({path:'tr0.png'});
 console.log(JSON.stringify(errs), await p.textContent('#sel-clear'));
 await b.close();})();
