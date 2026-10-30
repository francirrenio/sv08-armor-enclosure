import numpy as np,trimesh
from shapely.ops import unary_union as uu
c=trimesh.load('../ltop/053_fix.stl')
def sz(z):
    s=c.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-z],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
ref=sz(254.0)
for z in np.arange(248,264,1.0):
    p=sz(z); print(z, round(p.area,1), np.round(p.bounds,2).tolist(), round(p.symmetric_difference(ref).area,1), len(p.interiors) if p.geom_type=='Polygon' else p.geom_type)
p=sz(254.0).simplify(0.05)
print(np.round(np.array(p.exterior.coords),2).tolist())
