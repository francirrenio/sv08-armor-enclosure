import pickle,numpy as np
from shapely.geometry import Point
CT=pickle.load(open('CT.pkl','rb')); PG,PN=pickle.load(open('cv2d.pkl','rb'))
m=CT['R_verde_central']; pn=PN['verde_central']; inner=pn.buffer(-1.05)
zz,yy=np.meshgrid(np.arange(-80,-55,0.1),np.arange(50,66,0.1)); pts=np.c_[zz.ravel(),yy.ravel()]
sel=np.array([inner.contains(Point(p)) for p in pts]); pts=pts[sel]
for x in (283.79,283.7,283.0):
    c=m.contains(np.c_[np.full(len(pts),x),pts[:,1],pts[:,0]]); print(x,len(pts),(~c).sum(), pts[~c][:5])
import trimesh
a=m.area_faces; print('faces',len(a),'tiny',(a<1e-6).sum(), 'broken',len(trimesh.repair.broken_faces(m)))
