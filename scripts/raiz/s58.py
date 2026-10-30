import trimesh, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
m=trimesh.load('/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/coluna_frontal_D/_mundo/58_coluna_inferior_lateral_frontal_D_interna.stl')
print(np.round(m.bounds,2).tolist(), round(m.volume,1))
ys=[85,100,120,138,150,180,200,240,260,280,290,294]
fig,axs=plt.subplots(3,4,figsize=(20,15))
for ax,y in zip(axs.flat,ys):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    if s is None: ax.set_title(f'Y={y} none'); continue
    for e in s.discrete: ax.plot(e[:,0],e[:,2],'k-',lw=1)
    ax.set_aspect('equal'); ax.set_title(f'Y={y}  (h:X, v:Z)'); ax.grid(True,lw=.3); ax.set_xlim(262,286); ax.set_ylim(222,278)
plt.tight_layout(); plt.savefig('s58Y.png',dpi=55)
fig,axs=plt.subplots(1,6,figsize=(24,8))
for ax,x in zip(axs.flat,[266,268,271,274,277,282]):
    s=m.section(plane_origin=[x,0,0],plane_normal=[1,0,0])
    if s is None: ax.set_title(f'X={x} none'); continue
    for e in s.discrete: ax.plot(e[:,2],e[:,1],'k-',lw=1)
    ax.set_aspect('equal'); ax.set_title(f'X={x} (h:Z, v:Y)'); ax.grid(True,lw=.3)
plt.tight_layout(); plt.savefig('s58X.png',dpi=55)
