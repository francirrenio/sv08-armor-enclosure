import pickle,numpy as np,trimesh,glob,os
exec(open('geo.py').read())
DS=pickle.load(open('DS.pkl','rb')); CT=pickle.load(open('CT.pkl','rb')); TF=pickle.load(open('TF.pkl','rb')); TL=pickle.load(open('TL.pkl','rb'))
TD_='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
O={}
for k,v in CT.items():
    if hasattr(v,'bounds') and v.bounds is not None and v.bounds[1][1]>500: O['CT:'+k]=v
for k,v in TF.items(): O['TF:'+k]=v
for k,v in TL.items():
    if hasattr(v,'bounds') and v.bounds[1][1]>500: O['TL:'+k]=v
for f in sorted(glob.glob(TD_+'*.stl')):
    m=trimesh.load(f)
    if m.bounds[1][1]>500: O['T:'+os.path.basename(f)]=m
def esp(m):
    q=m.copy(); q.apply_transform(np.diag([-1,1,1,1])); 
    if q.volume<0: q.invert()
    return q
O2=dict(O)
for k,v in O.items():
    if k.startswith(('CT:','TL:')): O2[k+'(E)']=esp(v)
S=pickle.load(open('SUPT.pkl','rb'))
O2['DS:frame']=DS['frame2020']; O2['DS:slider']=DS['slider']
for part in ('lat52','lat55','hw_lat'):
    a=S[part]
    for k,v in O2.items():
        b=v.bounds; 
        if np.any(b[0]>a.bounds[1]) or np.any(b[1]<a.bounds[0]): continue
        try: x=I(a,v).volume
        except Exception as e:
            # malha nao volumetrica: conta vertices dentro
            x='nv:%d'%int(a.contains(v.vertices).sum()) if a.is_volume else 'err'
        if x!=0 and (not isinstance(x,float) or x>0.01): print(part,'x',k,x if not isinstance(x,float) else round(x,1), np.round(v.bounds,1).tolist())
print('fim')
