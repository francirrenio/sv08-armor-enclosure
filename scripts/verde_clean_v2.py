# verde de cima com faces lisas: sem o recorte do fecho (Y 404-456), sem os furos sem uso (Z 266, Y 441/459; frente Y 535),
# sem os rebaixos da cantoneira de cima; parte de cima refeita com a secao limpa de Y 499.
# As outras pecas (cantoneira de cima, espinha, banda) e que recebem a folga de 0,2 da verde.
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon, box
from shapely.ops import unary_union as uu
CF=pickle.load(open('CF.pkl','rb')); CT=pickle.load(open('CT_after_ext.pkl','rb'))
def sy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
def pxz(poly,y0,y1):
    gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.5]; ms=[]
    for g in gs:
        m=trimesh.creation.extrude_polygon(Polygon(g.exterior),y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
        if m.volume<0: m.invert()
        ms.append(m)
    return ms[0] if len(ms)==1 else U(*ms)
g0=CF['verde_sup']
gA=I(g0,B(200,300,300,499.5,200,300))
s370=sy(g0,370.0); s499=sy(g0,499.0)
print('s370',np.round(s370.bounds,2).tolist(),'s499',np.round(s499.bounds,2).tolist())
fill=pxz(s370,398.0,462.0)                                   # tampa o recorte do fecho e os 2 furos sem uso
gB=pxz(s499,499.4,558.2)                                     # parte larga inteira ate o topo (Y 558,2), sem recorte
top=Polygon([(200,251.1),(281.8,251.1),(300,269.3),(300,300),(200,300)])
gC=pxz(s499.intersection(top),537.9,558.2)                   # acima da banda: so de Z 251,1 para a frente (chanfro 2 na aresta de tras)
vs=U(gA,fill,gB)
vs=max(vs.split(only_watertight=False),key=lambda p:p.volume)
gv=grow(vs,0.2)
es=D(CT['espinha'],gv); es=max(es.split(only_watertight=False),key=lambda p:p.volume)
bd=D(CT['bandaB'],gv); bd=max(bd.split(only_watertight=False),key=lambda p:p.volume)
cap=D(CT['cant_top_F'],gv); cap=max(cap.split(only_watertight=False),key=lambda p:p.volume)
chk={'vs_es':I(vs,es).volume,'vs_bd':I(vs,bd).volume,'vs_cap':I(vs,cap).volume,'es_cap':I(es,cap).volume,'cap_vol_change':CT['cant_top_F'].volume-cap.volume,'es_vol_change':CT['espinha'].volume-es.volume}
for pid,lab,grp,m in pickle.load(open('parts.pkl','rb')):
    if grp=='atual' or pid in ('esp1','vsup1','bandaB','thCantF','base','perfil'): continue
    b=m.bounds
    if not (b[0]<vs.bounds[1]).all() or not (b[1]>vs.bounds[0]).all(): continue
    try: v=I(vs,m).volume
    except Exception: v=-1
    if abs(v)>0.01: chk['vs_'+pid]=v
    if not (b[0]<cap.bounds[1]).all() or not (b[1]>cap.bounds[0]).all(): continue
for f in ('035','047'):
    m=trimesh.load('../ltop/'+f+'.stl'); chk['vs_'+f]=I(vs,m).volume
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}), vs.is_volume, es.is_volume, bd.is_volume, cap.is_volume, np.round(vs.bounds,1).tolist())
CT['verde_sup']=vs; CT['espinha']=es; CT['bandaB']=bd; CT['cant_top_F']=cap
pickle.dump(CT,open('CT.pkl','wb'))
