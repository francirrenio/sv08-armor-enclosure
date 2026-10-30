import sys, trimesh, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def shade(m, ax, elev, azim, title):
    tri = m.triangles; n = m.face_normals
    L = np.array([0.4,-0.5,0.8]); L/=np.linalg.norm(L)
    s = 0.35+0.65*np.clip(n@L,0,1)
    pc = Poly3DCollection(tri, facecolors=np.c_[s*0.55,s*0.6,s*0.45,np.ones_like(s)], edgecolor='none')
    ax.add_collection3d(pc)
    b = m.bounds; c=(b[0]+b[1])/2; r=(b[1]-b[0]).max()/2
    ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r)
    ax.view_init(elev, azim); ax.set_title(title); ax.set_axis_off()
def sections(m, axis, vals, ax_list):
    for v, ax in zip(vals, ax_list):
        o = np.zeros(3); nrm = np.zeros(3); nrm[axis]=1; o[axis]=v
        s = m.section(plane_origin=o, plane_normal=nrm)
        if s is None: ax.set_title('vazio %s=%.1f'%('xyz'[axis],v)); continue
        for e in s.discrete:
            idx=[i for i in range(3) if i!=axis]
            ax.plot(e[:,idx[0]], e[:,idx[1]], 'k-', lw=0.8)
        ax.set_aspect('equal'); ax.set_title('corte %s=%.1f'%('xyz'[axis],v)); ax.grid(True, lw=0.3)
m = trimesh.load('stl/d0004228-corner-front-right-x1.stl')
fig = plt.figure(figsize=(16,10))
for i,(e,a) in enumerate([(30,-60),(30,120),(-30,-60),(90,-90)]):
    ax = fig.add_subplot(2,4,i+1, projection='3d'); shade(m, ax, e, a, 'elev %d azim %d'%(e,a))
b=m.bounds
axs=[fig.add_subplot(2,4,5+i) for i in range(4)]
sections(m, 2, [b[0][2]+1, b[0][2]+10, (b[0][2]+b[1][2])/2, b[1][2]-1], axs)
plt.tight_layout(); plt.savefig('corner.png', dpi=70)
p = trimesh.load('stl/b122a6ef-plain-panel-x-4.stl')
fig = plt.figure(figsize=(16,8))
b=p.bounds
axs=[fig.add_subplot(2,4,1+i) for i in range(8)]
sections(p, 0, [b[0][0]+1, b[0][0]+15, (b[0][0]+b[1][0])/2, b[1][0]-15], axs[:4])
sections(p, 2, [b[0][2]+1, b[0][2]+8, (b[0][2]+b[1][2])/2, b[1][2]-1], axs[4:])
plt.tight_layout(); plt.savefig('panel_sec.png', dpi=70)
