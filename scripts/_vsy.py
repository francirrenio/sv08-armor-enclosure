import pickle,numpy as np,trimesh
from shapely.ops import unary_union as uu
m=trimesh.load('vs.stl'); CF=pickle.load(open('CF.pkl','rb'))
def sy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
for y in (340,420,470,500,530,545,553,557):
    p=sy(m,y).simplify(0.03)
    for g in (p.geoms if hasattr(p,'geoms') else [p]): print(y,round(g.area,1),np.round(np.array(g.exterior.coords),2).tolist(),len(g.interiors))
p=sy(CF['verde_72'],300).simplify(0.03); print('v72@300',np.round(np.array(p.exterior.coords),2).tolist())
