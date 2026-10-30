import json, numpy as np, trimesh, manifold3d as mf, collections, time, re
t0=time.time()
def load(dirn, man):
    meshes={}; mans={}
    for i,x in enumerate(man):
        t=trimesh.load(dirn+'/'+x['f'],process=True); t.merge_vertices(digits_vertex=4)
        T=np.array(x['T']).reshape(4,4); T[:3,3]*=10.0; t.apply_transform(T)
        meshes[i]=t
        try:
            m=mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices,np.float32),tri_verts=np.asarray(t.faces,np.uint32)))
            mans[i]=m if m.status()==mf.Error.NoError else None
        except Exception: mans[i]=None
    return meshes,mans
E=json.load(open('aud/manifest.json')); P=json.load(open('audp/manifest.json'))
em,ema=load('aud',E); pm,pma=load('audp',P)
print('loaded',time.time()-t0, 'enc nonmanifold',sum(1 for v in ema.values() if v is None),'prn nonmanifold',sum(1 for v in pma.values() if v is None))
bad=[i for i in range(len(P)) if np.abs(pm[i].bounds.ravel()-np.array(P[i]['bb'])).max()>1.0]
print('printer bbox mismatches',len(bad))
def kind(x):
    a=x['ap']; n=x['body']; o=x['occ']
    if a=='R59_hardware' or re.search(r'M3x|M25_|M3_|porca|parafuso|Ferragem|insert|pino_',n+o,re.I): return 'hw'
    if a=='R59_glass' or re.search(r'acrilico|Acrilico|glass|vidro',n+o.split('+')[-1]): return 'acr'
    if re.search(r'2020|perfil|REF\b|_REF|REFERENCIA',n+o.split('+')[-1]): return 'ref'
    if a in ('R59_led','R59_screen') or re.search(r'Tela|LED_REF|Vedante|vedacao|EPDM',n): return 'other'
    if a=='R59_green' or re.search(r'verde|Verde|green|Green',n): return 'green'
    return 'black'
K=[kind(x) for x in E]
print(collections.Counter(K))
json.dump(K,open('aud_kinds.json','w'))
EB=np.array([em[i].bounds.ravel() for i in range(len(E))]); PB=np.array([pm[i].bounds.ravel() for i in range(len(P))])
def near(a,b,t=0.1): return not (a[3]<b[0]-t or b[3]<a[0]-t or a[4]<b[1]-t or b[4]<a[1]-t or a[5]<b[2]-t or b[5]<a[2]-t)
# 1) overlaps enclosure-enclosure (with volume and duplicate detection)
ov=[]
vol={i:(ema[i].volume() if ema[i] else 0) for i in ema}
for i in range(len(E)):
    if ema[i] is None: continue
    for j in range(i+1,len(E)):
        if ema[j] is None or not near(EB[i],EB[j],0): continue
        v=(ema[i]^ema[j]).volume()
        if v>0.5: ov.append([i,j,round(v,1),round(v/max(1e-6,min(vol[i],vol[j])),3)])
print('overlaps',len(ov),time.time()-t0)
# 2) overlaps enclosure-printer
op=[]
for i in range(len(E)):
    if ema[i] is None: continue
    for j in range(len(P)):
        if pma[j] is None or not near(EB[i],PB[j],0): continue
        v=(ema[i]^pma[j]).volume()
        if v>0.5: op.append([i,j,round(v,1)])
print('enc x printer',len(op),time.time()-t0)
# 3) gantry envelope intrusion
box=mf.Manifold.cube([2*268.4,523.5-81.1,2*273.4]).translate([-268.4,81.1,-273.4])
cols=None
for j in range(len(P)):
    if pma[j] is not None and P[j]['occ'].split('+')[-1].split(':')[0].endswith(('1.20.2','1.20.3','1.20.4','1.20.5.1.1')):
        cols = pma[j] if cols is None else cols+pma[j]
env=box-cols
gi=[]
for i in range(len(E)):
    if ema[i] is None or K[i]=='hw': continue
    b=EB[i]
    if b[3]<-268.4 or b[0]>268.4 or b[4]<81.1 or b[1]>523.5 or b[5]<-273.4 or b[2]>273.4: continue
    v=(ema[i]^env).volume()
    if v>0.5: gi.append([i,round(v,1)])
print('gantry intrusions',len(gi),time.time()-t0)
# 4) contact graph (gap<=0.05) enclosure+printer
N=len(E); adj=collections.defaultdict(set)
for i in range(N):
    if ema[i] is None: continue
    for j in range(i+1,N):
        if ema[j] is None or not near(EB[i],EB[j],0.1): continue
        if ema[i].min_gap(ema[j],0.1)<=0.05: adj[i].add(j); adj[j].add(i)
    for j in range(len(P)):
        if pma[j] is None or not near(EB[i],PB[j],0.1): continue
        if ema[i].min_gap(pma[j],0.1)<=0.05: adj[i].add(('p',j)); 
print('contacts done',time.time()-t0)
anch=[i for i in range(N) if any(isinstance(x,tuple) for x in adj[i])]
seen=set(anch); st=list(anch)
while st:
    a=st.pop()
    for b in adj[a]:
        if isinstance(b,tuple): continue
        if b not in seen: seen.add(b); st.append(b)
floating=[i for i in range(N) if i not in seen and ema[i] is not None]
# fasteners into printer: hw touching printer
hwp=[i for i in anch if K[i]=='hw']
json.dump({'ov':ov,'op':op,'gi':gi,'anch':anch,'floating':floating,'hwp':hwp,'adj':{str(k):[x if not isinstance(x,tuple) else 'p%d'%x[1] for x in v] for k,v in adj.items()}},open('analise_res.json','w'))
print('anchored direct',len(anch),'hw->printer',len(hwp),'floating',len(floating),time.time()-t0)
