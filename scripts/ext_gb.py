# verde e azul (espinha) sobem ~15 mm sobre a frente da banda do topo (Y 523 -> 538); a banda recua so nesse trecho
import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import box
from shapely.ops import unary_union as uu
CT=pickle.load(open('CT_before_ext.pkl','rb')); TL=pickle.load(open('TL.pkl','rb'))
def sy(m,y):
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float)); return uu([p for p in p2.polygons_full])
def pxz(poly,y0,y1):
    gs=[g for g in (poly.geoms if hasattr(poly,'geoms') else [poly]) if g.area>0.5]; ms=[]
    for g in gs:
        m=trimesh.creation.extrude_polygon(g,y1-y0); m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
        if m.volume<0: m.invert()
        ms.append(m)
    return ms[0] if len(ms)==1 else U(*ms)
for y in (521.0,521.5,522.0,522.3,522.6):
    print(y, np.round(sy(CT['verde_sup'],y).bounds,1).tolist(), np.round(sy(CT['espinha'],y).bounds,1).tolist())
YA,YB=521.0,538.0
gv=sy(CT['verde_sup'],520.0).intersection(box(279.0,200,290,252.5))
ge=sy(CT['espinha'],520.0).intersection(box(270.0,200,290,251.5))
vs=U(CT['verde_sup'],pxz(gv,YA,YB))
es=U(CT['espinha'],pxz(ge,YA,YB))
bd=D(TL['bandaB'],B(279.0,290.0,YA-1,YB+0.2,min(gv.bounds[1],ge.bounds[1])-0.2,300))   # sem fio de banda entre a verde e a azul
bd=max(bd.split(only_watertight=False),key=lambda p:p.volume)
chk={'vs_es':I(vs,es).volume,'vs_bd':I(vs,bd).volume,'es_bd':I(es,bd).volume,'vs_cap':I(vs,CT['cant_top_F']).volume,'es_cap':I(es,CT['cant_top_F']).volume}
for pid,lab,grp,m in pickle.load(open('parts.pkl','rb')):
    if grp=='atual' or pid in ('esp1','vsup1','bandaB','thCantF','base','perfil'): continue
    b=m.bounds
    if b[1][0]<270 or b[0][1]>540 or b[1][1]<519 or b[0][2]>253 or b[1][2]<218: continue
    for k,x in (('vs',vs),('es',es)):
        try: v=I(x,m).volume
        except Exception: v=-1
        if abs(v)>0.01: chk[k+'_'+pid]=v
print(json.dumps({k:round(float(v),2) for k,v in chk.items()}), vs.is_volume, es.is_volume, bd.is_volume, np.round(bd.bounds,1).tolist())
CT['verde_sup']=vs; CT['espinha']=es; CT['bandaB']=bd
pickle.dump(CT,open('CT.pkl','wb'))
