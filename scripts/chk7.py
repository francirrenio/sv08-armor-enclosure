import pickle,numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('geo.py').read())
from shapely.geometry import Polygon
from shapely.ops import unary_union
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
fig,ax=plt.subplots(2,1,figsize=(16,8))
for i,x in enumerate((282.0,283.6)):
  for k,c in (('verde_central','g'),('verde_braco_T','b'),('placa_A','k')):
    for m,ls in ((RL[k],'-'),(CT['R_'+k],'--')):
        s=section_polys(m,'x',x); gs=s.geoms if hasattr(s,'geoms') else [s]
        for g in gs:
            for r in [g.exterior]+list(g.interiors):
                xy=np.array(r.coords); ax[i].plot(xy[:,0],xy[:,1],c+ls,lw=0.6 if ls=='-' else 1.0, color=('r' if ls=='--' else c))
  ax[i].set_xlim(-215,-60); ax[i].set_ylim(0,70); ax[i].set_aspect('equal'); ax[i].set_title(str(x))
plt.savefig('chk7.png',dpi=110,bbox_inches='tight')
