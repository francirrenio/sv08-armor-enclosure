import numpy as np
exec(open('geo.py').read())
from shapely.geometry import box as sbox
HF=np.load('frontZ.npy'); pf=pockets(HF,45.0,0.0,0.5,262.5,265.0)
S1=175.0
_ZON=[((S1+1.5,194.0),(40.6,60.8)),((S1+1.5,194.0),(4.4,19.1)),((45.5,S1-1.5),(40.6,60.8)),((45.5,S1-1.5),(4.4,19.1))]
A=[]
for zi,(xr,yr) in enumerate(_ZON):
    clip=sbox(xr[0],yr[0],xr[1],yr[1])
    for p in pf:
        q=p.buffer(-0.4).intersection(clip)
        for g in (q.geoms if hasattr(q,'geoms') else [q]):
            if not g.is_empty and g.area>=25: A.append(g)
def thick(g):
    r=g.minimum_rotated_rectangle; c=np.array(r.exterior.coords)
    e=[np.linalg.norm(c[i+1]-c[i]) for i in range(2)]; return min(e), max(e), g.area/max(e)
KEEP={1,6,7,9,10,16,17,19,20}
for i,g in enumerate(A,1): print(i, i in KEEP, [round(v,1) for v in thick(g)], round(g.area))
H=np.load('sideX_full.npy'); print(H.shape, np.nanmin(H), np.nanmax(H))
