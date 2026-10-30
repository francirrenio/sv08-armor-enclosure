import pickle,numpy as np
exec(open('geo.py').read())
from shapely.geometry import Polygon
from shapely.ops import unary_union
RL=pickle.load(open('RL.pkl','rb'))
for k in ('verde_central','verde_braco_T'):
  for x in (281.5,283.0):
    s=section_polys(RL[k],'x',x); gs=s.geoms if hasattr(s,'geoms') else [s]
    pg=unary_union([Polygon(g.exterior) for g in gs]).simplify(0.05)
    print(k,x,round(pg.area,1),len(pg.exterior.coords))
    print([tuple(round(v,2) for v in c) for c in pg.exterior.coords])
