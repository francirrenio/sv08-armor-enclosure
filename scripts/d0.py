import pickle,numpy as np
exec(open('geo.py').read())
from shapely.geometry import Polygon
CT=pickle.load(open('CT.pkl','rb')); RL=pickle.load(open('RL.pkl','rb'))
A=pickle.load(open('../as03/as03_contornos_D.pkl','rb'))
for k,v in A.items(): print(k,[round(b,1) for b in v.bounds])
m=CT['E_moldura_conector']; print('mold',m.bounds.round(2).tolist())
s=section_polys(m,'x',282.0); print('mold sec',s.geom_type,[round(b,1) for b in s.bounds])
p=CT['R_E_placa_B']; print('placa',p.bounds.round(1).tolist())
for k in ('verde_lat_F_sup','verde_braco_F','verde_lat_F_inf'):
    print(k,RL[k].bounds.round(1).tolist())
