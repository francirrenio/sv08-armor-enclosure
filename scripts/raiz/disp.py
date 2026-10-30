import trimesh, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
s=trimesh.load('step/printer.glb'); m=s.to_geometry()
m.apply_scale(1000.0); m.apply_translation([68.8,47.7,-111.7])
# crop region near front base center
c=m.triangles_center
sel=(np.abs(c[:,0])<90)&(c[:,1]<90)&(c[:,2]>200)
sub=m.submesh([np.where(sel)[0]],append=True)
print('sub faces',len(sub.faces),'bounds',np.round(sub.bounds,1).tolist())
T=sub.triangles; N=sub.face_normals
o=np.argsort(T[:,:,2].mean(1))
sh=0.3+0.65*np.clip(N@np.array([0.3,0.4,0.85]),0,1)
fig=plt.figure(figsize=(9,5),dpi=110); ax=fig.add_axes([0.06,0.08,0.92,0.9])
ax.add_collection(PolyCollection(T[o][:,:,:2],facecolors=np.c_[sh,sh,sh][o]*0.8,edgecolors='none'))
ax.set_xlim(-90,90); ax.set_ylim(0,90); ax.set_aspect('equal'); ax.grid(True,lw=0.3); ax.set_xticks(range(-90,91,10)); ax.set_yticks(range(0,91,10))
fig.savefig('disp_front.png'); plt.close(fig)
# sections at x through hooks and at y
fig,axs=plt.subplots(1,3,figsize=(15,5))
for ax,(ax_i,val) in zip(axs,[(0,-30),(0,30),(1,50)]):
    o_=np.zeros(3); n=np.zeros(3); n[ax_i]=1; o_[ax_i]=val
    sec=sub.section(plane_origin=o_,plane_normal=n)
    if sec is not None:
        idx=[2,1] if ax_i==0 else [0,2]
        for e in sec.discrete: ax.plot(e[:,idx[0]],e[:,idx[1]],'k-',lw=0.7)
    ax.set_aspect('equal'); ax.grid(True,lw=0.3); ax.set_title('%s=%g'%('xyz'[ax_i],val))
fig.savefig('disp_sec.png',dpi=90)
