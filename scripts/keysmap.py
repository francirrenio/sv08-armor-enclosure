import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('geo.py').read())
from shapely.geometry import box as sbox
HF=np.load('frontZ.npy'); pf=pockets(HF,45.0,0.0,0.5,262.5,265.0)
S1=175.0
zones=[((S1+1.5,194.0),(40.6,60.8)),((S1+1.5,194.0),(4.4,19.1)),((45.5,S1-1.5),(40.6,60.8)),((45.5,S1-1.5),(4.4,19.1))]
keys=[]
for xr,yr in zones:
    clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        q=p.buffer(-0.4).intersection(clip)
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if not g.is_empty and g.area>=25: keys.append(g)
fig,ax=plt.subplots(figsize=(17,7))
ax.imshow(np.where(np.isnan(HF),np.nan,HF),origin='lower',extent=[45,270,0,81],cmap='Greys_r',vmin=255,vmax=276,alpha=0.85)
for i,g in enumerate(keys,1):
    xy=np.array(g.exterior.coords); ax.fill(xy[:,0],xy[:,1],fc='#e0402f',ec='k',lw=0.6,alpha=0.85)
    c=g.representative_point(); ax.text(c.x,c.y,str(i),ha='center',va='center',fontsize=11,fontweight='bold',color='white')
ax.axvline(S1,color='#1e6ee6',ls='--',lw=1); ax.text(S1+1,78,'emenda das estruturas X 175',color='#1e6ee6',fontsize=8)
ax.axhspan(19.5,40.5,color='#f2b13c',alpha=0.25); ax.text(50,29,'faixa do LED',fontsize=9,color='#8a5a00')
ax.set_xlim(45,262); ax.set_ylim(0,81); ax.set_aspect('equal'); ax.set_xlabel('X (mm) — vista de frente, sem as placas'); ax.set_ylabel('Y (mm)')
ax.set_title('Apoios da versão anterior (vermelho = encaixe nos bolsos da base), numerados',fontsize=12)
plt.tight_layout(); plt.savefig('apoios_numerados.png',dpi=95)
print(len(keys), [ (i+1, round(g.area), [round(v,1) for v in g.bounds]) for i,g in enumerate(keys)])
