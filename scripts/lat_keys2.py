import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('geo.py').read())
from shapely.geometry import box as sbox
H=np.load('sideX_full.npy')
vals,cnt=np.unique(np.round(H[H>200]),return_counts=True); print(list(zip(vals,cnt)))
ps=pockets(H,-276.0,0.0,0.5,257.5,260.0)
def thin(g):
    r=g.minimum_rotated_rectangle; c=np.array(r.exterior.coords); L=max(np.linalg.norm(c[i+1]-c[i]) for i in range(2)); return g.area/L
G=[]
for p in ps:
    q=p.buffer(-0.4)
    for g in (q.geoms if hasattr(q,'geoms') else [q]):
        if not g.is_empty and g.area>=25: G.append(g)
G.sort(key=lambda g:(-g.centroid.y//20, g.centroid.x))
for i,g in enumerate(G,1): print(i, round(thin(g),1), round(g.area), [round(v,1) for v in g.bounds])
import pickle; pickle.dump(G,open('latG.pkl','wb'))
