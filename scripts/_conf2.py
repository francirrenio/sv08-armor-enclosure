import pickle,numpy as np,trimesh
exec(open('geo.py').read())
m=pickle.load(open('CT.pkl','rb'))['cant_top_F']; m.export('ct_new.stl')
for pid,lab,grp,mm in pickle.load(open('parts.pkl','rb')):
    if pid in ('thCantF','thCantF0','esp1','vsup1') or grp=='atual': continue
    if not (mm.bounds[0]<m.bounds[1]).all() or not (mm.bounds[1]>m.bounds[0]).all(): continue
    try: v=I(m,mm).volume
    except Exception as e: v='nv'
    print(pid,grp,v if isinstance(v,str) else round(v,2))
