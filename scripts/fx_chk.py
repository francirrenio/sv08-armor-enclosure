import pickle,trimesh,numpy as np,json,glob
exec(open('geo.py').read()); exec(open('load.py').read())
parts=pickle.load(open('parts.pkl','rb'))
T='../ltop/'
lat={}
def grp(prefix,files):
    lat[prefix]=[trimesh.load(T+f) for f in files]
lat['fr430']=[trimesh.load(T+'%03d.stl'%i) for i in range(11,19)]
lat['tr430']=[trimesh.load(T+'%03d.stl'%i) for i in range(19,27)]
lat['topo']=[trimesh.load(T+'%03d.stl'%i) for i in range(27,35)]
lat['fr190']=[M[k] for k in M if 'fecho D frente Y190' in k]
def mz(m):
    q=m.copy(); q.apply_transform(np.diag([1,1,-1,1])); 
    if q.volume<0: q.invert()
    return q
lat['tr190']=[mz(m) for m in lat['fr190']]
hin={}
for y in (150,450):
    hin['D%d'%y]=[trimesh.load('../hingeW/SV-30-05%s_D%d.stl'%(c,y)) for c in 'abc']
res={}
def vol(a,b):
    try:
        if not a.is_volume: a=a.convex_hull
        if not b.is_volume: return -1
        return I(a,b).volume
    except Exception as e: return -2
for nm,ms in list(lat.items())+list(hin.items()):
    for j,m in enumerate(ms):
        for pid,label,g,pm in parts:
            if g not in ('prop','comum'): continue
            if np.any(m.bounds[0]>pm.bounds[1]+0.01) or np.any(m.bounds[1]<pm.bounds[0]-0.01): continue
            v=vol(m,pm)
            if v!=0: res.setdefault(nm,[]).append((j,pid,round(float(v),1)))
for k,v in res.items(): print(k,v)
pickle.dump((lat,hin),open('fx_src.pkl','wb'))
