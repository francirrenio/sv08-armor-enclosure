import numpy as np, pickle, trimesh, json
exec(open('geo.py').read())
from shapely.geometry import Polygon, box
from shapely import affinity as af
_G={}; exec(open('esb/geom_lat.py').read(),_G)
T='/tmp/claude-0/-home-claude/feeeb77d-0d0c-5101-9504-0705fb8bda2b/scratchpad/ltop/'
cap=trimesh.load(T+'053_fix.stl')
DY=521.0; XI,XO=284.0,293.3
lp=af.translate(_G['Lr'].intersection(box(190.0,2.0,255.0,47.0)),0,DY)   # perna + curva ate Y 568; para em Z 255 (nao cobre o furo do parafuso da cantoneira)
lp=lp.difference(box(247.7,0,300,531.0))                    # na ponta da aba a borda de baixo fica a da propria cantoneira     # mesma perna em L da cantoneira de baixo, sobre a banda (Y 523-555)
leg=prism_zy(lp,XI,XO); leg=chamfer_top(leg,'x',XO,5.5)
leg=I(leg,B(XI-1,XO+1,523.0,576.0,-262.0,262.0))
t=_G['rc'](Polygon([(229-7,17+DY-4.06),(229+7,17+DY-4.06),(229,17+DY+8.12)]),1.0)
leg=D(leg,prism_zy(t,XO-1.5,XO+1))
capL=U(cap,prism_zy(lp,XI,XO))
_s=section_polys(capL,'x',XO-0.05)
_s=max((_s.geoms if hasattr(_s,'geoms') else [_s]),key=lambda g:g.area)
capL=D(capL,chamfer_cutter(Polygon(_s.exterior),'x',XO,5.5,skip=lambda a,b: a[0]>247.6 and b[0]>247.6 and (a[1]>568.5 or b[1]>568.5)))      # chanfro so nas bordas da perna e na curva de dentro (as da cantoneira ficam como estao)
capL=D(capL,prism_zy(t,XO-1.5,XO+1))
TL=pickle.load(open('TL.pkl','rb')); CF=pickle.load(open('CF.pkl','rb')); FB=pickle.load(open('FB.pkl','rb'))
chk={k:round(I(leg,m).volume,2) for k,m in (('bandaB',TL['bandaB']),('bandaA',TL['bandaA']),('acab_sup',FB['acab_sup']),('espinha',CF['espinha']),('acr',TL['acrilico']))}
for f in ('035','047','027','028','029'):
    m=trimesh.load(T+f+'.stl')
    if m.is_volume: chk[f]=round(I(leg,m).volume,2)
print(json.dumps(chk), capL.is_volume, len(capL.split(only_watertight=False)), np.round(leg.bounds,1).tolist())
pickle.dump({'cant_top_F':capL},open('CT.pkl','wb'))
