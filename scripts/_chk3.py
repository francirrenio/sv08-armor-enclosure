import pickle,numpy as np,trimesh
exec(open('geo.py').read())
from shapely.geometry import box
CF=pickle.load(open('CF.pkl','rb'));TL=pickle.load(open('TL.pkl','rb'));FB=pickle.load(open('FB.pkl','rb'))
def sec_y(m,y):
    from shapely.ops import unary_union as uu
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    if s is None: return None
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return uu([p for p in p2.polygons_full])
for y in (540,549,550.5):
    s=sec_y(CF['verde_sup'],y); print('vs',y,round(s.area,1),np.round(s.bounds,1).tolist())
for y in (552,556):
  for k,m in (('esp',CF['espinha']),('bandaB',TL['bandaB']),('bandaA',TL['bandaA']),('acab_sup',FB['acab_sup'])):
    s=sec_y(m,y)
    if s is None or s.is_empty: print(y,k,'-'); continue
    s=s.intersection(box(235,215,290,290)); print(y,k,round(s.area,1),np.round(s.bounds,1).tolist() if not s.is_empty else '')
