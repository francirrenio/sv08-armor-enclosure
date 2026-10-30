const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(3000); await p.click('.item >> nth=3'); await p.waitForTimeout(800);
 await p.evaluate(()=>{}); 
 // zoom: scroll on canvas
 await p.mouse.move(420,450); for(let i=0;i<6;i++){await p.mouse.wheel(0,-300); await p.waitForTimeout(100);}
 await p.waitForTimeout(800); await p.screenshot({path:'a3.png'}); await b.close();})();
