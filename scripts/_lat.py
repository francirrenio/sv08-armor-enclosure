import pickle,numpy as np,trimesh
exec(open('geo.py').read())
from shapely.geometry import box
P={pid:(lab,grp,m) for pid,lab,grp,m in pickle.load(open('parts.pkl','rb'))}
W=box(195,470,262,570)
for x in (283.5,282.0,280.0,278.0):
  print('X',x)
  for pid,(lab,grp,m) in P.items():
    if grp=='atual' or m.bounds[0][0]>x or m.bounds[1][0]<x: continue
    s=section_polys(m,'x',x)
    if s is None: continue
    s=s.intersection(W)
    if s.is_empty or s.area<1: continue
    print('  ',pid,grp,round(s.area),np.round(s.bounds,1).tolist())
