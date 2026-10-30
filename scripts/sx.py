import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('load.py').read())
COL={'Corpo1@071.stl':'#d9d4c7','Corpo1@072.stl':'#c9ced4','10_chassis_3_1':'#963cc8','10_chassis_2_1':'#5a5a5a','10_chassis_2_2':'#3d3d3d','LED_REFERENCIA':'#f5b041','Regua_baixo_central_mod':'#6b8e23','SV-30-03c soleira (degrau) (2 de 2)':'#9ad','SV-30-03c soleira (degrau) (1 de 2)':'#9ad','65_suporte_P01_D':'#888888','21_lateral_chassis_2_D':'#f08c14','SV-30-01a moldura (1 de 2)':'#c8a2e0','SV-30-01b acrilico 225x453':'#bfe3f5','SV-30-01c vedacao EPDM 8x2':'#e33','SV-30-03a batente lateral D (1 de 3)':'#666','SV08_Espinha_L_FD_Black':'#1e6ee6','Moldura_LED_D_mod':'#3a3'}
Xs=[float(a) for a in sys.argv[1].split(',')]; out=sys.argv[2]; lim=[float(a) for a in sys.argv[3].split(',')]
fig,axs=plt.subplots(1,len(Xs),figsize=(7*len(Xs),7))
for ax,x in zip(np.atleast_1d(axs),Xs):
    for k,c in COL.items():
        if k not in M: continue
        m=M[k]
        if not (m.bounds[0][0]<x<m.bounds[1][0]): continue
        s=m.section(plane_origin=[x,0,0],plane_normal=[1,0,0])
        if s is None: continue
        for e in s.discrete: ax.fill(e[:,2],e[:,1],fc=c,ec='k',lw=0.4,alpha=0.85)
    ax.set_xlim(lim[0],lim[1]); ax.set_ylim(lim[2],lim[3]); ax.set_aspect('equal'); ax.grid(lw=0.2); ax.set_title('X=%g (Z horizontal, Y vertical)'%x); ax.set_xlabel('Z'); ax.set_ylabel('Y')
from matplotlib.patches import Patch
fig.legend(handles=[Patch(fc=c,label=k[:30]) for k,c in COL.items()],loc='lower center',ncol=6,fontsize=8)
plt.tight_layout(rect=[0,0.07,1,1]); plt.savefig(out,dpi=90)
