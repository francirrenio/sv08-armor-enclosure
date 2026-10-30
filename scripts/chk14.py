import pickle,numpy as np
exec(open('geo.py').read())
from shapely.ops import unary_union
PG,PN=pickle.load(open('cv2d.pkl','rb'))
for k in ('verde_central','verde_braco_T'):
    d=PG[k].symmetric_difference(PN[k]).buffer(-0.05).buffer(0.05)
    gs=d.geoms if hasattr(d,'geoms') else [d]
    print(k,[(round(g.area,2),[round(v,1) for v in g.bounds]) for g in gs])
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
ys=np.arange(3,10,0.02)
for nm,p,z in (('A',RL['placa_A'],-40),('EB',CT['E_placa_B'],40),('B',RL['placa_B'],40)):
  for x in (282.0,283.0,283.5):
    c=p.contains(np.c_[np.full_like(ys,x),ys,np.full_like(ys,z)]); print(nm,x,[round(ys[i],2) for i in np.flatnonzero(np.diff(c.astype(int)))])
ys=np.arange(40,70,0.02)
for nm,p in (('EB',CT['E_placa_B']),('EBn',CT['R_E_placa_B']),('B',RL['placa_B'])):
  for x in (282.0,283.0,283.5):
    c=p.contains(np.c_[np.full_like(ys,x),ys,np.full_like(ys,150)]); print(nm,'z150',x,[round(ys[i],2) for i in np.flatnonzero(np.diff(c.astype(int)))])
