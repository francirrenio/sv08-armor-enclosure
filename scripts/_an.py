import pickle,numpy as np,trimesh
exec(open('geo.py').read())
from shapely.geometry import Polygon,box
from shapely.ops import unary_union as uu
S=pickle.load(open('CT.pkl','rb'))['cant_top_F']
def sy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
for y in (524,530,545,560,578,600,625,633):
    p=sy(S,y); print(y,round(p.area,1),np.round(p.bounds,2).tolist(), p.geom_type)
p=sy(S,578).simplify(0.05)
g=p if p.geom_type=='Polygon' else max(p.geoms,key=lambda q:q.area)
print(np.round(np.array(g.exterior.coords),2).tolist())
def sx(m,x):
    s=m.section(plane_origin=[x,0,0],plane_normal=[1,0,0])
    p2,T=s.to_2D(to_2D=np.array([[0,0,1,0],[0,1,0,0],[1,0,0,-x],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
q=sx(S,260).simplify(0.05); g=q if q.geom_type=='Polygon' else max(q.geoms,key=lambda r:r.area)
print('front wing sec X260 (z,y):',np.round(np.array(g.exterior.coords),2).tolist())
