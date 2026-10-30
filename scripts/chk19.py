import pickle,numpy as np
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb'))
for k in ('verde_central','verde_braco_T','verde_braco_F'):
  m=RL[k]
  for x in (281.0,282.3,283.0,283.5,283.75):
    s=section_polys(m,'x',x); gs=s.geoms if hasattr(s,'geoms') else [s]
    print(k,x,[[round(Polygon(r).area,2) for r in g.interiors] for g in gs])
