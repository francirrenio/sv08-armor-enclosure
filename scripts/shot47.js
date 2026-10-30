const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:1000}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 const V=[[[520,330,-700],[240,310,-286],'pt6'],[[0,350,-1500],[0,300,0],'pt2'],[[420,140,-560],[200,110,-286],'pt3'],[[300,560,-560],[220,520,-286],'pt4'],[[300,470,420],[245,540,280],'pt5']];
 for(const [c,t,n] of V){ await p.evaluate(([c,t])=>window.__setView(c,t),[c,t]); await p.waitForTimeout(1500); await p.screenshot({path:n+'.png',clip:{x:16,y:80,width:1080,height:900},timeout:180000}); }
 console.log(JSON.stringify(errs)); await b.close();})();
