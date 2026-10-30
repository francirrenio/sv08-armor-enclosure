import trimesh, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
m = trimesh.load('/root/.claude/uploads/feeeb77d-0d0c-5101-9504-0705fb8bda2b/50ea2d4a-Teste_cantoneira_suporte_preto.stl')
b=m.bounds
def secs(axis, vals, fn):
    fig,axs=plt.subplots(2,(len(vals)+1)//2,figsize=(20,9))
    for ax,val in zip(axs.flat,vals):
        o=[0,0,0];o[axis]=val;nrm=[0,0,0];nrm[axis]=1
        s=m.section(plane_origin=o,plane_normal=nrm)
        if s is None: ax.set_title(f'{val} none');continue
        idx=[i for i in range(3) if i!=axis]
        for e in s.discrete:
            ax.plot(e[:,idx[0]],e[:,idx[1]],'k-',lw=0.8)
        ax.set_aspect('equal');ax.set_title(f'{"XYZ"[axis]}={val:.1f}  h:{"XYZ"[idx[0]]} v:{"XYZ"[idx[1]]}');ax.grid(True,lw=0.3)
    plt.tight_layout();plt.savefig(fn,dpi=60)
secs(1,[287,292,300,310,326,340,352,360,365],'secY.png')
secs(2,[225,230,240,255,270,280,284,286],'secZ.png')
secs(0,[236,240,250,260,270,276,279],'secX.png')
