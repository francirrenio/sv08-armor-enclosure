import trimesh, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
D='/mnt/user-data/uploads/SV08 Eclosure/docs/planos/carenagem/_stl/teste_cantoneira_central/'
S=trimesh.load('/root/.claude/uploads/feeeb77d-0d0c-5101-9504-0705fb8bda2b/50ea2d4a-Teste_cantoneira_suporte_preto.stl')
U=trimesh.load(D+'Teste_cantoneira_verde_superior.stl'); L=trimesh.load(D+'Teste_cantoneira_verde_inferior.stl')
fig,axs=plt.subplots(2,3,figsize=(21,12))
for ax,y in zip(axs.flat,[290,297,301,351,355,362]):
    for mm,c in ((S,'k'),(U,'g'),(L,'b')):
        s=mm.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
        if s is None: continue
        for e in s.discrete: ax.plot(e[:,0],e[:,2],c+'-',lw=0.8)
    ax.set_aspect('equal'); ax.set_title(f'Y={y}'); ax.grid(True,lw=0.3); ax.set_xlim(233,285); ax.set_ylim(248,288)
plt.tight_layout(); plt.savefig('secG.png',dpi=55)
fig,axs=plt.subplots(1,3,figsize=(21,6))
for ax,x in zip(axs.flat,[240,250,265]):
    for mm,c in ((S,'k'),(U,'g'),(L,'b')):
        s=mm.section(plane_origin=[x,0,0],plane_normal=[1,0,0])
        if s is None: continue
        for e in s.discrete: ax.plot(e[:,1],e[:,2],c+'-',lw=0.8)
    ax.set_aspect('equal'); ax.set_title(f'X={x}'); ax.grid(True,lw=0.3); ax.set_ylim(248,288)
plt.tight_layout(); plt.savefig('secGX.png',dpi=55)
