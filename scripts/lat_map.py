import numpy as np, pickle, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
G=pickle.load(open('latG.pkl','rb')); H=np.load('sideX_full.npy')
def thin(g):
    r=g.minimum_rotated_rectangle; c=np.array(r.exterior.coords); L=max(np.linalg.norm(c[i+1]-c[i]) for i in range(2)); return g.area/L
fig,ax=plt.subplots(figsize=(24,5.2))
ax.imshow(np.where(H<200,np.nan,H),origin='lower',extent=[-276,276,0,82],cmap='Greys_r',vmin=255,vmax=270,alpha=0.85)
for i,g in enumerate(G,1):
    t=thin(g); xy=np.array(g.exterior.coords)
    ax.fill(xy[:,0],xy[:,1],fc='#e0402f' if t<7.0 else '#999',ec='k',lw=0.6,alpha=0.85)
    c=g.representative_point(); ax.text(c.x,c.y,str(i),ha='center',va='center',fontsize=9,fontweight='bold',color='white')
ax.set_aspect('equal'); ax.set_xlim(-276,276); ax.set_ylim(0,82)
plt.tight_layout(); plt.savefig('lat_map_dbg.png',dpi=80)
