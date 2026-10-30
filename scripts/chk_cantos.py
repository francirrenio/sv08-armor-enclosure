import pickle,json
exec(open('geo.py').read())
RL=pickle.load(open('RL.pkl','rb')); CT=pickle.load(open('CT.pkl','rb'))
for k in ('verde_central','verde_braco_T','verde_braco_F','placa_A','placa_B'):
    a=RL[k]; b=CT['R_'+k]
    print(k, round(a.volume,1), round(b.volume,1), [list(map(lambda v:round(v,1),r)) for r in a.bounds], [list(map(lambda v:round(v,1),r)) for r in b.bounds])
    for x in (281.0,282.5):
        for side,(m) in (('old',a),('new',b)):
            s=section_polys(m,'x',x); print('  ',side,x,round(s.area,1),len(s.geoms) if hasattr(s,'geoms') else 1)
