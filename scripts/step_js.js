// ---- exportacao STEP (B-rep com faces planas, triangulos coplanares unidos) + STL, empacotados em .zip ----
function meshToStep(name,pos,idx,off){
  const nv=pos.length/3, P=new Float64Array(pos.length);
  for(let i=0;i<nv;i++){P[3*i]=pos[3*i]+off.x;P[3*i+1]=pos[3*i+1]+off.y;P[3*i+2]=pos[3*i+2]+off.z;}
  // juntar vertices iguais
  const key=i=>P[3*i].toFixed(4)+','+P[3*i+1].toFixed(4)+','+P[3*i+2].toFixed(4);
  const vmap=new Map(), remap=new Int32Array(nv), V=[];
  for(let i=0;i<nv;i++){const k=key(i); let j=vmap.get(k); if(j===undefined){j=V.length/3;vmap.set(k,j);V.push(P[3*i],P[3*i+1],P[3*i+2]);} remap[i]=j;}
  const T=[]; for(let t=0;t<idx.length;t+=3){const a=remap[idx[t]],b=remap[idx[t+1]],c=remap[idx[t+2]]; if(a!==b&&b!==c&&a!==c) T.push([a,b,c]);}
  {let vol=0; for(const [a,b,c] of T){const A=[V[3*a],V[3*a+1],V[3*a+2]],B=[V[3*b],V[3*b+1],V[3*b+2]],C=[V[3*c],V[3*c+1],V[3*c+2]];
     vol+=A[0]*(B[1]*C[2]-B[2]*C[1])-A[1]*(B[0]*C[2]-B[2]*C[0])+A[2]*(B[0]*C[1]-B[1]*C[0]);}
   if(vol<0) for(const tr of T){const x=tr[1]; tr[1]=tr[2]; tr[2]=x;}}
  const nt=T.length, N=new Float64Array(nt*3), Dp=new Float64Array(nt), AR=new Float64Array(nt), LE=new Array(nt);
  const vx=i=>[V[3*i],V[3*i+1],V[3*i+2]];
  for(let t=0;t<nt;t++){const [a,b,c]=T[t].map(vx); const u=[b[0]-a[0],b[1]-a[1],b[2]-a[2]],v=[c[0]-a[0],c[1]-a[1],c[2]-a[2]];
    let n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]; const l=Math.hypot(...n)||1; AR[t]=l/2; n=n.map(x=>x/l);
    {const tr=T[t]; let bl=-1,bk=0; for(let k=0;k<3;k++){const p=vx(tr[k]),q=vx(tr[(k+1)%3]); const d=Math.hypot(p[0]-q[0],p[1]-q[1],p[2]-q[2]); if(d>bl){bl=d;bk=k;}} LE[t]=[tr[bk],tr[(bk+1)%3],bl];}
    N[3*t]=n[0];N[3*t+1]=n[1];N[3*t+2]=n[2];Dp[t]=n[0]*a[0]+n[1]*a[1]+n[2]*a[2];}
  // vizinhanca por aresta e grupos coplanares conectados
  const ek=(a,b)=>a<b?a+'_'+b:b+'_'+a, emap=new Map();
  T.forEach((tr,t)=>{for(let k=0;k<3;k++){const e=ek(tr[k],tr[(k+1)%3]); (emap.get(e)||emap.set(e,[]).get(e)).push(t);}});
  const par=new Int32Array(nt).map((_,i)=>i), find=x=>{while(par[x]!==x){par[x]=par[par[x]];x=par[x];}return x;};
  const degen=t=>AR[t]<1e-6*Math.max(1e-9,LE[t][2]*LE[t][2]);
  const same=(s,t)=>!degen(s)&&!degen(t)&&Math.abs(N[3*s]*N[3*t]+N[3*s+1]*N[3*t+1]+N[3*s+2]*N[3*t+2]-1)<1e-7&&Math.abs(Dp[s]-Dp[t])<1e-3;
  for(const ts of emap.values()) if(ts.length===2&&same(ts[0],ts[1])){const a=find(ts[0]),b=find(ts[1]); if(a!==b) par[a]=b;}
  {const good=new Uint8Array(nt); for(let t=0;t<nt;t++) good[t]=degen(t)?0:1;
   const rootGood=()=>{const g=new Map(); for(let t=0;t<nt;t++) if(good[t]) g.set(find(t),1); return g;};
   for(let it=0;it<20;it++){ let changed=false; const rg=rootGood();
     for(let t=0;t<nt;t++){ if(!degen(t)) continue; if(rg.has(find(t))) continue;
       const tr=T[t]; const order=[[LE[t][0],LE[t][1]]]; for(let k=0;k<3;k++) order.push([tr[k],tr[(k+1)%3]]);
       for(const [a,b] of order){ const ts=emap.get(ek(a,b))||[]; let done=false; for(const o of ts){ if(o===t) continue; if(rg.has(find(o))){const x=find(t),y=find(o); if(x!==y){par[x]=y; changed=true;} done=true; break;} } if(done) break; } }
     if(!changed) break; } }
  const groups=new Map(); for(let t=0;t<nt;t++){const r=find(t); (groups.get(r)||groups.set(r,[]).get(r)).push(t);}
  // escrita
  const L=[]; let id=0; const E=s=>{id++; L.push('#'+id+'='+s+';'); return id;};
  const f=x=>{let s=(+x).toFixed(6); if(s.indexOf('.')<0) s+='.'; return s.replace(/0+$/,'').replace(/\.$/,'.0');};
  const ctxApp=E("APPLICATION_CONTEXT('core data for automotive mechanical design processes')");
  E("APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#"+ctxApp+")");
  const pc=E("PRODUCT_CONTEXT('',#"+ctxApp+",'mechanical')");
  const prod=E("PRODUCT('"+name+"','"+name+"','',(#"+pc+"))");
  const pdf=E("PRODUCT_DEFINITION_FORMATION('','',#"+prod+")");
  const pdc=E("PRODUCT_DEFINITION_CONTEXT('part definition',#"+ctxApp+",'design')");
  const pd=E("PRODUCT_DEFINITION('design','',#"+pdf+",#"+pdc+")");
  const pds=E("PRODUCT_DEFINITION_SHAPE('','',#"+pd+")");
  const mm=E("(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.))");
  const rad=E("(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.))");
  const sr=E("(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT())");
  const unc=E("UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-04),#"+mm+",'distance_accuracy_value','')");
  const gctx=E("(GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#"+unc+")) GLOBAL_UNIT_ASSIGNED_CONTEXT((#"+mm+",#"+rad+",#"+sr+")) REPRESENTATION_CONTEXT('',''))");
  const o0=E("CARTESIAN_POINT('',(0.,0.,0.))"), dz=E("DIRECTION('',(0.,0.,1.))"), dx=E("DIRECTION('',(1.,0.,0.))");
  const ax0=E("AXIS2_PLACEMENT_3D('',#"+o0+",#"+dz+",#"+dx+")");
  const vp=new Map(); const vpt=i=>{if(vp.has(i)) return vp.get(i); const c=E("CARTESIAN_POINT('',("+f(V[3*i])+","+f(V[3*i+1])+","+f(V[3*i+2])+"))"); const v=E("VERTEX_POINT('',#"+c+")"); const r={c,v}; vp.set(i,r); return r;};
  const edges=new Map();
  const edge=(a,b)=>{const k=ek(a,b); if(edges.has(k)) return edges.get(k); const s=Math.min(a,b),e=Math.max(a,b);
    const A=vpt(s),B=vpt(e); const d=[V[3*e]-V[3*s],V[3*e+1]-V[3*s+1],V[3*e+2]-V[3*s+2]]; const l=Math.hypot(...d)||1;
    const dr=E("DIRECTION('',("+f(d[0]/l)+","+f(d[1]/l)+","+f(d[2]/l)+"))"); const vec=E("VECTOR('',#"+dr+","+f(l)+")"); const ln=E("LINE('',#"+A.c+",#"+vec+")");
    const ec=E("EDGE_CURVE('',#"+A.v+",#"+B.v+",#"+ln+",.T.)"); const r={ec,s}; edges.set(k,r); return r;};
  const faces=[];
  for(const ts of groups.values()){
    // arestas de contorno do grupo (direcao do triangulo)
    const cnt=new Map(); for(const t of ts){const tr=T[t]; for(let k=0;k<3;k++){const e=ek(tr[k],tr[(k+1)%3]); cnt.set(e,(cnt.get(e)||0)+1);}}
    const nxt=new Map(); for(const t of ts){const tr=T[t]; for(let k=0;k<3;k++){const a=tr[k],b=tr[(k+1)%3]; if(cnt.get(ek(a,b))===1){(nxt.get(a)||nxt.set(a,[]).get(a)).push(b);}}}
    let t0=ts[0]; for(const t of ts) if(!degen(t)){t0=t;break;} const n=[N[3*t0],N[3*t0+1],N[3*t0+2]];
    if(ts.every(degen)) continue;
    const loops=[]; let guard=0;
    for(const [a0] of nxt){ while((nxt.get(a0)||[]).length){ const loop=[a0]; let cur=a0; 
        let prev=null;
        while(true){const arr=nxt.get(cur); if(!arr||!arr.length) break; let k=arr.length-1;
          if(arr.length>1&&prev!==null){ const pc=vx(cur),pp=vx(prev); const din=[pc[0]-pp[0],pc[1]-pp[1],pc[2]-pp[2]]; let bestA=1e9;
            arr.forEach((c,j)=>{const q=vx(c); const dout=[q[0]-pc[0],q[1]-pc[1],q[2]-pc[2]];
              const cr=[din[1]*dout[2]-din[2]*dout[1],din[2]*dout[0]-din[0]*dout[2],din[0]*dout[1]-din[1]*dout[0]];
              const ang=Math.atan2(cr[0]*n[0]+cr[1]*n[1]+cr[2]*n[2], din[0]*dout[0]+din[1]*dout[1]+din[2]*dout[2]); if(ang<bestA){bestA=ang;k=j;}}); }
          const nb=arr.splice(k,1)[0]; if(nb===a0&&!(nxt.get(a0)||[]).length) break; if(nb===a0){ break;} prev=cur; loop.push(nb); cur=nb; if(++guard>5e6) break;}
        loops.push(loop);} }
    const area=lp=>{let s=[0,0,0]; for(let i=0;i<lp.length;i++){const p=vx(lp[i]),q=vx(lp[(i+1)%lp.length]); s[0]+=p[1]*q[2]-p[2]*q[1]; s[1]+=p[2]*q[0]-p[0]*q[2]; s[2]+=p[0]*q[1]-p[1]*q[0];} return (s[0]*n[0]+s[1]*n[1]+s[2]*n[2])/2;};
    const p0=vx(T[t0][0]); let r=Math.abs(n[0])<0.9?[1,0,0]:[0,1,0]; let rx=[r[1]*n[2]-r[2]*n[1],r[2]*n[0]-r[0]*n[2],r[0]*n[1]-r[1]*n[0]]; const rl=Math.hypot(...rx); rx=rx.map(x=>x/rl);
    const pc_=E("CARTESIAN_POINT('',("+f(p0[0])+","+f(p0[1])+","+f(p0[2])+"))"); const nd=E("DIRECTION('',("+f(n[0])+","+f(n[1])+","+f(n[2])+"))"); const rd=E("DIRECTION('',("+f(rx[0])+","+f(rx[1])+","+f(rx[2])+"))");
    const pl=E("PLANE('',#"+E("AXIS2_PLACEMENT_3D('',#"+pc_+",#"+nd+",#"+rd+")")+")");
    // varias regioes no mesmo plano: cada contorno externo vira uma face, furos vao para o externo que os contem
    const u2=p=>[p[0]*rx[0]+p[1]*rx[1]+p[2]*rx[2], p[0]*(n[1]*rx[2]-n[2]*rx[1])+p[1]*(n[2]*rx[0]-n[0]*rx[2])+p[2]*(n[0]*rx[1]-n[1]*rx[0])];
    const inside=(pt,lp)=>{let c=false; const P2=lp.map(i=>u2(vx(i))); for(let i=0,j=P2.length-1;i<P2.length;j=i++){const [xi,yi]=P2[i],[xj,yj]=P2[j]; if(((yi>pt[1])!==(yj>pt[1]))&&(pt[0]<(xj-xi)*(pt[1]-yi)/(yj-yi)+xi)) c=!c;} return c;};
    const outs=[], holes=[];
    for(const lp of loops){ if(lp.length<3) continue; const a=area(lp); if(Math.abs(a)<1e-6) continue; (a>0?outs:holes).push({lp,a}); }
    if(!outs.length) continue;
    const mk=lp=>{const oe=lp.map((a,k)=>{const b=lp[(k+1)%lp.length]; const g=edge(a,b); return E("ORIENTED_EDGE('',*,*,#"+g.ec+","+(g.s===a?'.T.':'.F.')+")");}); return E("EDGE_LOOP('',("+oe.map(x=>'#'+x).join(',')+"))");};
    const asg=outs.map(()=>[]);
    for(const h of holes){ const pt=u2(vx(h.lp[0])); let k=outs.findIndex(o=>inside(pt,o.lp)); if(k<0){ let bk=0,ba=-1; outs.forEach((o,i)=>{if(o.a>ba){ba=o.a;bk=i;}}); k=bk;} asg[k].push(h); }
    outs.forEach((o,i)=>{ const bds=[E("FACE_OUTER_BOUND('',#"+mk(o.lp)+",.T.)")]; for(const h of asg[i]) bds.push(E("FACE_BOUND('',#"+mk(h.lp)+",.T.)"));
      faces.push(E("ADVANCED_FACE('',("+bds.map(x=>'#'+x).join(',')+"),#"+pl+",.T.)")); });
  }
  const sh=E("CLOSED_SHELL('',("+faces.map(x=>'#'+x).join(',')+"))");
  const br=E("MANIFOLD_SOLID_BREP('"+name+"',#"+sh+")");
  const rep=E("ADVANCED_BREP_SHAPE_REPRESENTATION('"+name+"',(#"+br+",#"+ax0+"),#"+gctx+")");
  E("SHAPE_DEFINITION_REPRESENTATION(#"+pds+",#"+rep+")");
  const now=new Date().toISOString().slice(0,19);
  return "ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('SV08 carenagem - "+name+"'),'2;1');\nFILE_NAME('"+name+".step','"+now+"',(''),(''),'','','');\nFILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n"+L.join('\n')+"\nENDSEC;\nEND-ISO-10303-21;\n";
}
function meshToStl(pos,idx,off){
  const nt=idx.length/3, buf=new ArrayBuffer(84+50*nt), dv=new DataView(buf); dv.setUint32(80,nt,true); let o=84;
  for(let t=0;t<nt;t++){ o+=12; for(let k=0;k<3;k++){const i=idx[3*t+k]; dv.setFloat32(o,pos[3*i]+off.x,true); dv.setFloat32(o+4,pos[3*i+1]+off.y,true); dv.setFloat32(o+8,pos[3*i+2]+off.z,true); o+=12;} o+=2; }
  return new Uint8Array(buf);
}
const _crcT=(()=>{const t=new Uint32Array(256); for(let n=0;n<256;n++){let c=n; for(let k=0;k<8;k++) c=c&1?0xEDB88320^(c>>>1):c>>>1; t[n]=c>>>0;} return t;})();
function crc32(u8){let c=0xFFFFFFFF; for(let i=0;i<u8.length;i++) c=_crcT[(c^u8[i])&0xFF]^(c>>>8); return (c^0xFFFFFFFF)>>>0;}
function makeZip(files){ // [{name, data:Uint8Array}] metodo "store"
  const enc=new TextEncoder(), parts=[], cen=[]; let off=0;
  for(const fl of files){const nm=enc.encode(fl.name), crc=crc32(fl.data), sz=fl.data.length;
    const h=new DataView(new ArrayBuffer(30)); h.setUint32(0,0x04034b50,true); h.setUint16(4,20,true); h.setUint16(6,0x0800,true); h.setUint16(8,0,true); h.setUint32(14,crc,true); h.setUint32(18,sz,true); h.setUint32(22,sz,true); h.setUint16(26,nm.length,true);
    parts.push(new Uint8Array(h.buffer),nm,fl.data);
    const c=new DataView(new ArrayBuffer(46)); c.setUint32(0,0x02014b50,true); c.setUint16(4,20,true); c.setUint16(6,20,true); c.setUint16(8,0x0800,true); c.setUint32(16,crc,true); c.setUint32(20,sz,true); c.setUint32(24,sz,true); c.setUint16(28,nm.length,true); c.setUint32(42,off,true);
    cen.push(new Uint8Array(c.buffer),nm); off+=30+nm.length+sz;}
  let cs=0; cen.forEach(x=>cs+=x.length);
  const e=new DataView(new ArrayBuffer(22)); e.setUint32(0,0x06054b50,true); e.setUint16(8,files.length,true); e.setUint16(10,files.length,true); e.setUint32(12,cs,true); e.setUint32(16,off,true);
  return new Blob([...parts,...cen,new Uint8Array(e.buffer)],{type:'application/zip'});
}
if(typeof module!=='undefined') module.exports={meshToStep,meshToStl,makeZip};
