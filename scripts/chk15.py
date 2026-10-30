import pickle,numpy as np
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'))
d=D(CT['R_E_placa_B'],CT['E_placa_B'])
ps=sorted(d.split(only_watertight=False),key=lambda p:-p.volume)
p=ps[0]; print(p.volume, p.bounds)
v=p.vertices; print(np.unique(np.round(v[:,0],2))[:20])
for zz in (80,100,150,200):
    sel=v[np.abs(v[:,2]-zz)<3]; 
    if len(sel): print(zz, sel[:,0].min().round(2), sel[:,0].max().round(2), sel[:,1].min().round(2), sel[:,1].max().round(2))
