import pickle,numpy as np,trimesh
from shapely.geometry import box
from shapely.ops import unary_union as uu
CT=pickle.load(open('CT.pkl','rb')); TL=pickle.load(open('TL.pkl','rb'))
def sy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    if s is None: return None
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
W=box(270,200,290,262)
for y in (520,522.5,524,530,540):
  for k,m in (('vs',CT['verde_sup']),('esp',CT['espinha']),('band',TL['bandaB'])):
    s=sy(m,y)
    if s is None: continue
    s=s.intersection(W)
    if s.is_empty: continue
    for g in (s.geoms if hasattr(s,'geoms') else [s]):
        g=g.simplify(0.05); print(y,k,np.round(np.array(g.exterior.coords),2).tolist())
