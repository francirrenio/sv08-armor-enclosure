import pickle,numpy as np,trimesh
exec(open('geo.py').read())
from shapely.ops import unary_union as uu
m=trimesh.load('vs.stl')
for x in (283.5,282.5,281.0,280.0):
    p=section_polys(m,'x',x).simplify(0.05)
    for g in (p.geoms if hasattr(p,'geoms') else [p]): print('X',x,'(z,y)',np.round(np.array(g.exterior.coords),1).tolist(), [len(g.interiors)])
def sz(z):
    s=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-z],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
for z in (285.5,284.5,283.5):
    p=sz(z).simplify(0.05)
    for g in (p.geoms if hasattr(p,'geoms') else [p]): print('Z',z,'(x,y)',np.round(np.array(g.exterior.coords),1).tolist())
print('---holes')
for x in (283.5,281.0):
    p=section_polys(m,'x',x)
    for g in (p.geoms if hasattr(p,'geoms') else [p]):
        for r in g.interiors:
            q=np.array(r.coords); print('X',x,'z,y',np.round(q.mean(0),1).tolist(),'d',round(q[:,0].max()-q[:,0].min(),1))
for z in (285.5,283.0):
    p=sz(z)
    for g in (p.geoms if hasattr(p,'geoms') else [p]):
        for r in g.interiors:
            q=np.array(r.coords); print('Z',z,'x,y',np.round(q.mean(0),1).tolist(),'d',round(q[:,0].max()-q[:,0].min(),1))
