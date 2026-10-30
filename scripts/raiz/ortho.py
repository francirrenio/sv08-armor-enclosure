import trimesh, numpy as np, matplotlib, sys
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
s=trimesh.load('step/printer.glb'); m=s.to_geometry()
V=m.vertices*1000.0; V=V+np.array([68.8,47.7,-111.7])
T=V[m.faces]; N=m.face_normals
def view(name, h, v, d, sign, light):
    P=T[:,:,[h,v]].copy()
    if h==2 and sign<0: pass
    depth=T[:,:,d].mean(1)*sign
    o=np.argsort(depth)
    sh=0.35+0.6*np.clip(N@np.array(light),0,1)
    col=np.c_[sh*0.62,sh*0.63,sh*0.66]
    fig=plt.figure(figsize=(6.2,6.4),dpi=100); ax=fig.add_axes([0,0,1,1])
    ax.add_collection(PolyCollection(P[o],facecolors=col[o],edgecolors='none'))
    ax.set_xlim(-310,310); ax.set_ylim(-20,620); ax.set_aspect('equal'); ax.axis('off')
    if (h==0 and sign<0) or (h==2 and sign<0): ax.invert_xaxis()
    fig.savefig(name,dpi=100); plt.close(fig)
view('front_zpos.png',0,1,2, 1,[0.3,0.4,0.85])
view('front_zneg.png',0,1,2,-1,[0.3,0.4,-0.85])
view('side_xpos.png',2,1,0, 1,[0.85,0.4,0.3])
print('ok')
