import trimesh, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
s=trimesh.load('step/printer.glb'); m=s.to_geometry()
V=m.vertices*1000.0+np.array([68.8,47.7,-111.7]); T=V[m.faces]; N=m.face_normals
def view(name,h,d,light,flip):
    P=T[:,:,[h,1]].copy()
    if flip: P[:,:,0]*=-1
    o=np.argsort(T[:,:,d].mean(1))
    sh=0.30+0.55*np.clip(N@np.array(light),0,1)
    col=np.c_[sh*0.35,sh*0.36,sh*0.40,np.ones_like(sh)]
    fig=plt.figure(figsize=(6.2,6.4),dpi=200); ax=fig.add_axes([0,0,1,1])
    ax.add_collection(PolyCollection(P[o],facecolors=col[o],edgecolors='none'))
    ax.set_xlim(-310,310); ax.set_ylim(-20,620); ax.axis('off')
    fig.savefig(name,dpi=200,transparent=True); plt.close(fig)
view('ghost_front.png',0,2,[0.3,0.4,0.85],False)
view('ghost_side.png',2,0,[0.85,0.4,0.3],False)
print(np.round(V.min(0),1),np.round(V.max(0),1))
