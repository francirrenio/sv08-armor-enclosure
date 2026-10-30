import pickle,numpy as np,trimesh
exec(open('geo.py').read())
T='../ltop/'
c=trimesh.load(T+'053_fix.stl');CF=pickle.load(open('CF.pkl','rb'))
print('cap',np.round(c.bounds,1).tolist(), c.is_volume)
for k in ('espinha','verde_sup'):
    i=I(c,CF[k]); print(k,round(i.volume,1),np.round(i.bounds,1).tolist() if i.volume>0 else '')
for y in (530,545,560):
    s=section_polys(c,'y',y); print(y, s.geom_type, np.round(s.bounds,1).tolist())
s=section_polys(CF['verde_sup'],'y',545); print('vs545',np.round(s.bounds,1).tolist(), s.area)
