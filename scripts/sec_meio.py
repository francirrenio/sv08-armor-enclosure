import pickle,numpy as np,trimesh,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('load.py').read()); exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb')); FB=pickle.load(open('FB.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
exec(open('latload.py').read())
P={'base':M['Corpo1@071.stl'],'est_meio':RL['est_meio'],'placa_B':RL['placa_B'],'placa_A':RL['placa_A'],'acab_inf':FB['acab_inf'],'mold_d2':FB['moldura_lat_d2'],
   'acril':CT['acrilico_lat'],'verde_c':RL['verde_central']}
C={'base':'#cfc8b8','est_meio':'#555','placa_B':'#222','placa_A':'#222','acab_inf':'#8fa6d9','mold_d2':'#8fa6d9','acril':'#bfe3f5','verde_c':'#3aa857'}
zs=[0.0,60.0,-60.0,120.0]
fig,axs=plt.subplots(1,len(zs),figsize=(18,7))
for ax,z in zip(axs,zs):
    for k,m in P.items():
        try: s=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
        except Exception: s=None
        if s is None: continue
        p2,_=s.to_planar(to_2D=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-z],[0,0,0,1]]),check=False)
        for poly in p2.polygons_full:
            x,y=poly.exterior.xy; ax.fill(x,y,fc=C[k],ec='k',lw=.4,alpha=.85,label=k)
    ax.set_xlim(250,290); ax.set_ylim(60,105); ax.set_aspect('equal'); ax.set_title('Z=%g'%z); ax.grid(alpha=.3)
h,l=axs[0].get_legend_handles_labels(); d=dict(zip(l,h)); axs[0].legend(d.values(),d.keys(),fontsize=7,loc='lower left')
plt.tight_layout(); plt.savefig('sec_meio.png',dpi=80)
