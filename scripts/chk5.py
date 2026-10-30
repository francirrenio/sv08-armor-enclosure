import pickle,numpy as np
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
for k in ('placa_A','placa_B','verde_central','verde_braco_T'):
    a=RL[k]; b=CT['R_'+k]
    for nm,d in (('perdeu',D(a,b)),('ganhou',D(b,a))):
        ps=[p for p in d.split(only_watertight=False) if abs(p.volume)>0.3]
        print(k,nm,round(d.volume,1),[(round(p.volume,1),[round(v,1) for v in p.bounds.ravel()]) for p in sorted(ps,key=lambda p:-p.volume)[:8]])
