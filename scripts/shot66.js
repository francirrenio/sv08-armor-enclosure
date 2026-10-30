const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:1000}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 const V=[[[300,150,420],[228,150,284],'x27'],[[120,140,380],[20,100,284],'x28'],[[0,300,330],[0,300,284],'x29'],[[330,800,560],[228,800,284],'x30']];
 for(const [c,t,n] of V){ await p.evaluate(([c,t])=>window.__setView(c,t),[c,t]); await p.waitForTimeout(1500); await p.screenshot({path:n+'.png',clip:{x:16,y:80,width:1080,height:900},timeout:180000}); }
 console.log(JSON.stringify(errs)); await b.close();})();
