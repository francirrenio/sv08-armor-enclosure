import pickle,numpy as np
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
xs=np.arange(279.0,284.0,0.02)
for nm,p in (('A',RL['placa_A']),('B',RL['placa_B']),('EB',CT['E_placa_B'])):
  for (y,z) in ((37,-50),(37,-150),(15,-150),(37,50),(37,150)):
    c=p.contains(np.c_[xs,np.full_like(xs,y),np.full_like(xs,z)])
    print(nm,y,z,[round(xs[i],2) for i in np.flatnonzero(np.diff(c.astype(int)))])
print([k for k in CT if k.startswith('R_')])
