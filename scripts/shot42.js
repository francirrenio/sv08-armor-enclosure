const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 const clk=async n=>{await p.$$eval('.item',(els,n)=>{const b=[...els].find(e=>e.querySelector('.num').textContent==n); b.click();},n); await p.waitForTimeout(1500);};
 
 for(const [i,c] of [[[150,380,0],[283,560,0]],[[150,420,40],[275,545,20]],[[200,450,60],[275,575,0]],[[600,560,0],[283,560,0]]].entries()){await p.evaluate(([c,t])=>window.__setView(c,t),c); await p.waitForTimeout(1200); await p.screenshot({path:'h'+i+'.png'});}
 console.log(JSON.stringify(errs)); await b.close();})();
