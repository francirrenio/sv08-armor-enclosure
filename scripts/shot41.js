const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1500,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load',timeout:120000});
 await p.waitForTimeout(7000);
 const clk=async n=>{await p.$$eval('.item',(els,n)=>{const b=[...els].find(e=>e.querySelector('.num').textContent==n); b.click();},n); await p.waitForTimeout(1500);};
 await clk('55'); await p.screenshot({path:'t55a.png'});
 await p.evaluate(()=>window.__setView([300,450,-700],[0,590,-260])); await p.waitForTimeout(1200); await p.screenshot({path:'t55b.png'});
 await clk('56'); await p.screenshot({path:'t56a.png'});
 await p.evaluate(()=>window.__setView([700,600,-450],[260,550,-60])); await p.waitForTimeout(1200); await p.screenshot({path:'t56b.png'});
 console.log(JSON.stringify(errs)); await b.close();})();
