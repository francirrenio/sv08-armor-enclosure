# Lista de ferragens a partir das pecas da proposta (grupo prop do visualizador, inclui os espelhos _E).
# Cada corpo das pecas de ferragem e classificado pela geometria (aneis de vertices ao longo do eixo principal):
# parafuso (diametro, comprimento nominal, tipo de cabeca, porca junto), porca, inserto, pino, cabeca solta, corpo solto.
# Externo = a cabeca e vista de fora: um raio saindo da cabeca para fora (sentido ponta -> cabeca) nao bate em nenhuma peca.
import pickle,numpy as np,trimesh,json,collections
L=pickle.load(open('parts.pkl','rb'))
HWIDS={'tcHW','tbHW','trHW','tnT','exHW','pfFchHW','pfHW','u_hwCapa','u_fixesp','fixesp','u_hwcol','u_acHW','u_fechosHW','u_tcHW','u_pfHW','u_pfFchHW','u_dobrHW','u_portaHW','u_portaIns','u_portaHWcD','u_portaHWcE','u_hw2020','tnF','tnL','tfHW','hwCapa','hwRiser','hwTopo','bandaPin','apHW','acHW','hwcol','portaHW','portaIns','portaHWcD','portaHWcE','dobrHW','fechosHW','hw1'}
isHW=lambda p: p[2]=='prop' and (p[0][:-2] if p[0].endswith('_E') else p[0]) in HWIDS
HW=[p for p in L if isHW(p)]
BLK=[p[3] for p in L if p[2] in ('prop','ref','comum') and not isHW(p) and len(p[3].faces)]
scene=trimesh.util.concatenate(BLK)
RI=trimesh.ray.ray_triangle.RayMeshIntersector(scene)
STD=[2,3,4,5,6,8,10,12,14,16,18,20,22,25,30]
def rings(c):
    v=c.vertices; ctr=v.mean(0); u,s,vt=np.linalg.svd(v-ctr,full_matrices=False); ax=vt[0]
    k=np.argmax(np.abs(ax))
    if abs(ax[k])>0.97: ax=np.eye(3)[k]*np.sign(ax[k])
    t=(v-ctr)@ax; r=np.linalg.norm((v-ctr)-np.outer(t,ax),axis=1)
    g=collections.defaultdict(float)
    for ti,ri in zip(np.round(t,1),r): g[ti]=max(g[ti],ri)
    R=sorted((ti,round(2*ri,2)) for ti,ri in g.items())
    return ctr,ax,R
def classify(c):
    e=sorted(c.extents)[::-1]
    ctr,ax,R=rings(c); Lt=R[-1][0]-R[0][0]; dmax=max(d for _,d in R)
    if e[0]<5.6 and 4.0<=e[1]<=4.9 and e[2]>=3.8: return dict(k='inserto M3',ctr=ctr)
    if e[0]>12 and e[1]<3.2 and abs(e[1]-e[2])<0.3 and dmax>3.6: return dict(k='pino 3x3',L=round(e[0]),ctr=ctr)
    if e[2]<=2.6 and 6.0<=e[0]<=6.6 and 5.3<=e[1]<=5.7: return dict(k='porca M3',ctr=ctr)
    if e[0]<=6.1 and e[2]<=3.2 and e[1]>=5.0: return dict(k='cabeca',d=e[0],ctr=ctr,ax=None,R=None)
    if Lt<=3.2 and dmax>=5.0: return dict(k='cabeca',d=dmax,ctr=ctr,ax=ax,R=R)
    v=c.vertices; t=(v-ctr)@ax; r=np.linalg.norm((v-ctr)-np.outer(t,ax),axis=1)
    rr=r[r>0.6]; shank=round(2*rr.min(),1) if len(rr) else 0
    endA=2*r[t<t.min()+0.06].max(); endB=2*r[t>t.max()-0.06].max()
    nutlike=lambda d: 6.2<=d<=6.8 or d>=10.5
    headlike=lambda d: any(abs(d-h)<0.3 for h in (4.0,5.5,5.7,6.0,8.5))
    if nutlike(endA) and not nutlike(endB): headB=True
    elif nutlike(endB) and not nutlike(endA): headB=False
    elif headlike(endA) and not headlike(endB): headB=False
    elif headlike(endB) and not headlike(endA): headB=True
    else: headB=endB>=endA
    if not headB: t=-t; ax=-ax
    th=t.max(); tt=t.min(); Lt=th-tt
    if 2*r[t>th-0.06].max()<shank+0.4: return dict(k='corpo',d=shank,L=Lt,ctr=ctr,ax=ax,tip=tt,head=th)
    hd=round(2*r[t>th-0.06].max(),2)
    near=(t>th-6.0)&(np.abs(2*r-hd)<0.3)
    head_h=th-t[near].min()
    nutz=(t<th-head_h-0.5)&(r>shank/2+0.25)
    nd=2*r[nutz].max() if nutz.any() else 0
    nut='porca T 2020 M5' if nd>=10.5 else ('porca M3' if 6.0<=nd<=6.8 else None)
    if head_h<0.3: hk='escareada (DIN 7991)'; nom=Lt
    else:
        nom=Lt-head_h
        HK={5.5:'cilindrica (DIN 912)',5.7:'abaulada (ISO 7380)',6.0:'escareada (DIN 7991)',8.5:'cilindrica (DIN 912)',4.0:'cilindrica'}
        k=min(HK,key=lambda q:abs(q-hd)); hk=HK[k] if abs(k-hd)<0.35 else 'cabeca %.1f'%hd
    M={2.0:'M2',2.5:'M2.5',3.0:'M3',4.0:'M4',5.0:'M5'}; mk=min(M,key=lambda q:abs(q-shank))
    return dict(k='parafuso',M=M[mk],nom=max(q for q in STD if q<=nom+0.6),raw=round(nom,2),hd=hd,hh=round(head_h,2),sh=shank,hk=hk,nut=nut,ctr=ctr,ax=ax,ph=ctr+ax*th)
