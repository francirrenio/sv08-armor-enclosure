import pickle,numpy as np,trimesh,os
exec(open('load.py').read()); exec(open('geo.py').read()); exec(open('latload.py').read())
src={}
for f in ('CT','TL','FB','RL','R5','CF','P','Q'):
    if os.path.exists(f+'.pkl'):
        d=pickle.load(open(f+'.pkl','rb'))
        for k,v in d.items():
            if hasattr(v,'bounds'): src[f+':'+k]=v
for k,v in M.items(): src['M:'+k]=v
for k,v in L.items(): src['L:'+k]=v
TD_=None
lo=np.array([-240,520,255]); hi=np.array([240,645,300])
for k,v in src.items():
    try: b=v.bounds
    except Exception: continue
    if b is None: continue
    if np.all(b[1]>lo) and np.all(b[0]<hi):
        print(k,np.round(b,1).tolist())
