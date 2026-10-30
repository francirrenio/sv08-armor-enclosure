import numpy as np, pickle, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
G=pickle.load(open('latG.pkl','rb')); H=np.load('sideX_full.npy')
KEEPL={4,6,8,10,15,17,22,24,27,31,35,37,39,41}
fig,ax=plt.subplots(figsize=(22,5.4))
ax.imshow(np.where(H<200,np.nan,H),origin='lower',extent=[-276,276,0,82],cmap='Greys_r',vmin=255,vmax=270,alpha=0.85)
for i,g in enumerate(G,1):
    xy=np.array(g.exterior.coords); k=i in KEEPL
    ax.fill(xy[:,0],xy[:,1],fc='#e0402f' if k else '#b9bcbf',ec='k',lw=0.6,alpha=0.9)
    c=g.representative_point(); ax.text(c.x,c.y,str(i),ha='center',va='center',fontsize=9,fontweight='bold',color='white' if k else '#333')
for z in (-145,145): ax.axvline(z,color='#1e6ee6',ls='--',lw=1); ax.text(z+1.5,76,'emenda Z %+d'%z,color='#1e6ee6',fontsize=8)
for z,yy in ((-220,18),(220,18)): ax.plot(z,yy,'o',mfc='none',mec='#1e6ee6',ms=9); ax.text(z+4,yy-6,'M3 na base',color='#1e6ee6',fontsize=8)
ax.set_aspect('equal'); ax.set_xlim(-276,276); ax.set_ylim(0,82)
ax.set_xlabel('Z (mm) — lateral direita vista de fora, sem placas (esquerda = fundo, direita = frente)'); ax.set_ylabel('Y (mm)')
ax.set_title('Apoios da lateral: vermelho = fica (tiras finas, mesma regra da frente) · cinza = sai',fontsize=12)
ax.legend(handles=[Patch(fc='#e0402f',label='fica'),Patch(fc='#b9bcbf',label='sai')],loc='lower right',fontsize=9)
plt.tight_layout(); plt.savefig('apoios_lateral.png',dpi=90)