rows=[]; loose_heads=[]; loose_bodies=[]
for pid,lab,g,m in HW:
    for c in m.split(only_watertight=False):
        if len(c.faces)<8 or abs(c.volume)<0.5: continue
        d=classify(c); d['pid']=pid; d['lab']=lab
        if d['k']=='cabeca': loose_heads.append(d); continue
        if d['k']=='corpo': loose_bodies.append(d); continue
        rows.append(d)
# junta cabecas soltas com corpos soltos (mesma peca, cabeca encostada na ponta do corpo)
for b in loose_bodies:
    best=None
    for h in loose_heads:
        if h['pid']!=b['pid'] or h.get('used'): continue
        for end,sgn in ((b['tip'],-1),(b['head'],1)):
            p=b['ctr']+b['ax']*end; dd=np.linalg.norm(h['ctr']-p)
            if dd<3.5 and (best is None or dd<best[0]): best=(dd,h,end,sgn)
    if best:
        dd,h,end,sgn=best; h['used']=True
        ax=b['ax'] if end==b['head'] else -b['ax']
        L_=b['L']; hk={5.7:'abaulada (ISO 7380)',5.5:'cilindrica (DIN 912)',6.0:'escareada (DIN 7991)'}
        k=min(hk,key=lambda k:abs(k-h['d']))
        rows.append(dict(k='parafuso',M='M3' if abs(b['d']-3)<0.3 else 'M%.1f'%b['d'],nom=min(STD,key=lambda s:abs(s-L_)),raw=round(L_,2),hk=hk[k],nut=None,ctr=b['ctr'],ax=ax,ph=b['ctr']+b['ax']*end,pid=b['pid'],lab=b['lab']))
    else:
        rows.append(dict(k='corpo sem cabeca',d=b['d'],L=round(b['L'],1),pid=b['pid'],lab=b['lab'],ctr=b['ctr']))
for h in loose_heads:
    if not h.get('used'): rows.append(dict(k='cabeca sem corpo',d=h['d'],pid=h['pid'],lab=h['lab'],ctr=h['ctr']))
# externo / interno
for r in rows:
    if r['k']!='parafuso': continue
    o=r['ph']+r['ax']*0.4
    hit=RI.intersects_any([o],[r['ax']])[0]
    r['ext']= not hit
pickle.dump(rows,open('bom_rows.pkl','wb'))
cnt=collections.Counter()
for r in rows:
    if r['k']=='parafuso': cnt[('EXT' if r['ext'] else 'INT',r['M'],r['nom'],r['hk'],r['nut'] or '')]+=1
    else: cnt[(r['k'],r.get('d',''),r.get('L',''))]+=1
for k,v in sorted(cnt.items(),key=lambda kv:str(kv[0])): print(v,k)
print('pecas por pid (parafusos):')
by=collections.defaultdict(collections.Counter)
for r in rows:
    if r['k']=='parafuso': by[r['pid']][('EXT' if r['ext'] else 'INT',r['M'],r['nom'],r['hk'][:4],(r['nut'] or '')[:6])]+=1
    else: by[r['pid']][(r['k'],)]+=1
for pid,c in by.items(): print(pid,dict(c))
