# espinha: a parte larga da perna lateral (Z 220,1-250,2, com a aba de fora) sobe ate o topo da espinha (Y 622)
# a banda termina antes dela; o riser lateral (047) fica por fora e e recortado por dentro para encaixar na perna (folga 0,1); a verde tem prioridade (folga 0,2)
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import box
from shapely.ops import unary_union as uu
CT=pickle.load(open('CT.pkl','rb'))
def sy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
def pxz(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
s=sy(CT['espinha'],520.0).intersection(box(265,200,290,250.6))
s=max((s.geoms if hasattr(s,'geoms') else [s]),key=lambda g:g.area)
perna=s.intersection(box(265,200,279.6,300)); aba=s.intersection(box(279.6,200,290,300))
E1=U(pxz(perna,519.5,622.0),pxz(aba,519.5,558.25))   # perna sobe ate o topo; a aba de fora so ate o riser
E2=B(279.6,283.8,538.2,558.25,220.1,250.2)            # no trecho da banda ocupa ate a face de fora; acima disso o riser cobre por fora
es=U(CT['espinha'],E1)   # a verde cobre por fora ate o topo: a espinha fica so por tras
es=D(es,grow(CT['verde_sup'],0.2))
es=max(es.split(only_watertight=False),key=lambda p:p.volume)
ge=grow(es,0.1)
bd=D(CT['bandaB'],ge,B(270,290,500,600,219.9,300));   # ponta da banda reta em Z 219,9 (sem a lamina sobre a espinha)
pb=bd.split(only_watertight=False); bd=max(pb,key=lambda p:p.volume)
r47=trimesh.load('../ltop/047.stl'); r47n=D(r47,ge); pr=r47n.split(only_watertight=False); r47n=max(pr,key=lambda p:p.volume)
chk={'es_vs':I(es,CT['verde_sup']).volume,'es_bd':I(es,bd).volume,'es_r47':I(es,r47n).volume,'es_cap':I(es,CT['cant_top_F']).volume,
     'bd_parts':len(pb),'r47_parts':len(pr),'r47_dv':r47.volume-r47n.volume}
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}), es.is_volume, bd.is_volume, r47n.is_volume, np.round(es.bounds,1).tolist(), np.round(r47n.bounds,1).tolist())
CT['espinha']=es; CT['bandaB']=bd; CT['riser47']=r47n
pickle.dump(CT,open('CT.pkl','wb'))
