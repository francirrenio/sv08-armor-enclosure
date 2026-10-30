import pickle,numpy as np
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
for kp,old in (('placa_A',RL['placa_A']),('E_placa_B',CT['E_placa_B'])):
  new=CT['R_'+kp]
  for nm,d in (('perdeu',D(old,new)),('ganhou',D(new,old))):
    ps=[p for p in d.split(only_watertight=False) if abs(p.volume)>0.2]
    print(kp,nm,[(round(p.volume,2),[round(v,1) for v in p.bounds.ravel()]) for p in sorted(ps,key=lambda p:-p.volume)[:10]])
