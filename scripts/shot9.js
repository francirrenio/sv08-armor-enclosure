const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']}); const p=await b.newPage({viewport:{width:1400,height:850}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e))); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 const html=require('fs').readFileSync('pe_coluna_FD.html','utf8');
 await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'networkidle'});
 await p.waitForTimeout(3000); await p.mouse.click(560,560); await p.waitForTimeout(800);
 const name=await p.evaluate(()=>document.getElementById('sel-n').textContent);
 await p.click('#sel-axes button >> nth=1'); await p.click('#sel-axes button >> nth=1'); await p.click('#sel-axes button >> nth=1');
 await p.click('#sel-drag'); await p.waitForTimeout(800); await p.screenshot({path:'mv1.png'});
 const v=await p.evaluate(()=>[...document.querySelectorAll('#sel-axes .v')].map(x=>x.textContent));
 await p.click('#sel-back'); await p.waitForTimeout(300);
 const v2=await p.evaluate(()=>[...document.querySelectorAll('#sel-axes .v')].map(x=>x.textContent));
 // teste do gerador STEP dentro da pagina
 const st=await p.evaluate(()=>{const g=new THREE.BoxGeometry(10,10,10); const pos=g.attributes.position.array, idx=g.index.array; const s=meshToStep('t',pos,idx,{x:0,y:0,z:0}); const z=makeZip([{name:'a.step',data:new TextEncoder().encode(s)}]); return [s.length,z.size];});
 console.log('sel',name,'off',JSON.stringify(v),'back',JSON.stringify(v2),'step',st,'ERR',JSON.stringify(errs)); await b.close();})();
