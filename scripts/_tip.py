import pickle,numpy as np,trimesh
from shapely.ops import unary_union as uu
m=trimesh.load('ct_new.stl')
def sx(x):
    s=m.section(plane_origin=[x,0,0],plane_normal=[1,0,0])
    p2,T=s.to_2D(to_2D=np.array([[0,0,1,0],[0,1,0,0],[1,0,0,-x],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
for x in (236,238,242,250):
    q=sx(x).simplify(0.05)
    for g in (q.geoms if hasattr(q,'geoms') else [q]):
        c=np.round(np.array(g.exterior.coords),2); c=c[c[:,1]<545]; print(x, c.tolist())
