import pickle,trimesh
exec(open('geo.py').read())
CT=pickle.load(open('CT.pkl','rb'))
a=CT['riser47_aletas']
for p in a.split(only_watertight=False): print(p.bounds.round(2).tolist(), round(p.volume,1))
s=section_polys(a,'z',120.0); gs=s.geoms if hasattr(s,'geoms') else [s]
for g in gs: print([tuple(round(c,2) for c in v) for v in g.exterior.coords])
m=CT['riser47_mold']; print('mold',m.bounds.round(2).tolist())
