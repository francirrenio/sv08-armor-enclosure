import trimesh, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def sec(m, axis, v, ax, xl=None):
    o=np.zeros(3); n=np.zeros(3); n[axis]=1; o[axis]=v
    s=m.section(plane_origin=o, plane_normal=n)
    idx=[i for i in range(3) if i!=axis]
    if s is not None:
        for e in s.discrete: ax.plot(e[:,idx[0]], e[:,idx[1]], 'k-', lw=0.7)
    ax.set_aspect('equal'); ax.set_title('%s=%.1f'%('xyz'[axis],v), fontsize=9); ax.grid(True, lw=0.3)
    if xl: ax.set_xlim(*xl)
m=trimesh.load('stl/d0004228-corner-front-right-x1.stl')
fig,axs=plt.subplots(2,4,figsize=(16,9)); axs=axs.ravel()
for ax,z in zip(axs,[-4.0,-1.0,0.5,2,12,45,56,60]): sec(m,2,z,ax)
plt.tight_layout(); plt.savefig('corner_z.png',dpi=65)
fig,axs=plt.subplots(1,4,figsize=(16,6))
for ax,x in zip(axs,[460,490,525,532]): sec(m,0,x,ax)
plt.tight_layout(); plt.savefig('corner_x.png',dpi=65)
p=trimesh.load('stl/b122a6ef-plain-panel-x-4.stl')
fig,axs=plt.subplots(4,1,figsize=(16,8))
for ax,z in zip(axs,[-4.0,0.5,45,58]): sec(p,2,z,ax,(60,200))
plt.tight_layout(); plt.savefig('panel_z.png',dpi=65)
# vertical through-holes: rays downward on grid
for name,mm in (('corner',m),('panel',p)):
    b=mm.bounds; xs=np.arange(b[0][0],b[1][0],1.0); ys=np.arange(b[0][1],b[1][1],1.0)
    X,Y=np.meshgrid(xs,ys); org=np.c_[X.ravel(),Y.ravel(),np.full(X.size,b[1][2]+5)]
    dirs=np.tile([0,0,-1.0],(len(org),1))
    hit=mm.ray.intersects_any(org,dirs)
    print(name,'grid',X.shape,'no-hit cells inside footprint (approx holes)', (~hit).sum())
