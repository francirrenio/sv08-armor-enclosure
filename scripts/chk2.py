import pickle
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
for k in ('placa_A','placa_B'):
  for x in (281.0,282.5,283.5):
    a=section_polys(RL[k],'x',x); b=section_polys(CT['R_'+k],'x',x)
    for nm,d in (('perdeu',a.difference(b)),('ganhou',b.difference(a))):
        gs=[g for g in (d.geoms if hasattr(d,'geoms') else [d]) if g.area>1]
        print(k,x,nm,[(round(g.area,1),[round(v,1) for v in g.bounds]) for g in gs])
for x in (281.0,281.3,282.0):
    s=section_polys(CT['R_verde_braco_T'],'x',x); print('bT',x,round(s.area,1),[round(v,1) for v in s.bounds])
