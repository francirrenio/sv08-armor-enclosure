import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon, box
T='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
cap=trimesh.load(T+'053_fix.stl')
# aba lateral esticada: corta a cantoneira original em Z 254 (secao constante), empurra a ponta 42,7 mm para tras
# e preenche com a mesma secao -> mesma ponta, mesmos chanfros e cantos da original
ZC,DZ=254.0,247.7-205.0
tipo=I(cap,B(200,300,500,650,0,ZC)); tipo.apply_translation([0,0,-DZ])
corpo=I(cap,B(200,300,500,650,ZC,320))
sec=Polygon([(288.14,633.6),(281.8,633.6),(281.8,551.0),(283.1,551.0),(283.8,550.3),(283.8,541.6),(284.0,541.6),(284.0,523.0),(288.14,523.0),(293.3,533.32),(293.3,623.28),(288.14,633.6)])
meio=prism_xy(sec,ZC-DZ-0.01,ZC+0.01)
capW=U(corpo,I(U(meio,tipo),B(284.2,300,500,650,0,320)))   # na parte esticada a face de dentro fica em X 284,2: passa 0,4 sobre a banda e 0,2 sobre o riser
TL=pickle.load(open('TL.pkl','rb'))
# chanfro de dentro da aba nova (lado da face X 284,2) nao precisa: fica encostada nas pecas
CF=pickle.load(open('CF.pkl','rb')); FB=pickle.load(open('FB.pkl','rb'))
chk={k:round(I(capW,m).volume,2) for k,m in (('bandaB',TL['bandaB']),('bandaA',TL['bandaA']),('acab_sup',FB['acab_sup']),('espinha',CF['espinha']),('verde_sup',CF['verde_sup']),('acr',TL['acrilico']),('faixa',TL['faixa_sup']))}
for f in ('035','047','043','027','028','029','056'):
    m=trimesh.load(T+f+'.stl')
    if m.is_volume: chk[f]=round(I(capW,m).volume,2)
print(json.dumps(chk), capW.is_volume, len(capW.split(only_watertight=False)), np.round(capW.bounds,1).tolist())
pickle.dump({'cant_top_F':capW},open('CT.pkl','wb'))
# verde de cima sobe ate Y 558,2 (encosta sob o riser do top hat), escondida sob a aba lateral nova
def sec_y(m,y):
    from shapely.ops import unary_union as uu
    s=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
    p2,T=s.to_2D(to_2D=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,-y],[0,0,0,1]],float))
    return uu([p for p in p2.polygons_full])
def prism_xz(poly,y0,y1):
    m=trimesh.creation.extrude_polygon(poly,y1-y0)
    m.apply_transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float))
    if m.volume<0: m.invert()
    return m
gp=sec_y(CF['verde_sup'],550.0)
vs=U(CF['verde_sup'],*[prism_xz(g,550.0,558.2) for g in (gp.geoms if hasattr(gp,'geoms') else [gp]) if g.area>0.5])
r35=trimesh.load(T+'035.stl'); r47=trimesh.load(T+'047.stl')
vs=D(vs,grow(capW,0.2),grow(CF['espinha'],0.2),grow(TL['bandaB'],0.2),*[grow(r,0.2) for r in (r35,r47) if r.is_volume])
esp=D(CF['espinha'],grow(capW,0.2))
vs=max(vs.split(only_watertight=False),key=lambda p:p.volume)
chk2={'vs_cap':I(vs,capW).volume,'vs_esp':I(vs,CF['espinha']).volume,'esp_cap':I(esp,capW).volume,'vs_parts':len(vs.split(only_watertight=False)),'esp_parts':len(esp.split(only_watertight=False))}
print(json.dumps({k:round(float(v),2) for k,v in chk2.items()}), np.round(vs.bounds,1).tolist(), vs.is_volume, esp.is_volume)
pickle.dump({'cant_top_F':capW,'verde_sup':vs,'espinha':esp},open('CT.pkl','wb'))
