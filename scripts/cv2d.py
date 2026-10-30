import pickle,numpy as np
exec(open('geo.py').read())
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
RL=pickle.load(open('RL.pkl','rb'))
R=6.0; GAP=1.0; FOLGA=0.6
def contorno(m,x=281.5):
    s=section_polys(m,'x',x); gs=s.geoms if hasattr(s,'geoms') else [s]
    return max([Polygon(g.exterior) for g in gs],key=lambda p:p.area)
def opening(p,r): return p.buffer(-r,join_style=1).buffer(r,join_style=1)
def closing(p,r): return p.buffer(r,join_style=1).buffer(-r,join_style=1)
PG={k:contorno(RL[k]) for k in ('verde_central','verde_braco_T','verde_braco_F','verde_lat_T_inf','verde_lat_F_inf','verde_lat_T_sup','verde_lat_F_sup')}
PN={}
PN['verde_central']=opening(PG['verde_central'],R)
for k in ('verde_braco_T','verde_braco_F'):
    a=closing(PG[k],R+GAP)
    a=a.difference(PN['verde_central'].buffer(GAP,join_style=1))
    PN[k]=opening(a,R)
for k in ('verde_lat_T_inf','verde_lat_F_inf','verde_lat_T_sup','verde_lat_F_sup'): PN[k]=PG[k]
pickle.dump((PG,PN),open('cv2d.pkl','wb'))
if __name__=='__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig,ax=plt.subplots(2,1,figsize=(16,8))
    cav=closing(unary_union([p.buffer(FOLGA,join_style=1) for p in PN.values()]),1.5)
    for i,(lo,hi) in enumerate(((-215,-60),(-100,-60))):
        for k in PG:
            for p,c in ((PG[k],'0.6'),(PN[k],'g')):
                xy=np.array(p.exterior.coords); ax[i].plot(xy[:,0],xy[:,1],color=c,lw=0.8)
        for g in (cav.geoms if hasattr(cav,'geoms') else [cav]):
            xy=np.array(g.exterior.coords); ax[i].plot(xy[:,0],xy[:,1],'k--',lw=0.6)
        ax[i].set_xlim(lo,hi); ax[i].set_ylim(0,70); ax[i].set_aspect('equal')
    plt.savefig('cv2d.png',dpi=110,bbox_inches='tight')
    for k in PN: print(k, round(PG[k].area,1), round(PN[k].area,1), PN[k].geom_type)
