import pickle,numpy as np,trimesh
exec(open('geo.py').read())
from shapely.geometry import Polygon
S=pickle.load(open('CT.pkl','rb'))['cant_top_F']
prof=Polygon([[281.8,254.0],[284.2,254.0],[284.2,205.0],[287.8,205.0],[293.3,210.5],[293.3,285.33],[283.13,295.5],[239.5,295.5],[234.0,290.0],[234.0,285.5],[234.8,285.5],[236.0,284.3],[236.0,284.15],[281.8,284.15]])
def pxz(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
F=pxz(prof,523.0,633.6)
Z=U(B(287.5,300,500,650,190,300),B(200,300,500,650,289.7,300),HS([285.15,580,285.15],(-1,0,-1)))
cav=I(I(D(F,S),Z),B(200,300,535,622,190,300))
for c in cav.split(only_watertight=False):
    if abs(c.volume)>0.5: print(round(c.volume,1),np.round(c.bounds,2).tolist())
