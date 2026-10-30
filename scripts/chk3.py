import pickle
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb'))
for k in ('placa_A','placa_B','verde_central','verde_braco_T'):
    ps=RL[k].split(only_watertight=False); print(k,[ (round(p.volume,1),[round(v,1) for v in p.bounds.ravel()]) for p in ps])
p=RL['placa_A']
for x in (283.75,283.5,283.0,282.0,281.0,280.9):
    s=section_polys(p,'x',x); print(x, round(s.area,1))
