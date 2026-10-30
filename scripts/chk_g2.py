import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('esb/geom_lat_v2.py').read())
from shapely.geometry import Point
fig,ax=plt.subplots(figsize=(15,4))
def dr(p,c,lw=1):
    for g in (p.geoms if hasattr(p,'geoms') else [p]):
        for r in [g.exterior]+list(g.interiors):
            a=np.array(r.coords); ax.plot(a[:,0],a[:,1],c,lw=lw)
for k,p in NG.items(): dr(p,'g')
dr(Lr,'k'); dr(M(Lr),'k')
for i in ILHAS: dr(i,'b',0.6)
for g in GRADES: dr(g,'b',0.5)
for z,y in SC: ax.plot(z,y,'ro',ms=4)
for y,z in HID: ax.plot(z,y,'mx',ms=6)
ax.set_aspect('equal'); ax.set_xlim(-280,280); ax.set_ylim(0,70)
plt.savefig('chk_g2.png',dpi=110,bbox_inches='tight')
print({k:[round(b,1) for b in p.bounds] for k,p in NG.items()})
print('min dist entre verdes', round(min(NG[a].distance(NG[b]) for a in NG for b in NG if a<b),2), 'asa-cant',round(NG['verde_asa_F'].distance(Lr),2), 'sup-cant',round(NG['verde_sup_F'].distance(Lr),2))
for z,y in SC:
    p=[q for q in NG.values() if q.contains(Point(z,y))]
    print('SC',round(z,1),round(y,1),'borda',round(p[0].exterior.distance(Point(z,y)) if p else -1,1), 'furo',round(min([Polygon(r).exterior.distance(Point(z,y)) for r in p[0].interiors] or [99]),1) if p else '')
for y,z in HID:
    p=[q for q in NG.values() if q.buffer(0.5).contains(Point(z,y).buffer(3.1))]
    print('HID',y,round(z,1),'coberto' if p else 'EXPOSTO')
