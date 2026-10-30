const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1100,height:1400}});
 const html=require('fs').readFileSync('lista_materiais.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head><body>'+html+'</body></html>',{waitUntil:'load'});
 await p.waitForTimeout(1500); await p.screenshot({path:'bom1.png'}); await b.close(); })();
