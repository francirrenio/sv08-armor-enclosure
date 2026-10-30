import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import box, Polygon
from shapely.ops import unary_union as uu
CT=pickle.load(open('CT.pkl','rb')); TL=pickle.load(open('TL.pkl','rb')); FB=pickle.load(open('FB.pkl','rb'))
def sy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
s=sy(CT['espinha'],520.0).intersection(box(265,200,290,250.6)).simplify(0.03)
for g in (s.geoms if hasattr(s,'geoms') else [s]): print('sec520',np.round(np.array(g.exterior.coords),2).tolist())
P={pid:m for pid,lab,grp,m in pickle.load(open('parts.pkl','rb'))}
E=B(273.0,283.8,520,622,220.1,250.2)
for k,m in [('fbS',FB['faixa_batente_sup']),('apB',TL['apoio_B']),('apHW',TL['apoio_hw']),('acr',TL['acrilico']),('acab_sup',FB['acab_sup']),('vs',CT['verde_sup']),('band',CT['bandaB']),('cap',CT['cant_top_F'])]+[(f,trimesh.load('../ltop/'+f+'.stl')) for f in ('035','047','050','052','055','060','062','064','068')]:
    try: i=I(E,m); print(k,round(i.volume,1),np.round(i.bounds,1).tolist() if i.volume>0 else '')
    except Exception as e: print(k,'err',e)
