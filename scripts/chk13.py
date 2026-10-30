import pickle,numpy as np
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
zs=np.arange(70,100,0.02)
for nm,p in (('B',RL['placa_B']),('EB',CT['E_placa_B']),('EBnew',CT['R_E_placa_B']),('Bnew',CT['R_placa_B'])):
  for y in (18.0,30.0,37.0):
    for x in (282.0,283.0,283.6):
      c=p.contains(np.c_[np.full_like(zs,x),np.full_like(zs,y),zs])
      print(nm,y,x,[round(zs[i],2) for i in np.flatnonzero(np.diff(c.astype(int)))])
